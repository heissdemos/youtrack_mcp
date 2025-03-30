# Test script for YouTrack MCP Server
import subprocess
import json
import sys

def send_request(request_data):
    """Send a request to MCP server via subprocess"""
    # Convert request to JSON string
    request_json = json.dumps(request_data)
    
    # Start the MCP server process
    process = subprocess.Popen(
        ['python', 'main.py'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Send request to stdin and get response from stdout
    stdout, stderr = process.communicate(input=request_json + '\n')
    
    # Print server output for debugging
    print("Server stderr output:")
    print(stderr)
    
    # Extract and parse the JSON response
    try:
        for line in stdout.strip().split('\n'):
            if line.startswith('{') and line.endswith('}'):
                return json.loads(line)
        return {"status": "error", "error": "No valid JSON response found"}
    except json.JSONDecodeError:
        return {"status": "error", "error": "Invalid JSON response"}

# Test 1: Server info
print("Test 1: Server info")
response = send_request({"name": "server_info"})
print(f"Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
print()

# Test 2: Search issues (if YouTrack credentials are configured)
print("Test 2: Search issues")
response = send_request({
    "name": "youtrack_search_issues",
    "query": "project: FXS",
    "top": 3
})
print(f"Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
print()

# Test 3: Unknown tool
print("Test 3: Unknown tool")
response = send_request({"name": "nonexistent_tool"})
print(f"Response: {json.dumps(response, indent=2, ensure_ascii=False)}")
