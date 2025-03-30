# YouTrack MCP

Model Context Protocol (MCP) server for YouTrack Cloud.

## Features

- Search issues
- Update issues (status, assignee, comments, etc.)
- Get issue details
- Add comments

## Requirements

- Python 3.7 or higher
- Access to YouTrack with API token

## Local Installation

1. Clone the repository: `git clone [repository-url]`
2. Install dependencies: `pip install -r requirements.txt`
3. Set parameters for connecting to YouTrack:
   - Environment variables:
     ```
     YOUTRACK_URL=https://your-instance.youtrack.cloud
     YOUTRACK_TOKEN=your-permanent-token
     ```
4. Run MCP server: `python main.py`

## Running MCP server

### Basic usage:

```bash
python main.py
```

### With additional parameters:

```bash
python main.py --transport stdio --verbose --youtrack-url https://your-instance.youtrack.cloud --youtrack-token your-token
```

### Command line parameters:

- `--transport` - Transport type (`stdio` or `sse`)
- `--port` - Port for SSE transport (default: 8000)
- `--verbose` or `-v` - Increase log detail level (can be used multiple times)
- `--read-only` - Run in read-only mode (blocks write operations)
- `--youtrack-url` - URL of your YouTrack instance
- `--youtrack-token` - API token for YouTrack

## Integration with Windsurf

### Step 1: Package preparation

1. Create a ZIP archive of the project, including the following files:
   - `main.py`
   - `youtrack_api.py`
   - `requirements.txt`

### Step 2: Installation in Windsurf

1. Open Windsurf and go to Settings
2. Find the "MCP Servers" or "Integrations" section
3. Click "Add MCP Server" and specify the path to your ZIP archive
4. Specify the server name (e.g., "YouTrack MCP")

### Step 3: Environment variable configuration

In the MCP server settings in Windsurf, specify:
- `YOUTRACK_URL` - URL of your YouTrack
- `YOUTRACK_TOKEN` - your API token for YouTrack

### Step 4: Activate the server

After configuration, activate the server in the list of available MCP servers. Windsurf should show that the server is successfully connected.

## Available tools

The server provides the following tools for working with YouTrack:

- `youtrack_search_issues` - Search for issues
- `youtrack_get_issue` - Get detailed issue information
- `youtrack_update_issue` - Update issue
- `youtrack_add_comment` - Add comment to issue

## Examples of use

### Search for issues:

```json
{
  "name": "youtrack_search_issues",
  "query": "project: YourProject",
  "top": 10
}
```

### Get issue information:

```json
{
  "name": "youtrack_get_issue",
  "issue_id": "YourProject-123"
}
```

### Add comment:

```json
{
  "name": "youtrack_add_comment",
  "issue_id": "YourProject-123",
  "comment_text": "New comment to issue"
}
