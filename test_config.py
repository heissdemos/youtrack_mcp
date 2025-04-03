# test_config.py - Configuration for testing YouTrack MCP server
# This file is for testing purposes only and should not contain real credentials

import os

# Set environment variables for testing
os.environ["YOUTRACK_URL"] = "https://example.youtrack.cloud"  # Test URL
os.environ["YOUTRACK_TOKEN"] = "test_token"  # Test token
os.environ["MCP_SERVER_NAME"] = "YouTrack MCP Test Server"
os.environ["MCP_LOG_LEVEL"] = "DEBUG"  # Use DEBUG for more detailed logs during testing
