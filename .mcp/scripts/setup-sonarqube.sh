#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$REPO_ROOT/.mcp/local/sonarqube-compose.env"

python3 "$SCRIPT_DIR/mcp_tooling.py" --repo-root "$REPO_ROOT" init-local-env

docker compose \
  --env-file "$ENV_FILE" \
  --env-file "$REPO_ROOT/.mcp/local/zap-mcp.env" \
  -f "$REPO_ROOT/.mcp/docker-compose.yml" \
  up -d sonarqube-db sonarqube

python3 "$SCRIPT_DIR/mcp_tooling.py" \
  --repo-root "$REPO_ROOT" \
  configure-sonarqube "$@"
