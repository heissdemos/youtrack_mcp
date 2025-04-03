# YouTrack MCP Server

A Model Context Protocol (MCP) server for YouTrack Cloud, implemented using the official [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk).

## Features

- Issue search
- Detailed issue information
- Update issues (status, assignee, etc.)
- Add comments to issues
- Standardized interface via MCP Python SDK
- Support for stdio and SSE transports
- Integration with Claude Desktop and other MCP-compatible clients

## Requirements

- Python 3.7 or higher
- Access to YouTrack with API token
- Installed MCP Python SDK

## Installation

### 1. Clone the repository

```bash
git clone [repository-url]
cd youtrack_mcp
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup connection to YouTrack

Create a `.env` file in the root directory of the project with the following variables:

```
YOUTRACK_URL=https://your-instance.youtrack.cloud
YOUTRACK_TOKEN=your-permanent-token
MCP_SERVER_NAME=YouTrack MCP Server
MCP_LOG_LEVEL=INFO
```

Or specify these parameters when starting the server via command line arguments.

## Run MCP server

### Development and debugging

```bash
# Запуск в режиме разработки с интерактивным веб-интерфейсом
mcp dev server.py

# With additional dependencies
mcp dev server.py --with pandas --with numpy
```

### Direct run

```bash
# Run via MCP module
python server.py

# With additional parameters
python server.py --youtrack-url https://your-instance.youtrack.cloud --youtrack-token your-token --read-only
```

### Command line parameters

- `--read-only` - Run in read-only mode (blocks write operations)
- `--youtrack-url` - URL of your YouTrack instance
- `--youtrack-token` - API token for YouTrack

## Integration with Claude Desktop

### Step 1: Install server

```bash
# Install server in Claude Desktop
mcp install server.py

# С пользовательским именем
mcp install server.py --name "YouTrack MCP"

# With environment variables
mcp install server.py -v YOUTRACK_URL=https://your-instance.youtrack.cloud -v YOUTRACK_TOKEN=your-token
mcp install server.py -f .env
```

### Step 2: Activate server

1. Open Claude Desktop
2. Go to Settings -> MCP Servers
3. Make sure "YouTrack MCP Server" is listed and activated

## Available tools

The server provides the following tools for working with YouTrack:

- `youtrack_search_issues` - Search for issues
- `youtrack_get_issue` - Get detailed information about an issue
- `youtrack_update_issue` - Update an issue
- `youtrack_add_comment` - Add a comment to an issue

## Usage examples

### Search for issues:

```json
{
  "type": "tool_call",
  "name": "youtrack_search_issues",
  "parameters": {
    "query": "project: YourProject",
    "top": 10
  }
}
```

### Get issue information:

```json
{
  "type": "tool_call",
  "name": "youtrack_get_issue",
  "parameters": {
    "issue_id": "YourProject-123"
  }
}
```

### Добавление комментария:

```json
{
  "type": "tool_call",
  "name": "youtrack_add_comment",
  "parameters": {
    "issue_id": "YourProject-123",
    "comment_text": "Новый комментарий к задаче"
  }
}
```

### Access resources:

```json
{
  "type": "resource_request",
  "uri": "server://info"
}
```

## Architecture

The MCP server is built using the official Python SDK for Model Context Protocol, ensuring full compatibility with the MCP specification.

Main components:
- `server.py` - MCP server with tool and resource definitions
- `youtrack_api.py` - Functions for interacting with YouTrack API

## Development and extension

To add new tools or resources, use the `@mcp.tool()` and `@mcp.resource()` decorators in the `server.py` file.

### Example of adding a new tool:

```python
@mcp.tool()
def youtrack_create_issue(project_id: str, summary: str, description: str = None) -> Dict[str, Any]:
    """
    Create a new issue in YouTrack.
    
    Args:
        project_id: The ID of the project
        summary: Issue summary
        description: Optional issue description
    """
    # Add implementation here
    return {"status": "success", "issue_id": "PROJECT-123"}
