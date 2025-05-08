#!/bin/bash
# Simple script to build and run the YouTrack MCP server in Docker

# Check if .env file exists
if [ ! -f ./.env ]; then
  echo "Error: .env file not found. Please create one based on .env.example"
  echo "cp .env.example .env"
  echo "Then edit .env with your actual YouTrack URL and token"
  exit 1
fi

# Build the Docker image
echo "Building Docker image..."
docker build -t youtrack-mcp:latest .

# Run the container
echo "Starting YouTrack MCP container..."
docker run -d --name youtrack-mcp-server \
  -p 8000:8000 \
  --env-file ./.env \
  youtrack-mcp:latest

# Check container status
echo "Container status:"
docker ps | grep youtrack-mcp-server

# Wait for server to start and then check health
echo "Waiting for server to start..."
sleep 3
echo "Checking server health:"
curl -s http://localhost:8000/health || echo "Health check not responding yet"

echo ""
echo "YouTrack MCP server should now be running at http://localhost:8000"
echo "Test with: curl -s -X POST -H \"Content-Type: application/json\" -d '{\"name\": \"server_info\"}' http://localhost:8000/mcp"
echo "To view logs: docker logs youtrack-mcp-server"
echo "To stop:      docker stop youtrack-mcp-server"
echo "To remove:    docker rm youtrack-mcp-server"