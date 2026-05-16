# RiskTrace Control Tower

RiskTrace Control Tower is a monorepo with a Python backend, React/Vite frontend, and local
Docker Compose runtime under `apps/`.

## Local MCP Tooling

Repository-local MCP-assisted quality and security tooling lives in `.mcp/`.

Use it for local SonarQube, OWASP ZAP, IBM Bob/VS Code MCP config generation, and optional
Sonatype Guide dependency guidance:

```bash
.mcp/scripts/setup-sonarqube.sh
.mcp/scripts/scan-sonarqube.sh
.mcp/scripts/start-zap.sh
source .mcp/scripts/generate-mcp-config.sh
```

The generator updates committed `.bob/mcp.json` for IBM Bob and local `.vscode/mcp.json` for VS
Code. `.bob/mcp.json` contains only non-secret values, environment variable references, and local
launcher env-file paths; local secret env files remain ignored by git. OWASP ZAP MCP is served by
the official ZAP MCP Integration add-on running inside the ZAP container, bridged to Bob through a
local launcher script. Sonatype Guide is added only when `SONATYPE_GUIDE_MCP_TOKEN` is exported in
your shell. OWASP ZAP setup starts the daemon only; active scans require explicit developer action.

Use `source .mcp/scripts/generate-mcp-config.sh` when launching direct HTTP MCP clients from the
same shell; it writes `.mcp/local/mcp-env.sh` and exports the generated local MCP secrets
immediately. IBM Bob's ZAP launcher can read `.mcp/local/zap-mcp.env` directly.

See `.mcp/README.md` for the full workflow.
