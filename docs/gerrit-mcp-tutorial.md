# MCP Tutorial for Gerrit in GitHub Copilot

This tutorial will guide you through setting up and using Model Context Protocol (MCP) with Gerrit Code Review in GitHub Copilot.

## Table of Contents
- [Prerequisites](#prerequisites)
- [What is Gerrit?](#what-is-gerrit)
- [Setup MCP for Gerrit](#setup-mcp-for-gerrit)
- [Configuration](#configuration)
- [Using MCP with Gerrit](#using-mcp-with-gerrit)
- [Advanced Operations](#advanced-operations)
- [Troubleshooting](#troubleshooting)

## Prerequisites

Before you begin, ensure you have:
- GitHub Copilot subscription
- VS Code or compatible IDE with Copilot installed
- Access to a Gerrit server
- Gerrit HTTP credentials
- Node.js 18+ (for MCP server)
- Basic knowledge of Gerrit and Git

## What is Gerrit?

Gerrit is a web-based code review and project management tool for Git repositories. It facilitates:
- Pre-commit code reviews
- Fine-grained access controls
- Integration with CI/CD systems
- Project and branch management

## Setup MCP for Gerrit

### Step 1: Install MCP Server for Gerrit

Install or create an MCP server that can communicate with Gerrit REST API:

```bash
# If available from npm
npm install -g @modelcontextprotocol/server-gerrit

# Or install a community implementation
npm install -g mcp-server-gerrit

# Or build from source
git clone https://github.com/your-org/mcp-server-gerrit
cd mcp-server-gerrit
npm install
npm run build
```

### Step 2: Generate Gerrit HTTP Credentials

1. Log in to your Gerrit instance
2. Navigate to: Settings → HTTP Credentials
3. Click "Generate New Password"
4. Save your username and generated password securely

**For Gerrit 3.x+:**
```
URL: https://gerrit.example.com
Username: your-username
HTTP Password: base64-encoded-password
```

### Step 3: Configure GitHub Copilot for MCP

#### For VS Code:

Create or update your settings file:

**Location:** `~/.config/Code/User/settings.json` (Linux/macOS) or `%APPDATA%\Code\User\settings.json` (Windows)

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "gerrit": {
          "command": "node",
          "args": [
            "/path/to/mcp-server-gerrit/dist/index.js"
          ],
          "env": {
            "GERRIT_URL": "https://gerrit.example.com",
            "GERRIT_USERNAME": "your-username",
            "GERRIT_HTTP_PASSWORD": "your-http-password"
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
    "gerrit": {
      "command": "node",
      "args": ["/path/to/mcp-server-gerrit/dist/index.js"],
      "env": {
        "GERRIT_URL": "https://gerrit.example.com",
        "GERRIT_USERNAME": "your-username",
        "GERRIT_HTTP_PASSWORD": "your-http-password",
        "GERRIT_PROJECT": "your-default-project",
        "GERRIT_BRANCH": "main"
      }
    }
  }
}
```

## Configuration

### Environment Variables

Configure these environment variables for your Gerrit connection:

| Variable | Description | Example |
|----------|-------------|---------|
| `GERRIT_URL` | Your Gerrit server URL | `https://gerrit.example.com` |
| `GERRIT_USERNAME` | Your Gerrit username | `john.doe` |
| `GERRIT_HTTP_PASSWORD` | HTTP password from Gerrit | `base64encodedpassword` |
| `GERRIT_PROJECT` | (Optional) Default project | `my-project` |
| `GERRIT_BRANCH` | (Optional) Default branch | `main` or `master` |
| `GERRIT_VERIFY_SSL` | (Optional) Verify SSL certificates | `true` or `false` |

### Secure Credential Storage

**Important:** Never commit credentials to version control!

Use one of these secure methods:

1. **Environment Variables File** (`.env`):
```bash
# .env (add to .gitignore!)
GERRIT_URL=https://gerrit.example.com
GERRIT_USERNAME=your-username
GERRIT_HTTP_PASSWORD=your-password
```

2. **System Keychain** (macOS/Linux):
```bash
# Store in keychain
security add-generic-password -a "gerrit-mcp" -s "http-password" -w "your-password"

# Retrieve in your config
export GERRIT_HTTP_PASSWORD=$(security find-generic-password -a "gerrit-mcp" -s "http-password" -w)
```

3. **Git Credential Helper:**
```bash
# Configure git credential helper
git config --global credential.helper store
git config --global credential.https://gerrit.example.com.username your-username
```

## Using MCP with Gerrit

Once configured, you can use GitHub Copilot to interact with Gerrit:

### Example Prompts for Gerrit:

1. **Search for Changes:**
   ```
   @copilot search Gerrit for open changes in project my-project
   ```

2. **Get Change Details:**
   ```
   @copilot get details for Gerrit change 12345
   ```

3. **Review a Change:**
   ```
   @copilot show me the code changes in Gerrit review 12345
   ```

4. **Check Change Status:**
   ```
   @copilot get the status of my latest Gerrit changes
   ```

5. **List Pending Reviews:**
   ```
   @copilot show all Gerrit changes waiting for my review
   ```

6. **Get Review Comments:**
   ```
   @copilot get comments from Gerrit change 12345
   ```

### Advanced Gerrit Operations:

```
@copilot List all Gerrit changes merged in the last week

@copilot Show me changes in project my-project that need rebasing

@copilot Get the CI/CD status for Gerrit change 12345

@copilot Show changes with negative votes (Code-Review -1 or -2)

@copilot List all my Gerrit changes that are work in progress

@copilot Show the change history for Gerrit review 12345
```

## Advanced Operations

### Working with Patchsets

```
@copilot Compare patchset 1 and patchset 3 of Gerrit change 12345

@copilot Show me the diff between the latest patchset and the base

@copilot List all patchsets for change 12345 with their upload times

@copilot Get the commit message for the latest patchset of change 12345
```

### Project and Branch Management

```
@copilot List all projects in Gerrit

@copilot Show branches for project my-project

@copilot Get project configuration for my-project

@copilot List all open changes for branch feature/new-api
```

### Querying and Filtering

Gerrit uses a powerful query language. You can use it through Copilot:

```
@copilot Search Gerrit for changes: status:open owner:me

@copilot Find changes with query: project:my-project branch:main status:open

@copilot Search: reviewer:john.doe status:open label:Code-Review>=1

@copilot Find: status:merged since:2024-01-01 project:my-project

@copilot Query Gerrit: owner:me status:open (label:Code-Review-1 OR label:Verified-1)
```

### Review Workflow Examples

#### Example 1: Pre-Review Preparation

```
1. @copilot list all changes waiting for my review in Gerrit
2. @copilot get details for change 12345 including files changed
3. @copilot show me the commit message and description
4. @copilot compare with previous patchset to see what changed
```

#### Example 2: Code Review Process

```
1. @copilot get the full diff for Gerrit change 12345
2. @copilot analyze this change for potential issues
3. @copilot check if this follows our coding standards
4. @copilot summarize the changes in this review
```

#### Example 3: Managing Your Changes

```
1. @copilot show all my open Gerrit changes
2. @copilot check CI status for change 12345
3. @copilot see what comments need to be addressed
4. @copilot check if change 12345 needs rebasing
```

### Integration with Git Workflow

```
@copilot help me create a commit message following Gerrit conventions

@copilot show me how to amend my commit for Gerrit review

@copilot what's the git command to push to Gerrit for review?

@copilot help me rebase my change 12345 onto the latest main branch
```

## Gerrit REST API Integration

The MCP server uses Gerrit's REST API. Common endpoints:

| Operation | API Endpoint | Example |
|-----------|--------------|---------|
| List changes | `/changes/` | Get all changes |
| Get change | `/changes/{change-id}` | Get specific change |
| List projects | `/projects/` | Get all projects |
| Get project | `/projects/{project-name}` | Get project info |
| Query changes | `/changes/?q={query}` | Search changes |

### Example API Queries via Copilot:

```
@copilot query Gerrit API for changes modified in the last 24 hours

@copilot use Gerrit REST API to get detailed diff for change 12345

@copilot call Gerrit API to list all reviewers for change 12345

@copilot get submit requirements for change 12345 via API
```

## Troubleshooting

### Connection Issues

**Problem:** "Cannot connect to Gerrit server"

**Solutions:**
1. Verify URL: `curl https://gerrit.example.com/` 
2. Test authentication:
   ```bash
   curl -u username:password https://gerrit.example.com/a/accounts/self
   ```
3. Check if server is accessible from your network
4. Verify SSL certificate is valid (or set `GERRIT_VERIFY_SSL=false` for self-signed)

### Authentication Errors

**Problem:** "401 Unauthorized" or "403 Forbidden"

**Solutions:**
1. Regenerate HTTP password in Gerrit (Settings → HTTP Credentials)
2. Verify username is correct
3. Check if account has required permissions
4. For SSH: Ensure SSH keys are properly configured
5. Verify you're using HTTP password, not your login password

### MCP Server Not Starting

**Problem:** MCP server fails to start or crashes

**Solutions:**
1. Check Node.js version: `node --version` (should be 18+)
2. Reinstall dependencies: `npm install`
3. Check server logs for detailed errors
4. Verify all required environment variables are set
5. Test Gerrit connectivity outside of MCP

### Copilot Not Using MCP

**Problem:** Copilot doesn't seem to access Gerrit

**Solutions:**
1. Restart VS Code after configuration changes
2. Check Copilot status: `Ctrl+Shift+P` → "Copilot: Check Status"
3. Verify MCP is enabled in settings
4. Check MCP server is running: `ps aux | grep mcp-server-gerrit`
5. Review VS Code Developer Console for errors

### Query/Search Issues

**Problem:** Gerrit queries return no results or errors

**Solutions:**
1. Verify Gerrit query syntax
2. Test query directly in Gerrit UI
3. Check project names and branch names are correct
4. Ensure you have permission to view the results
5. Use simpler queries first, then add complexity

### Performance Issues

**Problem:** Slow responses from Gerrit MCP server

**Solutions:**
1. Use more specific queries to reduce result sets
2. Limit the number of changes retrieved
3. Check Gerrit server load
4. Consider caching for frequently accessed data
5. Use pagination for large result sets

## Best Practices

1. **Security:**
   - Never commit credentials to repositories
   - Use secure credential storage
   - Rotate HTTP passwords regularly
   - Use least-privilege access
   - Enable 2FA on Gerrit when available

2. **Query Optimization:**
   - Be specific in queries to reduce API calls
   - Use project and branch filters
   - Limit result sets with appropriate status filters
   - Cache frequently accessed data

3. **Code Review:**
   - Review commits incrementally with Copilot's help
   - Use Copilot to generate review summaries
   - Leverage Copilot for consistency checks
   - Document review comments clearly

4. **Workflow Integration:**
   - Integrate Gerrit checks into your development workflow
   - Use Copilot for pre-commit checks
   - Automate common review tasks
   - Keep MCP configuration synchronized with team

5. **Collaboration:**
   - Document your MCP setup for team members
   - Share configuration templates (without credentials)
   - Establish consistent prompting patterns
   - Use project-specific conventions

## Gerrit-Specific Tips

1. **Change-Id Usage:**
   - Always include Change-Id in commit messages
   - Use `commit-msg` hook to auto-generate Change-Ids
   - Copilot can help format commit messages with Change-Ids

2. **Patchset Management:**
   - Review patchset diffs to understand iterations
   - Use `git commit --amend` for updating changes
   - Ask Copilot about best practices for amending commits

3. **Review Labels:**
   - Understand your project's label requirements
   - Use Copilot to check submit requirements
   - Query changes by label values

4. **Topic and Hashtag Usage:**
   - Use topics to group related changes
   - Use hashtags for categorization
   - Query by topics/hashtags for better organization

## Additional Resources

- [Gerrit Documentation](https://gerrit-review.googlesource.com/Documentation/)
- [Gerrit REST API](https://gerrit-review.googlesource.com/Documentation/rest-api.html)
- [Gerrit Query Operators](https://gerrit-review.googlesource.com/Documentation/user-search.html)
- [MCP Specification](https://modelcontextprotocol.io/)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

## Example MCP Server Implementation

If you need to create a custom MCP server for Gerrit, here's a basic structure:

```javascript
// Example: Basic Gerrit MCP Server structure
import { MCPServer } from '@modelcontextprotocol/sdk';
import axios from 'axios';

class GerritMCPServer extends MCPServer {
  constructor() {
    super({
      name: 'gerrit',
      version: '1.0.0'
    });
    
    this.gerritUrl = process.env.GERRIT_URL;
    this.auth = {
      username: process.env.GERRIT_USERNAME,
      password: process.env.GERRIT_HTTP_PASSWORD
    };
  }

  async listChanges(query) {
    const response = await axios.get(
      `${this.gerritUrl}/a/changes/?q=${query}`,
      { auth: this.auth }
    );
    return this.parseGerritResponse(response.data);
  }

  async getChange(changeId) {
    const response = await axios.get(
      `${this.gerritUrl}/a/changes/${changeId}/detail`,
      { auth: this.auth }
    );
    return this.parseGerritResponse(response.data);
  }

  parseGerritResponse(data) {
    // Remove Gerrit XSSI protection prefix
    return JSON.parse(data.substring(4));
  }
}

// Start the server
const server = new GerritMCPServer();
server.start();
```

## Contributing

Found an issue or have improvements? Contribute to this tutorial:
1. Fork the repository
2. Make your changes
3. Submit a pull request

## License

This tutorial is provided under the MIT License.
