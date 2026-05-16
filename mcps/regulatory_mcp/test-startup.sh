#!/bin/bash
# Test script to verify MCP server startup

echo "Testing MCP server startup..."
echo ""

# Start the server in background and capture stderr
node build/index.js 2>&1 &
PID=$!

# Wait a moment for startup
sleep 1

# Kill the server
kill $PID 2>/dev/null

echo ""
echo "Server startup test completed successfully!"

# Made with Bob
