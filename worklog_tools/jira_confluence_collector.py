"""
jira_confluence_collector.py
==============================
Jira / Confluence(Collab)에서 최근 업데이트된 내용을 취합하는 모듈.

기능:
  - 지정한 사용자 목록에 대해 assignee / reporter / watcher / comment 작성자 별
    날짜별 활동 집계
  - Jira 이슈의 최근 변경 이력(changelog) 수집
  - Confluence 페이지의 최근 편집·댓글 수집
  - 결과를 JSON / CSV 로 출력

사용법:
  python jira_confluence_collector.py \
      --jira-host http://jira.example.com \
      --jira-token TOKEN \
      --confluence-host http://confluence.example.com \
      --confluence-token TOKEN \
      --users alice bob charlie \
      --since 2026-06-01 \
      --output report.json
"""

import argparse
import csv
import json
import logging
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterator, List, Optional

import requests

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Data models
# ---------------------------------------------------------------------------

@dataclass
class Activity:
    source: str           # "jira" | "confluence"
    user: str
    date: str             # ISO 8601 date  e.g. "2026-06-20"
    activity_type: str    # "assignee" | "reporter" | "watcher" | "comment" | "edit" | "changelog"
    item_key: str         # Jira issue key or Confluence page ID/title
    item_summary: str
    detail: str           # 짧은 설명


# ---------------------------------------------------------------------------
# HTTP helper
# ---------------------------------------------------------------------------

class RestClient:
    """Bearer-token REST client with simple pagination support."""

    def __init__(self, base_url: str, token: str, verify_ssl: bool = True):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}",
                                     "Content-Type": "application/json"})
        self.verify_ssl = verify_ssl

    def get(self, path: str, params: Optional[Dict] = None) -> Any:
        url = f"{self.base_url}{path}"
        resp = self.session.get(url, params=params, verify=self.verify_ssl, timeout=30)
        resp.raise_for_status()
        return resp.json()

    def paginate_jira(self, path: str, params: Dict, key: str,
                      max_results: int = 200) -> Iterator[Any]:
        """Yield items from a Jira paginated endpoint."""
        start = 0
        while True:
            params.update({"startAt": start, "maxResults": max_results})
            data = self.get(path, params)
            items = data.get(key, [])
            yield from items
            total = data.get("total", 0)
            start += len(items)
            if start >= total or not items:
                break

    def paginate_confluence(self, path: str, params: Dict) -> Iterator[Any]:
        """Yield items from Confluence CQL paginated results."""
        start = 0
        limit = 50
        while True:
            params.update({"start": start, "limit": limit})
            data = self.get(path, params)
            results = data.get("results", [])
            yield from results
            if data.get("_links", {}).get("next") is None:
                break
            start += limit


# ---------------------------------------------------------------------------
# Jira collector
# ---------------------------------------------------------------------------

class JiraCollector:
    def __init__(self, client: RestClient, users: List[str], since: datetime):
        self.client = client
        self.users = set(users)
        self.since = since

    # ---- issues ----

    def _jql_for_users(self) -> str:
        user_list = ", ".join(f'"{u}"' for u in self.users)
        since_str = self.since.strftime("%Y-%m-%d")
        return (
            f"(assignee in ({user_list}) OR reporter in ({user_list}) "
            f"OR watcher in ({user_list}) OR comment ~ \"\") "
            f"AND updated >= \"{since_str}\" ORDER BY updated DESC"
        )

    def collect(self) -> List[Activity]:
        activities: List[Activity] = []

        jql = self._jql_for_users()
        fields = "summary,assignee,reporter,watches,comment,status,updated"
        params = {"jql": jql, "fields": fields}

        log.info("Jira: querying issues with JQL: %s", jql)

        for issue in self.client.paginate_jira("/rest/api/latest/search", params, "issues"):
            key = issue["key"]
            fields_data = issue.get("fields", {})
            summary = fields_data.get("summary", "")
            updated_raw = fields_data.get("updated", "")
            updated_date = updated_raw[:10] if updated_raw else ""

            # assignee
            assignee = (fields_data.get("assignee") or {}).get("name", "")
            if assignee in self.users and self._in_range(updated_date):
                activities.append(Activity(
                    source="jira", user=assignee, date=updated_date,
                    activity_type="assignee", item_key=key,
                    item_summary=summary,
                    detail=f"Assigned to {assignee} on {updated_date}"
                ))

            # reporter
            reporter = (fields_data.get("reporter") or {}).get("name", "")
            if reporter in self.users:
                created_raw = issue.get("fields", {}).get("created", updated_raw)
                created_date = created_raw[:10]
                if self._in_range(created_date):
                    activities.append(Activity(
                        source="jira", user=reporter, date=created_date,
                        activity_type="reporter", item_key=key,
                        item_summary=summary,
                        detail=f"Reported issue {key}"
                    ))

            # comments
            for comment in (fields_data.get("comment") or {}).get("comments", []):
                author = (comment.get("author") or {}).get("name", "")
                created = comment.get("created", "")[:10]
                if author in self.users and self._in_range(created):
                    body_preview = (comment.get("body") or "")[:120].replace("\n", " ")
                    activities.append(Activity(
                        source="jira", user=author, date=created,
                        activity_type="comment", item_key=key,
                        item_summary=summary,
                        detail=body_preview
                    ))

            # changelog (history)
            activities.extend(self._collect_changelog(key, summary))

        # watchers — separate API call per issue is expensive;
        # collect only for issues that have watchers in our user list
        log.info("Jira: collected %d raw activities so far", len(activities))
        return activities

    def _collect_changelog(self, issue_key: str, summary: str) -> List[Activity]:
        acts = []
        try:
            data = self.client.get(f"/rest/api/latest/issue/{issue_key}",
                                   {"expand": "changelog"})
        except requests.HTTPError as exc:
            log.warning("Changelog fetch failed for %s: %s", issue_key, exc)
            return acts

        for history in data.get("changelog", {}).get("histories", []):
            author = (history.get("author") or {}).get("name", "")
            created = history.get("created", "")[:10]
            if author not in self.users or not self._in_range(created):
                continue
            changes = "; ".join(
                f"{i.get('field')}: {i.get('fromString','?')} → {i.get('toString','?')}"
                for i in history.get("items", [])
            )
            acts.append(Activity(
                source="jira", user=author, date=created,
                activity_type="changelog", item_key=issue_key,
                item_summary=summary,
                detail=changes
            ))
        return acts

    def _in_range(self, date_str: str) -> bool:
        if not date_str:
            return False
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return d >= self.since
        except ValueError:
            return False


# ---------------------------------------------------------------------------
# Confluence collector
# ---------------------------------------------------------------------------

class ConfluenceCollector:
    def __init__(self, client: RestClient, users: List[str], since: datetime):
        self.client = client
        self.users = set(users)
        self.since = since

    def collect(self) -> List[Activity]:
        activities: List[Activity] = []
        since_str = self.since.strftime("%Y-%m-%d")

        # Pages recently edited by specified users
        for user in self.users:
            cql = (
                f"type = page AND contributor = \"{user}\" "
                f"AND lastModified >= \"{since_str}\""
            )
            params = {"cql": cql, "expand": "version,history"}
            log.info("Confluence: querying pages for user %s", user)
            try:
                for page in self.client.paginate_confluence("/rest/api/content/search", params):
                    page_id = page.get("id", "")
                    title = page.get("title", "")
                    version_info = page.get("version", {})
                    when = (version_info.get("when") or "")[:10]
                    by_user = (version_info.get("by") or {}).get("username", "")
                    if by_user == user and self._in_range(when):
                        activities.append(Activity(
                            source="confluence", user=user, date=when,
                            activity_type="edit",
                            item_key=page_id, item_summary=title,
                            detail=f"Edited page '{title}' (v{version_info.get('number', '?')})"
                        ))
            except requests.HTTPError as exc:
                log.warning("Confluence page query failed for %s: %s", user, exc)

            # Comments by user
            cql_comment = (
                f"type = comment AND creator = \"{user}\" "
                f"AND created >= \"{since_str}\""
            )
            params_c = {"cql": cql_comment, "expand": "container,version"}
            try:
                for comment in self.client.paginate_confluence("/rest/api/content/search",
                                                               params_c):
                    created = (comment.get("version", {}).get("when") or "")[:10]
                    container_title = (comment.get("container") or {}).get("title", "")
                    container_id = (comment.get("container") or {}).get("id", "")
                    body_preview = (
                        comment.get("body", {})
                               .get("storage", {})
                               .get("value", "")[:120]
                               .replace("\n", " ")
                    )
                    if self._in_range(created):
                        activities.append(Activity(
                            source="confluence", user=user, date=created,
                            activity_type="comment",
                            item_key=container_id, item_summary=container_title,
                            detail=body_preview
                        ))
            except requests.HTTPError as exc:
                log.warning("Confluence comment query failed for %s: %s", user, exc)

        return activities

    def _in_range(self, date_str: str) -> bool:
        if not date_str:
            return False
        try:
            d = datetime.strptime(date_str, "%Y-%m-%d").replace(tzinfo=timezone.utc)
            return d >= self.since
        except ValueError:
            return False


# ---------------------------------------------------------------------------
# Aggregation / reporting
# ---------------------------------------------------------------------------

def aggregate_by_user_date(activities: List[Activity]) -> Dict[str, Dict[str, List[Activity]]]:
    """Return {user: {date: [activities]}}"""
    result: Dict[str, Dict[str, List[Activity]]] = {}
    for act in activities:
        result.setdefault(act.user, {}).setdefault(act.date, []).append(act)
    return result


def print_summary(aggregated: Dict[str, Dict[str, List[Activity]]]) -> None:
    print("\n" + "=" * 70)
    print("WORKLOG SUMMARY")
    print("=" * 70)
    for user, dates in sorted(aggregated.items()):
        total = sum(len(v) for v in dates.values())
        print(f"\n[{user}]  총 {total}건")
        for date in sorted(dates.keys()):
            acts = dates[date]
            print(f"  {date}  ({len(acts)}건)")
            for a in acts:
                print(f"    [{a.source}/{a.activity_type}] {a.item_key} - {a.detail[:80]}")


def save_json(activities: List[Activity], path: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(a) for a in activities], f, ensure_ascii=False, indent=2)
    log.info("JSON 저장: %s", path)


def save_csv(activities: List[Activity], path: str) -> None:
    if not activities:
        return
    fieldnames = list(asdict(activities[0]).keys())
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(asdict(a) for a in activities)
    log.info("CSV 저장: %s", path)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Jira/Confluence worklog collector")
    p.add_argument("--jira-host", default=None, help="Jira base URL")
    p.add_argument("--jira-token", default=None, help="Jira Bearer token")
    p.add_argument("--confluence-host", default=None, help="Confluence base URL")
    p.add_argument("--confluence-token", default=None, help="Confluence Bearer token")
    p.add_argument("--users", nargs="+", required=True, help="Target user names")
    p.add_argument("--since", default="2026-06-01", help="Collect since date (YYYY-MM-DD)")
    p.add_argument("--output", default="worklog_report.json", help="Output JSON path")
    p.add_argument("--csv", default=None, help="Optional CSV output path")
    p.add_argument("--no-ssl-verify", action="store_true", help="Disable SSL verification")
    return p.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> None:
    args = parse_args(argv)
    since = datetime.strptime(args.since, "%Y-%m-%d").replace(tzinfo=timezone.utc)
    verify = not args.no_ssl_verify
    all_activities: List[Activity] = []

    # Jira
    if args.jira_host and args.jira_token:
        jira_client = RestClient(args.jira_host, args.jira_token, verify_ssl=verify)
        collector = JiraCollector(jira_client, args.users, since)
        acts = collector.collect()
        log.info("Jira: %d activities collected", len(acts))
        all_activities.extend(acts)

    # Confluence
    if args.confluence_host and args.confluence_token:
        conf_client = RestClient(args.confluence_host, args.confluence_token, verify_ssl=verify)
        collector_c = ConfluenceCollector(conf_client, args.users, since)
        acts_c = collector_c.collect()
        log.info("Confluence: %d activities collected", len(acts_c))
        all_activities.extend(acts_c)

    aggregated = aggregate_by_user_date(all_activities)
    print_summary(aggregated)
    save_json(all_activities, args.output)
    if args.csv:
        save_csv(all_activities, args.csv)


if __name__ == "__main__":
    main()
