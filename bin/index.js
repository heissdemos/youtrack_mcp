#!/usr/bin/env node

/**
 * YouTrack MCP Server launcher
 * This script runs the Python-based YouTrack MCP server
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');

// Get the directory where the package is installed
const packageDir = path.resolve(__dirname, '..');

// Path to the Python script
const serverPath = path.join(packageDir, 'server.py');

// Check if Python script exists
if (!fs.existsSync(serverPath)) {
  console.error(`Error: Could not find server.py at ${serverPath}`);
  process.exit(1);
}

// Run the Python script
const pythonProcess = spawn('python', [serverPath], {
  stdio: 'inherit',
  env: process.env
});

// Handle process events
pythonProcess.on('error', (err) => {
  console.error('Failed to start Python process:', err);
  process.exit(1);
});

pythonProcess.on('close', (code) => {
  if (code !== 0) {
    console.error(`Python process exited with code ${code}`);
    process.exit(code);
  }
});

// Handle termination signals
process.on('SIGINT', () => {
  pythonProcess.kill('SIGINT');
});

process.on('SIGTERM', () => {
  pythonProcess.kill('SIGTERM');
});
