"""
demo_worklog.py
================
실제 서버 없이 mock 데이터로 worklog_aggregator 파이프라인을 시연합니다.
결과 파일은 ./demo_reports/ 에 저장됩니다.
"""

import json
import os
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Dict, List

# ── 경로 설정 (worklog_tools 패키지를 직접 import) ──────────────────────────
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "worklog_tools"))

# ---------------------------------------------------------------------------
# Mock 데이터
# ---------------------------------------------------------------------------
MOCK_JIRA_ACTIVITIES = [
    # (source, user, date, type, key, summary, detail)
    ("jira","alice","2026-06-10","assignee","PROJ-101","Login bug fix","Assigned to alice"),
    ("jira","alice","2026-06-10","comment","PROJ-101","Login bug fix","Fixed null-pointer in AuthService"),
    ("jira","alice","2026-06-11","changelog","PROJ-101","Login bug fix","status: Open → In Progress"),
    ("jira","alice","2026-06-12","changelog","PROJ-101","Login bug fix","status: In Progress → Done"),
    ("jira","bob","2026-06-10","reporter","PROJ-102","Perf regression","Reported perf regression"),
    ("jira","bob","2026-06-11","comment","PROJ-102","Perf regression","Heap profiling shows 3x alloc"),
    ("jira","charlie","2026-06-13","assignee","PROJ-103","API rate limit","Assigned to charlie"),
    ("jira","charlie","2026-06-14","comment","PROJ-103","API rate limit","Added token bucket algorithm"),
    ("confluence","alice","2026-06-11","edit","12345","Design Doc: Auth Refactor","Edited page (v3)"),
    ("confluence","alice","2026-06-12","comment","12345","Design Doc: Auth Refactor","Added security notes"),
    ("confluence","bob","2026-06-13","edit","67890","Perf Analysis Q2","Edited page (v1)"),
]

MOCK_VCS_ACTIVITIES = [
    # (source, user, date, type, repo, change_id, summary, detail)
    ("gerrit","alice","2026-06-10","commit","platform/auth","Iabcdef01","Fix null-ptr in AuthService","Status: MERGED, Branch: main"),
    ("gerrit","bob","2026-06-10","review","platform/auth","Iabcdef01","Fix null-ptr in AuthService","Code-Review vote: +2"),
    ("gerrit","alice","2026-06-12","commit","platform/api","Iabcdef02","Add rate limit middleware","Status: MERGED, Branch: main"),
    ("gerrit","charlie","2026-06-12","review","platform/api","Iabcdef02","Add rate limit middleware","Code-Review vote: +1"),
    ("github","alice","2026-06-13","commit","org/frontend#a1b2c3d4","Fix login redirect","email=alice@example.com",""),
    ("github","bob","2026-06-14","review","org/frontend#42","Improve token refresh","State: APPROVED",""),
    ("gitlab","charlie","2026-06-15","commit","platform/infra#beef0001","Update k8s resource limits","https://gitlab.example.com/...",""),
    ("git-local","alice","2026-06-16","commit","/repos/local#deadbeef","WIP: oauth2 pkce flow","email=alice@example.com",""),
]

# ---------------------------------------------------------------------------
# Build WorklogEntry list from mock data
# ---------------------------------------------------------------------------
@dataclass
class WorklogEntry:
    user: str
    date: str
    source: str
    activity_type: str
    ref: str
    title: str
    detail: str
    duration_min: int = 0


def build_entries() -> List[WorklogEntry]:
    entries = []
    for row in MOCK_JIRA_ACTIVITIES:
        source, user, date, atype, key, summary, detail = row
        entries.append(WorklogEntry(
            user=user, date=date, source=source,
            activity_type=atype, ref=key, title=summary, detail=detail
        ))
    for row in MOCK_VCS_ACTIVITIES:
        if len(row) == 8:
            source, user, date, atype, repo, cid, summary, detail = row
        else:
            source, user, date, atype, repo_cid, summary, detail = row
            repo, cid = repo_cid, ""
        entries.append(WorklogEntry(
            user=user, date=date, source=source,
            activity_type=atype, ref=f"{repo}#{cid}", title=summary, detail=detail
        ))
    return entries


# ---------------------------------------------------------------------------
# Statistics
# ---------------------------------------------------------------------------
def compute_stats(entries: List[WorklogEntry]) -> Dict:
    stats = {}
    by_user = defaultdict(list)
    for e in entries:
        by_user[e.user].append(e)
    for user, acts in by_user.items():
        dates = sorted({a.date for a in acts})
        stats[user] = {
            "total_activities": len(acts),
            "active_days": len(dates),
            "first_activity": dates[0],
            "last_activity": dates[-1],
            "by_type": dict(Counter(a.activity_type for a in acts)),
            "by_source": dict(Counter(a.source for a in acts)),
        }
    return stats


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------
def save_json(entries, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump([asdict(e) for e in entries], f, ensure_ascii=False, indent=2)
    print(f"  [저장] {path}")


def save_markdown(entries, stats, output_dir):
    by_user = defaultdict(list)
    for e in entries:
        by_user[e.user].append(e)
    for user, acts in sorted(by_user.items()):
        by_date = defaultdict(list)
        for a in acts:
            by_date[a.date].append(a)
        s = stats[user]
        lines = [
            f"# Worklog: {user}", "",
            f"- 전체 활동: **{s['total_activities']}건**",
            f"- 활동 일수: **{s['active_days']}일**",
            f"- 기간: {s['first_activity']} ~ {s['last_activity']}", "",
            "## 활동 유형별", "",
        ]
        for t, cnt in sorted(s["by_type"].items()):
            lines.append(f"- {t}: {cnt}건")
        lines += ["", "## 소스별", ""]
        for src, cnt in sorted(s["by_source"].items()):
            lines.append(f"- {src}: {cnt}건")
        lines += ["", "---", "", "## 날짜별 상세", ""]
        for date in sorted(by_date):
            day = by_date[date]
            lines.append(f"### {date}  ({len(day)}건)")
            lines.append("")
            lines.append("| 소스 | 유형 | 참조 | 제목 | 상세 |")
            lines.append("|------|------|------|------|------|")
            for a in sorted(day, key=lambda x: x.source):
                lines.append(
                    f"| {a.source} | {a.activity_type} | {a.ref} | "
                    f"{(a.title or '')[:50]} | {(a.detail or '')[:70]} |"
                )
            lines.append("")
        path = os.path.join(output_dir, f"worklog_{user}.md")
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
        print(f"  [저장] {path}")


def print_summary(entries, stats):
    print("\n" + "=" * 70)
    print("  UNIFIED WORKLOG DEMO REPORT")
    print("=" * 70)
    for user, s in sorted(stats.items()):
        print(f"\n  [{user}]")
        print(f"    총 활동: {s['total_activities']}건  |  활동 일수: {s['active_days']}일")
        print(f"    기간: {s['first_activity']} ~ {s['last_activity']}")
        print(f"    유형별: {s['by_type']}")
        print(f"    소스별: {s['by_source']}")
        # 날짜별 상세
        by_date = defaultdict(list)
        for e in entries:
            if e.user == user:
                by_date[e.date].append(e)
        for date in sorted(by_date):
            print(f"\n    [{date}]")
            for a in by_date[date]:
                print(f"      - [{a.source}/{a.activity_type}] {a.ref}  {a.title[:50]}")
    print("\n" + "=" * 70)


# ---------------------------------------------------------------------------
# Run
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    out_dir = os.path.join(os.path.dirname(__file__), "demo_reports")
    os.makedirs(out_dir, exist_ok=True)

    entries = build_entries()
    stats = compute_stats(entries)

    print_summary(entries, stats)

    save_json(entries, os.path.join(out_dir, "worklog_all.json"))
    save_markdown(entries, stats, out_dir)

    # stats summary
    stats_path = os.path.join(out_dir, "stats_summary.json")
    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
    print(f"  [저장] {stats_path}")

    print("\n[완료] 리포트가 demo_reports/ 에 저장되었습니다.")
