#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${ZAP_MCP_ENV_FILE:-$REPO_ROOT/.mcp/local/zap-mcp.env}"

if [[ -f "$ENV_FILE" ]]; then
  # shellcheck disable=SC1090
  . "$ENV_FILE"
fi

if [[ "${ZAP_MCP_SECURITY_KEY:-}" == "\${env:ZAP_MCP_SECURITY_KEY}" ]]; then
  unset ZAP_MCP_SECURITY_KEY
fi

if [[ -z "${ZAP_MCP_SECURITY_KEY:-}" ]]; then
  echo "ZAP_MCP_SECURITY_KEY is not available. Run .mcp/scripts/start-zap.sh first." >&2
  exit 1
fi

ZAP_MCP_URL="${ZAP_MCP_URL:-http://127.0.0.1:${ZAP_MCP_PORT:-8282}}"
export ZAP_MCP_AUTH_HEADER="$ZAP_MCP_SECURITY_KEY"
unset ZAP_MCP_SECURITY_KEY ZAP_API_KEY

exec npx -y mcp-remote \
  "$ZAP_MCP_URL" \
  --transport http-only \
  --allow-http \
  --silent \
  --header 'Authorization:${ZAP_MCP_AUTH_HEADER}'
