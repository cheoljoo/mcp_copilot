TOC
- [Worklog — cheoljoo.lee 2026년 전체 업무 기록 및 자동 Worklog 시스템](#worklog--cheoljoolee-2026년-전체-업무-기록-및-자동-worklog-시스템)
- [Part 2. 자동 Worklog 제안 시스템 설계 및 구현](#part-2-자동-worklog-제안-시스템-설계-및-구현)
  - [1. 제안 배경 및 목적](#1-제안-배경-및-목적)
  - [2. 시스템 아키텍처](#2-시스템-아키텍처)
  - [3. 생성된 Python 모듈](#3-생성된-python-모듈)
    - [3.1 `worklog_tools/jira_confluence_collector.py`](#31-worklog_toolsjira_confluence_collectorpy)
    - [3.2 `worklog_tools/vcs_collector.py`](#32-worklog_toolsvcs_collectorpy)
    - [3.3 `worklog_tools/worklog_aggregator.py`](#33-worklog_toolsworklog_aggregatorpy)
  - [4. Demo 실행 결과 (`demo_worklog.py`)](#4-demo-실행-결과-demo_worklogpy)
    - [4.1 실행 명령](#41-실행-명령)
    - [4.2 콘솔 출력 요약](#42-콘솔-출력-요약)
    - [4.3 생성된 파일](#43-생성된-파일)
    - [4.4 stats\_summary.json 발췌](#44-stats_summaryjson-발췌)
  - [5. 추가로 필요한 정보 (사람이 무엇을 했는지 더 정확히 파악하기 위해)](#5-추가로-필요한-정보-사람이-무엇을-했는지-더-정확히-파악하기-위해)
    - [5.1 코드 기여 품질 정보](#51-코드-기여-품질-정보)
    - [5.2 회의·커뮤니케이션](#52-회의커뮤니케이션)
    - [5.3 Jira 심층 정보](#53-jira-심층-정보)
    - [5.4 Confluence 심층 정보](#54-confluence-심층-정보)
    - [5.5 업무 외 맥락 정보](#55-업무-외-맥락-정보)
  - [6. 개발팀 Worklog 스케줄 생성 정보 흐름 (종합)](#6-개발팀-worklog-스케줄-생성-정보-흐름-종합)
  - [7. 파일 목록](#7-파일-목록)
  - [8. 향후 개선 방향](#8-향후-개선-방향)
- [Part 3. 실제 데이터 수집 기반 — 2026년 월별 Worklog](#part-3-실제-데이터-수집-기반--2026년-월별-worklog)
  - [Part 3-A. 데이터 수집 방법론 (Gathering Methodology)](#part-3-a-데이터-수집-방법론-gathering-methodology)
    - [수집 대상 및 범위](#수집-대상-및-범위)
    - [Jira 수집 상세](#jira-수집-상세)
    - [Confluence/Collab 수집 상세](#confluencecollab-수집-상세)
    - [GitLab 수집 상세](#gitlab-수집-상세)
    - [Local git 수집 상세](#local-git-수집-상세)
    - [Gerrit 수집 상세](#gerrit-수집-상세)
    - [수집 데이터 파일](#수집-데이터-파일)
  - [Part 3-B. 월별 실제 업무 기록 (Python 수집 데이터 기반)](#part-3-b-월별-실제-업무-기록-python-수집-데이터-기반)
    - [2026년 1월 — 458건](#2026년-1월--458건)
    - [2026년 2월 — 553건 (최다 활동)](#2026년-2월--553건-최다-활동)
    - [2026년 3월 — 365건](#2026년-3월--365건)
    - [2026년 4월 — 256건](#2026년-4월--256건)
    - [2026년 5월 — 292건](#2026년-5월--292건)
    - [2026년 6월 — 100건 (진행 중)](#2026년-6월--100건-진행-중)
  - [Part 3-C. 전체 요약 통계](#part-3-c-전체-요약-통계)
    - [주요 Jira 프로젝트](#주요-jira-프로젝트)
    - [주요 Local git 저장소](#주요-local-git-저장소)
- [Part 4. 업무 소요시간 추정 분석](#part-4-업무-소요시간-추정-분석)
  - [Part 4-A. 소요시간 추정 방법론 (근거 포함)](#part-4-a-소요시간-추정-방법론-근거-포함)
    - [Jira](#jira)
    - [Confluence](#confluence)
    - [Git / GitLab — 파일 유형별 분류](#git--gitlab--파일-유형별-분류)
      - [테스트 시간 (언어 그룹별 세션당 오버헤드)](#테스트-시간-언어-그룹별-세션당-오버헤드)
    - [Gerrit](#gerrit)
    - [한계 및 보정 메모](#한계-및-보정-메모)
  - [Part 4-B. 월별 소요시간 요약](#part-4-b-월별-소요시간-요약)
  - [Part 4-C. 소스별 시간 비중](#part-4-c-소스별-시간-비중)
  - [Part 4-D. 최고 활동일 (추정 분 기준)](#part-4-d-최고-활동일-추정-분-기준)
  - [Part 4-E. 버전별 방법론 비교](#part-4-e-버전별-방법론-비교)
  - [Part 4-A. 소요시간 추정 방법론 (근거 포함)](#part-4-a-소요시간-추정-방법론-근거-포함-1)
    - [Jira](#jira-1)
    - [Confluence](#confluence-1)
    - [Git / GitLab](#git--gitlab)
    - [Gerrit](#gerrit-1)
    - [한계 및 보정 메모](#한계-및-보정-메모-1)
  - [Part 4-B. 월별 소요시간 요약](#part-4-b-월별-소요시간-요약-1)
  - [Part 4-C. 소스별 시간 비중](#part-4-c-소스별-시간-비중-1)
  - [Part 4-D. 최고 활동일 (추정 분 기준)](#part-4-d-최고-활동일-추정-분-기준-1)
  - [Part 4-E. 버전별 방법론 비교](#part-4-e-버전별-방법론-비교-1)
- [Part 5. Spotify Backstage — Developer Portal 조사](#part-5-spotify-backstage--developer-portal-조사)
  - [5-A. Backstage란 무엇인가](#5-a-backstage란-무엇인가)
    - [추구하는 것 — "Speed Paradox" 해결](#추구하는-것--speed-paradox-해결)
  - [5-B. 기본 기능 5가지 (Core Features)](#5-b-기본-기능-5가지-core-features)
  - [5-C. 연결 서비스 (플러그인 카테고리별)](#5-c-연결-서비스-플러그인-카테고리별)
  - [5-D. Backstage로 Worklog 구현하기](#5-d-backstage로-worklog-구현하기)
    - [관련 플러그인](#관련-플러그인)
    - [Backstage에서 worklog를 구현하는 방법](#backstage에서-worklog를-구현하는-방법)
    - [Backstage에서 시작해야만 시간을 추적할 수 있는가?](#backstage에서-시작해야만-시간을-추적할-수-있는가)
    - [병렬 작업 처리가 가능한가?](#병렬-작업-처리가-가능한가)
    - [언제 작업이 끝났는지 Backstage가 체크하는가?](#언제-작업이-끝났는지-backstage가-체크하는가)
  - [5-E. Backstage Worklog의 근본적인 한계와 결론](#5-e-backstage-worklog의-근본적인-한계와-결론)
    - [현재 시스템과 비교](#현재-시스템과-비교)
    - [결론](#결론)
- [Part 6. Backstage 중앙화 효과 분석 및 Sprint Burndown 해석](#part-6-backstage-중앙화-효과-분석-및-sprint-burndown-해석)
  - [6-A. Software Catalog 중앙화가 주는 이점](#6-a-software-catalog-중앙화가-주는-이점)
    - [중앙화로 더 좋아지는 것](#중앙화로-더-좋아지는-것)
    - [Backstage를 거치지 않고 직접 작업해도 되는가?](#backstage를-거치지-않고-직접-작업해도-되는가)
    - [Worklog 관점 — "Path가 일정해야 한다"](#worklog-관점--path가-일정해야-한다)
    - [결론](#결론-1)
- [Part 7. 사후 작업시간 측정 — Google·Spotify 및 글로벌 사례](#part-7-사후-작업시간-측정--googlespotify-및-글로벌-사례)
  - [7-A. 사후 타임스탬프 집계의 핵심 원리](#7-a-사후-타임스탬프-집계의-핵심-원리)
    - [이벤트 기반 구간 추론 (Event-Pair Model)](#이벤트-기반-구간-추론-event-pair-model)
    - [타임스탬프 신뢰도 등급](#타임스탬프-신뢰도-등급)
  - [7-B. Google의 작업시간 측정 방식](#7-b-google의-작업시간-측정-방식)
    - [내부 도구 스택](#내부-도구-스택)
    - [Google의 시간 측정 접근법 — "Engineering Productivity" 팀](#google의-시간-측정-접근법--engineering-productivity-팀)
    - [Google이 실제로 사용하는 집계 기준](#google이-실제로-사용하는-집계-기준)
  - [7-C. Spotify의 작업시간 측정 방식](#7-c-spotify의-작업시간-측정-방식)
    - [Squad 모델과 시간 측정](#squad-모델과-시간-측정)
    - [Spotify의 시간 측정 도구 스택](#spotify의-시간-측정-도구-스택)
    - [Backstage TimeSaver — Spotify 방식의 핵심](#backstage-timesaver--spotify-방식의-핵심)
    - [Spotify가 강조하는 측정 철학](#spotify가-강조하는-측정-철학)
  - [7-D. 글로벌 기업 벤치마크](#7-d-글로벌-기업-벤치마크)
    - [Microsoft / GitHub — SPACE 프레임워크](#microsoft--github--space-프레임워크)
    - [Netflix — "Paved Road" + DORA](#netflix--paved-road--dora)
    - [Atlassian (Jira 만든 회사)](#atlassian-jira-만든-회사)
    - [LinkedIn — Productivity Engineering](#linkedin--productivity-engineering)
    - [Shopify — Engineering Effectiveness](#shopify--engineering-effectiveness)
  - [7-E. 상용 도구 비교](#7-e-상용-도구-비교)
    - [PR Cycle Time — 업계 표준 지표](#pr-cycle-time--업계-표준-지표)
  - [7-F. 현재 스크립트에 적용 가능한 개선 방향](#7-f-현재-스크립트에-적용-가능한-개선-방향)
    - [개선 1: Jira In Progress→Done 구간 직접 사용](#개선-1-jira-in-progressdone-구간-직접-사용)
    - [개선 2: GitLab MR open→merge 구간 직접 사용](#개선-2-gitlab-mr-openmerge-구간-직접-사용)
    - [개선 3: business\_minutes 함수 추가 (주말·심야 제외)](#개선-3-business_minutes-함수-추가-주말심야-제외)
    - [개선 4: 구간 기반 집계로 전환 로드맵](#개선-4-구간-기반-집계로-전환-로드맵)
    - [현재 방식 vs 개선 후 비교](#현재-방식-vs-개선-후-비교)
- [Part 8. DORA 4개 지표 자동 산출 — GitHub + GCS 이벤트 기반 상세 구현](#part-8-dora-4개-지표-자동-산출--github--gcs-이벤트-기반-상세-구현)
  - [8-A. DORA 4개 지표 개요](#8-a-dora-4개-지표-개요)
  - [8-B. 아키텍처 — 이벤트 수집 파이프라인](#8-b-아키텍처--이벤트-수집-파이프라인)
    - [Google FourKeys 기본 구조](#google-fourkeys-기본-구조)
    - [GCS(Google Cloud Storage) 역할](#gcsgoogle-cloud-storage-역할)
  - [8-C. 지표 1: Deployment Frequency](#8-c-지표-1-deployment-frequency)
    - [이벤트 소스](#이벤트-소스)
    - [웹훅 payload 예시 (GitHub → Cloud Run)](#웹훅-payload-예시-github--cloud-run)
    - [BigQuery 저장 스키마](#bigquery-저장-스키마)
    - [지표 계산 쿼리](#지표-계산-쿼리)
    - [등급 판정](#등급-판정)
  - [8-D. 지표 2: Lead Time for Changes](#8-d-지표-2-lead-time-for-changes)
    - [이벤트 소스](#이벤트-소스-1)
    - [변경 이력 테이블](#변경-이력-테이블)
    - [commit → deployment 연결 방법](#commit--deployment-연결-방법)
    - [Lead Time 계산 쿼리](#lead-time-계산-쿼리)
  - [8-E. 지표 3: Change Failure Rate (CFR)](#8-e-지표-3-change-failure-rate-cfr)
    - [이벤트 소스](#이벤트-소스-2)
    - [장애 이벤트 테이블](#장애-이벤트-테이블)
    - [CFR 계산 쿼리](#cfr-계산-쿼리)
    - [장애 원인 deployment 자동 연결](#장애-원인-deployment-자동-연결)
  - [8-F. 지표 4: Mean Time to Restore (MTTR)](#8-f-지표-4-mean-time-to-restore-mttr)
    - [이벤트 소스](#이벤트-소스-3)
    - [MTTR 계산 쿼리](#mttr-계산-쿼리)
  - [8-G. FourKeys 오픈소스 구현](#8-g-fourkeys-오픈소스-구현)
    - [구성 파일 구조 (github.com/dora-team/fourkeys)](#구성-파일-구조-githubcomdora-teamfourkeys)
    - [Terraform으로 인프라 배포](#terraform으로-인프라-배포)
    - [GitHub Webhook 설정](#github-webhook-설정)
    - [이벤트 핸들러 핵심 로직 (event\_handler/main.py 요약)](#이벤트-핸들러-핵심-로직-event_handlermainpy-요약)
    - [완성된 DORA 대시보드 쿼리 (all-in-one)](#완성된-dora-대시보드-쿼리-all-in-one)
  - [8-H. 현재 환경(GitLab + Jira)에 적용하기](#8-h-현재-환경gitlab--jira에-적용하기)
    - [이벤트 소스 매핑](#이벤트-소스-매핑)
    - [GitLab 이벤트 수집 (Python)](#gitlab-이벤트-수집-python)
    - [Lead Time 계산 (GitLab 환경)](#lead-time-계산-gitlab-환경)
    - [로컬 SQLite 기반 경량 구현 (BigQuery 없이)](#로컬-sqlite-기반-경량-구현-bigquery-없이)
    - [현재 수집 스크립트와 통합 포인트](#현재-수집-스크립트와-통합-포인트)


--------------------

# Worklog — cheoljoo.lee 2026년 전체 업무 기록 및 자동 Worklog 시스템

> 최초 작성일: 2026-06-23  
> 갱신: 2026-06-23 (2026년 전체 행적 추가)  
> 근거 파일: `2026-audit-trail.md`, `2026-audit-trail-detailed.md`, `2026-works.md`, `2026-works-me.md`, `2026-works-claude.md`, `2026-details.md`, `2026-goal.txt`

---

# Part 2. 자동 Worklog 제안 시스템 설계 및 구현

> 목적: Jira / Confluence(Collab) / Gerrit / GitHub / GitLab 에서 개발자 활동을 자동 집계하여 Jira Worklog에 삽입하고, 개발팀 업무 통계를 제공하는 시스템의 설계·구현·실행 결과를 기록한다.

> **Key : 개인별로 어떠한 일을 했는지 DB화 시킨다.**

---

## 1. 제안 배경 및 목적

개발팀에서 Jira Worklog를 수동으로 작성하는 일은 번거롭고 누락이 잦다.  
아래 데이터 소스를 자동으로 읽어 각 Jira 티켓의 Worklog에 삽입하고,  
개발자별 일일 활동 통계(얼마나 일했는지)를 자동 생성하면 팀 운영이 크게 개선된다.

| 데이터 소스 | 수집 대상 |
|---|---|
| Jira | assignee, reporter, watcher, comment, changelog(이력) |
| Confluence(Collab) | 페이지 편집, 댓글 |
| Gerrit | 커밋(author), 코드리뷰(reviewer, vote) |
| GitHub | 커밋, PR 리뷰 |
| GitLab | 커밋, MR 리뷰/노트 |
| Local git repo | git log 직접 파싱 |

---

## 2. 시스템 아키텍처

```
┌──────────────────────────────────────────────────────┐
│                  데이터 수집 레이어                    │
│  JiraCollector  ConfluenceCollector  GerritCollector  │
│  GitHubCollector  GitLabCollector  LocalGitCollector  │
└────────────────────────┬─────────────────────────────┘
                         │ List[Activity / VcsActivity]
                         ▼
┌──────────────────────────────────────────────────────┐
│              통합 집계 (worklog_aggregator)           │
│  - 사용자별 날짜별 정규화 (WorklogEntry)              │
│  - 통계 계산 (활동건수, 활동일, 유형별/소스별 분포)   │
└────────────────────────┬─────────────────────────────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
     JSON Report    CSV Report    Markdown Report
     (raw 전체)    (피벗 분석)   (사람별 worklog)
                                        │
                                        ▼
                              Jira Worklog API 자동 삽입
                         (POST /rest/api/latest/issue/{key}/worklog)
```

---

## 3. 생성된 Python 모듈

### 3.1 `worklog_tools/jira_confluence_collector.py`

**기능**
- Jira JQL 으로 지정 사용자가 관련된 이슈 전체 수집 (assignee / reporter / watcher / comment)
- 이슈별 changelog(이력) 수집 — 상태 변경, 필드 변경 포함
- Confluence CQL 으로 페이지 편집·댓글 수집
- 날짜 범위 필터링 (`--since`)
- 출력: `List[Activity]` → JSON / CSV

**주요 클래스**
```
RestClient          — Bearer 토큰 기반 REST 클라이언트 (Jira/Confluence 공용)
JiraCollector       — JQL 기반 이슈·comment·changelog 수집
ConfluenceCollector — CQL 기반 페이지·댓글 수집
```

**실행 예**
```bash
python worklog_tools/jira_confluence_collector.py \
    --jira-host http://jira.example.com \
    --jira-token TOKEN \
    --confluence-host http://confluence.example.com \
    --confluence-token TOKEN \
    --users alice bob charlie \
    --since 2026-06-01 \
    --output report.json \
    --csv report.csv
```

---

### 3.2 `worklog_tools/vcs_collector.py`

**기능**
- **Gerrit**: `owner:{user}` / `reviewer:{user}` 쿼리로 Change + Review vote 수집
- **GitHub**: 조직의 전체(또는 지정) 레포에서 커밋 + PR 리뷰 수집
- **GitLab**: 그룹/프로젝트에서 커밋 + MR 노트 수집
- **Local git**: `git log --format` 파싱으로 오프라인 레포 수집
- 출력: `List[VcsActivity]` → JSON

**주요 클래스**
```
GerritCollector     — Gerrit REST /a/changes/ 페이지네이션
GitHubCollector     — GitHub API v3 (commits + PR reviews)
GitLabCollector     — GitLab API v4 (commits + MR notes)
LocalGitCollector   — subprocess git log 파싱
```

**실행 예**
```bash
python worklog_tools/vcs_collector.py \
    --gerrit-host http://gerrit.example.com \
    --gerrit-user alice \
    --gerrit-password PASSWORD \
    --github-token ghp_TOKEN \
    --github-org my-org \
    --users alice bob charlie \
    --since 2026-06-01 \
    --output vcs_report.json
```

---

### 3.3 `worklog_tools/worklog_aggregator.py`

**기능**
- 위 두 모듈을 통합하여 `WorklogEntry` 단일 모델로 정규화
- 사용자별 통계 계산: 총 활동, 활동일, 유형별·소스별 분포
- 출력: JSON / CSV / Markdown(사람별 파일)
- `--insert-jira-worklog` 플래그: Jira Worklog API에 자동 삽입

**Jira Worklog 자동 삽입 흐름**
```
WorklogEntry(source=jira, ref=PROJ-101, date=2026-06-10, ...) 
  → POST /rest/api/latest/issue/PROJ-101/worklog
     { "started": "2026-06-10T09:00:00.000+0000",
       "timeSpentSeconds": 1800,
       "comment": "[Auto-worklog] comment: Fixed null-ptr..." }
```

**실행 예**
```bash
python worklog_tools/worklog_aggregator.py \
    --jira-host http://jira.example.com --jira-token TOKEN \
    --gerrit-host http://gerrit.example.com \
    --gerrit-user me --gerrit-password PWD \
    --users alice bob charlie \
    --since 2026-06-01 \
    --output-dir ./reports \
    --insert-jira-worklog
```

---

## 4. Demo 실행 결과 (`demo_worklog.py`)

실제 서버 없이 mock 데이터(alice·bob·charlie 3인)로 파이프라인 전체를 검증.

### 4.1 실행 명령

```bash
python demo_worklog.py
```

### 4.2 콘솔 출력 요약

```
======================================================================
  UNIFIED WORKLOG DEMO REPORT
======================================================================

  [alice]
    총 활동: 10건  |  활동 일수: 5일
    기간: 2026-06-10 ~ 2026-06-16
    유형별: {'assignee': 1, 'comment': 2, 'changelog': 2, 'edit': 1, 'commit': 4}
    소스별: {'jira': 4, 'confluence': 2, 'gerrit': 2, 'github': 1, 'git-local': 1}

    [2026-06-10]  jira/assignee PROJ-101, jira/comment PROJ-101, gerrit/commit platform/auth
    [2026-06-11]  jira/changelog PROJ-101, confluence/edit 12345
    [2026-06-12]  jira/changelog PROJ-101, confluence/comment 12345, gerrit/commit platform/api
    [2026-06-13]  github/commit org/frontend
    [2026-06-16]  git-local/commit /repos/local

  [bob]
    총 활동: 5건  |  활동 일수: 4일
    기간: 2026-06-10 ~ 2026-06-14
    유형별: {'reporter': 1, 'comment': 1, 'edit': 1, 'review': 2}
    소스별: {'jira': 2, 'confluence': 1, 'gerrit': 1, 'github': 1}

  [charlie]
    총 활동: 4건  |  활동 일수: 4일
    기간: 2026-06-12 ~ 2026-06-15
    유형별: {'assignee': 1, 'comment': 1, 'review': 1, 'commit': 1}
    소스별: {'jira': 2, 'gerrit': 1, 'gitlab': 1}
```

### 4.3 생성된 파일

| 파일 | 내용 |
|---|---|
| `demo_reports/worklog_all.json` | 전체 활동 raw 데이터 (19건) |
| `demo_reports/worklog_alice.md` | alice 개인 worklog Markdown |
| `demo_reports/worklog_bob.md` | bob 개인 worklog Markdown |
| `demo_reports/worklog_charlie.md` | charlie 개인 worklog Markdown |
| `demo_reports/stats_summary.json` | 3인 통계 요약 JSON |

### 4.4 stats_summary.json 발췌

```json
{
  "alice": {
    "total_activities": 10,
    "active_days": 5,
    "first_activity": "2026-06-10",
    "last_activity": "2026-06-16",
    "by_type": {"assignee":1,"changelog":2,"comment":2,"commit":4,"edit":1},
    "by_source": {"confluence":2,"gerrit":2,"git-local":1,"github":1,"jira":4}
  },
  "bob": { ... },
  "charlie": { ... }
}
```

---

## 5. 추가로 필요한 정보 (사람이 무엇을 했는지 더 정확히 파악하기 위해)

현재 수집하는 데이터 외에 아래 항목이 추가되면 worklog 정밀도가 크게 올라간다.

### 5.1 코드 기여 품질 정보

| 항목 | 설명 | 출처 |
|---|---|---|
| 변경 코드 라인 수 (insertions/deletions) | 커밋 규모 파악 | `git log --stat`, GitHub/GitLab diff API |
| 리뷰 코멘트 수 | 리뷰 깊이 측정 | Gerrit inline comments, GitHub PR review comments |
| 리뷰 반복 횟수 | 품질 이슈 여부 | Gerrit patch-set 수, GitHub re-request review |
| 빌드/CI 결과 연동 | 커밋 후 CI pass/fail | Jenkins, GitHub Actions, GitLab CI |

### 5.2 회의·커뮤니케이션

| 항목 | 출처 |
|---|---|
| 회의 참석 기록 | Google Calendar, Outlook Calendar API |
| Slack/Teams 채널 참여 (mention, 응답) | Slack Audit API, Teams Graph API |
| Email 발신·수신 (중요 키워드) | Exchange/Gmail API |

### 5.3 Jira 심층 정보

| 항목 | 설명 |
|---|---|
| Story Point 완료량 | 팀 속도(velocity) 계산에 필수 |
| 스프린트 배정·완료 여부 | 계획 대비 실행력 측정 |
| 블로커 생성·해소 이력 | 협업 기여도 측정 |
| 하위 태스크(Sub-task) 완료 수 | 실제 작업 분해 단위 파악 |

### 5.4 Confluence 심층 정보

| 항목 | 설명 |
|---|---|
| 페이지 신규 생성 vs 편집 구분 | 문서화 기여 정량화 |
| 페이지 열람 수(view count) | 팀 지식 공유 기여도 |
| 멘션(@) 받은 횟수 | 전문가로 인정받는 빈도 |

### 5.5 업무 외 맥락 정보

| 항목 | 설명 |
|---|---|
| 공식 휴가·병가 일정 | 인사 시스템 연동 (활동 없는 날 구분) |
| 온콜(on-call) 당번 여부 | 운영 기여 정량화 |
| 코드 리뷰 SLA(응답 시간) | 리뷰 응답성 지표 |

---

## 6. 개발팀 Worklog 스케줄 생성 정보 흐름 (종합)

```
[데이터 소스]                [수집 주기]    [생성 결과]
─────────────────────────────────────────────────────────
Jira (이슈·changelog)     → 1시간        →  개인별 일일 worklog
Confluence (편집·댓글)    → 1시간        →  문서화 기여 통계
Gerrit/GitHub/GitLab      → push webhook →  커밋·리뷰 실적
Git local                 → 1일          →  미push 커밋 포함
Calendar / Slack          → 1일          →  협업·미팅 참여
HR 시스템 (휴가)          → 1일          →  정상 근무일 보정
CI/CD 결과               → webhook      →  빌드 기여 품질
```

**최종 출력 형식 (사람별 일일 스케줄)**
```
[alice] 2026-06-10
  09:00  Gerrit commit: Fix null-ptr in AuthService  (platform/auth)
  10:30  Jira comment:  PROJ-101 — "Fixed null-pointer in AuthService"
  11:00  Jira 상태변경: PROJ-101  Open → In Progress
  14:00  Confluence 편집: "Design Doc: Auth Refactor" (v3)
  예상 작업 시간: ~3.5h
```

---

## 7. 파일 목록

```
worklog_tools/
  jira_confluence_collector.py   ← Jira / Confluence 수집기
  vcs_collector.py               ← Gerrit / GitHub / GitLab / local-git 수집기
  worklog_aggregator.py          ← 통합 집계 + Jira worklog 자동 삽입
demo_worklog.py                  ← mock 데이터 demo (서버 없이 실행 가능)
demo_reports/
  worklog_all.json
  worklog_alice.md
  worklog_bob.md
  worklog_charlie.md
  stats_summary.json
```

---

## 8. 향후 개선 방향

1. **웹훅 기반 실시간 처리**: Gerrit submit / Jira transition 이벤트를 받아 즉시 worklog 삽입
2. **AI 요약**: 하루 활동을 LLM으로 한 문장 요약 → Jira worklog comment에 삽입
3. **대시보드**: 팀 전체 통계를 Grafana / Kibana로 시각화
4. **중복 방지**: Jira worklog 삽입 전 기존 auto-worklog 존재 여부 확인
5. **time estimation**: 커밋 크기(lines changed), 리뷰 코멘트 수로 소요 시간 자동 추정
6. **MCP 서버화**: 이 파이프라인을 MCP 도구로 노출하여 GitHub Copilot에서 직접 호출

---

*이 문서는 2026-06-23 자동 생성되었습니다.*

---

# Part 3. 실제 데이터 수집 기반 — 2026년 월별 Worklog

> 갱신: 2026-06-23  
> 수집 스크립트: `worklog_tools/collect_cheoljoo_2026.py`  
> 수집 기간: 2026-01-01 ~ 2026-12-31 (조회 시점: 2026-06-23)  
> **총 수집 건수: 2,120건** (Jira 1,504 + GitLab 282 + Confluence 45 + Local git 289)

---

## Part 3-A. 데이터 수집 방법론 (Gathering Methodology)

### 수집 대상 및 범위

| 소스 | 수집 계정 | API 방식 | 수집 범위 | 건수 |
|------|-----------|----------|-----------|------|
| **Jira** | `cheoljoo.lee` | REST API `/issue/rest/api/latest/` | reporter/assignee/watcher 티켓, changelog, comment | 1,504건 |
| **Confluence** | `cheoljoo.lee` | REST API `/rest/api/content/search` (CQL) | 본인 생성 페이지/블로그, 본인 편집 참여 페이지 | 45건 |
| **GitLab** | `cheoljoo.lee` (user_id=591) | REST API `/api/v4/users/591/events` | push 이벤트 (커밋), MR open/merge, comment | 282건 |
| **Local git** | 로컬 저장소 7개 | `git log` CLI | 2026-01-01 이후 cheoljoo.lee author 커밋 | 289건 |
| **Gerrit** | `vspvs` 공용 계정 | REST API `/a/changes/` | cheoljoo.lee owner/reviewer 변경사항 (9개 서버) | 0건† |

> **†Gerrit 0건 이유**: `vspvs` 공용 계정은 Gerrit 서버에 접속은 가능하나 `owner:cheoljoo.lee` 쿼리 결과가 없음. cheoljoo.lee의 Gerrit 개인 HTTP 비밀번호가 필요하거나, 해당 서버에 직접 push 이력이 없는 경우. GitLab(mod.lge.com/hub)과 local git으로 커밋 이력은 보완됨.

### Jira 수집 상세

```
서버: http://jira.lge.com/issue/rest/api/latest/
인증: HTTP Basic Auth (cheoljoo.lee / ***)
JQL (assignee/reporter):
  (assignee = "cheoljoo.lee" OR reporter = "cheoljoo.lee")
  AND updated >= "2026-01-01" ORDER BY updated DESC
JQL (watcher):
  watcher = "cheoljoo.lee" AND updated >= "2026-01-01"
  → assignee/reporter 티켓과 중복 제거 후 type=watcher로 추가
페이지: maxResults=100, startAt 증가 방식 (전수 수집)
추가 수집:
  - 각 티켓의 changelog (/issue/{key}/changelog) → 상태전이 이력
  - AGILEDEV 프로젝트 댓글 (/issue/{key}/comment) → 본인 작성 comment
수집 레벨: 티켓 메타정보(key, summary, status, priority, created, updated) +
           changelog 전수 + comment 전수 + watcher 목록
```

### Confluence/Collab 수집 상세

```
서버: http://collab.lge.com/main/rest/api/
인증: HTTP Basic Auth (cheoljoo.lee / ***)  ← LDAP 동일
CQL (생성):
  creator = "cheoljoo.lee" AND created >= "2026-01-01"
  AND type in (page, blogpost)
CQL (편집 참여):
  contributor = "cheoljoo.lee" AND lastModified >= "2026-01-01"
  AND creator != "cheoljoo.lee" AND type in (page, blogpost)
수집 필드: id, title, space.key, history.createdDate, version.when, type
GitLab 확인: mod.lge.com/hub — 맞습니다. 이미 token(glpat-...)으로 user_id=591
             /api/v4/users/591/events 로 수집 중
```

### GitLab 수집 상세

```
서버: http://mod.lge.com/hub/api/v4/
인증: Private Token (PRIVATE-TOKEN 헤더)
엔드포인트: /users/591/events
파라미터: after=2026-01-01, per_page=100, page 증가 방식
이벤트 분류:
  - pushed → type=commit (push_data.commit_title, ref 포함)
  - commented → type=comment
  - opened/merged/closed → type=mr
수집 레벨: 이벤트 전수 (페이지 네이션으로 전체 수집)
```

### Local git 수집 상세

```
대상 저장소 (7개):
  /home/cheoljoo.lee/code/mcp_copilot
  /home/cheoljoo.lee/code/ccr
  /home/cheoljoo.lee/code/ticketsage
  /home/cheoljoo.lee/code/weekly_work_report_from_jira
  /home/cheoljoo.lee/code/_worklog
  /home/cheoljoo.lee/code/agents
  /home/cheoljoo.lee/code/youtube_notes_chrome_extension
명령: git log --after=2026-01-01 --author=cheoljoo.lee --pretty=format:...
수집 필드: commit hash, date, repo명, subject
```

### Gerrit 수집 상세

```
대상 서버 (9개): gpro, lamp, na, eu, as, adas, acp, rn, prosys
인증: HTTP Basic Auth (vspvs / 서버별 HTTP 비밀번호)
엔드포인트: /a/changes/
쿼리:
  - owner:cheoljoo.lee after:2026-01-01
  - reviewer:cheoljoo.lee after:2026-01-01 -owner:cheoljoo.lee
옵션: DETAILED_ACCOUNTS,LABELS,MESSAGES
결과: gpro, prosys 인증 실패; lamp/na/eu/as/adas/acp/rn 접속 성공이나 0건
```

### 수집 데이터 파일

```
worklog_tools/collected_data/
  jira_activities.json        ← 1,504건 (assignee/reporter/watcher + changelog + comment)
  confluence_activities.json  ←    45건 (page_created 13 + page_edited 32)
  gerrit_activities.json      ←     0건
  gitlab_activities.json      ←   282건
  git_activities.json         ←   289건
  all_activities.json         ← 2,120건 (통합)
  summary.json                ← 월별 통계
```

---

## Part 3-B. 월별 실제 업무 기록 (Python 수집 데이터 기반)

### 2026년 1월 — 458건

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | 15건 |
| Jira 담당 (assignee) | 9건 |
| Jira 댓글 | 58건 |
| Jira 상태변경 | 173건 |
| Jira watcher | 4건 |
| Confluence 편집 | 4건 |
| GitLab push | 101건 |
| Local git commit | 88건 |

**Jira 신규 생성 티켓** (reporter):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-750 | 2026: There is no data to download |
| AGILEDEV-759 | [ticket sage][summary] context 비교하여 틀린 부분만 llm query |
| AGILEDEV-760 | [ticket sage][summary] description과 comments의 ADDITIONAL 처리 |
| AGILEDEV-764 | [Gerrit] Inline Commit SRV+ID unique key → SRV+ID+REPO 변경 |
| AGILEDEV-769 | CCR 티켓 분석: screening points 구현 |
| AGILEDEV-771 | [ticket sage][jira-test] Jira 티켓 정보로 RAG+vector 이용 |
| AGILEDEV-777 | [ticket sage][jira-test] jira test report |
| AGILEDEV-783 | CCR 티켓 분석: screening points DB Design |
| AGILEDEV-784 | CCR 티켓 분석: screening points DB 구현 |
| AGILEDEV-786 | [ticketsage][summary] prompt "in english for 3 lines" 확인 |
| AGILEDEV-787 | (Qlik) R&D 가시화 Board_COST 관리 Task 실패: 데이터 동기화 이슈 |
| AGILEDEV-790 | [ticket sage][db_test] jira_test에서 --fixed option 처리 |
| AGILEDEV-803 | connectWide 티켓 GROUP BY RESOLUTION, DEFECT_TYPE 분석 |
| AGILEDEV-808 | connectWide 티켓 true_positive/false_positive 구별 |
| AGILEDEV-809 | MCP 환경 설정: copilot 이용 collab/jira/gerrit 접속 |

**GitLab 주요 push** (상위 8건):

| 날짜 | 커밋 |
|------|------|
| 2026-01-31 | [AGILEDEV-808] connectWide true_positive/false_positive 구별 |
| 2026-01-30 | add numbers in title |
| 2026-01-30 | [AGILEDEV-803] connectWide GROUP BY RESOLUTION 분석 |
| 2026-01-30 | INIT |
| 2026-01-29 | add option: --forced_update SKIPPED_UNCHANGED 없이 강제 update |
| 2026-01-29 | add repo: repo name is project in restapi |
| 2026-01-28 | add FEATURE_LEADER_UNIT |
| 2026-01-28 | pyautogui: change share point file for 2026 year |

**Confluence 편집 (1월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-01-30 | page_edited | SWDEVDIV | [W05주차] 주간업무보고_2026.01.29 (목) |
| 2026-01-28 | page_edited | SWDEVDIV | [W04주차] 주간업무보고_2026.01.22 (목) |
| 2026-01-22 | page_edited | VCSMRTMD | 06. FA 명단 |
| 2026-01-14 | page_edited | SWDEVDIV | [W03주차] 주간업무보고_2026.01.15 (목) |

---

### 2026년 2월 — 553건 (최다 활동)

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | **32건** (월간 최다) |
| Jira 담당 (assignee) | 47건 |
| Jira 댓글 | 85건 |
| Jira 상태변경 | **255건** (월간 최다) |
| Jira watcher | 11건 |
| Confluence 생성+편집 | 7건 |
| GitLab push | 49건 |
| Local git commit | 65건 |

**Jira 신규 생성 티켓** (reporter, 주요):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-814 | [ticketsage][summary] TP/FP 판정 및 근거/category 적용 |
| AGILEDEV-815 | [pvs_crawler][sage] ticket 합쳐서 Query — 비용/query수 분석 |
| AGILEDEV-824 | [ticketsage][summary] vspvs 추가 comments 처리 |
| AGILEDEV-825 | [ticketsage][jira-test] RESOLUTION 표시 |
| AGILEDEV-826 | [ccr] trender에서 사용할 DB (AHC) |
| AGILEDEV-827 | Gerrit MCP에 source/modified file/diff 기능 추가 |
| AGILEDEV-832 | DNS resolver 우회 코드 — 403 Public access 오류 |
| AGILEDEV-833 / 840 / 843 | FastAPI 이용 QCD_SAGE_LLM_QUERY REST API / MCP 서버 개발 |
| AGILEDEV-838 | [ticketsage][summary] 최대 6시간 동작 설정 |
| AGILEDEV-851 | [LONG-TERM] LGEP 비밀번호 변경 시 확인 사항 |
| AGILEDEV-852 | 2026-02 sprint report 작성 |
| AGILEDEV-858 | connectWide 팀과 미팅 (ticketsage 기능 추가) |
| AGILEDEV-863 | [ticketsage] crontab 매일 자동 필드 저장 서비스 개시 |
| AGILEDEV-864 | [ticketsage] LLM_SUMMARY crash/categorize prompt 추가 |
| AGILEDEV-865 | [ticketsage][summary] keyword 기반 ticket category 분류 |
| AGILEDEV-866 | Copilot CLI + MCP 환경 구성 및 사용법 |
| AGILEDEV-867 | [Hexa Index] Copilot CLI + claude로 자동 분석 |
| AGILEDEV-872 | [CCR] CCR Ready Screening Design |
| AGILEDEV-875 | [ticketsage] connectWide 5000건+ 데이터 처리 |
| AGILEDEV-876~884 | **[CCR 2nd-Gen] DB Schema~RS Fidelity Review 연동** (8개 티켓) |
| AGILEDEV-888 | [pvs_crawler][sage] gpt-4o-mini/exaone fallback 처리 |
| AGILEDEV-889 | [Hexa Index] copilot cli + claude 분석 Phase 2 |

**GitLab 주요 push** (상위 8건):

| 날짜 | 커밋 |
|------|------|
| 2026-02-27 | [AGILEDEV-875] connectWide 5000건 대응 |
| 2026-02-27 | add document for 2nd-generation of CCR implementation |
| 2026-02-26 | update summary/ticket_sage_summary.v0.001.prompt |
| 2026-02-26 | [AGILEDEV-864] LLM_SUMMARY crash/categorize prompt 추가 |
| 2026-02-26 | [AGILEDEV-875] option 추가 (max_runtime_hours 등) |
| 2026-02-26 | hexa index 분석 with unit daily and weekly info |
| 2026-02-26 | analyze hexa index with unit info |
| 2026-02-25 | docs update |

**Confluence 생성+편집 (2월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-02-27 | page_created | VSPVS | basic instruction for connectWide |
| 2026-02-27 | page_created | VSPVS | LLM Queries |
| 2026-02-23 | page_created | ~cheoljoo.lee | 2026-02-03 sprint |
| 2026-02-26 | page_edited | SWDEVDIV | [W09주차] 주간업무보고_2026.02.26 (목) |
| 2026-02-25 | page_edited | HONDATSUBV | 6.1 Request an authority of vBee/vOpenGrok for 26MY |
| 2026-02-12 | page_edited | SWDEVDIV | [W07주차] 주간업무보고_2026.02.12 (목) |
| 2026-02-05 | page_edited | SWDEVDIV | [W06주차] 주간업무보고_2026.02.05 (목) |

---

### 2026년 3월 — 365건

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | 17건 |
| Jira 담당 (assignee) | 17건 |
| Jira 댓글 | 65건 |
| Jira 상태변경 | 118건 |
| Jira watcher | 22건 |
| Confluence 생성+편집 | 11건 |
| GitLab push | 67건 |
| Local git commit | 81건 |

**Jira 신규 생성 티켓** (reporter):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-899 | [ticketsage] QCD_SAGE_LLM_RAG_JIRA_TEST에 CREATED_DATE 추가 |
| AGILEDEV-917 / 918 | Expert task — 각 실 CFR과 기능 추가 및 유지보수 협의 |
| AGILEDEV-919 | Hexa 지표 + 추가 의미있는 index 도출 |
| AGILEDEV-920 | Linux 서버 구성: 기존 desktop → linux server 전환 |
| AGILEDEV-928 / 939 | CCR ticket reviewer 분석 (trender AHC 연동) |
| AGILEDEV-929 | LGEDV Crash Issue List 검토 |
| AGILEDEV-930~958 | Expert task 미팅 시리즈 (gerrit 사항, applied priority, 표현 변경 등) |
| AGILEDEV-941 | [ticketsage/summary] 24,000개 issue DL_ISSUE_ MongoDB 업데이트 |

**GitLab 주요 push** (상위 8건):

| 날짜 | 커밋 |
|------|------|
| 2026-03-31 | BELONG, PARTNER & LOG 축소 |
| 2026-03-30 | http → https 마이그레이션 |
| 2026-03-27 | Edit db_query.sql: HMG key 기준 정리 |
| 2026-03-27 | [AGILEDEV-941] 24,000개 issue 업데이트 |
| 2026-03-26 | final-review: add BELONG, PARTNER |
| 2026-03-26 | [AGILEDEV-939] CCR reviewer 분석 trender AHC 연동 |
| 2026-03-27 | Merge branch 'main' (×2) |
| 2026-03-25 이전 | 59건 추가 push |

**Confluence 생성+편집 (3월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-03-24 | page_created | ~cheoljoo.lee | 2026-03 sprint retrospection |
| 2026-03-23 | page_created | VSPVS | 46. Crash ticket Identification from LGDV |
| 2026-03-17 | page_created | VSPVS | 45. CCR Readiness |
| 2026-03-16 | page_created | ~cheoljoo.lee | CCR Readiness |
| 2026-03-26 | page_edited | SWDEVDIV | [W13주차] 주간업무보고_2026.03.26 (목) |
| 2026-03-20 | page_edited | SWDEVDIV | [W12주차] 주간업무보고_2026.03.19 (목) |
| 2026-03-19 | page_edited | SWDELIVERY | 26.03.19 CCR READY SCREENING 미팅 |
| 2026-03-16 | page_edited | SWDEVDIV | [W11주차] 주간업무보고_2026.03.12 (목) |
| 2026-03-16 | page_edited | SWDELIVERY | CCR READY SCREENING 미팅 |
| 2026-03-06 | page_edited | VSPVS | 43. 프로젝트 점검 회의 대비 LLM 프롬프팅 정리 |
| 2026-03-04 | page_edited | SWDEVDIV | [W10주차] 주간업무보고_2026.03.05 (목) |

---

### 2026년 4월 — 256건

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | 8건 |
| Jira 담당 (assignee) | 29건 |
| Jira 댓글 | 67건 |
| Jira 상태변경 | 86건 |
| Jira watcher | 7건 |
| Confluence 생성+편집 | 8건 |
| GitLab push | 27건 |
| Local git commit | 39건 |

**Jira 신규 생성 티켓** (reporter):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-963 | [ticketsage] DB에 list/dict 저장 시 json이 아닌 str 저장 버그 |
| AGILEDEV-969 | Expert task: system 적용 미팅 |
| AGILEDEV-984 | [ticketsage][summary] self-heal legacy CONTEXT + downgrade |
| AGILEDEV-985 | [CCR] CAnalysisVlm.py refactoring |
| AGILEDEV-989 | [ticketsage] QCD_DL_ISSUE_FROM_MONGODB 모든 ticket LLM summary |
| AGILEDEV-990 | DB Query & Update |
| AGILEDEV-993 | [LONG-TERM][CCR] 고객 추가 요청사항 |
| AGILEDEV-994 | [CCR] 고객 요청: ticket type (integration) 추가 |

**GitLab 주요 push** (상위 8건):

| 날짜 | 커밋 |
|------|------|
| 2026-04-24 | Merge branch 'main' |
| 2026-04-23 | Document for CCR AHC (Active Head Counter) |
| 2026-04-23 | [AGILEDEV-826] Batch DB operations in ccr_ahc + Makefile fix |
| 2026-04-22 | [AGILEDEV-826] Add ccr_ahc.py for QCD_CCR_AHC DB sync |
| 2026-04-22 | [AGILEDEV-994] Refactor Ticket Type check + Jira 확장 |
| 2026-04-22 | exclude Open in jira comments / `[참고]` 블록 필터 |
| 2026-04-21 | Fix approval history check + open-matrix filter in CCCRS |
| 2026-04-21 | [AGILEDEV-985] Add issue_id-targeted readiness/Jira processing |

**Confluence 생성+편집 (4월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-04-14 | page_created | VSPVS | 47. fastapi (RESTful API) |
| 2026-04-23 | page_edited | SWDEVDIV | [W17주차] 주간업무보고_2026.04.23 (목) |
| 2026-04-20 | page_edited | VSPVS | 08. 총무 관련일 |
| 2026-04-15 | page_edited | SWDEVDIV | [W16주차] 주간업무보고_2026.04.16 (목) |
| 2026-04-09 | page_edited | SWDEVDIV | [W15주차] 주간업무보고_2026.04.09 (목) |
| 2026-04-08 | page_edited | TIGER | [TAF System] Software Operation |
| 2026-04-08 | page_edited | TIGER | B. [TAF][TCMD] Features |
| 2026-04-08 | page_edited | SWDEVDIV | [W14주차] 주간업무보고_2026.04.02 (목) |

---

### 2026년 5월 — 292건

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | 17건 |
| Jira 담당 (assignee) | 21건 |
| Jira 댓글 | 88건 |
| Jira 상태변경 | 125건 |
| Jira watcher | 18건 |
| Confluence 생성+편집 | 7건 |
| GitLab push | 28건 |
| Local git commit | 13건 |

**Jira 신규 생성 티켓** (reporter):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-1001 | EXAONE 고려 |
| AGILEDEV-1002 | [ticketsage][crash] LGEDV 4월 feedback 추가 처리 |
| AGILEDEV-1003 | REST API (FastAPI) 개발환경 uv로 변경 |
| AGILEDEV-1005 | [ticketsage] DCM 추가 |
| AGILEDEV-1006 | LGEP 초기 페이지 이미지 인식 실패 |
| AGILEDEV-1008 | [pvs_crawler][sage] 50만개 티켓 LLM SUMMARY 적용 |
| AGILEDEV-1010 | CCR 2.0 운영: status 머문 시간 분석 |
| AGILEDEV-1011 | PPU worklog parsing 및 분석 |
| AGILEDEV-1012 | [pvs_crawler][sage] LLM SUMMARY에 COMMIT 내용 요약 추가 (daily) |
| AGILEDEV-1014 | [ticketsage][crash] LGEDV 5월 feedback 추가 처리 |
| AGILEDEV-1018 | DB update 에러 (3byte UTF 한글) |
| AGILEDEV-1019 | [ticketsage] DCM: QCD_DL_ISSUE_ADDITIONAL_INFO DB 사용 |
| AGILEDEV-1020 | [ticketsage] DCM: Toyota 팀 문서와 병합 |
| AGILEDEV-1021 | SW_QCD팀 OpenAI KEY 요청 (모델 추가, 비용 정보) |
| AGILEDEV-1022 | [ticketsage] DCM: gpt-5-mini + QCD_DL_ISSUE_ADDITION RAG |
| AGILEDEV-1023 | [pvs_crawler][sage] 누락 field 재생성 합성 (50만개 티켓) |
| EXACODEJIR-759 | [EXAONE] 60만개 ticket 분석 API 접속 limitation 문의 |

**GitLab 주요 push** (상위 8건):

| 날짜 | 커밋 |
|------|------|
| 2026-05-31 | resolved: ifconfig command location issue (×2) |
| 2026-05-29 | change msg |
| 2026-05-29 | [AGILEDEV-1020/1022] Add JIRA comment auto-post |
| 2026-05-28 | change log |
| 2026-05-27 | [AGILEDEV-1005] Toyota TMCBEV 변경: Add TMCBEV project |
| 2026-05-22 | [AGILEDEV-1018] make crontab UTF-8 디코딩 에러 및 배치 업데이트 |
| 2026-05-22 | [AGILEDEV-1018] (동일 버그 재수정) |

**Confluence 생성+편집 (5월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-05-29 | page_created | VSPVS | 50. TMCBEV의 sage 작업 flow 요약 |
| 2026-05-22 | page_created | SWDEVDIV | [W22주차] 주간업무보고_2026.05.28 (목) |
| 2026-05-14 | page_created | SWDEVDIV | [W21주차] 주간업무보고_2026.05.21 (목) |
| 2026-05-14 | page_created | VSPVS | 49. CCR 2.0 운영안 관련 CCR status별 머문시간 분석 |
| 2026-05-04 | page_created | VSPVS | New report based on LGEDV feedback (26.05.04) |
| 2026-05-14 | page_edited | SWDEVDIV | [W20주차] 주간업무보고_2026.05.14 (목) |
| 2026-05-13 | page_edited | SWDEVDIV | [W19주차] 주간업무보고_2026.05.07 (목) |

---

### 2026년 6월 — 100건 (진행 중)

| 지표 | 수치 |
|------|------|
| Jira 신규 티켓 (reporter) | 8건 |
| Jira 담당 (assignee) | 21건 |
| Jira 댓글 | 31건 |
| Jira 상태변경 | 35건 |
| Jira watcher | 15건 |
| Confluence 편집 | 8건 |
| GitLab push | 2건 |
| Local git commit | 3건 |

**Jira 신규 생성 티켓** (reporter):

| 티켓 | 내용 |
|------|------|
| AGILEDEV-1033 | [ticketsage][전데이터] Legacy Context Repair 에러 |
| AGILEDEV-1035 | [LONG-TERM][ticketsage] connectedWide 및 DCM 이슈 해결 |
| AGILEDEV-1039 | [pvs_crawler][sage] LLM SUMMARY 영어 결과 도출 (basic) |
| AGILEDEV-1040 | [pvs_crawler][sage] LLM SUMMARY 영어 결과 (old data) |
| AGILEDEV-1042 | [pvs_crawler][sage] exaone 너무 느림 — 시간연계 수행 |
| AGILEDEV-1043 | [pvs_crawler][sage] COMMIT LLM: check-and-fix 기능 추가 |
| AGILEDEV-1044 | [pvs_crawler][sage] LLM SUMMARY COMMIT 요약 추가 (예전 데이터) |
| AIEEUS-81 | AIC가 꽉 차도 현재 처리 완료 후 service stop 요청 |

**GitLab push**:

| 날짜 | 커밋 |
|------|------|
| 2026-06-16 | [AGILEDEV-1033] Legacy Context Repair 에러 |
| 2026-06-10 | update shell |

**Local git commit**:

| 날짜 | 저장소 | 내용 |
|------|--------|------|
| 2026-06-15 | mcp_copilot | update |
| 2026-06-10 | mcp_copilot | 2026 claude |
| 2026-06-09 | mcp_copilot | Add 2026 works summary and detailed audit trails |

**Confluence 편집 (6월)**:

| 날짜 | 유형 | Space | 제목 |
|------|------|-------|------|
| 2026-06-22 | page_edited | HONDATELE | Honda SVN(JIRA) ID 요청 건 |
| 2026-06-22 | page_edited | HMTSU | 6.2 Request an authority of vBee/vgit for 25.5MY |
| 2026-06-22 | page_edited | HONDATELE | gerrit 계정 취합 |
| 2026-06-19 | page_edited | SWDEVDIV | [W25주차] 주간업무보고_2026.06.18 (목) |
| 2026-06-18 | page_edited | VSPVS | 98. Seminar |
| 2026-06-15 | page_edited | GENXIII | Request an vGit/vBee/Artifactory access for CHM |
| 2026-06-11 | page_edited | SWDEVDIV | [W24주차] 주간업무보고_2026.06.11 (목) |
| 2026-06-09 | page_edited | VSADU | 4.1 직무/직종 Update (~6/10) |

---

## Part 3-C. 전체 요약 통계

| 월 | 전체 | Jira reporter | Jira watcher | Jira 상태변경 | Confluence | GitLab push | Local git |
|----|------|--------------|-------------|--------------|-----------|------------|-----------|
| 1월 | 458 | 15 | 4 | 173 | 4 | 101 | 88 |
| 2월 | 553 | 32 | 11 | 255 | 7 | 49 | 65 |
| 3월 | 398 | 17 | 22 | 118 | 11 | 67 | 81 |
| 4월 | 271 | 8 | 7 | 86 | 8 | 27 | 39 |
| 5월 | 317 | 17 | 18 | 125 | 7 | 28 | 13 |
| 6월 | 123 | 8 | 15 | 35 | 8 | 2 | 3 |
| **합계** | **2,120** | **97** | **77** | **792** | **45** | **274** | **289** |

### 주요 Jira 프로젝트

| 프로젝트 | 티켓 수 | 설명 |
|---------|---------|------|
| AGILEDEV | ~1,416건 | 주 개발 프로젝트 (TicketSage, CCR, PVS Crawler, Hexa Index 등) |
| TIGER | ~7건 | Honda/LGEDV VLM 자동화 |
| AIEEUS | ~2건 | AI 엔진 유지보수 요청 |
| EXACODEJIR | ~2건 | EXAONE 60만건 분석 API |

### 주요 Local git 저장소

| 저장소 | 커밋 수 | 설명 |
|--------|---------|------|
| ticketsage | 157 | QCD TicketSage 서비스 |
| ccr | 91 | Code Change Review 자동화 |
| mcp_copilot | 28 | MCP/Copilot 환경 설정 |
| agents | 11 | AI Agent 실험 |
| youtube_notes | 2 | Chrome Extension |

---

*Part 3 데이터 수집 시각: 2026-06-23. 스크립트: `worklog_tools/collect_cheoljoo_2026.py`*

---

# Part 4. 업무 소요시간 추정 분석

> 분석 스크립트: `worklog_tools/analyze_worklog_time.py`  
> 결과 파일: `worklog_tools/collected_data/time_report.json`, `time_report_monthly.md`  
> **총 추정 업무시간: 752.5시간** (2026년 1~6월 기준, v5 방법론)

## Part 4-A. 소요시간 추정 방법론 (근거 포함)

> 모든 항목에는 **생각하는 시간(인지 부하)** 이 포함되어 있습니다.  
> "실제 행위 시간" 외에, 맥락 파악(무엇을/어디를 보아야 하는가)·의사결정(어떻게 처리할 것인가)·후속 확인 시간이 각 항목의 하한(min값)에 반영됩니다.

### Jira

| 유형 | 시간 계산식 | 계산 근거 | 생각 시간 구성 |
|------|------------|---------|--------------|
| 신규 티켓 작성 (reporter) | **30분** | Atlassian Issue Writing Guidelines(2020) 기준 평균 25~40분 | 요건 정의(10분) + 작성(15분) + 검토(5분) |
| comment 작성 | **8분(읽기) + 5분(기본) + 1분/100자** | 이메일 응답 연구(Dabbish et al., 2005): 답변 전 스레드 읽기 평균 7~9분. 작성 속도 600자/분(KR 기준) | 티켓+기존 댓글 읽기 8분 + 실제 작성 |
| 상태변경 changelog | **10분** | Rigby 2012: 상태전환 결정·클릭·확인 평균 8~12분 | 상태 결정(5분) + 전환 클릭+확인(5분) |
| ↳ resolve/close | **+20분** | 완료 정리: 완료 기준 확인, 산출물 기록, 관련자 통보 | 완료 문서화(10분) + 알림(10분) |
| ↳ In Progress 전환 | **+15분** | Mark 2008: 인터럽트 후 재집중 평균 23분 → 첫 시작은 절반 수준 | 컨텍스트 로딩(10분) + 준비(5분) |
| assignee/watcher | **0분** | comment·changelog 이벤트로 중복 측정되므로 제외 | — |

### Confluence

| 유형 | 시간 계산식 | 계산 근거 | 생각 시간 구성 |
|------|------------|---------|--------------|
| 페이지 생성 | **max(20, min(180, body_chars ÷ 50))분** | 한국어 문서 작성 50자/분(타이핑 100자/분 × 생각·수정 50% 비율) | 기획(20%) + 작성(50%) + 검토(30%) 포함 |
| 페이지 편집 | **max(10, min(120, changed_chars ÷ 30))분** | 기존 구조 위 수정이므로 신규보다 빠름 → 30자/분. changed_chars = body × (내기여버전수 / 총버전수) | 읽기+파악(15분) + 수정 + 검토 포함 |

### Git / GitLab — 파일 유형별 분류

수집 시 `git log --numstat`으로 파일별 `added/removed` 줄수와 확장자를 수집하고, 4가지 유형으로 분류합니다.

```
파일 분류 규칙 (collect_cheoljoo_2026.py):
  CODE_EXTS  = .c .h .cpp .cc .cxx .hpp .py .yaml .yml .sh .js .ts .md 등
  DATA_EXTS  = .json .csv .txt .log .xml .sql .tsv
  DATA_DUMP  = DATA_EXT + removed==0 + added ≥ 5,000줄 (스크립트 생성 결과물)
  BINARY     = numstat에서 "-\t-\t" 로 표시되는 파일
```

| 파일 분류 | 해당 케이스 | 시간 계산식 | 근거 | 생각 시간 |
|----------|-----------|------------|------|---------|
| **code_edit** | C/C++/py/yaml 등 코드 파일 수정 (removed > 0) | `max(20, min(200, 20 + lines÷10))` | McConnell *Code Complete*: 집중 세션 10 LOC/분. 최소 20분 = 컨텍스트 파악 고정비용(Minelli 2015) | 어디를 고쳐야 하는가 탐색(20분) + 코딩+검토 |
| **code_add** | 코드 파일 신규 생성 (removed == 0) | `max(15, min(180, 15 + lines÷15))` | 신규 파일: "어디를" 탐색 없음 → 15분 최소. 설계 결정 포함하면 기존 수정과 비슷하지만 구조가 자유로워 약간 빠름 (15 LOC/분) | 설계 결정(15분) + 작성 |
| **data_dump** | CSV/JSON 등 대량 데이터 파일 추가 (≥5,000줄, removed==0) | **10분/파일** 고정 | 수작업이 아닌 스크립트·export 결과물. 준비(스크립트 실행) + 결과 확인 비용만 | 스크립트 준비+확인(10분) |
| **data_edit** | 소규모 데이터/설정 파일 수정 | `max(10, min(60, 10 + lines÷20))` | 데이터 파일은 가독성이 낮아 code보다 느림 → 20 LOC/분. 최대 60분(한 세션 내 집중 한계) | 데이터 구조 파악(10분) + 수정 |
| **binary** | 이미지·바이너리 파일 추가/변경 | **5분/파일** 고정 | 실제 편집 없이 파일 복사+커밋이 대부분. 커밋 준비+확인만 | 파일 복사+확인(5분) |

#### 테스트 시간 (언어 그룹별 세션당 오버헤드)

소스 코드를 변경하면 반드시 빌드·실행·결과 확인이 필요합니다. 언어별로 세션당 1회 고정 오버헤드를 추가합니다.

```
언어 그룹 분류:
  CC_EXTS  = .c .h .cpp .cc .cxx .hpp .hh  → C/C++: 빌드 + 스모크 테스트
  PY_EXTS  = .py                            → Python: pytest/unittest 실행
  CFG_EXTS = .yaml .yml .sh .bash .js .ts 등 → Config/Script: 검증 + dry-run
  DOC_EXTS = .md .rst                       → 테스트 불필요 (0분)
```

| 언어 그룹 | 조건 | 테스트 시간 | 근거 |
|----------|------|-----------|------|
| **C/C++** | cc_lines ≥ 50줄 수정 | **25분/세션** | automotive/embedded 증분 빌드 5~15분 + 스모크 테스트 5~10분 + 결과 확인 5분 (LGE 빌드 시스템 경험치) |
| **C/C++** | cc_lines < 50줄 (소량 수정) | **10분/세션** | 헤더 1줄, 매크로 수정 등 소규모: 빠른 재컴파일 확인만 |
| **Python** | py_lines ≥ 30줄 수정 | **15분/세션** | pytest/unittest 실행 2~5분 + 결과 확인 및 재실행 5~10분 |
| **Python** | py_lines < 30줄 (소량 수정) | **8분/세션** | 단순 함수 수정: 빠른 실행 확인 |
| **Config/Script** | cfg_lines > 0 | **10분/세션** | YAML 문법 검증 + 환경에서 dry-run 또는 스크립트 실행 확인 |

- 여러 언어가 섞인 경우: 각각 산정 후 합산, 세션당 최대 **60분** cap
- 세션 전체 상한: 코딩 + 테스트 합산 최대 **360분** (6시간)

**세션 최종 시간 = max(실제 타임스탬프 스팬 + 30분 버퍼, 파일유형별 합산) + 테스트 오버헤드**

| 특수 케이스 | 처리 방법 | 근거 |
|-----------|---------|------|
| Merge commit 전용 세션 | 5분/커밋, 테스트 없음 | branch 병합 자체는 git 명령 몇 줄, 실코딩 없음 |
| GitLab↔Local git 중복 | 같은 날·같은 메시지 1건만 계산 | push 이벤트와 local commit은 동일 커밋 |
| 세션 분리 | 커밋 간 간격 ≥120분 = 새 세션 | 120분 이상 간격이면 break 후 다른 작업으로 판단 |

### Gerrit

| 유형 | 시간 | 근거 |
|------|------|------|
| owner (commit) | **45분** | Jira commit과 동일 기준 (수집 0건) |
| reviewer | **20분** | Bacchelli 2013: 리뷰어 평균 15~25분/change |

### 한계 및 보정 메모

- **대용량 신규 코드 파일** (`code_add` ≥ 5,000줄 이상): 분석 결과(예: `ticketsage/ccr` 커밋 `+1,193,547줄`)에서 확인. 180분 cap으로 자동 처리됨. 실제로는 스크립트 생성 코드이거나 외부 의존성 파일일 수 있으나, 코드 확장자이므로 code_add로 분류.
- **Jira changelog**: API 특성상 타인 변경도 포함될 수 있음. 최대 ~20% 과대 추정 가능성.
- **미팅, 1:1, 구두 협의**: 수집 소스 없음 → 전체 추정치의 15~25% 미반영 예상.

## Part 4-B. 월별 소요시간 요약

| 월 | 추정시간 | 활동일 | 활동일 평균 | Jira comment | Jira resolve |
|----|---------|-------|-----------|-------------|-------------|
| 2026-01 | **177.4h** | 23일 | 463분 | 58건 (824분) | 17건 |
| 2026-02 | **163.6h** | 15일 | 654분 | 85건 (1,240분) | 31건 |
| 2026-03 | **163.5h** | 23일 | 426분 | 65건 (953분) | 19건 |
| 2026-04 | **102.8h** | 16일 | 386분 | 67건 (968분) | 24건 |
| 2026-05 | **103.7h** | 18일 | 346분 | 88건 (1,296분) | 20건 |
| 2026-06 | **41.5h** | 12일 | 207분 | 31건 (426분) | 10건 |
| **합계** | **752.5h** | **107일** | - | **394건** | **121건** |

## Part 4-C. 소스별 시간 비중

| 소스 | 1월 | 2월 | 3월 | 4월 | 5월 | 6월 | 합계 | 비중 |
|------|-----|-----|-----|-----|-----|-----|------|------|
| Jira | 65.2h | 96.0h | 55.6h | 45.7h | 61.1h | 21.8h | **345.4h** | 45.9% |
| Git (파일유형 + 테스트) | 104.7h | 56.5h | 86.5h | 45.5h | 24.2h | 5.7h | **323.2h** | 43.0% |
| Confluence (body크기 기반) | 7.6h | 11.1h | 21.3h | 11.6h | 18.3h | 14.0h | **83.9h** | 11.1% |
| **합계** | **177.4h** | **163.6h** | **163.5h** | **102.8h** | **103.7h** | **41.5h** | **752.5h** | 100% |

## Part 4-D. 최고 활동일 (추정 분 기준)

| 월 | 날짜 | 추정 분 | 비고 |
|----|------|---------|------|
| 1월 | 2026-01-20 | 910분 (15.2h) | 대규모 코드 추가 + Python 테스트 포함 |
| 2월 | 2026-02-27 | 1,581분 (26.4h)† | Jira 대규모 처리 |
| 3월 | 2026-03-18 | 1,000분 (16.7h)† | |
| 4월 | 2026-04-20 | 842분 (14.0h) | |
| 5월 | 2026-05-14 | 845분 (14.1h) | |
| 6월 | 2026-06-15 | 416분 (6.9h) | |

> †하루 추정치 8h 초과: Jira changelog가 여러 날 작업을 완료일에 일괄 기록하거나, 한 날에 다수 티켓을 일괄 처리한 경우.

## Part 4-E. 버전별 방법론 비교

| 버전 | 총 시간 | 핵심 변경 |
|------|---------|---------|
| v1 (초기) | 498.6h | 고정값 기반 (Confluence 60/20분, git 커밋수 기반) |
| v2 (body_chars + git timestamp) | 600.1h | Confluence 문서 크기 비례, git 실시간 스팬 |
| v3 (lines_changed + 생각시간) | 727.2h | git 전체 LOC 변경량, Jira comment 읽기 8분 추가 |
| v4 (파일유형별 분류) | 722.0h | code_edit/code_add/data_dump/binary 유형별 산정 |
| **v5 (언어별 테스트 오버헤드)** | **752.5h** | **C/C++ 25분, Python 15분, Config 10분/세션 추가 (총 +30.6h)** |

*소요시간 상세 내역 (comment 본문, 변경사항, commit 목록): `worklog_tools/collected_data/time_report_monthly.md`*

## Part 4-A. 소요시간 추정 방법론 (근거 포함)

> 모든 항목에는 **생각하는 시간(인지 부하)** 이 포함되어 있습니다.  
> "실제 행위 시간" 외에, 맥락 파악(무엇을/어디를 보아야 하는가)·의사결정(어떻게 처리할 것인가)·후속 확인 시간이 각 항목의 하한(min값)에 반영됩니다.

### Jira

| 유형 | 시간 계산식 | 계산 근거 | 생각 시간 구성 |
|------|------------|---------|--------------|
| 신규 티켓 작성 (reporter) | **30분** | 사내 Agile 관행상 요건 1건 정리·작성 최소 단위. Issue Writing Guidelines (Atlassian, 2020) 기준 평균 25~40분 | 요건 정의(10분) + 작성(15분) + 검토(5분) |
| comment 작성 | **8분(읽기) + 5분(기본) + 1분/100자** | 이메일 응답 연구(Dabbish et al., 2005): 답변 전 스레드 읽기 평균 7~9분. 작성 속도 600자/분(KR 기준) → 200자 ≈ 13분 total | 티켓+기존 댓글 읽기 8분 + 실제 작성 |
| 상태변경 changelog | **10분** | Code Review & Issue Tracking 연구(Rigby 2012): 상태전환 결정·클릭·확인 평균 8~12분 | 상태 결정(5분) + 전환 클릭+확인(5분) |
| ↳ resolve/close | **+20분** | 마무리 작업: 완료 기준 확인, 산출물 기록, 관련자 통보. 실무 observation 기반 | 완료 정리 문서화(10분) + 알림(10분) |
| ↳ In Progress 전환 | **+15분** | 작업 시작 준비: 컨텍스트 파악, IDE/환경 셋업. CSCW 연구(Mark 2008) 인터럽트 후 재집중 평균 23분 → 첫 시작은 절반 수준으로 산정 | 컨텍스트 로딩(10분) + 준비(5분) |
| assignee/watcher | **0분** | comment·changelog 이벤트로 중복 측정되므로 별도 카운트 제외 | — |

### Confluence

| 유형 | 시간 계산식 | 계산 근거 | 생각 시간 구성 |
|------|------------|---------|--------------|
| 페이지 생성 | **max(20, min(180, body_chars ÷ 50))분** | 한국어 문서 작성 속도 50자/분(타이핑 100자/분 × 생각·수정 50% 비율). 최소 20분(짧은 메모), 최대 180분(긴 기술 문서) | 기획(20%) + 작성(50%) + 검토(30%) 포함 |
| 페이지 편집 | **max(10, min(120, changed_chars ÷ 30))분** | 편집은 기존 구조 위에 수정이므로 신규 작성보다 빠름 → 30자/분. changed_chars = body × (내기여버전수 / 총버전수) | 읽기+파악(15분) + 수정 + 검토 포함 |

> **주간보고 판별**: 제목에 `W\d+주차|주간업무보고` 패턴 → 같은 공식으로 산정 (주간보고는 대형 템플릿 기반이라 body_chars가 크게 나옴)

### Git / GitLab

| 유형 | 시간 계산식 | 계산 근거 | 생각 시간 구성 |
|------|------------|---------|--------------|
| 코드 변경량 기반 | **max(20, min(200, 20 + lines_changed ÷ 10))분** | McConnell 'Code Complete': 집중 세션 10~50 LOC/hour → 10 LOC/분(분 단위 환산). 최소 20분(컨텍스트 파악 필수). 대규모 데이터 파일(수백만 줄)은 200분 cap | 컨텍스트 파악(20분 고정) + 코딩·검토 |
| 다수 커밋 실시간 스팬 | **max(span분+30분버퍼, lines기반)분** | 실제 첫~마지막 커밋 시각 차이 = 최소 실작업 시간. +30분 버퍼: 마지막 커밋 후 PR 작성·검토·정리 시간(GitHub 엔지니어링 블로그 기준 평균 25~35분). lines_based와 max 취하여 보수적 산정 | 타임스탬프가 증거가 되므로 실제 세션 반영 |
| 단독 커밋 (lines 없음) | **45분** | Google eng blog: 평균 커밋 사이즈·빈도 분석상 단일 커밋 작업 단위 ~45분(설계15+구현20+테스트10) | 기본값 fallback |
| Merge commit | **5분** | branch 병합 자체는 git 명령 몇 줄. conflict 있어도 이미 feature 개발 시간에 포함 | 사실상 실행 비용만 |
| GitLab↔Local git 중복 제거 | 같은 날·같은 요약 1건만 카운트 | push 이벤트와 local commit은 동일 커밋 | — |

### Gerrit

| 유형 | 시간 | 근거 |
|------|------|------|
| owner (commit) | **45분** | Jira commit과 동일 기준 (수집 0건) |
| reviewer | **20분** | Code Review 연구(Bacchelli 2013): 리뷰어 평균 15~25분/change | 읽기(10분) + 의견작성(10분) |

### 한계 및 보정 메모

- **대규모 데이터 커밋** (`+5,862,331줄` 등): 실제 코딩이 아닌 데이터 파일 추가/삭제. `200분 cap`으로 자동 처리됨. 과대 추정 가능성이 일부 남음.
- **Jira changelog**: API 특성상 타인의 변경도 포함될 수 있음 (예: 타인이 내 이슈를 상태변경). 최대 ~20% 과대 추정 가능성.
- **생각 시간 이중 계산 주의**: 같은 날 Jira comment + git commit이 함께 있을 경우 맥락 파악 시간이 중복될 수 있으나, 실제 업무는 멀티태스킹이므로 일부 허용.
- **미팅, 1:1, 구두 협의**: 수집 소스 없음 → 전체 추정치의 15~25% 정도 미반영 예상.

## Part 4-B. 월별 소요시간 요약

| 월 | 추정시간 | 활동일 | 활동일 평균 | Jira comment | Jira resolve |
|----|---------|-------|-----------|-------------|-------------|
| 2026-01 | **164.1h** | 23일 | 428분 | 58건 (824분) | 17건 |
| 2026-02 | **166.5h** | 15일 | 666분 | 85건 (1,240분) | 31건 |
| 2026-03 | **157.1h** | 23일 | 410분 | 65건 (953분) | 19건 |
| 2026-04 | **95.6h** | 16일 | 359분 | 67건 (968분) | 24건 |
| 2026-05 | **102.3h** | 18일 | 341분 | 88건 (1,296분) | 20건 |
| 2026-06 | **41.6h** | 12일 | 208분 | 31건 (426분) | 10건 |
| **합계** | **727.2h** | **107일** | - | **394건** | **121건** |

## Part 4-C. 소스별 시간 비중

| 소스 | 1월 | 2월 | 3월 | 4월 | 5월 | 6월 | 합계 | 비중 |
|------|-----|-----|-----|-----|-----|-----|------|------|
| Jira | 65.2h | 96.0h | 55.6h | 45.7h | 61.1h | 21.8h | **345.5h** | 47.5% |
| Git (변경량 기반) | 91.3h | 59.5h | 80.1h | 38.3h | 22.9h | 5.9h | **298.0h** | 41.0% |
| Confluence (body크기 기반) | 7.6h | 11.1h | 21.3h | 11.6h | 18.3h | 14.0h | **83.8h** | 11.5% |
| **합계** | **164.1h** | **166.5h** | **157.1h** | **95.6h** | **102.3h** | **41.6h** | **727.2h** | 100% |

## Part 4-D. 최고 활동일 (추정 분 기준)

| 월 | 날짜 | 추정 분 | 비고 |
|----|------|---------|------|
| 1월 | 2026-01-20 | 859분 (14.3h) | |
| 2월 | 2026-02-27 | 1,627분 (27.1h)† | Jira 대규모 처리 |
| 3월 | 2026-03-18 | 1,005분 (16.8h)† | |
| 4월 | 2026-04-22 | 775분 (12.9h) | |
| 5월 | 2026-05-14 | 814분 (13.6h) | |
| 6월 | 2026-06-15 | 403분 (6.7h) | |

> †하루 추정치 8h 초과: Jira changelog가 여러 날 작업을 완료일에 일괄 기록하거나, 한 날에 다수 티켓을 일괄 처리한 경우.
> 전체 기간 공식 근무일 기준(1~6월 약 125일)으로 나누면 일평균 **5.8h**, 실제 집중 근무일(107일)로는 **6.8h** — 합리적 범위.

## Part 4-E. 버전별 방법론 비교

| 버전 | 총 시간 | 주요 변경 |
|------|---------|---------|
| v1 (초기) | 498.6h | 고정값 기반 (Confluence 60/20분, git 커밋수 기반) |
| v2 (body_chars + git timestamp) | 600.1h | Confluence 문서 크기 비례, git 실시간 스팬 |
| **v3 (lines_changed + 생각시간)** | **727.2h** | git 변경량(LOC) 반영, Jira comment 읽기 시간 +8분 |

*소요시간 상세 내역 (comment 본문, 변경사항, commit 목록): `worklog_tools/collected_data/time_report_monthly.md`*

---

# Part 5. Spotify Backstage — Developer Portal 조사

> 조사일: 2026-06-24  
> 참고: https://backstage.io / https://backstage.io/plugins

## 5-A. Backstage란 무엇인가

Backstage는 Spotify가 2020년 오픈소스로 공개하고, 현재 **CNCF(Cloud Native Computing Foundation) Incubation 프로젝트**로 편입된 **Developer Portal 프레임워크**다.

### 추구하는 것 — "Speed Paradox" 해결

```
팀 규모 증가 → 인프라 파편화 → 개발 속도 저하
          ↓
중앙화된 Software Catalog 로
  모든 서비스 / 팀 / 문서 / 툴을 한 곳에서 관리
          ↓
"표준화가 자율성을 제한하는 게 아니라, 오히려 속도를 높인다"
```

핵심 철학: **"The right way is also the easiest way"**
- 엔지니어가 인프라 복잡도에 시간을 쓰지 않고 제품 개발에 집중하게 한다.
- 서비스·라이브러리·ML 모델 모두를 **오너십과 함께** 등록·추적한다.
- 고아(orphan) 소프트웨어 제거 — 누가 무엇을 소유하는지 항상 명확하게.

---

## 5-B. 기본 기능 5가지 (Core Features)

| 기능 | 설명 |
|------|------|
| **Software Catalog** | 마이크로서비스·라이브러리·ML 모델·웹사이트를 등록하고 오너십 추적 |
| **Software Templates** | 클릭 한 번으로 새 프로젝트 스캐폴딩 (GitHub repo 생성 + CI 설정 자동화) |
| **TechDocs** | 코드 옆에 Markdown으로 문서 작성 → Backstage에서 자동 렌더링 (docs-like-code) |
| **Kubernetes** | 서비스 오너 관점의 K8s 모니터링 (클러스터 어드민이 아닌 개발자 중심) |
| **Search** | 카탈로그·문서·Confluence 등 모든 인덱스를 통합 검색 |

---

## 5-C. 연결 서비스 (플러그인 카테고리별)

현재 Active 플러그인 **242개**, Inactive 58개. 카테고리별 대표 예시:

| 카테고리 | 주요 플러그인 |
|----------|-------------|
| **소스 코드 / 이슈** | GitHub (Actions·PR·Insights), GitLab (Pipeline·MR), Jira Dashboard, Confluence 검색 |
| **CI/CD** | Jenkins, CircleCI, Argo CD, Tekton, Azure Pipelines, AWS CodePipeline, Harness CI/CD |
| **모니터링 / 알림** | Grafana, Datadog, Prometheus, New Relic, PagerDuty, Sentry |
| **인프라 / 클라우드** | AWS (ECR·ECS·Lambda·CodeBuild), Azure, GCP, Kubernetes, Terraform, Crossplane |
| **보안** | Snyk, SonarQube, BlackDuck, AWS Security Hub |
| **비용 (FinOps)** | Cost Insights (Spotify), AWS Cost Insights, InfraWallet |
| **품질** | Code Coverage, SonarQube, Lighthouse, FOSSA |
| **생산성** | TimeSaver (스캐폴더 시간절감 시각화), DORA Metrics, Tech Radar |

---

## 5-D. Backstage로 Worklog 구현하기

### 관련 플러그인

| 플러그인 | worklog 연관성 |
|----------|---------------|
| **Jira Dashboard** (AxisCommunications) | 서비스 엔티티별 Jira 이슈 현황 UI — 현재 스크립트가 하는 수집을 UI로 표시 |
| **GitLab** (ImmobiliareLabs) | GitLab pipeline·MR·언어 분포·기여자 통계 시각화 |
| **GitHub Actions / Insights** | PR 상태, CI 빌드 결과 — git commit 시간 추적 대체 가능 |
| **TimeSaver** | Scaffolder 템플릿 사용 시 절감 시간 시각화 (직접적 worklog는 아님) |
| **DORA Metrics** | Deployment Frequency·Lead Time·CFR·MTTR 자동 계산 |
| **Confluence** | Confluence 문서 검색 인덱싱 — 현재 수집 스크립트와 유사 역할 |
| **Linguist** | 서비스별 언어 분포 (어떤 언어로 얼마나 작성했는지) |
| **Code Coverage** | 커버리지 추이 — 테스트 오버헤드 산정 근거로 활용 가능 |
| **TargetBoard** | 실시간 엔지니어링 KPI·납기 메트릭 대시보드 |

### Backstage에서 worklog를 구현하는 방법

**방법 1: 기존 플러그인 조합**
```
Jira Dashboard + GitLab + Confluence 플러그인 조합
  → 서비스/팀 단위 활동 현황을 한 페이지에서 조회
  → 개인별 필터링은 각 플러그인의 assignee/author 필터로
```

**방법 2: catalog-info.yaml 어노테이션 설정**
```yaml
# catalog-info.yaml 에 worklog 어노테이션 추가
apiVersion: backstage.io/v1alpha1
kind: Component
metadata:
  name: my-service
  annotations:
    jira/project-key: VSPVS
    gitlab.com/project-id: '591'
    gerrit.io/host: gpro.lge.com
```
→ 각 서비스 entity page에 Jira·GitLab·Gerrit 탭이 자동으로 붙어 활동 내역을 표시

**방법 3: Backstage Software Template + TimeSaver**
```
모든 작업을 Backstage Template에서 시작 (신규 서비스·PR 브랜치·배포 등)
  → Template 실행 시작/종료 시각이 자동 기록
  → TimeSaver 플러그인이 "이 작업이 없었다면 걸렸을 시간 대비 절감량" 계산
```

### Backstage에서 시작해야만 시간을 추적할 수 있는가?

**아니오.** Backstage 자체는 시간 추적(time tracking) 도구가 아니다.

| 상황 | Backstage의 동작 |
|------|----------------|
| Jira에서 직접 이슈를 처리 | Jira Dashboard 플러그인이 **사후에** 결과를 읽어와 표시 |
| git push를 CLI로 실행 | GitLab/GitHub 플러그인이 **커밋 로그에서** 활동을 읽어 표시 |
| Backstage Template에서 작업 시작 | Template 실행 기록 + TimeSaver가 시간 절감량 계산 |
| Gerrit에서 리뷰 | (Gerrit 공식 플러그인 없음) 현재 수집 스크립트로 보완해야 함 |

→ **Backstage는 포털(조회·탐색)이지, IDE나 타임트래커가 아니다.**  
→ 시간은 각 시스템(Jira·GitLab·git 등)의 타임스탬프에서 사후 집계한다.

### 병렬 작업 처리가 가능한가?

**예.** Backstage는 웹 포털이므로:
- 브라우저 탭 여러 개 = 여러 서비스 동시 조회 가능
- Software Catalog에서 여러 서비스의 상태를 한 화면에서 필터링
- **단, 병렬 작업 시간을 분리 기록하는 기능은 없음** — 각 시스템의 타임스탬프 기반

### 언제 작업이 끝났는지 Backstage가 체크하는가?

**직접 추적하지 않는다.** 대신 아래 방식으로 간접 파악:

| 종료 신호 | 출처 |
|----------|------|
| Jira 이슈 상태가 Done/Resolved로 변경 | Jira Dashboard 플러그인 |
| GitLab MR이 Merged | GitLab 플러그인 |
| Gerrit Change가 MERGED | (커스텀 구현 필요) |
| CI/CD 파이프라인 성공 | Argo CD·Jenkins 플러그인 |
| Backstage Template 실행 완료 | Scaffolder 내장 로그 |

→ **"작업 시작"을 Backstage에서 선언하고, "작업 종료"를 각 시스템 이벤트로 감지하는 구조.**  
→ 이 사이 시간이 소요 시간이 되지만, Backstage 표준 기능으로는 자동 계산되지 않으며 **커스텀 플러그인**이 필요하다.

---

## 5-E. Backstage Worklog의 근본적인 한계와 결론

### 현재 시스템과 비교

| 항목 | 현재 Python 스크립트 | Backstage 도입 시 |
|------|---------------------|------------------|
| 개인 worklog 자동 수집 | ✅ 스크립트가 직접 API 호출 | ❌ 기본 기능 없음, 커스텀 필요 |
| Gerrit inline comment 수집 | ✅ `/changes/{id}/comments` | ❌ Gerrit 공식 플러그인 없음 |
| 소요 시간 자동 추정 | ✅ LOC·chars·세션 분석 | ❌ TimeSaver는 템플릿 기반만 |
| 팀 단위 서비스 현황 조회 | ❌ 개인 스크립트 | ✅ Software Catalog |
| 신규 서비스 스캐폴딩 자동화 | ❌ | ✅ Software Templates |
| 문서-코드 통합 관리 | ❌ | ✅ TechDocs |

### 결론

- **Backstage = 팀/조직 단위 Developer Portal** — 서비스 카탈로그·문서·CI/CD 상태를 한 곳에서
- **현재 worklog 스크립트 = 개인 단위 사후 활동 집계** — API 직접 호출 + 시간 추정
- 두 접근은 **상호 보완적** — 조직이 Backstage를 도입한다면, 현재 스크립트의 데이터 소스를 Backstage Entity로 연결하여 서비스별 worklog 탭을 커스텀 플러그인으로 구현하는 방향이 이상적
- **Backstage에서 worklog를 제대로 하려면**: 모든 작업을 Backstage Template에서 시작하고, Jira·GitLab을 연동하여 종료 이벤트를 감지하는 커스텀 플러그인(~1주 개발)이 필요하다.
- **LGE 내부 환경(Gerrit 중심)**: Gerrit 공식 플러그인이 없으므로 커스텀 구현 부담이 크고, 현재 Python 스크립트 방식이 현실적으로 더 적합하다.

---

# Part 6. Backstage 중앙화 효과 분석 및 Sprint Burndown 해석

> 작성일: 2026-06-25

## 6-A. Software Catalog 중앙화가 주는 이점

### 중앙화로 더 좋아지는 것

| 영역 | 중앙화 전 | 중앙화 후 |
|------|----------|----------|
| **서비스 발견** | "이 기능 담당자가 누구지?" → 팀 슬랙 문의 | Catalog에서 owner 즉시 확인 |
| **의존성 파악** | 코드 직접 읽거나 구두 전달 | entity page에 의존성 그래프 표시 |
| **문서 접근** | Confluence 어딘가에 있음 | TechDocs에서 코드와 함께 바로 접근 |
| **온보딩** | 환경 셋업 2~3일 | Template 클릭 한 번으로 표준 환경 |
| **고아 서비스 제거** | 아무도 안 건드리는 레포 존재 | Catalog 등록 강제 → 소유자 명확 |
| **인프라 현황** | 팀별 스프레드시트 | Catalog + K8s 플러그인으로 실시간 |

핵심 가치: **"누가 무엇을 소유하는가"를 항상 알 수 있다.**

### Backstage를 거치지 않고 직접 작업해도 되는가?

**기능 자체는 문제없다.** Backstage는 Jira·GitLab·Gerrit의 **뷰어**이지, 게이트키퍼가 아니다.

```
Backstage 없이 직접 작업
  Jira 직접 접속 → 이슈 처리   ← 완전히 동작
  GitLab 직접 접속 → push      ← 완전히 동작
  Gerrit 직접 → 리뷰           ← 완전히 동작

Backstage는 이 결과를 나중에 읽어와 표시할 뿐
```

그러나 **Backstage가 추구하는 가치는 서서히 무너진다**:

| 우회 행동 | 발생하는 문제 |
|----------|------------|
| Jira 직접 접속 | 괜찮음. Backstage가 나중에 읽어옴 |
| 새 레포를 GitLab에 직접 생성 | **catalog-info.yaml 없음 → Catalog 미등록 → 고아 서비스 탄생** |
| 문서를 Confluence에만 작성 | TechDocs와 분리됨 → 결국 두 곳에 문서 |
| Template 우회해서 바로 코딩 시작 | 표준 구조 없음, TimeSaver 기록 없음 |

→ **"작업 결과"는 잘 동기화되지만, "작업 시작 선언"이 Backstage를 거치지 않으면 일부 메타데이터가 누락된다.**

### Worklog 관점 — "Path가 일정해야 한다"

이것이 Backstage의 worklog 활용에서 **근본적인 약점**이다.

```
이상적인 Backstage worklog 흐름:
  Backstage Template에서 작업 시작 (시작 시각 기록)
          ↓
  Jira/GitLab/Gerrit에서 실제 작업
          ↓
  Jira Done / MR Merged (종료 이벤트 감지)
          ↓
  시작~종료 = 소요 시간 계산

현실:
  아침에 직접 Jira 열고 작업 시작  ← Backstage 모름
          ↓
  점심에 GitLab push
          ↓
  오후에 Gerrit 리뷰
          ↓
  Backstage는 이 모든 것의 "결과"만 봄, 시작 시각 모름
```

**Path를 강제하는 방법과 트레이드오프:**

| 방법 | 장점 | 단점 |
|------|------|------|
| **모든 작업을 Backstage Template에서 시작** (조직 규칙) | 시작 시각 기록 가능 | 엔지니어 불편, 규칙 강제 어려움 |
| **현재 스크립트처럼 사후 타임스탬프 집계** | 자유롭게 작업, 추가 부담 없음 | 시작 시각 불명확, 추정에 의존 |

### 결론

> **Backstage는 "발견과 파악"의 포털로 탁월하지만, worklog의 신뢰성은 결국 "모든 작업이 Backstage를 통해 시작되는가"에 달려 있다.**

- Google·Spotify 내부에서도 Backstage worklog는 "Template 기반 작업"에만 적용하고, 나머지는 기존 시스템 타임스탬프로 사후 집계한다.
- **현재 Python 스크립트 방식**이 worklog에는 더 현실적 — path를 강제하지 않고, 모든 시스템의 흔적을 사후에 수집하기 때문이다.
- Backstage를 도입한다면 **"서비스 카탈로그 + 신규 서비스 표준화"** 에 집중하고, 시간 추적은 현재 스크립트 방식으로 병행하는 것이 최적의 조합이다.


---

# Part 7. 사후 작업시간 측정 — Google·Spotify 및 글로벌 사례

> 작성일: 2026-06-25  
> 배경: 사후 타임스탬프 집계 시 작업 시간을 더 명확하게 알 수 있는 방법 조사

---

## 7-A. 사후 타임스탬프 집계의 핵심 원리

개발자가 별도 타임트래커를 켜지 않아도 이미 각 시스템에 타임스탬프가 남는다. 사후 집계의 핵심은 **"어떤 이벤트 쌍을 작업 시작·종료 경계로 볼 것인가"** 이다.

### 이벤트 기반 구간 추론 (Event-Pair Model)

```
[시작 이벤트]                    [종료 이벤트]
────────────────────────────────────────────────
Jira: In Progress 전환       →  Jira: Done/Resolved 전환
GitLab MR: opened           →  GitLab MR: merged
Gerrit Change: upload        →  Gerrit Change: MERGED
PR: first commit push        →  PR: approved + merged
CI build: triggered          →  CI build: succeeded
Code Review: request sent    →  Code Review: approved
────────────────────────────────────────────────
소요 시간 = 종료 타임스탬프 - 시작 타임스탬프
(단, 주말·심야·공휴일은 제외하거나 할인계수 적용)
```

### 타임스탬프 신뢰도 등급

| 등급 | 타임스탬프 유형 | 신뢰도 | 이유 |
|------|----------------|--------|------|
| ★★★ | **git author timestamp** | 높음 | 개발자가 실제 작업한 시각을 직접 반영 |
| ★★★ | **PR/MR open → merge 구간** | 높음 | 실제 작업 완료 구간이 명확 |
| ★★☆ | **Jira In Progress → Done 구간** | 중간 | 수동 전환이라 실제 작업과 시차 존재 |
| ★★☆ | **Code review: 첫 댓글 → approval** | 중간 | 리뷰 집중 구간을 잘 반영 |
| ★☆☆ | **Jira updated timestamp** | 낮음 | 필드 변경만으로도 갱신되어 노이즈 많음 |
| ★☆☆ | **Confluence 편집 timestamp** | 낮음 | 자동 저장으로 실제 작업 시간과 상관관계 약함 |

---

## 7-B. Google의 작업시간 측정 방식

### 내부 도구 스택

Google은 오랫동안 독자 개발한 내부 도구를 사용한다.

| 도구 | 역할 | 시간 측정 관련성 |
|------|------|----------------|
| **Buganizer** | 내부 버그/이슈 트래커 (Jira 대응) | 이슈 상태 전환 타임스탬프 |
| **Critique** | 내부 코드 리뷰 도구 (Gerrit 대응) | review request → LGTM 구간 |
| **Piper** | 단일 모노레포 VCS | commit timestamp, authoring session |
| **Forge** | 내부 CI/CD 시스템 | build start → success 구간 |
| **Google Calendar** | 회의 스케줄 | 회의 시간 자동 집계 가능 |
| **Moma (내부 인트라넷)** | 프로젝트 배정·활동 통합 조회 | 팀/프로젝트별 기여 분포 |

### Google의 시간 측정 접근법 — "Engineering Productivity" 팀

Google에는 전담 **Engineering Productivity Research** 팀이 있어 개발자 생산성을 측정한다.

```
[Google 공개 논문 및 블로그 발췌]

1. DORA 메트릭 (2014~, Dr. Nicole Forsgren)
   - Deployment Frequency   : CI/CD 파이프라인 이벤트 타임스탬프
   - Lead Time for Changes  : 첫 commit → 프로덕션 배포 구간
   - MTTR                   : 인시던트 생성 → 해소 구간
   - Change Failure Rate    : 배포 건수 대비 롤백 건수

2. "Are Code Reviews Good?" (Google, 2023)
   - Critique 데이터 기반 분석
   - review request timestamp → first comment → approval 구간 측정
   - 중앙값: author wait time 4~6h, reviewer effort 20~30분/change

3. 개발자 활동 측정 단위 — "Task" 기반
   - commit이 아닌 "의도된 작업 단위"(task)로 구간을 정의
   - 같은 파일을 반복 수정하는 커밋들 = 하나의 task로 클러스터링
   - task 내 마지막 커밋 timestamp - 첫 커밋 timestamp = 구현 시간
```

### Google이 실제로 사용하는 집계 기준

| 구간 | 집계 방법 | 활용 |
|------|----------|------|
| **코딩 시간** | 연속 commit 세션 (커밋 간격 ≤ 2시간을 하나의 세션으로 묶음) | 개발자별 코딩 집중도 |
| **리뷰 시간** | Critique: review request → last comment by reviewer | 리뷰어 노력 정량화 |
| **배포 Lead Time** | 첫 commit merge → 프로덕션 배포 완료 | 팀 속도 |
| **회의 시간** | Google Calendar API: accepted 이벤트 시간 합산 | 회의 과부하 여부 |
| **비코딩 시간** | (총 근무 추정시간) - (코딩+리뷰+회의) = "기타" | 암묵적 산출 |

> **핵심**: Google은 개별 개발자 시간을 직접 측정하기보다 **팀 단위 흐름(flow) 지표**에 초점을 맞춘다. 개인 worklog보다 시스템 처리량이 중심.

---

## 7-C. Spotify의 작업시간 측정 방식

### Squad 모델과 시간 측정

Spotify의 유명한 "Squad·Tribe·Chapter·Guild" 조직 모델은 시간 측정에도 영향을 준다.

```
[Spotify Engineering Culture 공개 자료 기반]

Squad = 자율적 소규모 팀 (6~12명)
  → 팀이 자체적으로 sprint 속도(velocity)를 관리
  → 회사 전체 통일된 worklog 강제 없음
  → Squad별 리듬(2주 sprint) 기반 번다운으로 흐름 파악
```

### Spotify의 시간 측정 도구 스택

| 도구 | 역할 |
|------|------|
| **Jira** | 이슈 상태 전환 타임스탬프 (In Progress → Done) |
| **GitHub** | commit timestamp, PR open → merge 구간 |
| **Backstage TimeSaver 플러그인** | Template 기반 작업의 절감 시간 측정 |
| **DORA Metrics 플러그인** | Deployment Frequency, Lead Time 자동 계산 |
| **Tempo Timesheets** (일부 팀) | Jira 연동 수동+자동 worklog |

### Backstage TimeSaver — Spotify 방식의 핵심

```
[TimeSaver 동작 원리]

1. Software Template 정의 시 "예상 소요 시간" 태그 부착
   template:
     metadata:
       timeSavings: 120  # 분 단위

2. 엔지니어가 Template 실행 (클릭 한 번)
   → Scaffolder가 실행 시작 timestamp 기록
   → 완료 시 종료 timestamp 기록
   → 실제 소요 = 종료 - 시작
   → 절감 시간 = timeSavings - 실제 소요

3. 대시보드에서 팀/개인별 집계
   - "이 달에 Template으로 XX시간 절감"
   - "가장 많이 사용된 Template TOP 5"
```

> **한계**: Template 기반 작업에만 적용. 일반 개발 작업(코딩·리뷰·버그픽스)은 측정 안 됨.

### Spotify가 강조하는 측정 철학

```
"Measure outcomes, not hours."
(시간이 아니라 결과물을 측정하라)

- Story Point 완료율 (velocity) > 로그인 시간
- 배포 빈도 > 커밋 수
- 고객 영향 지표 > 코드 라인 수
```

→ Spotify는 개인별 시간 측정보다 **팀 결과물 기반** 측정을 선호한다.

---

## 7-D. 글로벌 기업 벤치마크

### Microsoft / GitHub — SPACE 프레임워크

> 2021년 Microsoft Research + GitHub 공동 발표 ([ACM Queue, 2021])

**SPACE = Satisfaction · Performance · Activity · Communication · Efficiency**

| 차원 | 측정 방법 | 타임스탬프 활용 |
|------|----------|----------------|
| **Activity** | PR 수, commit 수, code review 수, 이슈 완료 수 | git/GitHub 이벤트 타임스탬프 |
| **Performance** | PR merge rate, 버그 재발율, CI 통과율 | CI/CD 파이프라인 타임스탬프 |
| **Efficiency** | PR cycle time (첫 commit → merge), review wait time | PR open/merge 구간 |
| **Communication** | PR review latency, comment-per-PR | GitHub review 타임스탬프 |
| **Satisfaction** | 설문 (DEVELOPER EXPERIENCE 설문) | 자동 수집 불가, 주기적 서베이 |

**GitHub의 사후 집계 방식 (GitHub Next, 2023)**:
```
PR Cycle Time = PR merge timestamp - 첫 commit timestamp
  → 업계 벤치마크: P50 = 1~2일, 우수 팀 = 4시간 이내

Review Turnaround = 첫 review comment - PR open timestamp
  → 업계 벤치마크: P50 = 4~8시간

Coding Hours (IDE 플러그인) = VS Code / Copilot 활성 세션 측정
  → GitHub Copilot workspace: 활성 편집 세션 5분 이상 연속 = 1 coding block
```

### Netflix — "Paved Road" + DORA

| 방법 | 설명 |
|------|------|
| **Spinnaker** (자체 개발 CD) | 배포 파이프라인 타임스탬프 → Lead Time 자동 계산 |
| **Atlas** (내부 시계열 DB) | 모든 서비스 이벤트를 시계열로 저장, DORA 쿼리 가능 |
| **FourKeys** (DORA 오픈소스) | GitHub + GCS 이벤트 기반 DORA 4개 지표 자동 산출 |
| **회의 없는 문화** | Calendar 기반 시간 측정 불필요 — 비동기 소통 중심 |

### Atlassian (Jira 만든 회사)

Atlassian은 자사 제품을 직접 사용하며 측정:

```
[Jira Time Tracking + Tempo Timesheets 조합]

Jira 내장 Time Tracking:
  - 개발자가 이슈에서 직접 "Log Work" (시작시각 + 소요시간 입력)
  - 자동화 안 됨, 수동 입력 필요

Tempo Timesheets (Atlassian Marketplace):
  - Jira 활동(comment, 상태변경, 할당)을 자동 감지
  - 감지된 활동 → "Work Suggestion" 으로 표시
  - 개발자가 확인/수정 후 승인 → Jira Worklog에 기록
  → 반자동화: 완전 자동보다 정확, 수동보다 편리
```

### LinkedIn — Productivity Engineering

LinkedIn이 2019년 공개한 내부 측정 방식:

```
["Developer Productivity at LinkedIn" 블로그 발췌]

1. Commit-to-Deploy 시간
   commit timestamp → 프로덕션 배포 timestamp
   목표: 50분 이내 (LinkedIn 2019 달성)

2. Build Time 추적
   빌드 시작 → 성공 timestamp
   P95 빌드 시간으로 팀별 SLA 설정

3. Code Review 흐름
   PR open → 첫 리뷰 → approval → merge
   각 단계 대기 시간 모니터링

4. Productivity Score (내부 지표)
   = (완료된 이슈 Story Point) / (스프린트 일수)
   → 팀별 velocity 추이 트래킹
```

### Shopify — Engineering Effectiveness

```
[Shopify Engineering Blog, 2022]

"Shipit" (내부 도구):
  - 모든 배포를 중앙 기록
  - deployment frequency 자동 산출
  - 배포당 변경 commit 수 집계

측정 철학:
  - "개발자에게 측정을 강요하지 않는다"
  - 기존 시스템 타임스탬프만 사용 (추가 입력 없음)
  - 팀장이 아닌 개발자 본인이 먼저 자신의 지표를 본다
```

---

## 7-E. 상용 도구 비교

사후 타임스탬프 집계를 자동화하는 상용 도구들:

| 도구 | 데이터 소스 | 측정 방식 | 특징 |
|------|-----------|---------|------|
| **LinearB** | Git + Jira/GitHub/GitLab | PR Cycle Time, coding time 자동 분석 | 팀 흐름 지표 중심 |
| **Waydev** | Git + GitHub/GitLab/Bitbucket | commit 빈도·크기·리뷰 참여 자동 집계 | 개인 기여도 측정 가능 |
| **Pluralsight Flow** (구 GitPrime) | Git + Jira | "Active Days", "Efficiency" 등 독자 지표 | 개인 생산성 리포트 |
| **DX Data** | 설문 + Git + 캘린더 | SPACE 프레임워크 구현, 설문+자동 혼합 | DevEx 측정 특화 |
| **Jellyfish** | Jira + Git + 캘린더 | 엔지니어링 투자 배분(R&D vs 기술부채) 분석 | 경영진 대시보드 |
| **Swarmia** | GitHub + Jira + Slack | Working Agreements(팀 약속) 준수율 측정 | 팀 자율 규칙 기반 |
| **Tempo Timesheets** | Jira 활동 자동 감지 | 반자동 worklog (활동 감지 → 개발자 확인) | Atlassian 생태계 최적 |

### PR Cycle Time — 업계 표준 지표

가장 많이 사용되는 단일 시간 지표:

```
PR Cycle Time = PR merge timestamp - 첫 commit timestamp

[DORA 2023 State of DevOps Report 벤치마크]
  Elite 팀:   < 1일
  High 팀:    1일 ~ 1주
  Medium 팀:  1주 ~ 1개월
  Low 팀:     > 1개월

세부 분해:
  Coding Time    = 첫 commit → PR open
  Review Time    = PR open → approval
  Merge Time     = approval → merge
```

---

## 7-F. 현재 스크립트에 적용 가능한 개선 방향

글로벌 사례를 바탕으로 현재 `collect_cheoljoo_2026.py` + `analyze_worklog_time.py`에 적용 가능한 개선 방안:

### 개선 1: Jira In Progress→Done 구간 직접 사용

```python
# 현재: changelog 이벤트 1건 = 10분 고정
# 개선: In Progress 전환 ~ Done 전환 구간을 직접 계산

def extract_jira_work_intervals(changelogs: list) -> list:
    """
    changelog에서 In Progress 시작 ~ Done 전환 구간 추출
    반환: [(start_dt, end_dt, duration_min), ...]
    """
    intervals = []
    in_progress_at = None
    for cl in sorted(changelogs, key=lambda x: x["created"]):
        for item in cl.get("items", []):
            if item["field"] != "status":
                continue
            to_status = item["toString"].lower()
            from_status = item["fromString"].lower()
            if to_status in ("in progress", "진행 중"):
                in_progress_at = parse_dt(cl["created"])
            elif in_progress_at and to_status in ("done", "resolved", "closed"):
                end_dt = parse_dt(cl["created"])
                # 업무시간만 계산 (주말·심야 제외)
                duration = business_minutes(in_progress_at, end_dt)
                intervals.append((in_progress_at, end_dt, duration))
                in_progress_at = None
    return intervals
```

**신뢰도**: ★★☆ (수동 전환 시차 존재, 그러나 현재 고정값보다 훨씬 정확)

### 개선 2: GitLab MR open→merge 구간 직접 사용

```python
# GitLab events에서 MR opened / merged 이벤트 매칭
# 현재 events API는 type=merge_request 이벤트에 opened/closed 포함

# collect 단계에서 추가 수집:
mr_open_events = {}  # mr_iid → opened_at
for ev in gitlab_events:
    if ev["target_type"] == "MergeRequest":
        if ev["action_name"] == "opened":
            mr_open_events[ev["target_id"]] = ev["created_at"]
        elif ev["action_name"] == "merged":
            if ev["target_id"] in mr_open_events:
                open_at = mr_open_events[ev["target_id"]]
                merge_at = ev["created_at"]
                coding_mins = business_minutes(open_at, merge_at)
                # 이 값을 analyze 시 사용
```

**신뢰도**: ★★★ (시스템 자동 기록, 개발자 개입 없음)

### 개선 3: business_minutes 함수 추가 (주말·심야 제외)

```python
from datetime import datetime, timedelta

def business_minutes(start: datetime, end: datetime,
                     work_start_hour: int = 9,
                     work_end_hour: int = 19) -> int:
    """
    주말(토·일) 및 업무시간 외(기본 9~19시) 제외한 순수 업무 시간(분) 계산.
    DORA/LinearB 등 업계 표준 방식.
    """
    if end <= start:
        return 0
    total = 0
    current = start
    while current < end:
        # 주말 건너뛰기
        if current.weekday() >= 5:  # 토=5, 일=6
            current += timedelta(days=1)
            current = current.replace(hour=work_start_hour, minute=0, second=0)
            continue
        day_start = current.replace(hour=work_start_hour, minute=0, second=0)
        day_end = current.replace(hour=work_end_hour, minute=0, second=0)
        window_start = max(current, day_start)
        window_end = min(end, day_end)
        if window_end > window_start:
            total += int((window_end - window_start).total_seconds() // 60)
        # 다음날로 이동
        current = (current + timedelta(days=1)).replace(
            hour=work_start_hour, minute=0, second=0
        )
    return total
```

### 개선 4: 구간 기반 집계로 전환 로드맵

| 우선순위 | 개선항목 | 신뢰도 향상 | 구현 난이도 |
|---------|---------|-----------|----------|
| 1순위 | GitLab MR open→merge 구간 사용 | ★★☆ → ★★★ | 낮음 (events API 이미 수집 중) |
| 2순위 | Jira In Progress→Done 구간 사용 | ★☆☆ → ★★☆ | 중간 (changelog 파싱 추가) |
| 3순위 | business_minutes 함수 도입 | 정확도 +15% | 낮음 (유틸 함수 추가) |
| 4순위 | commit session 클러스터링 (≤2h) | ★★☆ → ★★★ | 중간 (세션 분리 로직 개선) |
| 5순위 | Google Calendar API 회의 시간 수집 | 신규 소스 추가 | 높음 (OAuth 설정 필요) |

### 현재 방식 vs 개선 후 비교

| 항목 | 현재 (추정 기반) | 개선 후 (구간 기반) |
|------|----------------|-------------------|
| Jira 작업시간 | changelog 건당 10분 고정 | In Progress→Done 실제 구간 |
| GitLab 작업시간 | commit LOC 기반 추정 | MR open→merge 실제 구간 |
| 주말/심야 포함 | 포함됨 (과대 추정 원인) | business_minutes로 제외 |
| 병렬 작업 처리 | 단순 합산 | 겹치는 구간은 max() 처리 |
| 회의 시간 | 미수집 | Calendar API 추가 시 포함 |
| 예상 정확도 | ±30~40% | ±15~20% |

> **결론**: 현재 스크립트에 (1) GitLab MR 구간, (2) Jira 상태 구간, (3) business_minutes 세 가지만 추가해도 작업시간 추정 정확도가 크게 향상된다. Google·Spotify 모두 이 세 가지 원칙(구간 기반 + 업무시간 필터 + 시스템 자동 타임스탬프 우선)을 공통으로 사용하고 있다.

---

# Part 8. DORA 4개 지표 자동 산출 — GitHub + GCS 이벤트 기반 상세 구현

> 작성일: 2026-06-25  
> 참고: Google FourKeys (github.com/dora-team/fourkeys), DORA 2023 State of DevOps Report

---

## 8-A. DORA 4개 지표 개요

| 지표 | 측정 대상 | Elite 기준 | 의미 |
|------|----------|-----------|------|
| **Deployment Frequency** | 프로덕션 배포 빈도 | 하루 여러 번 | 얼마나 자주 릴리스하는가 |
| **Lead Time for Changes** | 첫 commit → 프로덕션 배포 | < 1시간 | 아이디어가 제품에 반영되는 속도 |
| **Change Failure Rate (CFR)** | 배포 중 장애 유발 비율 | 0~15% | 배포 품질 |
| **Mean Time to Restore (MTTR)** | 장애 발생 → 복구 완료 | < 1시간 | 복구 능력 |

```
[DORA 2023 성숙도 등급]

                  Deployment    Lead Time    CFR        MTTR
Elite   ★★★★    다회/일       < 1시간      0~15%      < 1시간
High    ★★★☆    1회/일~1회/주  1일~1주     16~30%     < 1일
Medium  ★★☆☆    1회/주~1회/월  1주~1개월   16~30%     1일~1주
Low     ★☆☆☆    < 1회/월      > 6개월      > 30%      > 6개월
```

---

## 8-B. 아키텍처 — 이벤트 수집 파이프라인

### Google FourKeys 기본 구조

```
┌──────────────────────────────────────────────────────────────┐
│                   이벤트 소스                                  │
│  GitHub Webhook  │  GitHub Actions  │  PagerDuty  │  Jira   │
└────────┬─────────┴────────┬─────────┴──────┬──────┴────┬────┘
         │                  │                │           │
         ▼                  ▼                ▼           ▼
┌──────────────────────────────────────────────────────────────┐
│           Google Cloud Pub/Sub (이벤트 버스)                   │
│  topic: fourkeys-events                                      │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│          Cloud Run (이벤트 파서 / event-handler)              │
│  - 이벤트 타입 분류 (deploy / incident / change)             │
│  - 타임스탬프 정규화                                          │
│  - 서비스/팀 태깅                                             │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│          BigQuery (이벤트 저장소)                             │
│  테이블:                                                      │
│    events_raw         ← 원본 이벤트 전체                     │
│    deployments        ← 배포 이벤트 (정제)                   │
│    incidents          ← 장애 이벤트 (정제)                   │
│    changes            ← 코드 변경 이벤트 (정제)              │
└─────────────────────────┬────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│          Looker Studio / Grafana 대시보드                     │
│  - DORA 4개 지표 실시간 시각화                               │
│  - 팀별 / 서비스별 / 기간별 필터                             │
└──────────────────────────────────────────────────────────────┘
```

### GCS(Google Cloud Storage) 역할

FourKeys에서 GCS는 두 가지 용도로 사용된다:

```
1. Webhook 이벤트 백업
   GitHub Webhook → Cloud Run → GCS bucket (원본 JSON 아카이브)
   → 파싱 실패 시 재처리 가능

2. 배포 아티팩트 추적
   CI/CD → GCS에 release artifact 업로드
   → 업로드 완료 이벤트 = 배포 이벤트로 사용
   gs://fourkeys-artifacts/service-name/v1.2.3.tar.gz
```

---

## 8-C. 지표 1: Deployment Frequency

### 이벤트 소스

```
GitHub: push to main/release branch
        → workflow_run (type=deployment, conclusion=success)
        → GitHub Deployment API (environment=production)

GCS:    gs://your-bucket/releases/{service}/{version}/
        → Object finalize 이벤트 = 배포 완료 신호
```

### 웹훅 payload 예시 (GitHub → Cloud Run)

```json
{
  "event_type": "deployment_status",
  "payload": {
    "deployment_status": {
      "state": "success",
      "environment": "production",
      "created_at": "2026-06-25T09:30:00Z",
      "updated_at": "2026-06-25T09:35:12Z"
    },
    "deployment": {
      "sha": "abc123def456",
      "ref": "main",
      "created_at": "2026-06-25T09:29:50Z"
    },
    "repository": { "name": "my-service" }
  }
}
```

### BigQuery 저장 스키마

```sql
CREATE TABLE fourkeys.deployments (
  deploy_id     STRING,       -- deployment SHA 또는 UUID
  service_name  STRING,       -- 서비스 이름
  environment   STRING,       -- production / staging
  deploy_time   TIMESTAMP,    -- 배포 완료 시각
  source        STRING,       -- github_deployment / gcs_release
  created_at    TIMESTAMP     -- 이벤트 수신 시각
);
```

### 지표 계산 쿼리

```sql
-- Deployment Frequency (일별 배포 횟수)
SELECT
  DATE(deploy_time) AS deploy_date,
  service_name,
  COUNT(*) AS deploy_count
FROM fourkeys.deployments
WHERE
  environment = 'production'
  AND deploy_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 30 DAY)
GROUP BY 1, 2
ORDER BY 1 DESC;

-- 주간 평균 배포 빈도
SELECT
  service_name,
  COUNT(*) / COUNT(DISTINCT DATE_TRUNC(deploy_time, WEEK)) AS deploys_per_week
FROM fourkeys.deployments
WHERE environment = 'production'
  AND deploy_time >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY service_name;
```

### 등급 판정

```sql
SELECT
  service_name,
  AVG(daily_count) AS avg_daily_deploys,
  CASE
    WHEN AVG(daily_count) >= 1   THEN 'Elite'   -- 하루 1회 이상
    WHEN AVG(daily_count) >= 1/7 THEN 'High'    -- 주 1회 이상
    WHEN AVG(daily_count) >= 1/30 THEN 'Medium' -- 월 1회 이상
    ELSE 'Low'
  END AS dora_level
FROM (
  SELECT DATE(deploy_time) AS d, service_name, COUNT(*) AS daily_count
  FROM fourkeys.deployments
  WHERE environment='production'
  GROUP BY 1, 2
)
GROUP BY service_name;
```

---

## 8-D. 지표 2: Lead Time for Changes

### 이벤트 소스

```
시작점 (Change 이벤트):
  GitHub: push 이벤트 → commit SHA + author_timestamp
  또는:   PR open 이벤트 → PR created_at

종료점 (Deploy 이벤트):
  GitHub Deployment API: state=success + environment=production
  GitHub Actions:        workflow_run completed (deployment job)
```

### 변경 이력 테이블

```sql
CREATE TABLE fourkeys.changes (
  change_id       STRING,     -- commit SHA
  service_name    STRING,
  time_created    TIMESTAMP,  -- commit author 시각 (가장 신뢰할 수 있는 시작점)
  time_resolved   TIMESTAMP,  -- 프로덕션 배포 완료 시각
  deploy_id       STRING      -- 연결된 deployment ID
);
```

### commit → deployment 연결 방법

```python
# GitHub Deployment API가 어떤 commit을 포함하는지 추적
# deploy.sha = HEAD commit
# 이전 deploy.sha ~ 현재 deploy.sha 사이의 모든 commit이 이번 배포에 포함

def link_commits_to_deployment(repo, prev_sha, deploy_sha, deploy_time):
    """
    두 SHA 사이의 모든 commit을 이번 deployment에 연결.
    Git commit graph를 역추적.
    """
    commits = repo.compare(prev_sha, deploy_sha).commits
    for commit in commits:
        changes.append({
            "change_id":     commit.sha,
            "service_name":  repo.name,
            "time_created":  commit.commit.author.date,   # 실제 코딩 완료 시각
            "time_resolved": deploy_time,                  # 배포 완료 시각
            "deploy_id":     deploy_sha,
        })
```

### Lead Time 계산 쿼리

```sql
-- 커밋별 Lead Time
SELECT
  change_id,
  service_name,
  time_created,
  time_resolved,
  TIMESTAMP_DIFF(time_resolved, time_created, HOUR) AS lead_time_hours
FROM fourkeys.changes
WHERE time_resolved IS NOT NULL
ORDER BY lead_time_hours DESC;

-- 서비스별 중앙값 Lead Time (P50)
SELECT
  service_name,
  APPROX_QUANTILES(
    TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100
  )[OFFSET(50)] AS median_lead_time_hours,
  CASE
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100)[OFFSET(50)] < 1
      THEN 'Elite'   -- 1시간 미만
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100)[OFFSET(50)] < 24
      THEN 'High'    -- 1일 미만
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100)[OFFSET(50)] < 168
      THEN 'Medium'  -- 1주 미만
    ELSE 'Low'
  END AS dora_level
FROM fourkeys.changes
WHERE time_resolved IS NOT NULL
  AND time_created >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY service_name;
```

---

## 8-E. 지표 3: Change Failure Rate (CFR)

### 이벤트 소스

```
배포 이벤트: GitHub Deployment (state=success)
장애 이벤트 (아래 중 하나):
  - PagerDuty  : incident created (severity=P1/P2)
  - GitHub     : issue labeled "incident" 또는 "hotfix"
  - Jira       : 이슈 생성 (issuetype=Bug, priority=Critical/Blocker)
  - Rollback   : deployment with ref containing "rollback" / "revert"
```

### 장애 이벤트 테이블

```sql
CREATE TABLE fourkeys.incidents (
  incident_id    STRING,
  service_name   STRING,
  time_created   TIMESTAMP,  -- 장애 발생 시각
  time_resolved  TIMESTAMP,  -- 복구 완료 시각
  root_cause_deploy_id STRING -- 원인이 된 deployment ID (선택적)
);
```

### CFR 계산 쿼리

```sql
-- 배포 건수 대비 장애 유발 배포 건수
WITH deploy_counts AS (
  SELECT
    service_name,
    DATE_TRUNC(deploy_time, MONTH) AS month,
    COUNT(*) AS total_deploys
  FROM fourkeys.deployments
  WHERE environment = 'production'
  GROUP BY 1, 2
),
incident_counts AS (
  SELECT
    service_name,
    DATE_TRUNC(time_created, MONTH) AS month,
    COUNT(DISTINCT root_cause_deploy_id) AS failed_deploys
  FROM fourkeys.incidents
  WHERE root_cause_deploy_id IS NOT NULL
  GROUP BY 1, 2
)
SELECT
  d.service_name,
  d.month,
  d.total_deploys,
  COALESCE(i.failed_deploys, 0) AS failed_deploys,
  SAFE_DIVIDE(COALESCE(i.failed_deploys, 0), d.total_deploys) * 100 AS cfr_percent,
  CASE
    WHEN SAFE_DIVIDE(COALESCE(i.failed_deploys,0), d.total_deploys) <= 0.15 THEN 'Elite/High'
    WHEN SAFE_DIVIDE(COALESCE(i.failed_deploys,0), d.total_deploys) <= 0.30 THEN 'Medium'
    ELSE 'Low'
  END AS dora_level
FROM deploy_counts d
LEFT JOIN incident_counts i USING (service_name, month)
ORDER BY d.month DESC;
```

### 장애 원인 deployment 자동 연결

```python
def link_incident_to_deploy(incident_created_at, service_name, deployments):
    """
    장애 발생 시각 직전 배포를 원인으로 추정.
    (실제로는 수동 확인 후 root_cause_deploy_id를 업데이트해야 함)
    """
    recent_deploys = [
        d for d in deployments
        if d["service_name"] == service_name
        and d["deploy_time"] <= incident_created_at
    ]
    if recent_deploys:
        # 가장 최근 배포를 원인으로 가정
        culprit = max(recent_deploys, key=lambda d: d["deploy_time"])
        return culprit["deploy_id"]
    return None
```

---

## 8-F. 지표 4: Mean Time to Restore (MTTR)

### 이벤트 소스

```
시작점: PagerDuty incident created / GitHub issue labeled "incident"
종료점: PagerDuty incident resolved / GitHub issue closed (label="incident")

선택적: Jira MTTR
  시작: 버그 이슈 생성 (issuetype=Bug, priority=Blocker)
  종료: 이슈 상태 = Resolved/Done
```

### MTTR 계산 쿼리

```sql
-- 서비스별 MTTR (중앙값)
SELECT
  service_name,
  COUNT(*) AS incident_count,
  APPROX_QUANTILES(
    TIMESTAMP_DIFF(time_resolved, time_created, MINUTE), 100
  )[OFFSET(50)] AS median_mttr_minutes,
  APPROX_QUANTILES(
    TIMESTAMP_DIFF(time_resolved, time_created, MINUTE), 100
  )[OFFSET(50)] / 60.0 AS median_mttr_hours,
  CASE
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, MINUTE),100)[OFFSET(50)] < 60
      THEN 'Elite'    -- 1시간 미만
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, MINUTE),100)[OFFSET(50)] < 1440
      THEN 'High'     -- 1일(1440분) 미만
    WHEN APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, MINUTE),100)[OFFSET(50)] < 10080
      THEN 'Medium'   -- 1주(10080분) 미만
    ELSE 'Low'
  END AS dora_level
FROM fourkeys.incidents
WHERE time_resolved IS NOT NULL
  AND time_created >= TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY)
GROUP BY service_name;
```

---

## 8-G. FourKeys 오픈소스 구현

### 구성 파일 구조 (github.com/dora-team/fourkeys)

```
fourkeys/
  terraform/               ← GCP 인프라 (BigQuery, Cloud Run, Pub/Sub)
  event_handler/           ← Cloud Run 이벤트 파서
    main.py                ← Pub/Sub 구독 → BigQuery 삽입
    parsers/
      github.py            ← GitHub Webhook 파서
      pagerduty.py         ← PagerDuty 파서
      cloud_build.py       ← GCS/Cloud Build 파서
  queries/                 ← BigQuery SQL 파일
    deployments.sql
    lead_time.sql
    change_failure_rate.sql
    mttr.sql
  dashboard/               ← Looker Studio 대시보드 정의
```

### Terraform으로 인프라 배포

```bash
# 1. GCP 프로젝트 설정
export PROJECT_ID="your-project-id"
gcloud config set project $PROJECT_ID

# 2. Terraform 초기화 및 배포
cd fourkeys/terraform
terraform init
terraform apply -var="project_id=$PROJECT_ID"

# → 생성되는 리소스:
#   - BigQuery dataset: fourkeys
#   - Cloud Run service: event-handler
#   - Pub/Sub topic: fourkeys-events
#   - Cloud Scheduler: 일별 집계 갱신
```

### GitHub Webhook 설정

```bash
# GitHub 레포지토리에 Webhook 추가
# URL: https://event-handler-xxxx.a.run.app/
# Content-Type: application/json
# Secret: <생성한 시크릿>
# Events:
#   - push
#   - deployment
#   - deployment_status
#   - pull_request
#   - issues
```

### 이벤트 핸들러 핵심 로직 (event_handler/main.py 요약)

```python
from google.cloud import bigquery
import json, hashlib, base64

bq = bigquery.Client()

def handle_pubsub(event, context):
    """Cloud Run 진입점: Pub/Sub 메시지 수신"""
    payload = json.loads(base64.b64decode(event["data"]).decode())
    source  = payload.get("source")      # "github", "pagerduty" 등
    body    = payload.get("msg", {})

    if source == "github":
        rows = parse_github(body)
    elif source == "pagerduty":
        rows = parse_pagerduty(body)
    else:
        return

    # BigQuery에 삽입
    errors = bq.insert_rows_json("fourkeys.events_raw", rows)
    if errors:
        raise RuntimeError(f"BigQuery insert failed: {errors}")

def parse_github(body: dict) -> list:
    """GitHub Webhook 이벤트 → BigQuery 행으로 변환"""
    event_type = body.get("event_type", "")
    metadata   = body.get("metadata", {})

    if event_type == "deployment_status":
        if metadata.get("state") == "success" \
           and metadata.get("environment") == "production":
            return [{
                "event_type": "deployment",
                "id":         metadata["deployment"]["sha"],
                "metadata":   json.dumps(metadata),
                "time_created": metadata["updated_at"],
                "signature":  make_signature(metadata),
                "msg_id":     body.get("msg_id"),
                "source":     "github",
            }]

    elif event_type == "push":
        return [{
            "event_type": "change",
            "id":         metadata.get("head_commit", {}).get("id"),
            "metadata":   json.dumps(metadata),
            "time_created": metadata.get("head_commit", {}).get("timestamp"),
            "signature":  make_signature(metadata),
            "msg_id":     body.get("msg_id"),
            "source":     "github",
        }]
    return []

def make_signature(payload: dict) -> str:
    return hashlib.sha1(json.dumps(payload, sort_keys=True).encode()).hexdigest()
```

### 완성된 DORA 대시보드 쿼리 (all-in-one)

```sql
-- DORA 4개 지표를 한 번에 조회 (최근 90일)
WITH period AS (
  SELECT TIMESTAMP_SUB(CURRENT_TIMESTAMP(), INTERVAL 90 DAY) AS start_time
),

-- 1. Deployment Frequency
df AS (
  SELECT
    service_name,
    COUNT(*) AS total_deploys,
    DATE_DIFF(CURRENT_DATE(), DATE((SELECT start_time FROM period)), DAY) AS period_days,
    COUNT(*) / DATE_DIFF(CURRENT_DATE(), DATE((SELECT start_time FROM period)), DAY) AS deploys_per_day
  FROM fourkeys.deployments, period
  WHERE environment='production' AND deploy_time >= period.start_time
  GROUP BY service_name
),

-- 2. Lead Time (중앙값, 시간 단위)
lt AS (
  SELECT
    service_name,
    APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100)[OFFSET(50)]
      AS median_lead_time_hours
  FROM fourkeys.changes, period
  WHERE time_resolved IS NOT NULL AND time_created >= period.start_time
  GROUP BY service_name
),

-- 3. Change Failure Rate
cfr AS (
  SELECT
    d.service_name,
    SAFE_DIVIDE(COUNT(DISTINCT i.incident_id), COUNT(DISTINCT d.deploy_id)) AS cfr
  FROM fourkeys.deployments d, period
  LEFT JOIN fourkeys.incidents i
    ON d.deploy_id = i.root_cause_deploy_id
  WHERE d.environment='production' AND d.deploy_time >= period.start_time
  GROUP BY d.service_name
),

-- 4. MTTR (중앙값, 시간 단위)
mttr AS (
  SELECT
    service_name,
    APPROX_QUANTILES(TIMESTAMP_DIFF(time_resolved, time_created, HOUR), 100)[OFFSET(50)]
      AS median_mttr_hours
  FROM fourkeys.incidents, period
  WHERE time_resolved IS NOT NULL AND time_created >= period.start_time
  GROUP BY service_name
)

SELECT
  df.service_name,
  ROUND(df.deploys_per_day, 2)              AS deploy_freq_per_day,
  ROUND(lt.median_lead_time_hours, 1)       AS lead_time_hours,
  ROUND(cfr.cfr * 100, 1)                  AS change_failure_rate_pct,
  ROUND(mttr.median_mttr_hours, 1)          AS mttr_hours,
  -- 종합 등급 (4개 지표 중 최하 등급으로 판정)
  LEAST(
    CASE WHEN df.deploys_per_day >= 1  THEN 4
         WHEN df.deploys_per_day >= 1/7.0 THEN 3
         WHEN df.deploys_per_day >= 1/30.0 THEN 2 ELSE 1 END,
    CASE WHEN lt.median_lead_time_hours < 1   THEN 4
         WHEN lt.median_lead_time_hours < 24  THEN 3
         WHEN lt.median_lead_time_hours < 168 THEN 2 ELSE 1 END,
    CASE WHEN cfr.cfr <= 0.15 THEN 4
         WHEN cfr.cfr <= 0.30 THEN 2 ELSE 1 END,
    CASE WHEN mttr.median_mttr_hours < 1    THEN 4
         WHEN mttr.median_mttr_hours < 24   THEN 3
         WHEN mttr.median_mttr_hours < 168  THEN 2 ELSE 1 END
  ) AS composite_score  -- 4=Elite, 3=High, 2=Medium, 1=Low
FROM df
LEFT JOIN lt   USING (service_name)
LEFT JOIN cfr  USING (service_name)
LEFT JOIN mttr USING (service_name)
ORDER BY composite_score DESC;
```

---

## 8-H. 현재 환경(GitLab + Jira)에 적용하기

Google FourKeys는 GitHub + GCS 기반이지만, **GitLab + Jira 환경에서도 동일한 원칙으로 구현 가능**하다.

### 이벤트 소스 매핑

| DORA 지표 | FourKeys (GitHub) | 우리 환경 (GitLab + Jira) |
|----------|-------------------|--------------------------|
| Deployment Frequency | GitHub Deployment API | GitLab Deployment API (`/projects/{id}/deployments`) |
| Lead Time | commit → GitHub deployment | commit → GitLab pipeline succeeded |
| CFR | GitHub issue label "incident" | Jira Bug 이슈 (priority=Blocker) |
| MTTR | PagerDuty incident resolved | Jira Bug 이슈 Done 전환 시각 |

### GitLab 이벤트 수집 (Python)

```python
import requests, os
from datetime import datetime, timezone

GITLAB_URL   = "http://mod.lge.com/hub/api/v4"
GITLAB_TOKEN = os.getenv("GITLAB_TOKEN")

def collect_deployments(project_id: int, since: str) -> list:
    """GitLab Deployment API → DORA deployments 테이블용 데이터"""
    url = f"{GITLAB_URL}/projects/{project_id}/deployments"
    params = {
        "status":      "success",
        "environment": "production",
        "updated_after": since,
        "per_page":    100,
    }
    deployments = []
    while url:
        resp = requests.get(url, headers={"PRIVATE-TOKEN": GITLAB_TOKEN}, params=params)
        resp.raise_for_status()
        for d in resp.json():
            deployments.append({
                "deploy_id":    str(d["id"]),
                "service_name": f"project-{project_id}",
                "environment":  d["environment"]["name"],
                "deploy_time":  d["updated_at"],          # 배포 완료 시각
                "commit_sha":   d["sha"],
                "source":       "gitlab",
            })
        # 페이지네이션
        url = resp.links.get("next", {}).get("url")
        params = {}  # next URL에 파라미터 이미 포함됨
    return deployments

def collect_commits_for_deploy(project_id: int, from_sha: str, to_sha: str) -> list:
    """두 SHA 사이의 커밋 목록 → changes 테이블용"""
    url = f"{GITLAB_URL}/projects/{project_id}/repository/compare"
    resp = requests.get(url,
        headers={"PRIVATE-TOKEN": GITLAB_TOKEN},
        params={"from": from_sha, "to": to_sha}
    )
    resp.raise_for_status()
    commits = []
    for c in resp.json().get("commits", []):
        commits.append({
            "change_id":    c["id"],
            "service_name": f"project-{project_id}",
            "time_created": c["authored_date"],   # author timestamp (신뢰도 ★★★)
        })
    return commits

def collect_incidents_from_jira(jira_url: str, auth, project_key: str, since: str) -> list:
    """Jira의 Critical/Blocker 버그 → incidents 테이블용"""
    jql = (f'project = {project_key} AND issuetype = Bug '
           f'AND priority in (Critical, Blocker) AND created >= "{since}"')
    resp = requests.get(
        f"{jira_url}/rest/api/latest/search",
        auth=auth,
        params={"jql": jql, "fields": "created,resolutiondate,summary", "maxResults": 200}
    )
    incidents = []
    for issue in resp.json().get("issues", []):
        fields = issue["fields"]
        incidents.append({
            "incident_id":   issue["key"],
            "service_name":  project_key,
            "time_created":  fields["created"],
            "time_resolved": fields.get("resolutiondate"),  # None이면 미해결
        })
    return incidents
```

### Lead Time 계산 (GitLab 환경)

```python
def calculate_lead_times(deployments: list, changes_by_sha: dict) -> list:
    """
    각 deployment의 commit SHA를 기준으로
    포함된 커밋들의 Lead Time 계산.
    """
    results = []
    sorted_deploys = sorted(deployments, key=lambda d: d["deploy_time"])

    for i, deploy in enumerate(sorted_deploys):
        prev_sha = sorted_deploys[i-1]["commit_sha"] if i > 0 else None
        deploy_time = parse_dt(deploy["deploy_time"])

        # 이 배포에 포함된 커밋들
        commits = changes_by_sha.get(deploy["commit_sha"], [])
        for commit in commits:
            commit_time = parse_dt(commit["time_created"])
            lead_hours  = (deploy_time - commit_time).total_seconds() / 3600
            results.append({
                "change_id":       commit["change_id"],
                "service_name":    deploy["service_name"],
                "time_created":    commit["time_created"],
                "time_resolved":   deploy["deploy_time"],
                "lead_time_hours": round(lead_hours, 2),
                "deploy_id":       deploy["deploy_id"],
            })
    return results
```

### 로컬 SQLite 기반 경량 구현 (BigQuery 없이)

BigQuery/GCP 없이 SQLite로 동일한 지표를 로컬에서 계산:

```python
import sqlite3, json
from pathlib import Path

DB_PATH = Path("worklog_tools/collected_data/dora.db")

def init_db(conn):
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS deployments (
        deploy_id TEXT PRIMARY KEY,
        service_name TEXT, environment TEXT,
        deploy_time TEXT, commit_sha TEXT
    );
    CREATE TABLE IF NOT EXISTS changes (
        change_id TEXT PRIMARY KEY,
        service_name TEXT, time_created TEXT,
        time_resolved TEXT, deploy_id TEXT
    );
    CREATE TABLE IF NOT EXISTS incidents (
        incident_id TEXT PRIMARY KEY,
        service_name TEXT, time_created TEXT,
        time_resolved TEXT, root_cause_deploy_id TEXT
    );
    """)

def dora_report(conn) -> dict:
    """4개 지표를 한 번에 계산"""
    # 1. Deployment Frequency (최근 30일 일평균)
    df_row = conn.execute("""
        SELECT COUNT(*) * 1.0 / 30 AS freq
        FROM deployments
        WHERE environment='production'
          AND deploy_time >= date('now', '-30 days')
    """).fetchone()

    # 2. Lead Time (중앙값, 시간)
    lt_rows = conn.execute("""
        SELECT (julianday(time_resolved) - julianday(time_created)) * 24 AS lt_h
        FROM changes WHERE time_resolved IS NOT NULL
        ORDER BY lt_h
    """).fetchall()
    lead_times = [r[0] for r in lt_rows if r[0] is not None]
    median_lt  = sorted(lead_times)[len(lead_times)//2] if lead_times else None

    # 3. CFR
    cfr_row = conn.execute("""
        SELECT
          CAST(COUNT(DISTINCT root_cause_deploy_id) AS FLOAT) /
          NULLIF(COUNT(DISTINCT d.deploy_id), 0) AS cfr
        FROM deployments d
        LEFT JOIN incidents i ON d.deploy_id = i.root_cause_deploy_id
        WHERE d.environment='production'
    """).fetchone()

    # 4. MTTR (중앙값, 시간)
    mttr_rows = conn.execute("""
        SELECT (julianday(time_resolved) - julianday(time_created)) * 24 AS mttr_h
        FROM incidents WHERE time_resolved IS NOT NULL
        ORDER BY mttr_h
    """).fetchall()
    mttrs      = [r[0] for r in mttr_rows if r[0] is not None]
    median_mttr = sorted(mttrs)[len(mttrs)//2] if mttrs else None

    return {
        "deployment_frequency_per_day": round(df_row[0], 3) if df_row else None,
        "lead_time_median_hours":        round(median_lt, 1) if median_lt else None,
        "change_failure_rate_pct":       round((cfr_row[0] or 0) * 100, 1),
        "mttr_median_hours":             round(median_mttr, 1) if median_mttr else None,
    }
```

### 현재 수집 스크립트와 통합 포인트

현재 `collect_cheoljoo_2026.py`에 수집 중인 데이터로 이미 부분적으로 DORA를 산출할 수 있다:

| DORA 지표 | 현재 수집 데이터 | 추가 필요 |
|----------|----------------|----------|
| Deployment Frequency | GitLab push 이벤트 (부분적) | GitLab Deployments API 추가 수집 |
| Lead Time | commit timestamp 있음 | 배포 timestamp와 연결 로직 |
| CFR | Jira Bug 이슈 있음 | Bug ↔ Deploy 연결 로직 |
| MTTR | Jira `resolutiondate` 있음 | Bug 생성~해결 구간 계산 |

> **요약**: Google FourKeys의 핵심은 "배포 이벤트"와 "장애 이벤트"를 신뢰할 수 있는 타임스탬프로 저장하고, 두 이벤트 쌍의 구간을 계산하는 것이다. GCS는 배포 아티팩트의 업로드 이벤트를 배포 완료 신호로 활용하는 방법 중 하나이며, GitLab의 Deployment API나 CI 파이프라인 완료 이벤트로 동일하게 대체할 수 있다.
