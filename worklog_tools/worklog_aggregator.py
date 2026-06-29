"""
worklog_aggregator.py
======================
Jira/Confluence + Gerrit/GitHub/GitLab 활동을 하나로 합쳐
사람별 일자별 Worklog 리포트를 생성한다.

출력:
  - 콘솔 요약 (사람별 날짜별 활동 목록)
  - JSON: 전체 raw 활동 데이터
  - Markdown: 사람별 worklog 리포트 (Jira Worklog 삽입 포맷 호환)
  - CSV: 피벗 분석용

사용 예:
  python worklog_aggregator.py \
      --jira-host http://jira.example.com --jira-token TOKEN \
      --confluence-host http://conf.example.com --confluence-token TOKEN \
      --gerrit-host http://gerrit.example.com \
      --gerrit-user me --gerrit-password PWD \
      --users alice bob charlie \
      --since 2026-06-01 \
      --output-dir ./reports
"""

import argparse
import csv
import json
import logging
import os
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

# Internal modules (same directory)
try:
    from jira_confluence_collector import (
        Activity, JiraCollector, ConfluenceCollector, RestClient as JiraRestClient
    )
    from vcs_collector import (
        VcsActivity, GerritCollector, GitHubCollector, GitLabCollector,
        LocalGitCollector, RestClient as VcsRestClient
    )
except ImportError as e:
    print(f"[ERROR] Could not import sub-modules: {e}")
    print("Make sure jira_confluence_collector.py and vcs_collector.py are in the same directory.")
    raise

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Unified event model
# ---------------------------------------------------------------------------

@dataclass
class WorklogEntry:
    user: str
    date: str            # YYYY-MM-DD
    source: str          # jira / confluence / gerrit / github / gitlab / git-local
    activity_type: str   # commit / review / comment / changelog / assignee / reporter / edit
    ref: str             # issue key / change-id / PR number
    title: str           # summary / subject
    detail: str
    duration_min: int = 0   # optional: estimated minutes (0 = unknown)


def from_jira_activity(a: Activity) -> WorklogEntry:
    return WorklogEntry(
        user=a.user, date=a.date, source=a.source,
        activity_type=a.activity_type,
        ref=a.item_key, title=a.item_summary, detail=a.detail
    )


def from_vcs_activity(a: VcsActivity) -> WorklogEntry:
    return WorklogEntry(
        user=a.user, date=a.date, source=a.source,
        activity_type=a.activity_type,
        ref=f"{a.repo}#{a.change_id}", title=a.summary, detail=a.detail
    )


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------

def compute_stats(entries: List[WorklogEntry]) -> Dict[str, Any]:
    """Return per-user statistics dict."""
    stats: Dict[str, Any] = {}
    by_user: Dict[str, List[WorklogEntry]] = defaultdict(list)
    for e in entries:
        by_user[e.user].append(e)

    for user, acts in by_user.items():
        dates = sorted({a.date for a in acts})
        type_counts: Dict[str, int] = defaultdict(int)
        for a in acts:
            type_counts[a.activity_type] += 1

        stats[user] = {
            "total_activities": len(acts),
            "active_days": len(dates),
            "first_activity": dates[0] if dates else "",
            "last_activity": dates[-1] if dates else "",
            "by_type": dict(type_counts),
            "by_source": dict(Counter(a.source for a in acts)),
        }
    return stats


try:
    from collections import Counter
except ImportError:
    pass  # already available in stdlib


def compute_stats(entries: List[WorklogEntry]) -> Dict[str, Any]:
    from collections import Counter
    stats: Dict[str, Any] = {}
    by_user: Dict[str, List[WorklogEntry]] = defaultdict(list)
    for e in entries:
        by_user[e.user].append(e)

    for user, acts in by_user.items():
        dates = sorted({a.date for a in acts})
        stats[user] = {
            "total_activities": len(acts),
            "active_days": len(dates),
            "first_activity": dates[0] if dates else "",
            "last_activity": dates[-1] if dates else "",
            "by_type": dict(Counter(a.activity_type for a in acts)),
            "by_source": dict(Counter(a.source for a in acts)),
        }
    return stats


# ---------------------------------------------------------------------------
# Report generators
# ---------------------------------------------------------------------------

def save_json_report(entries: List[WorklogEntry], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
    log.info("JSON saved: %s", path)


def save_csv_report(entries: List[WorklogEntry], path: str) -> None:
    if not entries:
        return
    fields = list(asdict(entries[0]).keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(asdict(e) for e in entries)
    log.info("CSV saved: %s", path)


def save_markdown_report(entries: List[WorklogEntry], stats: Dict, output_dir: str) -> None:
    """One Markdown file per user."""
    by_user: Dict[str, List[WorklogEntry]] = defaultdict(list)
    for e in entries:
        by_user[e.user].append(e)

    os.makedirs(output_dir, exist_ok=True)

    for user, acts in sorted(by_user.items()):
        path = os.path.join(output_dir, f"worklog_{user}.md")
        by_date: Dict[str, List[WorklogEntry]] = defaultdict(list)
        for a in acts:
            by_date[a.date].append(a)

        user_stats = stats.get(user, {})
        lines = [
            f"# Worklog: {user}",
            "",
            f"- 전체 활동: **{user_stats.get('total_activities', 0)}건**",
            f"- 활동 일수: **{user_stats.get('active_days', 0)}일**",
            f"- 기간: {user_stats.get('first_activity', '')} ~ {user_stats.get('last_activity', '')}",
            "",
            "## 활동 유형별 집계",
            "",
        ]
        for t, cnt in sorted((user_stats.get("by_type") or {}).items()):
            lines.append(f"- {t}: {cnt}건")
        lines.append("")
        lines.append("## 소스별 집계")
        lines.append("")
        for s, cnt in sorted((user_stats.get("by_source") or {}).items()):
            lines.append(f"- {s}: {cnt}건")
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 날짜별 상세 활동")
        lines.append("")

        for date in sorted(by_date.keys()):
            day_acts = by_date[date]
            lines.append(f"### {date}  ({len(day_acts)}건)")
            lines.append("")
            lines.append("| 소스 | 유형 | 참조 | 제목 | 상세 |")
            lines.append("|------|------|------|------|------|")
            for a in sorted(day_acts, key=lambda x: x.source):
                detail_short = (a.detail or "")[:80].replace("|", "\\|")
                title_short = (a.title or "")[:60].replace("|", "\\|")
                lines.append(f"| {a.source} | {a.activity_type} | {a.ref} | {title_short} | {detail_short} |")
            lines.append("")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        log.info("Markdown saved: %s", path)


def print_console_summary(entries: List[WorklogEntry], stats: Dict) -> None:
    print("\n" + "=" * 72)
    print("  UNIFIED WORKLOG REPORT")
    print("=" * 72)
    for user, s in sorted(stats.items()):
        print(f"\n{'─'*60}")
        print(f" 사용자: {user}")
        print(f"  활동 총계: {s['total_activities']}건  |  활동일: {s['active_days']}일")
        print(f"  기간: {s['first_activity']} ~ {s['last_activity']}")
        print(f"  유형별: {s['by_type']}")
        print(f"  소스별: {s['by_source']}")
    print("\n" + "=" * 72)


# ---------------------------------------------------------------------------
# Jira Worklog auto-insert helper
# ---------------------------------------------------------------------------

def insert_jira_worklog(jira_client: JiraRestClient,
                        entries: List[WorklogEntry],
                        time_per_entry_seconds: int = 1800) -> None:
    """
    각 WorklogEntry를 해당 Jira 이슈의 worklog에 자동 삽입한다.
    (실제 실행 전에 --dry-run 플래그 확인 권장)

    time_per_entry_seconds: 활동 1건당 추정 소요 시간(초), 기본 30분
    """
    jira_entries = [e for e in entries if e.source == "jira"]
    for e in jira_entries:
        issue_key = e.ref
        started_dt = datetime.strptime(e.date, "%Y-%m-%d").replace(
            hour=9, minute=0, second=0, tzinfo=timezone.utc
        )
        payload = {
            "comment": f"[Auto-worklog] {e.activity_type}: {e.detail[:255]}",
            "started": started_dt.strftime("%Y-%m-%dT%H:%M:%S.000+0000"),
            "timeSpentSeconds": time_per_entry_seconds,
        }
        try:
            jira_client.session.post(
                f"{jira_client.base_url}/rest/api/latest/issue/{issue_key}/worklog",
                json=payload,
                verify=jira_client.verify_ssl,
                timeout=30
            ).raise_for_status()
            log.info("Worklog inserted: %s  (%s)", issue_key, e.activity_type)
        except Exception as exc:
            log.warning("Worklog insert failed for %s: %s", issue_key, exc)


# ---------------------------------------------------------------------------
# Main orchestrator
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Unified worklog aggregator")
    # Jira
    p.add_argument("--jira-host", default=None)
    p.add_argument("--jira-token", default=None)
    # Confluence
    p.add_argument("--confluence-host", default=None)
    p.add_argument("--confluence-token", default=None)
    # Gerrit
    p.add_argument("--gerrit-host", default=None)
    p.add_argument("--gerrit-user", default=None)
    p.add_argument("--gerrit-password", default=None)
    # GitHub
    p.add_argument("--github-token", default=None)
    p.add_argument("--github-org", default=None)
    p.add_argument("--github-repos", nargs="*")
    # GitLab
    p.add_argument("--gitlab-host", default=None)
    p.add_argument("--gitlab-token", default=None)
    p.add_argument("--gitlab-group", default=None)
    p.add_argument("--gitlab-projects", nargs="*")
    # Local git
    p.add_argument("--git-local-paths", nargs="*")
    # Common
    p.add_argument("--users", nargs="+", required=True)
    p.add_argument("--since", default="2026-06-01")
    p.add_argument("--output-dir", default="./worklog_reports")
    p.add_argument("--no-ssl-verify", action="store_true")
    p.add_argument("--insert-jira-worklog", action="store_true",
                   help="자동으로 Jira worklog에 삽입 (주의: 실제 데이터 변경)")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    verify = not args.no_ssl_verify
    entries: List[WorklogEntry] = []

    # --- Jira ---
    jira_client: Optional[JiraRestClient] = None
    if args.jira_host and args.jira_token:
        jira_client = JiraRestClient(args.jira_host, args.jira_token, verify_ssl=verify)
        acts = JiraCollector(jira_client, args.users, since).collect()
        entries.extend(from_jira_activity(a) for a in acts)
        log.info("Jira: %d activities", len(acts))

    # --- Confluence ---
    if args.confluence_host and args.confluence_token:
        conf_client = JiraRestClient(args.confluence_host, args.confluence_token, verify_ssl=verify)
        acts = ConfluenceCollector(conf_client, args.users, since).collect()
        entries.extend(from_jira_activity(a) for a in acts)
        log.info("Confluence: %d activities", len(acts))

    # --- Gerrit ---
    if args.gerrit_host and args.gerrit_user and args.gerrit_password:
        gclient = VcsRestClient(args.gerrit_host, user=args.gerrit_user,
                                password=args.gerrit_password, verify_ssl=verify,
                                digest_auth=True)
        acts_v = GerritCollector(gclient, args.users, since).collect()
        entries.extend(from_vcs_activity(a) for a in acts_v)
        log.info("Gerrit: %d activities", len(acts_v))

    # --- GitHub ---
    if args.github_token and args.github_org:
        acts_v = GitHubCollector(args.github_token, args.github_org,
                                 args.users, since, repos=args.github_repos).collect()
        entries.extend(from_vcs_activity(a) for a in acts_v)
        log.info("GitHub: %d activities", len(acts_v))

    # --- GitLab ---
    if args.gitlab_host and args.gitlab_token:
        gclient = VcsRestClient(args.gitlab_host, token=args.gitlab_token, verify_ssl=verify)
        acts_v = GitLabCollector(gclient, args.users, since,
                                 group=args.gitlab_group,
                                 projects=args.gitlab_projects).collect()
        entries.extend(from_vcs_activity(a) for a in acts_v)
        log.info("GitLab: %d activities", len(acts_v))

    # --- Local git ---
    if args.git_local_paths:
        acts_v = LocalGitCollector(args.git_local_paths, args.users, since).collect()
        entries.extend(from_vcs_activity(a) for a in acts_v)
        log.info("git-local: %d activities", len(acts_v))

    # --- Compute statistics ---
    stats = compute_stats(entries)

    # --- Output ---
    os.makedirs(args.output_dir, exist_ok=True)
    save_json_report(entries, os.path.join(args.output_dir, "worklog_all.json"))
    save_csv_report(entries, os.path.join(args.output_dir, "worklog_all.csv"))
    save_markdown_report(entries, stats, args.output_dir)
    print_console_summary(entries, stats)

    # --- Optional Jira worklog insertion ---
    if args.insert_jira_worklog and jira_client:
        log.info("Inserting worklogs into Jira...")
        insert_jira_worklog(jira_client, entries)

    log.info("Done. Reports saved to: %s", args.output_dir)


if __name__ == "__main__":
    main()
