# =============================================================================
# worklog_tools/Makefile
# =============================================================================
# cheoljoo.lee 의 2026년 업무 활동 데이터 수집 및 시간 분석 자동화 Makefile
#
# ┌─────────────────────────────────────────────────────────────────────────┐
# │  스크립트 구성 (실행 순서)                                               │
# │                                                                         │
# │  [A] collect_cheoljoo_2026.py  ─┐                                       │
# │      : 메인 수집 스크립트        │→ collected_data/*.json                │
# │        Jira / Confluence /       │                                       │
# │        Gerrit / GitLab / git     │                                       │
# │                                  │                                       │
# │  [B] jira_confluence_collector.py│→ worklog_report.json (범용 수집기)   │
# │  [C] vcs_collector.py           ─┤→ vcs_report.json    (범용 수집기)   │
# │  [D] worklog_aggregator.py      ─┘→ worklog_reports/   (통합 리포트)   │
# │                                                                         │
# │  [E] analyze_worklog_time.py                                            │
# │      : 수집된 데이터를 읽어 시간 추정 리포트 생성                         │
# │        → collected_data/time_report.json                                │
# │        → collected_data/time_report_monthly.md                          │
# └─────────────────────────────────────────────────────────────────────────┘
#
# 사용법:
#   make              → 기본: 수집 + 분석 전체 실행 (all)
#   make collect      → [A] 메인 수집 스크립트만 실행
#   make analyze      → [E] 시간 분석 스크립트만 실행 (수집 데이터 필요)
#   make pipeline     → 수집 → 분석 순서대로 실행 (가장 일반적인 사용)
#   make jira-collect → [B] 범용 Jira/Confluence 수집기 실행
#   make vcs-collect  → [C] 범용 VCS(Gerrit/GitLab/git) 수집기 실행
#   make aggregate    → [D] 통합 집계기 실행 (Jira+VCS 합산 리포트)
#   make show         → 최근 분석 결과 요약 출력
#   make clean        → collected_data/ 하위 JSON/MD 파일 삭제 (주의!)
#   make help         → 이 도움말 출력
#
# 실행 환경:
#   - Python: uv run (pyproject.toml 기반 가상환경 자동 관리)
#   - 작업 디렉토리: 이 Makefile이 있는 worklog_tools/ 기준
# =============================================================================

# ── 실행 환경 설정 ────────────────────────────────────────────────────────────
# uv 를 사용하여 pyproject.toml 의 의존성을 자동으로 관리한다.
# uv 가 없으면 python3 으로 폴백한다.
UV         := $(shell command -v uv 2>/dev/null)
ifdef UV
  PYTHON   := uv run python
else
  PYTHON   := python3
  $(warning [경고] uv 가 설치되지 않았습니다. python3 으로 실행합니다.)
endif

# 이 Makefile 이 있는 디렉토리 (worklog_tools/)
TOOLS_DIR  := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

# pyproject.toml 이 있는 프로젝트 루트 (worklog_tools/ 의 부모)
PROJECT_DIR := $(abspath $(TOOLS_DIR)/..)

# 수집 결과가 저장되는 디렉토리
DATA_DIR   := $(TOOLS_DIR)collected_data

# ── 사용자/기간 설정 ──────────────────────────────────────────────────────────
# 필요하면 환경 변수로 덮어쓸 수 있다:
#   make collect SINCE=2026-03-01
USER       ?= cheoljoo.lee
SINCE      ?= 2026-01-01

# ── LGE 내부 서버 설정 (범용 수집기용) ───────────────────────────────────────
# 토큰/비밀번호는 git에 커밋하지 않는다. 환경 변수로 주거나,
# 이 Makefile과 같은 디렉토리에 (git에 추적되지 않는) make.key.mk 파일을 만들어
# 아래 변수들을 덮어쓰면 된다. 예: echo 'GITLAB_TOKEN := glpat-xxx' >> make.key.mk
-include make.key.mk

JIRA_HOST        ?= http://jira.lge.com/issue
JIRA_TOKEN       ?=
CONFLUENCE_HOST  ?= http://collab.lge.com/main
CONFLUENCE_TOKEN ?=
GERRIT_HOST      ?= http://gpro.lge.com
GERRIT_USER      ?= vspvs
GERRIT_PASS      ?=
GITLAB_HOST      ?= http://mod.lge.com/hub
GITLAB_TOKEN     ?=

# ── 출력 파일 경로 ────────────────────────────────────────────────────────────
JIRA_OUT         := $(TOOLS_DIR)worklog_report.json
VCS_OUT          := $(TOOLS_DIR)vcs_report.json
AGG_OUT_DIR      := $(TOOLS_DIR)worklog_reports
TIME_REPORT_JSON := $(DATA_DIR)/time_report.json
TIME_REPORT_MD   := $(DATA_DIR)/time_report_monthly.md

# =============================================================================
# 기본 타겟: pipeline (수집 → 분석)
# =============================================================================
.DEFAULT_GOAL := pipeline

.PHONY: all pipeline collect analyze \
        jira-collect vcs-collect aggregate \
        show clean help

# =============================================================================
# all: collect + analyze 전체 실행 (pipeline 과 동일)
# =============================================================================
all: pipeline

# =============================================================================
# pipeline: 메인 수집 → 시간 분석 순서로 실행
#
# 가장 자주 사용하는 타겟이다.
# 1. collect_cheoljoo_2026.py 로 모든 소스에서 데이터 수집
# 2. analyze_worklog_time.py 로 시간 추정 리포트 생성
# =============================================================================
pipeline: collect analyze
	@echo ""
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  파이프라인 완료"
	@echo "  결과 파일:"
	@echo "    JSON : $(TIME_REPORT_JSON)"
	@echo "    MD   : $(TIME_REPORT_MD)"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# =============================================================================
# collect: 메인 수집 스크립트 실행
#
# collect_cheoljoo_2026.py 를 실행하여 다음 소스에서 데이터를 수집한다:
#   - Jira      : http://jira.lge.com  (assignee/reporter/watcher/comment/changelog)
#   - Confluence: http://collab.lge.com/main  (생성/편집 페이지)
#   - Gerrit    : 9개 서버  (owner change, reviewer change, inline comment)
#   - GitLab    : http://mod.lge.com/hub  (push/merge/comment 이벤트)
#   - Local git : 7개 로컬 repo (git log --numstat)
#
# 출력 디렉토리: collected_data/
#   jira_activities.json      Jira 활동 (1,500건 내외)
#   confluence_activities.json Confluence 활동
#   gerrit_activities.json    Gerrit 활동 (개인계정 필요 시 0건)
#   gitlab_activities.json    GitLab 활동
#   git_activities.json       로컬 git 커밋
#   all_activities.json       전체 통합본
#   summary.json              소스별 건수 요약
#
# 소요 시간: 약 3~10분 (서버 응답 속도에 따라 다름)
# =============================================================================
collect:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  [A] 데이터 수집 시작"
	@echo "  사용자: $(USER)  /  기간: $(SINCE) ~"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd $(PROJECT_DIR) && $(PYTHON) $(TOOLS_DIR)collect_cheoljoo_2026.py

# =============================================================================
# analyze: 시간 추정 분석 스크립트 실행
#
# analyze_worklog_time.py 를 실행하여 collected_data/*.json 을 읽어
# 각 활동의 소요 시간을 추정하고 월별 리포트를 생성한다.
#
# 시간 추정 방식:
#   Jira comment  : 읽기 8분 + 작성 5분 + 1분/100자
#                   (Gerrit 자동 통합 comment 는 0분 — 이중계산 방지)
#   Jira changelog: 10~30분 (resolve/start 여부에 따라)
#   Confluence    : body 글자수 기반 (50자/분, 최소 20분)
#   Git commit    : 파일 유형·변경량 기반 세션 분석
#                   + 테스트 오버헤드 (C/C++ 25분, Python 15분, Config 10분)
#   Gerrit commit : 45분 (jira_key 추출, Jira 연동 확인)
#   Gerrit review : 읽기 10분 + inline comment당 5분 + 100자당 1분
#
# 출력:
#   collected_data/time_report.json         전체 상세 데이터
#   collected_data/time_report_monthly.md   월별 마크다운 리포트
#
# collect 타겟 실행 후에만 의미 있는 결과가 나온다.
# =============================================================================
analyze:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  [E] 시간 분석 시작"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd $(PROJECT_DIR) && $(PYTHON) $(TOOLS_DIR)analyze_worklog_time.py

# =============================================================================
# jira-collect: 범용 Jira/Confluence 수집기 실행
#
# jira_confluence_collector.py 를 실행한다.
# 이 스크립트는 인수를 직접 받는 범용 수집기로, 환경 변수로 서버/토큰을 지정한다.
#
# 필요 환경 변수:
#   JIRA_HOST        Jira 서버 URL  (예: http://jira.lge.com/issue)
#   JIRA_TOKEN       Jira Bearer 토큰 (Basic auth 시 base64 인코딩값)
#   CONFLUENCE_HOST  Confluence 서버 URL
#   CONFLUENCE_TOKEN Confluence 토큰
#
# 출력: worklog_report.json
#
# 예시:
#   make jira-collect JIRA_HOST=http://jira.lge.com/issue JIRA_TOKEN=xxx
# =============================================================================
jira-collect:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  [B] Jira/Confluence 범용 수집기 실행"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd $(PROJECT_DIR) && $(PYTHON) $(TOOLS_DIR)jira_confluence_collector.py \
		--users $(USER) \
		--since $(SINCE) \
		--output $(JIRA_OUT) \
		--no-ssl-verify \
		$(if $(JIRA_HOST),       --jira-host       $(JIRA_HOST)) \
		$(if $(JIRA_TOKEN),      --jira-token      $(JIRA_TOKEN)) \
		$(if $(CONFLUENCE_HOST), --confluence-host $(CONFLUENCE_HOST)) \
		$(if $(CONFLUENCE_TOKEN),--confluence-token $(CONFLUENCE_TOKEN))

# =============================================================================
# vcs-collect: 범용 VCS(Gerrit/GitLab/git) 수집기 실행
#
# vcs_collector.py 를 실행한다.
# Gerrit, GitLab, 로컬 git repo 를 지원하는 범용 수집기다.
#
# 필요 환경 변수:
#   GERRIT_HOST   Gerrit 서버 URL
#   GERRIT_USER   Gerrit 사용자명
#   GERRIT_PASS   Gerrit HTTP 비밀번호
#   GITLAB_HOST   GitLab 서버 URL
#   GITLAB_TOKEN  GitLab 개인 접근 토큰
#
# 출력: vcs_report.json
#
# 예시:
#   make vcs-collect GERRIT_HOST=http://gpro.lge.com GERRIT_USER=cheoljoo.lee
# =============================================================================
vcs-collect:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  [C] VCS 범용 수집기 실행"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	cd $(PROJECT_DIR) && $(PYTHON) $(TOOLS_DIR)vcs_collector.py \
		--users $(USER) \
		--since $(SINCE) \
		--output $(VCS_OUT) \
		--no-ssl-verify \
		$(if $(GERRIT_HOST),  --gerrit-host     $(GERRIT_HOST)) \
		$(if $(GERRIT_USER),  --gerrit-user     $(GERRIT_USER)) \
		$(if $(GERRIT_PASS),  --gerrit-password $(GERRIT_PASS)) \
		$(if $(GITLAB_HOST),  --gitlab-host     $(GITLAB_HOST)) \
		$(if $(GITLAB_TOKEN), --gitlab-token    $(GITLAB_TOKEN))

# =============================================================================
# aggregate: 통합 집계기 실행
#
# worklog_aggregator.py 를 실행한다.
# Jira, Confluence, Gerrit, GitLab 을 한꺼번에 수집하여
# 사용자별·날짜별로 집계한 통합 리포트를 생성한다.
#
# 출력: worklog_reports/ 디렉토리 (JSON + CSV)
#
# 예시:
#   make aggregate JIRA_HOST=http://jira.lge.com/issue JIRA_TOKEN=xxx \
#                  GERRIT_HOST=http://gpro.lge.com GERRIT_USER=cheoljoo.lee
# =============================================================================
aggregate:
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	@echo "  [D] 통합 집계기 실행"
	@echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
	mkdir -p $(AGG_OUT_DIR)
	cd $(PROJECT_DIR) && $(PYTHON) $(TOOLS_DIR)worklog_aggregator.py \
		--users $(USER) \
		--since $(SINCE) \
		--output-dir $(AGG_OUT_DIR) \
		--no-ssl-verify \
		$(if $(JIRA_HOST),        --jira-host        $(JIRA_HOST)) \
		$(if $(JIRA_TOKEN),       --jira-token       $(JIRA_TOKEN)) \
		$(if $(CONFLUENCE_HOST),  --confluence-host  $(CONFLUENCE_HOST)) \
		$(if $(CONFLUENCE_TOKEN), --confluence-token $(CONFLUENCE_TOKEN)) \
		$(if $(GERRIT_HOST),      --gerrit-host      $(GERRIT_HOST)) \
		$(if $(GERRIT_USER),      --gerrit-user      $(GERRIT_USER)) \
		$(if $(GERRIT_PASS),      --gerrit-password  $(GERRIT_PASS)) \
		$(if $(GITLAB_HOST),      --gitlab-host      $(GITLAB_HOST)) \
		$(if $(GITLAB_TOKEN),     --gitlab-token     $(GITLAB_TOKEN))

# =============================================================================
# show: 최근 분석 결과 요약 출력
#
# collected_data/time_report_monthly.md 의 내용을 터미널에 출력한다.
# 분석 결과를 빠르게 확인할 때 사용한다.
# =============================================================================
show:
	@if [ -f "$(TIME_REPORT_MD)" ]; then \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		echo "  분석 결과: $(TIME_REPORT_MD)"; \
		echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"; \
		cat $(TIME_REPORT_MD); \
	else \
		echo "[오류] $(TIME_REPORT_MD) 파일이 없습니다. 먼저 'make analyze' 를 실행하세요."; \
		exit 1; \
	fi

# =============================================================================
# clean: 수집 결과 파일 삭제
#
# collected_data/ 하위의 JSON 및 MD 파일을 삭제한다.
# 스크립트 파일 자체는 삭제하지 않는다.
#
# ※ 주의: 삭제 전에 확인 프롬프트가 표시된다.
#    강제 삭제: make clean FORCE=1
# =============================================================================
clean:
ifndef FORCE
	@echo "collected_data/ 하위 JSON/MD 파일을 삭제합니다."
	@echo "계속하려면 Enter, 취소하려면 Ctrl+C 를 누르세요."
	@read _
endif
	@echo "  삭제 중..."
	@find $(DATA_DIR) -maxdepth 1 \( -name "*.json" -o -name "*.md" \) -delete
	@rm -f $(JIRA_OUT) $(VCS_OUT)
	@echo "  완료."

# =============================================================================
# help: 도움말 출력
# =============================================================================
help:
	@echo ""
	@echo "┌─────────────────────────────────────────────────────────────────────┐"
	@echo "│  worklog_tools Makefile  —  사용 가능한 타겟                        │"
	@echo "├──────────────────┬──────────────────────────────────────────────────┤"
	@echo "│  make            │  pipeline (수집 → 분석) 전체 실행                │"
	@echo "│  make pipeline   │  collect → analyze 순서 실행                     │"
	@echo "│  make collect    │  [A] 메인 수집 스크립트 (Jira/Gerrit/Git 등)     │"
	@echo "│  make analyze    │  [E] 시간 추정 분석 및 월별 리포트 생성           │"
	@echo "│  make jira-collect│ [B] 범용 Jira/Confluence 수집기                 │"
	@echo "│  make vcs-collect│  [C] 범용 VCS(Gerrit/GitLab/git) 수집기          │"
	@echo "│  make aggregate  │  [D] 통합 집계기 (Jira+VCS 합산 리포트)          │"
	@echo "│  make show       │  최근 분석 결과 터미널 출력                       │"
	@echo "│  make clean      │  collected_data/ JSON/MD 삭제 (주의!)            │"
	@echo "│  make help       │  이 도움말 출력                                   │"
	@echo "├──────────────────┴──────────────────────────────────────────────────┤"
	@echo "│  변수 덮어쓰기 예시:                                                 │"
	@echo "│    make collect SINCE=2026-03-01                                     │"
	@echo "│    make jira-collect JIRA_HOST=http://jira.lge.com JIRA_TOKEN=xxx   │"
	@echo "│    make clean FORCE=1                                                │"
	@echo "└─────────────────────────────────────────────────────────────────────┘"
	@echo ""
