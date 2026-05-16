#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"

python3 "$SCRIPT_DIR/mcp_tooling.py" --repo-root "$REPO_ROOT" init-local-env

set -a
# shellcheck disable=SC1091
. "$REPO_ROOT/.mcp/local/sonarqube-compose.env"
# shellcheck disable=SC1091
. "$REPO_ROOT/.mcp/local/zap-mcp.env"
set +a

docker compose \
  --env-file "$REPO_ROOT/.mcp/local/sonarqube-compose.env" \
  --env-file "$REPO_ROOT/.mcp/local/zap-mcp.env" \
  -f "$REPO_ROOT/.mcp/docker-compose.yml" \
  up -d zap

echo "OWASP ZAP daemon is configured at http://127.0.0.1:${ZAP_PORT:-8090}."
echo "OWASP ZAP MCP add-on is configured at ${ZAP_MCP_URL:-http://127.0.0.1:${ZAP_MCP_PORT:-8282}}."
echo "No spider or active scan was started."
