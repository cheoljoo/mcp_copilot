#!/usr/bin/env python3
"""
collect_cheoljoo_2026.py
========================
cheoljoo.lee의 2026년 실제 활동 데이터를 수집한다.

수집 소스:
  1. Jira  (jira.lge.com)
     - JQL: assignee/reporter/watcher 이슈, 2026-01-01 이후 updated
     - 각 이슈의 comment(작성자=cheoljoo.lee), changelog 전수 수집
     - AGILEDEV 프로젝트 전체에서 cheoljoo.lee comment 추가 수집
     - watcher 이슈: watcher = "cheoljoo.lee" 로 별도 수집 (중복 제거)
     - 수집 레벨: 이슈 필드 전체 + changelog 전 이력 + comment 본문 200자

  1-B. Confluence/Collab (collab.lge.com/main)
     - CQL: creator = cheoljoo.lee  (본인 생성 페이지)
     - CQL: contributor = cheoljoo.lee (본인 편집 참여 페이지)
     - 수집 레벨: 제목, space, 생성일, 최종수정일, URL

  2. Gerrit (gpro / lamp / na / eu / as / adas / rn / acp … — vspvs 공용 계정)
     - /changes/?q=owner:cheoljoo.lee  : 본인 commit
     - /changes/?q=reviewer:cheoljoo.lee : 리뷰 참여
     - MESSAGES 옵션으로 inline comment 포함
     - 수집 레벨: subject, branch, status, Code-Review vote, messages

  3. GitLab mod.lge.com/hub  (token: env GITLAB_HUB_TOKEN, user_id=591)
     - /users/591/events  (pushed / commented / merged)
     - 수집 레벨: commit_title, project_id, action, ref(branch)

  4. Local git repos (git log 직접 파싱)
     - ticketsage / ccr / mcp_copilot / agents / youtube_notes 등
     - 수집 레벨: sha, author email/name, date, subject

출력:
  collected_data/jira_activities.json
  collected_data/confluence_activities.json
  collected_data/gerrit_activities.json
  collected_data/gitlab_activities.json
  collected_data/git_activities.json
  collected_data/all_activities.json
  collected_data/summary.json
"""

import json
import os
import re
import subprocess
import time
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth

# ── 설정 ─────────────────────────────────────────────────────────────────────
USER           = "cheoljoo.lee"
USER_EMAIL     = "cheoljoo.lee@lge.com"
SINCE          = "2026-01-01"
UNTIL          = "2026-12-31"
OUT_DIR        = os.path.join(os.path.dirname(__file__), "collected_data")

# ── 파일 확장자 분류 (git numstat 분석용) ──────────────────────────────────────
# 코드 파일: 직접 작성하는 소스코드
CODE_EXTS = frozenset([
    ".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh",
    ".py", ".yaml", ".yml", ".sh", ".bash",
    ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java",
    ".md", ".rst",
])
# 데이터/설정 파일: 자동생성이나 대량 데이터일 수 있음 (> DATA_DUMP_THRESHOLD 줄이면 데이터 덤프로 간주)
DATA_EXTS = frozenset([".json", ".csv", ".txt", ".log", ".xml", ".sql", ".tsv"])
DATA_DUMP_THRESHOLD = 5000   # 이 줄수 이상이면 수작업이 아닌 데이터 덤프로 분류

# ── 테스트 오버헤드 산정을 위한 언어 그룹 분류 ───────────────────────────────────
# C/C++: 빌드(컴파일) + 스모크 테스트 필요
CC_EXTS  = frozenset([".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh"])
# Python: pytest/unit test 실행
PY_EXTS  = frozenset([".py"])
# Config/Script: 문법 검증 + dry-run (yaml, 셸스크립트, JS/TS 등)
CFG_EXTS = frozenset([".yaml", ".yml", ".sh", ".bash", ".js", ".ts", ".jsx", ".tsx", ".go", ".rs", ".java"])
# 문서: 테스트 불필요
DOC_EXTS = frozenset([".md", ".rst"])

JIRA_BASE      = "http://jira.lge.com/issue"
JIRA_USER      = "cheoljoo.lee"
JIRA_PASS      = os.environ.get("JIRA_PASS", "")

LADP_USER      = "vspvs"
LADP_PASS      = os.environ.get("LADP_PASS", "")

# Gerrit 서버 목록 (제공된 gerrit_conf_dict 기반)
# 각 서버의 비밀번호는 환경 변수로 주입한다 (GERRIT_PASS_<NAME>, make.key.mk 참고)
GERRIT_SERVERS = [
    {"name": "gpro",   "url": "http://gpro.lge.com",          "usr": LADP_USER, "pw": LADP_PASS},
    {"name": "lamp",   "url": "http://lamp.lge.com/review",   "usr": "vspvs",   "pw": os.environ.get("GERRIT_PASS_LAMP", "")},
    {"name": "na",     "url": "http://vgit.lge.com/na",       "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_NA", "")},
    {"name": "eu",     "url": "http://vgit.lge.com/eu",       "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_EU", "")},
    {"name": "as",     "url": "http://vgit.lge.com/as",       "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_AS", "")},
    {"name": "adas",   "url": "http://vgit.lge.com/adas",     "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_ADAS", "")},
    {"name": "acp",    "url": "http://vgit.lge.com/acp",      "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_ACP", "")},
    {"name": "rn",     "url": "https://rn.lge.com/git",       "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_RN", "")},
    {"name": "prosys", "url": "http://mod.lge.com/prosys",    "usr": LADP_USER, "pw": os.environ.get("GERRIT_PASS_PROSYS", "")},
]

# Confluence / Collab
COLLAB_BASE = "http://collab.lge.com/main"
COLLAB_USER = JIRA_USER
COLLAB_PASS = JIRA_PASS

# GitLab mod.lge.com/hub
GITLAB_HUB_URL   = "http://mod.lge.com/hub"
GITLAB_HUB_TOKEN = os.environ.get("GITLAB_HUB_TOKEN", "")
GITLAB_USER_ID   = 591   # cheoljoo.lee의 user_id

# cheoljoo.lee의 개인 git repo들 (로컬에 있는 것만)
LOCAL_GIT_DIRS = [
    "/home/cheoljoo.lee/code/mcp_copilot",
    "/home/cheoljoo.lee/code/ccr",
    "/home/cheoljoo.lee/code/ticketsage",
    "/home/cheoljoo.lee/code/weekly_work_report_from_jira",
    "/home/cheoljoo.lee/code/_worklog",
    "/home/cheoljoo.lee/code/agents",
    "/home/cheoljoo.lee/code/youtube_notes_chrome_extension",
]

os.makedirs(OUT_DIR, exist_ok=True)

def log(msg: str) -> None:
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")


# ═══════════════════════════════════════════════════════════════════
#  1. JIRA
# ═══════════════════════════════════════════════════════════════════

def jira_get(path: str, params: Dict = None, max_retry: int = 3) -> Any:
    url = f"{JIRA_BASE}/rest/api/latest{path}"
    auth = HTTPBasicAuth(JIRA_USER, JIRA_PASS)
    for attempt in range(1, max_retry + 1):
        try:
            r = requests.get(url, params=params, auth=auth,
                             timeout=30, verify=False)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            if attempt == max_retry:
                log(f"  [JIRA ERR] {path}: {e}")
                return {}
            time.sleep(2)
    return {}


def jira_paginate(jql: str, fields: str, max_per_page: int = 100) -> List[Dict]:
    issues = []
    start = 0
    while True:
        data = jira_get("/search", {
            "jql": jql, "fields": fields,
            "startAt": start, "maxResults": max_per_page
        })
        batch = data.get("issues", [])
        issues.extend(batch)
        total = data.get("total", 0)
        start += len(batch)
        if start >= total or not batch:
            break
        log(f"    ... {start}/{total}")
    return issues


# Gerrit-Jira 통합 auto-comment 감지 패턴
# Gerrit merge 시 자동으로 Jira 티켓에 달리는 comment (사람이 쓴 게 아님)
_GERRIT_AUTO_PATTERNS = [
    "patch set ",           # Gerrit 리뷰 이벤트 메시지
    "change-id: i",         # Gerrit Change-Id 포함
    "refs/changes/",        # Gerrit ref 경로
    "gerrit.lge.com",
    "gpro.lge.com",
    "lamp.lge.com/review",
    "vgit.lge.com",
    "rn.lge.com/git",
    "mod.lge.com/prosys",
    "has been successfully merged",
    "merged into",
    "commit merged",
]

def _is_gerrit_auto_comment(body: str) -> bool:
    """Gerrit-Jira 통합이 자동으로 작성한 comment인지 판별"""
    lower = body.lower()
    return any(p in lower for p in _GERRIT_AUTO_PATTERNS)


def collect_jira() -> List[Dict]:
    log("=== Jira 수집 시작 ===")
    activities = []

    # ── (A) assignee / reporter 이슈 ────────────────────────────────
    jql = (
        f'(assignee = "{USER}" OR reporter = "{USER}")'
        f' AND updated >= "{SINCE}" ORDER BY updated DESC'
    )
    fields = "key,summary,status,assignee,reporter,created,updated,comment,issuetype,priority,project"
    log(f"  Jira JQL: {jql}")
    issues = jira_paginate(jql, fields)
    log(f"  이슈 {len(issues)}건 수신")

    for issue in issues:
        key     = issue.get("key", "")
        f       = issue.get("fields", {})
        summary = f.get("summary", "")
        status  = (f.get("status") or {}).get("name", "")
        created = (f.get("created") or "")[:10]
        updated = (f.get("updated") or "")[:10]
        assignee_name = (f.get("assignee") or {}).get("name", "")
        reporter_name = (f.get("reporter") or {}).get("name", "")
        itype   = (f.get("issuetype") or {}).get("name", "")
        project = (f.get("project") or {}).get("key", "")

        # assignee 활동
        if assignee_name == USER:
            activities.append({
                "source": "jira", "user": USER, "date": updated,
                "type": "assignee", "key": key, "summary": summary,
                "status": status, "issuetype": itype, "project": project,
                "detail": f"Assigned: {key} ({status})"
            })

        # reporter 활동
        if reporter_name == USER and created >= SINCE:
            activities.append({
                "source": "jira", "user": USER, "date": created,
                "type": "reporter", "key": key, "summary": summary,
                "status": status, "issuetype": itype, "project": project,
                "detail": f"Reported: {key}"
            })

        # comments
        for c in (f.get("comment") or {}).get("comments", []):
            author = (c.get("author") or {}).get("name", "")
            cdate  = (c.get("created") or "")[:10]
            if author == USER and cdate >= SINCE:
                body = (c.get("body") or "")[:200].replace("\n", " ")
                is_auto = _is_gerrit_auto_comment(body)
                activities.append({
                    "source": "jira", "user": USER, "date": cdate,
                    "type": "comment", "key": key, "summary": summary,
                    "status": status, "issuetype": itype, "project": project,
                    "detail": body,
                    "is_gerrit_auto": is_auto,  # Gerrit 자동 통합 comment 여부
                })

    # ── (B) changelog (이력) — 별도 API ────────────────────────────
    log("  changelog 수집 중...")
    unique_keys = list({a["key"] for a in activities if a["source"] == "jira"})
    log(f"  changelog 대상 티켓 {len(unique_keys)}건")
    for i, key in enumerate(unique_keys):
        if i % 20 == 0:
            log(f"    changelog {i}/{len(unique_keys)}")
        data = jira_get(f"/issue/{key}", {"expand": "changelog"})
        for hist in data.get("changelog", {}).get("histories", []):
            author = (hist.get("author") or {}).get("name", "")
            hdate  = (hist.get("created") or "")[:10]
            if author == USER and hdate >= SINCE:
                changes = "; ".join(
                    f"{it.get('field')}: {it.get('fromString','?')} → {it.get('toString','?')}"
                    for it in hist.get("items", [])
                )
                activities.append({
                    "source": "jira", "user": USER, "date": hdate,
                    "type": "changelog", "key": key,
                    "summary": data.get("fields", {}).get("summary", ""),
                    "status": (data.get("fields", {}).get("status") or {}).get("name", ""),
                    "issuetype": (data.get("fields", {}).get("issuetype") or {}).get("name", ""),
                    "project": (data.get("fields", {}).get("project") or {}).get("key", ""),
                    "detail": changes[:300]
                })

    # ── (D) watcher 이슈 ───────────────────────────────────────────
    log("  watcher 이슈 수집 중...")
    jql_w = (
        f'watcher = "{USER}"'
        f' AND updated >= "{SINCE}" ORDER BY updated DESC'
    )
    watch_issues = jira_paginate(jql_w, fields)
    log(f"  watcher 이슈 {len(watch_issues)}건")
    existing_reporter_assignee_keys = {a["key"] for a in activities if a["source"] == "jira"}
    for issue in watch_issues:
        key     = issue.get("key", "")
        f_      = issue.get("fields", {})
        summary = f_.get("summary", "")
        status  = (f_.get("status") or {}).get("name", "")
        updated = (f_.get("updated") or "")[:10]
        itype   = (f_.get("issuetype") or {}).get("name", "")
        project = (f_.get("project") or {}).get("key", "")
        if key not in existing_reporter_assignee_keys:
            activities.append({
                "source": "jira", "user": USER, "date": updated,
                "type": "watcher", "key": key, "summary": summary,
                "status": status, "issuetype": itype, "project": project,
                "detail": f"Watching: {key} ({status})"
            })

    # ── (C) AGILEDEV 프로젝트 전체 (담당 외 comment 포함) ───────────
    log("  AGILEDEV comment 추가 수집 중...")
    jql2 = f'project = AGILEDEV AND comment ~ "{USER}" AND updated >= "{SINCE}"'
    issues2 = jira_paginate(jql2,
        "key,summary,status,comment,issuetype,project", max_per_page=50)
    existing_keys = {a["key"] for a in activities}
    for issue in issues2:
        key  = issue.get("key", "")
        f    = issue.get("fields", {})
        summary = f.get("summary", "")
        status  = (f.get("status") or {}).get("name", "")
        itype   = (f.get("issuetype") or {}).get("name", "")
        project = (f.get("project") or {}).get("key", "")
        for c in (f.get("comment") or {}).get("comments", []):
            author = (c.get("author") or {}).get("name", "")
            cdate  = (c.get("created") or "")[:10]
            if author == USER and cdate >= SINCE:
                body = (c.get("body") or "")[:200].replace("\n", " ")
                is_auto = _is_gerrit_auto_comment(body)
                activities.append({
                    "source": "jira", "user": USER, "date": cdate,
                    "type": "comment", "key": key, "summary": summary,
                    "status": status, "issuetype": itype, "project": project,
                    "detail": body,
                    "is_gerrit_auto": is_auto,  # Gerrit 자동 통합 comment 여부
                })

    log(f"=== Jira 수집 완료: {len(activities)}건 ===")
    return activities


# ═══════════════════════════════════════════════════════════════════
#  2. Gerrit  (여러 서버, vspvs 공용 계정)
# ═══════════════════════════════════════════════════════════════════

def gerrit_get(base_url: str, usr: str, pw: str, path: str, params: Dict = None) -> Any:
    url = f"{base_url.rstrip('/')}/a{path}"
    try:
        r = requests.get(url, params=params,
                         auth=HTTPBasicAuth(usr, pw),
                         timeout=15, verify=False)
        if r.status_code == 401:
            return []
        r.raise_for_status()
        text = r.text
        if text.startswith(")]}"):
            text = text[text.index("\n") + 1:]
        return json.loads(text)
    except Exception as e:
        return []


def gerrit_paginate(base_url: str, usr: str, pw: str, query: str) -> List[Dict]:
    results = []
    start = 0
    while True:
        batch = gerrit_get(base_url, usr, pw, "/changes/", {
            "q": query,
            "o": "DETAILED_ACCOUNTS,LABELS,MESSAGES",
            "S": start, "n": 100
        })
        if not isinstance(batch, list) or not batch:
            break
        results.extend(batch)
        if not batch[-1].get("_more_changes"):
            break
        start += len(batch)
    return results


def collect_gerrit() -> List[Dict]:
    log("=== Gerrit 수집 시작 ===")
    activities = []

    for srv in GERRIT_SERVERS:
        name     = srv["name"]
        base_url = srv["url"]
        usr      = srv["usr"]
        pw       = srv["pw"]

        # 접속 가능 여부 확인 (accounts/self)
        test = gerrit_get(base_url, usr, pw, "/accounts/self")
        if not test or isinstance(test, list):
            log(f"  [{name}] 인증 실패 또는 연결 불가 — skip")
            continue
        log(f"  [{name}] 접속 OK — 수집 시작")

        # owner (본인 commit)
        owner_changes = gerrit_paginate(base_url, usr, pw,
                                        f"owner:{USER} after:{SINCE}")
        log(f"    owner changes: {len(owner_changes)}건")
        for ch in owner_changes:
            date = (ch.get("updated") or ch.get("created") or "")[:10]
            subject = ch.get("subject", "")
            # Gerrit commit summary에서 Jira 티켓 ID 추출 (예: VSPVS-123, AGILEDEV-456)
            jira_keys = re.findall(r'\b([A-Z][A-Z0-9]+-\d+)\b', subject)
            jira_key = jira_keys[0] if jira_keys else ""
            activities.append({
                "source": "gerrit", "server": name, "user": USER, "date": date,
                "type": "commit",
                "repo": ch.get("project", ""),
                "change_id": str(ch.get("_number", "")),
                "branch": ch.get("branch", ""),
                "status": ch.get("status", ""),
                "summary": subject,
                "jira_key": jira_key,  # commit msg에서 추출한 Jira 티켓 ID
                "detail": f"Branch:{ch.get('branch','?')} Status:{ch.get('status','?')} Jira:{jira_key or 'N/A'}"
            })

        # reviewer (리뷰 참여)
        rev_changes = gerrit_paginate(base_url, usr, pw,
                                      f"reviewer:{USER} after:{SINCE} -owner:{USER}")
        log(f"    reviewer changes: {len(rev_changes)}건")
        for ch in rev_changes:
            date = (ch.get("updated") or "")[:10]
            cr_label = ch.get("labels", {}).get("Code-Review", {})
            score = "?"
            for voter in cr_label.get("all", []):
                vname = voter.get("username", "") or (voter.get("email") or "").split("@")[0]
                if USER.split(".")[0] in vname or USER in vname:
                    score = str(voter.get("value", "0"))
                    break

            # inline comment 수집: /changes/{id}/comments
            change_num = ch.get("_number", "")
            inline_count = 0
            inline_chars = 0
            inline_messages = []  # [{"file": ..., "line": ..., "message": ...}]
            try:
                comments_data = gerrit_get(base_url, usr, pw,
                                           f"/changes/{change_num}/comments")
                if isinstance(comments_data, dict):
                    for fname, file_comments in comments_data.items():
                        if isinstance(file_comments, list):
                            for c in file_comments:
                                author = c.get("author", {})
                                aname = (author.get("username", "")
                                         or (author.get("email") or "").split("@")[0])
                                if USER.split(".")[0] in aname or USER in aname:
                                    msg = c.get("message", "")
                                    inline_count += 1
                                    inline_chars += len(msg)
                                    inline_messages.append({
                                        "file": fname,
                                        "line": c.get("line", ""),
                                        "updated": (c.get("updated") or "")[:19],
                                        "message": msg,
                                    })
            except Exception:
                pass
            log(f"      change {change_num}: inline comments={inline_count}, chars={inline_chars}")

            activities.append({
                "source": "gerrit", "server": name, "user": USER, "date": date,
                "type": "review",
                "repo": ch.get("project", ""),
                "change_id": str(change_num),
                "branch": ch.get("branch", ""),
                "status": ch.get("status", ""),
                "summary": ch.get("subject", ""),
                "detail": f"Code-Review:{score} Status:{ch.get('status','?')}",
                "inline_comment_count": inline_count,
                "inline_comment_chars": inline_chars,
                "inline_messages": inline_messages,  # 실제 코멘트 내용 목록
            })

    log(f"=== Gerrit 수집 완료: {len(activities)}건 ===")
    return activities


# ═══════════════════════════════════════════════════════════════════
#  3. GitLab  (mod.lge.com/hub — user_id=591)
# ═══════════════════════════════════════════════════════════════════

def gitlab_get(path: str, params: Dict = None) -> Any:
    url = f"{GITLAB_HUB_URL}/api/v4{path}"
    try:
        r = requests.get(url, params=params,
                         headers={"PRIVATE-TOKEN": GITLAB_HUB_TOKEN},
                         timeout=15, verify=False)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"  [GITLAB ERR] {path}: {e}")
        return []


def collect_gitlab() -> List[Dict]:
    log("=== GitLab 수집 시작 ===")
    activities = []
    page = 1
    # action 파라미터 없이 전체 이벤트 가져오기 (pushed, commented, created, merged 등)
    while True:
        events = gitlab_get(f"/users/{GITLAB_USER_ID}/events", {
            "after": SINCE, "per_page": 100, "page": page
        })
        if not events or not isinstance(events, list):
            break
        for e in events:
            date = (e.get("created_at") or "")[:10]
            if date < SINCE:
                continue
            action = e.get("action_name", "")
            pd     = e.get("push_data") or {}
            project_id = e.get("project_id", "")

            datetime_full = e.get("created_at") or ""
            if "push" in action or pd.get("commit_title"):
                title  = pd.get("commit_title", "")
                branch = pd.get("ref", "")
                activities.append({
                    "source": "gitlab", "user": USER, "date": date,
                    "datetime": datetime_full,
                    "type": "commit",
                    "repo": str(project_id),
                    "change_id": (pd.get("commit_to") or "")[:8],
                    "branch": branch,
                    "summary": title,
                    "detail": f"action={action} ref={branch} proj={project_id}"
                })
            elif "comment" in action:
                target = e.get("target_title", "")
                activities.append({
                    "source": "gitlab", "user": USER, "date": date,
                    "datetime": datetime_full,
                    "type": "comment",
                    "repo": str(project_id),
                    "change_id": str(e.get("target_iid", "")),
                    "branch": "",
                    "summary": target,
                    "detail": f"action={action} proj={project_id}"
                })
            elif "merge" in action or "open" in action or "close" in action:
                target = e.get("target_title", "")
                activities.append({
                    "source": "gitlab", "user": USER, "date": date,
                    "datetime": datetime_full,
                    "type": "mr",
                    "repo": str(project_id),
                    "change_id": str(e.get("target_iid", "")),
                    "branch": "",
                    "summary": target,
                    "detail": f"action={action} proj={project_id}"
                })

        page += 1
        if len(events) < 100:
            break

    log(f"=== GitLab 수집 완료: {len(activities)}건 ===")
    return activities


# ═══════════════════════════════════════════════════════════════════
#  4. Confluence / Collab  (collab.lge.com/main — LDAP 인증)
# ═══════════════════════════════════════════════════════════════════

def collab_get(path: str, params: Dict = None) -> Any:
    url = f"{COLLAB_BASE}/rest/api{path}"
    try:
        r = requests.get(url, params=params,
                         auth=HTTPBasicAuth(COLLAB_USER, COLLAB_PASS),
                         timeout=30, verify=False)
        if r.status_code in (401, 403):
            log(f"  [COLLAB AUTH ERR] {r.status_code} {path}")
            return {}
        r.raise_for_status()
        return r.json()
    except Exception as e:
        log(f"  [COLLAB ERR] {path}: {e}")
        return {}


def collab_cql_paginate(cql: str) -> List[Dict]:
    results = []
    start = 0
    while True:
        data = collab_get("/content/search", {
            "cql": cql,
            "expand": "space,history,version",
            "limit": 50,
            "start": start,
        })
        batch = data.get("results", [])
        results.extend(batch)
        total = data.get("totalSize", 0)
        start += len(batch)
        if start >= total or not batch:
            break
        log(f"    ... {start}/{total}")
    return results


def collab_page_body(page_id: str) -> int:
    """페이지 현재 body 글자수 반환"""
    data = collab_get(f"/content/{page_id}", {"expand": "body.storage"})
    body = (data.get("body") or {}).get("storage", {}).get("value") or ""
    return len(body)


def collab_user_version_count(page_id: str) -> tuple:
    """
    (total_versions, user_versions) 반환.
    total_versions: ?expand=version 으로 현재 버전 번호(=총 버전 수)를 사용.
    user_versions: 기여 비율 추정 (cheoljoo.lee가 contributor 이므로 0.3 기본값).
    실제로는 history API로 최신 편집자를 확인하고 adjustable 0.2~0.5 범위 사용.
    """
    data = collab_get(f"/content/{page_id}", {"expand": "version"})
    version_info = (data.get("version") or {}) if isinstance(data, dict) else {}
    total = version_info.get("number", 10)  # 현재 버전 번호 = 총 버전 수 근사
    # 기여 비율: 마지막 편집자가 본인이면 0.4, 아니면 0.2 (contributor이므로 최소 기여)
    last_editor = (version_info.get("by") or {}).get("username", "")
    user_v = int(total * 0.4) if last_editor == USER else int(total * 0.2)
    return total, user_v


def collect_confluence() -> List[Dict]:
    log("=== Confluence/Collab 수집 시작 ===")
    activities = []

    since_cf = SINCE  # "2026-01-01"

    # (A) 본인이 생성한 페이지/블로그
    cql_created = (
        f'creator = "{USER}" AND created >= "{since_cf}"'
        f' AND type in (page, blogpost) ORDER BY created DESC'
    )
    log(f"  CQL(created): {cql_created}")
    created_pages = collab_cql_paginate(cql_created)
    log(f"  생성 페이지: {len(created_pages)}건")
    for p in created_pages:
        date    = (p.get("history", {}).get("createdDate") or "")[:10]
        space   = p.get("space", {}).get("key", "")
        title   = p.get("title", "")
        ptype   = p.get("type", "page")
        pid     = str(p.get("id", ""))
        url     = f"{COLLAB_BASE}/pages/viewpage.action?pageId={pid}" if pid else ""
        activities.append({
            "source": "confluence", "user": USER, "date": date,
            "type": "page_created",
            "space": space, "page_id": pid,
            "summary": title,
            "detail": f"type={ptype} space={space} url={url}"
        })

    # (B) 본인이 편집한 페이지 (contributor이나 creator는 아닌 것)
    cql_contrib = (
        f'contributor = "{USER}" AND lastModified >= "{since_cf}"'
        f' AND creator != "{USER}"'
        f' AND type in (page, blogpost) ORDER BY lastModified DESC'
    )
    log(f"  CQL(contributor): {cql_contrib}")
    contrib_pages = collab_cql_paginate(cql_contrib)
    log(f"  편집 참여 페이지: {len(contrib_pages)}건")
    for p in contrib_pages:
        date    = (p.get("version", {}).get("when") or "")[:10]
        space   = p.get("space", {}).get("key", "")
        title   = p.get("title", "")
        ptype   = p.get("type", "page")
        pid     = str(p.get("id", ""))
        url     = f"{COLLAB_BASE}/pages/viewpage.action?pageId={pid}" if pid else ""
        activities.append({
            "source": "confluence", "user": USER, "date": date,
            "type": "page_edited",
            "space": space, "page_id": pid,
            "summary": title,
            "detail": f"type={ptype} space={space} url={url}"
        })

    # ── (C) 본문 크기 + 버전 이력 수집 (소요시간 추정 정확도 향상) ─────────────
    log(f"  페이지 본문/버전 이력 수집 중 (총 {len(activities)}건)...")
    for i, act in enumerate(activities):
        pid = act.get("page_id", "")
        if not pid:
            continue
        # body 글자수
        body_chars = collab_page_body(pid)
        act["body_chars"] = body_chars

        if act["type"] == "page_created":
            # 본인이 처음 만든 페이지 → 전체 body가 본인 기여
            act["changed_chars"] = body_chars
        else:
            # 편집 참여 → 버전 이력으로 기여 비율 추정
            total_v, user_v = collab_user_version_count(pid)
            act["total_version_count"]  = total_v
            act["user_version_count"]   = user_v
            ratio = (user_v / total_v) if total_v > 0 else 0.2
            act["changed_chars"] = int(body_chars * ratio)

        if i % 10 == 9:
            log(f"    ... {i+1}/{len(activities)}건 완료")
        time.sleep(0.2)   # rate limiting

    log(f"=== Confluence/Collab 수집 완료: {len(activities)}건 ===")
    return activities


# ═══════════════════════════════════════════════════════════════════
#  5. Local git repos
# ═══════════════════════════════════════════════════════════════════

def _classify_file(path: str, added: int, removed: int, is_binary: bool) -> str:
    """
    파일 하나의 변경 종류 분류.
    반환값:
      "binary"     - binary 파일 (numstat에서 - / - 로 표시)
      "code_edit"  - 코드 파일 수정 (removed > 0)
      "code_add"   - 코드 파일 신규 추가 (removed == 0, deleted 제외)
      "data_dump"  - 데이터 파일 대량 추가 (added > DATA_DUMP_THRESHOLD)
      "data_edit"  - 데이터 파일 소량 수정
      "del"        - 파일 삭제 (added == 0, removed > 0)
      "other"      - 기타 확장자
    """
    if is_binary:
        return "binary"
    ext = os.path.splitext(path.lower())[1]
    if added == 0 and removed > 0:
        return "del"
    if ext in CODE_EXTS:
        return "code_edit" if removed > 0 else "code_add"
    if ext in DATA_EXTS:
        return "data_dump" if (removed == 0 and added >= DATA_DUMP_THRESHOLD) else "data_edit"
    return "other"


def _parse_numstat_commits(stdout: str) -> List[Dict]:
    """
    git log --format=COMMIT\\t... --numstat 출력 파싱.
    각 커밋에 file_stats 리스트와 집계 필드 포함.
    """
    parsed: List[Dict] = []
    cur: Optional[Dict] = None

    for line in stdout.splitlines():
        if line.startswith("COMMIT\t"):
            if cur is not None:
                parsed.append(cur)
            parts = line.split("\t", 5)
            if len(parts) == 6:
                _, sha, email, name, datetime_str, subject = parts
                cur = {
                    "sha": sha, "email": email, "name": name,
                    "datetime_str": datetime_str, "subject": subject,
                    "file_stats": [],
                    # 파일유형별 집계
                    "code_edit_added": 0, "code_edit_removed": 0,
                    "code_add_lines": 0,
                    "data_dump_files": 0, "data_dump_lines": 0,
                    "data_edit_added": 0, "data_edit_removed": 0,
                    "binary_files": 0,
                    "del_lines": 0,
                    "other_added": 0, "other_removed": 0,
                    # 언어 그룹별 집계 (테스트 오버헤드 산정용)
                    "cc_lines": 0,   # C/C++ 변경 줄수 (추가+삭제)
                    "py_lines": 0,   # Python 변경 줄수
                    "cfg_lines": 0,  # Config/Script 변경 줄수
                }
            else:
                cur = None
        elif cur is not None and line.strip():
            # numstat 행: "added\tremoved\tpath" (binary = "-\t-\tpath")
            stat_parts = line.split("\t", 2)
            if len(stat_parts) != 3:
                continue
            raw_add, raw_rem, fpath = stat_parts
            is_binary = (raw_add == "-" and raw_rem == "-")
            added   = 0 if is_binary else (int(raw_add) if raw_add.isdigit() else 0)
            removed = 0 if is_binary else (int(raw_rem) if raw_rem.isdigit() else 0)
            fclass  = _classify_file(fpath, added, removed, is_binary)
            ext     = os.path.splitext(fpath.lower())[1]

            cur["file_stats"].append({
                "path": fpath, "ext": ext,
                "added": added, "removed": removed,
                "is_binary": is_binary, "fclass": fclass,
            })
            # 집계
            if fclass == "binary":
                cur["binary_files"] += 1
            elif fclass == "code_edit":
                cur["code_edit_added"]   += added
                cur["code_edit_removed"] += removed
            elif fclass == "code_add":
                cur["code_add_lines"] += added
            elif fclass == "data_dump":
                cur["data_dump_files"] += 1
                cur["data_dump_lines"] += added
            elif fclass == "data_edit":
                cur["data_edit_added"]   += added
                cur["data_edit_removed"] += removed
            elif fclass == "del":
                cur["del_lines"] += removed
            else:
                cur["other_added"]   += added
                cur["other_removed"] += removed

            # 언어 그룹별 집계 (code_edit / code_add 에서만, 실제 소스 변경)
            if fclass in ("code_edit", "code_add"):
                total_changed = added + removed
                if ext in CC_EXTS:
                    cur["cc_lines"]  += total_changed
                elif ext in PY_EXTS:
                    cur["py_lines"]  += total_changed
                elif ext in CFG_EXTS:
                    cur["cfg_lines"] += total_changed
                # DOC_EXTS: 테스트 불필요, 집계 제외

    if cur is not None:
        parsed.append(cur)
    return parsed


def collect_local_git() -> List[Dict]:
    log("=== Local git 수집 시작 ===")
    activities = []
    match_patterns = [USER, "cheoljoo", "charles.lee", "cheoljoo.lee@"]

    for repo_path in LOCAL_GIT_DIRS:
        if not os.path.isdir(os.path.join(repo_path, ".git")):
            continue
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "log",
                 f"--after={SINCE}", "--all",
                 "--format=COMMIT\t%H\t%ae\t%an\t%aI\t%s",
                 "--numstat"],
                capture_output=True, text=True, timeout=60
            )
        except Exception as e:
            log(f"  git log 실패 {repo_path}: {e}")
            continue

        parsed = _parse_numstat_commits(result.stdout)
        repo_name = os.path.basename(repo_path)

        for c in parsed:
            matched = any(p in c["email"].lower() or p in c["name"].lower()
                         for p in match_patterns)
            if not matched:
                continue

            # 전체 lines 집계 (하위 호환)
            total_added   = (c["code_edit_added"] + c["code_add_lines"]
                             + c["data_edit_added"] + c["other_added"])
            total_removed = (c["code_edit_removed"] + c["data_edit_removed"]
                             + c["del_lines"] + c["other_removed"])

            activities.append({
                "source": "git-local", "user": USER,
                "date": c["datetime_str"][:10],
                "datetime": c["datetime_str"],
                "type": "commit",
                "repo": repo_name,
                "change_id": c["sha"][:8],
                "summary": c["subject"],
                # 기존 호환 필드
                "lines_added":   total_added,
                "lines_removed": total_removed,
                "lines_changed": total_added + total_removed,
                # 파일 유형별 집계
                "code_edit_added":   c["code_edit_added"],
                "code_edit_removed": c["code_edit_removed"],
                "code_add_lines":    c["code_add_lines"],
                "data_dump_files":   c["data_dump_files"],
                "data_dump_lines":   c["data_dump_lines"],
                "data_edit_added":   c["data_edit_added"],
                "data_edit_removed": c["data_edit_removed"],
                "binary_files":      c["binary_files"],
                "del_lines":         c["del_lines"],
                # 언어 그룹별 집계 (테스트 오버헤드 산정용)
                "cc_lines":  c["cc_lines"],
                "py_lines":  c["py_lines"],
                "cfg_lines": c["cfg_lines"],
                # 파일 목록 (분석용, 최대 20개만 저장)
                "file_stats":   c["file_stats"][:20],
                "total_files":  len(c["file_stats"]),
                "detail": (f"repo={repo_name} "
                           f"code_edit=+{c['code_edit_added']}/-{c['code_edit_removed']} "
                           f"code_add={c['code_add_lines']}줄 "
                           f"data_dump={c['data_dump_files']}파일 "
                           f"binary={c['binary_files']}"),
            })
        log(f"  {repo_path}: OK")

    log(f"=== Local git 수집 완료: {len(activities)}건 ===")
    return activities


# ═══════════════════════════════════════════════════════════════════
#  6. 통합 & 저장
# ═══════════════════════════════════════════════════════════════════

def make_summary(all_acts: List[Dict]) -> Dict:
    from collections import Counter
    by_month: Dict[str, List] = defaultdict(list)
    for a in all_acts:
        month = a.get("date", "")[:7]  # YYYY-MM
        by_month[month].append(a)

    summary = {
        "total": len(all_acts),
        "collected_at": datetime.now().isoformat(),
        "by_source": dict(Counter(a["source"] for a in all_acts)),
        "by_type":   dict(Counter(a["type"]   for a in all_acts)),
        "by_month": {
            m: {
                "count": len(acts),
                "by_type": dict(Counter(a["type"] for a in acts)),
                "by_source": dict(Counter(a["source"] for a in acts)),
            }
            for m, acts in sorted(by_month.items())
            if m >= "2026-01"
        }
    }
    return summary


def save(data: Any, filename: str) -> None:
    path = os.path.join(OUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    log(f"  저장: {path}  ({len(data) if isinstance(data, list) else '-'}건)")


def main() -> None:
    import urllib3
    urllib3.disable_warnings()

    log(f"수집 시작: {USER}  {SINCE} ~ {UNTIL}")
    log(f"출력 디렉토리: {OUT_DIR}")

    # --- Jira ---
    jira_acts = collect_jira()
    save(jira_acts, "jira_activities.json")

    # --- Gerrit ---
    gerrit_acts = collect_gerrit()
    save(gerrit_acts, "gerrit_activities.json")

    # --- GitLab ---
    gitlab_acts = collect_gitlab()
    save(gitlab_acts, "gitlab_activities.json")

    # --- Confluence/Collab ---
    confluence_acts = collect_confluence()
    save(confluence_acts, "confluence_activities.json")

    # --- Local git ---
    git_acts = collect_local_git()
    save(git_acts, "git_activities.json")

    # --- 통합 ---
    all_acts = jira_acts + gerrit_acts + gitlab_acts + confluence_acts + git_acts
    save(all_acts, "all_activities.json")

    summary = make_summary(all_acts)
    save(summary, "summary.json")

    # 콘솔 출력
    print("\n" + "=" * 60)
    print(f"  수집 완료: 총 {summary['total']}건")
    print(f"  소스별: {summary['by_source']}")
    print(f"  유형별: {summary['by_type']}")
    print("\n  월별 집계:")
    for m, ms in summary["by_month"].items():
        print(f"    {m}: {ms['count']}건  {ms['by_type']}")
    print("=" * 60)


if __name__ == "__main__":
    main()
