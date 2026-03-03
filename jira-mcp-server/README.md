# Jira MCP Server for LGE

이 서버는 LGE Jira를 MCP(Model Context Protocol)를 통해 접근할 수 있게 합니다.

## 설정 방법

GitHub Copilot CLI는 현재 사용 중인 환경에서 GitHub MCP 서버를 사용하고 있습니다.
추가 MCP 서버를 연결하려면 관리자가 설정해야 합니다.

## 대안: Direct API 접근

현재는 curl을 통해 직접 Jira API에 접근할 수 있습니다:

```bash
# 티켓 조회
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://jira.lge.com/issue/rest/api/latest/issue/AGILEDEV-653"

# JQL 검색
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://jira.lge.com/issue/rest/api/latest/search?jql=project=AGILEDEV"

# 코멘트 조회
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://jira.lge.com/issue/rest/api/latest/issue/AGILEDEV-653/comment"
```

## 환경 변수 설정

```bash
export JIRA_HOST="http://jira.lge.com"
export JIRA_TOKEN="your_personal_access_token_here"
```

## Jira API 엔드포인트

- Base URL: `http://jira.lge.com/issue/rest/api/latest`
- 티켓 조회: `/issue/{issueKey}`
- 검색: `/search?jql={jql}`
- 코멘트: `/issue/{issueKey}/comment`
