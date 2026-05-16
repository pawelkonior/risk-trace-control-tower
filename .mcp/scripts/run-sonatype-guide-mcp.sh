#!/usr/bin/env bash
set -euo pipefail

if [[ "${SONATYPE_GUIDE_MCP_TOKEN:-}" == "\${env:SONATYPE_GUIDE_MCP_TOKEN}" ]]; then
  unset SONATYPE_GUIDE_MCP_TOKEN
fi

if [[ -z "${SONATYPE_GUIDE_MCP_TOKEN:-}" ]]; then
  echo "SONATYPE_GUIDE_MCP_TOKEN is not set in the local environment." >&2
  exit 1
fi

exec npx -y mcp-remote \
  https://mcp.guide.sonatype.com/mcp \
  --header "Authorization: Bearer ${SONATYPE_GUIDE_MCP_TOKEN}"
