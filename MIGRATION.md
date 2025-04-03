# Migration to MCP Python SDK

This document describes the process of migrating the YouTrack MCP server to the official Python SDK for Model Context Protocol.

## What was done

1. **Server architecture changed**:
   - Transition from custom MCP implementation to official SDK
   - Replacement of `main.py` with `server.py` using `FastMCP` class
   - Improved type hints and code documentation

2. **Configuration improved**:
   - Added support for `.env` files
   - Implemented more flexible parameter management
   - Expanded command line options

3. **Added new capabilities**:
   - Integration with Claude Desktop
   - Support for development mode with web interface
   - Added new resources (server://info, youtrack://projects)

4. **Simplified development**:
   - Added script `setup.py` for simplifying installation and configuration
   - Improved logging and error handling
   - Added type hints for better IDE support

## Benefits of using MCP Python SDK

1. **Compatibility** - Full compatibility with MCP specification
2. **Extensibility** - Easy addition of new tools and resources
3. **Integration** - Built-in support for Claude Desktop and other MCP clients
4. **Modernization** - Using modern Python features
5. **Support** - Official support and SDK updates

## How to start using the new server

1. **Setup**:
   ```bash
   # Setup server
   python setup.py setup --youtrack-url https://your-instance.youtrack.cloud --youtrack-token your-token
   ```

2. **Run**:
   ```bash
   # Run server
   python setup.py run
   
   # Or run in development mode
   python setup.py dev
   ```

3. **Install in Claude Desktop**:
   ```bash
   # Install in Claude Desktop
   python setup.py install --name "YouTrack MCP"
   ```

## Retained functionality

All main tools from the previous version are retained:
- `youtrack_search_issues`
- `youtrack_get_issue`
- `youtrack_update_issue`
- `youtrack_add_comment`

## Backward compatibility

This server supports the same tools as the previous version, but with minor changes in request format in accordance with the MCP specification.

## Future improvements

In future versions, we plan to:
1. Add new tools for working with projects, agile boards, and reports
2. Expand resource support
3. Improve performance and caching management
4. Add unit tests
