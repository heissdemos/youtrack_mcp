# server.py - YouTrack MCP Server based on official MCP Python SDK

from mcp.server.fastmcp import FastMCP, Context
import os
import argparse
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator
from dataclasses import dataclass
import logging
from typing import Dict, Any, Optional
import sys

# Configure logging before anything else
log_level = os.environ.get("MCP_LOG_LEVEL", "INFO").upper()
logging.basicConfig(
    level=getattr(logging, log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('youtrack-mcp')

# Output server startup message
print(f"Starting YouTrack MCP Server (Python SDK version) - Log level: {log_level}")

# Try to load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import test configuration if specified
if len(sys.argv) > 1 and sys.argv[1] == "--test-config":
    try:
        import test_config
        logging.info("Loaded test configuration")
    except ImportError:
        logging.warning("Failed to load test configuration")
    # Remove the argument to avoid conflicts with FastMCP
    sys.argv.remove("--test-config")

# Import YouTrack API functions
from youtrack_api import (
    search_issues, 
    get_issue, 
    update_issue, 
    add_comment,
)

# MCP server instance
server_name = os.environ.get("MCP_SERVER_NAME", "YouTrack MCP Server")

# Add lifecycle management for the server
@dataclass
class AppContext:
    youtrack_url: str
    youtrack_token: str
    read_only: bool

@asynccontextmanager
async def app_lifespan(server: FastMCP) -> AsyncIterator[AppContext]:
    """Manage application lifecycle with context"""
    # Initialize on startup
    youtrack_url = os.environ.get("YOUTRACK_URL", "")
    youtrack_token = os.environ.get("YOUTRACK_TOKEN", "")
    read_only = os.environ.get("YOUTRACK_READ_ONLY", "false").lower() == "true"
    
    if not youtrack_url or not youtrack_token:
        logger.warning("YouTrack URL or token not configured. Set YOUTRACK_URL and YOUTRACK_TOKEN environment variables.")
    
    logger.info(f"Starting YouTrack MCP Server with URL: {youtrack_url}")
    logger.info(f"Read-only mode: {read_only}")
    
    try:
        yield AppContext(
            youtrack_url=youtrack_url, 
            youtrack_token=youtrack_token,
            read_only=read_only
        )
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down YouTrack MCP Server")

def parse_arguments():
    """Parse command line arguments for the MCP server."""
    parser = argparse.ArgumentParser(description='YouTrack MCP Server')
    parser.add_argument('--read-only', action='store_true',
                       help='Run in read-only mode (disables all write operations)')
    parser.add_argument('--youtrack-url', 
                       help='YouTrack URL (e.g., https://yourdomain.youtrack.cloud)')
    parser.add_argument('--youtrack-token',
                       help='YouTrack API permanent token')
    
    args = parser.parse_args()
    
    # Set environment variables from command line arguments
    if args.youtrack_url:
        os.environ["YOUTRACK_URL"] = args.youtrack_url
    if args.youtrack_token:
        os.environ["YOUTRACK_TOKEN"] = args.youtrack_token
    if args.read_only:
        os.environ["YOUTRACK_READ_ONLY"] = "true"
    
    return args

# Configure MCP server
mcp = FastMCP(
    server_name, 
    lifespan=app_lifespan,
    dependencies=["requests>=2.0.0", "python-dotenv>=0.19.0"]
)

# Define YouTrack tools

@mcp.tool()
def youtrack_search_issues(query: str, fields: str = "idReadable,summary,project(shortName)", 
                          custom_fields: str = None, top: int = 100, skip: int = 0) -> Dict[str, Any]:
    """
    Search for issues in YouTrack using a query.
    
    Args:
        query: The search query string (YouTrack query syntax)
        fields: Comma-separated list of fields to return for each issue
        custom_fields: Additional comma-separated list of custom fields to include
        top: The maximum number of issues to return
        skip: The number of issues to skip from the beginning of the results
    """
    logger.info(f"Searching YouTrack issues with query: '{query}'")
    return search_issues(query, fields, custom_fields, top, skip)

@mcp.tool()
def youtrack_get_issue(issue_id: str, fields: str = "idReadable,summary,description,project(shortName),customFields(projectCustomField(field(name)),value(name,login,fullName,text))", 
                      custom_fields: str = None) -> Dict[str, Any]:
    """
    Get details for a specific YouTrack issue by its ID.
    
    Args:
        issue_id: The ID of the issue (e.g., "PROJ-123")
        fields: Comma-separated list of fields to return for the issue
        custom_fields: Additional comma-separated list of custom fields to include
    """
    logger.info(f"Getting details for YouTrack issue: {issue_id}")
    return get_issue(issue_id, fields, custom_fields)

@mcp.tool()
def youtrack_update_issue(issue_id: str, data: Dict[str, Any], fields: str = "idReadable,summary") -> Dict[str, Any]:
    """
    Update an existing YouTrack issue by its ID.
    
    Args:
        issue_id: The ID of the issue to update
        data: A dictionary containing the fields to update and their new values
        fields: Comma-separated list of fields to return for the updated issue
    """
    logger.info(f"Updating YouTrack issue {issue_id}")
    return update_issue(issue_id, data, fields)

@mcp.tool()
def youtrack_add_comment(issue_id: str, comment_text: str, fields: str = "id,text,author(login)") -> Dict[str, Any]:
    """
    Add a comment to a YouTrack issue.
    
    Args:
        issue_id: The ID of the issue to comment on
        comment_text: The text content of the comment
        fields: Comma-separated list of fields to return for the created comment
    """
    logger.info(f"Adding comment to YouTrack issue {issue_id}")
    return add_comment(issue_id, comment_text, fields)

# Resource for server info
@mcp.resource("server://info")
def server_info() -> Dict[str, Any]:
    """Get YouTrack MCP Server information"""
    return {
        "status": "ok", 
        "version": "0.2.0", 
        "server": server_name,
        "youtrack_url": os.environ.get("YOUTRACK_URL", "Not configured")
    }

# Resource for accessing YouTrack projects
@mcp.resource("youtrack://projects")
def get_projects() -> str:
    """Get a list of YouTrack projects"""
    return "This resource provides access to YouTrack projects. Use youtrack_search_issues tool to query projects."

# Explicitly register the tools/list endpoint
@mcp.resource("mcp://tools/list")
def list_tools():
    """List all available tools in this MCP server"""
    # This will automatically return all registered tools
    return {
        "tools": [
            {
                "name": "youtrack_search_issues",
                "description": "Search for issues in YouTrack using a query"
            },
            {
                "name": "youtrack_get_issue",
                "description": "Get details for a specific YouTrack issue by its ID"
            },
            {
                "name": "youtrack_update_issue",
                "description": "Update an existing YouTrack issue by its ID"
            },
            {
                "name": "youtrack_add_comment",
                "description": "Add a comment to a YouTrack issue"
            }
        ]
    }

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()
    
    # Run the server
    mcp.run()
