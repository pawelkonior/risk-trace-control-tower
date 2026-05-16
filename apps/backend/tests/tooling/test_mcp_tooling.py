from __future__ import annotations

import importlib.util
import io
import json
from pathlib import Path
from types import ModuleType

REPO_ROOT = Path(__file__).resolve().parents[4]
MCP_TOOLING_PATH = REPO_ROOT / ".mcp" / "scripts" / "mcp_tooling.py"


def load_mcp_tooling() -> ModuleType:
    spec = importlib.util.spec_from_file_location("risktrace_mcp_tooling", MCP_TOOLING_PATH)
    assert spec is not None
    assert spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_config(repo_root: Path, path: str) -> dict:
    config_path = repo_root / path
    return json.loads(config_path.read_text(encoding="utf-8"))


def test_generate_config_skips_sonatype_without_token(tmp_path: Path) -> None:
    tooling = load_mcp_tooling()
    stream = io.StringIO()

    (tmp_path / ".bob").mkdir()
    (tmp_path / ".bob" / "mcp.json").write_text(
        json.dumps({"mcpServers": {"atlassian": {"command": "existing-command"}}}),
        encoding="utf-8",
    )
    tooling.generate_config(tmp_path, {}, stream=stream)

    output = stream.getvalue()
    bob_config = read_config(tmp_path, ".bob/mcp.json")
    vscode_config = read_config(tmp_path, ".vscode/mcp.json")

    assert "Skipping Sonatype Guide MCP" in output
    assert bob_config["mcpServers"]["atlassian"]["command"] == "existing-command"
    assert "owaspZap" in bob_config["mcpServers"]
    assert "risktrace-zap" not in bob_config["mcpServers"]
    assert "sonatype-guide" not in bob_config["mcpServers"]
    assert "owaspZap" in vscode_config["servers"]
    assert "risktrace-zap" not in vscode_config["servers"]
    assert "sonatype-guide" not in vscode_config["servers"]
    assert (tmp_path / ".mcp" / "local" / "zap-mcp.env").exists()
    assert (tmp_path / ".mcp" / "local" / "mcp-env.sh").exists()

    zap_env = tooling.read_env_file(tmp_path / ".mcp" / "local" / "zap-mcp.env")
    export_text = (tmp_path / ".mcp" / "local" / "mcp-env.sh").read_text(encoding="utf-8")
    bob_zap = bob_config["mcpServers"]["owaspZap"]
    vscode_zap = vscode_config["servers"]["owaspZap"]
    assert bob_zap["type"] == "streamable-http"
    assert bob_zap["url"] == zap_env["ZAP_MCP_URL"]
    assert bob_zap["headers"]["Authorization"] == "${env:ZAP_MCP_SECURITY_KEY}"
    assert zap_env["ZAP_MCP_SECURITY_KEY"] not in json.dumps(bob_config)
    assert f"export ZAP_MCP_SECURITY_KEY='{zap_env['ZAP_MCP_SECURITY_KEY']}'" in export_text
    assert "command" not in bob_zap
    assert vscode_zap["type"] == "http"
    assert vscode_zap["url"] == zap_env["ZAP_MCP_URL"]
    assert vscode_zap["headers"]["Authorization"] == "${env:ZAP_MCP_SECURITY_KEY}"


def test_generate_config_references_available_tokens_without_writing_values(
    tmp_path: Path,
) -> None:
    tooling = load_mcp_tooling()
    stream = io.StringIO()
    env = {
        "SONARQUBE_URL": "http://127.0.0.1:9000",
        "SONARQUBE_TOKEN": "sonar-secret-value",
        "SONATYPE_GUIDE_MCP_TOKEN": "sonatype-secret-value",
        "ZAP_API_KEY": "zap-secret-value",
        "ZAP_MCP_SECURITY_KEY": "zap-mcp-secret-value",
    }

    tooling.generate_config(tmp_path, env, stream=stream)

    bob_text = (tmp_path / ".bob" / "mcp.json").read_text(encoding="utf-8")
    vscode_text = (tmp_path / ".vscode" / "mcp.json").read_text(encoding="utf-8")
    bob_config = json.loads(bob_text)

    assert "risktrace-sonarqube" in bob_config["mcpServers"]
    assert "owaspZap" in bob_config["mcpServers"]
    assert "sonatype-guide" in bob_config["mcpServers"]
    assert bob_config["mcpServers"]["owaspZap"]["type"] == "streamable-http"
    assert "${env:SONARQUBE_TOKEN}" in bob_text
    assert "${env:SONATYPE_GUIDE_MCP_TOKEN}" in bob_text
    assert "${env:ZAP_MCP_SECURITY_KEY}" in bob_text
    for secret_value in env.values():
        if secret_value.startswith("http://"):
            continue
        assert secret_value not in bob_text
        assert secret_value not in vscode_text


def test_gitignore_protects_generated_configs_and_local_secret_files() -> None:
    gitignore = (REPO_ROOT / ".gitignore").read_text(encoding="utf-8")

    assert ".mcp/local/" in gitignore
    assert ".mcp/.env.*" in gitignore
    assert "!.mcp/.env.example" in gitignore
    assert ".bob/mcp" not in gitignore
    assert ".vscode" in gitignore
