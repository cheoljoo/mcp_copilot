#!/usr/bin/env python3
"""
analyze_worklog_time.py
=======================
수집된 활동 데이터(all_activities.json)를 분석하여
각 활동에 소요 시간을 추정하고 월별 worklog 리포트를 생성한다.

────────────────────────────────────────────────────
■ 소요 시간 추정 방법론 (Heuristic)

[Jira]
  - comment 작성    : 5분(기본) + 1분 per 100글자
  - changelog(상태변경): 10분 / resolve→+20분 / In Progress→+15분
  - reporter(신규 티켓) : 30분
  - assignee/watcher : 0분 (다른 이벤트로 측정)

[Confluence/Collab]
  - page_created : body 글자수 / 50자/분, 최소 20분, 최대 180분
  - page_edited  : (body_chars × 기여비율) / 30자/분, 최소 10분, 최대 120분
    * 기여비율 = user가 만든 버전 수 / 전체 버전 수
  - body_chars / changed_chars 미수집 시 → 기존 고정값 사용

[GitLab / Local git]
  - datetime(ISO 8601 타임스탬프) 기반 실제 세션 계산:
    * 같은 레포 내 커밋 간격 ≤ SESSION_BREAK(120분) → 같은 세션
    * 세션 시간 = (마지막 커밋 - 첫 커밋) + BUFFER(30분)
    * 단독 커밋 → 45분
    * Merge-only 세션 → 5분/건
  - datetime 없는 경우(구 데이터) → 커밋 수 기반 추정
  - GitLab↔local git 중복 제거 (같은 날, 같은 요약)

[Gerrit]
  - owner commit: 45분, review: 20분 (현재 0건)

────────────────────────────────────────────────────
■ 분석 출력
  - 월별 소요 시간 추정 합계
  - 소스별 비중
  - 일별 활동 히트맵 (활동이 있는 날)
  - 상세 활동 목록 (일자별)
  - collected_data/time_report.json
  - collected_data/time_report_monthly.md
"""

import json
import os
import re
from collections import defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

# ── 경로 ──────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(__file__)
DATA_DIR   = os.path.join(BASE_DIR, "collected_data")
OUT_JSON   = os.path.join(DATA_DIR, "time_report.json")
OUT_MD     = os.path.join(DATA_DIR, "time_report_monthly.md")

# ── 설정 ──────────────────────────────────────────────────────────
YEAR = "2026"
SESSION_BREAK_MINS = 120   # 이 분 이상 간격이면 새 세션
SESSION_BUFFER_MINS = 30   # 세션 종료 후 마무리 시간 여유

# ══════════════════════════════════════════════════════════════════
# 0. datetime 헬퍼
# ══════════════════════════════════════════════════════════════════

def _norm(s: str) -> str:
    """커밋 메시지 정규화 (중복 비교용)"""
    return re.sub(r"\s+", " ", (s or "").strip().lower())[:80]


def _parse_dt(s: str) -> Optional[datetime]:
    """ISO 8601 또는 날짜 문자열을 timezone-aware datetime으로 파싱"""
    if not s:
        return None
    try:
        s2 = s.strip().replace("Z", "+00:00")
        if "T" in s2:
            return datetime.fromisoformat(s2)
        # 날짜만 있는 경우 KST 기준 자정
        return datetime.fromisoformat(s2 + "T00:00:00+09:00")
    except Exception:
        return None


def _gap_minutes(dt1: Optional[datetime], dt2: Optional[datetime]) -> Optional[int]:
    """두 datetime 사이 분 차이 (dt2 - dt1). None이면 None 반환"""
    if dt1 is None or dt2 is None:
        return None
    delta = (dt2 - dt1).total_seconds() / 60
    return int(delta)

# ══════════════════════════════════════════════════════════════════
# 1. 소요 시간 추정 함수
# ══════════════════════════════════════════════════════════════════

def _is_weekly_report(title: str) -> bool:
    """주간업무보고 판단 (Confluence page 제목)"""
    return bool(re.search(r"W\d+\uac00?\ucc28|\uc8fc\uac04\uc5c5\ubb34\ubcf4\uace0", title))


def estimate_jira(act: Dict) -> Tuple[int, str]:
    """
    Jira 활동 소요 시간(분) 추정.
    반환: (분, 근거 설명)
    """
    atype  = act.get("type", "")
    detail = act.get("detail", "") or ""
    summary = act.get("summary", "") or ""

    if atype == "reporter":
        return 30, "신규 티켓 작성 30분"

    if atype == "comment":
        # Gerrit-Jira 통합 auto-comment: 시스템이 자동으로 달아주는 알림 → 사람 작업 없음
        if act.get("is_gerrit_auto"):
            return 0, "Gerrit 자동 통합 comment (이중계산 방지 — 해당 작업은 Gerrit commit으로 산정)"
        body_len = len(detail)  # detail에 최대 200자 저장됨
        # 사전읽기(컨텍스트 파악) 8분 + 작성 5분 기본 + 내용 길이 1분/100자
        # 근거: 코멘트 작성 전 티켓 설명·기존 스레드 읽기 평균 8분 (Nielsen 2013,
        #        이메일 응답 연구의 pre-reading 시간 참조)
        reading_overhead = 8
        writing_mins = 5 + max(0, body_len // 100)
        mins = reading_overhead + writing_mins
        return mins, f"comment: 읽기 {reading_overhead}분 + 작성 {writing_mins}분({body_len}자) = {mins}분"

    if atype == "changelog":
        # detail 예: "status: Open → In Progress"
        base = 10
        bonus_reason = ""
        lower = detail.lower()
        # resolve / close
        if any(k in lower for k in ["resolved", "closed", "done", "complete", "\ud574\uacb0", "\uc885\ub8cc"]):
            base += 20
            bonus_reason = " (+20분 resolve)"
        elif any(k in lower for k in ["in progress", "\uc9c4\ud589", "open → in"]):
            base += 15
            bonus_reason = " (+15분 시작)"
        return base, f"상태변경 {base}분{bonus_reason} | {detail[:60]}"

    if atype in ("assignee", "watcher"):
        return 0, "담당/관찰 — 다른 이벤트로 측정"

    return 0, f"미분류 type={atype}"


def estimate_confluence(act: Dict) -> Tuple[int, str]:
    """Confluence 활동 소요 시간 추정 — body 글자수 우선, 없으면 고정값"""
    atype      = act.get("type", "")
    title      = act.get("summary", "") or ""
    body_chars = act.get("body_chars", 0) or 0
    changed    = act.get("changed_chars", 0) or 0

    if atype == "page_created":
        if body_chars > 0:
            # 50자/분 (타이핑+사고), 최소 20분, 최대 180분
            mins = max(20, min(180, body_chars // 50))
            return mins, f"생성 body={body_chars}자 → {mins}분"
        if _is_weekly_report(title):
            return 30, f"주간보고 작성 30분 | {title[:40]}"
        return 60, f"문서 작성 60분(기본값) | {title[:40]}"

    if atype == "page_edited":
        if changed > 0:
            # 30자/분, 최소 10분, 최대 120분
            mins = max(10, min(120, changed // 30))
            user_v = act.get("user_version_count", "?")
            total_v = act.get("total_version_count", "?")
            return mins, f"편집 변경량={changed}자(v{user_v}/{total_v}) → {mins}분"
        if _is_weekly_report(title):
            return 20, f"주간보고 편집 20분(기본값) | {title[:40]}"
        return 20, f"문서 편집 20분(기본값) | {title[:40]}"

    return 0, f"미분류 type={atype}"


def _lines_to_mins(lines: int) -> int:
    """코드 변경량(추가+삭제 합산) → 예상 작업 시간(분). 하위 호환용."""
    if lines <= 0:
        return 0
    return max(20, min(200, 20 + lines // 10))


# 세션당 테스트 오버헤드 상한 (코딩 시간에 추가되는 값)
TEST_OVERHEAD_CAP = 60   # 세션당 테스트 오버헤드 최대 60분

def _test_overhead_mins(cc_lines: int, py_lines: int, cfg_lines: int) -> Tuple[int, str]:
    """
    언어 그룹별 테스트 소요 시간 추정 (세션당 1회만 적용).

    근거:
      C/C++ (.c .h .cpp .cc .cxx .hpp .hh)
        - 빌드(컴파일): 증분 빌드 기준 5~15분 (LGE automotive 빌드 시스템 경험치)
        - 스모크/유닛 테스트 실행: 5~15분
        - 결과 확인 + 실패 시 재수정 반복: 5분
        → 세션당 25분 고정 (1회 build+test 사이클 기준)
        → 단, 실제 변경량이 작으면(< 50줄) 10분으로 감소 (헤더 1줄 수정 등)

      Python (.py)
        - pytest / unittest 실행: 2~5분
        - 결과 확인 + 수정: 5~10분
        → 세션당 15분 고정
        → 변경량 < 30줄이면 8분 (단순 함수 수정)

      Config/Script (.yaml .yml .sh .js .ts 등)
        - YAML: 문법 검증 + CI dry-run / 파이프라인 확인: 10분
        - Shell/JS/TS: 실행해서 동작 확인: 5~10분
        → 세션당 10분 고정

      문서 (.md .rst): 테스트 불필요 → 0분

    여러 언어가 섞인 경우: 각각 산정 후 합산, TEST_OVERHEAD_CAP(60분)으로 cap
    """
    if cc_lines + py_lines + cfg_lines == 0:
        return 0, ""

    parts: List[str] = []
    total = 0

    if cc_lines > 0:
        m = 10 if cc_lines < 50 else 25
        total += m
        parts.append(f"C/C++빌드+테스트{m}분(변경{cc_lines}줄)")

    if py_lines > 0:
        m = 8 if py_lines < 30 else 15
        total += m
        parts.append(f"Python테스트{m}분(변경{py_lines}줄)")

    if cfg_lines > 0:
        total += 10
        parts.append(f"Config검증10분(변경{cfg_lines}줄)")

    capped = min(total, TEST_OVERHEAD_CAP)
    detail = " + ".join(parts) + (f" → cap {capped}분" if capped < total else "")
    return capped, detail


def _estimate_git_file_types(act: Dict) -> Tuple[int, str]:
    """
    커밋 활동의 파일 유형별 집계 필드로 시간(분) 산정.
    파일 유형별 근거:
      code_edit  : 기존 코드 수정. 컨텍스트 파악(20분) + 10 LOC/분 (McConnell)
                   max(20, min(200, 20 + lines//10))
      code_add   : 신규 코드 파일 생성. 설계·구조 결정이 필요하지만 "어디를 고치나"
                   탐색 없음 → 15 LOC/분 (신규작성이 수정보다 빠름)
                   max(15, min(180, 15 + lines//15))
      data_dump  : CSV/JSON 등 대량 데이터 파일 추가(>5000줄). 수작업이 아닌
                   스크립트·export 결과물 → 파일당 10분(준비+확인) 고정
      data_edit  : 소규모 데이터/설정 수정 → code_edit 절반 속도 (가독성↓)
                   max(10, min(60, 10 + lines//20))
      binary     : 이미지·바이너리 파일 추가/변경 → 파일당 5분 고정
                   (실제 편집 없이 파일 복사+커밋이 대부분)
      other      : 기타 확장자 → code_edit의 절반 기준
    """
    # 파일 유형별 집계 (필드 없으면 0으로 fallback)
    code_edit = (act.get("code_edit_added", 0) or 0) + (act.get("code_edit_removed", 0) or 0)
    code_add  = act.get("code_add_lines",   0) or 0
    data_dump_files = act.get("data_dump_files", 0) or 0
    data_edit = (act.get("data_edit_added", 0) or 0) + (act.get("data_edit_removed", 0) or 0)
    binary    = act.get("binary_files",     0) or 0
    # other = total - above (하위 호환: 구필드만 있는 경우)
    if code_edit + code_add + data_dump_files + data_edit + binary == 0:
        return None, "파일유형 정보 없음"

    parts: List[str] = []
    mins = 0

    if code_edit > 0:
        m = max(20, min(200, 20 + code_edit // 10))
        mins += m
        parts.append(f"코드수정{code_edit}줄→{m}분")

    if code_add > 0:
        m = max(15, min(180, 15 + code_add // 15))
        mins += m
        parts.append(f"코드신규{code_add}줄→{m}분")

    if data_dump_files > 0:
        m = data_dump_files * 10
        mins += m
        parts.append(f"데이터덤프{data_dump_files}파일→{m}분")

    if data_edit > 0:
        m = max(10, min(60, 10 + data_edit // 20))
        mins += m
        parts.append(f"데이터수정{data_edit}줄→{m}분")

    if binary > 0:
        m = binary * 5
        mins += m
        parts.append(f"바이너리{binary}파일→{m}분")

    detail = " | ".join(parts)
    return max(mins, 15), detail  # 최소 15분 (컨텍스트 파악)


def _make_git_session(repo: str, acts: List[Dict]) -> Dict:
    """커밋 목록 → 세션 dict 생성 (datetime 간격 + 파일유형별 변경량 + 테스트 시간 반영)"""
    date = acts[0].get("date", "")
    summaries = [a.get("summary", "")[:60] for a in acts[:5]]

    # ── 파일 유형별 집계 (세션 전체) ─────────────────────────
    code_edit = sum((a.get("code_edit_added",   0) or 0) +
                    (a.get("code_edit_removed",  0) or 0) for a in acts)
    code_add  = sum( a.get("code_add_lines",    0) or 0  for a in acts)
    data_dump = sum( a.get("data_dump_files",   0) or 0  for a in acts)
    data_edit = sum((a.get("data_edit_added",   0) or 0) +
                    (a.get("data_edit_removed",  0) or 0) for a in acts)
    binary    = sum( a.get("binary_files",      0) or 0  for a in acts)
    has_type_info = (code_edit + code_add + data_dump + data_edit + binary) > 0

    # ── 언어 그룹별 집계 (테스트 오버헤드용) ──────────────────
    cc_lines  = sum(a.get("cc_lines",  0) or 0 for a in acts)
    py_lines  = sum(a.get("py_lines",  0) or 0 for a in acts)
    cfg_lines = sum(a.get("cfg_lines", 0) or 0 for a in acts)

    total_added   = sum(a.get("lines_added",   0) or 0 for a in acts)
    total_removed = sum(a.get("lines_removed", 0) or 0 for a in acts)

    # ── Merge-only 세션 ────────────────────────────────────
    all_merge = all("merge branch" in (a.get("summary", "") or "").lower()
                    for a in acts)
    if all_merge:
        mins = 5 * len(acts)
        return {"source": "git-session", "date": date, "repo": repo,
                "commits": len(acts), "commit_summaries": summaries,
                "lines_added": total_added, "lines_removed": total_removed,
                "test_overhead_mins": 0,
                "estimated_minutes": mins,
                "reason": f"merge commit {len(acts)}건 × 5분 (branch 병합)"}

    # ── 파일유형 기반 코딩 시간 산정 ──────────────────────────
    if has_type_info:
        type_mins = 0
        type_parts: List[str] = []
        if code_edit > 0:
            m = max(20, min(200, 20 + code_edit // 10))
            type_mins += m; type_parts.append(f"코드수정{code_edit}줄→{m}분")
        if code_add > 0:
            m = max(15, min(180, 15 + code_add // 15))
            type_mins += m; type_parts.append(f"코드신규{code_add}줄→{m}분")
        if data_dump > 0:
            m = data_dump * 10
            type_mins += m; type_parts.append(f"데이터덤프{data_dump}파일→{m}분")
        if data_edit > 0:
            m = max(10, min(60, 10 + data_edit // 20))
            type_mins += m; type_parts.append(f"데이터수정{data_edit}줄→{m}분")
        if binary > 0:
            m = binary * 5
            type_mins += m; type_parts.append(f"바이너리{binary}파일→{m}분")
        type_mins = max(type_mins, 15)
        type_detail = " | ".join(type_parts) if type_parts else "변경없음"
    else:
        total_lines = total_added + total_removed
        type_mins   = _lines_to_mins(total_lines) if total_lines > 0 else None
        type_detail = f"전체{total_lines}줄(파일유형미분류)"

    # ── 테스트 오버헤드 산정 ───────────────────────────────────
    test_mins, test_detail = _test_overhead_mins(cc_lines, py_lines, cfg_lines)

    # ── datetime 스팬 계산 ─────────────────────────────────
    dts = [_parse_dt(a.get("datetime") or a.get("date", "")) for a in acts]
    dts_valid = [dt for dt in dts if dt is not None]
    span_mins: Optional[int] = None
    if len(dts_valid) >= 2:
        gap = _gap_minutes(min(dts_valid), max(dts_valid))
        if gap is not None and gap >= 0:
            span_mins = min(gap + SESSION_BUFFER_MINS, 240)

    # ── 코딩 시간 확정: max(스팬, 파일유형) ───────────────────
    if span_mins is not None and type_mins:
        coding_mins = max(span_mins, type_mins)
        coding_reason = (f"실제스팬+{SESSION_BUFFER_MINS}분={span_mins}분 vs "
                         f"파일유형={type_mins}분 → max={coding_mins}분 | {type_detail}")
    elif span_mins is not None:
        coding_mins = span_mins
        coding_reason = f"실제스팬+{SESSION_BUFFER_MINS}분={coding_mins}분 (파일유형정보없음)"
    elif type_mins:
        coding_mins = min(type_mins, 240)
        coding_reason = f"파일유형기반={coding_mins}분 | {type_detail}"
    else:
        coding_mins = min(45 + (len(acts) - 1) * 15, 240)
        coding_reason = f"커밋수기반={coding_mins}분 ({len(acts)}커밋, 메타없음)"

    # ── 최종 세션 시간 = 코딩 + 테스트 ───────────────────────
    # 세션 전체 상한: 360분 (6h). 하루 단일 태스크 최대값으로 설정
    SESSION_TOTAL_CAP = 360
    mins = min(coding_mins + test_mins, SESSION_TOTAL_CAP)
    if test_mins > 0:
        reason = (f"{coding_reason} | 테스트: {test_detail} "
                  f"→ 합계={coding_mins}+{test_mins}={mins}분")
    else:
        reason = coding_reason

    return {"source": "git-session", "date": date, "repo": repo,
            "commits": len(acts), "commit_summaries": summaries,
            "lines_added": total_added, "lines_removed": total_removed,
            "code_edit_lines": code_edit, "code_add_lines": code_add,
            "data_dump_files": data_dump, "binary_files": binary,
            "cc_lines": cc_lines, "py_lines": py_lines, "cfg_lines": cfg_lines,
            "test_overhead_mins": test_mins,
            "estimated_minutes": mins, "reason": reason}


def group_git_sessions(git_acts: List[Dict]) -> List[Dict]:
    """
    git 커밋을 레포 기준으로 묶고, datetime 간격으로 세션을 분리.
    GitLab/local-git 중복 제거: 같은 날 같은 요약 → 1건만 사용.
    """
    # 중복 제거
    seen: set = set()
    deduped: List[Dict] = []
    for a in sorted(git_acts,
                    key=lambda x: (x.get("datetime") or x.get("date", ""),
                                   x.get("source", ""))):
        key = (a.get("date", ""), _norm(a.get("summary", "")))
        if key not in seen:
            seen.add(key)
            deduped.append(a)

    # 레포별로 분리
    by_repo: Dict[str, List[Dict]] = defaultdict(list)
    for a in deduped:
        by_repo[a.get("repo", "")].append(a)

    sessions: List[Dict] = []
    for repo, acts in by_repo.items():
        # datetime 또는 date 기준 정렬
        acts_sorted = sorted(
            acts,
            key=lambda x: x.get("datetime") or x.get("date", "")
        )

        # 세션 분리 (SESSION_BREAK_MINS 이상 간격 = 새 세션)
        current: List[Dict] = [acts_sorted[0]]
        for prev, curr in zip(acts_sorted, acts_sorted[1:]):
            prev_dt = _parse_dt(prev.get("datetime") or prev.get("date", ""))
            curr_dt = _parse_dt(curr.get("datetime") or curr.get("date", ""))
            gap = _gap_minutes(prev_dt, curr_dt)

            # gap이 None(날짜만)이거나 SESSION_BREAK 초과면 새 세션
            if gap is None or gap > SESSION_BREAK_MINS:
                sessions.append(_make_git_session(repo, current))
                current = [curr]
            else:
                current.append(curr)
        sessions.append(_make_git_session(repo, current))

    return sessions


# ══════════════════════════════════════════════════════════════════
# 2. 데이터 로드 & 분석
# ══════════════════════════════════════════════════════════════════

def load_activities() -> List[Dict]:
    path = os.path.join(DATA_DIR, "all_activities.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def analyze() -> Dict:
    acts = load_activities()
    print(f"전체 활동: {len(acts)}건")

    # ── 소스별 분리 ────────────────────────────────────────────────
    jira_acts       = [a for a in acts if a["source"] == "jira"]
    confluence_acts = [a for a in acts if a["source"] == "confluence"]
    git_acts        = [a for a in acts if a["source"] in ("gitlab", "git-local")]
    gerrit_acts     = [a for a in acts if a["source"] == "gerrit"]

    # ── Jira 개별 추정 ─────────────────────────────────────────────
    jira_results = []
    for a in jira_acts:
        mins, reason = estimate_jira(a)
        if mins > 0:
            jira_results.append({
                "source": "jira",
                "date": a.get("date",""),
                "type": a.get("type",""),
                "key": a.get("key",""),
                "summary": (a.get("summary","") or "")[:60],
                "estimated_minutes": mins,
                "reason": reason,
                "detail": (a.get("detail","") or "")[:100],
            })

    # ── Confluence 개별 추정 ───────────────────────────────────────
    conf_results = []
    for a in confluence_acts:
        mins, reason = estimate_confluence(a)
        if mins > 0:
            conf_results.append({
                "source": "confluence",
                "date": a.get("date",""),
                "type": a.get("type",""),
                "space": a.get("space",""),
                "summary": (a.get("summary","") or "")[:60],
                "estimated_minutes": mins,
                "reason": reason,
            })

    # ── Git 세션 추정 ──────────────────────────────────────────────
    git_sessions = group_git_sessions(git_acts)

    # ── Gerrit 개별 추정 ───────────────────────────────────────────
    gerrit_results = []
    for a in gerrit_acts:
        atype = a.get("type", "")
        if atype == "commit":
            mins = 45
            reason = "Gerrit commit 45분 (change 작성)"
        elif atype == "review":
            # inline comment 수 + 내용 길이(chars) 기반 산정
            # ─ 코드 읽기: 10분 기본
            # ─ 코멘트 작성: 1개당 5분 + 100자당 1분 (작성 타이핑 시간)
            # ─ 최대 120분 cap
            n = int(a.get("inline_comment_count") or 0)
            chars = int(a.get("inline_comment_chars") or 0)
            if n == 0:
                mins = 10
                reason = "Gerrit review 10분 (vote만, inline comment 없음)"
            else:
                read_mins = 10                        # 코드 읽기 기본
                write_mins = n * 5 + chars // 100    # 작성: 개당 5분 + 100자당 1분
                mins = min(read_mins + write_mins, 120)
                reason = (f"Gerrit review {mins}분 "
                          f"(읽기10 + 작성{write_mins}: comment {n}개/{chars}자)")
        else:
            continue
        gerrit_results.append({
            "source": "gerrit", "date": a.get("date", ""),
            "type": atype, "repo": a.get("repo", ""),
            "summary": (a.get("summary", "") or "")[:60],
            "estimated_minutes": mins,
            "reason": reason,
        })

    # ── 통합 & 월별 집계 ───────────────────────────────────────────
    all_timed = jira_results + conf_results + git_sessions + gerrit_results

    by_month: Dict[str, List] = defaultdict(list)
    for item in all_timed:
        month = item["date"][:7]
        if month.startswith(YEAR):
            by_month[month].append(item)

    monthly_summary = {}
    for month, items in sorted(by_month.items()):
        total_min = sum(i["estimated_minutes"] for i in items)
        by_source = defaultdict(int)
        by_type   = defaultdict(int)
        for i in items:
            src = i["source"].replace("git-session","git")
            by_source[src] += i["estimated_minutes"]
            by_type[i.get("type","?")] += i["estimated_minutes"]

        # 일별 활동 집계
        by_day: Dict[str, int] = defaultdict(int)
        for i in items:
            by_day[i["date"]] += i["estimated_minutes"]

        active_days = len(by_day)
        avg_per_active_day = total_min / active_days if active_days else 0

        # Jira 상세
        jira_comments = [i for i in items if i.get("type") == "comment"]
        jira_resolved = [i for i in items
                         if i.get("type") == "changelog"
                         and any(k in (i.get("reason","")).lower()
                                 for k in ["resolve", "close", "done"])]

        monthly_summary[month] = {
            "total_minutes": total_min,
            "total_hours": round(total_min / 60, 1),
            "active_days": active_days,
            "avg_min_per_active_day": round(avg_per_active_day, 0),
            "by_source_minutes": dict(by_source),
            "by_type_minutes": dict(by_type),
            "jira_comment_count": len(jira_comments),
            "jira_comment_total_min": sum(i["estimated_minutes"] for i in jira_comments),
            "jira_resolved_count": len(jira_resolved),
            "top_active_days": sorted(by_day.items(), key=lambda x: -x[1])[:5],
            "items": items,  # 상세 보관
        }

    # 전체 합계
    grand_total_min = sum(
        ms["total_minutes"] for ms in monthly_summary.values()
    )
    grand_total_by_source = defaultdict(int)
    for ms in monthly_summary.values():
        for src, m in ms["by_source_minutes"].items():
            grand_total_by_source[src] += m

    return {
        "generated_at": datetime.now().isoformat(),
        "grand_total_minutes": grand_total_min,
        "grand_total_hours": round(grand_total_min / 60, 1),
        "grand_total_by_source": dict(grand_total_by_source),
        "monthly": monthly_summary,
    }


# ══════════════════════════════════════════════════════════════════
# 3. 리포트 출력
# ══════════════════════════════════════════════════════════════════

def print_console(report: Dict) -> None:
    print("\n" + "=" * 68)
    print(f"  📊 cheoljoo.lee 2026년 업무 소요시간 추정 리포트")
    print(f"  총 추정시간: {report['grand_total_hours']}시간"
          f" ({report['grand_total_minutes']}분)")
    print(f"  소스별: {report['grand_total_by_source']}")
    print("=" * 68)
    for month, ms in report["monthly"].items():
        print(f"\n[{month}]  {ms['total_hours']}h  "
              f"(활동일: {ms['active_days']}일 / "
              f"활동일 평균 {ms['avg_min_per_active_day']:.0f}분)")
        print(f"  소스별(분): {ms['by_source_minutes']}")
        print(f"  Jira comment: {ms['jira_comment_count']}건 "
              f"({ms['jira_comment_total_min']}분)")
        print(f"  Jira resolve: {ms['jira_resolved_count']}건")
        if ms["top_active_days"]:
            top = ms["top_active_days"][0]
            print(f"  최고 활동일: {top[0]} ({top[1]}분)")


def write_markdown(report: Dict) -> None:
    lines = []
    lines.append("# cheoljoo.lee 2026년 업무 소요시간 추정 리포트\n")
    lines.append(f"> 생성: {report['generated_at'][:16]}  \n")
    lines.append(f"> 총 추정시간: **{report['grand_total_hours']}시간**"
                 f" ({report['grand_total_minutes']}분)\n\n")
    lines.append("---\n\n")

    # 방법론 요약
    lines.append("## 0. 소요시간 추정 방법론\n\n")
    lines.append("| 소스 | 유형 | 추정 방법 |\n|------|------|----------|\n")
    rows = [
        ("Jira", "신규 티켓 작성 (reporter)", "30분/건"),
        ("Jira", "comment 작성", "5분 기본 + 1분/100글자"),
        ("Jira", "상태 변경 (changelog)", "10분/건 (resolve +20분, In Progress +15분)"),
        ("Jira", "담당/관찰 (assignee/watcher)", "0분 — 다른 이벤트로 측정"),
        ("Confluence", "페이지 생성 (page_created)", "60분 (주간보고 30분)"),
        ("Confluence", "페이지 편집 (page_edited)", "20분/건"),
        ("GitLab/git", "단독 커밋 (하루 1건)", "45분/세션"),
        ("GitLab/git", "복수 커밋 세션", "45분 + 15분×(커밋수-1), 최대 240분"),
        ("GitLab/git", "Merge commit만", "5분/건"),
        ("GitLab/git", "GitLab↔Local git 중복", "1건만 계산 (dedup)"),
        ("Gerrit", "owner commit", "45분/건"),
        ("Gerrit", "reviewer", "20분/건"),
    ]
    for src, typ, method in rows:
        lines.append(f"| {src} | {typ} | {method} |\n")
    lines.append("\n---\n\n")

    # 전체 통계
    lines.append("## 1. 전체 요약\n\n")
    lines.append("| 월 | 추정시간(h) | 활동일 | 활동일 평균 | Jira comment | Jira resolve |\n")
    lines.append("|-----|------------|-------|-----------|------------|-------------|\n")
    for month, ms in report["monthly"].items():
        lines.append(
            f"| {month} | **{ms['total_hours']}h** "
            f"| {ms['active_days']}일 "
            f"| {ms['avg_min_per_active_day']:.0f}분 "
            f"| {ms['jira_comment_count']}건({ms['jira_comment_total_min']}분) "
            f"| {ms['jira_resolved_count']}건 |\n"
        )
    total_h = report['grand_total_hours']
    lines.append(f"| **합계** | **{total_h}h** | - | - | - | - |\n\n")

    # 소스별 비중
    lines.append("## 2. 소스별 시간 비중\n\n")
    lines.append("| 소스 | 월별 시간(h) → |\n")
    sources = sorted({
        src
        for ms in report["monthly"].values()
        for src in ms["by_source_minutes"]
    })
    months = sorted(report["monthly"].keys())
    header = "| 소스 | " + " | ".join(m[5:] for m in months) + " | 합계 |\n"
    lines.append(header)
    sep = "|------|" + "------|" * (len(months) + 1) + "\n"
    lines.append(sep)
    for src in sources:
        row_mins = [report["monthly"][m]["by_source_minutes"].get(src, 0)
                    for m in months]
        total = sum(row_mins)
        cells = " | ".join(f"{v//60}h{v%60:02d}m" for v in row_mins)
        lines.append(f"| {src} | {cells} | {total//60}h{total%60:02d}m |\n")
    lines.append("\n---\n\n")

    # 월별 상세
    for month, ms in report["monthly"].items():
        lines.append(f"## {month} 상세 활동 ({ms['total_hours']}h)\n\n")

        # 최다 활동일
        if ms["top_active_days"]:
            lines.append("**활동 많은 날 TOP 5:**\n\n")
            lines.append("| 날짜 | 추정 분 |\n|------|--------|\n")
            for day, mins in ms["top_active_days"]:
                lines.append(f"| {day} | {mins}분 ({mins//60}h{mins%60:02d}m) |\n")
            lines.append("\n")

        # Jira comment 목록
        comments = [i for i in ms["items"] if i.get("type") == "comment"]
        if comments:
            lines.append(f"**Jira comment 작성 ({len(comments)}건):**\n\n")
            lines.append("| 날짜 | 티켓 | 내용(요약) | 추정 분 |\n")
            lines.append("|------|------|----------|--------|\n")
            for c in sorted(comments, key=lambda x: x["date"]):
                detail_preview = (c.get("detail","") or "")[:50].replace("\n"," ")
                lines.append(
                    f"| {c['date']} | {c['key']} "
                    f"| {detail_preview} "
                    f"| {c['estimated_minutes']}분 |\n"
                )
            lines.append("\n")

        # Jira 신규/변경 목록
        changelog_items = [i for i in ms["items"]
                           if i.get("type") in ("changelog", "reporter")]
        if changelog_items:
            lines.append(f"**Jira 티켓 처리 ({len(changelog_items)}건):**\n\n")
            lines.append("| 날짜 | 유형 | 티켓 | 변경내용 | 추정 분 |\n")
            lines.append("|------|------|------|---------|--------|\n")
            for c in sorted(changelog_items, key=lambda x: x["date"])[:50]:
                detail_preview = (c.get("reason","") or "")[:50]
                lines.append(
                    f"| {c['date']} | {c['type']} | {c.get('key','')} "
                    f"| {detail_preview} | {c['estimated_minutes']}분 |\n"
                )
            if len(changelog_items) > 50:
                lines.append(f"| ... | | 외 {len(changelog_items)-50}건 | | |\n")
            lines.append("\n")

        # Confluence
        conf_items = [i for i in ms["items"] if i.get("source") == "confluence"]
        if conf_items:
            lines.append(f"**Confluence 작업 ({len(conf_items)}건):**\n\n")
            lines.append("| 날짜 | 유형 | Space | 제목 | 추정 분 |\n")
            lines.append("|------|------|-------|-----|--------|\n")
            for c in sorted(conf_items, key=lambda x: x["date"]):
                lines.append(
                    f"| {c['date']} | {c['type']} | {c.get('space','')} "
                    f"| {c['summary'][:45]} | {c['estimated_minutes']}분 |\n"
                )
            lines.append("\n")

        # Git 세션
        git_items = [i for i in ms["items"] if i.get("source") == "git-session"]
        if git_items:
            lines.append(f"**Git 코딩 세션 ({len(git_items)}세션):**\n\n")
            lines.append("| 날짜 | 레포 | 커밋수 | 주요 커밋 | 추정 분 |\n")
            lines.append("|------|------|-------|---------|--------|\n")
            for g in sorted(git_items, key=lambda x: x["date"]):
                commits_preview = "; ".join(
                    (s or "")[:30] for s in g.get("commit_summaries",[])[:2]
                )
                lines.append(
                    f"| {g['date']} | {g['repo']} | {g['commits']}건 "
                    f"| {commits_preview} | {g['estimated_minutes']}분 |\n"
                )
            lines.append("\n")

        lines.append("---\n\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.writelines(lines)
    print(f"\n  Markdown 리포트 저장: {OUT_MD}")


def save_json(report: Dict) -> None:
    # items 내 상세 내용은 제외한 요약만 저장 (파일 크기)
    summary_report = {
        "generated_at": report["generated_at"],
        "grand_total_minutes": report["grand_total_minutes"],
        "grand_total_hours": report["grand_total_hours"],
        "grand_total_by_source": report["grand_total_by_source"],
        "monthly": {
            m: {k: v for k, v in ms.items() if k != "items"}
            for m, ms in report["monthly"].items()
        },
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(summary_report, f, ensure_ascii=False, indent=2)
    print(f"  JSON 리포트 저장: {OUT_JSON}")


# ══════════════════════════════════════════════════════════════════
# 4. 실행
# ══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("cheoljoo.lee 2026 소요시간 분석 시작...")
    report = analyze()
    print_console(report)
    save_json(report)
    write_markdown(report)
    print("\n완료.")
