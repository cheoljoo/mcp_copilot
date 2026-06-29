# Worklog Brief — 자동 Worklog 시스템 설계 및 조사 요약

> 원본: `worklog.md`  
> 본 문서는 코드(SQL/Python) 및 개인 실제 업무 기록(월별 Jira 티켓/커밋 상세, 소요시간 추정 수치)을 제외하고, 시스템 설계와 외부 사례 조사 내용만 요약합니다.

---

## 1. 배경 및 목적

개발팀의 Jira Worklog 수동 작성은 번거롭고 누락이 잦다. Jira / Confluence(Collab) / Gerrit / GitHub / GitLab / Local git 등 여러 데이터 소스에서 개발자 활동을 자동으로 수집·집계하여, 개인별 활동 통계를 만들고 Jira Worklog에 자동 삽입하는 시스템을 설계·구현했다.

핵심 목표: **"개인별로 어떠한 일을 했는지 DB화 시킨다."**

---

## 2. 시스템 아키텍처 (개요)

```
[데이터 수집 레이어]
  Jira / Confluence / Gerrit / GitHub / GitLab / Local git 수집기
            ↓ (List[Activity])
[통합 집계 레이어]
  사용자별·날짜별 정규화, 통계 계산 (활동건수/활동일/유형별/소스별 분포)
            ↓
[출력]
  JSON(raw) / CSV(피벗) / Markdown(개인별 worklog) → Jira Worklog API 자동 삽입
```

구현 모듈: Jira/Confluence 수집기, Gerrit/GitHub/GitLab/Local-git 수집기, 통합 집계기(+Jira worklog 자동 삽입 기능). Mock 데이터 기반 데모로 파이프라인 전체 동작을 검증했다.

### 더 정밀한 worklog를 위해 추가로 필요한 정보

| 영역 | 항목 |
|---|---|
| 코드 기여 품질 | 변경 라인 수, 리뷰 코멘트 수/반복 횟수, CI 결과 연동 |
| 회의·커뮤니케이션 | 캘린더 참석, Slack/Teams 활동, Email |
| Jira 심층 | Story Point, 스프린트 배정/완료, 블로커, 하위 태스크 |
| Confluence 심층 | 신규 생성 vs 편집 구분, 열람 수, 멘션 수 |
| 업무 외 맥락 | 휴가/병가, 온콜 여부, 리뷰 SLA |

### 향후 개선 방향 (시스템 자체)

1. 웹훅 기반 실시간 처리 (이벤트 발생 즉시 worklog 삽입)
2. AI 요약 — 하루 활동을 LLM이 한 문장으로 요약해 Jira 댓글로 삽입
3. 팀 통계 대시보드 (Grafana/Kibana)
4. 중복 방지 (기존 auto-worklog 존재 여부 확인)
5. 커밋 크기·리뷰 코멘트 수 기반 소요시간 자동 추정
6. MCP 서버화 — 파이프라인을 MCP 도구로 노출하여 Copilot에서 직접 호출

---

## 3. Spotify Backstage(Developer Portal) 조사 결론

Backstage는 Spotify가 공개하고 현재 CNCF Incubation 프로젝트로 운영되는 Developer Portal 프레임워크. Software Catalog(서비스/오너십 등록), Software Templates(스캐폴딩), TechDocs(문서), Kubernetes 뷰, 통합 검색이 핵심 기능이며, Jira/GitLab/GitHub/DORA Metrics 등 다양한 플러그인 생태계를 가진다.

**Worklog 관점 핵심 결론**
- Backstage는 시간 추적 도구가 아니라 "포털(조회·탐색)"이다. 각 시스템(Jira/GitLab/git 등)의 타임스탬프를 사후에 읽어와 보여줄 뿐이다.
- "작업 시작"을 Backstage Template에서 선언해야만 시작 시각을 신뢰성 있게 기록할 수 있고(TimeSaver 플러그인), 나머지는 결과만 사후 반영된다.
- 우리 환경(Gerrit 중심)은 Gerrit용 공식 플러그인이 없어 커스텀 구현 부담이 크다 → **현재의 Python 스크립트(사후 수집) 방식이 현실적으로 더 적합**.
- Backstage와 현재 스크립트는 상호 보완적: Backstage = 팀/조직 단위 카탈로그·표준화, 현재 스크립트 = 개인 단위 사후 활동 집계.

### Backstage 중앙화 효과 분석 (추가 조사)

- 중앙화(Software Catalog)는 서비스 발견, 의존성 파악, 문서 접근, 온보딩, 고아 서비스 제거 등에서 명확한 이점을 준다.
- 그러나 Backstage를 거치지 않고 직접 작업해도 기능적으로는 문제없다 — Backstage는 게이트키퍼가 아니라 뷰어이기 때문. 다만 "작업 시작 선언"이 Backstage를 거치지 않으면 메타데이터(특히 시간)가 누락된다.
- 결론: Backstage는 "발견과 파악"의 포털로는 탁월하지만, worklog 신뢰성은 "모든 작업이 Backstage를 통해 시작되는가"에 달려 있다. Google·Spotify도 Template 기반 작업에만 시간 추적을 적용하고 나머지는 사후 집계한다.

---

## 4. 사후 작업시간 측정 — 글로벌 사례 조사 결론

별도 타임트래커 없이 각 시스템에 남는 타임스탬프를 사후에 집계하는 방법론을 조사함.

**핵심 원리**: 어떤 이벤트 쌍을 작업의 시작/종료 경계로 볼 것인가 (Event-Pair Model).
신뢰도 등급: git author timestamp·PR open→merge 구간(★★★) > Jira In Progress→Done, 리뷰 첫 댓글→approval(★★☆) > Jira updated timestamp, Confluence 편집 timestamp(★☆☆, 노이즈 많음).

**기업별 접근**
- **Google**: Buganizer/Critique/Piper/Forge 등 자체 도구 스택. 개인 시간보다 팀 단위 흐름(flow) 지표(DORA, 리뷰 wait time 등) 중심. "Task" 단위(연속 커밋 클러스터링)로 구현 시간을 추정.
- **Spotify**: Squad 자율 운영, 회사 전체 강제 worklog 없음. Backstage TimeSaver로 Template 기반 작업만 시간 절감 측정. 철학: "결과를 측정하라, 시간이 아니라."
- **Microsoft/GitHub**: SPACE 프레임워크(Satisfaction/Performance/Activity/Communication/Efficiency)와 PR Cycle Time 지표.
- **Netflix**: Paved Road + DORA, 회의 없는 비동기 문화.
- **Atlassian**: Jira 내장 수동 Log Work + Tempo Timesheets의 반자동 활동 감지.
- **LinkedIn/Shopify**: Commit-to-Deploy 시간, PR 단계별 대기 시간 모니터링. "개발자에게 측정을 강요하지 않는다"는 철학 공유.

**상용 도구**: LinearB, Waydev, Pluralsight Flow, DX Data, Jellyfish, Swarmia, Tempo Timesheets — 대부분 Git+Jira/GitHub 타임스탬프 기반의 사후 집계.

**현재 시스템에 적용 가능한 개선 방향 (우선순위)**
1. GitLab MR open→merge 구간을 실제 소요시간으로 직접 사용 (신뢰도 ★★★, 구현 난이도 낮음)
2. Jira In Progress→Done changelog 구간을 고정값 대신 실제 구간으로 계산
3. 업무시간(주말/심야 제외) 필터 함수 도입
4. 커밋 세션 클러스터링(간격 2시간 이내 = 동일 세션)으로 신뢰도 향상
5. Google Calendar API 연동으로 회의 시간 보강 (신규 소스, 구현 난이도 높음)

---

## 5. DORA 4개 지표 자동 산출 조사 결론

DORA(Deployment Frequency, Lead Time for Changes, Change Failure Rate, MTTR) 4개 지표를 이벤트 기반으로 자동 산출하는 구조를 Google FourKeys(오픈소스) 기준으로 조사함.

- 아키텍처 공통 패턴: [이벤트 소스(웹훅/CI)] → [이벤트 버스] → [파서] → [정형 저장소] → [대시보드].
- 각 지표는 "시작 이벤트 ↔ 종료 이벤트" 쌍의 시간 차로 계산된다 (예: 첫 commit→배포 완료 = Lead Time, 장애 생성→해소 = MTTR).
- 우리 환경(GitLab + Jira)에서도 동일한 원칙으로 매핑 가능: GitLab Deployment API/Pipeline 성공 이벤트, Jira Bug 이슈(priority=Blocker)의 생성~해결 구간을 각각 배포·장애 이벤트로 사용.
- 현재 수집 스크립트가 이미 가진 데이터(GitLab push, commit timestamp, Jira resolutiondate)만으로도 DORA 지표를 부분적으로 산출할 수 있으며, 추가로 필요한 것은 GitLab Deployments API 수집과 배포↔커밋/버그 연결 로직이다.

---

## 6. 향후 계획

### Short-term (현재 보유 자산 기반, 수주~1~2개월)

- **GitLab MR open→merge, Jira In Progress→Done 구간 적용**: 기존 `collect_cheoljoo_2026.py` / `analyze_worklog_time.py`에 실제 이벤트 구간 기반 시간 계산을 추가해 소요시간 추정 정확도를 높인다(현재 추정 방식의 가장 손쉬운 개선).
- **business_minutes(업무시간 필터) 도입**: 주말·심야를 제외한 순수 업무시간만 집계하도록 보정.
- **Jira Worklog 자동 삽입 파이프라인 검증**: 현재 mock 데모로만 검증된 `worklog_aggregator.py`의 `--insert-jira-worklog` 흐름을 실제 Jira 서버 대상 소규모 파일럿으로 검증.
- **중복 방지 로직 추가**: 동일 활동에 대해 worklog가 중복 삽입되지 않도록 기존 auto-worklog 존재 여부 확인 로직 추가.
- **Gerrit 수집 보완**: 현재 0건으로 수집되는 Gerrit 데이터를 개인 HTTP 비밀번호 발급 등으로 보완.

### Long-term (3개월 이상, 구조적 확장)

- **MCP 서버화**: 현재 파이프라인(수집기+집계기)을 MCP 도구로 노출하여 Copilot/Claude 등에서 직접 호출 가능하게 만든다.
- **이벤트 기반 실시간 처리**: 배치(주기적 polling) 방식에서 Gerrit submit/Jira transition 등 웹훅 기반 실시간 처리로 전환.
- **AI 기반 일일 활동 요약**: 하루 활동을 LLM이 요약해 Jira worklog 코멘트로 자동 삽입.
- **DORA 지표 자동화**: GitLab Deployments API 및 Jira Bug 이슈를 연결해 Deployment Frequency / Lead Time / CFR / MTTR을 정기적으로 산출하는 경량(SQLite 등) 파이프라인 구축.
- **팀 단위 대시보드**: 개인 worklog 누적 데이터를 팀 단위로 시각화(Grafana/Kibana 등)하여 흐름(flow) 지표 중심으로 운영에 활용.
- **Backstage 도입 검토(선택적)**: 서비스 카탈로그·신규 서비스 표준화가 필요해지는 시점에, 현재 worklog 스크립트를 Backstage Entity와 연동하는 커스텀 플러그인 형태로 통합하는 방안을 재검토.
