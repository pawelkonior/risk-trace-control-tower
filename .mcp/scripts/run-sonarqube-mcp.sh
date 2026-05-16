#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="${SONARQUBE_MCP_ENV_FILE:-$REPO_ROOT/.mcp/local/sonarqube-mcp.env}"

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
fi

if [[ "${SONARQUBE_TOKEN:-}" == "\${env:SONARQUBE_TOKEN}" ]]; then
  unset SONARQUBE_TOKEN
fi

if [[ -z "${SONARQUBE_TOKEN:-}" ]]; then
  echo "SONARQUBE_TOKEN is not available. Run .mcp/scripts/setup-sonarqube.sh or export SONARQUBE_TOKEN." >&2
  exit 1
fi

export SONARQUBE_URL="${SONARQUBE_URL:-http://127.0.0.1:9000}"
export SONARQUBE_TOOLSETS="${SONARQUBE_TOOLSETS:-projects,analysis,issues,quality-gates}"

exec docker run \
  --init \
  --pull=missing \
  --network host \
  -i \
  --rm \
  -e SONARQUBE_URL \
  -e SONARQUBE_TOKEN \
  -e SONARQUBE_TOOLSETS \
  mcp/sonarqube
