#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd -- "$SCRIPT_DIR/../.." && pwd)"
SONAR_ENV_FILE="${SONARQUBE_MCP_ENV_FILE:-$REPO_ROOT/.mcp/local/sonarqube-mcp.env}"
TARGET="${1:-all}"

usage() {
  cat >&2 <<'EOF'
Usage: .mcp/scripts/scan-sonarqube.sh [backend|frontend|all]

Runs SonarScanner against local SonarQube using the local token in
.mcp/local/sonarqube-mcp.env. Run .mcp/scripts/setup-sonarqube.sh first.
EOF
}

if [[ "$TARGET" == "-h" || "$TARGET" == "--help" ]]; then
  usage
  exit 0
fi

if [[ "$TARGET" != "backend" && "$TARGET" != "frontend" && "$TARGET" != "all" ]]; then
  usage
  exit 2
fi

if [[ ! -f "$SONAR_ENV_FILE" ]]; then
  echo "Missing $SONAR_ENV_FILE. Run .mcp/scripts/setup-sonarqube.sh first." >&2
  exit 1
fi

set -a
# shellcheck disable=SC1090
. "$SONAR_ENV_FILE"
set +a

if [[ -z "${SONARQUBE_URL:-}" || -z "${SONARQUBE_TOKEN:-}" ]]; then
  echo "SONARQUBE_URL and SONARQUBE_TOKEN are required in $SONAR_ENV_FILE." >&2
  exit 1
fi

run_scan() {
  local name="$1"
  local settings_file="$2"

  echo "Running SonarQube scan for ${name}..."
  docker run --rm \
    --pull=missing \
    --network host \
    -e SONAR_HOST_URL="$SONARQUBE_URL" \
    -e SONAR_TOKEN="$SONARQUBE_TOKEN" \
    -v "$REPO_ROOT:/usr/src" \
    sonarsource/sonar-scanner-cli \
    -Dproject.settings="$settings_file"
}

if [[ "$TARGET" == "backend" || "$TARGET" == "all" ]]; then
  run_scan "backend" ".mcp/sonarqube/backend-project.properties"
fi

if [[ "$TARGET" == "frontend" || "$TARGET" == "all" ]]; then
  run_scan "frontend" ".mcp/sonarqube/frontend-project.properties"
fi
