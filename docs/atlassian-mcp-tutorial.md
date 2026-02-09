# MCP Tutorial for Atlassian (Jira & Confluence) in GitHub Copilot

This tutorial will guide you through setting up and using Model Context Protocol (MCP) with Atlassian tools (Jira and Confluence) in GitHub Copilot.

## Table of Contents
- [Prerequisites](#prerequisites)
- [What is MCP?](#what-is-mcp)
- [Setup MCP for Atlassian](#setup-mcp-for-atlassian)
- [Configuration](#configuration)
- [Using MCP with Jira](#using-mcp-with-jira)
- [Using MCP with Confluence](#using-mcp-with-confluence)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:
- GitHub Copilot subscription (Copilot Individual, Business, or Enterprise)
- VS Code or compatible IDE with Copilot installed
- Access to Atlassian Jira and/or Confluence
- API tokens for Atlassian services
- Node.js 18+ (for MCP server)
- Basic knowledge of REST APIs

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables AI assistants like GitHub Copilot to securely interact with external data sources and tools.

## Setup MCP for Atlassian

### Step 1: Install MCP Server for Atlassian

First, you'll need to install or set up an MCP server that can communicate with Atlassian APIs:

```bash
# Install using npm
npm install -g @modelcontextprotocol/server-atlassian

# Or clone and build from source
git clone https://github.com/modelcontextprotocol/servers
cd servers/atlassian
npm install
npm run build
```

### Step 2: Generate Atlassian API Tokens

1. **For Jira Cloud:**
   - Go to https://id.atlassian.com/manage-profile/security/api-tokens
   - Click "Create API token"
   - Give it a descriptive label (e.g., "MCP GitHub Copilot")
   - Copy and save the token securely

2. **For Confluence Cloud:**
   - Use the same Atlassian API token as above
   - API tokens work across all Atlassian Cloud products

3. **For Self-Hosted (Server/Data Center):**
   - Create a Personal Access Token from your profile settings
   - Or use username/password authentication (not recommended)

### Step 3: Configure GitHub Copilot for MCP

GitHub Copilot integrates with MCP through configuration files. You'll need to configure the MCP server connection.

#### For VS Code:

Create or update your settings file:

**Location:** `~/.config/Code/User/settings.json` (Linux/macOS) or `%APPDATA%\Code\User\settings.json` (Windows)

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "atlassian": {
          "command": "node",
          "args": [
            "/path/to/mcp-server-atlassian/dist/index.js"
          ],
          "env": {
            "ATLASSIAN_DOMAIN": "your-domain.atlassian.net",
            "ATLASSIAN_EMAIL": "your-email@example.com",
            "ATLASSIAN_API_TOKEN": "your-api-token-here"
          }
        }
      }
    }
  }
}
```

#### Alternative: Using MCP Configuration File

Create `~/.mcp/config.json`:

```json
{
  "mcpServers": {
    "atlassian": {
      "command": "node",
      "args": ["/path/to/mcp-server-atlassian/dist/index.js"],
      "env": {
        "ATLASSIAN_DOMAIN": "your-domain.atlassian.net",
        "ATLASSIAN_EMAIL": "your-email@example.com",
        "ATLASSIAN_API_TOKEN": "your-api-token-here",
        "JIRA_PROJECT_KEY": "PROJ",
        "CONFLUENCE_SPACE_KEY": "SPACE"
      }
    }
  }
}
```

## Configuration

### Environment Variables

Configure these environment variables for your Atlassian connection:

| Variable | Description | Example |
|----------|-------------|---------|
| `ATLASSIAN_DOMAIN` | Your Atlassian domain | `company.atlassian.net` |
| `ATLASSIAN_EMAIL` | Your Atlassian account email | `user@company.com` |
| `ATLASSIAN_API_TOKEN` | API token from Atlassian | `ATATT3xFfGF0...` |
| `JIRA_PROJECT_KEY` | (Optional) Default Jira project | `PROJ` |
| `CONFLUENCE_SPACE_KEY` | (Optional) Default Confluence space | `DOCS` |

### Secure Token Storage

**Important:** Never commit API tokens to version control!

Use one of these secure methods:

1. **Environment Variables File** (`.env`):
```bash
# .env (add to .gitignore!)
ATLASSIAN_DOMAIN=your-domain.atlassian.net
ATLASSIAN_EMAIL=your-email@example.com
ATLASSIAN_API_TOKEN=your-token-here
```

2. **System Keychain** (macOS/Linux):
```bash
# Store in keychain
security add-generic-password -a "atlassian-mcp" -s "api-token" -w "your-token"

# Retrieve in your config
export ATLASSIAN_API_TOKEN=$(security find-generic-password -a "atlassian-mcp" -s "api-token" -w)
```

3. **Windows Credential Manager:**
```powershell
# Store credential
cmdkey /generic:atlassian-mcp /user:api-token /pass:your-token

# Use in scripts with credential manager APIs
```

## Using MCP with Jira

Once configured, you can use GitHub Copilot to interact with Jira:

### Example Prompts for Jira:

1. **Search for Issues:**
   ```
   @copilot search Jira for all open bugs in project PROJ
   ```

2. **Create an Issue:**
   ```
   @copilot create a Jira bug ticket for the authentication error in login.js
   ```

3. **Get Issue Details:**
   ```
   @copilot get details for Jira issue PROJ-123
   ```

4. **Update an Issue:**
   ```
   @copilot update Jira issue PROJ-123 status to "In Progress"
   ```

5. **List Sprint Tasks:**
   ```
   @copilot show all tasks in the current sprint for project PROJ
   ```

6. **Code Context Integration:**
   ```
   @copilot analyze this function and create a Jira task for refactoring it
   ```

### Advanced Jira Operations:

```
@copilot List all Jira issues assigned to me that are due this week

@copilot Create a Jira subtask for PROJ-123 to add unit tests

@copilot Add a comment to PROJ-456 with the deployment notes

@copilot Show me the issue history for PROJ-789

@copilot Link this code file to Jira issue PROJ-123
```

## Using MCP with Confluence

### Example Prompts for Confluence:

1. **Search Pages:**
   ```
   @copilot search Confluence for API documentation
   ```

2. **Get Page Content:**
   ```
   @copilot get the content of Confluence page "Architecture Overview"
   ```

3. **Create a Page:**
   ```
   @copilot create a Confluence page with documentation for this API endpoint
   ```

4. **Update Documentation:**
   ```
   @copilot update the Confluence page "API Guide" with these changes
   ```

5. **Generate Documentation:**
   ```
   @copilot analyze this code and create Confluence documentation in the DEV space
   ```

### Advanced Confluence Operations:

```
@copilot List all pages in the DOCS space modified in the last 7 days

@copilot Create a Confluence page from this README.md file

@copilot Add a code block to the "API Reference" page with this function

@copilot Show me the page tree structure for the TECH space

@copilot Create a table in Confluence comparing these API versions
```

## Workflow Examples

### Example 1: Bug Fix Workflow

```
1. @copilot search Jira for bug PROJ-234
2. @copilot show me the code related to the authentication module
3. [Make your code changes]
4. @copilot update PROJ-234 with fix details and set status to "Code Review"
5. @copilot create a Confluence page documenting this fix
```

### Example 2: Feature Development

```
1. @copilot get details for Jira epic PROJ-100
2. @copilot create subtasks for implementing the user profile feature
3. [Implement feature]
4. @copilot generate API documentation and save to Confluence
5. @copilot update all related Jira tasks to "Done"
```

### Example 3: Code Review with Context

```
1. @copilot get Jira issue PROJ-567 requirements
2. @copilot analyze this pull request against the requirements
3. @copilot add code review comments to PROJ-567
```

## Troubleshooting

### Connection Issues

**Problem:** "Cannot connect to Atlassian API"

**Solutions:**
1. Verify your domain: `curl https://your-domain.atlassian.net/rest/api/3/myself -u email:token`
2. Check API token is valid and not expired
3. Ensure your email matches the Atlassian account
4. Verify firewall/proxy settings

### Authentication Errors

**Problem:** "401 Unauthorized" or "403 Forbidden"

**Solutions:**
1. Regenerate your API token
2. Check token has required permissions:
   - Jira: Read/Write access to projects
   - Confluence: Read/Write access to spaces
3. Verify you're using the correct email address
4. For self-hosted: Check your base URL is correct

### MCP Server Not Starting

**Problem:** MCP server fails to start or crashes

**Solutions:**
1. Check Node.js version: `node --version` (should be 18+)
2. Reinstall dependencies: `npm install`
3. Check server logs: `npm run dev` for verbose output
4. Verify all environment variables are set
5. Check port conflicts

### Copilot Not Using MCP

**Problem:** Copilot doesn't seem to access Jira/Confluence

**Solutions:**
1. Restart VS Code after configuration changes
2. Check Copilot settings: `Ctrl+Shift+P` → "Copilot: Check Status"
3. Verify MCP is enabled in settings
4. Check MCP server is running: `ps aux | grep mcp`
5. Review VS Code Developer Console: Help → Toggle Developer Tools

### Rate Limiting

**Problem:** "429 Too Many Requests"

**Solutions:**
1. Add delays between operations
2. Use batch operations when possible
3. Check Atlassian API rate limits for your plan
4. Consider upgrading your Atlassian plan

### Data Not Updating

**Problem:** Copilot shows stale data from Jira/Confluence

**Solutions:**
1. MCP servers may cache data - restart the server
2. Check your query is specific enough
3. Verify the data exists in Atlassian
4. Clear any local caches

## Best Practices

1. **Security:**
   - Never commit API tokens to repositories
   - Use environment variables or secret managers
   - Rotate tokens regularly
   - Use least-privilege access

2. **Performance:**
   - Be specific in your queries to reduce API calls
   - Use project/space keys to narrow searches
   - Cache frequently accessed data
   - Monitor API rate limits

3. **Productivity:**
   - Create templates for common operations
   - Use keyboard shortcuts for frequent Copilot commands
   - Combine operations in single prompts when possible
   - Keep your MCP server configuration up to date

4. **Collaboration:**
   - Document your MCP setup for team members
   - Share configuration templates (without tokens)
   - Establish naming conventions for Jira/Confluence
   - Use consistent prompting patterns

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [Atlassian REST API Documentation](https://developer.atlassian.com/cloud/jira/platform/rest/v3/)
- [Confluence REST API](https://developer.atlassian.com/cloud/confluence/rest/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)

## Contributing

Found an issue or have improvements? Contribute to this tutorial:
1. Fork the repository
2. Make your changes
3. Submit a pull request

## License

This tutorial is provided under the MIT License.
