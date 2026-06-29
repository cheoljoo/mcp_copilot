"""
vcs_collector.py
=================
Gerrit / GitHub(git) / GitLab 서버에서 커밋·리뷰 활동을 취합하는 모듈.

지원 소스:
  - Gerrit  REST API  (Change 목록, Review comments, Reviewer actions)
  - GitHub  REST API  (Commits, PR reviews, PR comments)
  - GitLab  REST API  (Commits, Merge-request reviews, notes)
  - Local git repo    (git log 직접 파싱)

사용법:
  python vcs_collector.py \
      --gerrit-host http://gerrit.example.com \
      --gerrit-user alice \
      --gerrit-password PASSWORD \
      --github-token ghp_TOKEN \
      --github-org my-org \
      --gitlab-host https://gitlab.example.com \
      --gitlab-token TOKEN \
      --users alice bob charlie \
      --since 2026-06-01 \
      --output vcs_report.json
"""

import argparse
import json
import logging
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List, Optional

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------

@dataclass
class VcsActivity:
    source: str        # "gerrit" | "github" | "gitlab" | "git-local"
    user: str
    date: str          # YYYY-MM-DD
    activity_type: str # "commit" | "review" | "comment" | "approve" | "reject"
    repo: str
    change_id: str     # commit hash / change-id / MR iid / PR number
    summary: str       # first line of commit message or title
    detail: str


# ---------------------------------------------------------------------------
# HTTP helper (reusable)
# ---------------------------------------------------------------------------

class RestClient:
    def __init__(self, base_url: str, token: Optional[str] = None,
                 user: Optional[str] = None, password: Optional[str] = None,
                 verify_ssl: bool = True, digest_auth: bool = False):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.verify_ssl = verify_ssl
        if token:
            self.session.headers["Authorization"] = f"Bearer {token}"
        elif user and password:
            auth = HTTPDigestAuth(user, password) if digest_auth else HTTPBasicAuth(user, password)
            self.session.auth = auth

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, verify=self.verify_ssl, timeout=30)
        resp.raise_for_status()
        # Gerrit prepends ")]}'\n" to XSSI-protect
        text = resp.text
        if text.startswith(")]}'"):
            text = text[text.index("\n") + 1:]
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return resp.json()


# ---------------------------------------------------------------------------
# Gerrit collector
# ---------------------------------------------------------------------------

class GerritCollector:
    """Collect Gerrit changes + review comments for a list of users."""

    def __init__(self, client: RestClient, users: List[str], since: datetime):
        self.client = client
        self.users = set(users)
        self.since = since

    def collect(self) -> List[VcsActivity]:
        activities: List[VcsActivity] = []
        since_str = self.since.strftime("%Y-%m-%d")

        for user in self.users:
            # Changes authored by user
            query = f"owner:{user} after:{since_str}"
            try:
                changes = self._paginate_changes(query)
                for ch in changes:
                    date = (ch.get("updated", "") or ch.get("created", ""))[:10]
                    activities.append(VcsActivity(
                        source="gerrit", user=user, date=date,
                        activity_type="commit",
                        repo=ch.get("project", ""),
                        change_id=ch.get("change_id", ch.get("_number", "")),
                        summary=ch.get("subject", ""),
                        detail=f"Status: {ch.get('status','?')}, Branch: {ch.get('branch','?')}"
                    ))
            except requests.HTTPError as exc:
                log.warning("Gerrit author query failed for %s: %s", user, exc)

            # Changes reviewed by user
            query_review = f"reviewer:{user} after:{since_str}"
            try:
                for ch in self._paginate_changes(query_review):
                    date = (ch.get("updated", ""))[:10]
                    score = self._get_user_vote(ch, user)
                    activities.append(VcsActivity(
                        source="gerrit", user=user, date=date,
                        activity_type="review",
                        repo=ch.get("project", ""),
                        change_id=ch.get("change_id", ch.get("_number", "")),
                        summary=ch.get("subject", ""),
                        detail=f"Code-Review vote: {score}, Status: {ch.get('status','?')}"
                    ))
            except requests.HTTPError as exc:
                log.warning("Gerrit reviewer query failed for %s: %s", user, exc)

        return activities

    def _paginate_changes(self, query: str) -> List[Dict]:
        results = []
        start = 0
        while True:
            params = {
                "q": query,
                "o": "DETAILED_ACCOUNTS,LABELS",
                "S": start,
                "n": 100,
            }
            batch = self.client.get("/a/changes/", params)
            if not isinstance(batch, list):
                break
            results.extend(batch)
            if not batch or not batch[-1].get("_more_changes"):
                break
            start += len(batch)
        return results

    def _get_user_vote(self, change: Dict, user: str) -> str:
        labels = change.get("labels", {}).get("Code-Review", {})
        for voter in labels.get("all", []):
            if voter.get("username") == user or voter.get("email", "").startswith(user):
                return str(voter.get("value", "0"))
        return "?"


# ---------------------------------------------------------------------------
# GitHub collector
# ---------------------------------------------------------------------------

class GitHubCollector:
    """Collect GitHub commits + PR reviews for specified users in an org."""

    BASE = "https://api.github.com"

    def __init__(self, token: str, org: str, users: List[str], since: datetime,
                 repos: Optional[List[str]] = None):
        self.client = RestClient(self.BASE, token=token)
        self.client.session.headers["Accept"] = "application/vnd.github+json"
        self.client.session.headers["X-GitHub-Api-Version"] = "2022-11-28"
        self.org = org
        self.users = set(users)
        self.since = since
        self.repos = repos  # None = all org repos

    def collect(self) -> List[VcsActivity]:
        activities: List[VcsActivity] = []
        repo_list = self.repos or self._list_repos()

        for repo in repo_list:
            log.info("GitHub: scanning repo %s/%s", self.org, repo)
            activities.extend(self._collect_commits(repo))
            activities.extend(self._collect_pr_reviews(repo))

        return activities

    def _list_repos(self) -> List[str]:
        repos = []
        page = 1
        while True:
            data = self.client.get(f"/orgs/{self.org}/repos",
                                   {"per_page": 100, "page": page, "type": "all"})
            if not data:
                break
            repos.extend(r["name"] for r in data)
            page += 1
            if len(data) < 100:
                break
        return repos

    def _collect_commits(self, repo: str) -> List[VcsActivity]:
        acts = []
        since_iso = self.since.isoformat()
        for user in self.users:
            page = 1
            while True:
                try:
                    commits = self.client.get(
                        f"/repos/{self.org}/{repo}/commits",
                        {"author": user, "since": since_iso,
                         "per_page": 100, "page": page}
                    )
                except requests.HTTPError:
                    break
                if not commits:
                    break
                for c in commits:
                    date = (c.get("commit", {}).get("author", {}).get("date", ""))[:10]
                    msg = (c.get("commit", {}).get("message", "")).split("\n")[0]
                    acts.append(VcsActivity(
                        source="github", user=user, date=date,
                        activity_type="commit",
                        repo=f"{self.org}/{repo}",
                        change_id=c.get("sha", "")[:8],
                        summary=msg,
                        detail=c.get("html_url", "")
                    ))
                page += 1
                if len(commits) < 100:
                    break
        return acts

    def _collect_pr_reviews(self, repo: str) -> List[VcsActivity]:
        acts = []
        # list PRs updated since
        page = 1
        since_iso = self.since.isoformat()
        while True:
            try:
                prs = self.client.get(
                    f"/repos/{self.org}/{repo}/pulls",
                    {"state": "all", "sort": "updated", "direction": "desc",
                     "per_page": 50, "page": page}
                )
            except requests.HTTPError:
                break
            if not prs:
                break
            stop = False
            for pr in prs:
                if pr.get("updated_at", "") < since_iso:
                    stop = True
                    break
                pr_number = pr["number"]
                pr_title = pr.get("title", "")
                try:
                    reviews = self.client.get(
                        f"/repos/{self.org}/{repo}/pulls/{pr_number}/reviews"
                    )
                except requests.HTTPError:
                    continue
                for rv in reviews:
                    reviewer = (rv.get("user") or {}).get("login", "")
                    submitted = (rv.get("submitted_at") or "")[:10]
                    if reviewer in self.users and submitted >= self.since.strftime("%Y-%m-%d"):
                        acts.append(VcsActivity(
                            source="github", user=reviewer, date=submitted,
                            activity_type="review",
                            repo=f"{self.org}/{repo}",
                            change_id=str(pr_number),
                            summary=pr_title,
                            detail=f"State: {rv.get('state','?')}"
                        ))
            page += 1
            if len(prs) < 50 or stop:
                break
        return acts


# ---------------------------------------------------------------------------
# GitLab collector
# ---------------------------------------------------------------------------

class GitLabCollector:
    """Collect GitLab commits + MR reviews for specified users."""

    def __init__(self, client: RestClient, users: List[str], since: datetime,
                 group: Optional[str] = None, projects: Optional[List[str]] = None):
        self.client = client
        self.users = set(users)
        self.since = since
        self.group = group
        self.projects = projects  # list of "namespace/project" slugs

    def collect(self) -> List[VcsActivity]:
        activities: List[VcsActivity] = []
        project_ids = self.projects or self._list_group_projects()

        for proj in project_ids:
            log.info("GitLab: scanning project %s", proj)
            activities.extend(self._collect_commits(proj))
            activities.extend(self._collect_mr_notes(proj))

        return activities

    def _list_group_projects(self) -> List[str]:
        if not self.group:
            return []
        projects = []
        page = 1
        while True:
            data = self.client.get(
                f"/api/v4/groups/{self.group}/projects",
                {"per_page": 100, "page": page, "include_subgroups": "true"}
            )
            if not data:
                break
            projects.extend(str(p["id"]) for p in data)
            page += 1
            if len(data) < 100:
                break
        return projects

    def _collect_commits(self, project_id: str) -> List[VcsActivity]:
        acts = []
        since_iso = self.since.isoformat()
        page = 1
        while True:
            try:
                commits = self.client.get(
                    f"/api/v4/projects/{project_id}/repository/commits",
                    {"since": since_iso, "per_page": 100, "page": page, "all": "true"}
                )
            except requests.HTTPError:
                break
            if not commits:
                break
            for c in commits:
                author = c.get("author_name", "") or c.get("committer_name", "")
                # match by display name or username
                matched_user = self._match_user(author, c.get("author_email", ""))
                if matched_user:
                    date = (c.get("authored_date") or c.get("committed_date", ""))[:10]
                    acts.append(VcsActivity(
                        source="gitlab", user=matched_user, date=date,
                        activity_type="commit",
                        repo=project_id,
                        change_id=(c.get("id") or "")[:8],
                        summary=(c.get("title") or c.get("message", "")).split("\n")[0],
                        detail=c.get("web_url", "")
                    ))
            page += 1
            if len(commits) < 100:
                break
        return acts

    def _collect_mr_notes(self, project_id: str) -> List[VcsActivity]:
        acts = []
        since_str = self.since.strftime("%Y-%m-%d")
        page = 1
        while True:
            try:
                mrs = self.client.get(
                    f"/api/v4/projects/{project_id}/merge_requests",
                    {"state": "all", "updated_after": self.since.isoformat(),
                     "per_page": 50, "page": page}
                )
            except requests.HTTPError:
                break
            if not mrs:
                break
            for mr in mrs:
                mr_iid = mr.get("iid")
                mr_title = mr.get("title", "")
                try:
                    notes = self.client.get(
                        f"/api/v4/projects/{project_id}/merge_requests/{mr_iid}/notes",
                        {"per_page": 100}
                    )
                except requests.HTTPError:
                    continue
                for note in notes:
                    author = (note.get("author") or {}).get("username", "")
                    created = (note.get("created_at") or "")[:10]
                    if author in self.users and created >= since_str:
                        body = (note.get("body") or "")[:120].replace("\n", " ")
                        acts.append(VcsActivity(
                            source="gitlab", user=author, date=created,
                            activity_type="review",
                            repo=project_id,
                            change_id=str(mr_iid),
                            summary=mr_title,
                            detail=body
                        ))
            page += 1
            if len(mrs) < 50:
                break
        return acts

    def _match_user(self, name: str, email: str) -> Optional[str]:
        """Try to match commit author name/email to our user list."""
        for u in self.users:
            if u.lower() in name.lower() or u.lower() in email.lower():
                return u
        return None


# ---------------------------------------------------------------------------
# Local git repo collector
# ---------------------------------------------------------------------------

class LocalGitCollector:
    """Parse local git repos via git log."""

    def __init__(self, repo_paths: List[str], users: List[str], since: datetime):
        self.repo_paths = repo_paths
        self.users = users
        self.since = since

    def collect(self) -> List[VcsActivity]:
        acts = []
        for path in self.repo_paths:
            log.info("git-local: scanning %s", path)
            acts.extend(self._collect_repo(path))
        return acts

    def _collect_repo(self, path: str) -> List[VcsActivity]:
        acts = []
        since_str = self.since.strftime("%Y-%m-%d")
        try:
            result = subprocess.run(
                ["git", "-C", path, "log",
                 f"--after={since_str}",
                 "--all",
                 "--format=%H\t%ae\t%an\t%ad\t%s",
                 "--date=short"],
                capture_output=True, text=True, timeout=60
            )
        except (subprocess.TimeoutExpired, FileNotFoundError) as exc:
            log.warning("git log failed for %s: %s", path, exc)
            return acts

        for line in result.stdout.splitlines():
            parts = line.split("\t", 4)
            if len(parts) < 5:
                continue
            sha, email, name, date, subject = parts
            matched_user = self._match(name, email)
            if matched_user:
                acts.append(VcsActivity(
                    source="git-local", user=matched_user, date=date,
                    activity_type="commit",
                    repo=path,
                    change_id=sha[:8],
                    summary=subject,
                    detail=f"email={email}"
                ))
        return acts

    def _match(self, name: str, email: str) -> Optional[str]:
        for u in self.users:
            if u.lower() in name.lower() or u.lower() in email.lower():
                return u
        return None


# ---------------------------------------------------------------------------
# Summary / reporting
# ---------------------------------------------------------------------------

def print_vcs_summary(activities: List[VcsActivity]) -> None:
    by_user: Dict[str, List[VcsActivity]] = {}
    for a in activities:
        by_user.setdefault(a.user, []).append(a)

    print("\n" + "=" * 70)
    print("VCS ACTIVITY SUMMARY")
    print("=" * 70)
    for user, acts in sorted(by_user.items()):
        commits = [a for a in acts if a.activity_type == "commit"]
        reviews = [a for a in acts if a.activity_type == "review"]
        print(f"\n[{user}]  커밋: {len(commits)}  리뷰: {len(reviews)}")
        for a in sorted(acts, key=lambda x: x.date):
            print(f"  {a.date}  [{a.source}/{a.activity_type}]  {a.repo}  {a.change_id}  {a.summary[:60]}")


def save_json(activities: List[VcsActivity], path: str) -> None:
    import json
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(a) for a in activities], f, ensure_ascii=False, indent=2)
    log.info("JSON 저장: %s", path)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="VCS (Gerrit/GitHub/GitLab/local-git) worklog collector")
    p.add_argument("--gerrit-host", default=None)
    p.add_argument("--gerrit-user", default=None)
    p.add_argument("--gerrit-password", default=None)
    p.add_argument("--github-token", default=None)
    p.add_argument("--github-org", default=None)
    p.add_argument("--github-repos", nargs="*", help="Specific repos (default: all org repos)")
    p.add_argument("--gitlab-host", default=None)
    p.add_argument("--gitlab-token", default=None)
    p.add_argument("--gitlab-group", default=None)
    p.add_argument("--gitlab-projects", nargs="*")
    p.add_argument("--git-local-paths", nargs="*", help="Local git repo paths")
    p.add_argument("--users", nargs="+", required=True)
    p.add_argument("--since", default="2026-06-01")
    p.add_argument("--output", default="vcs_report.json")
    p.add_argument("--no-ssl-verify", action="store_true")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    verify = not args.no_ssl_verify
    all_activities: List[VcsActivity] = []

    # Gerrit
    if args.gerrit_host and args.gerrit_user and args.gerrit_password:
        client = RestClient(args.gerrit_host, user=args.gerrit_user,
                            password=args.gerrit_password, verify_ssl=verify,
                            digest_auth=True)
        gc = GerritCollector(client, args.users, since)
        acts = gc.collect()
        log.info("Gerrit: %d activities", len(acts))
        all_activities.extend(acts)

    # GitHub
    if args.github_token and args.github_org:
        ghc = GitHubCollector(args.github_token, args.github_org,
                              args.users, since, repos=args.github_repos)
        acts = ghc.collect()
        log.info("GitHub: %d activities", len(acts))
        all_activities.extend(acts)

    # GitLab
    if args.gitlab_host and args.gitlab_token:
        client = RestClient(args.gitlab_host, token=args.gitlab_token, verify_ssl=verify)
        glc = GitLabCollector(client, args.users, since,
                              group=args.gitlab_group, projects=args.gitlab_projects)
        acts = glc.collect()
        log.info("GitLab: %d activities", len(acts))
        all_activities.extend(acts)

    # Local git
    if args.git_local_paths:
        lgc = LocalGitCollector(args.git_local_paths, args.users, since)
        acts = lgc.collect()
        log.info("git-local: %d activities", len(acts))
        all_activities.extend(acts)

    print_vcs_summary(all_activities)
    save_json(all_activities, args.output)


if __name__ == "__main__":
    main()
