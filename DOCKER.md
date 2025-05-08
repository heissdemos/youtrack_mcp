# YouTrack MCP Server Docker Guide

This document explains how to build and run the YouTrack MCP Server in a Docker container.

## Quick Start

1. Create a `.env` file with your YouTrack configuration:
   ```bash
   cp .env.example .env
   # Edit .env with your actual YouTrack URL and token
   ```

2. Build the Docker image:
   ```bash
   docker build -t youtrack-mcp:latest .
   ```

3. Run the container using environment variables from your `.env` file:
   ```bash
   docker run -d --name youtrack-mcp-server \
     -p 8000:8000 \
     --env-file ./.env \
     youtrack-mcp:latest
   ```

## Available Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| YOUTRACK_URL | URL of your YouTrack instance | (required) |
| YOUTRACK_TOKEN | Permanent API token | (required) |
| YOUTRACK_READ_ONLY | Enable read-only mode | false |
| MCP_SERVER_NAME | Name of the MCP server | YouTrack MCP Server |
| MCP_HOST | Host to bind the server to | 0.0.0.0 |
| MCP_PORT | Port to bind the server to | 8000 |
| MCP_LOG_LEVEL | Logging level (DEBUG, INFO, WARNING, ERROR) | INFO |

## Testing the Server

Once the container is running, you can check if it's working by accessing the health endpoint:

```bash
curl http://localhost:8000/health
```

You should receive a response indicating the server is healthy:

```json
{"status":"ok","version":"0.1.0","env":"https://yourdomain.youtrack.cloud/"}
```

## Checking Server Information

You can also check the server information:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"name": "server_info"}' http://localhost:8000/mcp
```

Example response:
```json
{"status": "success", "result": {"status": "ok", "version": "0.1.0", "server": "YouTrack MCP Server"}}
```

## Production Deployment

For production deployment, consider:

1. Using a specific tag version instead of 'latest'
2. Setting up proper log collection
3. Using a container orchestration platform (Kubernetes, Docker Swarm)
4. Setting up a reverse proxy with TLS termination

## Example Docker Compose Configuration

```yaml
version: '3'

services:
  youtrack-mcp:
    build: .
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "/app/healthcheck.sh"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
```