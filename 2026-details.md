# 2026년 성과 근거 상세 보고서 (Detailed Evidence)

본 문서는 `2026-works-me.md`에 기술된 성과들을 검증하고 상세 내용을 파악하기 위한 근거 자료입니다. 각 항목별 관련 시스템 위치, Jira 티켓, Confluence 링크 및 기술 상세 정보를 포함합니다.

---

## 1. 전사 데이터 인프라 및 글로벌 프로젝트 적용

### [1.1] TicketSage 글로벌 프로젝트 (connectWide / Toyota) 적용
*   **근거 Jira**: `AGILEDEV-875` ([ticketsage] connectWide filter변경으로 인한 데이터 처리)
*   **상세 내용**:
    - **connectWide**: HKMC connectWide 필터 변경에 대응하기 위해 JQL 쿼리 최적화 및 DB 수집 로직(QCD_DL_ISSUE_FROM_MONGODB)을 수정하였습니다.
    - **Toyota TMCBEV**: Toyota 전용 데이터 스키마를 정의하고, TMCBEV 프로젝트의 특이 사항(보안 정책 등)을 반영한 데이터 수집 모듈을 확장 중입니다.
*   **데이터 위치**: `MOD (http://mod.lge.com/hub/cheoljoo.lee/ticketsage)` 내 `jira.jql`, `db_query.sql` 파일.

### [1.2] TicketSage 병렬 처리 아키텍처
*   **기술 상세**: 5,000건 이상의 스냅샷 데이터를 처리하기 위해 `max_runtime_hours` 옵션을 통해 강제 종료 및 재시작 로직을 구현하였습니다.
*   **구현 위치**: `ticketsage_llm_summary.py` 내 `_call_llm_per_key_prompt()` 및 `Makefile`의 batch-start/end 옵션.
*   **성과 데이터**: 2026-02-24 스냅샷 기준 20시간 연속 동작을 통해 15,984건의 유효 데이터 필터링 성공.

---

## 2. 차세대 CCR 품질 검증 및 Jira 통합

### [2.1] CCR Readiness Jira 탭(Tab) 제공
*   **근거 Confluence**: [45. CCR Readiness](http://collab.lge.com/main/display/VSPVS/45.+CCR+Readiness)
*   **상세 내용**:
    - Jira의 이슈 상세 화면에 `Readiness` 탭을 추가하여, 서버에서 실시간으로 분석한 결과를 JSON/Markdown 형태로 시각화하여 노출합니다.
    - 개발자는 자신의 티켓이 왜 `Analyzed`로 넘어가지 못하는지(예: CFR 미지정, F4 필드 누락 등)를 Jira 화면에서 즉시 확인 가능합니다.
*   **시스템 연동**: `CAnalysisVlm.py` (분석 엔진) ↔ `Jira REST API` (데이터 포스팅) ↔ `Jira UI Extension`.

### [2.2] 워크플로우 검증 로직 (W1~W4)
*   **근거 Confluence**: [COMMIT based Code Change Request Ticket](http://collab.lge.com/main/display/VSRMU/COMMIT+based+Code+Change+Request+Ticket)
*   **기술 상세**:
    - `W1 (Order)`: `CCCRStatus.py L1782` - 역방향 전이(예: Resolved → In-Progress) 탐지.
    - `W2 (Skipped)`: `CCCRStatus.py L1787` - 필수 단계 건너뜀 탐지.
    - `W3 (Author)`: `CCCRStatus.py L1792` - 권한 없는 사용자의 승인 행위 탐지.
    - `W4 (Duration)`: `CCCRStatus.py L1895` - 체류 시간 분석 (0일 즉시 전이 또는 30일 이상 방치).
*   **구현 파일**: `CCCRStatus.py`, `CAnalysisVlm.py`.

---

## 3. AI(LLM) 에이전트 및 초거대 데이터 처리

### [3.1] Sage/PVS Crawler 60만 건 요약 및 VDA 연동
*   **근거 Jira**: `AGILEDEV-1023` (Sage LLM Summary 적용)
*   **성과 지표**:
    - **60만 건**: `QCD_DL_ISSUE_FROM_MONGODB`의 전체 데이터에 대해 LLM Summary를 수행 완료하였습니다.
    - **VDA 연동**: 요약 결과를 VDA(VS Defect Agent)의 벡터 DB에 주입하여 검색 및 분석 속도를 3배 이상 향상시켰습니다.
*   **기술 가이드**: [LLM Queries](http://collab.lge.com/main/display/VSPVS/LLM+Queries) (프롬프트 튜닝 내역 기술).

### [3.2] Per-key Prompt (Self-Healing) 기술
*   **기술 상세**: LLM 답변이 JSON 형식을 벗어나거나 특정 Key(예: 'root_cause')가 누락된 경우, 해당 Key 전용 프롬프트를 사용하여 자동으로 재쿼리하는 3단계 복구 로직입니다.
*   **구현 위치**: `sage-check-llm-answer.py` 및 `run_sage_llm_summary()`.
*   **효과**: 단일 호출 대비 데이터 완결성을 약 25% 향상 (누락율 15% → 2% 미만).

---

## 4. 역량 강화 및 전사 교육 활동

### [4.1] 팀 세미나 (98. Seminar)
*   **상세 리스트**:
    - **1/21**: Chrome Extension (Youtube Notes) 배포 [WebStore 링크](https://chromewebstore.google.com/detail/youtube-notes/bnpcngcgngopbgdhlfaadmdppfnljmba).
    - **3/18**: Copilot CLI 실습 가이드 [MOD 가이드](http://mod.lge.com/hub/cheoljoo.lee/publish/-/blob/main/lge/linux-copilot-cli-setup-korean.md).
    - **4/15**: FastAPI 및 AI Skills 구조화 [MOD 기술서](https://github.com/cheoljoo/agents/blob/main/skills_and_instruct_ions.md).
    - **5/27**: 주식 알고리즘 검증 시스템 [Backtest 사이트](http://psncs.iptime.org/stock_candle/index.html).

### [4.2] 외부 기여
*   **AX Fair**: 부스 전시 및 LLM 요약 기술 시연.
*   **헥커톤 심사**: 전사 AI 헥커톤 본선 심사위원 참여 및 기술 피드백 수행.
*   **사내 교육**: 신입/전입 사원 대상 'Data 기반 QCD 관리' 강의 3회 수행.

---

## 데이터 소스 맵핑 테이블

| 성과 키워드 | 주요 소스 (URL/Path) | 관련 티켓 |
| :--- | :--- | :--- |
| **TicketSage** | mod/cheoljoo.lee/ticketsage | AGILEDEV-875 |
| **CCR Readiness** | collab/display/VSPVS/45.+CCR+Readiness | AGILEDEV-872 |
| **Sage Agent** | mod/cheoljoo.lee/ticketsage/summary | AGILEDEV-1023 |
| **MCP/CLI** | mod/cheoljoo.lee/publish/lge/linux-copilot-cli-setup-korean.md | AGILEDEV-866 |
| **W1-W4 엔진** | workspace/CCCRStatus.py | AGILEDEV-1002 |
| **Crash Report** | collab/display/VSPVS/46.+Crash+ticket... | - |
