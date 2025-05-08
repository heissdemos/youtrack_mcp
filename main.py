# main.py - YouTrack MCP Server

import json
import sys
import logging
import argparse
from typing import Dict, Any, List, Optional, Callable

# Import the YouTrack API module
from youtrack_api import (
    search_issues, 
    get_issue, 
    update_issue, 
    add_comment,
)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger('youtrack-mcp')

# MCP Tools implementation
TOOLS = {
    # Basic YouTrack tools
    "youtrack_search_issues": search_issues,
    "youtrack_get_issue": get_issue,
    "youtrack_update_issue": update_issue,
    "youtrack_add_comment": add_comment,
    
    # MCP-specific service functions
    "server_info": lambda: {"status": "ok", "version": "0.1.0", "server": "YouTrack MCP Server"}
}

def parse_arguments():
    """Parse command line arguments for the MCP server."""
    parser = argparse.ArgumentParser(description='YouTrack MCP Server')
    parser.add_argument('--transport', choices=['stdio', 'sse'], default='stdio',
                        help='Transport type (stdio or sse)')
    parser.add_argument('--port', type=int, default=8000,
                        help='Port number for SSE transport')
    parser.add_argument('--verbose', '-v', action='count', default=0,
                        help='Increase verbosity (can be used multiple times)')
    parser.add_argument('--read-only', action='store_true',
                        help='Run in read-only mode (disables all write operations)')
    
    # Add YouTrack-specific arguments
    parser.add_argument('--youtrack-url', 
                        help='YouTrack URL (e.g., https://yourdomain.youtrack.cloud)')
    parser.add_argument('--youtrack-token',
                        help='YouTrack API permanent token')
    
    args = parser.parse_args()
    
    # Set logging level based on verbosity
    if args.verbose == 1:
        logger.setLevel(logging.INFO)
    elif args.verbose >= 2:
        logger.setLevel(logging.DEBUG)
    
    return args

def validate_request(request_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Validates the incoming MCP request format.
    
    Returns None if valid, or an error dict if invalid.
    """
    if not isinstance(request_data, dict):
        return {"error": "Request must be a JSON object"}
    
    if "name" not in request_data:
        return {"error": "Request missing 'name' field"}
    
    if request_data["name"] not in TOOLS:
        return {"error": f"Unknown tool: {request_data['name']}"}
    
    return None

def execute_tool(request_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Executes the requested tool with provided parameters.
    
    Args:
        request_data: The request object containing the tool name and parameters
        
    Returns:
        dict: Response object with results or error information
    """
    tool_name = request_data["name"]
    tool_function = TOOLS[tool_name]
    
    # Extract parameters, excluding the 'name' field
    params = {k: v for k, v in request_data.items() if k != "name"}
    
    try:
        # Call the tool function with the provided parameters
        logger.debug(f"Executing tool '{tool_name}' with params: {params}")
        if params:
            result = tool_function(**params)
        else:
            result = tool_function()
            
        return {
            "status": "success",
            "result": result
        }
    except TypeError as e:
        logger.error(f"Parameter error executing {tool_name}: {e}")
        return {
            "status": "error",
            "error": f"Invalid parameters: {str(e)}"
        }
    except Exception as e:
        logger.error(f"Error executing {tool_name}: {e}")
        return {
            "status": "error",
            "error": str(e)
        }

def handle_request(request_data: Dict[str, Any]) -> str:
    """
    Handles incoming MCP requests.
    
    Args:
        request_data: The parsed JSON request data
        
    Returns:
        str: JSON string response
    """
    logger.debug(f"Received request: {request_data}")
    
    # Validate request format
    validation_error = validate_request(request_data)
    if validation_error:
        return json.dumps(validation_error)
    
    # Execute the requested tool
    response = execute_tool(request_data)
    
    return json.dumps(response)

def start_stdio_transport():
    """Start the MCP server using stdio transport"""
    logger.info("YouTrack MCP Server started (stdio transport). Waiting for requests...")
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response_json = handle_request(request)
            print(response_json, flush=True)
        except json.JSONDecodeError:
            error_response = {"status": "error", "error": "Invalid JSON input"}
            print(json.dumps(error_response), flush=True)
        except Exception as e:
            error_response = {"status": "error", "error": str(e)}
            print(json.dumps(error_response), flush=True)

def start_sse_transport(port):
    """
    Start the MCP server using Server-Sent Events (SSE) transport
    
    Args:
        port: The port number to listen on
    """
    try:
        # Only import these if SSE transport is requested
        from flask import Flask, request, Response
        import os
        
        app = Flask(__name__)
        
        @app.route('/mcp', methods=['POST'])
        def mcp_endpoint():
            try:
                request_data = request.json
                response_json = handle_request(request_data)
                return Response(response_json, mimetype='application/json')
            except Exception as e:
                error_response = {"status": "error", "error": str(e)}
                return Response(json.dumps(error_response), mimetype='application/json')
        
        @app.route('/health', methods=['GET'])
        def health_check():
            """Einfacher Health-Check-Endpunkt"""
            return {"status": "ok", "version": "0.1.0", "env": os.environ.get("YOUTRACK_URL", "")}
        
        logger.info(f"YouTrack MCP Server started (SSE transport) on port {port}")
        app.run(host='0.0.0.0', port=port)
        
    except ImportError:
        logger.error("Flask is required for SSE transport. Install it with 'pip install flask'")
        sys.exit(1)

app = None

def create_app():
    """Erstellt und konfiguriert die Flask-App für WSGI-Server"""
    from flask import Flask
    app = Flask(__name__)

    @app.route('/mcp', methods=['POST'])
    def mcp_endpoint():
        try:
            request_data = request.json
            response_json = handle_request(request_data)
            return Response(response_json, mimetype='application/json')
        except Exception as e:
            error_response = {"status": "error", "error": str(e)}
            return Response(json.dumps(error_response), mimetype='application/json')

    @app.route('/health', methods=['GET'])
    def health_check():
        """Einfacher Health-Check-Endpunkt"""
        return {"status": "ok", "version": "0.1.0", "env": os.environ.get("YOUTRACK_URL", "")}

    return app

if __name__ == "__main__":
    args = parse_arguments()
    
    # Start the appropriate transport
    if args.transport == 'stdio':
        start_stdio_transport()
    else:  # args.transport == 'sse'
        start_sse_transport(args.port)
