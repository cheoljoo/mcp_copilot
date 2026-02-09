# MCP Integration Guide for Other Development Tools

This guide covers integrating Model Context Protocol (MCP) with various other development and collaboration tools in GitHub Copilot.

## Table of Contents
- [General MCP Setup](#general-mcp-setup)
- [GitLab](#gitlab)
- [Bitbucket](#bitbucket)
- [Azure DevOps](#azure-devops)
- [Linear](#linear)
- [Notion](#notion)
- [Slack](#slack)
- [PagerDuty](#pagerduty)
- [Creating Custom MCP Servers](#creating-custom-mcp-servers)

## General MCP Setup

### Basic Configuration Structure

Most MCP integrations follow a similar configuration pattern in VS Code:

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "service-name": {
          "command": "node",
          "args": ["/path/to/mcp-server/dist/index.js"],
          "env": {
            "SERVICE_URL": "https://service.example.com",
            "SERVICE_TOKEN": "your-api-token"
          }
        }
      }
    }
  }
}
```

## GitLab

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "gitlab": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-gitlab"],
          "env": {
            "GITLAB_URL": "https://gitlab.com",
            "GITLAB_PERSONAL_ACCESS_TOKEN": "your-token",
            "GITLAB_PROJECT_ID": "your-project-id"
          }
        }
      }
    }
  }
}
```

### Generate GitLab Token

1. Go to GitLab Settings → Access Tokens
2. Create a Personal Access Token with scopes:
   - `api` - Access to GitLab API
   - `read_repository` - Read repository data
   - `write_repository` - Write to repository (if needed)
3. Save the token securely

### Example Prompts

```
@copilot list all open merge requests in GitLab

@copilot create a GitLab issue for this bug

@copilot show CI/CD pipeline status for merge request 123

@copilot get GitLab project statistics
```

## Bitbucket

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "bitbucket": {
          "command": "node",
          "args": ["/path/to/mcp-server-bitbucket/dist/index.js"],
          "env": {
            "BITBUCKET_URL": "https://bitbucket.org",
            "BITBUCKET_USERNAME": "your-username",
            "BITBUCKET_APP_PASSWORD": "your-app-password",
            "BITBUCKET_WORKSPACE": "your-workspace"
          }
        }
      }
    }
  }
}
```

### Generate Bitbucket App Password

1. Go to Bitbucket Settings → Personal Settings → App passwords
2. Click "Create app password"
3. Grant permissions:
   - Account: Read
   - Repositories: Read, Write
   - Pull requests: Read, Write
   - Issues: Read, Write
4. Save the password securely

### Example Prompts

```
@copilot list all pull requests in Bitbucket repository

@copilot create a Bitbucket branch for this feature

@copilot show build status for pull request 456

@copilot get Bitbucket repository insights
```

## Azure DevOps

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "azuredevops": {
          "command": "node",
          "args": ["/path/to/mcp-server-azuredevops/dist/index.js"],
          "env": {
            "AZUREDEVOPS_ORG": "your-organization",
            "AZUREDEVOPS_PROJECT": "your-project",
            "AZUREDEVOPS_PAT": "your-personal-access-token"
          }
        }
      }
    }
  }
}
```

### Generate Azure DevOps PAT

1. Go to User Settings → Personal access tokens
2. Create a new token with scopes:
   - Code (Read, Write, Status)
   - Work Items (Read, Write)
   - Build (Read)
   - Release (Read)
3. Save the token securely

### Example Prompts

```
@copilot list all work items assigned to me in Azure DevOps

@copilot create a work item for this feature

@copilot show build pipeline status

@copilot get details for pull request 789
```

## Linear

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "linear": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-linear"],
          "env": {
            "LINEAR_API_KEY": "your-api-key"
          }
        }
      }
    }
  }
}
```

### Generate Linear API Key

1. Go to Settings → API → Personal API keys
2. Click "Create new key"
3. Give it a label (e.g., "MCP Copilot")
4. Save the API key securely

### Example Prompts

```
@copilot list all Linear issues in the current cycle

@copilot create a Linear issue for this bug

@copilot update Linear issue LIN-123 to "In Progress"

@copilot show my Linear issues due this week
```

## Notion

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "notion": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-notion"],
          "env": {
            "NOTION_API_KEY": "your-integration-token"
          }
        }
      }
    }
  }
}
```

### Create Notion Integration

1. Go to https://www.notion.so/my-integrations
2. Click "New integration"
3. Give it a name and select capabilities:
   - Read content
   - Update content
   - Insert content
4. Copy the Internal Integration Token
5. Share your database/pages with the integration

### Example Prompts

```
@copilot search Notion for API documentation

@copilot create a Notion page with this code documentation

@copilot update Notion database with this project status

@copilot get content from Notion page "Architecture Design"
```

## Slack

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "slack": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-slack"],
          "env": {
            "SLACK_BOT_TOKEN": "xoxb-your-bot-token",
            "SLACK_TEAM_ID": "your-team-id"
          }
        }
      }
    }
  }
}
```

### Create Slack App

1. Go to https://api.slack.com/apps
2. Create a new app
3. Add OAuth scopes:
   - `channels:read` - View basic channel info
   - `channels:history` - View messages in public channels
   - `chat:write` - Send messages
   - `users:read` - View people in workspace
4. Install the app to your workspace
5. Copy the Bot User OAuth Token

### Example Prompts

```
@copilot send a Slack message to #dev-team about this deployment

@copilot search Slack for discussions about authentication

@copilot get recent messages from #project-updates

@copilot create a Slack thread with code review summary
```

## PagerDuty

### Setup

```json
{
  "github.copilot.advanced": {
    "mcp": {
      "enabled": true,
      "servers": {
        "pagerduty": {
          "command": "node",
          "args": ["/path/to/mcp-server-pagerduty/dist/index.js"],
          "env": {
            "PAGERDUTY_API_TOKEN": "your-api-token",
            "PAGERDUTY_USER_EMAIL": "your-email@example.com"
          }
        }
      }
    }
  }
}
```

### Generate PagerDuty API Token

1. Go to User Icon → User Settings
2. Navigate to API Access
3. Create a new API key
4. Save the token securely

### Example Prompts

```
@copilot list all active PagerDuty incidents

@copilot create a PagerDuty incident for this critical error

@copilot check on-call schedule

@copilot get incident details for INC-123
```

## Creating Custom MCP Servers

If there's no existing MCP server for your tool, you can create one:

### Basic MCP Server Template

```javascript
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  ListToolsRequestSchema,
  CallToolRequestSchema
} from '@modelcontextprotocol/sdk/types.js';

class CustomMCPServer {
  constructor() {
    this.server = new Server(
      {
        name: 'custom-service',
        version: '1.0.0',
      },
      {
        capabilities: {
          tools: {},
        },
      }
    );

    this.setupToolHandlers();
    this.setupErrorHandling();
  }

  setupToolHandlers() {
    // List available tools
    this.server.setRequestHandler(
      ListToolsRequestSchema,
      async () => ({
        tools: [
          {
            name: 'search_items',
            description: 'Search for items in the service',
            inputSchema: {
              type: 'object',
              properties: {
                query: {
                  type: 'string',
                  description: 'Search query'
                }
              },
              required: ['query']
            }
          },
          {
            name: 'get_item',
            description: 'Get details for a specific item',
            inputSchema: {
              type: 'object',
              properties: {
                id: {
                  type: 'string',
                  description: 'Item ID'
                }
              },
              required: ['id']
            }
          }
        ]
      })
    );

    // Handle tool calls
    this.server.setRequestHandler(
      CallToolRequestSchema,
      async (request) => {
        const { name, arguments: args } = request.params;

        switch (name) {
          case 'search_items':
            return await this.searchItems(args.query);
          case 'get_item':
            return await this.getItem(args.id);
          default:
            throw new Error(`Unknown tool: ${name}`);
        }
      }
    );
  }

  async searchItems(query) {
    // Implement your API call here
    const results = await fetch(
      `${process.env.SERVICE_URL}/api/search?q=${query}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.SERVICE_TOKEN}`
        }
      }
    ).then(r => r.json());

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(results, null, 2)
        }
      ]
    };
  }

  async getItem(id) {
    // Implement your API call here
    const item = await fetch(
      `${process.env.SERVICE_URL}/api/items/${id}`,
      {
        headers: {
          'Authorization': `Bearer ${process.env.SERVICE_TOKEN}`
        }
      }
    ).then(r => r.json());

    return {
      content: [
        {
          type: 'text',
          text: JSON.stringify(item, null, 2)
        }
      ]
    };
  }

  setupErrorHandling() {
    this.server.onerror = (error) => {
      console.error('[MCP Error]', error);
    };

    process.on('SIGINT', async () => {
      await this.server.close();
      process.exit(0);
    });
  }

  async run() {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    console.error('Custom MCP server running on stdio');
  }
}

// Start the server
const server = new CustomMCPServer();
server.run().catch(console.error);
```

### Publishing Your MCP Server

1. **Package Structure:**
```
mcp-server-myservice/
├── src/
│   └── index.ts
├── dist/
│   └── index.js
├── package.json
├── README.md
└── tsconfig.json
```

2. **Package.json:**
```json
{
  "name": "@your-org/mcp-server-myservice",
  "version": "1.0.0",
  "description": "MCP server for MyService",
  "main": "dist/index.js",
  "bin": {
    "mcp-server-myservice": "dist/index.js"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  }
}
```

3. **Publish to npm:**
```bash
npm publish --access public
```

## Best Practices for All Tools

1. **Security:**
   - Use environment variables for credentials
   - Never commit tokens to version control
   - Rotate credentials regularly
   - Use least-privilege access

2. **Error Handling:**
   - Implement retry logic for API calls
   - Handle rate limiting gracefully
   - Provide clear error messages
   - Log errors for debugging

3. **Performance:**
   - Cache frequently accessed data
   - Use pagination for large result sets
   - Implement request throttling
   - Monitor API usage

4. **Documentation:**
   - Document available operations
   - Provide example prompts
   - Include troubleshooting guides
   - Keep configuration up to date

## Additional Resources

- [MCP Specification](https://modelcontextprotocol.io/)
- [MCP SDK Documentation](https://github.com/modelcontextprotocol/sdk)
- [MCP Servers Repository](https://github.com/modelcontextprotocol/servers)
- [GitHub Copilot Documentation](https://docs.github.com/copilot)

## Contributing

Have an integration to add? Contributions are welcome:
1. Fork the repository
2. Add your integration guide
3. Submit a pull request

## License

This guide is provided under the MIT License.
