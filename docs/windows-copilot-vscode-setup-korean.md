# LGE MCP-Atlassian 설치 및 사용 가이드

> **대상**: LGE 내부 개발자 (초보자용)  
> **버전**: 2.1.0  
> **패키지**: MCP server for Atlassian (Confluence and Jira) integration  
> **환경**: LGE 내부망 (http://jira.lge.com, http://collab.lge.com)

---

## 🎯 이 가이드는 무엇인가요?

이 문서는 VS Code에서 GitHub Copilot과 함께 **LGE Jira/Confluence를 자동으로 연동**하여 사용할 수 있도록 도와주는 가이드입니다.

**할 수 있는 일:**
- 💬 Copilot에게 "CCR-30895 이슈 정보 알려줘" 라고 물어보면 자동으로 Jira에서 가져옴
- 📄 "Confluence 페이지 3564252579 내용 요약해줘" 라고 요청 가능
- 🔍 "내가 담당한 이슈 목록 보여줘" 같은 자연어 명령 사용
- ✍️ Confluence 페이지 생성/수정, Jira 댓글 추가 등 자동화

---

## 📦 1단계: MCP-Atlassian 설치하기

### 방법 1: VS Code 터미널에서 설치 (권장)

1. **VS Code 실행**
2. **터미널 열기**: `Ctrl + `` (백틱) 또는 상단 메뉴 > Terminal > New Terminal
3. **작업 폴더로 이동**:
   ```powershell
   cd D:\PVS\mcp
   ```

4. **패키지 설치**:
   ```powershell
   npm install mcp-atlassian
   npm install @modelcontextprotocol/server-sequential-thinking
   ```

   ✅ 설치 성공 시: `node_modules` 폴더에 각 패키지 폴더 생성됨

### 방법 2: 이미 설치되어 있는지 확인

```powershell
# 설치 확인
Test-Path "D:\PVS\mcp\node_modules\mcp-atlassian"
Test-Path "D:\PVS\mcp\node_modules\@modelcontextprotocol\server-sequential-thinking"
```
- `True` 출력 → 이미 설치됨, 다음 단계로
- `False` 출력 → 방법 1로 설치 필요

---

## 📚 설치되는 MCP 서버 소개

### 1️⃣ MCP Atlassian Server
- **목적**: LGE Jira 및 Confluence와 통합
- **Jira URL**: http://jira.lge.com/issue
- **Confluence URL**: http://collab.lge.com/main
- **인증**: Personal Access Token 사용
- **SSL 검증**: 비활성화됨 (내부 시스템)

**사용 가능한 주요 도구:**
- `search_jira_issues`: JQL을 사용한 Jira 이슈 검색
- `read_jira_issue`: 특정 Jira 이슈의 상세 정보 조회
- `search_confluence_pages`: CQL을 사용한 Confluence 페이지 검색
- `read_confluence_page`: 특정 Confluence 페이지의 내용 조회
- `create_confluence_page`: 새 Confluence 페이지 생성
- `update_confluence_page`: 기존 페이지 업데이트
- `add_jira_comment`: Jira 이슈에 댓글 추가

### 2️⃣ MCP Sequential Thinking Server
- **목적**: 순차적 사고 및 구조화된 추론 기능
- **기능**: 단계별 분석, 문제 해결 프레임워크 제공

**사용 가능한 도구:**
- `start_thinking`: 새로운 사고 프로세스 시작
- `add_thinking_step`: 사고 프로세스에 단계 추가
- `get_thinking_process`: 전체 사고 체인 검토
- `analyze_reasoning`: 추론 분석 및 인사이트 제공
- `structured_thinking`: 구조화된 사고 방법론 적용
  - **First Principles** (제1원리): 근본부터 다시 생각하기
  - **5 Whys** (5가지 이유): 근본 원인 파악
  - **SWOT 분석**: 강점/약점/기회/위협 분석
  - **Reverse Engineering** (역공학): 결과로부터 과정 추론

---

## 🔑 2단계: LGE Personal Access Token 발급받기

### Jira 토큰 발급

1. **Jira 접속**: http://jira.lge.com/issue
2. **우측 상단 프로필 아이콘** 클릭
3. **"Personal Access Tokens"** 메뉴 선택
4. **"Create token"** 버튼 클릭
5. 토큰 이름 입력 (예: "MCP-Atlassian-VSCode")
6. **생성된 토큰 복사** (⚠️ 다시 볼 수 없으니 바로 복사!)
7. 안전한 곳에 임시 저장 (메모장 등)

### Confluence 토큰 발급

1. **Confluence 접속**: http://collab.lge.com
2. **우측 상단 프로필 아이콘** 클릭
3. **"Personal Access Tokens"** 메뉴 선택
4. **"Create token"** 버튼 클릭
5. 토큰 이름 입력 (예: "MCP-Atlassian-VSCode")
6. **생성된 토큰 복사** (⚠️ 다시 볼 수 없으니 바로 복사!)
7. 안전한 곳에 임시 저장 (메모장 등)

> 💡 **팁**: 두 토큰을 메모장에 다음과 같이 정리해두세요:
> ```
> Jira Token: aBc123DeF456GhI789JkL012MnO345PqR678StU901VwX234Yz...
> Confluence Token: xYz987WvU654TsR321PoN098MlK765JiH432GfE109DcB876Aa...
> ```

---

## ⚙️ 3단계: VS Code MCP 설정하기

### 3-1. mcp.json 파일 열기

1. **Windows 탐색기 열기**: `Win + E`
2. **주소창에 입력**:
   ```
   %APPDATA%\Code\User
   ```
3. **Enter 키** → VS Code 설정 폴더로 이동
4. **mcp.json 파일 찾기**
   - 있으면: 해당 파일을 VS Code로 열기
   - 없으면: VS Code에서 새로 만들기 (다음 단계)

### 3-2. mcp.json 파일 생성/편집

**VS Code에서 파일 열기:**
- `Ctrl + O` 누르고
- `%APPDATA%\Code\User\mcp.json` 입력
- "파일을 찾을 수 없습니다" 나오면 "확인" 클릭 (새로 만들어짐)

**아래 내용을 복사해서 붙여넣기:**

```json
{
  "servers": {
    "mcp-atlassian": {
      "command": "node",
      "args": ["D:\\PVS\\mcp\\node_modules\\mcp-atlassian\\dist\\index.js"],
      "type": "stdio",
      "env": {
        "JIRA_URL": "http://jira.lge.com/issue",
        "JIRA_PERSONAL_TOKEN": "여기에_위에서_복사한_Jira_토큰_붙여넣기",
        "JIRA_SSL_VERIFY": "false",
        "CONFLUENCE_URL": "http://collab.lge.com",
        "CONFLUENCE_PERSONAL_TOKEN": "여기에_위에서_복사한_Confluence_토큰_붙여넣기",
        "CONFLUENCE_SSL_VERIFY": "false",
        "MCP_VERBOSE": "true"
      }
    },
    "sequential-thinking": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-sequential-thinking"],
      "type": "stdio"
    }
  }
}
```

**⚠️ 중요: 토큰 교체하기**
- `"여기에_위에서_복사한_Jira_토큰_붙여넣기"` → 2단계에서 복사한 Jira 토큰으로 교체
- `"여기에_위에서_복사한_Confluence_토큰_붙여넣기"` → 2단계에서 복사한 Confluence 토큰으로 교체
- **큰따옴표(")는 그대로 유지**

**예시:**
```json
"JIRA_PERSONAL_TOKEN": "qR7sT9uV2wX4yZ6aB8cD0eF3gH5iJ1kL4mN7oP0qR2sT5u...",
"CONFLUENCE_PERSONAL_TOKEN": "zY6xW4vU2tS0rQ9pO7nM5lK3jI1hG9fE7dC5bA3zA1yX9w...",
```

**저장**: `Ctrl + S`

### 3-3. Gerrit 서버 설정 (선택사항)

LAMP Gerrit 코드 리뷰 시스템도 함께 사용하려면:

#### Gerrit HTTP Password 발급

1. **Gerrit 접속**: http://lamp.lge.com/review
2. **우측 상단 사용자 아이콘** 클릭 > **Settings**
3. **좌측 메뉴에서 "HTTP Credentials"** 선택
4. **"Generate New Password"** 버튼 클릭
5. **생성된 비밀번호 복사** (⚠️ 재표시 안됨!)

#### mcp.json에 Gerrit 서버 추가

기존 mcp.json의 `"servers"` 섹션에 추가:

```json
{
  "servers": {
    "mcp-atlassian": { ... },
    "sequential-thinking": { ... },
    "lamp-gerrit": {
      "command": "node",
      "args": ["D:\\PVS\\mcp\\servers\\lamp-gerrit-server.js"],
      "type": "stdio",
      "env": {
        "GERRIT_URL": "http://lamp.lge.com/review",
        "GERRIT_USERNAME": "여기에_본인_LGE_아이디",
        "GERRIT_HTTP_PASSWORD": "여기에_위에서_복사한_HTTP_Password",
        "GERRIT_SSL_VERIFY": "false",
        "MCP_VERBOSE": "true"
      }
    }
  }
}
```

**⚠️ 주의**: Gerrit 서버를 사용하려면 `D:\PVS\mcp\servers\lamp-gerrit-server.js` 파일이 필요합니다.

**저장**: `Ctrl + S`

### 3-4. settings.json 설정 (선택사항)

MCP 서버를 수동으로 시작하려면 (권장):

1. **VS Code 설정 열기**: `Ctrl + ,`
2. **우측 상단 "설정 열기(JSON)" 아이콘** 클릭 (파일 아이콘)
3. **아래 내용 추가**:

```json
{
  "chat.mcp.gallery.enabled": true,
  "chat.mcp.autoStart": false
}
```

**설명:**
- `gallery.enabled`: MCP 서버 목록 표시
- `autoStart: false`: VS Code 시작 시 자동 시작 안 함 (필요할 때만 시작, 빠른 시작)

**저장**: `Ctrl + S`

---

## 🚀 4단계: VS Code 재시작 및 테스트

### 4-1. VS Code 완전히 재시작

1. VS Code **모든 창 닫기**
2. VS Code **다시 실행**

### 4-2. MCP 서버 연결 확인

1. **GitHub Copilot Chat 열기**: `Ctrl + Alt + I` 또는 좌측 채팅 아이콘
2. **Chat 창 상단 `@` 버튼** 클릭
3. **사용 가능한 MCP 서버 확인**:
   - ✅ `mcp-atlassian` - Jira/Confluence 연동
   - ✅ `sequential-thinking` - 순차적 사고
   - ✅ `lamp-gerrit` - Gerrit 코드 리뷰 (설정한 경우)

   ✅ 보이면: 설정 성공!  
   ❌ 안 보이면: 3단계 설정 다시 확인

### 4-3. 실제 동작 테스트

**Copilot Chat 창에 다음 명령 입력:**

```
@mcp-atlassian CCR-30895 이슈 정보 알려줘
```

또는

```
@mcp-atlassian 내가 담당한 이슈 목록 보여줘
```

✅ **성공**: Jira에서 실제 데이터를 가져와서 표시  
❌ **실패**: 오류 메시지 확인 → 5단계 문제 해결 참고

---

## 💡 5단계: Copilot Chat에서 자주 사용하는 명령어 예시

> **📍 사용 위치**: VS Code의 GitHub Copilot Chat 창 (`Ctrl + Alt + I`)  
> **💬 입력 방법**: 아래 명령어를 Chat 창에 그대로 입력하면 됩니다

### Jira 관련

```
# 특정 이슈 조회
@mcp-atlassian AGILEDEV-844 이슈 상세 정보 알려줘

# 내 할당 이슈 목록
@mcp-atlassian 나한테 할당된 이슈 목록 보여줘

# 프로젝트의 열린 이슈 검색
@mcp-atlassian CCR 프로젝트에서 Open 상태인 이슈 찾아줘

# 이슈에 댓글 추가
@mcp-atlassian CCR-30895에 "검토 완료했습니다" 댓글 추가해줘
```

### Jira 이슈 심층 분석 (Sequential Thinking 활용)

```
# 이슈 원인 분석
@mcp-atlassian @sequential-thinking CCR-30895 이슈를 분석해서 근본 원인을 단계별로 추론해줘. 
증상, 재현 조건, 관련 컴포넌트, 예상 원인을 순차적으로 분석해줘.

# 소스 코드 구조 분석
@mcp-atlassian @sequential-thinking CCR-30895 이슈를 해결하기 위해 필요한 소스 코드 구조를 분석해줘.
1) 관련 파일 식별
2) 함수 호출 흐름 추적
3) 의존성 관계 파악
4) 수정이 필요한 부분 우선순위화

# 이슈 해결 전략 수립
@mcp-atlassian @sequential-thinking CCR-30895 해결을 위한 단계별 전략을 세워줘.
현재 상태 파악 → 문제 격리 → 해결 방안 도출 → 테스트 계획 → 배포 전략 순으로 상세히 설명해줘.

# 유사 이슈 패턴 분석
@mcp-atlassian @sequential-thinking CCR 프로젝트에서 CCR-30895와 유사한 이슈들을 찾아서 패턴을 분석해줘.
공통점, 차이점, 반복되는 근본 원인, 예방 방법을 단계적으로 도출해줘.

# 영향도 분석
@mcp-atlassian @sequential-thinking CCR-30895 수정이 시스템에 미칠 영향을 분석해줘.
직접 영향 → 간접 영향 → 리스크 요소 → 테스트 범위 순으로 체계적으로 정리해줘.

# 리팩토링 필요성 판단
@mcp-atlassian @sequential-thinking CCR-30895를 보고 관련 코드의 리팩토링 필요성을 판단해줘.
현재 코드 품질 평가 → 기술 부채 식별 → 개선 우선순위 → 리팩토링 계획 제시
```

### Confluence 관련

```
# 페이지 ID로 내용 조회
@mcp-atlassian Confluence 페이지 3564252579 내용 요약해줘

# 페이지 검색
@mcp-atlassian "MCP 설치" 키워드로 Confluence 페이지 검색해줘

# 최근 페이지 조회
@mcp-atlassian 내가 최근에 본 Confluence 페이지 목록 보여줘

# 페이지 생성
@mcp-atlassian "테스트 페이지" 제목으로 새 Confluence 페이지 만들어줘
```

### Gerrit 관련 (선택사항)

```
# Change 정보 조회
@lamp-gerrit Change 280419 정보 알려줘

# 파일 변경 내역 확인
@lamp-gerrit Change 280419의 파일 변경 내역 보여줘

# 리뷰어 및 점수 확인
@lamp-gerrit Change 280419 리뷰어 정보와 점수 알려줘

# Change 검색
@lamp-gerrit main 브랜치에서 merge된 Change 최근 10개 찾아줘

# Sequential Thinking으로 코드 리뷰
@lamp-gerrit @sequential-thinking Change 280419를 상세히 분석해줘:
- 변경 내용 요약
- 코드 품질 평가
- 잠재적 이슈 식별
- 개선 제안
```

### 복합 작업

```
# 이슈 분석 후 Confluence 페이지 생성
@mcp-atlassian CCR-30895 이슈 분석해서 요약 페이지 만들어줘

# 여러 페이지 비교
@mcp-atlassian 페이지 3564252579와 1896449377 비교해줘
```

---

## 🔍 6단계: 문제 해결

### ❌ "mcp-atlassian이 목록에 없어요"

**원인**: mcp.json 설정 오류

**해결책:**
1. `%APPDATA%\Code\User\mcp.json` 파일 확인
2. JSON 문법 오류 확인 (쉼표, 중괄호 등)
3. 경로 확인: `D:\\PVS\\mcp\\node_modules\\mcp-atlassian\\dist\\index.js`
4. VS Code 완전히 재시작

### ❌ "API 연결 실패" 또는 "인증 오류"

**원인**: 토큰이 잘못되었거나 만료됨

**해결책:**
1. Jira/Confluence에서 토큰 재발급
2. mcp.json에서 토큰 다시 확인
3. 토큰 앞뒤 공백 제거 확인
4. 큰따옴표(") 포함 여부 확인 (포함하면 안 됨)

### ❌ "권한이 없습니다"

**원인**: 해당 프로젝트/스페이스 접근 권한 없음

**해결책:**
1. 웹 브라우저에서 직접 Jira/Confluence 접속
2. 해당 이슈/페이지에 접근 가능한지 확인
3. 프로젝트 관리자에게 권한 요청

### ❌ "검색 결과가 없어요"

**원인**: CQL/JQL 문법 오류 또는 실제 데이터 없음

**해결책:**
1. Copilot에게 더 구체적으로 요청
2. 웹에서 먼저 검색해서 데이터 존재 확인
3. 프로젝트명, 스페이스명 정확히 입력

### ❌ "MCP 서버가 시작되지 않아요"

**원인**: Node.js 또는 패키지 설치 문제

**해결책:**
```powershell
# Node.js 버전 확인 (v18 이상 권장)
node --version

# mcp-atlassian 재설치
cd D:\PVS\mcp
npm install mcp-atlassian

# VS Code 재시작
```

---

## 📚 7단계: 사용 가능한 기능 목록

### Confluence 기능 (13개)

| 기능 | 설명 | 예시 명령 |
|------|------|----------|
| `get_confluence_current_user` | 로그인 사용자 정보 | "내 Confluence 정보 알려줘" |
| `read_confluence_page` | 페이지 읽기 | "페이지 3564252579 내용 보여줘" |
| `search_confluence_pages` | 페이지 검색 | "MCP 키워드로 검색해줘" |
| `list_confluence_spaces` | 스페이스 목록 | "스페이스 목록 보여줘" |
| `create_confluence_page` | 페이지 생성 | "새 페이지 만들어줘" |
| `update_confluence_page` | 페이지 수정 | "페이지 내용 업데이트해줘" |
| `export_confluence_page` | HTML/Markdown 내보내기 | "페이지를 마크다운으로 내보내줘" |
| `list_confluence_attachments` | 첨부파일 목록 | "첨부파일 목록 보여줘" |
| `download_confluence_attachment` | 첨부파일 다운로드 | "첨부파일 다운로드해줘" |
| `upload_confluence_attachment` | 파일 업로드 | "파일 업로드해줘" |
| `add_confluence_comment` | 댓글 추가 | "페이지에 댓글 추가해줘" |
| `add_confluence_page_label` | 라벨 추가 | "라벨 추가해줘" |
| `get_my_recent_confluence_pages` | 최근 페이지 | "최근 본 페이지 보여줘" |

### Jira 기능 (9개)

| 기능 | 설명 | 예시 명령 |
|------|------|----------|
| `get_jira_current_user` | 로그인 사용자 정보 | "내 Jira 정보 알려줘" |
| `read_jira_issue` | 이슈 상세 조회 | "CCR-30895 보여줘" |
| `search_jira_issues` | 이슈 검색 (JQL) | "Open 상태 이슈 찾아줘" |
| `list_jira_projects` | 프로젝트 목록 | "프로젝트 목록 보여줘" |
| `list_jira_boards` | 보드 목록 | "보드 목록 보여줘" |
| `list_jira_sprints` | 스프린트 목록 | "스프린트 목록 보여줘" |
| `create_jira_issue` | 이슈 생성 | "새 이슈 만들어줘" |
| `add_jira_comment` | 댓글 추가 | "이슈에 댓글 추가해줘" |
| `get_my_jira_issues` | 내 할당 이슈 | "나한테 할당된 이슈 보여줘" |
| ~~`attach_jira_file`~~ | 파일 첨부 (**MCP 미지원**) | PowerShell REST API 직접 호출 필요 |

> ⚠️ **Jira 파일 첨부는 MCP 미지원** — 아래 PowerShell 스크립트로 직접 첨부하세요:
> ```powershell
> $token = "YOUR_JIRA_TOKEN"
> $issueKey = "AGILEDEV-809"
> $filePath = "D:\PVS\mcp\파일명.md"
> Add-Type -AssemblyName System.Net.Http
> $handler = New-Object System.Net.Http.HttpClientHandler
> $handler.ServerCertificateCustomValidationCallback = { $true }
> $client = New-Object System.Net.Http.HttpClient($handler)
> $client.DefaultRequestHeaders.Add("Authorization", "Bearer $token")
> $client.DefaultRequestHeaders.Add("X-Atlassian-Token", "no-check")
> $content = New-Object System.Net.Http.MultipartFormDataContent
> $fileStream = [System.IO.File]::OpenRead($filePath)
> $fileContent = New-Object System.Net.Http.StreamContent($fileStream)
> $fileContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse("text/markdown")
> $content.Add($fileContent, "file", [System.IO.Path]::GetFileName($filePath))
> $response = $client.PostAsync("http://jira.lge.com/issue/rest/api/2/issue/$issueKey/attachments", $content).Result
> Write-Host "HTTP: $($response.StatusCode)"
> $fileStream.Close(); $client.Dispose()
> ```

### Sequential Thinking 기능 (5개)

| 기능 | 설명 | 사고 방법론 |
|------|------|-------------|
| `start_thinking` | 사고 프로세스 시작 | - |
| `add_thinking_step` | 단계 추가 | - |
| `get_thinking_process` | 사고 체인 검토 | - |
| `analyze_reasoning` | 추론 분석 | - |
| `structured_thinking` | 구조화된 사고 | First Principles, 5 Whys, SWOT, Reverse Engineering |

### Gerrit 기능 (6개, 선택사항)

| 기능 | 설명 | 예시 명령 |
|------|------|----------|
| `gerrit_get_change` | Change 기본 정보 | "Change 280419 정보 알려줘" |
| `gerrit_get_files` | 파일 변경 내역 | "파일 변경 내역 보여줘" |
| `gerrit_get_reviewers` | 리뷰어 정보 | "리뷰어 점수 알려줘" |
| `gerrit_get_comments` | 리뷰 코멘트 | "코멘트 내용 보여줘" |
| `gerrit_search_changes` | Change 검색 | "main 브랜치 Change 찾아줘" |
| `gerrit_analyze_change` | 통합 분석 | "Change 전체 분석해줘" |

---

## 🎓 8단계: 실전 활용 시나리오

### 시나리오 1: 주간 보고서 작성

```
1. @mcp-atlassian 이번 주 내가 작업한 이슈 목록 가져와줘
2. @mcp-atlassian 이슈들을 분석해서 주간 보고서 초안 만들어줘
3. @mcp-atlassian Confluence에 "Y26W08 주간보고" 페이지 생성해줘
```

### 시나리오 2: 이슈 분석 및 공유

```
1. @mcp-atlassian CCR-30895 이슈 상세 분석해줘
2. @mcp-atlassian 관련 이슈들도 같이 찾아줘
3. @mcp-atlassian 분석 결과를 Confluence 페이지로 만들어줘
```

### 시나리오 2-1: Sequential Thinking으로 심층 이슈 분석

```
1. @mcp-atlassian CCR-30895 이슈 정보를 가져와줘
2. @sequential-thinking 위 이슈의 근본 원인을 다음 순서로 분석해줘:
   - 증상 분석
   - 재현 조건 파악
   - 관련 컴포넌트 식별
   - 로그/스택 트레이스 분석
   - 예상 원인 도출
3. @mcp-atlassian 분석 결과를 "CCR-30895 근본원인분석" 제목으로 Confluence 페이지 생성해줘
```

### 시나리오 3: 프로젝트 현황 파악

```
1. @mcp-atlassian CCR 프로젝트 Open 이슈 통계 보여줘
2. @mcp-atlassian 우선순위 High인 이슈 목록
3. @mcp-atlassian 지연된 이슈 있는지 확인해줘
```

### 시나리오 4: 코드 구조 분석 및 해결 전략 수립

```
1. @mcp-atlassian CCR-30895 이슈 가져와줘
2. @sequential-thinking 이 이슈 해결을 위한 코드 분석을 다음 순서로 해줘:
   Step 1: 관련 소스 파일 식별
   Step 2: 함수/메서드 호출 흐름 추적
   Step 3: 데이터 흐름 분석
   Step 4: 의존성 관계 파악
   Step 5: 수정 필요 부분과 영향 범위 예측
3. @sequential-thinking 위 분석을 바탕으로 해결 전략을 수립해줘:
   - 단기 해결 방안 (핫픽스)
   - 중기 해결 방안 (리팩토링)
   - 장기 개선 방안 (아키텍처)
4. @mcp-atlassian 분석 및 전략을 "CCR-30895 해결전략" 페이지로 Confluence에 생성해줘
```

### 시나리오 5: 유사 이슈 패턴 분석 및 예방책 마련

```
1. @mcp-atlassian CCR 프로젝트에서 "NullPointerException" 키워드로 이슈 검색해줘
2. @sequential-thinking 검색된 이슈들의 패턴을 분석해줘:
   - 공통 발생 조건
   - 주요 발생 모듈/컴포넌트
   - 반복되는 근본 원인
   - 수정 후 재발 여부
3. @sequential-thinking 위 분석을 바탕으로 예방책을 제시해줘:
   - 코딩 가이드라인 개선
   - 정적 분석 도구 활용
   - 단위 테스트 강화 방안
   - 코드 리뷰 체크리스트
4. @mcp-atlassian "NullPointerException 예방 가이드" 페이지 생성해줘
```

### 시나리오 6: Gerrit 코드 리뷰 자동화 (선택사항)

```
1. @lamp-gerrit Change 280419 정보와 파일 변경 내역 가져와줘
2. @sequential-thinking 위 Change를 다음 관점에서 분석해줘:
   - 코드 품질 (가독성, 유지보수성)
   - 잠재적 버그 (널 체크, 예외 처리)
   - 성능 영향도
   - 보안 취약점
   - 테스트 커버리지
3. @sequential-thinking 개선 제안을 우선순위별로 정리해줘:
   - Critical (반드시 수정)
   - High (수정 권장)
   - Medium (개선 고려)
   - Low (참고 사항)
4. @lamp-gerrit Change 280419에 리뷰 의견 댓글 추가해줘
5. @mcp-atlassian "Change 280419 코드 리뷰 리포트" Confluence 페이지 생성해줘
```

---

## 🔗 참고 링크

- **LGE Jira**: http://jira.lge.com/issue
- **LGE Confluence**: http://collab.lge.com
- **LGE Gerrit**: http://lamp.lge.com/review
- **Confluence CQL 검색 문법**: https://confluence.atlassian.com/doc/confluence-search-syntax-158720.html
- **Jira JQL 검색 문법**: https://support.atlassian.com/jira-software-cloud/docs/use-advanced-search-with-jira-query-language-jql/
- **Gerrit 검색 문법**: https://gerrit-review.googlesource.com/Documentation/user-search.html

---

## 📊 현재 설치 상태 체크리스트

- [ ] Node.js 설치 확인 (`node --version`)
- [ ] mcp-atlassian 패키지 설치 (`D:\PVS\mcp\node_modules\mcp-atlassian`)
- [ ] sequential-thinking 패키지 설치 (`D:\PVS\mcp\node_modules\@modelcontextprotocol\server-sequential-thinking`)
- [ ] Jira Personal Access Token 발급
- [ ] Confluence Personal Access Token 발급
- [ ] (선택) Gerrit HTTP Password 발급
- [ ] mcp.json 파일 설정 (`%APPDATA%\Code\User\mcp.json`)
- [ ] VS Code 재시작
- [ ] Copilot Chat에서 @mcp-atlassian 확인
- [ ] Copilot Chat에서 @sequential-thinking 확인
- [ ] (선택) Copilot Chat에서 @lamp-gerrit 확인
- [ ] 테스트 명령 실행 성공

---

## 💬 도움이 필요하면?

1. **VS Code Output 패널 확인**:
   - `Ctrl + Shift + U` 눌러 Output 패널 열기
   - 드롭다운에서 "GitHub Copilot Chat" 또는 "MCP" 선택
   - 에러 메시지 확인

2. **MCP 로그 확인**:
   - mcp.json에 `"MCP_VERBOSE": "true"` 설정되어 있는지 확인
   - 더 자세한 로그 출력됨

3. **재설치가 필요한 경우**:
   ```powershell
   cd D:\PVS\mcp
   Remove-Item node_modules\mcp-atlassian -Recurse -Force
   npm install mcp-atlassian
   ```

---

**마지막 업데이트**: 2026-02-26  
**대상 환경**: LGE 내부망 개발자
