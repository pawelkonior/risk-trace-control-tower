#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$REPO_ROOT/.mcp/local/mcp-env.sh"

if [[ ! -f "$ENV_FILE" ]]; then
  python3 "$SCRIPT_DIR/mcp_tooling.py" --repo-root "$REPO_ROOT" init-local-env >/dev/null
fi

set -a
# shellcheck disable=SC1090
. "$ENV_FILE"
set +a

if [[ "$#" -eq 0 ]]; then
  echo "Usage: .mcp/scripts/with-mcp-env.sh <command> [args...]" >&2
  exit 2
fi

exec "$@"
