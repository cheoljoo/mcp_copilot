# MCP Copilot Tutorials

Comprehensive tutorials for integrating Model Context Protocol (MCP) with various development tools in GitHub Copilot.

## What is MCP?

Model Context Protocol (MCP) is an open protocol that standardizes how applications provide context to Large Language Models (LLMs). It enables AI assistants like GitHub Copilot to securely interact with external data sources and tools, bringing your development workflow directly into your IDE.

## Available Tutorials

### 📊 Project Management & Issue Tracking

- **[Atlassian (Jira & Confluence)](docs/atlassian-mcp-tutorial.md)** - Comprehensive guide for integrating Jira issue tracking and Confluence documentation with GitHub Copilot
  - Create and manage Jira issues
  - Search and update tickets
  - Generate and update Confluence documentation
  - Workflow examples and best practices

### 🔍 Code Review Tools

- **[Gerrit](docs/gerrit-mcp-tutorial.md)** - Complete guide for Gerrit Code Review integration
  - Review changes and patchsets
  - Query and filter reviews
  - Check CI/CD status
  - Manage code review workflows

### 🛠️ Other Development Tools

- **[Additional Tools Guide](docs/other-tools-mcp-guide.md)** - Integration guides for:
  - **GitLab** - Merge requests, issues, and CI/CD pipelines
  - **Bitbucket** - Pull requests and repository management
  - **Azure DevOps** - Work items and build pipelines
  - **Linear** - Modern issue tracking
  - **Notion** - Documentation and knowledge management
  - **Slack** - Team communication integration
  - **PagerDuty** - Incident management
  - **Custom MCP Servers** - Build your own integrations

## Quick Start

### Prerequisites

- GitHub Copilot subscription (Individual, Business, or Enterprise)
- VS Code or compatible IDE with Copilot installed
- Node.js 18+ (for running MCP servers)
- API credentials for the services you want to integrate

### Basic Setup Steps

1. **Install MCP Server** for your tool (see specific tutorial)
   ```bash
   npm install -g @modelcontextprotocol/server-<toolname>
   ```

2. **Generate API Credentials** from your service (Jira, Gerrit, etc.)

3. **Configure VS Code** by updating your settings:
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
               "SERVICE_URL": "https://your-service.com",
               "SERVICE_TOKEN": "your-api-token"
             }
           }
         }
       }
     }
   }
   ```

4. **Restart VS Code** and start using Copilot with your integrated tools!

## Example Use Cases

### Jira Integration
```
@copilot search Jira for all open bugs in project MYPROJECT
@copilot create a Jira task for fixing the authentication issue
@copilot update MYPROJECT-123 status to "In Progress"
```

### Gerrit Integration
```
@copilot show all Gerrit changes waiting for my review
@copilot get details for Gerrit change 12345
@copilot compare patchset 1 and 3 of change 12345
```

### Confluence Integration
```
@copilot search Confluence for API documentation
@copilot create a Confluence page documenting this API endpoint
@copilot update the "Architecture Guide" page with these changes
```

## Security Best Practices

⚠️ **Important Security Guidelines:**

1. **Never commit API tokens** to version control
2. Use **environment variables** or secure credential storage
3. **Rotate credentials** regularly
4. Use **least-privilege access** - only grant necessary permissions
5. Consider using **secret managers** for production environments

## Troubleshooting

### Common Issues

1. **Connection Problems**
   - Verify API credentials are correct
   - Check network connectivity to the service
   - Ensure firewall/proxy settings allow access

2. **Authentication Errors**
   - Regenerate API tokens
   - Verify token has required permissions
   - Check token hasn't expired

3. **MCP Server Issues**
   - Verify Node.js version (18+ required)
   - Check server logs for errors
   - Ensure all environment variables are set
   - Restart VS Code after configuration changes

For detailed troubleshooting, see the specific tool's tutorial.

## Contributing

We welcome contributions! To add or improve tutorials:

1. Fork the repository
2. Create a new branch for your changes
3. Add or update documentation in the `docs/` directory
4. Submit a pull request

### Contribution Guidelines

- Follow the existing tutorial structure
- Include practical examples and use cases
- Add troubleshooting sections
- Test all configuration examples
- Keep security best practices in mind

## Features

✅ **Comprehensive Coverage** - Tutorials for major development tools  
✅ **Step-by-Step Guides** - Clear setup instructions with examples  
✅ **Security Focused** - Best practices for credential management  
✅ **Real-World Examples** - Practical prompts and workflows  
✅ **Troubleshooting** - Solutions to common problems  
✅ **Extensible** - Guide for creating custom MCP servers  

## Resources

- [MCP Specification](https://modelcontextprotocol.io/) - Official MCP documentation
- [MCP SDK](https://github.com/modelcontextprotocol/sdk) - SDK for building MCP servers
- [MCP Servers](https://github.com/modelcontextprotocol/servers) - Official MCP server implementations
- [GitHub Copilot Docs](https://docs.github.com/copilot) - GitHub Copilot documentation

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For questions or issues:
- Open an issue in this repository
- Check the specific tutorial's troubleshooting section
- Refer to the official MCP and tool documentation

---

**Made with ❤️ for developers who want to supercharge GitHub Copilot with their favorite tools**
