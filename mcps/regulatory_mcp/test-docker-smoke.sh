#!/usr/bin/env bash
# Docker Smoke Test for Regulatory MCP Server
# Tests that the Docker container builds, starts, and responds correctly

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

cleanup() {
    log_info "Cleaning up..."
    docker compose down --volumes --remove-orphans 2>/dev/null || true
}

trap cleanup EXIT

# Step 1: Build the Docker image
log_info "Step 1: Building Docker image..."
if docker compose build regulatory-mcp; then
    log_info "✓ Docker image built successfully"
else
    log_error "✗ Docker image build failed"
    exit 1
fi

# Step 2: Start the container
log_info "Step 2: Starting container..."
if docker compose up -d regulatory-mcp; then
    log_info "✓ Container started"
else
    log_error "✗ Container failed to start"
    exit 1
fi

# Step 3: Wait for container to be healthy
log_info "Step 3: Waiting for container to be ready..."
MAX_WAIT=30
WAITED=0
while [ $WAITED -lt $MAX_WAIT ]; do
    if docker compose ps regulatory-mcp | grep -q "Up"; then
        log_info "✓ Container is running"
        break
    fi
    sleep 1
    WAITED=$((WAITED + 1))
done

if [ $WAITED -ge $MAX_WAIT ]; then
    log_error "✗ Container failed to become ready within ${MAX_WAIT}s"
    docker compose logs regulatory-mcp
    exit 1
fi

# Step 4: Check container logs for errors
log_info "Step 4: Checking container logs..."
LOGS=$(docker compose logs regulatory-mcp 2>&1)
if echo "$LOGS" | grep -qi "error\|exception\|failed"; then
    log_warn "Container logs contain error messages:"
    echo "$LOGS" | grep -i "error\|exception\|failed" || true
else
    log_info "✓ No errors in container logs"
fi

# Step 5: Verify corpus loaded
log_info "Step 5: Verifying corpus loaded..."
if echo "$LOGS" | grep -q "Corpus loaded"; then
    log_info "✓ Corpus loaded successfully"
    
    # Extract corpus stats from logs
    REG_COUNT=$(echo "$LOGS" | grep -oP 'regulations: \K\d+' | head -1 || echo "0")
    CTRL_COUNT=$(echo "$LOGS" | grep -oP 'controls: \K\d+' | head -1 || echo "0")
    
    if [ "$REG_COUNT" -ge 9 ]; then
        log_info "✓ Loaded $REG_COUNT regulations (expected ≥9)"
    else
        log_error "✗ Only loaded $REG_COUNT regulations (expected ≥9)"
        exit 1
    fi
    
    if [ "$CTRL_COUNT" -ge 15 ]; then
        log_info "✓ Loaded $CTRL_COUNT controls (expected ≥15)"
    else
        log_error "✗ Only loaded $CTRL_COUNT controls (expected ≥15)"
        exit 1
    fi
else
    log_error "✗ Corpus not loaded"
    exit 1
fi

# Step 6: Verify MCP server started
log_info "Step 6: Verifying MCP server started..."
if echo "$LOGS" | grep -q "MCP server started"; then
    log_info "✓ MCP server started successfully"
else
    log_error "✗ MCP server did not start"
    exit 1
fi

# Step 7: Test container can be stopped cleanly
log_info "Step 7: Testing clean shutdown..."
if docker compose stop regulatory-mcp; then
    log_info "✓ Container stopped cleanly"
else
    log_error "✗ Container failed to stop cleanly"
    exit 1
fi

# Final summary
echo ""
log_info "=========================================="
log_info "Docker Smoke Test: ${GREEN}PASSED${NC}"
log_info "=========================================="
log_info "All checks completed successfully:"
log_info "  ✓ Docker image builds"
log_info "  ✓ Container starts"
log_info "  ✓ Corpus loads (≥9 regulations, ≥15 controls)"
log_info "  ✓ MCP server starts"
log_info "  ✓ Container stops cleanly"
echo ""

# Made with Bob
