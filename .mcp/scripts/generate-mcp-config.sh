#!/usr/bin/env bash
if [[ "${BASH_SOURCE[0]}" != "$0" ]]; then
  SOURCED=1
else
  SOURCED=0
  set -euo pipefail
fi

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$REPO_ROOT/.mcp/local/mcp-env.sh"

if ! python3 "$SCRIPT_DIR/mcp_tooling.py" --repo-root "$REPO_ROOT" generate-config "$@"; then
  STATUS=$?
  if [[ "$SOURCED" -eq 1 ]]; then
    return "$STATUS"
  fi
  exit "$STATUS"
fi

if [[ -f "$ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  . "$ENV_FILE"
  set +a
  echo "Exported MCP environment variables from .mcp/local/mcp-env.sh."
fi

if [[ "$SOURCED" -eq 1 ]]; then
  return 0
fi
