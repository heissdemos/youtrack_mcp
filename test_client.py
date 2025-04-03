#!/usr/bin/env python
# test_client.py - Simple test client for YouTrack MCP Server

import requests
import json
import sys
import subprocess
import time
from typing import Dict, Any

# Server configuration
SERVER_ENDPOINT = "http://localhost:8000/mcp"  # Default MCP endpoint

def test_server_info() -> None:
    """Test the server info resource"""
    print("Testing server info resource...")
    response = requests.post(
        SERVER_ENDPOINT,
        json={"type": "resource_request", "uri": "server://info"}
    )
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")

def test_search_issues(query: str = "project: TEST") -> None:
    """Test the search issues tool"""
    print(f"Testing search issues tool with query: '{query}'...")
    response = requests.post(
        SERVER_ENDPOINT,
        json={
            "type": "tool_call",
            "name": "youtrack_search_issues",
            "parameters": {
                "query": query,
                "top": 5
            }
        }
    )
    print(f"Response status: {response.status_code}")
    if response.status_code == 200:
        print(f"Response data: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"Error: {response.text}")

def main() -> None:
    """Run all tests"""
    print("Starting YouTrack MCP test client")
    
    # Test server info
    test_server_info()
    
    # Test search issues
    test_search_issues()

if __name__ == "__main__":
    main()
