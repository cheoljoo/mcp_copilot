# 2026년 상반기 업무 성과 보고 (목표 대비 실적)

> 작성자: 이철주 책임 (SW QCD Management Unit)
> 보고 기준: 2026년 1월 ~ 6월 (상반기)
> 근거 자료: `2026-audit-trail-detailed.md` (Confluence 기술문서 / Jira 티켓·코멘트 전수 감사추적), `2026-goal.txt`

---

## 0. 요약 (Executive Summary)

2026년 상반기 동안 조직의 3대 목표인 **① Data 기반 리소스 관리(40%)**, **② Data 기반 프로젝트 관리(40%)**, **③ 역량 강화(20%)** 에 직접 부합하는 업무를 중심으로 수행했습니다.

핵심 성과는 다음과 같습니다.

- **TicketSage(결함 티켓 자동 분석 플랫폼)** 를 구축·고도화하여, 50만 건 규모의 전사 결함 티켓에 대한 LLM 기반 요약·분류·진성/가성(TP/FP) 판정 체계를 마련했습니다. → **품질 데이터 기반 의사결정의 토대 확보**.
- **CCR(Code Change Request) Readiness / CCR 2.0(Gen2)** 분석 체계를 설계·구현하여 Shift-Left 관점의 프로세스 준수 여부를 자동 검증하고, 상태별 체류시간·리뷰어 부하 등 **QCD 복합지표를 신규 발굴**했습니다.
- **LGEDV Crash 검출 자동화** 에서 고객(LGEDV) 검증 기준 **True Positive 검출 정확도 100%** 를 달성하여 고객으로부터 "더 이상 파일 업로드가 불필요하다"는 회신을 받았습니다.
- **Copilot CLI / MCP / FastAPI 기반 AI 분석 인프라** 를 구축하여 LLM 자동 분석(Hexa Index)과 사내 활용 환경을 마련하고, 관련 **세미나 3건 이상**을 통해 조직 역량 강화에 기여했습니다.

---

## 1. 목표 ① Data 기반 리소스 관리 (가중치 40%)

> **조직 KPI**: SW개발 생산성 지표 평균 3.75/5.0 (25년 3.26 대비 15% 개선, 결함밀도 포함)
> **Action Item**: SW 개발자 생산성 지표 고도화 / 데이터 기반 의사결정 지원 및 최적화 방안 도출

### 1.1 개발자 생산성·리소스 지표 데이터화

| 업무 | 티켓 | 내용 및 성과 |
|---|---|---|
| Worklog(PPU) 파싱·분석 | AGILEDEV-1011 | Jira worklog를 크롤링하여 Unit별 일/주/월 단위 투입 시간, 인원수, 입력률(%), 평균 근무시간 등을 산출하는 분석 파이프라인 구축 (후속 담당자에게 이관) |
| CCR 리뷰어 부하 분석 | AGILEDEV-928, 939 | CCR 티켓의 reviewer/approval 인원 분포 분석. Trender(AHC)와 연계하여 **승인 인원 1명당 처리 CCR 건수**, 특정 인원 집중도 등 리소스 편중 지표 도출 |
| CCR 상태 체류시간 분석 | AGILEDEV-1010 | Analyzed / In Review 상태 체류시간을 조직별·Ticket Type별·Category별로 통계화. **Approval 인원당 머문 시간**을 산출해 병목 인원·구간을 식별 |

### 1.2 데이터 기반 의사결정 지원: Hexa Index 자동 분석

| 업무 | 티켓 | 내용 및 성과 |
|---|---|---|
| Hexa Index LLM 자동 분석 | AGILEDEV-866, 867, 889, 919 | Copilot CLI + MCP를 활용하여 프로젝트 점검회의용 지표를 LLM이 자동 분석·요약하도록 구성. **매월 보고 시 문제 항목을 LLM이 자동 선정**하는 체계 설계 (Active Head Count 10 미만 제외 등 운영 규칙 반영) |
| 의미있는 Index 도출 | AGILEDEV-919 | 분석 데이터로부터 개발자에게 유용한 정보를 Trender DB로 환류하는 구조 설계 |

### 1.3 운영 인프라 안정화 (리소스 데이터 수집 기반)

- 전사 크롤러 운영 관리 (AGILEDEV-471, 617): 연초 백업/재기동 등 데이터 수집 파이프라인 상시 운영.
- DB 안정성 개선 (AGILEDEV-1018): 대용량/UTF-8 처리 안정화를 위해 `mysql-connector` → `pymysql`(utf8mb4) 드라이버 교체로 배치 업데이트 실패 문제 해결.

**→ 목표 ① 부합도**: 개발자 생산성(worklog), 리뷰 리소스(CCR 리뷰어/체류시간), 자동화된 의사결정 지원(Hexa Index)까지 **생산성 지표 고도화와 데이터 기반 의사결정 지원**이라는 Action Item을 직접 수행했습니다.

---

## 2. 목표 ② Data 기반 프로젝트 관리 (가중치 40%)

> **조직 KPI**: 다각도/고차원 QCD 관련 복합지표 발굴 3개
> **Action Item**: QCD 관점 주요 지표 세분화 및 핵심 진척사항 관리 / SW 개발 효율화 활동 효과성 검증 및 개선 포인트 발굴

### 2.1 신규 발굴 QCD 복합지표 (KPI: 3개 ↔ 달성)

| # | 복합지표 | 근거 업무 | 관점 |
|---|---|---|---|
| **1** | **결함 티켓 진성/가성(TP/FP) 비율 및 결함 분류 지표** | AGILEDEV-808, 814, 803, 865 (TicketSage) | Quality — 결함밀도의 신뢰도 보정 |
| **2** | **CCR 프로세스 준수도(Shift-Left Matrix 완성도 / 워크플로우 위반)** | AGILEDEV-876~884 (CCR Gen2), 769, 784 (Screening Points) | Delivery/Process — 개발 프로세스 충실도 |
| **3** | **CCR 상태별 체류시간 · 리뷰어 부하 지표** | AGILEDEV-1010, 928, 939 | Cost/Delivery — 리뷰 리드타임·리소스 효율 |
| (+) | **RS Fidelity 점수** (Shift-Left Write RS 단계 충실도) | AGILEDEV-884 | Quality — 요구사항 리뷰 충실도 |
| (+) | **Crash 검출 지표** (프로젝트별 Crash 분포·검출률) | AGILEDEV-914, 926, 929, 1002, 1014 | Quality — 치명 결함 가시화 |

> KPI 목표(3개)를 충족하며, 추가로 RS Fidelity·Crash 등 보조 복합지표까지 확장 발굴했습니다.

### 2.2 TicketSage — 품질 데이터 기반 결함 분석 플랫폼

전사 결함 티켓을 LLM으로 요약·분류·판정하는 핵심 자산을 구축했습니다.

- **대규모 LLM Summary 적용** (AGILEDEV-989, 1008, 1023): `QCD_DL_ISSUE_FROM_MONGODB`의 약 **50만~60만 건** 티켓에 대해 3-Line Summary, Root Cause, Key Decision 등 구조화 요약을 생성. exaone 처리량 한계(동시 5세션, 60만건 추정 87일)를 분석하여 **오래된 데이터는 exaone, 최근 데이터는 gpt-4o-mini로 분리 처리**하는 하이브리드 운영안 도출.
- **필드 누락 자기치유(self-heal)** (AGILEDEV-984, 1023): LLM 응답의 필드 누락을 감지해 **누락 key만 per-key 재질의**하여 최소 호출로 보정하는 구조(`PER_KEY_RETRY`) 구현 — 비용·정확도 동시 개선.
- **진성/가성(TP/FP) 판정 및 분류** (AGILEDEV-808, 814, 803): ConnectWide 결함 티켓의 진성/가성을 자동 판정하고 근거·카테고리를 부여 → 결함밀도 KPI의 신뢰도 향상.
- **Component / error_type 자동 분류** (AGILEDEV-1013, 865): 결함을 모듈/근본원인 유형으로 분류해 향후 Wiki vectorDB·Agent 연동 기반 마련.
- **RAG 기반 Jira Test** (AGILEDEV-771, 1019, 1022): 누적 LLM_SUMMARY를 RAG로 활용하여 신규 티켓을 자동 검증. Toyota DCM(26BEV) 팀의 관리 문서를 병합(AGILEDEV-1020)하여 Feature/Module 매핑 정확도 향상.
- **COMMIT 정보 연계** (AGILEDEV-1012): 결함 티켓과 Gerrit 커밋(`QCD_DL_ISSUE_COMMIT_INFO`)을 연결해 변경 내용을 요약·연동.

### 2.3 CCR Readiness / CCR 2.0(Gen2) — 프로세스 충실도 자동 검증

- **CCR Readiness 체계** (Confluence 45, AGILEDEV-872, 917, 930, 953~957): 각 CCR 티켓의 Status 전환 시 필드(F1~F6)·Matrix 요구사항 준수를 자동 점검. 리뷰어/개발자 모두 부족 항목을 즉시 인지하도록 가이드. Baseline 적용 및 경고→Reject 단계적 운영 협의 주도.
- **CCR Gen2 (Shift-Left)** (AGILEDEV-876~884): DB 스키마 신규 설계(`QCD_CCR_GEN2_RESULT` 외 4개 테이블), Workflow 상태 전이 검증(W1~W4), Shift-Left Matrix 단계 검증(S3·S5), 필수 필드 검증(F1~F6), 위반 티켓 Jira 자동 코멘트 등록, Excel/CSV 리포트, End-to-End 통합 테스트까지 일괄 구현.
- **Screening Points** (AGILEDEV-769, 783, 784): FLU 정의 항목 기반 심사 포인트 DB 설계·구현.
- **고객 대응** (AGILEDEV-994, 1016): Integration Ticket Type 추가, 현대 ConnectWide 전체 CCR 티켓 추출 등 고객 요청 직접 처리.

### 2.4 LGEDV Crash 검출 — 효과성 검증 성과

- **검출 정확도 100% 달성** (AGILEDEV-914, 926, 929, 1002, 1014): LGEDV가 분류한 Crash 리스트를 LLM 프롬프트로 재분류, 196건 티켓에 대해 검출 가능 81.1% 확보 및 누락/중복 피드백을 반영. 고객으로부터 **"True Positive 검출 100%, 더 이상 파일 업로드 불필요"** 회신 확보 → **효율화 활동의 효과성을 고객 검증으로 입증**.

### 2.5 Agile / 프로젝트 진척 관리

- Sprint Report·Story Point 기반 리포트(AGILEDEV-852, 659, 676), Jira Dashboard 자동 업데이트(AGILEDEV-658), Agile 운영방법 설정(AGILEDEV-657) — QCD 진척사항의 정례 관리 체계 운영.

**→ 목표 ② 부합도**: QCD 복합지표 3개 이상 발굴(KPI 충족), 지표 세분화 및 핵심 진척 관리, Crash 검출 효과성의 고객 검증까지 **Action Item 전 항목을 직접 수행**했습니다.

---

## 3. 목표 ③ 역량 강화 (공통, 가중치 20%)

> **조직 KPI**: Data 및 AI 영역 역량 강화
> **Action Item**: 팀 세미나 3건 / AX Fair 참여·전사 헥커톤 심사 / 시스템·지표 설명회·사내교육 3회 이상

### 3.1 팀 세미나 (KPI: 3건 ↔ 달성)

| 일자 | 주제 | 산출물 |
|---|---|---|
| 1/21 | Chrome Extension 만들기 (YouTube Notes) | [Chrome Web Store 게시](https://chromewebstore.google.com/detail/youtube-notes/bnpcngcgngopbgdhlfaadmdppfnljmba) / GitHub 공개 |
| 3/18 | Linux에서 Copilot CLI 실습 + MCP 실습 및 Flow | [setup 문서](https://github.com/cheoljoo/mcp_copilot) — 실습 서버 활용 |
| 4/15 | FastAPI 소개 / AI Skills·Instructions 비교 및 사용법 | worklog skill 등 실사용 예제 공유 |

> 위 3건 외 추가 발표(독자 직강 등)도 진행하여 **세미나 KPI 3건을 충족**했습니다.

### 3.2 AI 분석 인프라 구축 (Data/AI 역량의 실체)

- **MCP / Copilot CLI 환경 구성** (AGILEDEV-809, 840, 866): Collab·Jira·Gerrit 접속을 내부 Copilot으로 자동화하는 MCP 환경 구성. Gerrit MCP에 source/diff 수집 기능 **오픈소스 컨트리뷰션**(AGILEDEV-827).
- **FastAPI / REST API / Fast MCP 서버** (AGILEDEV-833, 840, 843): `QCD_SAGE_LLM_QUERY` 접근용 REST API·MCP 서버 구축, 개발환경 `uv` 전환(AGILEDEV-1003).
- **EXAONE 등 다중 LLM 운용** (AGILEDEV-888, 1001): gpt-4o / gpt-4o-mini / exaone 우선순위 기반 하이브리드 모델 선택 구조로 비용·가용성 대응.

**→ 목표 ③ 부합도**: 세미나 3건 + 시스템/사용법 설명·사내 공유를 통해 **Data·AI 역량 강화 KPI 및 교육 3회 이상**을 충족했습니다.

---

## 4. 목표 외 추가 수행 업무 (Beyond Goals)

목표에 직접 명시되지 않았으나 조직 운영상 필요해 추가로 수행한 업무입니다.

- **운영 장애 대응 / 안정화**: DB UTF-8 디코딩·배치 실패(AGILEDEV-1018), DNS resolver 우회(AGILEDEV-832), crontab 로그 정리(AGILEDEV-937), 대량 delete 속도 개선(AGILEDEV-425), Qlik 데이터 동기화 이슈(AGILEDEV-787) 등 상시 운영 이슈 처리.
- **고객/타 부서 직접 지원**: 현대 ConnectWide CCR 전체 추출(AGILEDEV-1016), Toyota DCM 26BEV 멤버/문서 연동(AGILEDEV-1020), HONDA 자동 테스트 실패 티켓 대응(TIGER-54560/55998).
- **타 담당자 협업·이관**: Worklog 분석 기본 코드 작성 후 이관(AGILEDEV-1011), connectWide·RM Unit·Expert Task 협의 등 조직 간 조율.
- **성능·비용 최적화**: 티켓 병합 질의로 LLM 호출 수·비용 절감(AGILEDEV-815), 모델 폴백 구조(AGILEDEV-888).
- **개발 생산성 도구 개발**: VSCode Markdown Preview Enhanced 기능 추가(AGILEDEV-502), worklog/skills 등 사내 공유용 Agent Skill 제작.

---

## 5. 종합 및 향후 계획

### 5.1 목표 대비 종합

| 목표 | 가중치 | 핵심 KPI | 달성 현황 |
|---|---|---|---|
| ① Data 기반 리소스 관리 | 40% | 생산성 지표 3.75/5.0 고도화 | Worklog·리뷰어·체류시간 지표화 + Hexa Index 자동 의사결정 지원 구축 — **부합** |
| ② Data 기반 프로젝트 관리 | 40% | QCD 복합지표 3개 발굴 | TP/FP·프로세스 준수도·체류시간 등 **3개+ 발굴 / Crash 100% 효과성 입증** — **달성** |
| ③ 역량 강화 | 20% | 세미나 3건·교육 3회 | 세미나 3건 + MCP/FastAPI 인프라·설명회 — **달성** |

### 5.2 진행 중 / 후속 과제 (상반기 말 기준)

- **50만 건 전수 LLM Summary** (AGILEDEV-1008, 1012): 모델 처리량 제약으로 분할 진행 중 — 하반기 완료 예정.
- **DCM RAG Jira Test 고도화** (AGILEDEV-1019, 1022): gpt-5-mini 기반 RAG 검증 진행 중.
- **CCR Gen2 운영 전환**: 경고 수준 → 시스템 Reject 반영 단계로 단계적 확대 예정.

> 종합적으로, 상반기 업무는 **3대 조직 목표에 정합적으로 정렬**되어 있으며, 특히 ②Data 기반 프로젝트 관리에서 QCD 복합지표 발굴 KPI를 충족하고 Crash 검출 효과성을 고객 검증으로 입증한 점, 그리고 ①③에서 데이터 의사결정·AI 역량 인프라를 동시에 구축한 점이 핵심 성과입니다.
