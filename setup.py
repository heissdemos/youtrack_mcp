# setup.py - Setup and configuration script for YouTrack MCP Server

import os
import sys
import argparse
import subprocess
from typing import Dict, Any, Optional, List

def parse_arguments():
    """Parse command line arguments for setting up and installing the MCP server."""
    parser = argparse.ArgumentParser(description='Setup and install YouTrack MCP Server')
    
    # Commands
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Setup command - environment configuration
    setup_parser = subparsers.add_parser('setup', help='Setup environment')
    setup_parser.add_argument('--youtrack-url', required=True,
                             help='Your YouTrack URL (e.g., https://yourdomain.youtrack.cloud)')
    setup_parser.add_argument('--youtrack-token', required=True,
                             help='YouTrack API permanent token')
    setup_parser.add_argument('--server-name', default='YouTrack MCP Server',
                             help='MCP server name')
    
    # Install command - install to Claude Desktop
    install_parser = subparsers.add_parser('install', help='Install to Claude Desktop')
    install_parser.add_argument('--name', default='YouTrack MCP Server',
                              help='Server name in Claude Desktop')
    
    # Run command - run the server
    run_parser = subparsers.add_parser('run', help='Run the server')
    run_parser.add_argument('--read-only', action='store_true',
                          help='Run in read-only mode')
    
    # Dev command - run in development mode
    dev_parser = subparsers.add_parser('dev', help='Run in development mode')
    
    return parser.parse_args()

def create_env_file(youtrack_url: str, youtrack_token: str, server_name: str) -> None:
    """Create .env file with server settings."""
    env_content = f"""# YouTrack MCP Server - Environment Settings
# Created automatically by setup.py

# YouTrack
YOUTRACK_URL={youtrack_url}
YOUTRACK_TOKEN={youtrack_token}

# MCP server
MCP_SERVER_NAME={server_name}
MCP_LOG_LEVEL=INFO
"""
    
    with open('.env', 'w') as env_file:
        env_file.write(env_content)
    
    print(f"+ .env file created with URL: {youtrack_url}")

def install_dependencies() -> None:
    """Install project dependencies."""
    print("Installing dependencies...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                       check=True)
        print("+ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"Error installing dependencies: {e}")
        sys.exit(1)

def install_in_claude(name: str) -> None:
    """Install server in Claude Desktop."""
    print(f"Installing server '{name}' in Claude Desktop...")
    try:
        subprocess.run(['mcp', 'install', 'server.py', '--name', name, '-f', '.env'], 
                      check=True)
        print(f"+ Server '{name}' successfully installed in Claude Desktop")
    except subprocess.CalledProcessError as e:
        print(f"Error installing server: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: 'mcp' command not found. Make sure MCP CLI is installed")
        print("   Install it with: pip install mcp")
        sys.exit(1)

def run_server(read_only: bool = False) -> None:
    """Run the MCP server."""
    cmd = [sys.executable, 'server.py']
    if read_only:
        cmd.append('--read-only')
    
    print(f"Starting YouTrack MCP server...")
    if read_only:
        print("Read-only mode activated")
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nServer stopped")

def run_dev_mode() -> None:
    """Run the server in development mode."""
    print("Starting YouTrack MCP server in development mode...")
    try:
        subprocess.run(['mcp', 'dev', 'server.py'])
    except subprocess.CalledProcessError as e:
        print(f"Error running server in development mode: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped")
    except FileNotFoundError:
        print("Error: 'mcp' command not found. Make sure MCP CLI is installed")
        print("   Install it with: pip install mcp")
        sys.exit(1)

def main() -> None:
    """Main script function."""
    args = parse_arguments()
    
    if args.command == 'setup':
        create_env_file(args.youtrack_url, args.youtrack_token, args.server_name)
        install_dependencies()
        print("\nSetup completed! Now you can run the server:")
        print("   python setup.py run")
    
    elif args.command == 'install':
        install_in_claude(args.name)
    
    elif args.command == 'run':
        run_server(args.read_only)
    
    elif args.command == 'dev':
        run_dev_mode()
    
    else:
        print("Please specify a command. Use --help for help.")
        sys.exit(1)

if __name__ == "__main__":
    main()
