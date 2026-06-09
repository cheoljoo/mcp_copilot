# 2026년 성과 감사 추적 전수 데이터 (Full Audit Trail)

## 1. Confluence 기술 문서 상세 내용

### [Confluence] 45. CCR Readiness
기능 추가 및 문의는 SW QCD Managemeent Unit으로 해주시기 바랍니다. (담당자 : 이철주 책임)1. CCR Readiness 작성 목적각 CCR Ticket의 Status를 변경할때  규칙에 부합하는지 Check 해 줍니다.리뷰어 관점 : 검토 해야 하는 필수 내용들이 잘 적혀있는지를 한 눈에 파악할 수 있습니다.개발자 관점 : 리뷰 요청을 올린 사항 중 무엇이 부족한지를 바로 알 수 있으며 , 이를 참조하여 부족한 부분들을 보완하면 됩니다.2. BasementSystem SW Expert Task에서 Release 되는 CCR의  에 있는 프로세스 기반으로 구현 하였습니다.2.1 Status 전환 흐름Open (초기정보 입력)  ↓    [F1~F3, F6 입력 + Matrix 비어있음]Analyzed (영향도 분석)  ↓    [F4 입력 + 요구사항 분석: O/URL]In-Progress (개발 진행)  ↓    [요구사항 분석: O/URL/O(CFR승인)]In Review (코드리뷰)  ↓    [F5 Gerrit + Matrix 3행 2~3열 완성]Build Request (빌드요청)  ↓    [Matrix 3행 × 3열 완전히 완성]Resolved (반영완료)  ↓    [Resolution 입력]Closed (종료)필드 위반 (Field Violations)F1 (Ticket Type)F2 (Unit Leader)F3 (Feature Leader)F4 (Change Scope &amp; Difficulty)F5 (Gerrit Link)F6 (Applied Project)Matrix 위반 (Matrix Violations)Open 상태에서 Matrix 값 입력Status별 필드 미입력체크리스트 예시⚠️ 중요: 각 체크리스트는 해당 status까지의 모든 이전 요구사항을 포함합니다.2.2 각 Status별 Check ListsOpen → Analyzed 전환 체크리스트Open 요구사항 [ ] F1 : Ticket Type (CR/Issue/SV/Integration등) 입력 : None 이외의 값 선택[ ] F2 : Unit Leader 지정[ ] F3 : Feature Leader 지정[ ] F6 : Applied Project 지정[ ] Matrix 모든 행이 비어있음Analyzed → In-Progress 전환 체크리스트Open 요구사항 (계속 검증됨)[ ] Ticket Type, Unit Leader, Feature Leader, Applied Project 입력Analyzed 요구사항[ ] F4 : Change Scope 입력[ ] F4 : Change Difficulty 입력[ ] F_CFR : CFR(Chief Function Reviewer) 필드 지정[ ] Matrix : 요구사항 분석 - 수행여부: O[ ] Matrix : 요구사항 분석 - 근거Link: URL 입력[ ] Matrix : 요구사항 분석 - 승인: O (CFR 승인 필수)In Review → Build Request 전환 체크리스트Open~In-Progress 요구사항 (계속 검증됨)[ ] 모든 이전 필드 및 Matrix 요구사항 완료In Review 요구사항[ ] F5 : Gerrit Link 입력 (1개 이상)[ ] Matrix : 요구사항 분석: O / URL / O[ ] Matrix : 설계 리뷰: O / URL / O[ ] Matrix : 자가 검증: O / URL / (빈칸)Build Request → Resolved 전환 체크리스트Open~In Review 요구사항 (계속 검증됨)[ ] 모든 이전 필드 및 Matrix 요구사항 완료Build Request 요구사항[ ] Matrix 3행 × 3열 완벽하게 완성[ ] 모든 위반사항 0개3. Jira Posting Format 예제 및 대응 방법3.1 Jira Posting FormatCCR-32249 에 대한 Readiness 분석 결과trueFinal FormatCCR 분석에 대한 설명 페이지 : http://collab.lge.com/mai...

---

### [Confluence] COMMIT based Code Change Request Ticket
http://collab.lge.com/main/download/attachments/465479490/userstyle.css?api=v2CW preCCR한국어Shift-left소프트웨어 개발 프로세스의 초기(왼쪽) 단계로 품질, 보안, 성능 및 성능 검증을 전환하여 문제를 더 빨리 감지하고 해결하는 접근 방식전통적인 검증(테스트, 보안 검토 등)을 Release 직전이 아닌 설계·개발 단계부터 적용하는 것을 의미목적버그·취약점·설계결함을 조기에 발견 → 수정 비용과 시간 절감신속한 피드백 → 개발 주기와 SW 배포 주기를 단축품질과 안정성을 초기에 확보 → Release risk 저하CCR코드 변경 요청 프로세스의 변경 단위는 커밋(또는 집합)이며, CCR은 커밋·이슈·설계·검증 결과를 포함하여 리뷰 및 승인배경기존 개발 프로세스에서 설계·설계 검토·구현·검증 단계의 산출물의 명시적 관리 미흡변경점 추적 및 프로세스 수행 여부 확인이 어려웠던 점을 보완하기 위해 CCR을 도입각 단계의 산출물을 관리하고, 적절한 승인자의 승인하에 다음 단계로 진행할 수 있도록 프로세스를 강화적용 범위적용 브랜치: Project 별로 상이하나 기본적으로 Main MP branch적용 기간: 개발 중 발생하는 모든 변경 내용적용 대상: 해당 프로젝트에 반영 되는 모든 소스 코드 및 개발자모든 변경점이 대상이며, 변경점 발생 시 CCR Ticket을 생성 (http://jira.lge.com/issue/projects/CCR/)프로젝트 확대 적용 일정 필독 사항Chief Function Review를 반드시 Assign 필요CFR Assign을 하지 않으면 Review 진행이 안됨 CFR List 참고 : CFR 분들은 Unit 내 개발자, FO분들에게(국내, 해외) 사전에 공지 필요 프로세스 개요CCR 활동은 기본적으로 각 개발 Unit 내부에서 완결되어야 하는 활동이다.SW의 모든 변경점은 티켓으로 등록/관리되며, 모든 코드 변경은 CCR Ticket이 없으면 병합될 수 없다.「SW 변경 위원회」를 거쳐 변경여부를 필요로 하는 경우에 한하여 Unit Leader / Chief Function Reviewer 가 승인한다.CCR Ticket에서 「설계 → 설계리뷰 → 구현 → 자가검증 → 코드리뷰」 등의 코드변경과 관련된 모든 활동을 점검한다.        세부 업무 절차Create생성 주체: Assignee (FO 또는 개발자)생성 조건CR: OEM으로부터 CR을 요청받아 CR 적용 여부를 시작할 때CR과 무관하지만 코드 변경이 필요한 경우자체 개선 항목OEM 이슈FIT 버그DQA 버그이외 commit이 필요한 모든 사항 (단, baseline을 위한 manifest 관련 commit은 제외; CI unit에서 작성)생성 절차Project : VS Code Change Request (CCR) Issue Type : &quot;Task&quot;로 지정CCR title: [Change Type][Project] SummaryChange Type[CR]: Change Request[Issue]: OEM 이슈, QE 버그, DQA 버그[Integration]: Code sync[SV]: 자체 개선 항목, 이외 commit이 필요한 모든 사항(ex: unit test, static analysis)Project : [ConnectWide]Component : 본인의 소속 부서 입력인도/베트남의 경우, HQ 담당하는 부서 입력Assignee : FO (일반적으로, 생성주체가 FO이므로 assign to me)Unit Leader : 소속 Unit leader입력, 인도/ 베트남의 경우, HQ 담당 Unit LeaderChief function Reviewer: 소속 Unit에 배정된 CFR 입력(Option) Expert Group: 7대 주요 항목 해당 시, CFR이 작성Priority : issue(OEM/QE/DQA)에 의한 변경 시, 변경원인이 된 issue 티켓의priority와 동일하게 입력Ticket Type :CR : OE...

---

### [Confluence] 46. Crash ticket Identification from LGDV
git repository : http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/tree/main/crash?ref_type=headshttp://lotto645.lge.com:8088/cheoljoo.lee/code/ticketsage/crash/동일 내용 markdown : http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/crash/report.md?ref_type=headsLGEDV Excel PVS Crawler Report기준 파일: LGEDV_2025_Crash Issue List_20251231.xlsx작성일: 2026-03-23통계 출처: match_issue_url.log 말미 통계와 동일한 값(워크스페이스에는 log 파일 미존재, crash/README.md 실행결과 블록과 일치)실행 파일 : match_issue_url.py1) 전체 196개 Ticket의 위치(상태) 분포구분 (IsConnect)건수비율의미DB Matched8543.4%DB ISSUE_URL 매칭 성공Unmatched: Connectable7437.8%DB 미매칭이나 URL 접속 가능Unmatched: HTTP_ERROR_STATUS3718.9%HTTP 4xx/5xx 응답합계건수비율Crawl 가능 (DB Matched + Connectable)15981.1%Crawl 불가 (HTTP_ERROR_STATUS)3718.9%Total196100.0%2) Crawl 가능 Ticket의 Project 분포 (상위)순위Project건수1TOYOTA 24DCM222BMW ICON203RENAULT AIVI2184BMW WAVE165NISSAN CDC126HKMC Connect Wide87TOYOTA 26BEV78GM Gen1279HONDA MY26510Porsche E3PA511Porsche J1PA412RENAULT ACCESS DA413RENAULT CDC414VW FPK Gen2 MY25315NISSAN AIVI2316JLR TCUA317HKMC ccIC318HONDA MY23319Porsche E3G3220GM CHM23) HTTP_ERROR_STATUS Ticket Link 정렬 목록 (37건)NoDepartmentTeamProjectTicket LinkIsConnect1VSD2MULTIMEDIANISSAN AIVI2C2LST-9109Unmatched: HTTP_ERROR_STATUS2VSD2MULTIMEDIARENAULT AIVI2CCSEXT-202723Unmatched: HTTP_ERROR_STATUS3VSD2FUNCTION TECHNOLOGY 2RENAULT AIVI2CCSEXT-217900Unmatched: HTTP_ERROR_STATUS4VSD2MULTIMEDIANISSAN CDCCDCFM-10326Unmatched: HTTP_ERROR_STATUS5VSD2MULTIMEDIANISSAN CDCCDCFM-12127Unmatched: HTTP_ERROR_STATUS6VSD2MULTIMEDIANISSAN CDCCDCFM-14239Unmatched: HTTP_ERROR_STATUS7VSD2CYBER SECURITYRENAULT AIVI2dl_oem&amp;clm_CCSEXT-213916Unmatched: HTTP_ERROR_STATUS8VSD2CYBER SECURITYRENAULT AIVI2dl_oem&amp;clm_CCSEXT-215085Unmatched: HTTP_ERROR_STATUS9VSD1PHONE PROJECTIONHKMC ccICDCM-4976Unmatched: HTTP_ERROR_STATUS10VSD1CLUSTERHKMC Connect WideHKMCCLUHUD-23305Unmatched: HTTP_ERROR_STATUS11VSD1PHONE PROJECTIONVW ICAS3CN MP2022ICASMPCHN-719Unmatched: HTTP_ERROR_STATUS12VSD1CONNECTIVITY FRAMEWORKBMW IC...

---

### [Confluence] 98. Seminar
해당 세미나는 매주 Scrum 시간 이후에 진행합니다. 이외 시간 진행 시 시간을 적어주세요.Collab 문서를 사용하지 않을 경우 세미나 파일은 파일명에 일자를 적은 후 아래의 자료 폴더에 넣어주세요. 예) 20250919-생성형AI.pptx자료 폴더: Seminar (OneDrive)26년 세미나 목표는 1년에 2번 세미나를 준비해주셨으면 합니다. (의무 사항은 아니며 ,  뭔가 공유하고 싶은 내용들이 있으시면 아무 내용이나 같이 공유하면 좋을 듯 합니다.)세미나 일정파트 세미나true세미나 2026false,false,false날짜시간Sparkline이름Filtration paneltruePoint (.)이름‚주제‚날짜시간true,,-&gt;true150,150주제yy-mm-dd1766706146554_-2128439573365|5|8|y w d h m|y w d h mAND0,1,2완료여부이름주제날짜시간발표시간발표자료기타

10
complete
 

이철주chrome extension 만들기 (youtube에 자신의 분류와 의견을 남기자)1/2120분published chrome extension link for youtube notes : https://chromewebstore.google.com/detail/youtube-notes/bnpcngcgngopbgdhlfaadmdppfnljmbagit repository : https://github.com/cheoljoo/youtube_notes_chrome_extension

11
complete
 

이기영VSCode DefectAgent expansion 및 자체 RAG서버 개발1/2830

12
complete
 

이정미MCP 도구를 통해 Jira, confluence, AI chat 으로 활용하는 사례공유2/415분이용사례 1. NEXT JIRA42905e30-a731-3aef-b7b0-a61a07f1651aAGILEDEV-8102. 3. 환경설정파일 공유

13
complete
 

오지은Flutter로 앱 만들기3/430분Hello World!

14
complete
 

이철주linux에서 copilot cli 실습 + MCP 실습 및 flow3/1845분https://github.com/cheoljoo/mcp_copilot/blob/main/docs/linux-copilot-cli-setup-korean.md10.231.76.112  (현재 SW QCD Unit의 DB backup server) 서버 사용하여 실습vscode copilot과 token이 별도로 계산되는 듯!긴 것을 걸어두고 다른 것을 하고 싶을때~여러개를 동시에 돌려두고 싶을때MCP 사용 : 

15
complete
 

이철주fastapi 소개AI skills / instructions 비교 및 사용법4/1530분fastapi 소개 (restapi 툴) : ex) http://tiger02.lge.com:8002/docsskills와 instructions의 비교 및 사용법 : https://github.com/cheoljoo/agents/blob/main/skills_and_instruct_ions.mdworklog skill : 오늘 한 일 정리 및 commit msg 생성- https://github.com/cheoljoo/agents/blob/main/.github/skills/worklog-manager/SKILL.md예) /instructions  , /skills list

16
incomplete
 

이철주독자 직강 : 캔들챠트 하나로 끝내는 추세추종 투자구현 내용 설명5/2745분캔들챠트 하나로 끝내는 추세추종 투자 에 대한 요약 및 backtest 결과http://psncs.iptime.org/stock_candle/index.html

17
complete
 

김기만Langraph기반 HexaChat구현 소개 5/2010분PVS Crawler API - Swagger UI구현 과정 설명:1.MS365 Copilot에서 설명한 방식으로 개발방향 잡음...

---

## 2. Jira 티켓 및 코멘트 전수 내역

### [TIGER-55998] [TRDK][HONDA 25.5][app-service]Auto report failed test cases to VLM ticket(Unique ID: abedd17bcc)
- **상태**: Open | **최종 업데이트**: 2026-05-27T11:49:28.000+0900
- **티켓 본문**: Tiger Autotest runs all available testcases on a daily basis.Test environment:Target board - JapanThe following testcase(s) failed in today test:auto_test_app-service.csv:5:TestCase#SWIT: sldd am broadcast_post test_action /res: Fail fail_n:1 fail_type:0x10Please take a look at it!Below are some helpful documents for troubleshooting.Logs file:Daily log: http://tiger.lge.com/DailyTest/honda_tsu_25.5my_release/2026-05-09/TA_TRDK_test/TRDK_test.out_log.txtTigris Log file: http://tiger.lge.com/DailyTest/honda_tsu_25.5my_release/2026-05-09/TA_TRDK_test/tgr_logTAF Guide: How to interpret Testcase Error MessageWhy testcases test is importantevaluate system under certain circumtanceallow developers and testers to discover errors that may occurs during executionensure your application can run prope...

---

### [TIGER-54560] [TRDK][HONDA 25.5][app-service]Auto report failed test cases to VLM ticket(Unique ID: abedd17bcc)
- **상태**: Resolved | **최종 업데이트**: 2026-04-23T14:43:06.000+0900
- **티켓 본문**: Tiger Autotest runs all available testcases on a daily basis.Test environment:Target board - JapanThe following testcase(s) failed in today test:auto_test_app-service.csv:5:TestCase#SWIT: sldd am broadcast_post test_action /res: Fail fail_n:1 fail_type:0x10Please take a look at it!Below are some helpful documents for troubleshooting.Logs file:Daily log: http://tiger.lge.com/DailyTest/honda_tsu_25.5my_release/2025-12-17/TA_TRDK_test/TRDK_test.out_log.txtTigris Log file: http://tiger.lge.com/DailyTest/honda_tsu_25.5my_release/2025-12-17/TA_TRDK_test/tgr_logTAF Guide: How to interpret Testcase Error MessageWhy testcases test is importantevaluate system under certain circumtanceallow developers and testers to discover errors that may occurs during executionensure your application can run prope...
- **작업 히스토리 (User Comments)**:
  - [2026-04-23T14:43:06.000+0900] moved to other department

---

### [AGILEDEV-1023] [pvs_crawler][sage]  누락 field만 다시 생성하여 합성 < 50만개의 모든 ticket에서 LLM SUMMARY 적용 - QCD_DL_ISSUE_FROM_MONGODB의 모든 ticket에 대해서 LLM summary 개발
- **상태**: Resolved | **최종 업데이트**: 2026-06-01T11:05:58.000+0900
- **티켓 본문**: 누락 필드만 다시 query하여 생성

누락 필드를 위한 prompt를 다시 생성할수 있도록 코드를 만들어야 한다. 

누락된 필드만 다시 물어봐서  얻은 답을 insert (udpate)하는 방식을 취한다.
- **작업 히스토리 (User Comments)**:
  - [2026-06-01T10:44:40.000+0900] c1347e4 (2026-05-16) 커밋입니다.
[AGILEDEV-1008][service중 아님] Add SAGE LLM checker, regenerate pipeline, and --from-oldest mode

이 커밋에서 누락 키에 대해 각각의 Prompt로 개별 query하는 기능이 처음 도입되었습니다:

missing_keys_by_issue_model: 누락된 top-level key를 모델별로 묶어 system prompt에 주입
_build_missing_keys_instruction() 신규 함수 추가
sage-check-llm-answer.py 신규: 누락 key 감지 → 모델 조합별 issue 묶음 → run_sage_llm_summary() 호출로 최소 LLM 호출 구조
이후 4c49738 (2026-05-31)에서 per-key retry 개선이 추가되었습니다 (_call_llm_per_key_prompt, PER_KEY_RETRY DB ...
  - [2026-06-01T10:49:14.000+0900] h2. 2.14. per-key prompt 기능 도입 이력 및 Prerequisite (v2026-06-01)
h3. 2.14.1. 기능 도입 커밋 이력

누락 key 각각에 대해 개별 Prompt로 LLM을 호출하는 기능은 두 커밋에 걸쳐 도입·개선되었다.
||커밋||날짜||내용||
|{{c1347e4}}|2026-05-16|*최초 도입* — {{missing_keys_by_issue_model}} 필드로 누락 key를 모델별로 수집하고 {{{}_build_missing_keys_instruction(){}}}을 통해 메인 prompt system message에 주입. {{sage-check-llm-answer.py}} 신규 추가(구조 검사 + regenerate orchestrator). 모델 조합별 issue 묶음 호출로 최소 LLM 호출 전략 도입.|
|{{4c49738}}|2026-05-31|*per-key 개별 호출 추가* — {{_call_llm_per_k...
  - [2026-06-01T11:05:58.000+0900] log에서는 PER_KEY_RETRY 로 찾으면 동작한 것을 볼수 있습니다. 

prompt가 잘 만들어지면 거의 볼수 없음.

---

### [AGILEDEV-1022] [ticketsage] DCM  : (RAG) gpt-5-mini 및 QCD_DL_ISSUE_ADDITIONAL_INFO 을 이용한 jira test 만들기
- **상태**: In Progress | **최종 업데이트**: 2026-05-29T16:48:54.000+0900
- **티켓 본문**: QCD_DL_ISSUE_ADDITIONAL_INFO 의 LLM_SUMAMRY를 이용하여 ,  Jira test를 수행한다. 

코드 시작 부분에서는 JIRA_TEST DB에 있는 것에 대해서 closed되어 내용을 확인할 수 있는 것에 대해서 최종 결과를 확인하는 기능을 추가해야 한다. (기존에 만들어진 것을 확인 및 수정)
- **작업 히스토리 (User Comments)**:
  - [2026-05-28T16:34:12.000+0900] project = TMCBEV AND status in ('Closed','Resolved') AND cf[25328] = DQA AND type = bug ORDER BY priority DESC, updated DESC

이것을 하니 454개 정도가 나옵니다. 

 

그러므로 jira test를 할때는 , 

project = TMCBEV AND status not in ('Closed','Resolved') AND cf[25328] = DQA AND type = bug AND updated >= -2d ORDER BY priority DESC, updated DESC

으로 하니 지금은 27개 정도 나오네요. HOLDING, INQURE TO REPORTER 는 제외해는게 좋을 듯도 하고....

 

결국 , project = TMCBEV AND status in ('REOPENED','NEW','IN PROGRESS') AND cf[25328] =...
  - [2026-05-29T16:48:54.000+0900] 정리 : http://collab.lge.com/main/spaces/VSPVS/pages/3691259355/50.+TMCBEV%EC%9D%98+sage+%EC%9E%91%EC%97%85+flow+%EC%9A%94%EC%95%BD+starting+points

RAG까지 처리한 값이 QCD_SAGE_TMCBEV_LLM_RAG_JIRA_TEST에 쌓임
RAG  수행시 toyota 팀에서 제공한 management 문서를 병합함.


{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
{noformat}

branch : 260526/tmcbev


{noformat}
$  git log -1
commit 037a98c26...

---

### [AGILEDEV-1020] [ticketsage] DCM : toyota 팀에서 받은 문서와 병합 (prompt 또는 프로그래밍)
- **상태**: In Progress | **최종 업데이트**: 2026-05-29T16:54:40.000+0900
- **티켓 본문**: toyota 팀에서 받은 관리용 문서를 같이 합쳐야 합니다.
- **작업 히스토리 (User Comments)**:
  - [2026-05-27T14:39:58.000+0900] Toyota 26BEV DCM SW PL 전성염 책임입니다.

 
개발자 명단과 FO 명단 공유 드립니다.
26BEV_MemberList_250527_v0.4_Reviewed_v02.xlsx 가 개발자들이 유닛내 개발자 변경시 Shared point상의 파일에 업데이트 하는 자료이고,
csv로 전달드린 건 취합된 excel에서 지난 4월에 조금 프로그래밍 적용하기 쉽게 수정한 파일입니다.
  - [2026-05-28T09:38:43.000+0900] $  git branch

* 260526/tmcbev

$  git remote -v origin  
http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch) origin  
http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
  - [2026-05-28T16:37:50.000+0900] db_test/tmcbev_member_role.py will make new csv 

[^26BEV_MemberList_new_normalized.csv]  ->  [^tmcbev_member_role.csv]

^ticket을 읽어서 어떤 feature,module인지 알기 위해서는 LLM에 문의를 하거나 keyword matching을 한다.^
  - [2026-05-29T16:54:40.000+0900] 생성된   tmcbev_member_role.csv 내용을 읽어서 RAG 과정에서 prompt에 같이 넣어서 LLM 문의 값을 얻음. 이를 기반으로 mapping 값 도출

prompt에 삽입한 내용:
1. {feature_module_section}    위의 파일 내용
2. 4. **Feature/Module Match**: From the Feature/Module Reference List above, select the TOP 2 entries that best match the current ticket content. The first entry should be the closest match. For each selected entry, provide a reason explaining why it matches the current ticket content. If no entry matches, return an empty list.
3. 
{code:...

---

### [AGILEDEV-1019] [ticketsage] DCM  : (RAG) 사용DB를 QCD_DL_ISSUE_ADDITIONAL_INFO 안의 LLM_SUMMARY의 내용을 활용
- **상태**: Resolved | **최종 업데이트**: 2026-05-28T14:37:16.000+0900
- **티켓 본문**: vector는 기존과 같이 사용

QCD_DL_ISSUE_ADDITIONAL_INFO의 LLM_SUMAMRY안의 model : gpt-4o-mini 와 exaone 에 대해 RAG로 만들어진 것을 활용하여 , test_gpt_model만 gpt-4o-mini 와 exaone으로 돌려서 시험을 해본다. (위의 모든 사항은 RAG관련)
이유 : 모든 내용에 대해서 이것을 쌓아두고 있으므로 , 앞으로 QCD_DL_ISSUE_ADDITIONAL_INFO의 LLM_SUMAMRY 을 계속 사용할수 있을가하는 취지로 시험을 해두어야함.
- **작업 히스토리 (User Comments)**:
  - [2026-05-28T09:38:21.000+0900] {noformat}
$  git branch * 260526/tmcbev

$  git remote -v origin  
http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch) origin  
http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push){noformat}
  - [2026-05-28T14:06:28.000+0900] mode = adddb 가 매일 쌓이는 기본적인 QCD_DL_ISSIE_ADDITIONAL_INFO를 사용한 시험 내용이다.

http://tiger02.lge.com/cheoljoo.lee/code/dcm/db_test/compare_sage_html.html
h1. 📊 sage_*.html 비교 리포트

생성일시: 2026-05-28 09:52:31

ⓘ Mode 설명
||Mode||플래그||읽는 DB||저장 DB||설명||
|*base*|(없음)|{{QCD_SAGE_TMCBEV_LLM_QUERY}}
{{QCD_SAGE_TMCBEV_LLM_RAG_QUERY}}
{{QCD_SAGE_TMCBEV_LLM_RAG_VECTOR}}|{{QCD_SAGE_TMCBEV_LLM_RAG_DB_TEST}}|기본 모드 — 추가 플래그 없이 전체 이슈 대상 테스트|
|*known_only*|{{--known-only}}|{{QCD_SAGE_TMCBEV_LLM_QUERY}}
{{QC...

---

### [AGILEDEV-1018] DB update 에러 (3byte UTF 한글)
- **상태**: Resolved | **최종 업데이트**: 2026-06-02T10:43:50.000+0900
- **티켓 본문**: [INFO] QCD_CCR_READINESS ISSUE_ID=CCR-35861: changed=context+status_context+jira_detail (jira_detail_changed=critical_point+detail_text) -> will UPDATE
  [CONTEXT][CCR-34551] CHANGED fields: ['Change Difficulty', 'Change Function_VLM', 'Change Scope', 'Impact Level_VLM', 'status', 'status_history']
  [STATUS_CONTEXT][CCR-34551] CHANGED fields: ['avReview', 'current_status_check_description', 'current_status_check_result', 'current_status_check_violations', 'current_status_screening_point', 'current_status_screening_point_critical', 'current_status_workflow_validation_result']
[INFO] QCD_CCR_READINESS ISSUE_ID=CCR-34551: changed=context+status_context+jira_detail (jira_detail_changed=critical_point+detail_text) -> will UPDATE
    [CCR-34337] Gerrit link changed (db=1 urls, cur=2 urls) →...
- **작업 히스토리 (User Comments)**:
  - [2026-05-22T09:28:22.000+0900] {noformat}
$  git log -1
commit a0148fd6e1b0669b91c4a69e431021b9533a392b (HEAD -> main, origin/main, origin/HEAD)
Merge: 675a422 b89d02a
Author: charles.lee 
Date:   Fri May 22 09:27:09 2026 +0900

    [AGILEDEV-1018] make crontab 실행 중 발생한 utf-8 디코딩 에러 및 배치 업데이트 실패 문제를 해결하였습니다.
    
      주요 수정 사항
    
       1. 데이터베이스 드라이버 교체 (CDataBase.py):
           * 기존 mysql-connector-python 드라이버에서 대용량 데이터 및 UTF-8 처리에 더 안정적인 pymysql 드라이버로 교체하였습니다.
           * 연결 문자열에 charset=utf8mb4 설정을 추가하여 ...

---

### [AGILEDEV-1016] 현대 conectwide CCR 날짜 관계 없이 전체 티켓 엑셀 자료 요청 
- **상태**: Resolved | **최종 업데이트**: 2026-05-20T14:31:11.000+0900
- **티켓 본문**: CCR  티켓 수집 요청 

현대 CCR 전체 티켓 수집 요청 

예시는 아래의 엑셀에서 확인 가능
- **작업 히스토리 (User Comments)**:
  - [2026-05-20T14:31:11.000+0900] 결과 파일을 첨부하였습니다.


{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)
{noformat}

 
{noformat}
$  git log -1
commit b89d02a01fd260a9ebc68671215b9ae4e71ca745 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed May 20 14:29:34 2026 +0900

    전체 범위에 대한 target(머문시간) 요청에 대응
{noformat}

---

### [AGILEDEV-1014] [ticketsage][crash] LGEDV 5월 feedback에 대한 추가 처리
- **상태**: Resolved | **최종 업데이트**: 2026-05-22T12:22:20.000+0900
- **티켓 본문**: After reviewing the extracted data that you shared, it shows a great improvement of true positive detection. Thank you very much for your efforts.
As the correct detection is 100%, I don't upload the file anymore.
 
In comparison with human manual monitoring, we found that there are 2 points that need to improve further.
1. Duplicate ticket based on url
__
|dl_oem&clm_TMCDCMTF-36788|+http://jira.lge.com/issue/browse/TMCDCMTF-36788+|
|vlm=TMCDCMTF-36788|+http://jira.lge.com/issue/browse/TMCDCMTF-36788+|
This ticket was recorded 2 times. And I assume that the problem might come from a different Issue_ID. As it is one ticket, it is expected to show one record only.
 
2. Missing crash defects * 
http://jira.lge.com/issue/browse/WAVE-82888
 * 
http://jira.lge.com/issue/browse/PFIF...
- **작업 히스토리 (User Comments)**:
  - [2026-05-18T14:12:55.000+0900] [~hakchoong.kim] 님 요청 내용

nam 의 회신 메일중에 왜 없냐고 물어본 리스트에 마지막 이슈는 우리 DB에 있는데 왜 빠진건지 알아봐주세용~!

[*http://vscb.lge.com:8080/cb/issue/37428680*]

 

*답변 :*

주신 내용은 PGZ25PGZMGJ00  은 아래의 project_code에 들어가 있지 않아서 crash 조사를 하는 대상이 안되었기 때문입니다.

 

이유는 무르겠지만, 당시에는 project code 로 filter를 만들었었습니다.

============================================================
Unique PROJECT_CODEs (27 total):
============================================================
PGZ17PGZ00T00
PGZ19PGZRNP00
PGZ19PGZRO6...
  - [2026-05-22T11:08:27.000+0900] http://jira.lge.com/issue/browse/AGILEDEV-854  에서 마무리 될 것이고 , 
관련 정보도 이 ticket에 추가하겠습니다.  
--> http://jira.lge.com/issue/browse/AGILEDEV-854  에서 Comment ::   이철주 cheoljoo.lee added a comment - 2026/05/22 12:19

---

### [AGILEDEV-1013] LLM Summary에 Component 및 error_type 추가 
- **상태**: Open | **최종 업데이트**: 2026-05-20T15:13:17.000+0900
- **티켓 본문**: 철주C님,

LLM_Summary 생성 시, component와 error_type도 json 생성 결과에 추가 반영하면 좋을 것 같습니다. (향후 wiki vectorDB index와 agent 및 skill 연동 확대 처리를 위함)

아래는 component와 error_type을 위한 제안 프롬프트입니다.

[SYSTEM]
당신은 자동차 SW 개발 프로젝트의 Defect Ticket 분류 전문가입니다.
아래 Ticket 분석 내용을 보고, 이 Ticket이 속하는
component과 error_type을 자유롭게 판단하여 제안하세요.

 

규칙:
- component: 이슈가 발생한 SW/HW 모듈 또는 기능 영역
  (예: BT, WiFi, HMI, ADAS, Audio, OTA, Navigation, IVC 등)
- error_type: 이슈의 근본 문제 유형
  (예: 연결오류, 크래시, 환경설정오류, 성능저하, UI오류, 라이센스오류 등)
- 반드시 아래 JSON 형식으로만 답하세요.
- 목록에 없는 새로운 값도 자유롭게 제안 가능합니다.

 

출력 형식:
{
  "component": "단일 값",
  "error_type": "단일 값",
  "confidence": 0.0 ~ 1.0,
  "reason": "한 줄 근거"
}

 

[USER]
## Ticket 요약
{LLM_WITHIN_500_TOKEN}

 

## 근본 원인
{Root_Cause}

 

## 문제 분류
{True_False_Positi...
- **작업 히스토리 (User Comments)**:
  - [2026-05-15T21:32:23.000+0900] [~just.lee]  책임님,

!image-2026-05-15-21-31-51-033.png!

사진과 같이 Preformatted 이용하여 다시 작성해주세요.

원문 글자가 깨지니 가져다 사용할 수가 없습니다.
  - [2026-05-18T11:04:05.000+0900] {noformat}
이렇게 나와야 합니다. 
{noformat}



\{noformat\}  들 사이에 입력합니다.
  - [2026-05-20T13:39:15.000+0900] [~just.lee]   님 ,  다음과 같이 반영에정입니다.
{noformat}
"MODULE_FUNCTION": {{
    "component_group": "The SW/HW module or functional area where the issue occurred. Suggest a concise, consistent label in English. (Common examples: BT, WiFi, HMI, ADAS, Audio, OTA, Navigation,IVC, Display, Boot, Camera, Power, Memory, Other).   파일 하단 [MODULE_FUNCTION 규칙] 참조",
    "error_type": "The root cause category of the issue. Suggest a concise, consistent label in English. (Common examples: ConnectionError, Crash, ...
  - [2026-05-20T15:13:17.000+0900] !screenshot-1.png! 
그림과 같이 생성됨. 확인하였습니다.
내일부터 동작할 것이고 , SNAPDATE로 2026-05-20 부터 적용될 것 입니다.   21일날 20일 것을 동작시킵니다.

---

### [AGILEDEV-1012] [pvs_crawler][sage] LLM SUMMARY 에 COMMIT 내용 요약 추가
- **상태**: In Progress | **최종 업데이트**: 2026-06-01T17:26:02.000+0900
- **티켓 본문**: {color:#aaaaaa}SELECT{color} * {color:#739eca}FROM{color} {color:#b788d3}QCD_DL_ISSUE_COMMIT_INFO{color} {color:#b788d3}qdici{color}

에 있는 커밋정보를 LLM_SUMMARY 에 같이 포함시키는 방안이요. 그냥 제가 상상한거라서 가능할지 검토가 되면 좋을것 같아요.
 # 이슈에 있는 COMMIT_ISSUE_ID 와 로 커밋을 찾아 이슈 연관 커밋임을 표시 (제목/URL)   : QCD_DL_ISSUE_FROM_MONGODB.COMMIT_ISSUE_ID -> QCD_DL_ISSUE_COMMIT_INFO.COMMIT_ISSUE_ID을 찾는다. 
 # 커멘트에 Commit link 가 있는 경우에는 1과 함께 표시 (제목/URL) : comments에서 나오는 [http://vgit.. 이면     QCD_DL_ISSUE_COMMIT_INFO 에 없으면 ISSUE_ID,COMMIT_ISSUE_ID 으로 추가|http://vgit/]
 # 혹시 URL 을 가지고 수정 전/후 를 가져와서 대략적으로 요약해서 (제목/URL/SUMMARY) 로 저장할수 있을지 확인. : [QCD_DL_ISSUE_COMMIT_INFO|http://vgit/] 에 field를 만들어 무슨 내용을 변경했는지를 요약해서 추가   : 내부적으로 COMMIT_URL로 최신의 SNAPDATE 기준으로 dict를 만들고 있으면, 중복되지 않게 query 가능
- **작업 히스토리 (User Comments)**:
  - [2026-05-14T14:11:41.000+0900] exaone 으로 전 data를 update 하기로 결정함.
  - [2026-05-14T14:11:42.000+0900] * LLM 결과가 제대로 값들을 포함하는지 checkgk하였는데 , Field들을 누락한 경우 발생  (공통 사항 : 첫번째 항목은 누락 안시키네요. 중요한 Three-Line_Summary와 Three-Line_Summary_In_English을 제일 앞에 두게 변경해야 할 것임)

 * 
 ** [[prompt_file] sage_llm_summary.v0.006.prompt|https://llm-api.lge-vs.com/]
 ** [[exaone] OK=562, NG=46 / 608건 (7.6%) ◀ NG 있음|https://llm-api.lge-vs.com/]
 *** (41건) 누락: ['Discussion_Flow', 'Key_Decisions', 'Key_Technical_Keywords', 'Meaningful_Sentence_Extraction', 'Opinion_Exchange', 'RAG', 'Resolution_Owner', 'Root_Cause_An...
  - [2026-05-14T14:11:44.000+0900] {color:#aaaaaa}SELECT{color} * {color:#739eca}FROM{color} {color:#b788d3}QCD_DL_ISSUE_COMMIT_INFO{color} {color:#b788d3}qdici{color}

에 있는 커밋정보를 LLM_SUMMARY 에 같이 포함시키는 방안이요. 그냥 제가 상상한거라서 가능할지 검토가 되면 좋을것 같아요.
 # 이슈에 있는 COMMIT_ISSUE_ID 와 로 커밋을 찾아 이슈 연관 커밋임을 표시 (제목/URL)   : QCD_DL_ISSUE_FROM_MONGODB.COMMIT_ISSUE_ID -> QCD_DL_ISSUE_COMMIT_INFO.COMMIT_ISSUE_ID을 찾는다. 
 # 커멘트에 Commit link 가 있는 경우에는 1과 함께 표시 (제목/URL) : comments에서 나오는 [http://vgit.. 이면     QCD_DL_ISSUE_COMMIT_INFO 에 없으면 ISSUE_ID,COMM...
  - [2026-05-14T14:42:09.000+0900] QCD_DL_ISSUE_ADDITIONAL_INFO에 LLM_SUMMARY에 "commit" 관련 내용은 프로그램으로 추가를 해서 넣으면 된다.

"commit" [

  \{"commit_id":..   ,"commit_url":...   ,"commit_status":...   , "commit_llm_summary"}:...  , ... ],

"comment_commit" [     # "commit"에 있는 것은 추가하지 않는다.

  \{"commit_id":..   ,"commit_url":...   ,"commit_status":...   , "commit_llm_summary"}:...  , ... ],

 

로 두면 될 것이고,

 

QCD_DL_ISSUE_COMMIT_INFO에 LLM_SUMMARY field를 두어 commit_url당으로 LLM query한 결과를 넣어두게 하면 될 것으로 보인다. : 매일 한번씩 동작하며  QC...
  - [2026-05-14T16:10:03.000+0900] Design Note
 # pvs_crawler/gerrit process : QCD_DL_ISSUE_FROM_MONGODB 의 COMMIT_ISSUE_ID -> QCD_DL_ISSUE_ADDITIONAL_INFO의 COMMENTS의 내용을 QCD_DL_ISSUE_COMMIT_INFO 에 등록
 ## COMMIT_ISSUE_ID , COMMIT_URL 만 저장 가능...   추가하면 gerrit rest api로 모든 내용을 받아와서 채울수 있음.  
 ### gerrit 접속이 되지 않는 것은 ERROR를 남기고 뺀다.  (이유는 서버 에러 일수 있기에 , 필요시 추후 이것들만 다시 돌릴수 있기에)
 ## QCD_DL_ISSUE_COMMIT_INFO을 COMMIT_URL  기준으로 dict만들어 최대한 재활용
 ## 이때 COMMIT LLM summary까지 만드는게 가장 좋을 듯.  (속도 문제가 되면 따로 동작시키는 것도 가능)
 # sage process : 위에 ...
  - [2026-06-01T17:08:48.000+0900] 진행된 것 없는데요. 현재 적용된 것은 최근 ticket보시면 아시겠지만, commit DB에 있는 내용을 받아서 같이 저장하고 있는 정도 입니다.

---

### [AGILEDEV-1011] PPU worklog parsing 및 분석
- **상태**: Resolved | **최종 업데이트**: 2026-05-20T13:57:36.000+0900
- **티켓 본문**: crawling을 한다. 
worklog 값을 분석한다. 
- raw data : work seconds : jira 내용을  table로 변경
- unit 마다 일별 일한 시간 ,unit의 인원수, 입력한 인원수 , MAX_seconds  , MAX_author : 평균 일한 시간
- 일별 주별 월별 입력% AVG ,  주별/월별 입력된 일수 ,
- **작업 히스토리 (User Comments)**:
  - [2026-05-19T10:06:17.000+0900] [~dongwook.song] 님에게 넘김

기본 동작만 코딩



http://mod.lge.com/hub/dongwook.song/worklog

[http://mod.lge.com/hub/dongwook.song/worklog/-/commit/e266eca5b9f6aa08d753c03c8a020e6df1ea4e24]

결과 : worklog.csv

---

### [AGILEDEV-1010] CCR 2.0 운영 관련 데이터 분석 : status (Analyzed , In Review) 머문 시간 측정건
- **상태**: Resolved | **최종 업데이트**: 2026-05-18T15:44:41.000+0900
- **티켓 본문**: # 
{*}Analyzed 상태{*}도 In Review 상태와 같이 처리 시간을 현대, 토요타, 혼다 관련해서 CCR 티켓과 함께 부탁 드리겠습니다. *(둘이 합치지 말고 각 각 뽑아 주세요)*
 # 
Analyzed 상태 Data 나오게 되면 In Review 처리 시간 Data와 함께
*-조직별 (JIRA Component 필드)로*
*-Ticket Type별로*
*-Category_VLM 별로 통계 Data* 가 나왔으면 좋겠습니다.
 # 
질문 : 각 조건에 따라    Analyzed와 In Review에서의 처리시간을 각기 뽑아달라는 말씀이시죠? *YES*


 # 
더불어 조직별로
*- Approval 인원이 몰려 있는지,*
*-평균 몇명인지,  -Approval 인원이 평균 몇개 CCR 리뷰 하는지,*
 # 
*합쳐서 :*   *approval 인원이 몇개씩 소화를 하고 이는지?    approval 인원당 CCR 갯수를 구한다.   CCR갯수/approval인원*

            *-Approval 인원이 1건 CCR 을 위해서 Analyzed 및 In Review 에 머무는 시간이 긴 특정 인원이 누구인지?*
        **        approval  인원이 포함된 CCR들에 대해서 Analyzed 와 Review에서 머문시간의 평균이 얼마인지를 표시하면 되는거죠?  (소트하면 누가 approval한 것에 대해서 머무는 시간이 많은지 알 수 있으므로) *YES* # 
 그리고 Analyzed 나 In Review 에서 {*}Reject 을 많...
- **작업 히스토리 (User Comments)**:
  - [2026-05-13T13:08:25.000+0900] collab :  http://collab.lge.com/main/spaces/VSPVS/pages/3666960232/49.+CCR+2.0+%EC%9A%B4%EC%98%81%EC%95%88+%EA%B4%80%EB%A0%A8+CCR+status%EB%B3%84+%EB%A8%B8%EB%AC%B8%EC%8B%9C%EA%B0%84%EB%93%B1%EC%97%90+%EB%8C%80%ED%95%9C+%EB%B6%84%EC%84%9D
분석 결과 :   [^target-2026-0513.zip]

---

### [AGILEDEV-1008] [pvs_crawler][sage]  50만개의 모든 ticket에서 LLM SUMMARY 적용 - QCD_DL_ISSUE_FROM_MONGODB의 모든 ticket에 대해서 LLM summary 개발
- **상태**: In Progress | **최종 업데이트**: 2026-06-01T10:33:42.000+0900
- **티켓 본문**: 결정된 후에 수행
- **작업 히스토리 (User Comments)**:
  - [2026-05-13T12:41:28.000+0900] exaone 으로 전 data를 update 하기로 결정함.
  - [2026-05-14T13:37:09.000+0900] * LLM 결과가 제대로 값들을 포함하는지 checkgk하였는데 , Field들을 누락한 경우 발생  (공통 사항 : 첫번째 항목은 누락 안시키네요. 중요한 Three-Line_Summary와 Three-Line_Summary_In_English을 제일 앞에 두게 변경해야 할 것임)

 * 
 ** [[prompt_file] sage_llm_summary.v0.006.prompt|https://llm-api.lge-vs.com/]
 ** [[exaone] OK=562, NG=46 / 608건 (7.6%) ◀ NG 있음|https://llm-api.lge-vs.com/]
 *** (41건) 누락: ['Discussion_Flow', 'Key_Decisions', 'Key_Technical_Keywords', 'Meaningful_Sentence_Extraction', 'Opinion_Exchange', 'RAG', 'Resolution_Owner', 'Root_Cause_An...
  - [2026-05-14T14:07:56.000+0900] {color:#aaaaaa}SELECT{color} * {color:#739eca}FROM{color} {color:#b788d3}QCD_DL_ISSUE_COMMIT_INFO{color} {color:#b788d3}qdici{color}

에 있는 커밋정보를 LLM_SUMMARY 에 같이 포함시키는 방안이요. 그냥 제가 상상한거라서 가능할지 검토가 되면 좋을것 같아요.
 # 이슈에 있는 COMMIT_ISSUE_ID 와 로 커밋을 찾아 이슈 연관 커밋임을 표시 (제목/URL)   : QCD_DL_ISSUE_FROM_MONGODB.COMMIT_ISSUE_ID -> QCD_DL_ISSUE_COMMIT_INFO.COMMIT_ISSUE_ID을 찾는다. 
 # 커멘트에 Commit link 가 있는 경우에는 1과 함께 표시 (제목/URL) : comments에서 나오는 [http://vgit.. 이면     QCD_DL_ISSUE_COMMIT_INFO 에 없으면 ISSUE_ID,COMM...
  - [2026-05-14T16:24:08.000+0900] http://jira.lge.com/issue/browse/AGILEDEV-1012  을 참조하면 ,  QCD_DL_ISSUE_COMMIT_INFO 에 모든 내용이 save 되어져있다. 

QCD_DL_ISSUE_FROM_MONGODB.COMMIT_ISSUE_ID -> QCD_DL_ISSUE_COMMIT_INFO.COMMIT_ISSUE_ID 을 참조하여, 

이 안의 값들을 가져와서 추가를 하면 된다. 

미리 코드는 만들어두면 될 것이다. *으로 가져오면 향후 field가 늘어나면  row(key,'')으로 내용을 받을수 있기 때문이다.

 

QCD_DL_ISSUE_COMMIT_INFO 이 완료되는 시점에서 commit 관련 내용만 update되게 다시 동작시켜주면 된다.

QCD_DL_ISSUE_FROM_MONGODB 와 QCD_DL_ISSUE_ADDITIONAL_INFO 의 ISSUE_ID는 1:1 이다.
  - [2026-05-16T11:55:31.000+0900] 보통 다음과 같이 exaone에서 1개를 처리하는데 드는 시간은 50초 / 4개 이다.  60만개를 처리하는데 드는 시간은 7500000 초 (2083시간) (87일)  이다.
현재 exaone을 사용하는 동시 session은 max가 5개이다.   문제는 시스템당이 아니라 전체인 듯 합니다. A , B  host에서 5세션씩 열어 각기 돌리면 바로 limit exceed error가 발생합니다.
[sage_llm_summary][_call_llm_single] RateLimitError (exaone, dl_oem&clm_MQBFPK-32506) [4/5]: Error code: 429 - {'error': 'concurrent request limit exceeded (max 5)'}

{noformat}
[sage_llm_summary][_call_llm_single] LLM 호출 완료 (exaone) [batch=4, worker=ThreadPoolExecutor-1...
  - [2026-05-18T15:46:44.000+0900] exaone에 성능 추가 요청
  - [2026-05-18T15:59:53.000+0900] * 문제점: exaone api 의 사용은 제가 받은 해당 키로는 system을 분산해서 접속해도 *5개의 session이 MAX* 입니다.
 ** 보통 다음과 같이 exaone에서 1개를 처리하는데 드는 시간은 50초 / 4개 이다. *60만개를 처리하는데 드는 시간은 7500000 초 (2083시간) (87일)* 이다.
현재 exaone을 사용하는 동시 session은 max가 5개이다. 문제는 시스템당이 아니라 전체인 듯 합니다. A , B host에서 5세션씩 열어 각기 돌리면 바로 limit exceed error가 발생합니다.

 ** *WorkAround : 오래된 data는 exaone으로 진행중이고 ,  최근의 데이터는 gpt-4o-mini로 진행중입니다.*
 ** field 누락되는 문제점 :  *에러가 발생하면 여러번 수행시킴  (누락되는 field가 있을때, 이를 찾아 누락된 field를 정보도 넣어주어 LLM query를 수행하여 개선)*
 *** ...
  - [2026-05-29T15:57:52.000+0900] {noformat}
$  git remote -v
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (fetch)
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (push)

$  git log -1
commit 09eb6da812a6653ec3b51db4c34bd0f3debbeada (HEAD -> master, origin/master, origin/HEAD)
Author: charles.lee 
Date:   Fri May 29 15:56:46 2026 +0900

[sage NO auto-crawling][AGILEDEV-1008] Add sage.sh auto-regenerate, sendmail.py, rtime-trend, and AUTO_FIX

- sage/sage.sh: main 실행 후 sage-check-llm-answer.py...
  - [2026-06-01T10:33:42.000+0900] 처리 대기 22651 rows / 전체 586161 rows (3.9% 남음)

---

### [AGILEDEV-1006] LGEP 초기 페이지 이미지 인식 실패
- **상태**: Resolved | **최종 업데이트**: 2026-05-08T09:32:28.000+0900
- **티켓 본문**: -> INIT
::fINIT
path D:\code\misc\pyautogui
download path D:\code\misc\pyautogui\downloads
path D:\code\misc\pyautogui
pressed win+1 : run chrome
sleep 3 seconds :
sleep 3 seconds :
sleep 3 seconds :
press ctrl+L and write sso.lge.com
sleep 3 seconds :
Point(x=1919, y=10)
INIT -> 002SSO
::f002sso
sleep 3 seconds : before sso LGEP
output/002_sso/ocr/10100.png :  : start scan
output/002_sso/ocr/10100.png 이미지를 찾을 수 없습니다. 예외가 발생했습니다. pyautogui.ImageNotFoundException
login.png :  : start scan
login.png 이미지를 찾을 수 없습니다. 예외가 발생했습니다. pyautogui.ImageNotFoundException
error ::f002sso : This is not LGEP login page. Not found image in screen : login.png
output/hr.png :  : start scan
output/hr.png 이미지를 찾았습니다: Box(left=np.int64(455), top=np.int64(98), width=37, height=21)
output/tim...
- **작업 히스토리 (User Comments)**:
  - [2026-05-08T09:32:28.000+0900] {noformat}
commit aba03c02a808f607907f52a9dc1bcde483ce00da (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Fri May 8 09:08:40 2026 +0900

    -

commit 0ad0430a9169de93f04e35f7df9b1cf4e571f285
Author: cheoljoo.lee 
Date:   Fri May 8 09:02:13 2026 +0900

    [pyautogui] add text check in f003logon
{noformat}

---

### [AGILEDEV-1005] [ticketsage] DCM 추가
- **상태**: Resolved | **최종 업데이트**: 2026-05-28T14:10:53.000+0900
- **티켓 본문**: DCM 에도 ticketsage를 적용하자.
고려사항 : 
- DB 별도 분리 유무 (별도 추천)
- 코드 별도 생성 (가능하면 한 코드로 가도록 변경)
- 수행 directory 분리 (별도로 가는 것이 맞다)
- 어디서 수행 (pvs_crawler 있는 곳에서 수행? 아니면 , test server)
- 어떤 AI 모델 적용 : exaone까지 multiple로 고려를 할 것인가?
-- priority : gpt-4o , exaone , gpt-4o-mini
- 학습은 여러개의 DCM project로 학습(RAG) ,  sage 추천(jira test)은 현재 진행되는 1개이 project에 진행
- RAG 학습이나, 다른 학습시 VDA에서 전체를 학습을 해야 하는 것과 연동을 하면 어떨까 함. 이유는 VDA를 위해서는 결국 모든 closed된 것을 봐야 하고 , 이에 대한 학습을 수행하게 된다.  할때 같이 하면 좋을 것 같다.   이렇게 되면 나중에 타 project로 확대시도 수월해질 것으로 보인다.   >> RAG summary만을 합친다.
-- priority : gpt-4o , exaone , gpt-4o-mini
-- embedding vector는 모든 티켓에서 필요한 것이 아니므로, DB를 분리해서 가지고 있어야 할 것이다.   >>  필요해서 넣은 embedding vector도 ADDTIOONAL DB에 같이 추가를 할까?
- text-embedding-3-small 에 대해서등 다양한 DB test 필요 (얼마나 차이가 있는지 보고 결정해야 할 듯)
- **작업 히스토리 (User Comments)**:
  - [2026-05-11T14:05:47.000+0900] !20260511_133228188.jpg|width=1024! 

1. function (components)에 해당되는 것을 먼처 찾는다. vector에서 먼저 선정시 모든 vector를 가지고 consine_similarity를 돌리는게 아님
2. 퇴사한 사람들은 top30을 만들이 지워버린다.   (closed ticket들에 대해서 인원이 퇴사한 것이면 vector나 RAG에 넣지도 말자)
3. LLM을 최종 문의할때 created, resolved 내용도 같이 주어 ,  시간을 고려한 답변을 받게 prompt를 조절하자.

FO를 가이드 하는 것도 보여주는 것은 맞지만,  이게 assign되는 값에 넣는 것은 맞지 않는 듯하다. (이건 추후에 결정)
  - [2026-05-27T14:21:59.000+0900] {noformat}
$  git branch
* 260526/tmcbev

$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)

$  git log -1
commit 35454aa3dad5e019ffc5913de57749415b0389db (HEAD -> 260526/tmcbev, origin/260526/tmcbev)
Author: charles.lee 
Date:   Wed May 27 12:41:42 2026 +0900    [AGILEDEV-1005] Toyota TMCBEV 를 위한 변경 : Add TMCBEV project support and FUNCTION accuracy stats
    
    - TMCBEV 프로젝트 멀티 지원...

---

### [AGILEDEV-1003] rest api (fast api)  개발환경 uv로 변경
- **상태**: Resolved | **최종 업데이트**: 2026-05-18T15:33:50.000+0900
- **티켓 본문**: pvs_crawler_rest_api 에 대해서 pipenv환경, uv환경 겹쳐있는데요, Owner를 이책임님께서 하시는 만큼, uv환경으로 통일하였으면 합니다.(pipenv관련 파일들 삭제하고, uv로만 운영될수 있도록 readme.md 포함 업데이트 부탁드립니다~)
- **작업 히스토리 (User Comments)**:
  - [2026-05-18T15:33:12.000+0900] 김기만 책임님이 완료해주심

 

Windows에서도 uv  있다면  (windows 용도 있습니다.)   

command 창에서   uv run fastapi_app.py   을 수행하시면 됩니다.  

이때 module이 없어 에러가 나오면 uv add 모듈이름     을 추가하시면 됩니다. 

uv에서는 pyproject.toml and uv.lock 을 commit 하시면 됩니다. 

 

uv는 project마다 따로 가지므로 uv run 으로 수행시 해당 project에 환경이 깔려져있지 않으면 module install을 먼저 하고 수행을 합니다.

 

 

make fastapi-server-restart

uv run fastapi_app.py 의 수행 확인 완료
  - [2026-05-18T15:33:31.000+0900] [http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_crawler_rest_api/commits/c53f306cbb69dfd4c91c7aa89a006762b7d3b805#README.md]

[http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_crawler_rest_api/commits]

---

### [AGILEDEV-1002] [ticketsage][crash] LGEDV 4월 feedback에 대한 추가 처리
- **상태**: Resolved | **최종 업데이트**: 2026-05-18T11:27:42.000+0900
- **티켓 본문**: LGEDV Human 판단 기반 모델/프롬프트 비교 파이프라인 추가
- **작업 히스토리 (User Comments)**:
  - [2026-05-04T12:31:07.000+0900] http://collab.lge.com/main/spaces/VSPVS/pages/3650916120/New+report+based+on+LGEDV+feedback+26.05.04
http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/crash/report_2026-05-04.eng.md?ref_type=heads

{noformat}
commit aaf4f621892d4a95fc45a35f414868db8fec1b91
Author: cheoljoo.lee 
Date:   Mon May 4 12:00:29 2026 +0900

    [AGILEDEV-929] feat(crash): LGEDV Human 판단 기반 모델/프롬프트 비교 파이프라인 추가
    
    - crash/compare.py: 모델별 성능 비교 리포트 스크립트
      - TP/TN/FP/FN/Accuracy/Precision/Recal...
  - [2026-05-04T15:07:41.000+0900] commit e682bd141ab2533106dc628473edf78127673e8d (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Mon May 4 15:06:51 2026 +0900

    [AGILEDEV-1002] feat(crash): add RESOLVED date filter, timeout visibility, and adaptive timeout retry
    
    - llm_parallel_project_code.py
      - add --resolved-start / --resolved-end options to filter rows by RESOLVED date
      - add _extract_timeout_duration() helper to parse timeout value from exception message
      - print LL...
  - [2026-05-06T09:18:19.000+0900] ==============================================================================================================================================================================
  [모델별 성능 비교]
==============================================================================================================================================================================
  [범례]
    4o-mini/003   = gpt-4o-mini(v0.003)
    4o/003        = gpt-4o(v0.003)
    5-mini/0021   = gpt-5-mini(v0.0021)
    5/0...
  - [2026-05-06T09:19:24.000+0900] Exaone 에 대한 내용도 추가합니다.  Exaone이 제일 좋네요.

{noformat}
버전별 모델 비교
============================================================================
  [버전 고정 → 모델별 비교]  (행=프롬프트버전, 열=모델)
============================================================================
  지표            exaone       gpt-4o  gpt-4o-mini        gpt-5   gpt-5-mini
  --------------------------------------------------------------------------
                       -            -            -       100.0%        89.7%  ← Accura...
  - [2026-05-08T09:53:38.000+0900] {noformat}
commit a246e9613d1c1585d67ba02206b35c75a56bd626 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Fri May 8 09:52:38 2026 +0900

    [AGILEDEV-1002] feat(crash): add PROJECT_CODE, ASSIGNEE_NAME columns and LGEDV subset output
    
    - Add PROJECT_CODE, ASSIGNEE_NAME to _OUTPUT_COLS (after SOURCE / after ASSIGNEE)
    - Extend cache-patch loop to cover PROJECT_CODE and ASSIGNEE_NAME from input CSV
    - Extract iproject_code, iassignee_name in run_task()...

---

### [AGILEDEV-1001] EXAONE 고려
- **상태**: Resolved | **최종 업데이트**: 2026-05-08T12:43:32.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-05-08T11:00:31.000+0900] [AGILEDEV-1001][service중 아님] sage_llm_summary: EXAONE 지원, 다중 모델, 프롬프트 개선, --interval-days 추가

- EXAONE 클라이언트 추가: `_get_llm_client()` factory, EXAONE system role 미지원 대응
  (system+user 합산 단일 user 메시지)
- 다중 모델 지원: `--models gpt-4o-mini exaone` 등 복수 지정, 모델별 결과 병합 저장
- prompt/model/hash 3단계 skip 판단: 불필요한 LLM 재호출 방지
- `--prompt` / `--issues` CLI 옵션 추가
- 에러 처리 강화: AuthenticationError 즉시 종료, RateLimitError/InternalServerError retry
- 서버별 독립 Semaphore: `_g_exaone_sem(5)` + `_g_other_sem(10)`
- `...
  - [2026-05-08T12:43:32.000+0900] {noformat}
$  git log -1
commit 80b226b6bba84d012d41e89c774dccbb3d279ef4 (HEAD -> master, origin/master, origin/HEAD)
Author: charles.lee 
Date:   Fri May 8 11:02:36 2026 +0900

    sage_llm_summary: EXAONE 지원, 다중 모델, 프롬프트 개선, --interval-days 추가
    
    - EXAONE 클라이언트 추가: `_get_llm_client()` factory, EXAONE system role 미지원 대응
      (system+user 합산 단일 user 메시지)
    - 다중 모델 지원: `--models gpt-4o-mini exaone` 등 복수 지정, 모델별 결과 병합 저장
    - prompt/model/hash 3단계 skip 판단: 불필요한 LLM 재호출 방지
   ...

---

### [AGILEDEV-994] [CCR] 고객 요청 : ticket type (integration) 추가
- **상태**: Resolved | **최종 업데이트**: 2026-04-23T08:53:18.000+0900
- **티켓 본문**: CCR Ticket 에서 Ticket Type 은 현재 "Integration"도 선택 가능하며, 실제 [CCR-46624|https://kor01.safelinks.protection.outlook.com/?url=http%3A%2F%2Fjira.lge.com%2Fissue%2Fbrowse%2FCCR-46624&data=05%7C02%7Ccheoljoo.lee%40lge.com%7C9ac9f8cec96b4c1dac1508dea02ef9e7%7C5069cde4642a45c08094d0c2dec10be3%7C0%7C0%7C639124320774860974%7CUnknown%7CTWFpbGZsb3d8eyJFbXB0eU1hcGkiOnRydWUsIlYiOiIwLjAuMDAwMCIsIlAiOiJXaW4zMiIsIkFOIjoiTWFpbCIsIldUIjoyfQ%3D%3D%7C0%7C%7C%7C&sdata=5GtxhU5fMYXmk4TQ5hxfqFeNY9OerwhFjziKtl8J9eo%3D&reserved=0] 은 3{^}rd{^} party 업체 산출물의 Integration 용 ticket 입니다.
 
아래 내용에서
Ticket Type (CR/Issue/SV) 에 "Integration"도 추가하여
Ticket Type (CR/Issue/SV/Integration) 으로 수정이 필요해 보입니다.
- **작업 히스토리 (User Comments)**:
  - [2026-04-22T15:00:56.000+0900] 문관식 책임님 , 틀린 부분에 대해 말씀해주셔서 감사합니다. 
 
Ticket Type에 대해서 이후 추가될 부분도 고려하여 None이나 Null 만을 check하는게 맞습니다.   적어주신 내용 반영하겠습니다.  ({*}내일 아침에 변경이 잘되었는지 제가 확인하도록 하겠습니다.{*})
Doc은 미리 변경해두겠습니다 .  [http://collab.lge.com/main/display/VSPVS/45.+CCR+Readiness]
 
2가지 변경사항 이 적용됩니다.  * 
Ticket Type이 integration 문제 해결.  다음 msg 가 사라질 것 입니다.
 * 
  01. [Open] [F1_TICKET_TYPE] Ticket Type
    - 항목: Ticket Type
    - 내용: 유효하지 않은 Ticket Type: Integration
    - 기대값: CR / Issue / SV
    - 현재값: Integration


 * ...
  - [2026-04-23T08:53:18.000+0900] 확인 완료 : 정상 동작 : 처리 완료
http://jira.lge.com/issue/browse/CCR-46624?attachmentSortBy=dateTime&attachmentOrder=asc

{noformat}
[Updated At] 2026-04-23 04:36:03 KST 에 [Build request] CCR-46624 을 분석하였습니다.
CCR 분석에 대한 설명 페이지 : http://collab.lge.com/main/display/VSPVS/45.+CCR+Readiness

[대상 티켓] CCR-46624 - [Integration][NSCDC]Marelli QNX Application package integration for PI.30.01.03 (CW17)
[상태] Build request / P2 / Integration / 담당: julius.moon (Cluster Unit)

  추가 확인이 필요한 항목이 없습니다.
{noforma...

---

### [AGILEDEV-993] [LONG-TERM][CCR] 고객 추가 요청사항
- **상태**: Holding | **최종 업데이트**: 2026-05-18T15:51:18.000+0900
- **티켓 본문**: 개발자들의 요청 사항에 대응

---

### [AGILEDEV-990] DB Query & Update
- **상태**: Resolved | **최종 업데이트**: 2026-04-24T15:21:34.000+0900
- **티켓 본문**: - SNAPDATE로 가장 최근 3일전까지의 update된 list를 얻는다.
  DL_MONGO , DL_ADDITIONAL 모두의 SNAPDATE를 고려 한다.   이때 , 각 table의 NO도 같이 받아야 한다.
- llm 처리후에 해당 table에 update한다.
- **작업 히스토리 (User Comments)**:
  - [2026-04-21T16:42:02.000+0900] SELECT
    A.*, B.DESCRIPTION, B.COMMENTS, B.LLM_SUMMARY, B.NO AS B_NO , 
    GREATEST(
        COALESCE(A.SNAPDATE, '1970-01-01'),
        COALESCE(B.SNAPDATE, '1970-01-01')
    ) AS BIG_SNAPDATE
FROM CRAWLER.QCD_DL_ISSUE_FROM_MONGODB A
JOIN CRAWLER.QCD_DL_ISSUE_ADDITIONAL_INFO B ON A.ISSUE_ID = B.ISSUE_ID
WHERE
    GREATEST(
        COALESCE(A.SNAPDATE, '1970-01-01'),
        COALESCE(B.SNAPDATE, '1970-01-01')
    ) >= NOW() - INTERVAL 3 DAY
ORDER BY BIG_SNAPDATE DESC;

이며,  오늘이...
  - [2026-04-24T15:21:34.000+0900] SELECT
    A.NO, A.PROJECT_CODE, A.SOURCE, A.DOMAIN, A.TRACKER_ID, A.TRACKER,
    A.ISSUE_TYPE, A.ISSUE_ID, A.SUMMARY, A.FUNCTION, A.REPRODUCIBILITY,
    A.STATUS, A.DEV_STATUS, A.RESOLUTION, A.SEVERITY,
    A.ROOT_CAUSE, A.ROOT_CAUSE_TYPE, A.CORRECTIVE_ACTION,
    A.ASSIGNEE, A.ASSIGNEE_NAME, A.OWNER,
    A.CREATED, A.UPDATED, A.RESOLVED, A.CLOSED,
    B.DESCRIPTION, B.COMMENTS,
    B.NO      AS B_NO,
    B.SNAPDATE AS B_SNAPDATE,
    B.DL_BIG_SNAPDATE,
    B.LLM_SUMMARY,
    B.HASH...

---

### [AGILEDEV-989] [ticketsage] QCD_DL_ISSUE_FROM_MONGODB의 모든 ticket에 대해서 LLM summary 개발
- **상태**: Resolved | **최종 업데이트**: 2026-05-08T13:26:27.000+0900
- **티켓 본문**: - [https://llm-api.lge-vs.com/] 사용 환경 설정
 - pvs_crawler에 넣는다.
 - gpt-4o-mini 이용 (비용) : exaone까지 multiple로 넣는 것은 안되려나? 비용고려
 - 병렬 수행 (속도)  : 요즘 exaone이 속도도 빨라지고 좋아졌다고함.
 - DB는 QCD_DL_ISSUE_ADDITIONAL_INFO 에 Field (LLM_SUMMARY)
 - LLM summary를 rest api로 제공
- **작업 히스토리 (User Comments)**:
  - [2026-04-21T16:26:22.000+0900] 날짜마다의 처리량

{noformat}
SELECT
    DATE(GREATEST(
        COALESCE(A.SNAPDATE, '1970-01-01'),
        COALESCE(B.SNAPDATE, '1970-01-01')
    )) AS SNAPDATE_DATE,
    COUNT(*) AS ITEM_COUNT
FROM CRAWLER.QCD_DL_ISSUE_FROM_MONGODB A
JOIN CRAWLER.QCD_DL_ISSUE_ADDITIONAL_INFO B ON A.ISSUE_ID = B.ISSUE_ID
GROUP BY SNAPDATE_DATE
ORDER BY SNAPDATE_DATE DESC;
{noformat}

 !screenshot-1.png!
  - [2026-04-24T15:23:10.000+0900] {noformat}
$  git log -1
commit a7bf08813843b019c8892f142c82a6603e671810 (HEAD -> master, origin/master, origin/HEAD)
Author: charles.lee 
Date:   Fri Apr 24 15:22:23 2026 +0900

    [AGILEDEV-989] [service중 아님] Add adaptive worker control and snapdate field to sage_llm_summary / Fix sage_llm_summary LLM endpoint and SQL performance
    
    - Semaphore 기반 Adaptive worker 도입
      - INITIAL_WORKERS=5에서 시작
      - timeout 없이 완료 시 +1 (최대 MAX_WORKERS=13)
      - timeout 발생 시 -1 (최소 1)
 ...
  - [2026-05-08T12:45:49.000+0900] https://llm-api.lge-vs.com/ 사용 환경 설정 (완료)
pvs_crawler에 넣는다. (일단 별도로 운영 : source만 같이 넣어둠)
gpt-4o-mini 이용 (비용) : exaone까지 multiple로 넣는 것은 안되려나? 비용고려 (완료)
병렬 수행 (속도) (완료)
요즘 exaone이 속도도 빨라지고 좋아졌다고함. (완료)
DB는 QCD_DL_ISSUE_ADDITIONAL_INFO 에 Field (LLM_SUMMARY) (완료)
RAG prompt도 합체 (완료)
LLM summary를 rest api로 제공 (완료)

---

### [AGILEDEV-985] [CCR] CAnalysisVlm.py  refactoring
- **상태**: Resolved | **최종 업데이트**: 2026-04-22T13:52:33.000+0900
- **티켓 본문**: 4209 아래 내용들에 대해서 별로도 수행 가능하도록 refactoring을 진행한다.
make ccr-post
- **작업 히스토리 (User Comments)**:
  - [2026-04-20T15:00:54.000+0900] {noformat}
$  git log -1
commit 0796e2d3b11258349ee5ad563f7363dca2d35244 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Mon Apr 20 14:58:17 2026 +0900

    [AGILEDEV-985] Add standalone ccr_post flow and Makefile target docs / worklog in vscode
    
    - Add `ccr_post.py` standalone `main()` to read `data/final_data.json` and execute post-statistics generation path
    - Reconstruct required post inputs (`row`, `wrong_tickets`, `screening_fieldnames`, `violation_...

---

### [AGILEDEV-984] [ticketsage][summary] self-heal legacy CONTEXT and downgrade recoverable parse logs
- **상태**: Resolved | **최종 업데이트**: 2026-04-20T09:31:12.000+0900
- **티켓 본문**: [ERROR] [QueryContext] Processing batch 251 ~ 300 issue_id:vlm=HMCCW-1333 json.loads(CONTEXT) failed (len=19954): Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

[ERROR] [QueryContext] Processing batch 1451 ~ 1500 issue_id:vlm=HMCCW-323 json.loads(CONTEXT) failed (len=41330): Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

[ERROR] [QueryContext] Processing batch 1651 ~ 1700 issue_id:vlm=HMCCW-361 json.loads(CONTEXT) failed (len=5346): Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

[ERROR] [QueryContext] Processing batch 1651 ~ 1700 issue_id:vlm=HMCCW-3617 json.loads(CONTEXT) failed (len=6549): Expecting property name enclosed in double quotes: line 1 column 2 (char 1)

[ERROR] [QueryContext] Pro...
- **작업 히스토리 (User Comments)**:
  - [2026-04-20T09:31:06.000+0900] fix(summary): self-heal legacy CONTEXT and downgrade recoverable parse logs

- Change recoverable `json.loads(CONTEXT)` failure log from ERROR to WARNING
- Add legacy CONTEXT repair path to normalize python-dict strings into canonical JSON
- Persist repaired CONTEXT back to `QCD_SAGE_LLM_QUERY` via context-only update
- Deduplicate repair updates by `ISSUE_ID` within batch
- Update `README.md` with 2026-04 recent changes


{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/che...

---

### [AGILEDEV-969] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : system 적용 및 동작 확인 (post_jira)
- **상태**: Resolved | **최종 업데이트**: 2026-04-22T15:07:44.000+0900
- **티켓 본문**: Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : system 적용 및 동작 확인 (post_jira)
- **작업 히스토리 (User Comments)**:
  - [2026-04-20T13:41:33.000+0900] before : http://jira.lge.com/issue/browse/CCR-46842
after: http://jira.lge.com/issue/browse/CCR-44426
  - [2026-04-20T13:45:51.000+0900] {noformat}
$  git log -1
commit 2ee887dbdbde9130f93e4b1ba1187780e8feb24b (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Mon Apr 20 13:45:07 2026 +0900

    [AGILEDEV-969] Fix Open matrix baseline and update Jira detail header / change crontab
    
    - Fix `CCCRStatus._check_open_matrix()` to evaluate Open violations against the initial history snapshot instead of current final matrix
    - Add `_get_open_reference_matrix()` and use first `Shift-Left-Matrix-Histo...
  - [2026-04-20T13:49:30.000+0900] 4/21 오전 동작 확인 필요
  - [2026-04-21T14:35:57.000+0900] 문제점들이 발견되어 추가 작업

## 2026-04-21 13:45 ~ 14:16 (0h 31m) [tool: vscode-copilot / session: unknown]
- **[승인 컬럼 history 변경 이력 기반 체크 도입]** `_is_matrix_approval_ever_changed()` 신규 추가: Open 시점 비교 대신 history 전체 스냅샷을 set으로 수집해 값이 한 번이라도 바뀐 적 있으면 통과, 단일값(`O→O→O`)이면 위반으로 처리
- **[승인 호출부 4곳 교체]** In Progress / In Review(요구사항·설계리뷰) / Build Request 승인 체크를 `_is_matrix_value_filled_and_changed_from_open` → `_is_matrix_approval_ever_changed`로 교체
- **[M_OPEN_APPROVAL 항목 필터링 버그 수정]** `_is_matrix_approval_check...
  - [2026-04-21T14:36:52.000+0900] 4/22 결과 확인
- post_jira_comment.txt
- log 
- updated ticket contents
  - [2026-04-22T15:07:44.000+0900] 주간업무보고 작성

 

Shift-Left 활동의 가속화 및 효율화를 위해 CCR(Code Change Request) 티켓의 리뷰 준비 상태를 자동 점검하고 해당 티켓 내 코멘트로 이를 안내하는 CCR Readiness 서비스를 운영 시작하였습니다(4/21,화 ~). 매일 평균 약 700건의 티켓을 분석 중이며, System SW Expert Task에서 Release되는 COMMIT 기반 CCR 티켓을 대상으로 티켓 상태(Status) 변경 시점마다 사전 정의된 규칙에 부합하는지 자동 점검하도록 구성하였습니다. 본 기능은 리뷰어 관점에서는 검토 필수 항목의 충족 여부를 한눈에 파악할 수 있고, 개발자 관점에서는 보완이 필요한 영역을 즉시 확인하여 빠르게 보강할 수 있는 환경을 제공합니다. 공식 서비스 오픈전 각 개발실의 CFR(Chief Function Reviewer)을 대상으로 설명회 및 VoE를 수집하여 1차 개선을 진행하였으며, 주요 개선 항목으로는 ① Gerri...

---

### [AGILEDEV-963] [ticketsage] DB에 저장되는 값이 list 나 dict 를 저장시 json이 아닌 str로 저장하여 추후 list, dict로 원복이 안되는 문제
- **상태**: Resolved | **최종 업데이트**: 2026-04-06T09:53:43.000+0900
- **티켓 본문**: 1. field들을 조사하여 값들이 list 나 dict가 들어간 field들을 확인

2. 들어간 내용들을 json load 가 될수 있게 변경

3. 실제 str로 저장하는 것을 json형식으로 저장하게 하여야 하며,   read할때도 json 형식이 아니면 [ERROR] 가 발생하도록 만들어야함.
- **작업 히스토리 (User Comments)**:
  - [2026-04-02T10:42:06.000+0900] # check : db_check.py
 # DB 변경 : db_migration_dryrun.py
 #  소스 변경하고 확인도 해야함.
  - [2026-04-02T13:45:54.000+0900] 1,2번을 처음에는 잘못하여 QCD_SAGE_LLM_QUERY 이외의 것은 그냥 txt가 들어가는 것을 망각함.

QCD_SAGE_LLM_QUERY  에만 CONTEXT에 json이 들어가고 , 다른 것들은 그냥 text

json은 {  니나 [  으로 시작해야 함
  - [2026-04-02T14:59:29.000+0900] CONTEXT에 대해서 QCD_SAGE_LLM_QUERY  에만 CONTEXT에 json이 들어가게 변경: field별로 모두 있는지를 조사하고 , 변경된 것이 있으면 해당 key를 print

json일때 json error가 발생하면 [ERROR] 를 넣게함.

db_migration_dryrun.py 을 이용하여 기존 DB에 {  [ 로 시작하는 것에 대해서는  json 형태가 맞는지 확인 및 json.dumps()가 에러가 나면 제대로 된 json으로 변환해서 upload함.

serialize , deserialize를 명확하게 표현함.

 

{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
{noformat}
...

---

### [AGILEDEV-958] skills 분석 및 적용
- **상태**: Resolved | **최종 업데이트**: 2026-04-17T14:26:46.000+0900
- **티켓 본문**: *Copilot은 먼저 skill의 name과 description만 읽고, 사용자 요청과 매칭되면 그때 SKILL.md 본문을 컨텍스트에 주입합니다. 따라서 description을 얼마나 잘 쓰느냐가 라우팅 정확도를 결정합니다 .github/skills/ 폴더에 넣으면 description 기반으로 자동 매칭됩니다. 별도로 "이걸 읽어라"고 지정할 필요 없습니다.*

 

*큰 그림을 그리고, 상세 내용은 한 단계씩 채워가는 방식은 올바른 접근입니다. Plan Mode에서 Copilot이 먼저 요구사항을 분석하고 구현 계획을 세운 뒤 사용자 확인을 거쳐 구현하는게 정석이라고 합니다.*

 

*현재는 특정 task를 수행후 종료하기전에 무조건 self-verification을 수행하여 문제가 없을때만 종료되게 해두었는데.. 별도의 skill로 구현할 수 있을지 한번 고려해보겠습니다! 좋은 의견 감사드립니다!*

 

[http://source.lge.com/gitlab/test-auto/aea_public]

 ** 스킬은 여기에 구현되어 있습니다. 헌데 아직 진행중이라 ㅠㅜ 완벽하지 않습니다.

 ** 조금 더 정교하게 만들어서 4월 초/중순에 정식 배포할 예정입니다.

 ** 테스트는 Agent모드에서 스킬에 해당되는 프롬프트를 입력하면 자동으로 관련된 스킬을 호출합니다.

 ** 

*!image-2026-03-31-10-42-11-081.png|width=468,height=225!*
- **작업 히스토리 (User Comments)**:
  - [2026-03-31T10:44:38.000+0900] 가이드 5번에 보시면 사용시나리오 예시가 있는데 이대로 따라해보시면,  [^AEA_사용가이드_v2 (1) 1.pdf]

스코프맵 생성, Task decomposition, 코드 젠 하는게 순서대로 나와 있습니다! 
 * 가이드에 나와 있는것과 별개로 custom agent를 선택하지 않으셔도 사용 가능하십니다.
 * 별도 스킬들은 코드 리뷰해줘, 버그 분석해줘, 리팩토링해줘 이렇게 프롬프트 입력하면 자동으로 스킬들 사용될 것입니다.
  - [2026-03-31T10:59:55.000+0900] test 문구

 
{noformat}
아래 요구사항을 task로 분해해줘.
---
#### SyRS-003: 차량 상태 기반 처리 조정
**설명**: 시스템은 차량 속도와 조향각에 따라 이미지 처리 우선순위를 조정해야 한다.**상세 명세**:
- 입력: 차량 속도 (km/h), 조향각 (degrees), 가속도 (m/s²)
- 처리 모드:
  - **저속 모드** (속도 < 30 km/h): 표준 처리, 지연 허용 100ms
  - **중속 모드** (30 ≤ 속도 < 60 km/h): 향상된 처리, 지연 < 70ms
  - **고속 모드** (속도 ≥ 60 km/h): 최우선 처리, 지연 < 50ms{noformat}
 

tasks/tasks.json <- 결과 확인

 

 

Task 확인
생성된 Task는 아래 방법으로 확인 가능하다.
1. Agent에게 요청
"Task list 보여줘.", "Task 1 보여줘"
2. tm 명...
  - [2026-03-31T19:13:53.000+0900] [http://source.lge.com/gitlab/test-auto/aea_public.git]

 



각 단계별 skills 에 대한 comments를 작성하였습니다.

[http://source.lge.com/gitlab/test-auto/aea_public/-/issues/1]

 

 
{noformat}
@youngjae.cho 님 , 작성하느라 수고 많으셨습니다.  감사합니다.
requirement의 예제를 주시면, 거기에 맞추어 gmail 관련 project에 대한 요구사항을 넣고 수행해보고 feedback을 남기겠습니다. 

- 일하는 순서는 어떻게 되는가? 아래의 순서대로 되나요? 이렇게 수행되도록 하는 prompt 예제가 있었으면 좋겠습니다.                                                                                                          ...
  - [2026-04-06T09:47:43.000+0900] worklog skill

 

{noformat}
---
description: "일을 정리 해주세요" 트리거 — README, worklog, lessons 자동 정리
---

# 스킬: 작업 정리

사용자가 **"일을 정리 해주세요"** 또는 **"일을 정리 해줘"** 라고 입력하면
아래 순서대로 수행한다.

---

## 사전 단계 A — 월별 아카이브 체크 (매월 초 자동 처리)

현재 날짜의 **월(YYYY-MM)** 과 `worklog.md` 첫 줄의 월이 다르면 (= 새 달):

1. `worklog.md` → `worklog/YYYY-MM.md` 로 이동 (YYYY-MM = 지난달)
2. `data/worklog.json` → `data/worklog/YYYY-MM.json` 으로 이동
3. `worklog.md` 새로 생성 (빈 파일 + 헤더)
4. `data/worklog.json` 새로 생성 (`[]`)
5. `work...
  - [2026-04-17T14:26:14.000+0900] 세미나 완료
skills와 instructions의 비교 및 사용법 : https://github.com/cheoljoo/agents/blob/main/skills_and_instruct_ions.md

worklog skill : 오늘 한 일 정리 및 commit msg 생성

- https://github.com/cheoljoo/agents/blob/main/.github/skills/worklog-manager/SKILL.md

예) /instructions  , /skills list

---

### [AGILEDEV-957] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : 연속적으로 동작을 하여 개발자가 변경 후에 빠르게 응답을 받을수 있게 하기
- **상태**: Resolved | **최종 업데이트**: 2026-05-08T10:43:10.000+0900
- **티켓 본문**: CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
 - 현재 필요한 것으로 Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. 이때 , gerrit에 대한 사항도 check되었으면 한다. (action item 반영)
 - 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다. ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
 - 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
 - shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
 - 필수 항목들은 mandatory로 설정되면 좋을 듯 하다.
 - 메시지 관련 : Critical 과 같은 표현보다는 "~을 더 봐달라!" 나 "논의가 더 필요하다" / "다음 사항 중 빠진 것이 있는지 체크 부탁드립니다." 와 같은 표현이었으면 한다. (action item 반영)
 - AI가 더 제대로 활용될수 있게 token을 확보해주어으면 한다.
 - gerrit에 bot 들이 너무 많은 comments를 남겨 이에 대한 처리도 시간이 많이 든다.

문의점 :
 - 메일이 많아지는 문제 (To 이효진)
 - action item : - 연속적으로 동작을 하여 개발자가 변경 후에 빠르...
- **작업 히스토리 (User Comments)**:
  - [2026-03-31T10:33:54.000+0900] 매일 오전 1번씩 수행
DB와 비교를 해서 (conf를 만들어 post_comments를 하는 시기로 입력을 받게 하자)
 * status의 변경될시 check 
 * gerrit 변경시 check
 * 요청이 있는 applied project에 대해서
3개를 모두 or 로 하여 처리

---

### [AGILEDEV-956] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : applied project에 따른 추가적 field나 값 check
- **상태**: Resolved | **최종 업데이트**: 2026-04-07T08:54:50.000+0900
- **티켓 본문**: CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
 - 현재 필요한 것으로 Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. 이때 , gerrit에 대한 사항도 check되었으면 한다. (action item 반영)
 - 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다. ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
 - 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
 - shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
 - 필수 항목들은 mandatory로 설정되면 좋을 듯 하다.
 - 메시지 관련 : Critical 과 같은 표현보다는 "~을 더 봐달라!" 나 "논의가 더 필요하다" / "다음 사항 중 빠진 것이 있는지 체크 부탁드립니다." 와 같은 표현이었으면 한다. (action item 반영)
 - AI가 더 제대로 활용될수 있게 token을 확보해주어으면 한다.
 - gerrit에 bot 들이 너무 많은 comments를 남겨 이에 대한 처리도 시간이 많이 든다.

문의점 :
 - 메일이 많아지는 문제 (To 이효진)
 - action item : - 연속적으로 동작을 하여 개발자가 변경 후에 빠르...
- **작업 히스토리 (User Comments)**:
  - [2026-03-31T10:34:57.000+0900] 현대 CW의 경우 적어도 Ticket Type: 에
CR,  LGE Issue(DQA/QE) 기입되어있는경우에는 Internal-Issue-Link: 가 무조건 있어야하고
OEM Issue 인경우 External-Issue-Link: 필요하고
Integration, SV : 링크없어도됩니다.
  - [2026-03-31T15:29:20.000+0900] *조직을 Check하여 추가할수 있게 만들자.(전체를 할수도 있고, 특정 조직들만 할수도 있게)*

 
이건프로젝트마다 상황이 다르기때문에 한번 조사해보셔야할것같습니다. 
당장에 현대에서 지적온사항들이 CCR내용이기때문에 위와같은 내용들이 포함되면 좋을것같습니다..
>> 현대ConnectWide 에 대해서 추가하도록 하겠습니다. 
  * 
이내용은 plm에서 정해진게 아닙니다. 일괄반영하시면안됩니다.
팀내에서의 기본적인 추적성 rule입니다. 이런건 ccr관리부서에 내용확인후 도입하셔야할것같습니다. 

 
 
 
status 가 architecture 리뷰가 딱 시작되는순간의 status 에 대해서만 snapshot찍어서 위반사항에 대해 공유하면 좋을것같습니다. 
>> In Review 에 들어갔을때만 check해 달라는 것인지요?  아니면 , 각 status에 처음 도달했을때 check해 달라는 것인지요? * 
실제 inreview로 FA에게 리뷰받을때 ...
  - [2026-04-07T08:51:34.000+0900] applied project == 현대ConnectWide일때  Ticket Type을 보고 check

{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)
{noformat}


{noformat}
 $  git log -1
commit 7c8a4ebd2176248dcf18f659eb72f92acb1d7ee3 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Mon Apr 6 16:10:20 2026 +0900

    [AGILEDEV-953,954,955] Refactor ConnectWide check to CCCRStatus, fix Gerrit URL parsing...

---

### [AGILEDEV-955] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : 표현변경
- **상태**: Resolved | **최종 업데이트**: 2026-04-08T16:15:55.000+0900
- **티켓 본문**: CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
 - 현재 필요한 것으로 Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. 이때 , gerrit에 대한 사항도 check되었으면 한다. (action item 반영)
 - 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다. ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
 - 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
 - shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
 - 필수 항목들은 mandatory로 설정되면 좋을 듯 하다.
 - *메시지 관련 : Critical 과 같은 표현보다는 "~을 더 봐달라!" 나 "논의가 더 필요하다" / "다음 사항 중 빠진 것이 있는지 체크 부탁드립니다." 와 같은 표현이었으면 한다. (action item 반영)*
 - AI가 더 제대로 활용될수 있게 token을 확보해주어으면 한다.
 - gerrit에 bot 들이 너무 많은 comments를 남겨 이에 대한 처리도 시간이 많이 든다.

문의점 :
 - 메일이 많아지는 문제 (To 이효진)
 - action item : - 연속적으로 동작을 하여 개발자가 변경 후에 ...
- **작업 히스토리 (User Comments)**:
  - [2026-04-08T16:15:40.000+0900] {noformat}
 $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)

$  git log -1
commit d4692d505f79e007744108ebb9d56102359fea0b (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed Apr 8 16:14:12 2026 +0900

    [AGILEDEV-955][CCR] Fix Gerrit cache, MERGED status, Resolved/Closed skip, URL space indent

    - Fix Gerrit DB cache comparison: use _normalize_gerrit_link_for_compare() ...

---

### [AGILEDEV-954] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : gerrit 사항 반영
- **상태**: Resolved | **최종 업데이트**: 2026-04-02T17:43:11.000+0900
- **티켓 본문**: !image-2026-03-31-10-36-26-347.png!

 

CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
 - 현재 필요한 것으로 Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. 이때 , *gerrit에 대한 사항도 check되었으면 한다.* (action item 반영)
 - 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다. ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
 - 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
 - shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
 - 필수 항목들은 mandatory로 설정되면 좋을 듯 하다.
 - 메시지 관련 : Critical 과 같은 표현보다는 "~을 더 봐달라!" 나 "논의가 더 필요하다" / "다음 사항 중 빠진 것이 있는지 체크 부탁드립니다." 와 같은 표현이었으면 한다. (action item 반영)
 - AI가 더 제대로 활용될수 있게 token을 확보해주어으면 한다.
 - gerrit에 bot 들이 너무 많은 comments를 남겨 이에 대한 처리도 시간이 많이 든다.

문의점 :
 - 메일이 많아지는 문제 (To 이효진)...
- **작업 히스토리 (User Comments)**:
  - [2026-04-02T17:43:11.000+0900] $  make gerrit-review 
Start : make gerrit-review
uv run python -u gerrit_review.py --input-csv gerrit_url_list.csv --output-json gerrit_url_list.json --brief
- server=acp | state=pending | project=acp/com.webos.service.hccmanager | change=1187 | status=NEW
  -> missing: Software-Integration-Release(No votes), CodeReview-Verified(No votes), Code-Review(No votes), Verified(No votes)
- server=adas | state=pass | project=icmu/external-mcu | change=149428 | status=MERGED
- server=as | state=pe...

---

### [AGILEDEV-953] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅 : 현재 필요한 것으로  Build Request에서 reject가 되는 경우를 In Review에서 미리 방지
- **상태**: Resolved | **최종 업데이트**: 2026-04-07T08:52:23.000+0900
- **티켓 본문**: CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
*- 현재 필요한 것으로  Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. *이때 , gerrit에 대한 사항도 check되었으면 한다.  (action item 반영)
- 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다.  ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
- 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
- shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
- 필수 항목들은 mandatory로 설정되면 좋을 듯 하다.
- 메시지 관련 : Critical 과 같은 표현보다는 "~을 더 봐달라!" 나 "논의가 더 필요하다" / "다음 사항 중 빠진 것이 있는지 체크 부탁드립니다." 와 같은 표현이었으면 한다. (action item 반영)
- AI가 더 제대로 활용될수 있게 token을 확보해주어으면 한다.
- gerrit에 bot 들이 너무 많은 comments를 남겨 이에 대한 처리도 시간이 많이 든다.

문의점 :
- 메일이 많아지는 문제  (To 이효진)
  - action item : - 연속적으로 동작을 하여 개발자가 변경 후에 빠르게 ...
- **작업 히스토리 (User Comments)**:
  - [2026-04-01T15:32:43.000+0900] 현재 status가 {{{}In Review{}}}이면 [CCCRStatus.check_status('In Review')|vscode-file://vscode-app/c:/Users/cheoljoo.lee/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/workbench/workbench.html]에서 아래가 모두 실행됩니다.
 * {{Open}} 체크
 * {{Analyzed}} 체크
 * {{In Progress}} 체크
 * *{{In Review}} 체크* ✅

그리고 이 시점에는
 * [Build Request|vscode-file://vscode-app/c:/Users/cheoljoo.lee/AppData/Local/Programs/Microsoft%20VS%20Code/resources/app/out/vs/code/electron-browser/wo...

---

### [AGILEDEV-941] [ticketsage/summary] 24000개 issue udpate From DL_ISSUE_.._MONGO DB
- **상태**: Resolved | **최종 업데이트**: 2026-04-02T10:41:01.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-03-27T10:43:45.000+0900] 원인 : DL_ISSUE_*MONGO 에서 약 24,000 개의 변경이 생김.  이때 기존에 filter걸어두었던 AND NOT (A.SNAPDATE = '2026-02-24' AND CUSTOM1 = 'HMG'); 까지 모두 update가 되어버림.
어떻게 check했는가?  이리 2,000 개 이상의 변경이 생기면 ERROR 발생하게함.  --> [ERROR] ⚠️ Yesterday's data count (23938) exceeds 2000! Abnormal data volume detected. Exiting.
해결책 : 어제 발생한 것으로 AND NOT (A.SNAPDATE = '2026-02-24' AND CUSTOM1 = 'HMG');  -> AND NOT (A.SNAPDATE = '2026-03-26' AND CUSTOM1 = 'HMG'); 으로 변경하고 ,    DL_ISSUE_*MONGO 수집시 Updated field는 변경 내용에서 삭제

앞으로의 예측 ...

---

### [AGILEDEV-939] CCR ticket안의 reviewer들에 대한 분석 : trender의 AHC와 함께 
- **상태**: Resolved | **최종 업데이트**: 2026-03-26T15:22:24.000+0900
- **티켓 본문**: trender의 AHC는 월에 대한 내용이 없어서 각 월별로 뽑아야 한다.
이것과 비교를 하여 1,2월에 대한 CCR only를 뽑아야 한다.
실 이름까지 추출을 해야 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-03-26T11:06:45.000+0900] 실 이름은 VCOD SVC의 QCD_UNIT_INFO를 참조
  - [2026-03-26T15:12:48.000+0900] 월마다 trender에서 뽑은 data와 비교한 것인 csv 파일 마지막 행의 Trender_Active 입니다. False인 것이 CCR only 입니다.   Active*.xlsx의 월마다 받은 trender에서 download 받은 것도 첨부 합니다.


{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)
{noformat}


{noformat}
$  git log -1
commit fbf5e10ffa669f9a26d4150281cfb7984b4610f4 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Thu Mar 26 15:18:43 2026 +0900

   ...

---

### [AGILEDEV-937] crontab 서비스 관련 log 정리.  딱 주로 보는 내용과 ERROR만
- **상태**: Resolved | **최종 업데이트**: 2026-04-06T13:58:30.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-03-26T08:53:36.000+0900] ccr

{noformat}
$  git log -1
commit 185c1d92c31ec3c46abe746b0ddda899aac46584 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed Mar 25 13:12:58 2026 +0900

    [AGILEDEV-928] CCR ticket안의 reviewer들에 대한 분석
    
    - CAnalysisVlm.py
      - reduce LOG
{noformat}
  - [2026-03-26T10:43:47.000+0900] ticketsage/summary

{noformat}
$  git log -1
commit f8dc49a5c59b6204d028fc0c67ff2c54f9a25142 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Thu Mar 26 10:43:18 2026 +0900

    [AGILEDEV-937] crontab 서비스 관련 log 정리. 딱 주로 보는 내용과 ERROR만 : ticketsage/summary 로그 축소
    
    - ticketsage/summary 로그 축소
{noformat}
  - [2026-03-26T13:24:57.000+0900] ticketsage/db_test (jira_test)

{noformat}
$  git log -1
commit 4bdddc46489428f55e9243f6f351f67e88a33613 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Thu Mar 26 13:24:14 2026 +0900

    [AGILEDEV-937] crontab 서비스 관련 log 정리. 딱 주로 보는 내용과 ERROR만 : ticketsage/db_test (jira_test) 로그 축소
    
    - ticketsage/db_test/CSAGE_JIRA_TEST.py 로그 축소
    - db_all.py : CDataBase를 선언지 debug 값을 set해줌. (CDBALL에서의 self.debug)
    - summary/ticketsage_llm_summary.py : CDataBase 에...
  - [2026-03-27T10:56:20.000+0900] ccr :  변경된 tickt이 800개이상이어 각각 2줄씩만 pritn하는데도 많음.   전체 값을 먼저 보여주고 , 뒤에 어떤 field들이 몇번이나 변했는지 sumamry정보만 나타내는 것이 좋을 듯

---

### [AGILEDEV-930] Expert task 협의하여 기능 추가 및 유지 보수 - 각 실  대표 CFR과 미팅
- **상태**: Resolved | **최종 업데이트**: 2026-04-01T15:31:48.000+0900
- **티켓 본문**: 각 실의 대표 CFR과 미팅

취지 설명하고 더 도움이 되는 방향으로...
- **작업 히스토리 (User Comments)**:
  - [2026-03-25T14:31:19.000+0900] 미팅 요청 메일 전송
  - [2026-04-01T15:31:48.000+0900] CCR Readiness 회의록
참석자 : 신경진 , 주혜진 , 한찬재 , 권민우 , 김지선 , 이효진 , 최성우,이정미,이철주
회의록 :
 * 
 -- 현재 필요한 것으로 Build Request에서 reject가 되는 경우를 In Review에서 미리 방지를 했으면 한다. *이때 , gerrit에 대한 사항도 check되었으면 한다. (action item 반영)

 - 당일 끝나는 것들이 있다. 하루에 1번 동작을 한다면 당일 끝나는 것들에 대해서는 feedback을 못 받는다. ticket 변경사항에 대한 빠른 feedback이 있었으면 한다. (action item 반영 / 문의점)
 - 모델에 따른 field를 추가적으로 Check가 되었으면 한다. (action item 반영)
 - shift-matrix나 status 변경시 누가 했는지는 중요하지 않는 것 같다. (action item 반영)
 - 필수 항목들은 mandatory로 설정되면 좋을 듯 하...

---

### [AGILEDEV-929] LGEDV Crash Issue List 검토 : LGEDV 검토 이슈해당 project들에 대한 crash 검출 (기간 resolvedDate 기준 26년 데이터) - 병렬 query
- **상태**: Resolved | **최종 업데이트**: 2026-05-04T12:28:26.000+0900
- **티켓 본문**: 병렬로 query를 하여 LLM query시간을 줄이자.
- **작업 히스토리 (User Comments)**:
  - [2026-03-25T15:51:32.000+0900] {noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
{noformat}


{noformat}
$  git log -1
commit c1713cedd325b438f3f2e5fbc4776000040b2d8e (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Wed Mar 25 15:48:06 2026 +0900

    [AGILEDEV-929] LGEDV Crash Issue List 검토 : LGEDV 검토 이슈해당 project들에 대한 crash 검출 (기간 resolvedDate 기준 26년 데이터) - 병렬 query
    
    LGE...

---

### [AGILEDEV-928] CCR ticket안의 reviewer들에 대한 분석
- **상태**: Resolved | **최종 업데이트**: 2026-03-26T10:52:20.000+0900
- **티켓 본문**: 우선은 담당님 숙제는 각 유닛에서 커밋을 하는 인원을 몇명이 되고 커밋은 평균 얼마씩 하나요? 였는데요
저희가 해당 정보를 제공할때 리뷰어까지 포함을 하여서 Data를 제공하였습니다.
헌데 유닛 리더분들이 더 나아가.. CCR 티켓 관련해서도 내용을 포함 해달라고 요청이 왔습니다.

우선 담당님 숙제 Due Date 인 27일까지는 불가능하다고  inform 하였고 Unit 리더들이 알아서 Tracking 해 달라고 요청 드렸는데요.

JIRA CCR 티켓 관련해서 티켓의 필드 정보로 리뷰어 구분할 수 있는지?  만약 불가능하다면
코멘트로 리뷰어를 구분해야 하는지? (아직 구분하라는 것은 아닙니다.)
- **작업 히스토리 (User Comments)**:
  - [2026-03-24T15:22:35.000+0900] 생성시간 25년 12월 ,26년 1월 , 2월 데이터를 DB로 뽑아보겠습니다. 
CCR 정보에 CFR field가 있습니다. 그러나, 이것은 26년 2/11 부터 생성되었습니다. 
field 변경자들 : Unit Leader (지난번 말씀드렸듯이 real 아닌 다수) , Assignee 와 shift-left matrix를 update한 사람들이 누구인지 알수 있습니다.
comments 추가자들 : 추가로 comment를 단 사람들 list와 건수도 같이 추가하도록 하겠습니다.
status 변경자들

그 외에 더 봐야 하는 것이 있으면 말씀해주십시요. 
CCR 분석시 LLM을 사용하는 부분은 없습니다.
  - [2026-03-25T13:15:18.000+0900] {noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)
{noformat}


{noformat}
$  git log -1
commit 185c1d92c31ec3c46abe746b0ddda899aac46584 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed Mar 25 13:12:58 2026 +0900

    [AGILEDEV-928] CCR ticket안의 reviewer들에 대한 분석
    
    - CAnalysisVlm.py
      - reduce LOG
      - add option : --no_write_db (do not add or upd...

---

### [AGILEDEV-926] LGEDV Crash Issue List 검토 : LGEDV 검토 이슈해당 project들에 대한 crash 검출 (기간 resolvedDate 기준 26년 데이터)
- **상태**: Resolved | **최종 업데이트**: 2026-04-01T08:55:50.000+0900
- **티켓 본문**: LGEDV Crash Issue List 검토 : LGEDV 검토 이슈해당 project들에 대한 crash 검출 (기간 resolvedDate 기준 26년 데이터)
1. Matching되는 ticket들에 대한 project code를 뽑는다.
2. 뽑힌 project code들의 26년 데이터에 대해서 LLM 동작시켜 결과를 뽑는다.
- **작업 히스토리 (User Comments)**:
  - [2026-03-25T13:47:21.000+0900] LGDV 25년도 자료의 Project_Code를 기반으로 26년도 내용에 대한 Crash 조사
SQL - Generated SQL (RESOLVED: 2026-01 ~ 2026-03):
============================================================
SELECT A.*, B.DESCRIPTION, B.COMMENTS, B.SNAPDATE AS DL_ADDITIONAL_SNAPDATE
FROM CRAWLER.QCD_DL_ISSUE_FROM_MONGODB A
JOIN CRAWLER.QCD_DL_ISSUE_ADDITIONAL_INFO B ON A.ISSUE_ID = B.ISSUE_ID
WHERE ASSIGNEE  'no_assigned'
  AND DEV_STATUS = 'closed'
  AND (
        A.PROJECT_CODE LIKE '%PGZ17PGZ00T00%'
        OR A.PROJECT_COD...
  - [2026-03-25T15:18:44.000+0900] {noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
{noformat}


{noformat}
$  git log -1
commit 36b5a1b417df072f1cfba2ea7d2335a78d01cf44 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Wed Mar 25 15:18:01 2026 +0900

    [AGILEDEV-926] LGEDV Crash Issue List 검토 : LGEDV 검토 이슈해당 project들에 대한 crash 검출 (기간 resolvedDate 기준 26년 데이터)
    
    ```
    LGEDV...

---

### [AGILEDEV-919] 분석된 데이터로부터 Hexa 지표나 그 외의 다른 의미있는 index 도출
- **상태**: Resolved | **최종 업데이트**: 2026-04-14T14:31:09.000+0900
- **티켓 본문**: trender에는 개발자들에게 유용한 정보로 넣어주어야 한다. 
CCR Ready Screening의 경우는 expert unit 인원들에게 필요한 것을 처리해주어야함.

expert unit에 필요한 일을 처리해주면서 , 그때 모인 reject 등의 자료를 가지고 trender DB를 만들면 좋을 듯!
- **작업 히스토리 (User Comments)**:
  - [2026-04-09T11:37:10.000+0900] 다른 ticket으로 처리.. CCR trender 분석
http://jira.lge.com/issue/browse/AGILEDEV-826

---

### [AGILEDEV-918] RM unit과 협의하여 기능 추가 및 유지 보수
- **상태**: Resolved | **최종 업데이트**: 2026-03-31T10:38:33.000+0900
- **티켓 본문**: trender에는 개발자들에게 유용한 정보로 넣어주어야 한다. 
CCR Ready Screening의 경우는 expert unit 인원들에게 필요한 것을 처리해주어야함.

expert unit에 필요한 일을 처리해주면서 , 그때 모인 reject 등의 자료를 가지고 trender DB를 만들면 좋을 듯!
- **작업 히스토리 (User Comments)**:
  - [2026-03-31T10:38:33.000+0900] RM 응답 없음.

이성조 선임님의 vsautorelease 가 AI를 사용하여 모든 Build Request에 온 내용 처리로 완료인듯!

---

### [AGILEDEV-917] Expert task 협의하여 기능 추가 및 유지 보수
- **상태**: Resolved | **최종 업데이트**: 2026-04-01T15:27:57.000+0900
- **티켓 본문**: trender에는 개발자들에게 유용한 정보로 넣어주어야 한다. 
CCR Ready Screening의 경우는 expert unit 인원들에게 필요한 것을 처리해주어야함.

expert unit에 필요한 일을 처리해주면서 , 그때 모인 reject 등의 자료를 가지고 trender DB를 만들면 좋을 듯!
- **작업 히스토리 (User Comments)**:
  - [2026-03-20T09:40:12.000+0900] 회의록

CCR 실행 주체
Process 및 운영 가이드 : system SW Expert task
실행 : CFR 중심의 개발완결형 CCR 실행
CCR Readiness 반영 순서
1주일 후부터 서비스 수행한다는 공지를 먼저 하고 , 이때 VOE를 취합
서비스시 Baseline (2/11 이후의 ticket중에서 resolved/closed되지 않은 ticket) 에 적용하고 , 이후 updated 된 것들 기준으로 반영
In Review , Build Request에서 중점으로 처리
우선 경고 수준으로 처리 : 가이드 하는 목적으로 채워주세요 / 맞는지 확인해주세요. (참고: System 편의 관리 내용보다, 직관적으로 관련자가 이해 가능하도록 변경)
추후 진행 상황을 보고 system상에서 Reject를 반영
Build Request로 갈때의 승인자는 CFR / Unit Leader / Expert Group 이다. (참고: 해당 필드에 등록된 인원, 즉 누...
  - [2026-03-20T10:34:53.000+0900] http://collab.lge.com/main/display/VSPVS/45.+CCR+Readiness

---

### [AGILEDEV-914] LGEDV Crash Issue List 검토
- **상태**: Resolved | **최종 업데이트**: 2026-04-01T08:55:49.000+0900
- **티켓 본문**: # 대상 프로젝트 리스트 확보 - 엑셀에 있는 Jira/Code Beamer 중에 PVS 대상과 그렇지 않은것 분류(vspvs접근 권한 확인)
 # LGEDV에서 분류한 198건의 Crash 리스트를 Prompt 로 재분류했을 때 Crash 로 잘 분류가 되는지 확인하여 Prompt 보강이 필요하면 Prompt 보강. 미스매치인 이슈는 Crash 여부 재확인 해보기.
 # 보강된 Prompt 를 이용하여 1의 대상 프로젝트 리스트에 대해서 2026년도 이슈중 Crash 리스트 뽑아서 첨부파일처럼 엑셀 작성.
 # 3에서 뽑은 이슈 검토하여 LGEDV 송부하여 검토 요청하기.
- **작업 히스토리 (User Comments)**:
  - [2026-03-13T14:51:53.000+0900] 일 순서
1. crach keyword로 LGEDV의 내용을 접속하여 fields안에 keyword 가 들어가 있는지를 찾아보고 비교한다.
2-1. LLM에 LGEDV의 ticket들의 내용과 LGED 분석 내용을 주고 , 어떻게 하면 이런 분석들이 될지에 대해 문의한다.  
2-2. LLM 답변을 기반으로 추가적으로 할 것이 있는지를 체크
  - [2026-03-20T16:04:50.000+0900] {noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)

$  git log -1
commit 7ff237beb543f95e7d62bc659d9e67e494698312 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Fri Mar 20 16:03:23 2026 +0900

    [AGILEDEV-914] LGEDV Crash Issue List 검토
    
    - crash 검토를 통해서 prompt를 증가시켰다. (improvement) : summary/ticket_sage_summary.v0.001.prompt
    - crash/READM...
  - [2026-03-24T09:49:51.000+0900] [~hakchoong.kim] 님 , 조사 내용입니다.
전체 조사 report :  http://collab.lge.com/main/display/VSPVS/46.+Crash+ticket+Identification+from+LGDV       http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/crash/report.md?ref_type=heads

* 대상 프로젝트 리스트 확보 - 엑셀에 있는 Jira/Code Beamer 중에 PVS 대상과 그렇지 않은것 분류(vspvs접근 권한 확인)
   DL_ISSIE..FROM_MONGO (Closed) 에 포함된 것은 전체 196개중에 85개(43.4%) 입니다. 아래는 이 85개를 대상으로 LLM으로 crash인지 판별하는 시험을 하였습니다.
   3) HTTP_ERROR_STATUS Ticket Link 정렬 목록 (37건)  항목을 보시면 PVS Crawler 계정으로 ...

---

### [AGILEDEV-899] [ticketsage] QCD_SAGE_LLM_RAG_JIRA_TEST에 CREATED_DATE추가
- **상태**: Resolved | **최종 업데이트**: 2026-03-06T14:52:36.000+0900
- **티켓 본문**: QCD_SAGE_LLM_RAG_JIRA_TEST 에 CREATED_DATE 추가
- **작업 히스토리 (User Comments)**:
  - [2026-03-06T14:39:55.000+0900] SQL:

UPDATE CRAWLER.QCD_SAGE_LLM_RAG_JIRA_TEST t
JOIN CRAWLER.QCD_DL_ISSUE_FROM_MONGODB m
  ON t.ISSUE_ID = m.ISSUE_ID
SET t.CREATED_DATE = DATE_FORMAT(m.CREATED, '%Y-%m-%d');

이것은 의미가 없다. 
현재 추가되는 ticket들은 open이나 In-Progress일 것이다.
그리고, QCD_DL_ISSUE_FROM_MONGODB  에는 모두 closed된 것들이다.
  - [2026-03-06T14:52:26.000+0900] QCD_DL_ISSUE_NOT_CLOSED 와 CRAWLER.QCD_DL_ISSUE_FROM_MONGOD   을 2번 수행하여

맞는게 있으면 채워넣으면 될 것으로 보인다. 

 

 
{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
$  git log -3
commit 7c1f548143dbe0b958ef632bccb01c0983010600 (HEAD -> main, origin/main, origin/HEAD)
Merge: 2b6feec 9900e40
Author: cheoljoo.lee 
Date:   Fri Mar 6 14:51:40 2026 +0900

    Merge branch 'main' of http://mod.lge.com/hub/cheoljoo.lee/ticketsage

commit 2b6feec0bf1b89...

---

### [AGILEDEV-889] [Hexa Index LLM 이용한 자동 분석] copilot cli를 이용한 claude 분석 : phase 2
- **상태**: Resolved | **최종 업데이트**: 2026-03-05T13:58:05.000+0900
- **티켓 본문**: @ 2026-02-27(금) 회으록
- 분석시 방향성을 빼고 분석해 볼 것
- 수식보다 문장으로 => 읽기 쉽게 , 짧게 , check 해야 할 사항 위주로 분석 해달라고 요청
- 설기간 고려한 분석 요청 : 2/12~2/20일까지는 설 연휴로 분석에서 제외시켜야 할 것이다.
- 계속 작업한 내용을 LLM이 학습할수 있게 만들어야 한다.
-- 우리가 작업한 내용을 어디에 적어두어야 한다. http://collab.lge.com/main/display/VSPVS/LLM+Queries 밑에 여러가지 page로 추가 예정
-- 이를 가지고 MCP를 같이 운영하여 분석하도록 한다. 
-- project 점검회의 학습
- Active Head Count가 10 미만인 경우는 제외하는 것도 고려
- 매달 보고할대 hexa index 항목이 변경되게 하는 것이 맞다.  알아서 LLM에 분석해서 문제가 되는 항목을 선정하도록하는 것이 좋을 것이다.
- 차주 수요일 2시 회의시 내용중에서 쓸만한 내용에 대해서 추리는 작업을 해야함.
- **작업 히스토리 (User Comments)**:
  - [2026-02-27T15:09:35.000+0900] 2/27일 금요일 오전 11시 회의록 입니다. 업무 참조하시기 바랍니다.
http://collab.lge.com/main/display/VSPVS/LLM+Queries  아래에 page들을 모아두도록 하겠습니다.

prompt는 다음과 같이 MCP 연결 내용이 추가되면 될 것으로 판단됩니다.
"confluence page http://collab.lge.com/main/display/VSPVS/basic+instruction+for+connectWide  은 분석시 고려해야 할 사항을 모아둔 것입니다. 분석시 page안의 instruction들을 따라주세요."
  - [2026-03-05T13:57:49.000+0900] 43.프로젝트 점검 회의 대비 LLM 프롬프팅 정리
http://collab.lge.com/main/pages/viewpage.action?pageId=3564258412    <- 여기 모두 정리해둠.

https://github.com/cheoljoo/mcp_copilot.git
branch : llm

---

### [AGILEDEV-888] [pvs_crawler][sage] gpt-4o-mini exaone를 주로 사용하는 것을 이것이 없을때 다른 것이 있으면 그것을 사용할수 있게도 해주는 것. (비용문제 발생시)
- **상태**: Resolved | **최종 업데이트**: 2026-05-13T13:06:38.000+0900
- **티켓 본문**: [ticketsage][summary] gpt-4o를 주로 사용하는 것을 이것이 없을때 다른 것이 있으면 그것을 사용할수 있게도 해주는 것. (비용문제 발생시)

현재까지 진행중인 것은 summary에서 QCD_SAGE_LLM_QUERY 안에 SUMMARY / RAG에 대해서 gpt-4o를 사용하여 query를 하였음.
그러므로 , 당연히 jira-test 와 db-test에서는 RAG에 대해서 gpt-4o로 RAG query한 내용을 적용하였다.   

비용문제 발생시 QCD_SAGE_LLM_QUERY에 SUMMARY / RAG를 gpt-4o-mini  로 query를 하게 될 수 있다. 
이때 ,  연속성을 위해서 gpt-4o , gpt-4o-mini의 내용을 모두 사용할수 있게 jira-test 와 db-test의 코드를 변경해주어야 한다. 
예를 들면 gpt-4o를 먼저 찾고 , 없으면 gpt-4o-mini 를 찾아서 사용하는 hybrid방식을 사용하는 것이다.   이렇게 하기 위해서는 gpt-4o,gpt-4o-mini 와 같이 2가지 모두를 사용하도록 , --gpt_model 에 복수의 model을 넣을수 있게 코드가 변경되어져야 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-05-11T15:22:26.000+0900] 넣어주는 것은 지금처럼 model별로 값까지 넣어주면 되고, 
**pvs_crawler/sage 에 코드는 방영되어져있고 , 이대로 동작함.**

받아서 쓰는 곳에서만 Priority를 가지고 무엇을 쓸지 정해서 쓰면 됩니다.
  - [2026-05-13T13:06:17.000+0900] {noformat}
$  git remote -v
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (fetch)
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (push)
{noformat}
 

{noformat}
$  git log  -1
commit e727cf13e90ca52bf86c02372a68bfb3004cb8be (HEAD -> master)
Author: charles.lee 
Date:   Mon May 11 10:09:58 2026 +0900

    [AGILEDEV-1001][service중 아님] sage_llm_summary: DB 재연결 retry, _g_db_error 플래그, --max-run-hours 옵션 추가
    
    - `--max-run-hours N`: 프로그램 최대 실행 시간 CLI 옵션 추...

---

### [AGILEDEV-884] [CCR][2nd-Gen] RS Fidelity Review 연동 — CW RS 변경 항목 식별 및 RE/FRE 리뷰 상태 분석
- **상태**: Closed | **최종 업데이트**: 2026-03-18T13:32:46.000+0900
- **티켓 본문**: h2. 목적

CW 프로젝트의 신규/변경 RS items를 식별하고, RE/FRE 리뷰 완료 상태를 CCR 티켓과 연동하여 RS Fidelity 점수를 산출한다.

h2. 배경
* 2026-03~ 적용 대상
* V09.6 기준 Shift-Left Activity에서 RS Fidelity Review는 Write RS 단계에서 RE Expert가 수행
* 현재 RS Fidelity 충실도를 자동으로 측정하는 기능이 없음

h2. 구현 위치
* {{CAnalysisVlm.py}} 또는 별도 {{CAnalysisRS.py}} 신규 파일

h2. 작업 내역
# CW RS 변경 항목 수집
** Jira JQL 또는 Confluence API 활용
** CCR 티켓과 연결된 RS item 목록 추출
# RE/FRE 리뷰 상태 연동
** "리뷰 요청됨 → 리뷰 완료" 전이 확인
** RE Expert, FRE Expert 참여 이력 추적
# CCR 티켓 ↔ RS item 연결
** issue link 또는 customfield 기반 매핑
# RS Fidelity 점수 산출
** 리뷰 완료 비율 (완료 RS item / 전체 변경 RS item)
# 결과 DB 저장 및 CSV/Excel 출력

h2. 선행 조건
* G2-08 (CLI 통합 완료)

h2. 검증
* 파일럿 CW 티켓 10건으로 연동 정확성 확인

h2. 참조
* 설계서: design_notes/gen2/README.md 섹션 7.3 Phase 7 — Story G2-09
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:23:57.000+0900] h2. 🚧 신규 파일 구현 완료 — {{CAnalysisRS.py}} (2026-03-18)

h3. 구현 방식
* 기존 {{CAnalysisVlm.py}} 코드 변경 없이 *독립 신규 파일* {{CAnalysisRS.py}} 구현
* DB 저장 없음, CSV 없음 — *콘솔 출력 전용*
* Auth: {{get_jira_auth_from_qcd_env()}} 동일 패턴 사용

h3. 파일 위치
{{CAnalysisRS.py}} (프로젝트 루트)

h3. 주요 기능

|| 기능 || 설명 ||
| RS 항목 수집 | JQL로 CW 프로젝트 RS items 페이징 조회 |
| RE/FRE 리뷰 확인 | {{customfield_25344}} (Expert Group) + status + comment 분석 |
| CCR 연동 | {{issuelinks}} 기반 연결 CCR 티켓 키 추출 |
| Fidelity 점수 | {{리뷰 완료 건수 / 전체 RS 건수 × 100%}} |
| Un...
  - [2026-03-18T13:32:33.000+0900] h2. ❌ Close — 구현 불가 (Not Applicable) (2026-03-18)

h3. 사유

RS Fidelity 점수 산출의 핵심 데이터 소스인 *RS items가 CodeBeamer(codebeamer.lge.com)* 에 저장되어 있음이 확인되었습니다.
* Jira {{project = CW}} — 존재하지 않음
* Jira {{issuetype = RS}} — 존재하지 않음
* CCR 티켓 summary의 {{[CB-RS#XXXXXXX]}} 패턴 → CodeBeamer RS item 참조

CodeBeamer API 연동을 하지 않는 현재 범위에서는 *전체 변경 RS item 목록(분모)*을 가져올 방법이 없으므로 RS Fidelity 점수 산출이 불가능합니다.

h3. 재개 조건

CodeBeamer REST API 연동이 프로젝트 범위에 추가되는 시점에 재개 가능합니다.

---

### [AGILEDEV-883] [CCR][2nd-Gen] CLI 옵션 통합 (--gen2, --post_comment) + Excel Gen2 시트 + End-to-End 통합 테스트
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:36:51.000+0900
- **티켓 본문**: h2. 목적

G2-01~G2-07 구현을 하나의 실행 흐름으로 통합하고, Excel 출력 및 End-to-End 통합 테스트를 완성한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — argparse 섹션 + {{main()}} 진입점

h2. 작업 내역
# argparse 옵션 추가:
** {{--gen2}} (기본값 False): Gen2 검증 전체 활성화 (work_func 내 ⑥~⑩ 실행)
** {{--post_comment}} (기본값 False): 위반 티켓에 Jira Comment 자동 등록
# {{--gen2}} 미활성화 시 Gen2 블록 전체 skip 보장 (기존 Gen1 동작 완전 보존)
# Excel 파일(ccr.xlsx)에 Gen2 시트 추가:
** {{ccr_8}}: Workflow Validation 결과
** {{ccr_9}}: Matrix Stage Check 결과
** {{ccr_10}}: Field Validation 결과
# End-to-End 통합 테스트:
** 샘플 티켓 20건 (위반 케이스 포함)으로 --gen2 --parallel 실행
** CSV 3종(ccr_8, ccr_9, ccr_10) + DB 5개 테이블 결과 검증
** 실행 시간 측정 (20K 티켓 기준 추산)
** 기존 CSV(ccr_1~7) 결과 변경 없음 확인 (회귀 방지)

h2. 선행 조건
* G2-07 (Jira Comment 기능)

h2. 검증
* {{python CAnalysisVlm.py --gen2 --parallel}} 실행 후 결과 확인
* {{python CAnaly...
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:20:49.000+0900] h2. ✅ 목표 재정의 — Resolved (2026-03-18)

h3. 구현 방식 변경

원래 계획: {{--gen2}} 옵션 추가, Gen2/Gen1 분기  
*실제 구현: --gen2 옵션 없이 Gen2 분석이 기본 수행됨*

h3. 현재 구현된 CLI 옵션 목록

{code}python CAnalysisVlm.py [options]

분석 옵션:
  --inputdir           입력 JSON 디렉토리 (기본: json)
  --finalfile          최종 결과 파일 경로 (기본: data/final_data.json)
  --inputfileprefix    입력 파일 접두사 (기본: jira)
  --outputfileprefix   출력 파일 접두사 (기본: now)
  --reuse_rt                기존 분석 결과 재사용 (기본: False)
  --no_write_final          final_...

---

### [AGILEDEV-882] [CCR][2nd-Gen] 위반 티켓 Jira Comment 자동 등록 (--post_comment) + QCD_CCR_COMMENT_LOG DB 저장
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:37:17.000+0900
- **티켓 본문**: h2. 목적

Workflow/Matrix/Field 위반이 있는 활성 CCR 티켓에 Jira Comment를 자동 등록하고, 발송 이력을 QCD_CCR_COMMENT_LOG 테이블에 저장한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{post_jira_comment()}} 신규 함수 + {{main()}} 호출 블록

h2. 작업 내역

h3. 1. post_jira_comment(issue_key, violations_dict, jira_url, auth) 함수 구현
* Jira REST API: POST /rest/api/2/issue/{key}/comment
* auth: secure_info.py에서 인증 정보 로드

h3. 2. Comment 내용 자동 구성 (템플릿)

{code}[Gen2 Auto Check] CCR Shift-Left Activity 자동 검증 결과
=====================================================
검증 일시: {YYYY-MM-DD HH:MM}

⚠ [Workflow 위반]
  - {backward_transition 내용}
  - {skipped_status 내용}
  - {author_violation 내용}

⚠ [Shift-Left Matrix 미완성]
  - {row_name} / {col_name}: {violation_type} (기대: {expected}, 실제: {actual})

⚠ [필수 필드 누락]
  - {check_id} ({field_label}): {violation_reason...
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:20:46.000+0900] h2. ✅ 구현 완료 — Resolved (2026-03-18)

h3. 구현 내용

위반 티켓에 대한 Jira 필드 자동 업데이트 기능이 구현되어 있습니다.

*구현 방식:*  
원래 계획의 {{QCD_CCR_COMMENT_LOG}} DB 저장 없이, *필요 시 생성하여 사용하는 방식*으로 구현됨  
(검증 결과 텍스트는 {{final_data.json}}의 {{"jira_screening_detail_text"}} 키로 확인 가능)

h3. 구현 위치

*1. 위반 내용 텍스트 생성:*  
{{CCCRStatus.build_jira_screening_detail()}} — CCCRStatus.py L1317  
* CCR 분석 설명 URL 포함
* 대상 티켓 정보 (ID, 상태, 우선순위, 담당자)
* 스크리닝 점수 (Critical / Warning / Total)
* Critical Violations 목록 (check_name, point, v...

---

### [AGILEDEV-881] [CCR][2nd-Gen] 필수 필드 검증 (F1~F6) + QCD_CCR_FIELD_VIOLATIONS DB 저장 + ccr_10_Field_Validation.csv 출력
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:34:15.000+0900
- **티켓 본문**: h2. 목적

CCR 티켓의 6개 필수 필드를 status별 필수 시점 기준으로 검증하고 결과를 DB/CSV로 저장한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{work_func()}} 내 helper 함수 + {{main()}} 출력 블록

h2. 작업 내역

h3. 1. check_required_fields(ticket_data, current_status) 구현

|| CHECK_ID || customfield || 검증 조건 || 필수 시점 ||
| F1 | customfield_25346 | CR / Issue / SV 중 하나 | Open 이후 항상 |
| F2 | customfield_25345 | 비어있지 않아야 함 | Open 이후 항상 |
| F3 | customfield_25344 | 비어있지 않아야 함 | Open 이후 항상 |
| F4 | customfield_27073 + 27074 | 두 필드 모두 비어있지 않아야 함 | Analyzed 이후 |
| F5 | customfield_27077 | Gerrit URL 1개 이상 (http://vsgit.lge.com 또는 http://android-review.lge.com 패턴) | In Review 이후 |
| F6 | customfield_25711 | 비어있지 않아야 함 | Open 이후 항상 |
* 반환 dict: {field_valid: bool, field_violations: [{check_id, field_label, customfield_id, actual_value, violation_re...
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:01:15.000+0900] h2. 구현 현황 검토 결과 (2026-03-18) — In Progress 전환

h3. ✅ 구현된 내용
F0~F6 필드 검증 로직이 {{CCCRStatus.py}}에 완전히 구현되어 있습니다:

|| CHECK_ID || 함수명 || customfield || 필수 시점 || 위치 ||
| F0 | {{_check_field_f0_assignee()}} | assignee | 항상 | CCCRStatus.py L927 |
| F1 | {{_check_field_f1_ticket_type()}} | customfield_25346 | Open 이후 | CCCRStatus.py L952 |
| F2 | {{_check_field_f2_unit_leader()}} | customfield_25345 | Open 이후 | CCCRStatus.py L984 |
| F3 | {{_check_field_f3_feature_leader()}} | customfield_25344 | Open 이...
  - [2026-03-18T13:20:44.000+0900] h2. ✅ 구현 완료 — 목표 재정의 및 Resolved (2026-03-18)

h3. 구현 방식 변경

원래 계획: {{check_required_fields()}} 독립 함수 + {{QCD_CCR_FIELD_VIOLATIONS}} 별도 테이블 + {{ccr_10_Field_Validation.csv}}  
*실제 구현: {{CCCRStatus}} 클래스 내 F0~F6 메서드 완성 + {{QCD_CCR_READINESS.CONTEXT}}에 통합 저장, CSV 불필요*

h3. 구현 내용

*Field 검증 로직 ({{CCCRStatus.py}}):*

|| CHECK_ID || 함수 || customfield || 필수 시점 ||
| F0 | {{_check_field_f0_assignee()}} L927 | assignee | 항상 |
| F1 | {{_check_field_f1_ticket_type()}} L952 | customfield_25346 |...

---

### [AGILEDEV-880] [CCR][2nd-Gen] ccr_9_Matrix_Stage_Check.csv 출력 및 상태별 위반 집계
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:34:46.000+0900
- **티켓 본문**: h2. 목적

G2-04 Matrix 검증 결과를 CSV로 출력하고 상태별 위반 통계를 print한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{main()}} 집계/출력 블록

h2. 작업 내역
# {{QCD_CCR_GEN2_RESULT}}에 Matrix 관련 컬럼 저장:
** MATRIX_STAGE_OK, MATRIX_VIOLATION_COUNT
# {{ccr_9_Matrix_Stage_Check.csv}} 생성
** 컬럼: ISSUE_KEY, CURRENT_STATUS, MATRIX_STAGE_OK, VIOLATION_COUNT, VIOLATION_ROWS, VIOLATION_COLS, VIOLATION_TYPES
# print 출력: 상태별 Matrix 위반 집계 테이블 (status × 위반유형 cross-tab)
# {{--gen2}} 옵션 활성화 시에만 실행

h2. 선행 조건
* G2-04 (Matrix 검증 함수)

h2. 검증
* 상태별 집계 수치 수작업 확인 (샘플 10건)

h2. 참조
* 설계서: design_notes/gen2/README.md 섹션 7.3 Phase 4 — Story G2-05
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:01:13.000+0900] h2. 구현 현황 검토 결과 (2026-03-18)

h3. ❌ 미구현 항목 (Open 유지 사유)

이 티켓은 AGILEDEV-879 (Matrix 검증) 및 AGILEDEV-876 (DB Schema) 완료 후 작업 가능합니다.

*현재 미구현:*
# {{QCD_CCR_GEN2_RESULT}}에 MATRIX_STAGE_OK, MATRIX_VIOLATION_COUNT 저장 — 미구현
# {{ccr_9_Matrix_Stage_Check.csv}} 생성 — 미구현  
   (컬럼: ISSUE_KEY, CURRENT_STATUS, MATRIX_STAGE_OK, VIOLATION_COUNT, VIOLATION_ROWS, VIOLATION_COLS, VIOLATION_TYPES)
# 상태별 Matrix 위반 집계 cross-tab print 출력 — 미구현
# {{--gen2}} 옵션 가드 — 미구현

h3. 📌 선행 작업 필요
* AGILEDEV-876: DB Schema 구현
* AGI...
  - [2026-03-18T13:20:42.000+0900] h2. ✅ 목표 재정의 — Resolved (2026-03-18)

h3. 이 티켓은 구현 불필요

AGILEDEV-879에서 Matrix 검증 결과가 {{QCD_CCR_READINESS.STATUS_CONTEXT}}에 완전히 저장됨으로써, 별도 {{ccr_9_Matrix_Stage_Check.csv}} 생성은 불필요합니다.

*이유:*
* DB에 저장된 데이터로 필요 시 언제든지 조회/집계 가능
* CSV는 중복 산출물로 유지 비용 발생
* AGILEDEV-879가 이 티켓의 목표를 포함하여 완성됨

이 티켓은 AGILEDEV-879로 커버됩니다.

---

### [AGILEDEV-879] [CCR][2nd-Gen] Shift-Left Matrix 단계별 완성도 검증 (S3, S5) + QCD_CCR_MATRIX_VIOLATIONS DB 저장
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:35:15.000+0900
- **티켓 본문**: h2. 목적

현재 status에 따라 Shift-Left Matrix 각 셀의 기대값과 실제값을 비교하고 위반을 탐지한다.  
탐지된 위반 상세를 QCD_CCR_MATRIX_VIOLATIONS 테이블에 저장한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{work_func()}} 내 helper 함수

h2. 작업 내역

h3. 1. check_matrix_by_stage(matrix_parsed, current_status) 구현 — S3, S5
* matrix_parsed: 기존 parseJiraTable() 반환 dict (3행×3열) 재사용
* 상태별 기대 완성도 규칙:

|| 상태 || 요구사항분석(수행여부/근거Link/승인) || 설계리뷰(수행여부/근거Link/승인) || 자가검증(수행여부/근거Link/승인) ||
| Open | 빈칸/빈칸/빈칸 | 빈칸 | 빈칸 |
| Analyzed | O/URL/빈칸가능 | 빈칸 | 빈칸 |
| In-Progress | O/URL/O(CFR승인) | 빈칸 | 빈칸 |
| In Review | O/URL/O | O/URL/O | 빈칸 |
| Build Request 이후 | O/URL/O | O/URL/O | O/URL/O |
* 근거 Link 유효성 (S3): http://collab.lge.com 또는 http://jira.lge.com 패턴 포함 여부 정규식 검사
* 반환 dict: {matrix_stage_ok: bool, matrix_violations: [{row_name, col_name, expected, actual, v...
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T13:01:12.000+0900] h2. 구현 현황 검토 결과 (2026-03-18) — In Progress 전환

h3. ✅ 구현된 내용
Matrix 검증 로직이 {{CCCRStatus.py}}에 완전히 구현되어 있습니다:

|| 검증 단계 || 구현 함수 || 위치 ||
| Open | {{_check_open_matrix()}} | CCCRStatus.py L619 |
| Analyzed | {{_check_analyzed_matrix()}} | CCCRStatus.py L659 |
| In Progress | {{_check_in_progress_matrix()}} | CCCRStatus.py L694 |
| In Review | {{_check_in_review_matrix()}} | CCCRStatus.py L761 |
| Build Request 이후 | {{_check_build_request_matrix()}} | CCCRStatus.py L841 |

*검증 내용:*
* S3 (근거Link 유효성...
  - [2026-03-18T13:20:40.000+0900] h2. ✅ 구현 완료 — 목표 재정의 및 Resolved (2026-03-18)

h3. 구현 방식 변경

원래 계획: {{check_matrix_by_stage()}} 독립 함수 + {{QCD_CCR_MATRIX_VIOLATIONS}} 별도 테이블  
*실제 구현: {{CCCRStatus}} 클래스 내 상태별 메서드 + {{QCD_CCR_READINESS.STATUS_CONTEXT}}에 통합 저장*

h3. 구현 내용

*Matrix 검증 로직 ({{CCCRStatus.py}}):*
* {{_check_open_matrix()}} (L619): Open 상태 빈칸 확인
* {{_check_analyzed_matrix()}} (L659): 요구사항분석 수행여부/근거Link
* {{_check_in_progress_matrix()}} (L694): 승인(O) + CFR 작성자 검증
* {{_check_in_review_matrix()}} (L761): 요구사항분...

---

### [AGILEDEV-878] [CCR][2nd-Gen] Workflow 검증 결과 DB 저장 및 ccr_8_Workflow_Validation.csv 출력
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:35:41.000+0900
- **티켓 본문**: h2. 목적

G2-02에서 산출된 Workflow 검증 결과를 DB에 저장하고 CSV로 출력한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{main()}} 집계/출력 블록

h2. 작업 내역
# {{QCD_CCR_GEN2_RESULT}} 테이블에 Workflow 관련 컬럼 저장:
** WORKFLOW_VALID, WORKFLOW_BACKWARD_COUNT, WORKFLOW_SKIPPED_COUNT, WORKFLOW_AUTHOR_VIOLATION_CNT, WORKFLOW_LONG_STAY_COUNT
# {{QCD_CCR_WORKFLOW_TRANSITIONS}} 테이블에 전이 이력 저장 (1건당 N개 row):
** SEQ, FROM_STATUS, TO_STATUS, TRANSITION_DATE, TRANSITION_AUTHOR, DURATION_DAYS, IS_BACKWARD, IS_SKIPPED, IS_AUTHOR_VIOLATION, IS_LONG_STAY, IS_ZERO_STAY, NOTE
** 기존 row는 ISSUE_ID 기준 DELETE 후 재삽입 (재실행 안전)
# {{ccr_8_Workflow_Validation.csv}} 생성
** 컬럼: ISSUE_KEY, CURRENT_STATUS, WORKFLOW_VALID, BACKWARD_COUNT, SKIPPED_COUNT, AUTHOR_VIOLATION_CNT, LONG_STAY_COUNT, VIOLATION_SUMMARY
# print 출력: 전체 티켓 수, 위반 티켓 수, 위반 유형별 집계 (W...
- **작업 히스토리 (User Comments)**:
  - [2026-03-04T13:51:30.000+0900] comments를 추가했습니다. 메일 가나요?

기존 comments 수정
  - [2026-03-18T13:00:32.000+0900] h2. 구현 현황 검토 결과 (2026-03-18) — In Progress 전환

h3. ✅ 구현된 내용
Workflow 검증 결과 계산 자체는 완료되어 있습니다:
* {{CCCRStatus.py}}의 {{perform_workflow_validation()}} 호출 → {{v['current_status_workflow_validation_result']}}에 저장 (CAnalysisVlm.py L1298)
* {{workflow_checks}} (W1~W4 상세), {{overall_passed}}, {{total_violations}} 포함된 dict 형태로 생성

h3. ❌ 미구현 항목 (In Progress 전환 사유)

*선행 조건 미충족:*
* AGILEDEV-876 (DB Schema) 미완료로 인해 Gen2 테이블 없음

*DB 저장 미구현:*
* {{QCD_CCR_GEN2_RESULT}}에 WORKFLOW_VALID, WORKFLOW_BACKWARD_COUNT, ...
  - [2026-03-18T13:20:38.000+0900] h2. ✅ 구현 완료 — 목표 재정의 및 Resolved (2026-03-18)

h3. 구현 방식 변경

원래 계획: {{QCD_CCR_GEN2_RESULT}}, {{QCD_CCR_WORKFLOW_TRANSITIONS}} 별도 테이블 + {{ccr_8_Workflow_Validation.csv}}  
*실제 구현: {{QCD_CCR_READINESS.STATUS_CONTEXT}}에 통합 저장, CSV 불필요*

h3. 구현 내용

*Workflow 검증 결과 저장 위치:*
{{QCD_CCR_READINESS.STATUS_CONTEXT}} → {{current_status_workflow_validation_result}} 키

{code:json}{
  "workflow_checks": [
    {"check_id": "W1", "check_name": "Workflow Order", "passed": true/false, "details": [...]}...

---

### [AGILEDEV-877] [CCR][2nd-Gen] Workflow 상태 전이 순서 검증 (W1, W2) + Host 검증 (W3) + 체류 시간 분석 (W4)
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:36:08.000+0900
- **티켓 본문**: h2. 목적

{{CAnalysisVlm.py}}의 {{work_func()}} 내부에 Workflow 전이 관련 3개 검증 함수를 구현하고 결과를 티켓 dict에 저장한다.

h2. 구현 위치
* {{CAnalysisVlm.py}} — {{work_func()}} 내, 별도 helper 함수로 분리

h2. 작업 내역

h3. 1. check_workflow_transition(status_history) 구현 — W1, W2
* 정상 순서: Open → Analyzed → In-Progress → In Review → Build Request → Resolved → Closed
* Reject 예외: 어떤 status에서든 Closed (resolution=REJECTED) 전이는 위반 아님
* W1: 역방향 전이 탐지 (backward_transitions list 반환)
* W2: 필수 상태 건너뜀 탐지 (skipped_statuses list 반환)
* 반환 dict: {workflow_valid: bool, backward_transitions: [...], skipped_statuses: [...]}

h3. 2. check_workflow_author(status_history, ticket_data) 구현 — W3
* Analyzed → In-Progress: 전이 author가 CFR 필드(customfield_25349)와 일치하는지 확인
* In Review → Build Request: author가 Unit Leader(customfield_25345) 또는 Feature Leader...
- **작업 히스토리 (User Comments)**:
  - [2026-03-18T12:59:48.000+0900] h2. 구현 완료 (2026-03-18)

h3. ✅ 구현된 내용

*{{CCCRStatus.py}}에 W1~W4 모든 Workflow 검증 함수가 구현됨:*

|| 검증 ID || 함수명 || 설명 || 위치 ||
| W1 | {{check_workflow_order()}} | 역방향 전이 탐지 (backward_transitions) | CCCRStatus.py L1782 |
| W2 | {{check_workflow_skipped()}} | 필수 상태 건너뜀 탐지 (skipped_statuses) | CCCRStatus.py L1787 |
| W3 | {{check_workflow_author()}} | 상태 전이 작업자 검증 (CFR/UL/FL 역할) | CCCRStatus.py L1792 |
| W4 | {{check_workflow_duration()}} | 체류 시간 분석 (0일/30일 이상 이상치) | CCCRStatus.py L1895 |

*통...

---

### [AGILEDEV-876] [CCR][2nd-Gen] DB Schema 설계 및 마이그레이션 — QCD_CCR_GEN2_RESULT 외 4개 신규 테이블 + QCD_CCR_SCREENING_POINTS 컬럼 확장
- **상태**: Resolved | **최종 업데이트**: 2026-03-18T13:21:10.000+0900
- **티켓 본문**: h2. 목적

Gen2 분석 결과 저장을 위한 DB 스키마를 설계하고, CDataBase.py에 신규 테이블 Create/Alter DDL을 추가한다.

h2. 구현 위치
* {{CDataBase.py}}
* {{CAnalysisVlm.py}} (초기화 코드)

h2. 작업 내역
# {{QCD_CCR_GEN2_RESULT}} 테이블 CREATE (티켓별 Gen2 분석 요약 — 1티켓 = 1row)
** 컬럼: ISSUE_ID(PK), ISSUE_KEY, PROJECT_KEY, CURRENT_STATUS, RESOLUTION, TICKET_TYPE, UNIT_LEADER, FEATURE_LEADER, ASSIGNEE, APPLIED_PROJECT, CHANGE_SCOPE, CHANGE_DIFFICULTY, GERRIT_LINKS, CREATED_DATE, RESOLVED_DATE, CLOSED_DATE, SCREENING_POINT
** Gen2 검증 결과: WORKFLOW_VALID, WORKFLOW_BACKWARD_COUNT, WORKFLOW_SKIPPED_COUNT, WORKFLOW_AUTHOR_VIOLATION_CNT, WORKFLOW_LONG_STAY_COUNT
** Matrix 결과: MATRIX_STAGE_OK, MATRIX_VIOLATION_COUNT
** Field 결과: FIELD_VALID, FIELD_F1_PASS ~ FIELD_F6_PASS
** 메타: COMMENT_POSTED, COMMENT_POSTED_DATE, ANALYSIS_DATE, DB_ACTION, LAST_UPDATED
...
- **작업 히스토리 (User Comments)**:
  - [2026-03-05T15:33:18.000+0900] {noformat}

- Database Table
  - 7.2.1 QCD_CCR_GEN2_RESULT — 티켓별 Gen2 분석 요약
    - ticket당 1개이며 , 아래의 7.2.5 QCD_CCR_COMMENT_LOG ,  7.2.6 QCD_CCR_SCREENING_POINTS 을 포함한다.
    - history에서 status의 변경 내용만을 추적한다.
    - fields
      - unique : ISSUE_ID
      - ISSUE_ID
      - CREATED_DATE
      - UPDATED_DATE
      - RESOLVED_DATE
      - STATUS_DATE
      - STATUS
      - STATUS_HISTORY
      - ASSIGNEE
      - ASSIGNEE_UNIT
      - SCREENING_POINT
      - STATUS_HISTORY
      - IS...
  - [2026-03-18T12:59:41.000+0900] h2. 구현 현황 검토 결과 (2026-03-18)

h3. ✅ 구현된 내용
* {{CCCRStatus.py}} 및 {{CAnalysisVlm.py}}에서 Gen2 분석 로직(Workflow/Matrix/Field 검증) 자체는 구현됨
* {{QCD_CCR_SCREENING_POINTS}} 테이블 조회/저장 로직은 기존대로 동작 중
* {{QCD_CCR_READINESS}} 테이블 저장 로직 구현됨

h3. ❌ 미구현 항목 (In Progress 유지 사유)

*CDataBase.py에 신규 Gen2 테이블이 생성되지 않음:*
# {{QCD_CCR_GEN2_RESULT}} 테이블 CREATE — 미구현
# {{QCD_CCR_WORKFLOW_TRANSITIONS}} 테이블 CREATE — 미구현
# {{QCD_CCR_MATRIX_VIOLATIONS}} 테이블 CREATE — 미구현
# {{QCD_CCR_FIELD_VIOLATIONS}} 테이블 CREATE — 미구현
# {{QCD_CC...
  - [2026-03-18T13:20:35.000+0900] h2. ✅ 구현 완료 — 목표 재정의 및 Resolved (2026-03-18)

h3. 구현 방식 변경 (원래 계획 vs 실제 구현)

원래 계획: Gen2 전용 5개 신규 테이블 생성
*실제 구현: 기존 2개 테이블로 모든 Gen2 데이터 통합 처리*

h3. 최종 DB 구조 (2개 테이블)

|| 테이블명 || 역할 || 저장 내용 ||
| {{QCD_CCR_SCREENING_POINTS}} | 스크리닝 점수 | ISSUE_ID, SNAPDATE, CONTEXT, SCREENING_POINT, ASSIGNEE, STATUS 등 |
| {{QCD_CCR_READINESS}} | Gen2 분석 전체 | ISSUE_ID, CONTEXT (ccr_fields 전체), STATUS_CONTEXT (current_status* 검증 결과 전체), SCREENING_CONTEXT (screening* 점수 데이터) |

h3. 저장 내용 상세

*QCD_CCR_READINESS.CONTEX...

---

### [AGILEDEV-875] [ticketsage] connectWide filter변경으로 인해 5000 개 정도 늘어나는 데이터 처리
- **상태**: Resolved | **최종 업데이트**: 2026-02-27T14:27:42.000+0900
- **티켓 본문**: summary는 처리 (SUMMARY)
jira test에서의 처리 (VECTOR , RAG)
에 영향을 미침

너무 많이 동작하는 것에 대한 에러 처리도 해야 할 것으로 생각됨.
현재는 6시간의 limitation을 걸어두었음.

추가적으로 2000 건이 넘기는 건에 대해서는 메일 error를 따로 보내는 것으로 설정해야 할 것으로 보임.  초기에 전체수를 count해야 할 것임. (? : 추후 고려)
- **작업 히스토리 (User Comments)**:
  - [2026-02-26T14:22:48.000+0900] summary (SUMMARY)는 5000 건의 데이터 처리를 해야함. VDA(VS Defect Agent)에서 3 line summary를 사용하기 때문임.

vector , rag의 경우는 5000 건의 데이터를 처리하지 않음.  여기 5000 건에는 기존의 것에서 update된 것들도 포함되여져있음.
- 400 개 정도의 기존 vector , rag data를 지워주게 됨.
- 5000 건이 update되는 것을 미리 알았을 경우에는 방지 할수 있는 방법이 있었음. (현재는 모두 update 가 된 것으로   그냥 해당 날짜의 데이터를 지우는 것 밖에 방법이 없음)
-- 추후에는 filter등이 변경되거나,
-- 사전에 미리 check를 하여 변경량이 1000 건 이상인 경우는 이상한 날로 판별하여 , 동작을 중단시키는 것이 필요함.  (이번에 코드를 추가해 두어야 할 것임.)
-- 이번 경우 동작만 20시간으로 한시적인 동작제한 시간을 변경해야함. (기본 6시간이...
  - [2026-02-26T16:15:44.000+0900] {noformat}
 $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
 main  4?  16:15  tiger02  ~/code/crontab/ticketsage/summary  $  git log -1
commit e6af994b05ef13c4274fa11826b4974f9c664450 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Thu Feb 26 15:50:30 2026 +0900

    [AGILEDEV-875] [ticketsage][summary,jira_test] option추가(max_runtime_hours,batch_start_count,batch_...
  - [2026-02-26T18:12:26.000+0900] SELECT *
FROM QCD_DL_ISSUE_FROM_MONGODB
WHERE PROJECT_CODE = 'PGZ22PGZT6R00'
  AND SOURCE = 'DQA'
  AND SNAPDATE = '2026-02-24'
  AND CUSTOM1 != 'HMG'

이것으로 조정 가능한지 살펴볼 것:  
그냥 처음부터 처리해야 하는 것만 SQL로 받는 것이 제일 좋다.
  - [2026-02-27T14:27:20.000+0900] DB QUERY를 다음과 같이 변경함으로써 , 코드 상에서는 2026-02-24 에 대한 처리를 할 필요가 없습니다.

2024-02-27 : db_query.sql에 2026-02-24에 대한 조건을 추가함으로 인해서 사전에 filtering을 함.
$  cat db_query.sql 
{code:sql}
SELECT A.*, B.DESCRIPTION, B.COMMENTS, B.SNAPDATE AS DL_ADDITIONAL_SNAPDATE
FROM CRAWLER.QCD_DL_ISSUE_FROM_MONGODB A
JOIN CRAWLER.QCD_DL_ISSUE_ADDITIONAL_INFO B ON A.ISSUE_ID = B.ISSUE_ID
WHERE ASSIGNEE  'no_assigned' 
  AND TRACKER_ID = 'HMCCW' 
  AND DEV_STATUS = 'closed' 
  AND (A.PROJECT_CODE LIKE '%PGZ22PGZT6R...

---

### [AGILEDEV-872] [CCR] CCR Ready Screening Design
- **상태**: Resolved | **최종 업데이트**: 2026-02-27T13:43:35.000+0900
- **티켓 본문**: 기능 정의 : 단계별 정의
DB 생성 : 무엇을 위한  field들인가?  어떤 데이터를 모을 것인가? 어떤 DB가 되어야 효과적인가?  table이 여러개이면 서간의 relation은 어떻게? trender에 사용할 것은?

기준 : CFL , UNIT
- **작업 히스토리 (User Comments)**:
  - [2026-02-27T13:43:35.000+0900] 현재는 jira/confluence에대한 MCP setting이 완료된 상태 입니다.  
claude-sonnet-4.6 (medium) (1x)
- MCP setup in linux : http://mod.lge.com/hub/cheoljoo.lee/publish/-/blob/main/lge/linux-copilot-cli-setup-korean.md?ref_type=heads
  windows : https://github.com/cheoljoo/mcp_copilot/blob/main/docs/windows-copilot-vscode-setup-korean.md
- 기본 instruction 추가
$  cat ~/.copilot/copilot-instructions.md 
collab.lge.com 에 접근할 때는 항상 mcp-atlassian의 Confluence 도구를 사용하세요.

prompt1:
ccr_part1.png  ccr_part2.png  ccr_...

---

### [AGILEDEV-867] [Hexa Index LLM 이용한 자동 분석] copilot cli를 이용한 claude 분석
- **상태**: Resolved | **최종 업데이트**: 2026-02-27T15:01:56.000+0900
- **티켓 본문**: http://collab.lge.com/main/pages/viewpage.action?pageId=3559587543


{noformat}
# Hexa Index (LLM 이용한 자동분석)
- 2/24
- 회의록
   - 국내 connectWide filter 변경
- action items
   - trender에 export page 밑에 project / 구간 / 여러가지 값으로 hexa index 값을 json 과 csv 로 얻는 기능 추가 (김하석C)
   - 위의 내용이 trender에 반영되기 전 connectWide 에 대한 hexa index 값 공유 /  ccIC와 connectWide에 대한 issue input flow 관련 내용 공유 (이상재S)
   - ccIC와 connectWide에 대한 issue input flow 관련 내용 공유된 내용을 기반으로 issue input prediction flow 결과 (성환혁C)
   - export한 내용으로 copilot cli를 통한 분석 진행 (공통)
   - copilot cli 환경 구성 방법 공유 (이철주C)
       - MCP를 이용한 collab의 내용과 같이 작성해 달라는 결과
{noformat}

   - export한 내용으로 copilot cli를 통한 분석 진행 (공통)
- **작업 히스토리 (User Comments)**:
  - [2026-02-25T12:08:49.000+0900] project와 unit 에 대한 json / csv 파일 기다림.
  - [2026-02-26T14:30:51.000+0900] 결과 : http://collab.lge.com/main/pages/viewpage.action?pageId=3564258412#%ED%94%84%EB%A1%9C%EC%A0%9D%ED%8A%B8%EC%A0%90%EA%B2%80%EB%8C%80%EB%B9%84%ED%94%84%EB%A1%AC%ED%94%84%ED%8C%85-2016651820
 !screenshot-1.png!

---

### [AGILEDEV-866] [Hexa Index LLM 이용한 자동 분석] copilot cli 환경 및 MCP 사용법 구성
- **상태**: Resolved | **최종 업데이트**: 2026-02-25T13:21:03.000+0900
- **티켓 본문**: {noformat}
# Hexa Index (LLM 이용한 자동분석)
- 2/24
- 회의록
   - 국내 connectWide filter 변경
- action items
   - trender에 export page 밑에 project / 구간 / 여러가지 값으로 hexa index 값을 json 과 csv 로 얻는 기능 추가 (김하석C)
   - 위의 내용이 trender에 반영되기 전 connectWide 에 대한 hexa index 값 공유 /  ccIC와 connectWide에 대한 issue input flow 관련 내용 공유 (이상재S)
   - ccIC와 connectWide에 대한 issue input flow 관련 내용 공유된 내용을 기반으로 issue input prediction flow 결과 (성환혁C)
   - export한 내용으로 copilot cli를 통한 분석 진행 (공통)
   - copilot cli 환경 구성 방법 공유 (이철주C)
       - MCP를 이용한 collab의 내용과 같이 작성해 달라는 결과
{noformat}

   - copilot cli 환경 구성 방법 공유 (이철주C)
       - MCP를 이용한 collab의 내용과 같이 작성해 달라는 결과
- **작업 히스토리 (User Comments)**:
  - [2026-02-25T11:50:11.000+0900] https://github.com/cheoljoo/mcp_copilot/blob/main/docs/linux-copilot-cli-setup-korean.md
  - [2026-02-25T11:51:32.000+0900] 자료 (특히 , prompt) http://collab.lge.com/main/pages/viewpage.action?pageId=3564258412  에 모아둠
 !image-2026-02-25-12-07-44-787.png!

---

### [AGILEDEV-865] [ticketsage][summary]  ticket처리시 keyword에 찾아서 ticket의 category화를 시킬 것
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:17:23.000+0900
- **티켓 본문**: # VDA 미팅
- 2/24
- 회의록
   - Crash 관련 LLM 문의하여 DB로 (ticketsage/summary에 LLM query에 crash관련 내용 추가) (이철주C)
*   - tcietsage/summary에서 ticket처리시 keyword에 찾아서 ticket의 category화를 시킬 것 (이철주C)*

여기서 중요한 부분은  keyword에서 위의 LLM에서 문의한 내용으로 추가가 되는 부분이 있다면 , 이 내용을 keyword 들을 자동/승인으로 추가하도록 하는 기능 추가 할 것
- **작업 히스토리 (User Comments)**:
  - [2026-02-26T16:48:26.000+0900] leader와 DB field를 상의하여 추가해야함.
먼저 LLM query에 추가함. http://jira.lge.com/issue/browse/AGILEDEV-864

---

### [AGILEDEV-864] [ticketsage] LLM_SUMMARY 관련 prompt 추가 : crash / categorize 기능 추가
- **상태**: Resolved | **최종 업데이트**: 2026-03-12T08:37:50.000+0900
- **티켓 본문**: # VDA 미팅
- 2/24
- 회의록
   - Crash 관련 LLM 문의하여 DB로 (ticketsage/summary에 LLM query에 crash관련 내용 추가) (이철주C)
   - tcietsage/summary에서 ticket처리시 keyword에 찾아서 ticket의 category화를 시킬 것 (이철주C)

# connectWide 팀과 ticketsage 관련 적용 회의
- 2/24
- 참석자 : 김영삼 , 하진태 , 김현민 , 이상재 , 이철주
- 회의록
   - 별도의 field를 생성하여 comments를 달기로함.  tab (ex. HKMC tab)의 형식으로 만들면 화면을 깨지도 않고 , 많이 적어도 됨.
      - 내용에 대해서는 assignee / componets 를 같이 적어주는 것이 도움이 된다고함.
      - connectWide 팀에서 2개의 fields 생성 후 해당 field에 결과 넣어주기로함. (접는 것보다 더 효과적일 것으로 생각됨)
   - 향후 진행 안 논의
      - 현대차 issue인지 3rd party issue인지 구별해 달라. (field가 정해져있는 것 같음)
*         - 자사 ticket이 아니어도 모든 ticket에 대해서 분류(categorize) 가 되었으면 한다. 이유는 system UI등은 우리에게도 영향이 있는 issue들이다. 예로 VR이 사고 많이 발생하는데 서로가 봐야 하는 경우가 많다.*
- **작업 히스토리 (User Comments)**:
  - [2026-02-26T16:46:50.000+0900] prompt 추가 :
+"Crash_Related": {{
+    "Crash_Keywords": [
+        "crash", "abort", "exception", "hang", "ANR", "segfault", "null pointer", "nullptr",
+        "fatal", "watchdog", "reboot", "panic", "freeze", "deadlock", "stack overflow",
+        "out of memory", "OOM", "assertion failed", "signal", "SIGSEGV", "SIGABRT",
+        "force close", "tombstone", "kernel panic", "sudden restart", "unexpected shutdown",
+        "unhandled exception", "core dump", "bus error", "illegal instru...
  - [2026-02-27T10:15:24.000+0900] 잘 생성됨을 확인함.
결과:

{code:python}
    "Crash_Related": {
      "Crash_Keywords": [
        "crash",
        "abort",
        "exception",
        "hang",
        "ANR",
        "segfault",
        "null pointer",
        "nullptr",
        "fatal",
        "watchdog",
        "reboot",
        "panic",
        "freeze",
        "deadlock",
        "stack overflow",
        "out of memory",
        "OOM",
        "assertion failed",
        "signal",
        "SIGSEGV",
    ...

---

### [AGILEDEV-858] connectWide 팀과 회의 (ticketsage 기능추가 여부)
- **상태**: Resolved | **최종 업데이트**: 2026-02-25T11:45:43.000+0900
- **티켓 본문**: connectWide 팀과 회의 (ticketsage 기능추가 여부)
- **작업 히스토리 (User Comments)**:
  - [2026-02-25T06:10:04.000+0900] {noformat}
# connectWide 팀과 ticketsage 관련 적용 회의
- 2/24
- 참석자 : 김영삼 , 하진태 , 김현민 , 이상재 , 이철주
- 회의록
   - 별도의 field를 생성하여 comments를 달기로함.  tab (ex. HKMC tab)의 형식으로 만들면 화면을 깨지도 않고 , 많이 적어도 됨.
      - 내용에 대해서는 assignee / componets 를 같이 적어주는 것이 도움이 된다고함.
      - connectWide 팀에서 2개의 fields 생성 후 해당 field에 결과 넣어주기로함. (접는 것보다 더 효과적일 것으로 생각됨)
   - 향후 진행 안 논의
      - 현대차 issue인지 3rd party issue인지 구별해 달라. (field가 정해져있는 것 같음)
      - CQIW의 모든 내용을 받고 있다. (1월말부터)
         - 고객사의 이슈도 우리에게 어떤 용향을 미치는지 알...

---

### [AGILEDEV-852] 2026-02 sprint report 작성
- **상태**: Resolved | **최종 업데이트**: 2026-02-24T13:12:34.000+0900
- **티켓 본문**: sprint report 작성
- spot
- due 변경 ...
- 추가적으로 주의요하는 점1
- **작업 히스토리 (User Comments)**:
  - [2026-02-23T11:58:59.000+0900] http://jira.lge.com/issue/secure/RapidBoard.jspa?rapidView=42133&view=reporting&chart=sprintRetrospective&sprint=85691
  - [2026-02-24T13:12:15.000+0900] 2월 Sprint 요약 
sprint report by Atlassian : http://jira.lge.com/issue/secure/RapidBoard.jspa?rapidView=42133&view=reporting&chart=sprintRetrospective&sprint=85691
요약 : 2026-02-03 sprint
- 대부분 story point를 입력하며 작업중 (잘한점)
- Epic 을 지정하지 않고 작업하는게 많음.  (미진한점 : 아직 Epic에 대해서 분류를 꼭 해야 하는 이유는 모르겠음)
- Sport ticket의 비율이 전달 대비 증가 :  계획하지 않았던 ticket이 story point기준으로 34% 이며 , ticket 수 기준으로는 45%임.   (1월 : 27% Total-SP: 108.1)
다음 스프린트를 위해서 다음 사항들에 대해서 생각해봐주십시요.
-- story point을 입력하지 않은 부분들이 약간 보임
-- 2026-...

---

### [AGILEDEV-851] [LONG-TERM] LGEP 비밀번호 바뀔때 확인 사항들
- **상태**: Holding | **최종 업데이트**: 2026-05-18T15:50:44.000+0900
- **티켓 본문**: 3개월마다 LGEP 비밀번호 바뀌면 해야 할 일
1. crontab 의 mysetting.py 와 같은 비밀번호 넣는 부분 변경
2. teams 비밀번호 변경  및 이에 대해서 pyautogui의 노트북의 용역task 에 대한 init web에 대한 비밀번호 변경

---

### [AGILEDEV-843] fastapi를 이용한 QCD_SAGE_LLM_QUERY access 가능한 RESTAPI server 만들기-pvs_crawler_rest_api에 적용
- **상태**: Resolved | **최종 업데이트**: 2026-04-17T14:22:40.000+0900
- **티켓 본문**: fastapi를 이용한 QCD_SAGE_LLM_QUERY access 가능한 RESTAPI server 만들기 : 
 # [pvs_crawler_rest_api|http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_crawler_rest_api/browse] 에 적용

 

시스템에서 동작하고 있으니 crontab들을 보면 동작시간을 알 수 있다.
- **작업 히스토리 (User Comments)**:
  - [2026-02-11T13:21:08.000+0900] !image-2026-02-11-13-20-21-865.png!

!image-2026-02-11-13-20-59-313.png!
  - [2026-04-09T11:21:22.000+0900] 추가 기능으로 일반적으로 만들어야 한다. 
1. 승인된 DB table에 대해서는 승인해준 field명에 대해서 ...
2. help를 주어 어떻게 가져올수 있는지를 알려준다.
3. 조건에 대해서 넣어주면 쉽게 가져올수 있게 ...
4. SQL을 주면 그것에 대해서 return도 해주도록하는 것 (보안을 조금 더 생각해야하고 help에는 숨김)
  - [2026-04-14T14:35:26.000+0900] {noformat}
$  git remote -v
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler_rest_api.git (fetch)
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler_rest_api.git (push)
{noformat}


{noformat}
$  git log -6
commit 984318e601ba9b60bff80013e7846d4ee7f3c91e (HEAD -> master, origin/master, origin/HEAD)
Author: charles.lee 
Date:   Tue Apr 14 10:38:42 2026 +0900

    fastapi : example 추가

commit dae33e675b9642503defd4f813d9a87342ffc87e
Author: charles.lee 
Date:   Tue Apr 1...
  - [2026-04-17T14:22:40.000+0900] test 모두 완료

http://10.158.15.134:8000/docs

문서 : http://collab.lge.com/main/pages/viewpage.action?pageId=3618594627

---

### [AGILEDEV-840] fastapi를 이용한 QCD_SAGE_LLM_QUERY access 가능한 fast MCP 만들기
- **상태**: Open | **최종 업데이트**: 2026-04-23T15:19:45.000+0900
- **티켓 본문**: MCP로 copilot에서 다음의 query를 하면 
값들이 나오게 해야 한다.

fastapi_mcp_for_llm_query/MCP_SETUP_GUIDE.md 을 참조.
- **작업 히스토리 (User Comments)**:
  - [2026-02-13T10:28:37.000+0900] {noformat}
# MCP 서버 및 Copilot CLI 연동 가이드

## MCP 서버 환경 및 구성
- MCP 서버: stdio 기반 Python 서버 (`mcp/main.py`)
- Python 가상환경: `.venv` (uv, tiktoken 등 의존성 설치)
- DB 접근: summary/ticketsage_llm_summary.py 등에서 직접 처리
- MCP config: Linux 환경에서 Copilot CLI가 사용하는 설정 파일

## MCP 서버 실행 예시
```sh
# 가상환경 활성화 (uv 또는 venv)
source .venv/bin/activate

# MCP 서버 직접 실행
PYTHONPATH=/data01/cheoljoo.lee/code/ticketsage DEFAULT_GPT_MODEL=gpt-4o \
  .venv/bin/python /data01/cheoljoo.lee/code/ticketsage/mcp/main.p...
  - [2026-02-13T10:30:18.000+0900] {noformat}
$  git remote -v
origin http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)

$  git log -1
commit c4813e06650a9ed95ce50d5f6887e6ffda5fb78c (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Wed Feb 11 22:26:09 2026 +0900

    add MCP
{noformat}

---

### [AGILEDEV-838] [ticketsage][summary] 최대 6시간 동작으로 설정 & QCD_SAGE_LLM_QUERY: CONTEXT를 new_style로 정정
- **상태**: Resolved | **최종 업데이트**: 2026-02-24T08:39:49.000+0900
- **티켓 본문**: [ticketsage][summary] 최대 6시간 동작으로 설정 & QCD_SAGE_LLM_QUERY: CONTEXT를 new_style로 정정

* summary/check_emoji.py : emoji를 지우고 , check하여 CONTEXT를 update할 것이 무엇인지 판단.
* summary/update_context.py : emoji를 지운 상태로 CONTEXT생성
- **작업 히스토리 (User Comments)**:
  - [2026-02-09T16:16:52.000+0900] {noformat}
 ~/code/ticketsage/summary  $  git remote -v
\origin http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)
 16:16  main  29?  lotto  ~/code/ticketsage/summary  $  git log -1
commit 7a9b3f83e1d44c30899f9f3852e1c17a6bb5c404 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Mon Feb 9 16:16:03 2026 +0900

    [AGILEDEV-838] [ticketsage][summary] 최대 6시간 동작으로 설정 & QCD_SAGE_LLM_QUERY: CONTEXT를...

---

### [AGILEDEV-833] fastapi를 이용한 QCD_SAGE_LLM_QUERY access 가능한 RESTAPI server 만들기
- **상태**: Resolved | **최종 업데이트**: 2026-04-14T14:34:32.000+0900
- **티켓 본문**: fastapi를 이용한 QCD_SAGE_LLM_QUERY access 가능한 RESTAPI server 만들기

목적 : Defect Agent web 에서 3 line summary를 접근하려 한다. 바로 mySQL db를 접근하는 것이 아닌 , REST API Server를 통해서 접근할때 사용하려 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-02-10T13:50:33.000+0900] FASTAPI 구축 완료 : http://tiger02.lge.com:8000/api/llm_summary/HMCCW-29178
다음과 같이 return

{code:python}
{"issue_id":"HMCCW-29178","model":"gpt-4o","llm_summary":"{\"prompt_ver\": 0.001, \"prompt_file\": \"ticket_sage_summary.v0.001.prompt\", \"llm\": {\"issue_id\": \"vlm=HMCCW-29178\", \"Assignee\": \"sangkyu.lim\", \"Problem Analysis\": {\"Specific Issue or Bug\": \"하이패스 X1 화면에서 사용 패턴 진입 후 그래프 하단 좌우 스크롤이 가능하지만, 결제 이력 진입 후에는 하단 좌우 스크롤이 불가능한 문제.\", \"Symptoms and Impact\": \"사용자가 결제 이력 화면에서 그래프 ...
  - [2026-02-11T09:10:21.000+0900] 여러개의 ticket에 대해서도 문의 가능하게 함.

다음 3가지 방식 참조
 * [http://lotto645.lge.com:8000/api/llm_summary/HMCCW-29178]
 * [http://lotto645.lge.com:8000/api/llm_summaries?issue_ids=HMCCW-29178,HMCCW-25118,HMCCW-10|http://lotto645.lge.com:8000/api/llm_summaries?issue_ids=HMCCW-29178,HMCCW-25118,HMCCW-10&model=gpt-4o]
 * [http://lotto645.lge.com:8000/api/llm_summaries?issue_ids=HMCCW-29178,HMCCW-25118,HMCCW-10&model=gpt-4o]

---

### [AGILEDEV-832] DNS resolver 우회 코드 : {'code': '403', 'message': 'Public access is disabled. Please configure private endpoint.'}
- **상태**: Resolved | **최종 업데이트**: 2026-02-24T08:39:49.000+0900
- **티켓 본문**: DNS resolver 우회 코드 : {'code': '403', 'message': 'Public access is disabled. Please configure private endpoint.'}
- **작업 히스토리 (User Comments)**:
  - [2026-02-06T17:12:05.000+0900] $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)

안의 
summary/db_all.py의 query_llm_with_refinement 부분을 참조

{noformat}
                # Custom DNS resolver to bypass /etc/hosts without root access
                # Maps vs-sw.openai.azure.com to private endpoint IP 10.182.188.50
{noformat}

---

### [AGILEDEV-828] [Defect Agent] 운영 검증 자동화 업그레이드 
- **상태**: Resolved | **최종 업데이트**: 2026-03-04T10:01:33.000+0900
- **티켓 본문**: 이철주 책임님 아래 요청 사항 검토 부탁드립니다.

티켓 설명 :
pvs_crawler 의 defect_lib.py 에 있는 defect_agent_service_check() 함수를 업그레드
이 함수는 매일 아침 defect agent 에 로그인해서 전날 Open 상태인 이슈의 Summary 를 사용하여 20번의 무작위 검색을 실시하고 시간을 측정하는 용도로 제작하였습니다.

초기에 시간이 너무 오래걸리는 이슈가 있어 메일 시간을 체크하기 위해 만들었고 대충 만들어서 많은걸 확인하기 어려운 상태입니다.

요청 사항 : 
- 무작위 20번 검색결과에서 좀더 많은 것을 확인하기 쉬운형태로 메일로 보내도록....
1. 시간 체크는 여전히 필요 (각각의 검색 시간, 20회 검색 시간의 평균)
2. 검색시 결과의 갯수 체크
3. 검색결과의 json 형태 오류 없는지 체크 (최근에 Token 이 잘려 Json 형태가 온전히 넘어오지 못하는 이슈가 있어서 이거 체크하는 용도.)
4. 검색쿼리와 검색결과의 제목들만 메일로 깔끔하게 보내기... (지금은 결과 전체를 복붙...)
5. 결과 전체는 첨부파일로 첨부.....
6. 결과는 저를 포함해서 기영책임님, 철주 책임님, 오책임님까지 4명이 전부 받을수 있도록 추가.
- **작업 히스토리 (User Comments)**:
  - [2026-02-23T14:22:58.000+0900] {noformat}
$  git remote -v
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (fetch)
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (push)

$  git log -1
commit 8c55b16b1282b7dbc7f73d385120092da59da22f (HEAD -> master, origin/master, origin/HEAD)
Author: charles.lee 
Date:   Mon Feb 23 13:51:33 2026 +0900

    [AGILEDEV-828] [Defect Agent] 운영 검증 자동화 업그레이드
    
    - ISSUE_ID information 추가
    - send html table as result
{noformat}

---

### [AGILEDEV-827] gerrit MCP에 source / modified file / diff 를 받는 기능 contribution
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:32:09.000+0900
- **티켓 본문**: gerrit MCP에 source / modified file / diff 를 받는 기능 contribution

Gerrit 코드리뷰 서버. 코드 변경 이력, 리뷰 자동화 등

https://github.com/cayirtepeomer/gerrit-code-review-mcp
- **작업 히스토리 (User Comments)**:
  - [2026-04-09T11:32:09.000+0900] 필요치 않음.

---

### [AGILEDEV-826] [ccr] trender에서 사용할 DB (AHC)
- **상태**: Resolved | **최종 업데이트**: 2026-05-13T10:22:10.000+0900
- **티켓 본문**: trender에는 개발자들에게 유용한 정보로 넣어주어야 한다. 
CCR Ready Screening의 경우는 expert unit 인원들에게 필요한 것을 처리해주어야함.

expert unit에 필요한 일을 처리해주면서 , 그때 모인 reject 등의 자료를 가지고 trender DB를 만들면 좋을 듯!
- **작업 히스토리 (User Comments)**:
  - [2026-04-21T16:45:38.000+0900] CCR_AHC 라는 table을 만들어서 , 아래의 field들의 값을 채우고 있으면 될까요?
| who | org | belong | partner | department  | snapdate | created | resolved | issue_id | type(assign, comments, status change, approval | count
 
created or resolved date로 어느 조직이 누가 CCR review를 했는지에 대한 통계를 낼 것으로 생각됩니다.

-----------------------

근데 몇몇 DB 칼럼 이름은 기존 db와 통일 시키는 것은 어떨가요? 
ex) who --> assignee_name  or email, department --> Unit, 
-> 이름은 바꾸어야죠.. 모두 대문자이고 다른 곳에서 아용하는 것 좋습니다.    찾아보고 그렇게 바꾸도록 하겠습니다. 
 
그리고 type는 각각 활동 별로 칼...
  - [2026-04-22T15:12:18.000+0900] data/ 밑에서 ccr_ahc.py 를 만들어 처리하는 것으로 하겠다. input으로 받아들이는 final*.json으로 부터 처리하는 것으로 한다. 

final*.json에 대해서는 다루는 것에따라 다를 수 있으니 , 이 부분은 Makefile에 2가지 경우에 대해서 처리하게 하면 될 것으로 보인다. 
 # data/ccr 은 crontab의 경우 일반적으로 2일치의 처리가 되게 된다.  이것에 대한 CAnalysisVlm.py를 한 경우인 final_data.json 과
 # 2026-01-01로부터 gather한 data/review 에 대한 결과를 분석한 final_review_data.json 이 존재한다. 

1,2 의 경우를 받아서 각기 처리하게 하면 될 것이다.
  - [2026-04-22T15:13:00.000+0900] QCD_CCR_AHC table

NO
ISSUE_ID   30
USER_ID  100
ORG   500
BELONG   100
PARTER   500
DEPARTMENT   500
SNAPDATE   date
CREATED_DATE   date
RESOLVED_DATE  date
COUNT_ASSIGN   int
COUNT_COMMENT  int
COUNT_STATUS_CHANGE int
COUNT_APPROVAL int
  - [2026-04-22T16:11:33.000+0900] prompt:
{noformat}
ccr_ahc.py 의 요구사항
참조할 내용은 final_review.py 이다.
--input 으로 받은 json file에는 final_data.json 과 같은 정보가 들어가 있다.  --input 의 default 값은 ./final_data.json 이다.
final_review.py 코드 중에서 다음을 만들기 위한 부분을 뽑아내면 됩니다. 
- `monthly_person_review_summary.csv`
    - 월/사람/조직 기준 상세 통계입니다.
    - 포함 항목: `department`, `ticket_count`, `assignee_ticket_count`, `comments_count`, `same_team_comments_count`, `cross_team_comments_count`, `statusChanger_count`, `cfr_count`, `unitLeader_count`, `shiftLeftA...
  - [2026-04-22T16:16:53.000+0900] {noformat}
$  git log -1
commit 1107cdc510b70bc02bc283bbf7d57e70c229f740 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed Apr 22 16:14:55 2026 +0900

    [AGILEDEV-826] Add ccr_ahc.py for QCD_CCR_AHC DB sync and Makefile targets
    
    - `data/ccr_ahc.py` 신규 작성:
      - `final_data.json`을 읽어 (ISSUE_ID, USER_ID) 기준으로
        `QCD_CCR_AHC` 테이블에 ADD / UPDATE / DELETE 반영
      - `final_review.py`의 사람 추출 로직(extract_people, normalize_person 등) 재활용
      - user_hi...
  - [2026-04-23T11:06:45.000+0900] 서비스 시나리오.
1. 일단 2026-01-01 부터 내용을 받아서 해당 내용데 대한 QCD_CCR_AHC에 값을 채워야 한다.  (데이터가 없으니 한번만)
    ccr/make reviewer   -> ccr/data/make reviewer-ahc 까지도 call됨.
    이때 reviewer-ahc 에서는 final_reviewer_data.json을 가지고 처리를 한다.  해당 data로 DB를 채워넣게 된다.
2. 매일 ccr을  crontab에서 돌린다. 이 data에서 읽는 값을 QCD_CCR_AHC에 updat해야한다. (매일)
    이때 만들어지는 final_data.json을 가지고 QCD_CCR_AHC를 udpate한다.
이렇게 하면 모두 처리 완료될 것으로 생각됨.


{noformat}
$  git log -1
commit c55255b82c27c493ed76b6b42cf24c91a9f26952 (HEAD -> main, origin/...
  - [2026-04-23T15:14:32.000+0900] 위 comments의 1번에 대한 실행과 DB 삽입은 잘되어진 것을 확인함. (1번)
4/24 에 log와 DB를 보고 제대로 crontab daily의 내용이 반영되는지 확인을 해야 한다. (2번)
  - [2026-04-24T08:49:26.000+0900] [~haseok.kim] 님 ,   trender DB 의 QCD_CCR_AHC table 값 확인 부탁드립니다.
2026-01-01 이후의 것은 모두 포함되어져있습니다.,     (이전의 것도 일부는 있습니다.)
문제가 있는 것은 의견주시고 ,  추가해야 할 것도 알려주세요. 

매일 새벽에 add / update / delete 될 예정입니다.  기존 내용에서 comments를 delete했다던지 , 담당자가 바뀌는 경우 등..
  - [2026-05-08T11:24:24.000+0900] 추가 요청 from 김하석 책임님 , 
ASSIGNEE_NAME 을 추가해달라.
  - [2026-05-08T14:09:24.000+0900] SQL :

{code:sql}
UPDATE CRAWLER.QCD_CCR_AHC a
JOIN CRAWLER.QCD_VS_LOOKUP v ON a.USER_ID = v.USER_ID
SET a.NAME_EMAIL = CONCAT(COALESCE(v.NAME, ''), ' ', COALESCE(v.EMAIL, ''))
WHERE a.NAME_EMAIL IS NULL OR a.NAME_EMAIL = '' OR a.NAME_EMAIL = 'UNKNOWN';
{code}


{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push)
{noformat}


{noformat}
$  git log -1
commit 0e763f167b27ccc717bd03dd4e...

---

### [AGILEDEV-824] [ticketsage][summary] ticketsage 분석시 : vspvs에서 추가한 comments들을 빼고 분석해야함.
- **상태**: Resolved | **최종 업데이트**: 2026-02-25T11:40:14.000+0900
- **티켓 본문**: ticketsage 분석시 : vspvs에서 추가한 comments들을 빼고 분석해야함.

vspvs에서 추가한 comments는 자동으로 생성되는 것으로 분석에 영향을 미치면 안됨.
- QCD_SAGE_LLM_QUERY 에서만 comments를 처리하므로 이를 추가 필요.
- context에서도 vspvs comments를 빼야 할지 ?   빼는게 맞기는 함
- **작업 히스토리 (User Comments)**:
  - [2026-02-06T14:49:49.000+0900] DESIGN
 !20260206_143639214.jpg! 

DL_ISSUE.. (ADDITIONAL) table에 COMMENTS에 vspvs 작성한 comments가 빠져서 오면 제일 좋겠지만,  
빠져서 오지 않는다고 가정하고 작성한 것입니다.
  - [2026-02-06T19:07:16.000+0900] ~/code/ticketsage/summary  $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)

~/code/ticketsage/summary  $  git log -1
commit 5d922988f38526b106fead309701f828672dbe76 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Fri Feb 6 18:50:46 2026 +0900

    [AGILEDEV-824] DNS 우회 &  [ticketsage][summary] ticketsage 분석시 : vspvs에서 추가한 comments들을 빼고 분석해야함.
    
    - use cust...
  - [2026-02-09T16:28:50.000+0900] summary 의  crontab log의 마지막에
vspvs를 가진 issue list를 쓰게 함.  

comments를 달고 이 부분에 issue가 찍히면 이 ticket을 resolve

---

### [AGILEDEV-817] CCR DB 데이터오류확인건
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T13:31:28.000+0900
- **티켓 본문**: 책임님 

예를들어 assignee값이 금일 DB를 조회하니 이런식으로 깨져있습니다.

다른 필드도 이런경우들이 있어서 데이터 확인 필요합니다.

 

!image-2026-02-02-17-52-53-651.png!
- **작업 히스토리 (User Comments)**:
  - [2026-02-02T19:43:07.000+0900] [~jungmee.lee]님 , 감사합니다. ticket 번호가 무엇인지요?

아래 그림과 같이 DB에서는 json 모양이 깨져 있지 않은듯 해서요.
 !screenshot-1.png! 

 !image-2026-02-02-19-44-35-887.png!
  - [2026-02-03T13:01:50.000+0900] [~jungmee.lee] 님 , 첨부가 깨져있는 것 확인하였습니다.
 !screenshot-2.png! 

CCR-20201 ticket 입니다.
1. DB 확인 ->  잘 들어가져있습니다.
 !screenshot-3.png! 
2. DB 에서 python으로 읽어서 xlsx로 만들었습니다. -> 잘 들어가져있습니다.
ccr에서 CAnalysisVlm.py 을 실행시키면 , 앞 부분에서 qcd_ccr_screening_points.xlsx  파일을 만들게 해두었습니다. 
 !screenshot-4.png! 

의심 사항 : ccr.xlsx를 어떻게 받으셨는지 모르겠지만, 그 받는 tool이 제대로 excel로 변환을 해주지 못하는 듯 합니다.
qcd_ccr_screening_points.xlsx 을 사용하시면 어떨까요?  첨부에 추가해두었습니다.
ccr repository 에서 git pull 하시면 실행시 qcd_ccr_screening_points.xlsx...
  - [2026-02-03T13:25:21.000+0900] resolved합니다 문제 있으면 다시 알려주세요.

---

### [AGILEDEV-815] [pvs_crawler][sage] ticket을 합쳐서 Query함으로써 , 전체 비용과 query하는 수를 줄여 전체 응답 속도를 향상시킨다.
- **상태**: Resolved | **최종 업데이트**: 2026-05-13T13:05:58.000+0900
- **티켓 본문**: [ticketsage][summary] ticket을 합쳐서 Query함으로써 , 전체 비용과 query하는 수를 줄여 전체 응답 속도를 향상시킨다.

현재는 한 ticket마다 query를 수행하는데 , 이를 여러개의 ticket을 합쳐서 query가 가능하도록 변경하자.   ticket마다의 token수를 계산하여 , max token 안에서는 1개의 query로 여러개의 ticket을 처리하면 효율적일 것으로 생각한다.   
sequential이 아닌 , 사이즈에 따라 최적의 갯수가 되도록 만들어야 할 것이다.
제일 큰 것들을 배치한다.   작은 것들을 채워넣기 시작한다. 이런 방식으로 문의 


{code:python}
def min_buckets_ffd(balls, bucket_capacity):
    # 1. 공을 내림차순으로 정렬 (큰 것부터)
    sorted_balls = sorted(balls, reverse=True)
    
    # 버킷들의 현재 사용량을 저장하는 리스트
    buckets = []

    for ball in sorted_balls:
        placed = False
        
        # 2. 기존 버킷들 중 들어갈 곳이 있는지 확인
        for i in range(len(buckets)):
            if buckets[i] + ball <= bucket_capacity:
                buckets[i] += ball
                placed = T...
- **작업 히스토리 (User Comments)**:
  - [2026-02-05T20:25:01.000+0900] sort
큰 것부터 선택
- 큰 것 선택하고 ,   작은 것중에서 MAX가 되게 채운다.   10 box에서 6 을 처음에 선택하게 되면 , 뒤에는 3,2,1 이 남으면 3먼저 선택 , 다음에 1을 선택
- 계속 이렇게 해 나간다. 

N logN
  - [2026-02-09T18:09:19.000+0900] 현재는 저장하는 것 까지 고려해서 50개마다 LLM을 처리한다. 
나중에도 LLM 처리한 것에 대해서는 저장을 하고 진행을 하면 되므로 , 
뒤에 처리해야 할 티켓들을 모두 모아서 20번의 query마다 처리하게 하면 될 것이다.
1. size를 check한다. 
2. 위의 algorithm으로 몇번의 query를 할지를 정한다.
3. 30개의 query마다 해당 내용에 대한 save를 한다.
얼마나 query수가 줄어두는지를 보면 알 것이다.  input (system query) size는 같다. (user query는 줄어든다)    output size도 결국 같다. 
별 영향이 없으려나!~~  속도만 빨라지려나?
여러개의 ticket들을 한 query에 넣으므로 , 내부에서 ticket들끼리 영향을 받는 것은 없으려나?
  - [2026-05-13T13:03:36.000+0900] *{*}pvs_crawler/sage 에 코드는 방영되어져있고 , 이대로 동작함.{*}*
sage_llm_summary.v0.005.prompt  에 RAG와 summary 가 모두 되도록 prompt를 변경하였음
  - [2026-05-13T13:05:41.000+0900] {noformat}
$  git remote -v
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (fetch)
origin  ssh://git@mod.lge.com:2222/swpmviz/pvs_crawler.git (push)
{noformat}
 

{noformat}
$  git log  -1
commit e727cf13e90ca52bf86c02372a68bfb3004cb8be (HEAD -> master)
Author: charles.lee 
Date:   Mon May 11 10:09:58 2026 +0900

    [AGILEDEV-1001][service중 아님] sage_llm_summary: DB 재연결 retry, _g_db_error 플래그, --max-run-hours 옵션 추가
    
    - `--max-run-hours N`: 프로그램 최대 실행 시간 CLI 옵션 추...

---

### [AGILEDEV-814] [ticketsage][summary] TP/FP 판정 및 근거 및 category 적용
- **상태**: Resolved | **최종 업데이트**: 2026-02-11T08:43:50.000+0900
- **티켓 본문**: [ticketsage][summary] TP/FP 판정 및 근거 및 category 적용
- **작업 히스토리 (User Comments)**:
  - [2026-02-02T20:50:47.000+0900] repository : http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git
branch : 260130/true_false_positive
directory : ~/code/ticketsage/tp_fp
ticketsage/summary/ticket_sage_summary.v0.001.prompt , ticketsage_llm_summary.py

{noformat}
commit edbd67f6f625dbb9801588e05e35a91e2bcac367 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Mon Feb 2 20:49:04 2026 +0900

    summary: update prompt

commit f2389534abab884c4c34bc296f43bb68b4caea28
Author: charles.lee 
Date:   Mon...
  - [2026-02-03T11:09:19.000+0900] ~/code/ticketsage/tp_fp 에서 
$ make tp-fp-today
그날 그날 추가된 LLM_SUMMARY의 tp fp 의 내용을 확인한다.

---

### [AGILEDEV-809] mcp 환경 설정 : 내부적으로 copilot을 사용하여 collab, jira , gerrit 에 접속하여 분석이 용이하게 환경 구성
- **상태**: Resolved | **최종 업데이트**: 2026-02-26T17:13:03.000+0900
- **티켓 본문**: mcp 환경 설정 : 내부적으로 copilot을 사용하여 collab, jira , gerrit 에 접속하여 분석이 용이하게 환경 구성

[http://collab.lge.com/main/display/~dongsoo.choi/mcp+server+setup]
- **작업 히스토리 (User Comments)**:
  - [2026-02-10T14:46:43.000+0900] jira,confluence setup 완료 in linux copilot-cli
https://github.com/cheoljoo/mcp_copilot/blob/main/docs/linux-copilot-cli-setup-korean.md
  - [2026-02-10T15:06:14.000+0900] {expand:title=Configuration}
configuration in linux:
{code}
$ cat /data01/cheoljoo.lee/.copilot/mcp-config.json
{code}

{json}
{
  "mcpServers": {
    "jira": \{ ... }
  }
}
{json}
{expand}

{expand:title=Troubleshooting}
- jira 연결 잘 안될때
- URL 경로 수정 필요: http://jira.lge.com/issue/rest/api/2/issue/AGILEDEV-653
{expand}
  - [2026-02-26T14:36:43.000+0900] 문서 : http://mod.lge.com/hub/cheoljoo.lee/publish/-/blob/main/lge/linux-copilot-cli-setup-korean.md?ref_type=heads

MCP의 경우는 copilot으로 만들어도 됨.
특히 , 회사의 gerrit들은 처리 방식들도 조금씩 다를수 있어, 이를 만들어야함. 
https://github.com/cayirtepeomer/gerrit-code-review-mcp 소스를 가져와서 변경하면 됨


http://collab.lge.com/main/display/~dongsoo.choi/mcp+server+setup
mcp server 설치 전 사전에 준비해야 할 항목

1. vs code install (system x64)

2. github copilot install

3. github copilot chat install

4. log in _lgevs (w/o pwd)

...

---

### [AGILEDEV-808] connectWide ticket들에 대해  true_positive/false_positive 구별
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T13:18:43.000+0900
- **티켓 본문**: 성환혁 책임님의 분류 로 진성 / 가성 구별

현재 이 프롬프트로 돌리고 있는데요,
 

{noformat}
나는 이슈 리포트 파일을 첨부해줄거야.
 
## 지시
너는 첨부된 파일의 내용을 분석한 후 이슈 중에서 정말 버그가 맞는 티켓과 버그라고 볼 수 없는 티켓을 분류해줘.
결과는 엑셀표로 내려받게 해줘.
 
## 조건
* 표형태로 만들어줘.
* 1번 열 : 첨부해주었던 파일명
* 2번 열 : 이슈 ID
* 3번 열 : Summary
* 4번 열 : Status
* 5번 열 : Assignee
* 6번 열 : 이슈에 대한 간단한 1줄 설명
* 7번 열 : 이슈가 진짜 버그인지 여부를 입력해줘. (진짜 이슈일 경우 "진성", 이슈가 아닐 경우 "가성")
* 8번 열 : 진짜 버그인지 여부를 확인한 근거를 짧게 적어줘.
 
## 진성, 가성의 분류 기준 (예시)
### 진성
* 개발자가 수정해야 할 버그가 맞고, 이미 수정했거나, 수정하기로 한 경우
* 버그가 맞으나 수정을 다음에 하기로 미루거나, 안하기로 협의한 경우
 
### 가성
* 테스트를 잘못 수행한 경우
* Spec(요구사항 문서, 요구사항 티켓, 설계 문서 등)에 맞게 개발된 경우 (=Spec이 잘못된 경우)
* 담당 개발자가 수정하지 않는 외부 이슈인 경우(3rd Party가 수정해야 하거나, OEM(고객사)이 수정해야 하거나 등)
* TC가 잘못된 경우
* UI/UX가 잘못된 경우 (UI/UX 담당자가 수정해야 하는 경우 등)
{noformat}
- **작업 히스토리 (User Comments)**:
  - [2026-02-02T21:14:38.000+0900] [^cli_defect_reports_20260131_131319.zip]  은 작업한 전체 내용이 들어있습니다.
cli_defect_reports_20260131_131319/*.md는 각 ticket에 대한 comments와 llm_summary 를 넣어둔 파일들 입니다.

여기서는 copilot cli를 사용하였습니다. (이유는 copilot만을 사용하면 각 file안의 comments 를 일고 category화를 시켜 달라고 했더니,  특히 Allow를 계속 눌러주어야 하고 Python code를 만들어 처리를 합니다.)
그래서,  copilot  cli 를 사용하여 그 안의 prompt에 python code만들지 말고  수동으로 각 file을 직접 읽어서 처리를 하라고 하니, 처리는 하는데 중간중간 일괄로 처리하는 듯도 하구요. 이것들이 제대로 처리하는지를 모르겠습니다. 그리고, copilot cli를 쓸때  claude-sonnet-4.5 를 사용하면 그나마 많이...

---

### [AGILEDEV-803] connectWide ticket들에 대해  GROUP BY RESOLUTION , DEFECT_TYPE  이고 RESOLUTION이 Fixed는 아닌 것 들에 대해서 각 DEFECT_TYPE이 왜 나왔는지 categorize
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T13:31:17.000+0900
- **티켓 본문**: http://collab.lge.com/main/pages/viewpage.action?pageId=3517233462#WeeklyReport-1280533932

에서 

GROUP BY RESOLUTION , DEFECT_TYPE  이고 RESOLUTION이 Fixed는 아닌 것 들에 대해서
각 DEFECT_TYPE이 왜 나왔는지 categorize를 해야 한다.
- 주어지는 정보는 
-- comments 
-- comments + llm_summary
-- llm_summary

우선 GROUP BY에 각각에 대한 data file들을 생성하고 , 
생성된 data 파일을 copilot에 upload하여 category 형성을 요청 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-30T16:24:19.000+0900] {noformat}
[AGILEDEV-803] connectWide ticket들에 대해  GROUP BY RESOLUTION , DEFECT_TYPE  이고 RESOLUTION이 Fixed는 아닌 것 들에 대해서 각 DEFECT_TYPE이 왜 나왔는지 categorize

- branch : 260130/defect_type_in_not_fixed
- modified files
    - defect_type_in_wont_fix/*.md : 설명 파일
    - defect_type_in_wont_fix/README.md : 마지막에 copilot에서 prompt를 어떻게 만드는지 설명 추가함.
    - defect_type_in_wont_fix/results_example : make run 하면 초기 생성된 results_example/INDEX_BACKUP.md 에서 copilot prompt를 수행시 생성되는 results_example/INDEX.md
...

---

### [AGILEDEV-802] CCR DB 추가항목
- **상태**: Resolved | **최종 업데이트**: 2026-02-11T08:43:50.000+0900
- **티켓 본문**: {noformat}
QCD_CCR_SCREENING_POINTS
에 추가할 필드가 있습니다.
{noformat}
   1) ticket_type
      2) Change Scope
      3) Change Function_VLM

4) Created

5)STATUS 

6)resolution 

7)CCR URL
- **작업 히스토리 (User Comments)**:
  - [2026-01-29T14:59:27.000+0900] CCR URL 외는 모두 추가 완료
CCR URL은 http://jira.lge.com/issue/browse/ 뒤에 ISSUE_ID를 붙이면 됨

## option --forced_update ON
[INFO] Loaded 19 fields from table 'QCD_CCR_SCREENING_POINTS'
[INFO] Fields: ['NO', 'SNAPDATE', 'ISSUE_ID', 'ERR_MSG', 'SCREENING_POINT', 'SCREENING_POINT_DICT', 'CONTEXT', 'SCREENING_POINT_TOTAL', 'ASSIGNEE', 'ASSIGNEE_UNIT', 'FEATURE_LEADER', 'UPDATED_DATE', 'FEATURE_LEADER_UNIT', 'CREATED_DATE', 'STATUS', 'RESOLUTION', 'TICKET_TYPE', 'CHANGE_SCOPE', 'CHANGE_FUNCTION_VLM']
[INF...

---

### [AGILEDEV-790] [ticket sage][db_test] db_teest와 jira_test에서 --fixed  option 적용 : RESOLUTION이 fixed인 것만을 대상으로 train
- **상태**: Resolved | **최종 업데이트**: 2026-02-05T19:37:21.000+0900
- **티켓 본문**: [ticket sage][db_test] db_teest와 jira_test에서 --fixed  option 적용 : RESOLUTION이 fixed인 것만을 대상으로 train

jira_test는 train 을 fixed인 것만으로 ...
db_test에서도 train을 fixed인 것만으로 ..
- **작업 히스토리 (User Comments)**:
  - [2026-02-03T13:55:32.000+0900] Fixed만이 제대로 처리된게 아닐수 도 있다. Spec등 다른 ticket들도 유효한 것이고, Won't Fix라고 할지라도 의미가 있다고 보고 있음.

Fixed에 대해서 Train 시키는 것은 embedding vector에 대해서만 살펴볼 것이다. 
결과가 얼마나 차이가 나는지 살펴보야 할 것이다.
  - [2026-02-05T19:36:58.000+0900] VECTOR  TEST 

ORG
{noformat}
=========================================
=== CUMULATIVE TOTALS BY SCENARIO (ORG) ===
=========================================
Scenario             | Top1 Hits Top3 Hits Total  | Top1%   Top3%  
----------------------------------------------------------------------
ALL   ALL            |      6775      7946  14379 |   47.1%   55.3% 
ALL   TRAINED        |      2174      2472   3929 |   55.3%   62.9% 
FIXED ALL            |      4564      5491  14379 |   ...

---

### [AGILEDEV-787] (Qlik) R&D 가시화 Board_COST 관리Task 실패 : 데이터 동기화 이슈
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T13:31:08.000+0900
- **티켓 본문**: Task가 실패되어 관련 log 파일 보내드립니다.
필드명이 변경되었거나 누락된 것 같습니다.


이전과 동일 상황으로 아무래도 자동화 data 추출에 문제가 있는 것 같습니다만, 확인 좀 부탁드립니다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-26T19:26:45.000+0900] 해당 월로 예산 현황이 나오는 것으로 보임. (12월하는 경우만 에러 발생)
현재 월을 구해서 그 월로 눌러 처리하도록 변경할 것


위의 내용은 cost관련하여 효율화 task에서 update해야 할 내용이어야 할 것 같음.
  - [2026-01-27T16:10:40.000+0900] 개발 진행 되는 상세 flow 작성
bug fix : 기존 예산현황에서 1~12월까지를 무조건 얻던 것에서 현재의 월까지만 정보를 얻는 거으로 변경 (12월로 하면 에러 발생)

- `PMS.xlsx`: 통합 분석 보고서 : 26년으로 변경된 내용이 들어 있습니다. 
- `PMS_cost.xlsx`: 비용 분석 보고서  :  web URL로 개발자들이 입력하는 엑셀로 현재는 25년 자료임.
- `PMS_mm.xlsx`: 월별 대시보드 분석 : 정종우 책임님게서 자원운영으로부터 받아 작업해서 upload하는 것으로 현재는 25년 11월 자료입니다.

pyautogui 에 대한 workflow입니다.  (특히 생성되는 input / output file에 대한 설명)
업무 참조하세요. (pyautogui/README.md)
http://tiger02.lge.com/cheoljoo.lee/code/misc/pyautogui/README.html
  - [2026-01-27T19:29:49.000+0900] 동기화 이슈
- PMS 26년 데이터 Crawling 완료
- 해외R&D 효율화 task 에서 SW TDR 으로 이관 (정종경 책임님 이동)
-- PMS_MM은 기존과 같이 26년도 용으로 유지 : (26년가예산적용) ■연구용역■26년예산반영기준.xlsm
-- dash_board는 지연됨.  PMS_mm.xlsx로 자원운영에서 제공했던 MM 관련 내용이 반영이 안됩니다.

---

### [AGILEDEV-786] [ticketsage][summary] prompt 확인 필요 (add "in english for 3 line summary")
- **상태**: Resolved | **최종 업데이트**: 2026-02-09T16:14:41.000+0900
- **티켓 본문**: [ticketsage][summary] prompt 확인 필요 (add "in english for 3 line summary")
+
[ticketsage][jira_test] RAG에서 vlm 3개 주는 것이 문제 없이 잘 나오는지 확인 (issue1 has higher similarity than issue2)
- **작업 히스토리 (User Comments)**:
  - [2026-01-26T19:29:07.000+0900] {"prompt_ver": 0.001, "prompt_file": "ticket_sage_summary.v0.001.prompt", "llm": {"issue_id": "vlm=HMCCW-5465", "Assignee": "jitender.singh", "Problem Analysis": {"Specific Issue or Bug": "HUD 회전 제어 시 DLT 로그에 'CF_AVN_HudRotationSet' 값이 출력되지 않음.", "Symptoms and Impact": "HUD 디스플레이에서 회전 제어 팝업은 정상적으로 표시되지만, DLT 로그에 필요한 데이터가 출력되지 않아 디버깅 및 확인이 어려움."}, "Resolution Owner": {"Lead Resolver": "jitender.singh", "Final Resolver": "dongryeol.seo"}, "Solution": {"Detailed Solution": "SysRS VC 파일을 업데이트하여 IVC ...

---

### [AGILEDEV-784] CCR 티켓 분석 : screening points DB 구현
- **상태**: Resolved | **최종 업데이트**: 2026-02-11T08:43:50.000+0900
- **티켓 본문**: screening points을 위한 DB화 할 것
- **작업 히스토리 (User Comments)**:
  - [2026-01-22T23:21:05.000+0900] branch : 260122/DB
{noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ccr.git (push){noformat}
 
{noformat}
commit 0d3aa09e46b378f313f4dcb0a7ea300c29a75c41 (HEAD -> 260122/DB, origin/260122/DB)
Author: cheoljoo.lee 
Date:   Thu Jan 22 23:18:56 2026 +0900    [AGILEDEV-784] CCR 티켓 분석 : screening points DB 구현
    
    - $  make analyze-parallel-filtered
    - CDataBase('QCD_CCR_SCREENING_POINTS', unique_key...

---

### [AGILEDEV-783] CCR 티켓 분석 : screening points DB Design
- **상태**: Resolved | **최종 업데이트**: 2026-02-11T08:43:49.000+0900
- **티켓 본문**: screening points을 위한 DB design 및 생성
- **작업 히스토리 (User Comments)**:
  - [2026-01-22T23:23:37.000+0900] !screenshot-1.png|width=1200!

---

### [AGILEDEV-777] [ticket sage][jira-test] jira test report
- **상태**: Resolved | **최종 업데이트**: 2026-02-06T09:04:40.000+0900
- **티켓 본문**: db_test/CSAGE_DB_REPORT.py 을 이용하여 jira_test에 대한 결과도 table 과  graph를 보여준다.
여기서는 REAL_ASSIGNEE가 값이 있는 것을 query하여 이것에 대한 report를 만들어야 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-23T17:24:01.000+0900] 여기에 계속 update 자동으로 되게 함
http://tiger02.lge.com/cheoljoo.lee/code/crontab/ticketsage/db_test/sage_rag_jira_report_gpt-4o_text-embedding-3-large_gpt-4o-mini.html
  - [2026-02-05T19:59:10.000+0900] http://tiger02.lge.com/cheoljoo.lee/code/crontab/ticketsage/db_test/sage_rag_jira_report_gpt-4o_text-embedding-3-large_gpt-4o-mini.html
http://tiger02.lge.com/cheoljoo.lee/code/crontab/ticketsage/db_test/sage_vector_jira_report_gpt-4o_text-embedding-3-large_gpt-4o-mini.html

1월 것 까지만 보여준다. 
오늘 날짜까지 보여주게 변경해 달라.
  - [2026-02-06T09:04:40.000+0900] [AGILEDEV-777] jira_report until now

~/code/ticketsage/db_test  $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)


~/code/ticketsage/db_test  $  git log -1
commit 220098dc0aa9b5bda4aa1ad63beebdd1a4a6f9f8 (HEAD -> main, origin/main, origin/HEAD)
Author: cheoljoo.lee 
Date:   Fri Feb 6 09:03:26 2026 +0900

    [AGILEDEV-777] jira_report until now

---

### [AGILEDEV-771] [ticket sage][jira-test] jira ticket에서 얻은 정보로 RAG와 vector를 이용한 결과 도출 lib
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:33.000+0900
- **티켓 본문**: [ticket sage][jira-test] jira ticket에서 얻은 정보로 RAG와 vector를 이용한 결과 도출 lib
jira ticket의 내용 (summary , description , function)을 가지고 RAG , vector에 대한 결과를 도출하는 lib 생성
class를 생성하여 __init__ 에서 train 을 하고 , 
함수를 부르면 그 안에서 vector top 30을 뽑아 vector에 대한 rank를 뽑고 , 
top 30을 가지고 llm_rag_query를 하여 rag top3를 이유와 함께 뽑는다.
이 dictionary형식의  데이터를 return하여 jira comments를 작성하는 base로 활용하게 하는 lib를 만든다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-20T07:29:27.000+0900] [AGILEDEV-771] jira_test & DNS resolver


{noformat}
- db_test/CSAGE_JIRA_TEST.py 을 작업하였습니다.  추후 jira_test directory를 만들어 작업하시면 될 듯하고 , 이 내용 참조하시거나 참조하라고 copilot에 알리면 쉽게 코딩 되지 않을까 합니다.
- make jira-single     <- 1 개 추가하는 것 해볼수 있음.
- make jira-reuse-all   <- 어제 이후 모든 update된 ticket들에 대한 처리  (jira에서 읽는 시간이 많이 걸리므로 , 한번 읽고 file로 남겨서 재사용)  - cache file : jira_reuse.json
- make jira-all     <- 언제나 JIRA API로 새로 읽음.

# db_test/CSAGE_JIRA_TEST.py에 아래의 comments를 남겼습니다. 해당 부분에 작업하셔도 됩니다.
  - 이상재님...

---

### [AGILEDEV-769] CCR 티켓 분석 : screening points 구현
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T13:30:48.000+0900
- **티켓 본문**: POC 완료
- 팀장님 26-01-14 주간회의 결정 사항
  : screening points를 AI를 사용하지 않는 선에서 dashboard를 구현하라.


[Screening Point]  
FLU에서  screening points 정의를 매우 잘해주셨습니다. 주어진 문서에 일부 코드까지 포함되어져있습니다.
총 25점 ,  이중에 현재 구현된 내용은 10.5 점을 구현함.  FLU에서는 25점 만점중에서 14점 이상일때만 자신들이 검토를 시작한다는 기준을 세운듯 합니다.  13점 이하는 reject

## clarity  (FLU에서 정의한 screening points 상세 항목)
### 1. Summary Tag Check (1점)  : 구현 
### 2. Summary Specificity Check (1점) : 구현
### 3. Description Length Check (1점) : 구현
### 4. AS-IS/TO-BE Check (1점) : 미구현 (구현 조건 : description인지 comments인지 어디를 봐야 하는지 알면 text를 보고 처리하므로 추가 가능)
### 5. Technical Detail Check (1점) : 미구현 (구현 조건 : description인지 comments인지 어디를 봐야 하는지 알면 text를 보고 처리하므로 추가 가능)
## rationale
### 1. External Ticket Link Check (2점) : 구현
### 2. Root Cause Analysis Check (2점) : 미구현 (구현 조건 : ...
- **작업 히스토리 (User Comments)**:
  - [2026-01-15T07:57:01.000+0900] [~jungmee.lee]님 , 이 ticket 내용이 맞는지 확인 부탁드립니다.
  - [2026-01-22T23:26:34.000+0900] CCR screening points 구현 완료하였습니다.
전체 category는 5개이며 , sub-category는 20개 입니다. (FLU(Feature Leader Unit)에서 제안한 것은 19개의 sub-category는 19개인데 , 제가 1개는 더 세분화하였습니다.)
구현시 LLM의 판단을 필요로 하는 부분은 없었습니다.  CCR안에 field들이 모두 정의되어져 있어서 , 해당 내용들을 분석하여 모두 값을 얻을 수 있었습니다.
(내용 분석시 조금 더 natural한 글에 대해서도 판단을 해야 하는게 필요하면 LLM 적용이 필요합니다.)
CCR 티켓 갯수 : 18769

# 첨부된 엑셀의 screening points관련 sheet

{noformat}
4.Unit Screening Points : unit별 screening points 와 평균이며 , 평균으로 sort   (-25점이 제일 안 좋은 점수 입니다.)
4-1. Screening Evi...

---

### [AGILEDEV-764] [Gerrit] Inline Commit에서 SRV+ID unique key에서 SRV+ID + REPO 로 key를 변경
- **상태**: Resolved | **최종 업데이트**: 2026-02-25T11:40:37.000+0900
- **티켓 본문**: base table의 SRV / ID / REPO 를 DB field는 그대로 둔다. 
그러나, QCD_GERRIT_INLINE_COMMIT인 내가 programming한 부분에서는 REPO field를 가지고 있지 않다.   GERRIT_INLINE_COMMIT* DB field추가해야함.
REPO를 추가하여 넣고 , GERRIT으로 부터 오는 내용을 보고 처리하면 됨.
여기도 REPO를 추가하여 repo까지를 key로 인식해야 한다.  그리고, 그 내용을 해당 srv+id 로 1개만을 가지는게 아닌 , srv_id+repo를 key가 되도록 만들어주어야 한다.

기존 srv+id로 찾으면 , 여러개의 gerrit이 나온다. 기존에는 그 중 가장 오래된 (의미있는) 것을 선택하여 그 gerrit에 대해서만 처리함.
새로운 것은 srv+id로 찾으면 여러개가 나왔을때 , 이중 같은 REPO 중에서 오래된 것을 골라야하고 , REPO 값까지 넣어서 결과를 update한다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-22T11:17:30.000+0900] 현재 김학중 책임님 작업 내용 기반 처리해야 할 일
 * GERRIT_INLINE table에 REPO field를 추가하여 기본에서 REPO값을 copy해두는데 NULL인 것들이 있다.
 ** 이 의미는 srv+id 가 서로 안 맞는 것으로 보인다. 이렇게 srv+id를 변경해서 저장을 하는 코드가 생길수 있는지 살펴봐야 한다.
  - [2026-01-30T15:50:10.000+0900] $  git log -1
commit 0c1961aa7b1c0c9021e554f91cbba5b7e8066611 (HEAD -> feature/add_repos_to_commit_key, origin/feature/add_repos_to_commit_key)
Author: charles.lee 
Date:   Thu Jan 29 15:25:01 2026 +0900

    [AGILEDEV-764] [Gerrit] Inline Commit에서 SRV+ID unique key에서 SRV+ID + REPO 로 key를 변경
    
    - CGerritCommitInline.py
        - class CGerritCommitInline: 수정 : repo (gerrit REST api에서는 project) 로 query를 하여 query된 내용에 대해 분석
            - 다수의 branch가 존재하면 MERGED이고 제일 오래된 ticket에 대해 분...

---

### [AGILEDEV-760] [ticket sage][summary] description과 comments를 다루는 ADDITIONAL table에 대해서는 SNAPDATE를 비교
- **상태**: Open | **최종 업데이트**: 2026-04-20T09:38:12.000+0900
- **티켓 본문**: 현재는 description과 comments를 다루는 ADDITIONAL table에 대해서는 SNAPDATE를 비교하여 처리하는 것이 없다.
1. table들에 DL_ADDITIONAL_SNAPDATE 를 추가로 만들어야 한다.
2. 각 table들에 이 값을 update해야 한다.
3. 비교를 할때 (DL_SNAPDATE or DL_ADDITIONAL_SNAPDATE ) and CONTEXT의 변화가 있을때 update하는 것으로 변경해야함.
- **작업 히스토리 (User Comments)**:
  - [2026-04-20T09:38:12.000+0900] 확인 필요 : 새로 update되었다고 판단 기준 DL_ISSUE의 SNAPDATE로 판단하는가?
질문 :
1. 어떤 ticket에 대해서 comments만 변경되었다고 하면 , DL_ISSUE와 ADDITIONAL table의 SNAPDATE가 모두 변경되는가/ 아니면 ADDITONAL 의 SNAPDATE만 변경되는가?

---

### [AGILEDEV-759] [ticket sage][summary] context를 비교하여 틀린 부분이 있을때만 llm query를 해라.
- **상태**: Resolved | **최종 업데이트**: 2026-01-16T07:34:43.000+0900
- **티켓 본문**: 어느날 변경된 갯수가 매우 많음


------- 이철주C 문의
다음과 같이 01-12일에 QCD_DL_ISSUE_FROM_MONGODB table에 update된 ticket이 918개 였습니다.
ticketsage에서 update되었다고 판단은 SNAPDATE 를 저장해두었다가 , SNAPDATE가 최신으로 udpate되면  update가 되었다고 판단합니다.

문의 1 : 이때 , 내용까지 보고 QCD_DL_ISSUE_FROM_MONGODB을 update하는 것인지 문의드립니다.  DB에 필요한 field들인 comments , description , sumamry , root cause , function 등이 변한 것인지를 확인하는지 문의드립니다.
내용 변경없이 jira updated 날짜만 변경되는 경우들이 있어서 문의드립니다.


문의 2 : 
HMCCW-1265 의 JIRA를 보면 updated 가 2025/05/21 09:51 입니다.
QCD_DL_ISSUE_FROM_MONGODB에서는 SNAPDATE가 2026-01-11 이었습니다. 
문의 :  QCD_DL_ISSUE_FROM_MONGODB  에서는 무엇때문에 update된 것일까요?

--------- 김학중C  답변
문의1: Update 판단 로직은 아래와 같습니다. (잘동작한다고 생각했는데....)
변경시 업데이트해야할 항목에 대해서 1개라도 변경이 있다면 업데이트 리스트에 추가하여 DB 를 업데이트 합니다. 따라서 아래 로직에 따라서 updated 날짜가 변경된 경우에도 updated 날짜와 함께 S...
- **작업 히스토리 (User Comments)**:
  - [2026-01-13T02:40:24.000+0900] 처리 : $  git log -1
commit 48eaffb94ff8d5f73ca7c7f443c698dfc53bfffb (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Tue Jan 13 02:31:42 2026 +0900

    summary : add context to reduce llm query. so we compare the contents(context).

남은 문제 : 현재는 description과 comments를 다루는 ADDITIONAL table에 대해서는 SNAPDATE를 비교하여 처리하는 것이 없다. 
1. table들에 DL_ADDITIONAL_SNAPDATE 를 추가로 만들어야 한다.
2. 각 table들에 이 값을 update해야 한다.
3. 비교를 할때 (DL_SNAPDATE  or DL_ADDITIONAL_SNAPDATE ) and CONTEXT의 변...

---

### [AGILEDEV-750] 2026: There is no data to download
- **상태**: Resolved | **최종 업데이트**: 2026-01-07T08:44:23.000+0900
- **티켓 본문**: # 2026년의 것을 제대로 처리하는지?
 # 2025년도의 마지막 data를 commit해둔다.
 # 연초이므로 data가 없어 , There is no data to download 에 대한 처리 (기존 자료 copy해둠)
 # 연도가 2025로 선택이 되어져서 이른 2026으로 변경하는 작업 진행: 항상 최신 연도를 선택하게 변경
- **작업 히스토리 (User Comments)**:
  - [2026-01-07T08:44:23.000+0900] # 2026년의 것을 제대로 처리하는지?
 # 2025년도의 마지막 data를 commit해둔다.
 # 연초이므로 data가 없어 , There is no data to download 에 대한 처리 (기존 자료 copy해둠)
 # 연도가 2025로 선택이 되어져서 이른 2026으로 변경하는 작업 진행: 항상 최신 연도를 선택하게 변경



 

commit c97e7710ad6bf3eff8c25486a021f8de44bd205b (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Mon Jan 5 13:14:19 2026 +0900

    pyautogui : -

commit 43196b059bb91f9be5b2016e73f450d9210355f4
Author: charles.lee 
Date:   Mon Jan 5 12:17:26 2026 +0900

    pyauto...

---

### [AGILEDEV-719] CCR 티켓 분석 : Feature Unit screen POC
- **상태**: Resolved | **최종 업데이트**: 2026-01-15T07:57:43.000+0900
- **티켓 본문**: CCR 티켓 분석 : Feature Unit screen POC

 

| 항목 | 배점 | 검증 방법 | Pass 조건 |

|------|------|-----------|----------|

| ***1. Summary 태그*** | 1점 | 정규식 매칭 | `[Issue]`, `[Test]`, `[CR]` 중 1개 이상 |  %%

| ***2. Summary 구체성*** | 1점 | 키워드 검사 | 차종/모듈명 포함 (예: ccIC27, Home) | %%

| ***3. Description 길이*** | 1점 | 문자 수 계산 | 최소 200자 이상 | %%

| ***4. AS-IS/TO-BE*** | 1점 | 키워드 검사 | "AS-IS", "TO-BE", "기존", "변경 후" 중 1개 이상 |

| ***5. 기술 세부사항*** | 1점 | 패턴 매칭 | 파일명, 함수명, 코드 스니펫 중 2개 이상 |

| 항목 | 배점 | 검증 방법 | Pass 조건 |

|------|------|-----------|----------|

| ***1. 외부 티켓 링크*** | 2점 | Issue Links 확인 | DQA/OEM/Customer 티켓 1개 이상 | %%

| ***2. Root Cause*** | 2점 | 키워드 + 분석 길이 | "원인" + 상세 설명 100자 이상 |

| ***3. 사양/요구사항*** | 1점 | 키워드 검사 | "사양", "요구사항", "Spec" 중 1개 |

| 항목 | 배점 | 검증 방법 | Pass 조...
- **작업 히스토리 (User Comments)**:
  - [2025-12-24T00:48:42.000+0900] merge request : http://mod.lge.com/hub/cheoljoo.lee/ccr/-/merge_requests/3
branch : 251223/FL_Unit_Screening_POC

result

{noformat}
======================================================================
=== 5. Unit별 Screening Points 통계 (Assignee Organization 기준) ===
======================================================================

Unit (Assignee Organization)                                      Count    Total Pts    Avg Pts
-----------------------------------------------------...
  - [2025-12-24T08:54:05.000+0900] 주간보고 보고 내용 :
 * 회의 내용 공유
 ** 준 내용 중에 이들의 screen rule이 있음
 * 아이디어 (팀의 PVS trender나 Defect Agent에 넣는 방법)
 ** Hexa Index로 다음을 사용하면 어떨까?
 *** created ~ closed 나 그 외의 중요한 status 들 간의 걸린 시간
 *** screening rule에 의한 Unit별 통계 가능 (항목별 또는 전체 점수 화 가능)
 ** Defect Agent : CCR과 연결된 ticket 들의 내용을 가지고 defect agent에 문의하여 결과를 특정 field나 comments로 추가해주는 것.
 *** 연결 ticket에 대한 내용이 Defect Agent에 있는 경우 내용을 받아 comments등에 넣어줌
 *** CCR에 대해서는 다른 prompt를 가지고 분석을 하여 분석
 ** Process Mining : 
 *** gerrit 이나 CCR  활동에서...
  - [2025-12-24T14:13:23.000+0900] [~jungmee.lee]님 , 제가 코드에 다음과 같이  한 것은 위에 requirement를 넣어두었고,
Todo는 아직 안한 것입니다.


{code:python}
            # screening category 2-1. | **1. 외부 티켓 링크** | 2점 | Issue Links 확인 | DQA/OEM/Customer 티켓 1개 이상 |
            issuelinks_len = len(issue['fields'].get('issuelinks', []))
            v['screening_issuelinks_length'] = issuelinks_len
            if issuelinks_len < 1:
                v['screening_points'] -= 2
                v['screening_minus_evidence'].append(
                    ...
  - [2025-12-24T15:41:41.000+0900] 1월에 무슨 이야기 인지 확인하면 될 듯 합니다. 
FL Unit 내부적으로 이야기 할 것을 우리에게 메일을 보내는 느낌입니다.
  - [2025-12-30T22:06:07.000+0900] ======================================================================
=== 3. 전체 티켓 통계 (Feature Leader 구분 없음) ===
======================================================================
{noformat}
Field                                      SUM   Ratio(%)
------------------------------------------------------------
Total                                    16238     100.00
shift_left_complete                      10241      63.07
shift_left_approval_complete             11108      68.41
wr...
  - [2026-01-15T07:57:43.000+0900] good job

---

### [AGILEDEV-676] [scrum] sprint spot ticket 기능 추가
- **상태**: Resolved | **최종 업데이트**: 2026-02-03T11:14:32.000+0900
- **티켓 본문**: Spot Ticket 정의: Sprint 시작 시간 이후에 생성된 티켓

- created > sprint.startDate 조건으로 판단
출력 내용:
- 상단 요약: Total Issues: 20, Spot Tickets: 2 (Sprint 시작 이후 생성된 티켓)
- Spot Tickets 별도 섹션:
-- Assignee별로 그룹화하여 출력
-- Epic별로 그룹화하여 출력
-- 각 티켓의 생성일, SP, Status 표시
- 개별 이슈 출력: 🚨[SPOT] 마커로 Spot Ticket 표시
- By Assignee 통계: Spot: 1개/10.0SP 형식으로 Spot Ticket 수와 SP 합계 표시
- By Epic 통계: 동일하게 Spot Ticket 정보 표시
- 최종 통계: 🚨 Spot Tickets: 2개 (Total SP: 11.5) 표시

JSON 출력: is_spot_ticket, created 필드 추가 및 stats에 spot_tickets, spot_tickets_sp 추가
- **작업 히스토리 (User Comments)**:
  - [2025-12-04T13:34:04.000+0900] # *새 탭 "🚨 Spot Tickets"* - Issues 탭 바로 다음에 위치

 # {*}요약 정보{*}:

 ** Spot Tickets 수
 ** Total SP (Spot Ticket의 Story Point 합계)
 ** Total Issues (전체 이슈 수)
 ** Spot Ratio (Spot Ticket 비율 %)
 ** Sprint Start Date 표시
 # {*}By Assignee 섹션{*}:

 ** Assignee별로 Spot Ticket 그룹화
 ** 각 Assignee의 티켓 수, SP 합계, 티켓 목록 표시
 # {*}By Epic 섹션{*}:

 ** Epic별로 Spot Ticket 그룹화
 ** 각 Epic의 티켓 수, SP 합계, 티켓 목록 (Assignee 포함)
 # {*}All Spot Tickets 테이블{*}:

 ** 생성일 최신순 정렬
 ** Issue Key, Summary, Assignee...
  - [2025-12-04T13:36:19.000+0900] commit info :   http://mod.lge.com/hub/cheoljoo.lee/misc/-/commit/90488022d856ffb55b139a84336a561b26022461

---

### [AGILEDEV-675] [ticket sage][summary] implementation design
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:34.000+0900
- **티켓 본문**: implementation을 하기 위한 DB와 코드 디자인이 필요하다.
- **작업 히스토리 (User Comments)**:
  - [2025-12-10T09:11:54.000+0900] http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/summary/implementation_design.md

---

### [AGILEDEV-659] [scrum] story point 위주로 report 만들기
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:05:35.000+0900
- **티켓 본문**: sprint안의 ticket들에 대해서 초기 설정된 story point 또는 resolve 되기 전의 story point와 resolve 된 후의 story point의 차이를 분석한다.
이유는 우리의 예측력이 어떻게 되는지를 보기 위해서이다. 
resolve 되기 바로 전과 resolved된 후의 story point가 같다면 이것이 resolved된 후의 story point로 보는게 맞을 것이다.

story point를 넣어주는 앞뒤의 값을 보고 
인별 , epic 별 예측력일 보여줄수 있다.

예외 : story point가 없는 경우 , unassigned 인 경우 ,  story point가 15을 넘는 경우  (이 부분은 일부러 길게 잡아 예측할수 없음을 표시한 것과 같이 취급)
- **작업 히스토리 (User Comments)**:
  - [2025-11-28T06:46:20.000+0900] [~gina.oh] 님 , 위 description과 아래 질문에 대한 고견을 듣고 싶습니다.
- 이것을 보기 편하게 잘 표현할 방법이 있을까요?
- jira dashboard로 만드는게 좋을까요?  아니면,  python으로 만들어 html의 결과를 뽑아내는게 좋을까요?
  - [2025-11-28T13:34:41.000+0900] source code [http://mod.lge.com/hub/cheoljoo.lee/misc/-/commit/7ae493c71185486120cbd2e57de0b8a5448d4c82]
결과 확인 URL : [http://jira.lge.com/issue/secure/Dashboard.jspa?selectPageId=84103]
!image-2025-11-28-13-35-52-907.png|width=800! 
!image-2025-11-28-13-36-32-000.png|width=800!

html을 수정후 upload하기 원하면 , ```make html_upload```
수행을 하기를 원하는 ```uv run story_point_history.py -d 날짜``` 보기 원하는 sprint 기간 안에 들어가는 날짜

```txt
$ uv run story_point_history.py -h
usage: story_point_history.py [-h] [-...

---

### [AGILEDEV-658] jira dashboard의 gadget에 변경한 내용 자동 update하기
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:05:36.000+0900
- **티켓 본문**: jira dashboard의 gadget에 변경한 내용 자동 update하기

*세미나도 할수 있는 내용으로 보임*

jira dashboard를 만들어 여기서 javascript code (html)들을 넣어서 , jira 의 내용들을 읽어서 원하는 형식으로 표시하는 기능을 만든다.
이때 , 매번 변경한 html을 dashboard이 해당 gadget을 열어 paste를 해주어야하는 번거로움이 있어서 , 
자동으로 내용을 update하는 것을 만들었으면 한다.
- **작업 히스토리 (User Comments)**:
  - [2025-11-28T06:32:44.000+0900] [~gina.oh] 님 , 이미 만들어 쓰고 계실지 모르지만,  이제 수동으로 copy & paste할 필요가 없습니다.  JIRA Dashboard의 HTML Gadget을 자동으로 업데이트하는 Python 스크립트입니다.
copy & paste 하는게 귀찮아 만들어봤습니다.
http://mod.lge.com/hub/cheoljoo.lee/misc/-/blob/main/update_jira_dashboard/README.md?ref_type=heads

실행은 
git clone하고 update_jira_dashboard 에 들어가셔서 , gina.html 을 변경하신후에
make를 하시면 
http://jira.lge.com/issue/secure/Dashboard.jspa?selectPageId=84103    에서 변경된 내용을 보실수 있습니다.
--help를 해보시면 dashboard 나 gadget id등도 설정할수 있습니다.



$  git log...

---

### [AGILEDEV-657] agile 운영 방법 설정
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:05:35.000+0900
- **티켓 본문**: 어떻게 운영할 것인지?
어떤 것들을 활용

할 것인지?

works
 - 고민 1일
 - 문의 및 뭘 할수 있는지 범위 설정 1일
- **작업 히스토리 (User Comments)**:
  - [2025-11-28T13:45:17.000+0900] sprint운영 방식
 - 3주 운영 (목요일 점심 시작 ~ 3주후 금요일까지 22일)
 - 1주 retrospection 및 안된 것들 / 미진한 부분 완료 / 다음에 할 것 준비 (월 ~ 수요일)
 - retrospection
 -- close sprint하기 전에 문제나 도움이 필요한 것이 무엇인지?
 -- 다음에 Unassigned 된 ticket의 assignee 선정 / story point 입력 및 그 안에 할수 있는 일인지 , 너무 큰 것을 나눌수 없는지?
 - 보고 싶은 내용 : 
-- 초기에 생성시 처음 set한 story point와 끝났을때의 story point가 어떻게 변화가 되었는지를 알고 싶다.
sprint중에서 현재의 날짜나 지정할 날짜와 가장 가까운 날의 sprint에 안의 ticket들이 대상이다.
-- 모두 1건씩 세미나 진행 (주제 아무거나, 시간은 하고 싶으신대로)

sprint board : [http://jira.lge....

---

### [AGILEDEV-656] [ticket sage][train] module단위의 접근으로 각 모듈에 대한 정의 (Components)값 활용
- **상태**: Closed | **최종 업데이트**: 2026-01-28T09:35:57.000+0900
- **티켓 본문**: [ticket sage][train] module단위의 접근으로 각 모듈에 대한 정의 (Components)값 활용

다음과 같이 components가 잘 구성된 것이 있다면,,,
http://jira.lge.com/issue/projects/REAVN?selectedItem=com.atlassian.jira.jira-projects-plugin:components-page

이를 활용하여 components (modules)와 기준으로 candidates 추출
이때 추가적으로 필요한 자료가 components 별로 하는 일등을 기존 ticket에서 추출하여 AI를 통해서 sumamry 형식으로 정의를 해준다면,  최종 RAG query시 더 명확한 선정이 될 것으로 보인다.

추가로, 해당 ticket이 설정된 components와 맞는지도 확인해봐야 한다.
- **작업 히스토리 (User Comments)**:
  - [2026-01-28T09:35:57.000+0900] ORG로만 처리하고, module단위 접근은 필요성이 있을때 다시 시도.
ORG의 적중률이 높아서 필요없을 듯.

추후 ORG 이름들이 바뀌면 mapping table정도가 필요할 듯

---

### [AGILEDEV-653] [ticket sage][train] LLM 접속 에러가 반복적으로 일어날때, 이에 대한 처리 (에러가 많이 일어난 것을 모아서 다음 날에 다시 처리) -> 처리 안된 것들은 mail 전송
- **상태**: Resolved | **최종 업데이트**: 2026-06-01T17:17:03.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-06-01T17:17:03.000+0900] pvs_crawler에서 json에 대한 것이나 반복적으로 에러가 나는 것을 

SWPMUtil/sage_llm_summary_json_failures.csv 

에 저장을 하여 다음에 skip 하도록 함. 

주기적으로 파악하여 지워주고 다시 돌려보게 한다.

---

### [AGILEDEV-651] [ticket sage][test] Design
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:32.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T11:08:47.000+0900] db-test와 jira-test를 구별하기로 함.
vector의 값은 
- db-test에서는 summary에서 저장하는 QCD_SAGE_LLM_RAG_VECTOR 의 LLM_VECTOR 값 재사용
- jira-test에서는 새로 vector값을 구함. 어디에도 save되지 않음. QCD_SAGE_LLM_RAG_JIRA_DB 에는 결과만 save됨.  code에는 context가 바뀌면 새로 처리되게 만들겠지만,  회의때 논의한대로 일단 처음에 set하면 끝인 것으로 구현한다.
참조 :  [^SAGE_Design_v04.pptx]

---

### [AGILEDEV-650] [ticket sage][train] Design
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:33.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T11:11:38.000+0900] db-test의 경우는 test  하기 전날까지의 ticket들에 대해서 train 한다.
jira-test의 경우는 QCD_SAGE_LLM_RAG_VECTOR 에 있는 모든 내용에 대해서 train을 한다. 

참조 :  [^SAGE_Design_v04.pptx]

---

### [AGILEDEV-649] [ticket sage][summary]Design - System Architecture Design
- **상태**: Closed | **최종 업데이트**: 2026-02-04T09:14:36.000+0900
- **티켓 본문**: System Architecture Design
- **작업 히스토리 (User Comments)**:
  - [2025-11-28T19:30:18.000+0900] 결과 : http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/summary/README.md?ref_type=heads

2개의 ticket이 적용
 * tickagesage/summary 에 Design note
 ** git : [http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git] 
 ** 
{noformat}
commit 15df0ca75a53ee2e21a1dbbecb847bf13d8f7b3a
Author: charles.lee 
Date:   Fri Nov 28 19:25:20 2025 +0900    [AGILEDEV-649] [ticket sage][summary]Design - System Architecture Design
    
    - ticketsage/summary/README.md{noformat}

 * misc/scrum_spirnt 에...
  - [2025-11-28T19:47:58.000+0900] [~sangjae0.lee]  님 , 완료하였습니다. 

2가지 해보세요.
 # Design note : [http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/summary/README.md?ref_type=heads]
 # [http://jira.lge.com/issue/secure/Dashboard.jspa?selectPageId=84103]  에서 조회 > PlantUML Diagram (TAB) > Generate Diagram  을 눌러보세요.  위의 Design Note의 내용이 ticket status에 맞게 변경됩니다.

잘 쉬시고 복귀하시면서 이런 재미난 것도 있구나 하시면 좋을듯~

미리 새해 복 많이 받으세요.

---

### [AGILEDEV-648] [ticket sage][verification] Design
- **상태**: Open | **최종 업데이트**: 2026-02-25T06:37:07.000+0900
- **티켓 본문**: 

---

### [AGILEDEV-647] [ticket sage][verification] 매일 매일 동작시 flow상으로 문제가되는 부분은 없었는지 알려주는 것
- **상태**: Open | **최종 업데이트**: 2026-02-25T06:37:27.000+0900
- **티켓 본문**: 

---

### [AGILEDEV-645] [ticket sage][verification] test시 DB화한 내용을 토대로 accuracy가 어떻게 되는지 보여주는 기능 (considered update / 일별)
- **상태**: Resolved | **최종 업데이트**: 2026-01-16T07:33:40.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-16T07:33:15.000+0900] db-report:
	uv run python -u sage.py --mode=db-report --gpt_model=exaone --embedding_model=text-embedding-3-large --debug
db-report-4o-mini:
	uv run python -u sage.py --mode=db-report --gpt_model=gpt-4o-mini --embedding_model=text-embedding-3-large --debug

---

### [AGILEDEV-642] [ticket sage][test] RAG를 이용한 결과 획득 및 DB화 할 것
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:33.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T11:16:35.000+0900] exaone으로 DB화 진행중
QCD_SAGE_LLM_RAG_DB_TEST table
  - [2026-01-13T10:15:43.000+0900] gpt-4o-mini 도 DB화 진행중
  - [2026-01-13T15:06:55.000+0900] gpt-4o-mini 는 5월까지 측정한 data를 사용한 vector / rag report :  [^sage_vector_db_report_gpt-4o-mini_text-embedding-3-large.html]    [^sage_rag_db_report_gpt-4o-mini_text-embedding-3-large.html] 
exaone은 7월까지 측정한 data를 사용한 vector / rag report :  [^sage_vector_db_report_exaone_text-embedding-3-large.html]   [^sage_rag_db_report_exaone_text-embedding-3-large.html] 

vector 의미 는 embedding-3-large만 적용한 경우 (top1,3만 찾음)
rag 의미는 이후 RAG를 적용하여 top 30 안에서 top1,3를 찾고 , reason도 설명함.


source : $  git log -1
...

---

### [AGILEDEV-639] [ticket sage][jira_test] 얼마나 자주 동작 할 것인지? process run 시간이 길어서 2개가 떠 있는 상태를 방지 필요
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:07:41.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-23T10:03:05.000+0900] 매일 -2d 로 동작을 시킨다.  아직 안 끝나도 별수 없다. 그러면 , 2개가 돌면 삽입이 2번 될수도 있기에 안됨.

작업시 llm query하는 시간이 올래 걸릴 것으로 보이니, 해당 부분에 시간 print를 넣어 check해보고 , 시간이 긴 부분에서 시간을 check하여 20시간이 지난 경우에는 강제로 quit(4) 라도록 하여 error를 발생시키게 하고 , 수동으로 작업하거나, 문제를 해결해야 할 것이다.
  - [2026-01-23T10:39:35.000+0900] {code:python}
    def check_if_long_running_time(self):
        """Exit if running time exceeds 20 hours since self.start_time."""
        elapsed = (datetime.now() - self.start_time).total_seconds()
        if elapsed > 20 * 3600:
            print(f"[ERROR] Process has been running for more than 20 hours ({elapsed/3600:.2f} hours). Exiting.")
            quit(4)
{code}

---

### [AGILEDEV-638] [ticket sage][jira_test] 하루에 1번 reset (재실행) + get jira를 제일 먼저하도록
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:07:32.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-23T10:03:37.000+0900] crontab에 넣어서 수행되게 만들어야 한다. updated >= -2d 로 설정한다.
  - [2026-01-23T14:55:33.000+0900] {noformat}
$  git log -1
commit 1035bd0ae64899f64a454e839cfd7fd4ca3b7125 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Fri Jan 23 14:54:51 2026 +0900

    [AGILEDEV-638] [ticket sage][jira_test] 하루에 1번 reset (재실행) + get jira를 제일 먼저하도록
    
    - add class VSPVS to get id,passwd from QCD_ENV
    - we will get jira data above all. then we will process jira data after finishing gathering MONGODB.
        - jira will start at 4:30 am
        - process jira data wil...
  - [2026-01-23T15:08:58.000+0900] crontab -l
{noformat}
32 7 * * *  /bin/bash /home/cheoljoo.lee/code/crontab/ticketsage/summary/daily.sh
# daily jira test
30 5 * * *  /bin/bash /home/cheoljoo.lee/code/crontab/ticketsage/db_test/daily.sh
{noformat}

daily.sh
{noformat}
#!/bin/bash
export PATH=$HOME/.local/bin:$PATH

cd /home/cheoljoo.lee/code/crontab/ticketsage/db_test ; make jira-all > /home/cheoljoo.lee/code/crontab/ticketsage/db_test/cron_daily.log  2>&1
cp /home/cheoljoo.lee/code/crontab/ticketsage/db_test/cron_...

---

### [AGILEDEV-637] [ticket sage][train] train과 test간의 (embedding vector 및 정보) interface는?  (파일/ DB)
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:35.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T10:58:15.000+0900] DB를 통해서 data를 share한다.
 !screenshot-1.png|width=1200!

---

### [AGILEDEV-636] [ticket sage][train] train 자동 update (once a day)
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:46:30.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-23T10:04:11.000+0900] 수행을 하면 DB에 쌓인 것으로 train이 되게 적용되어짐.
  - [2026-01-23T14:45:48.000+0900] train set을 만들때 resolution이  fixed 인 것만을 대상으로 할지? -> http://jira.lge.com/issue/browse/AGILEDEV-790

---

### [AGILEDEV-633] [ticket sage][train] RAG를 위한 summary prompt 확인
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:34.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2025-12-23T08:59:30.000+0900] ticketsage/summary에서 filter하는 방식을 그대로 사용할 것이다. library로 만들어 사용할 것이다.
RAG에서는 llm을 이용하여 내용을 축약하여 사용하지 않고 , 가능한 원본의 내용을 그대로 사용할 것이다.
ticketsage/summary 에서 작업해둔 내용으로 train / test data를 만들 것이다.
해당 내용에서 top 30 / 10 에 대해서 LLM (RAG)를 이용하여 더 정확한 값이 무엇인지를 찾아내는 것이다. 이때 2가지를 사용해볼 것이다. 1은 있는 내용들을 그대로 넣어주는 것.

*또 나의 실수 : RAG를 위해서는 top 30을 모두 넣을수 없기에 이를 줄여야 하고 , 이를 위해서는 summary된 것이 필요하다. 결국 RAG를 위해서라도 모든 ticket에 대한 description 에 대한 summary가 필요한 것이다. *
  - [2026-01-12T10:45:22.000+0900] 뒤에 --debug option을 붙여서 , debug file생성

uv run python -u sage.py --mode=db-test --gpt_model=exaone --embedding_model=text-embedding-3-large --date=2026-01-08 --debug  # ./debug_data/vlm*

 

 
$  cat vlm_HMCCW-17634.json
{noformat}
{
  "approach_1_assignee": [
    {
      "assignee": "minje1.kim",
      "reason": "Handles theme-related issues consistently, particularly around theme persistence and application after system events like reboot. The issues vlm=HMCCW-4441, vlm=HMCCW-15703...

---

### [AGILEDEV-632] [ticket sage][train] FUNCTION 포함하여 재학습
- **상태**: Resolved | **최종 업데이트**: 2026-01-13T10:17:15.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T10:38:17.000+0900] # embedding model에 넣을 context로 할 경우는 # SUMMARY, #DESCRIPTION, #FUNCTION을 모두 합쳐서 사용 해야 한다.
            context = f"## SUMMARY\n\n- \{summary}\n## DESCRIPTION\n\n- \{processed_description}\n## FUNCTION\n\n- \{function}"
exaone으로 학습 진행중
  - [2026-01-13T10:17:15.000+0900] 동작 완료

---

### [AGILEDEV-631] [ticket sage][train] filter 기능 설정 및 협의 / 구현 (내용이 큰 ticket)
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:34.000+0900
- **티켓 본문**: [ticket sage][train] filter 기능 설정 및 협의 / 구현 (내용이 큰 ticket)
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T10:37:13.000+0900] summary/ticketsage_llm_summary.py  구현된

process_text_for_llm()을 공통으로 사용

---

### [AGILEDEV-630] [ticket sage][summary] 중복 ticket이 없는지 파악하고 , 있으면 그에 대한 처리
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:34.000+0900
- **티켓 본문**: [ticket sage][summary] 중복 ticket이 없는지 파악하고 , 있으면 그에 대한 처리
- **작업 히스토리 (User Comments)**:
  - [2025-12-12T10:29:41.000+0900] stop when program finds the duplication.

---

### [AGILEDEV-628] [ticket sage][summary] 기능 개발 및 DB화
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:35.000+0900
- **티켓 본문**: [ticket sage][summary] 기능 개발 및 DB화
- **작업 히스토리 (User Comments)**:
  - [2025-11-26T17:55:52.000+0900] !screenshot-1.png!
  - [2025-11-26T17:57:40.000+0900] 새로운 Table을 만든다. 
ISSUE_ID , SNAPDATE , LLM 으로 만든다.

추후 Defect Agent에서 사용하는 Elastic Search를 위해서 항목별로 필드를 만드는 것은 별도록 작업
  - [2025-12-12T13:58:45.000+0900] 기본적인 구현 완료
- DL db read 하여 , 해당 ticket의 값을 받는다.
- openai 에 prompt로 문의하여 값을 얻는다.

$  git log -1
commit 21f5e2eaa5f2748b5363cc0e0969128bfd93bfad (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Fri Dec 12 13:57:08 2025 +0900
[AGILEDEV-628] [ticket sage][summary] 기능 개발 및 DB화 - POC
- POC 구현을 하였으며,
- 이후는 pvs_crawler에서 작업 예정
http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/summary/README.md?ref_type=heads



pvs_crawler에서 나머지 작업 이어서 할 예정
- model 실행할때 설정된 ...
  - [2025-12-24T10:28:28.000+0900] exaone으로 connetWide ticket 11,000 개 summary 생성 완료

RAG위한 LLM 동작중

---

### [AGILEDEV-627] [ticket sage][summary] fix prompt considered defect-agent
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:36.000+0900
- **티켓 본문**: [ticket sage][summary] Prompt fix considered defect-agent


{noformat}
당신은 소프트웨어 개발 이슈를 체계적이고 심층적으로 분석하는 전문 분석가입니다. 아래 주어진 정보를 바탕으로 다음 8개 항목에 대해 구체적이고 명확하게 분석해주세요.

기본 정보:
- ISSUE ID: {issue_id}
- SUMMARY: {summary}
- FUNCTION: {function}
- ROOT_CAUSE: {root_cause}
- ASSIGNEE: {assignee}

- DESCRIPTION:
{description}

- COMMENTS:
{comments_text}

각 섹션을 아래 형식에 맞춰 명확히 구분하여 답변해주세요. 만약 특정 항목에 대한 정보가 충분하지 않다면, '정보 부족' 또는 '확인 불가' 등으로 명확히 명시해주세요.
다음을 json 형식으로 답변해주세요. 

{{
"Assignee": "ASSIGNEE의 id를 설정해주세요.",
"Problem Analysis": {{
"Specific Issue or Bug": "이 이슈에서 발생한 구체적인 문제나 버그는 무엇인가요?",
"Symptoms and Impact": "문제의 증상과 영향범위를 설명해주세요."
}},
"Resolution Owner": {{
"Lead Resolver": "이 이슈를 주도적으로 해결한 사람은 누구인가요?",
"Final Resolver": "COMMENTS에서 해결책을 제시하거나 최종 해결을 담당한 사람을 찾아주...
- **작업 히스토리 (User Comments)**:
  - [2025-11-26T11:42:17.000+0900] collab에 비용 예측할때 정리 한 페이지가 있음 : http://collab.lge.com/main/pages/viewpage.action?pageId=3385944150
  - [2025-11-26T12:59:19.000+0900] Flow 반영 (defect agent)
{noformat}
당신은 소프트웨어 개발 이슈를 체계적이고 심층적으로 분석하는 전문 분석가입니다. 아래 주어진 정보를 바탕으로 다음 8개 항목에 대해 구체적이고 명확하게 분석해주세요.

기본 정보:
- ISSUE ID: {issue_id}
- SUMMARY: {summary}
- FUNCTION: {function}
- ROOT_CAUSE: {root_cause}
- ASSIGNEE: {assignee}

- DESCRIPTION:
{description}

- COMMENTS:
{comments_text}

각 섹션을 아래 형식에 맞춰 명확히 구분하여 답변해주세요. 만약 특정 항목에 대한 정보가 충분하지 않다면, '정보 부족' 또는 '확인 불가' 등으로 명확히 명시해주세요.
다음을 json 형식으로 답변해주세요. 

{{
"Assignee": "ASSIGNEE의 id를 설정해주세요.",
"Proble...

---

### [AGILEDEV-625] [ticket sage][summary] filter 기능 확인 (긴 description이나 comments에 대해서 어떻게 줄일지)
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:35.000+0900
- **티켓 본문**: [ticket sage][summary] filter 기능 확인 (긴 description이나 comments에 대해서 어떻게 줄일지)
- **작업 히스토리 (User Comments)**:
  - [2025-12-11T13:12:38.000+0900] [~youngjae.cho] 님 , 검토 부탁드려요.

    처리 내용:
    1. \r\n을 \n으로 정규화
    2. hex dump 패턴 제거 (0x로 시작하는 16진수 라인들)
    3. 반복되는 라인 제거 (2회 이상 연속 시 첫 번째만 유지)
    4. 의미 없는 라인 제거 (숫자/특수문자 80% 이상)
    5. 중복 문장 제거
    6. 연속된 빈 줄을 하나로 압축

def clean_and_compress_text(text)
- # 1. 반복 라인 체크 (빈 줄과 관계없이 동일 내용 연속 탐지)

- # 2. 단순 hex dump 라인 체크 (hex 값들이 공백으로 구분된 경우, 최소 20자 이상)
  # 순수 hex dump 패턴: 공백으로 구분된 hex만 있고, 최소 20자 이상인 경우
    # (짧은 문자열은 의미있는 텍스트일 수 있음: "ACE", "DEAD" 등)
    # 순수 hex dump 패턴: 공백으로 구분...
  - [2025-12-11T13:17:16.000+0900] http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/blob/main/summary/ticketsage_llm_summary.py?ref_type=heads   -> def clean_and_compress_text(text)

$  git log -1
commit 077bff23e9177cf4a6f35275d06ffef180e9f4ff (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Thu Dec 11 13:15:47 2025 +0900

    [AGILEDEV-625] [ticket sage][summary] filter 기능 확인 (긴 description이나 comments에 대해서 어떻게 줄일지)
    
    def clean_and_compress_text(text)
    1. \r\n을 \n으로 정규화
    2. hex dump 패...
  - [2025-12-11T15:52:13.000+0900] [~youngjae.cho] 님 , 의견 감사합니다.
 7번은 제 능력으로는 어렵.    
    순간적으로 언뜻 스치는 방법은,  해당 부분을 1 byte씩 뒤로 가면서 찾는 것인데요. 물론 window를 사용하 jump하면서 찾으면 좀 더 big O (operation) 를 줄일수는 있을 듯 합니다.  comments가 N 이라고 하고 length가 M 이라면 O (N* M * M) 이 될 듯 합니다.  추후 비용을 줄여야 하는 경우 고려하겠습니다.
8번은 그냥 놔둬도 될 듯.  이유는 LLM input 이 output 보다 훨씬 저렴함.

---

### [AGILEDEV-621] ticketsage 개발 환경 구축
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:35.000+0900
- **티켓 본문**: project name 선정
새로운 작업 공간 마련 (기존 코드 중 최신의 것에서 시작할수 있도록)
ground rule 마련
관련 documents 작성
- **작업 히스토리 (User Comments)**:
  - [2025-11-28T14:20:03.000+0900] http://mod.lge.com/hub/cheoljoo.lee/ticketsage/-/tree/main/ticketsage?ref_type=heads

 

각 내용들이 잘 동작하는지 확인 필요 : 확인하고 resolve
  - [2025-12-03T11:28:08.000+0900] {noformat}
$  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/ticketsage.git (push)$  git log -1
commit 9f3d9df713b9b84cf21e0d9040f5e0ef5fd322c8 (HEAD -> main, origin/main, origin/HEAD)
Author: charles.lee 
Date:   Wed Dec 3 11:13:28 2025 +0900    [AGILEDEV-621] ticketsage 개발 환경 구축
    
    - modified:   ticketsage/README.md
        - update documents (how to run)
    - modified:   ticketsage/get_data_oem.py
...

---

### [AGILEDEV-620] Ticket Sage
- **상태**: Open | **최종 업데이트**: 2026-05-28T14:15:14.000+0900
- **티켓 본문**: connect Wide에 적용할 ticket helper
회의 내용 요약 : 
**기능 개요**  
1. 새로운 티켓 생성 시, 해당 티켓과 연관성이 높은 티켓 3개의 정보를 함께 제공  
2. 제공 방식은 *comment* 형식으로 등록 예정  
3. 예시:  
   - 구성: ISSUE ID / ASSIGNEE / REASON / ISSUE 바로가기 링크  
 !screenshot-1.png! 

**향후 진행 방향**  
1. *comment* 자동 등록 시스템 구축  
   - AI를 활용해 연관성이 높은 티켓을 탐색  
   - 티켓 생성 시 실시간으로 *comment* 자동 등록  
2. *comment*에 포함될 내용에 대한 피드백 수집  
   - 문장 표현  검토  
   - 내용의 명확성과 전달력 개선  

------------------------------------

추가되는 사항 
- connect Wide에 대한 3줄 요약 (3줄은 아니고 summary를 한 내용을 의미함) 하여 DB화 한다. 
  추후 이 내용도 같이 comments로 보여줄 것이다.

---

### [AGILEDEV-617] [ResourceMgmt] 2026년 연초 동작 상황 확인 (12월말 백업 필요)
- **상태**: Resolved | **최종 업데이트**: 2026-01-07T09:38:29.000+0900
- **티켓 본문**: 2026년 연초 동작 상황 확인
- crawler의 동작을 확인해야 함.
- 날짜 관련 영향이 있는지 살펴야함.
- 2025년것을 마지막에 backup 해두어야함.  12월 말
- **작업 히스토리 (User Comments)**:
  - [2026-01-05T09:35:05.000+0900] 예산현황

- 연도를 최근의 것으로 선택하는 기능 추가 (마우스 스크롤 및 mouse point추가)

- 연구용역 선택 후 data가 없는 경우에 대한 처리 (연초에는 연구용역 결재 올라온 것이 없을때)
  - [2026-01-05T13:44:05.000+0900] 예산 현황의 데이터가 없을때 , (There is no data to download)

2025년의 데이터를 copy 해 두었습니다.

 

 $  git remote -v
origin  http://mod.lge.com/hub/cheoljoo.lee/misc.git (fetch)
origin  http://mod.lge.com/hub/cheoljoo.lee/misc.git (push)

commit c97e7710ad6bf3eff8c25486a021f8de44bd205b

---

### [AGILEDEV-606] [ticket sage][train] assignee 및 unit에 대해서도 RAG 구현 : Unit 단위로 먼저 찾고, 그 안에서 사람으로...
- **상태**: Resolved | **최종 업데이트**: 2026-02-04T09:14:35.000+0900
- **티켓 본문**: Unit 단위로 먼저 찾고, 그 안에서 사람으로...
우선 id 당 Unit 정보를 확인 해야 한다. (중복되는 것은 없는지?)
중복될 경우는 어떻게 처리할 것인지?
- **작업 히스토리 (User Comments)**:
  - [2026-01-12T11:23:08.000+0900] AGILEDEV-633 참조 : 해당 prompt로 해결 : approach 3

---

### [AGILEDEV-576] New QI / Part View component 제작 시 자동문서화
- **상태**: Closed | **최종 업데이트**: 2026-04-06T14:45:05.000+0900
- **티켓 본문**: 새 View에서는 Google Chart 사용을 지양하고, 간단한 정의가 가능한 custom component 제작.

component 제작시에는 module화 하여 제작하고 해당 feature에 대한 사용법을 포함한 문서를 제작한다
- **작업 히스토리 (User Comments)**:
  - [2025-10-16T15:50:51.000+0900] [~gina.oh] 님,

여기 관련된 다른 일도 볼수 있게 epic 하나 정해서 epic을 달았으면 합니다.

제가 assign 받으면 될까요?
  - [2025-10-28T16:01:53.000+0900] [~gina.oh] 님 , 위 내용은 숙지 했습니다.
코드 등의 위치를 알려주시면 보고 doxygen을 수행시켜보겠습니다.  추가/변경 필요하면 어떻게 할지 논의도 하구요.
  - [2025-10-30T15:52:29.000+0900] 숙제:
 # doxygen에서 여기와 같이 formatting이 가능한지?
 ## xml로 뽑아서 , 이를 해석하여 markdown으로 변환하세요.  (이걸 지원하는 open source가 있는지 찾아봐야 할 듯)
 # 소스는 [http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents?a…|http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents?at=refs%2Fheads%2Fgina%2Fvs_custom_bar_chart] 을 보시오
 # document api : http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/documents/api?at=gina%2Fvs_custom...
  - [2025-11-12T16:50:09.000+0900] Doxygen XML을 파싱하기 위해 Python에서는 doxmlparser 라이브러리(PyPI)를 사용하거나, xml.etree와 같은 XML 파싱 라이브러리를 직접 사용하여 XML 구조를 분석할 수 있습니다. 또한, doxypy와 같은 다른 파서를 사용하거나, Doxygen XML을 JSON으로 변환하는 스크립트(예: xml_to_json_parser.py)를 활용하는 방법도 있습니다.
  - [2025-11-14T09:32:14.000+0900] EXTENSION_MAPPING = js=javascript
을 Doxyfile에 추가시키면 됨.   결과를 볼수 있음. https://github.com/doxygen/doxygen/issues/8235


jsdoc 예제 blog : https://velog.io/@eunjeong/React-Doxygen
  - [2025-11-14T11:42:16.000+0900] pvs_trender 의 gina/vs_custom_bar_chart branch 밑에   
pvs_trender/src/components/globalComponents/charles  라는 directory를 만들어 작업한 내용들 모아두었습니다. 
[README.md|http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents/charles/README.md?at=refs%2Fheads%2Fgina%2Fvs_custom_bar_chart]를 보시면 됩니다.



 gina/vs_custom_bar_chart  ⬆  18?  11:38  tiger02  ~/code/…/components/globalComponents/charles  $  cheoljoopushmod 
git config credential.helper store
git push
Enu...
  - [2025-11-17T16:49:27.000+0900] http://tiger02.lge.com/cheoljoo.lee/code/pvs_trender/src/components/globalComponents/generated_api_docs/
http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents/DOXYGEN_TO_MARKDOWN_README.md?at=refs%2Fheads%2Fgina%2Fvs_custom_bar_chart
http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents/generated_api_docs/VSClusteredBarChart.md?at=refs%2Fheads%2Fgina%2Fvs_custom_bar_chart

{noformat}
    [AGILEDEV-576] a...
  - [2025-11-19T12:44:04.000+0900] http://mod.lge.com/code/projects/SWPMVIZ/repos/pvs_trender/browse/src/components/globalComponents/generated_api_docs/VSHorizontalBarChart.md?at=refs%2Fheads%2Fgina%2Fvs_custom_bar_chart

와 같이 tiger02.lge.com을 이용하여 바로 그림을 볼수 있다.
deflate_and_encode를 하여 뒤에 내용을 encode하여 붙였다. url에 바로 넣으면 그 내용을 GET하여 바로 처리를 하게 되어져있다. plantuml 진짜 잘 만들어져있다.

---

### [AGILEDEV-502] 기능 추가 : https://github.com/cheoljoo/vscode-markdown-preview-enhanced
- **상태**: Reopened | **최종 업데이트**: 2026-02-06T19:21:40.000+0900
- **티켓 본문**: 기능 추가 : plantuml server가 외부에 있을때 이를 이용하여 svg or png 를 받아서 보여주는 기능 추가
이 경우가 되면 remote 작업 github에서도 plantuml이 제대로 나오게 할수 있을 것이다.
- **작업 히스토리 (User Comments)**:
  - [2025-09-17T11:18:43.000+0900] 실제 plantuml server에 넘길때 파일을 넘기기가 힘들다.
이때는 ,  다음의 plantuml 내용을 deflate_and_encode() 하여 encoding하여 서버에 보내주어야 한다.

{noformat}
@startuml
start
#palegreen:AlarmManager.cpp 152 ~ 164;
#gold:android::sp AlarmManager::findAlarmListener(int32_t AlarmID);
: android::sp<AlarmEx;     android::sp<Ala;     android::Mutex:;
partition for {
while (  it =  liestener_list .begin(); it !=  liestener_list .end(); ++it)
:         LOGD( "Find;
if ((*it)->getAlarmID() == AlarmID) then (yes)
:             ...
  - [2025-09-17T11:29:29.000+0900] 다음과 같이 하면 바로 나옴.

svg 뒤에 들어가는 것은 puml 내용을 deflate_and_encode 한 값이다.

{noformat}
http://tiger02.lge.com:18080/svg/dL1TIyD047o_Np54IXC8WaKGOYtzYFXIyJSioJKvUhaBUnjHnFnsB_Y13nMA-p0imymEitDONv4Oxr1WOucxHtBKQBviiRYvnZYXckCmkEfBzMnO1hAVwlkNth3Uco3QQIwAyGIRPceTXAAhioeSZUk9gKD4CPNfoGdU5E9igJesx0TNxxpr33JUrb3lwhSqEP6GOBb4kiilDcLvjLraMAsKywB1fcd_iiJ8_rJHhiPqM-6S1EoV7ieqANKGpw_ZY5aFreSgbfIxMPtaqfgGTpJPl_diLk4dPHstwMyV
{noformat}

---

### [AGILEDEV-471] [LONG-TERM][Resource Manager] crawler 운영 관리
- **상태**: Holding | **최종 업데이트**: 2026-05-18T15:50:52.000+0900
- **티켓 본문**: 자동으로 동작하는 crawler 운영 관리
- 문제가 있을때의 화면을 capture해 두자.
- 해결책도 적어두자.
- **작업 히스토리 (User Comments)**:
  - [2025-08-11T08:53:58.000+0900] 주말 동작 못함. 
whale browser (sharepoint 다루는 browser) 에서 에러가 발생했었음. refresh를 제대로 못하고 에러가 발생

해결책: 에러 창을 확인 눌러주고 , 변경된 것이 없어서 다시 수행
  - [2025-09-17T12:29:47.000+0900] Stderr:
2025-09-17 06:19:06,189 - ftp_download - INFO - Successfully downloaded 202507-MM-Dashboard.xlsb to .\202507-MM-Dashboard.xlsb
2025-09-17 06:19:06,224 - ftp_download - DEBUG - 07-03-25  09:46AM              8165739 202505-MM-Dashboard.xlsb
2025-09-17 06:19:06,224 - ftp_download - DEBUG - 09-02-25  03:16PM             10412307 202507-MM-Dashboard.xlsb
2025-09-17 06:19:06,224 - ftp_download - DEBUG - 09-16-25  01:16PM             11755793 202508-MM-DashBoard.xlsb

Command: uv run pyt...

---

### [AGILEDEV-469] [newQI][CCR] process mining 고민해 볼 것 : 회사에서 필요한지! -> New CCR Design 문서 for gen2
- **상태**: Resolved | **최종 업데이트**: 2026-03-05T14:01:53.000+0900
- **티켓 본문**: !image-2025-11-25-14-17-29-878.png! 
에서 CCR 부분을 어떻게 표시해야 QI에서 도움이 될지?
- **작업 히스토리 (User Comments)**:
  - [2025-09-18T08:57:52.000+0900] PM best practice 자료
http://collab.lge.com/main/pages/viewpage.action?pageId=2721247521
  - [2025-10-31T06:46:28.000+0900] CCR
- http://jira.lge.com/issue/browse/CCR-19140   모든 내용이 채워져야 팀장이 승인을 해준다고 함.  
- 승인 받은 ticket : http://jira.lge.com/issue/browse/CCR-21651?attachmentSortBy=dateTime&attachmentOrder=asc
-  매일 정기적인 시간에 코드리뷰부터 다들 받아요...CCR필요한 사람들은..  매일 10시쯤 정기적으로 회의실 잡아 놓고 리뷰해요(거의 매일 commit이 있어서
- 베트남것도 HQ가 CCR해야 하는것으로 알고 있습니다.(요건 HQ 불만 사항이긴 한데..)
- zepher test 티켓은 현재는 ccic27만 하고 있다고 하네요. 사람이 일일이 입력 하는건 맞습니다.
  - [2026-01-28T10:25:44.000+0900] CCR 리뷰 참석 문의 메일 보낼 것
- CCR 리뷰에 참석하여 다음 사항들을 공유 받고 문의 할 예정
-- CCR 진행 방식 : CCR에서 무엇을 중요시 생각하는지?
-- CCR의 앞 뒷단에는 뭐가 있고 , 각각을 확인을 어떻게 하는지?
  - [2026-01-30T17:25:55.000+0900] 소정규 책임님 설명 내용
 !rotate -20260130_172126474.jpg|width=1200!
  - [2026-02-03T15:39:37.000+0900] [회의록 정리]
 !screenshot-1.png! 
In Review에 오면 expert task에서 리뷰
리뷰에 이상이 없으면 -> Build Request
FL은 수평전개까지 챙기고 있음.   소정규 책임님의 경우 AsIs,ToBe에 대한 내용들을 flow chart와 sequence diagram을 직접 그려주며 챙기고 있음
gerrit의 란의 gerrit들은 모두 merge가 되어져있어야 review가능.    이상한 것이 ready to merge가 되직 위해서는 FL의 +2가 필요할텐데 , 이 부분에 대해서는 status가 추가적으로 없음. (과정 좀 살펴볼 필요가 있을듯)
InReview에서 FL이 +1/+2를 준다고함. 이미 InReview에 온 상태네요.  그러면 , In Review에 온 상태에서는 Merged가 아닌 것이고, 와서 Merged로 변경되는 것임. 
Build Reuqst에서 모두 Merged가 되는 것임
Build Request에서 ...
  - [2026-02-05T19:49:22.000+0900] 참고 link:
http://collab.lge.com/main/pages/viewpage.action?pageId=3538590201
http://collab.lge.com/main/display/VSRMU/COMMIT+based+Code+Change+Request+Ticket
  - [2026-02-05T19:50:57.000+0900] 답변 : 실제 단계별로 확인을 하지 않고, Build Request 까지 완료 되는 것으로 보고 있습니다. 
 
제안 : 이 문서와 같이 단계별로 넘어가는 것을 check해서 개발자들에게 무엇이 잘못되었는지 알려주는 것은 어떨까요?  status를 변경하고 부족한 부분에 대한 comments를 주는...
- patchset의 변환 등에 대해서도 처리
  - [2026-02-06T08:50:13.000+0900] 회의때 나온 이슈들 (함명규,정희훈,정경훈C)
- build request를 할때 commit이 update가 되었다.  즉 , patchset 10번으로 승인을 하였는데 , patchset이 계속 증가한다. 이런 경우는?
- CCR은 하나라도 빠지면 rejet를 하는게 맞다. (사람마다 의견이 다름)
- build request후에 최종 merge가 된다.   이때 문제는 LAMP 같은 git들을 계속 변하고 CCC를 따로 진행하므로 해당 git 들이 모두 review가 완료되었는지 일일히 들어가서 check해봐야 한다.
- 모든 ticket을 expert팀에서 처리할수 없어서 , 각 unit들이 알아서 review하도록 한다고함.  
- (함) 꼭 check해야 하는 항목 : description (issue , anaalyze , design) , gerrit code review 를 했는지는 mandatory. 
- CCR이 잘 관리되도록 해야 한다는 의견이 나옴....
  - [2026-02-10T14:53:47.000+0900] CCR 미팅 회의록 및 follow up
http://collab.lge.com/main/pages/viewpage.action?pageId=3538590201
  - [2026-02-13T10:31:56.000+0900] 아래 collab에는 CCR 에 대한 설명이 되어져있습니다.  [COMMIT based Code Change Request Ticket|http://collab.lge.com/main/display/VSRMU/COMMIT+based+Code+Change+Request+Ticket]
 
  # 
Screening Ready Points는 진행 방향에 대해서 문의를 해두었습니다.  여기서 나오는 값들은 DB 화 예정입니다. 
 # 
팀장님께 문의 사항 :  (아래 사항은 expert task에서 요구한 내용은 아닙니다.)
 # 
각 status마다 해야 할 일들이 정해져있습니다.  (새로 renewal 되어져있습니다. CFL추가됨, reject도 추가됨)  각 status에 도달할때 얼마나 잘 지켜지고 있는지를 DB화 하고 , 몇번 굴러갔는지 (status 뒤로 가는 경우) 각 status에 머물러 있는 시간도 DB화를 한다면 , CCR 진행시 문제되는 것이 뭔지 파악하기 ...
  - [2026-03-05T14:01:06.000+0900] design 문서 : http://mod.lge.com/hub/cheoljoo.lee/ccr/-/blob/main/design_notes/gen2/README.md?ref_type=heads

---

### [AGILEDEV-425] delete를 한번에 처리하여 속도 향상
- **상태**: Resolved | **최종 업데이트**: 2026-01-28T09:37:08.000+0900
- **티켓 본문**: * SQL 문법: WHERE (SRV, ID) IN (('s1', 'u1'), ('s2', 'u2'), ...) 구문을 사용하세요.
   * `WHERE` 절 길이: 한 번의 쿼리에 수백 개에서 1,000개의 조건을 포함하는 것을 목표로 하세요.
   * 대용량 삭제: 삭제할 데이터가 수천 건을 넘는다면, 반드시 배치(batch) 처리를 구현하여 시스템 부하와 락 경합을 최소화해야 합니다.
   * 커밋 시점: 각 배치가 성공적으로 완료될 때마다 COMMIT을 실행하여 트랜잭션을 짧게 유지하는 것이 좋습니다.


   1 DELETE FROM YourTable
   2 WHERE (SRV, ID) IN (
   3     ('server1', 'userA'),
   4     ('server2', 'userB'),
   5     ('server3', 'userC'),
   6     ...
   7     ('serverN', 'userZ')
   8 );


    1 def delete_data_in_batches(data_pairs, batch_size=500):
    2     """
    3     주어진 (SRV, ID) 쌍 리스트를 배치 단위로 나누어 삭제합니다.
    4
    5     Args:
    6         data_pairs (list): ('server1', 'userA') 형태의 튜플 리스트
    7         batch_size (int): 한 번의 DELETE 문으로 처리할 쌍의 개수
    8     """
   ...
- **작업 히스토리 (User Comments)**:
  - [2025-07-09T12:19:04.000+0900] 위의 idea에 의하면 NO 를 이용하여 , 지워주면  indexing이 되어 엄청 빠를 듯
  - [2025-07-11T05:19:08.000+0900] http://jira.lge.com/issue/browse/AGILEDEV-427  에서 UPDATE에 대한 성능 향상이 있으니 참조하면 됨.
  - [2026-01-28T09:37:08.000+0900] 이미 NO 기준으로 update 구현 완료

---

### [AGILEDEV-397] collab page에 대해서 문제가 될는 부분을 실행 초기에 판단할수 있는 코드 필요 - 에러나 warning 만이라도 보여주자.
- **상태**: Resolved | **최종 업데이트**: 2026-02-26T16:19:14.000+0900
- **티켓 본문**: collab page에 대해서 문제가 될는 부분을 실행 초기에 판단할수 있는 코드 필요
- 에러나 warning 만이라도 보여주자.

우리가 collab 기준으로 download하는 페이지가 이거 한가지 인가요?
페이지는 개발 dev 운용일 때 dev 붙지 않은 겁니다. 한 가지가 맞습니다. 
그게 아니면 , 또 collab등 pvs_crawler 소스 외에 영향을 받는 것이 무엇이 있을까요?
서버 상태에 따라서 에러 발생합니다. 
소스 외에 영향을 주는 것들이 변경되어졌을때 , 어디가 문제인지 쉽게 알수 있는 방법은 있을까요?
쉽게 알 방법이 없습니다. collab에 문제는 결국에는 수집을 통해서 에러를 알 수 있습니다. 


안녕하세요 Agile Unit 이상재 선임입니다. 
@이철주/책임연구원/Agile개발Unit님 
좋은 의견 감사합니다. 
ISSUE EXCEL DEV/ISSUE EXCEL 에 diff 를 떠서 실행시에 로그에 보여주는 방식으로 하려고 합니다. 

다만, verify 방식은 어려울 것 같습니다. 
우선 ISSUE EXCEL DEV/ISSUE EXCEL 이 다른 경우도 있습니다. 
바로 반영이 하지 않고, 테스트 용도로 내용을 쓰기 때문입니다. 
그리고 반영 주체도 저와 이정미 책임님이 각각 쓰기 때문에 내용이 상이 할 수 있습니다. 

그리고 diff를 보여줘도 수동 방식은 그대로 가져가야 합니다. 
사유는 아래와 같습니다. 
1. DIFF 볼 때 결국에는 개발 서버에서만 확인 가능 -> 실제 운용 서버 엑셀에 문제 발생
2. verify가 불...
- **작업 히스토리 (User Comments)**:
  - [2026-02-26T16:19:14.000+0900] 자체적으로 3단계 check 하는 방식으로 해결된듯!

---

### [AGILEDEV-279] adu-기타
- **상태**: Open | **최종 업데이트**: 2026-05-20T13:57:27.000+0900
- **티켓 본문**: 어디에 속하지 않는 이것 저것

---

### [AGILEDEV-39] [POC] inline comments : 상관관계 구하기 위한 field 추가 및 crawling
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:34:13.000+0900
- **티켓 본문**: http://vlm.lge.com/issue/browse/SWPMSWDEVE-1155

[POC] inline comments : 
상관관계 구하기 위한 crawling : 
변경된 source code 양 : VLM : VLM 처리 시간 : Patchset 수 : reject 횟수 : inline comments수
- **작업 히스토리 (User Comments)**:
  - [2025-04-21T08:43:44.000+0900] - 변경 소스의 양과 comments의 양 비교 (inline comments양) : 많은 코드에 대해서도 comments들이 잘 이루어지고 있는지?
변경 소스 양과 comments의 상관관계를 구해보자. (더 클수록 review가 더 안될 듯 하다.) - 이 경우 commit단 변경 소스 양을 줄이는 작업을 해야만 품질이 좋아짐
comments를 형식적으로 하는 부분에 대한 구분 필요
commit 이후 merge 될때까지의 시간  : commit +2 점을 받기까지의 시간
ticket과 연결된 ticket의 자료를 보고 어떤 type인지 뽑아내어 project / OEM / QE 등 어느 부분인지 뽑아낸다.
  - [2026-02-26T16:18:18.000+0900] 상관관계를 결과를 AI 에 문의를 해본다. 
필요한 data를 뽑아서 넣어주면 된다.  
http://mod.lge.com/hub/cheoljoo.lee/publish/-/blob/main/lge/linux-copilot-cli-setup-korean.md?ref_type=heads
  - [2026-04-09T11:34:13.000+0900] 요청이 있을시 처리

---

### [AGILEDEV-32] c/c++ 외에 java 언어 추가
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:32:58.000+0900
- **티켓 본문**: c/c++ 외에 java / cotlin 언어 추가
- **작업 히스토리 (User Comments)**:
  - [2025-04-21T08:40:20.000+0900] 📚 Doxygen이 지원하는 언어
C, C++

Java ✅

Python

Objective-C

C#

PHP

IDL

Fortran

VHDL

etc...

즉, Java는 공식적으로 Doxygen이 완전히 지원하는 언어 중 하나야.


/**
 * 이 클래스는 테스트용입니다.
 */
public class TestClass {
    
    /**
     * 이 메서드는 값을 더합니다.
     * @param a 첫 번째 정수
     * @param b 두 번째 정수
     * @return 두 수의 합
     */
    public int add(int a, int b) {
        return a + b;
    }
}


OPTIMIZE_OUTPUT_JAVA = YES
FILE_PATTERNS         = *.java
EXTRACT_ALL           = YES...
  - [2026-04-09T11:32:58.000+0900] AI 로 대치

---

### [AGILEDEV-31] 주석 삭제
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:33:16.000+0900
- **티켓 본문**: 합친후에 주석 삭제
- **작업 히스토리 (User Comments)**:
  - [2026-04-09T11:33:16.000+0900] AI 로 대치

---

### [AGILEDEV-30] function 단위 처리
- **상태**: Resolved | **최종 업데이트**: 2026-04-09T11:33:41.000+0900
- **티켓 본문**: 파일을 원복 시킨후에 doxygen을 이용하여 분석을 해서 , 함수가 변한 것이 있는지? return이 변한 것이있는지를 확인
class도 마찬가지로 변한 것이 있는지 확인

global variable에 대해서도 마찬가지로 해석 필요
- **작업 히스토리 (User Comments)**:
  - [2026-04-09T11:33:41.000+0900] AI 로 대치

---

### [AGILEDEV-25] adu-[Resource Management] 협력사 비용 및 MM 가시화
- **상태**: In Progress | **최종 업데이트**: 2026-05-08T13:27:41.000+0900
- **티켓 본문**: 
- **작업 히스토리 (User Comments)**:
  - [2025-04-04T23:32:33.000+0900] label "제외된Epic_Agile개발Unit(2025)" 일때 보이지 않게 set된다고 함

---

### [AGILEDEV-24] adu-[Gerrit] Inline Commit 수치 개발
- **상태**: In Progress | **최종 업데이트**: 2026-01-13T16:55:41.000+0900
- **티켓 본문**: 

---

