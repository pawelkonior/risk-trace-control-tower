#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import secrets
import stat
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Mapping
from pathlib import Path
from typing import Any, TextIO

BACKEND_PROJECT_KEY = "risktrace-control-tower-backend"
FRONTEND_PROJECT_KEY = "risktrace-control-tower-frontend"
BACKEND_PROJECT_NAME = "RiskTrace Control Tower Backend"
FRONTEND_PROJECT_NAME = "RiskTrace Control Tower Frontend"
DEFAULT_SONAR_URL = "http://127.0.0.1:9000"
DEFAULT_ZAP_PORT = "8090"
DEFAULT_ZAP_MCP_PORT = "8282"
DEFAULT_ZAP_TARGET_URL = "http://127.0.0.1:5173"
ENV_REF_PREFIX = "${env:"


def env_ref(name: str) -> str:
    return f"{ENV_REF_PREFIX}{name}}}"


def default_repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def mcp_dir(repo_root: Path) -> Path:
    return repo_root / ".mcp"


def local_dir(repo_root: Path) -> Path:
    return mcp_dir(repo_root) / "local"


def read_env_file(path: Path) -> dict[str, str]:
    if not path.exists():
        return {}

    values: dict[str, str] = {}
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export ") :].strip()
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip("'").strip('"')
        if key:
            values[key] = value
    return values


def write_env_file(path: Path, values: Mapping[str, str], header: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {line}" for line in header.splitlines()]
    lines.append("")
    lines.extend(f"{key}={value}" for key, value in values.items())
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def shell_quote(value: str) -> str:
    return "'" + value.replace("'", "'\"'\"'") + "'"


def write_export_env_file(path: Path, values: Mapping[str, str], header: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {line}" for line in header.splitlines()]
    lines.append("")
    for key, value in values.items():
        lines.append(f"export {key}={shell_quote(value)}")
    lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")
    path.chmod(stat.S_IRUSR | stat.S_IWUSR)


def ensure_env_file(path: Path, values: Mapping[str, str], header: str) -> str | None:
    if not path.exists():
        write_env_file(path, values, header)
        return "created"

    existing = read_env_file(path)
    missing_values = {key: value for key, value in values.items() if key not in existing}
    if not missing_values:
        return None

    merged_values = dict(values)
    merged_values.update(existing)
    write_env_file(path, merged_values, header)
    return "updated"


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    path.chmod(stat.S_IRWXU)


def random_secret(prefix: str) -> str:
    return f"{prefix}_{secrets.token_urlsafe(32)}"


def is_available_secret(value: str | None) -> bool:
    if value is None:
        return False
    stripped = value.strip()
    return bool(stripped) and not (stripped.startswith("<") and stripped.endswith(">"))


def compose_env_path(repo_root: Path) -> Path:
    return local_dir(repo_root) / "sonarqube-compose.env"


def sonarqube_mcp_env_path(repo_root: Path) -> Path:
    return local_dir(repo_root) / "sonarqube-mcp.env"


def zap_env_path(repo_root: Path) -> Path:
    return local_dir(repo_root) / "zap-mcp.env"


def mcp_export_env_path(repo_root: Path) -> Path:
    return local_dir(repo_root) / "mcp-env.sh"


def ensure_local_env(repo_root: Path, env: Mapping[str, str]) -> list[str]:
    ensure_private_dir(local_dir(repo_root))
    messages: list[str] = []

    compose_path = compose_env_path(repo_root)
    compose_status = ensure_env_file(
        compose_path,
        {
            "SONAR_POSTGRES_DB": env.get("SONAR_POSTGRES_DB", "risktrace_sonarqube"),
            "SONAR_POSTGRES_USER": env.get("SONAR_POSTGRES_USER", "risktrace_sonar"),
            "SONAR_POSTGRES_PASSWORD": env.get(
                "SONAR_POSTGRES_PASSWORD", random_secret("sonar_db")
            ),
            "SONARQUBE_PORT": env.get("SONARQUBE_PORT", "9000"),
            "SONARQUBE_ADMIN_USER": env.get("SONARQUBE_ADMIN_USER", "admin"),
            "SONARQUBE_ADMIN_PASSWORD": env.get("SONARQUBE_ADMIN_PASSWORD", "admin"),
            "ZAP_PORT": env.get("ZAP_PORT", DEFAULT_ZAP_PORT),
        },
        "Local SonarQube Docker Compose values.\n"
        "This file may contain local-only passwords and is ignored by git.",
    )
    if compose_status:
        messages.append(f"{compose_status} {compose_path.relative_to(repo_root)}")

    zap_path = zap_env_path(repo_root)
    existing_zap_values = read_env_file(zap_path)
    compose_values = read_env_file(compose_path)
    zap_port = env.get("ZAP_PORT") or compose_values.get("ZAP_PORT", DEFAULT_ZAP_PORT)
    zap_mcp_port = (
        env.get("ZAP_MCP_PORT") or existing_zap_values.get("ZAP_MCP_PORT") or DEFAULT_ZAP_MCP_PORT
    )
    zap_status = ensure_env_file(
        zap_path,
        {
            "ZAP_BASE_URL": env.get("ZAP_BASE_URL", f"http://127.0.0.1:{zap_port}"),
            "ZAP_API_KEY": env.get("ZAP_API_KEY", random_secret("zap")),
            "ZAP_MCP_PORT": zap_mcp_port,
            "ZAP_MCP_URL": env.get("ZAP_MCP_URL", f"http://127.0.0.1:{zap_mcp_port}"),
            "ZAP_MCP_SECURITY_KEY": env.get("ZAP_MCP_SECURITY_KEY", random_secret("zap_mcp")),
            "ZAP_MCP_TARGET_URL": env.get("ZAP_MCP_TARGET_URL", DEFAULT_ZAP_TARGET_URL),
        },
        "Local OWASP ZAP API and MCP add-on values.\n"
        "This file may contain local-only API keys and is ignored by git.",
    )
    if zap_status:
        messages.append(f"{zap_status} {zap_path.relative_to(repo_root)}")

    return messages


def write_mcp_export_env(repo_root: Path, env: Mapping[str, str]) -> Path:
    values = merged_local_env(repo_root, env)
    export_keys = (
        "ZAP_BASE_URL",
        "ZAP_API_KEY",
        "ZAP_MCP_PORT",
        "ZAP_MCP_URL",
        "ZAP_MCP_SECURITY_KEY",
        "ZAP_MCP_TARGET_URL",
        "SONARQUBE_URL",
        "SONARQUBE_TOKEN",
        "SONARQUBE_TOOLSETS",
        "SONARQUBE_BACKEND_PROJECT_KEY",
        "SONARQUBE_FRONTEND_PROJECT_KEY",
    )
    exports = {
        key: values[key]
        for key in export_keys
        if key in values and is_available_secret(values.get(key))
    }
    export_path = mcp_export_env_path(repo_root)
    write_export_env_file(
        export_path,
        exports,
        "Local MCP environment exports generated from .mcp/local/*.env.\n"
        "Source this file, or source .mcp/scripts/generate-mcp-config.sh, "
        "before launching IBM Bob.",
    )
    return export_path


def merged_local_env(repo_root: Path, env: Mapping[str, str]) -> dict[str, str]:
    merged: dict[str, str] = {}
    for path in (
        compose_env_path(repo_root),
        zap_env_path(repo_root),
        sonarqube_mcp_env_path(repo_root),
    ):
        merged.update(read_env_file(path))
    merged.update(env)
    return merged


def http_request(
    method: str,
    url: str,
    *,
    auth_user: str,
    auth_password: str,
    data: Mapping[str, str] | None = None,
    timeout: float = 15.0,
) -> dict[str, Any]:
    encoded_data = None
    headers = {"Accept": "application/json"}
    if data is not None:
        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        headers["Content-Type"] = "application/x-www-form-urlencoded"

    token = base64.b64encode(f"{auth_user}:{auth_password}".encode()).decode("ascii")
    headers["Authorization"] = f"Basic {token}"
    request = urllib.request.Request(url, data=encoded_data, headers=headers, method=method)  # noqa: S310

    with urllib.request.urlopen(request, timeout=timeout) as response:  # noqa: S310
        body = response.read().decode("utf-8")
    if not body:
        return {}
    return json.loads(body)


def wait_for_sonarqube(
    sonar_url: str,
    *,
    auth_user: str,
    auth_password: str,
    timeout_seconds: int,
    stream: TextIO,
) -> None:
    deadline = time.monotonic() + timeout_seconds
    status_url = f"{sonar_url.rstrip('/')}/api/system/status"
    last_error = ""

    while time.monotonic() < deadline:
        try:
            payload = http_request(
                "GET",
                status_url,
                auth_user=auth_user,
                auth_password=auth_password,
                timeout=10.0,
            )
            status = str(payload.get("status", ""))
            if status == "UP":
                print("SonarQube is UP.", file=stream)
                return
            last_error = f"SonarQube status is {status or 'unknown'}"
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            last_error = str(exc)

        time.sleep(5)

    raise RuntimeError(f"Timed out waiting for SonarQube at {sonar_url}: {last_error}")


def ensure_sonarqube_project(
    sonar_url: str,
    *,
    auth_user: str,
    auth_password: str,
    key: str,
    name: str,
    stream: TextIO,
) -> None:
    base_url = sonar_url.rstrip("/")
    query = urllib.parse.urlencode({"projects": key})
    payload = http_request(
        "GET",
        f"{base_url}/api/projects/search?{query}",
        auth_user=auth_user,
        auth_password=auth_password,
    )
    components = payload.get("components", [])
    if any(component.get("key") == key for component in components):
        print(f"SonarQube project already exists: {key}", file=stream)
        return

    http_request(
        "POST",
        f"{base_url}/api/projects/create",
        auth_user=auth_user,
        auth_password=auth_password,
        data={"project": key, "name": name},
    )
    print(f"Created SonarQube project: {key}", file=stream)


def generate_sonarqube_token(
    sonar_url: str,
    *,
    auth_user: str,
    auth_password: str,
    token_name: str,
) -> str:
    payload = http_request(
        "POST",
        f"{sonar_url.rstrip('/')}/api/user_tokens/generate",
        auth_user=auth_user,
        auth_password=auth_password,
        data={"name": token_name},
    )
    token = payload.get("token")
    if not isinstance(token, str) or not token:
        raise RuntimeError("SonarQube did not return a user token.")
    return token


def configure_sonarqube(repo_root: Path, env: Mapping[str, str], timeout_seconds: int) -> None:
    ensure_local_env(repo_root, env)
    values = merged_local_env(repo_root, env)
    sonar_url = values.get("SONARQUBE_URL", DEFAULT_SONAR_URL)
    auth_user = values.get("SONARQUBE_ADMIN_USER", "admin")
    auth_password = values.get("SONARQUBE_ADMIN_PASSWORD", "admin")

    wait_for_sonarqube(
        sonar_url,
        auth_user=auth_user,
        auth_password=auth_password,
        timeout_seconds=timeout_seconds,
        stream=sys.stdout,
    )
    ensure_sonarqube_project(
        sonar_url,
        auth_user=auth_user,
        auth_password=auth_password,
        key=values.get("SONARQUBE_BACKEND_PROJECT_KEY", BACKEND_PROJECT_KEY),
        name=values.get("SONARQUBE_BACKEND_PROJECT_NAME", BACKEND_PROJECT_NAME),
        stream=sys.stdout,
    )
    ensure_sonarqube_project(
        sonar_url,
        auth_user=auth_user,
        auth_password=auth_password,
        key=values.get("SONARQUBE_FRONTEND_PROJECT_KEY", FRONTEND_PROJECT_KEY),
        name=values.get("SONARQUBE_FRONTEND_PROJECT_NAME", FRONTEND_PROJECT_NAME),
        stream=sys.stdout,
    )

    token_path = sonarqube_mcp_env_path(repo_root)
    token_values = read_env_file(token_path)
    if is_available_secret(token_values.get("SONARQUBE_TOKEN")):
        print(f"SonarQube MCP token already stored in {token_path.relative_to(repo_root)}.")
        return

    token = generate_sonarqube_token(
        sonar_url,
        auth_user=auth_user,
        auth_password=auth_password,
        token_name=values.get("SONARQUBE_TOKEN_NAME", "risktrace-local-mcp"),
    )
    write_env_file(
        token_path,
        {
            "SONARQUBE_URL": sonar_url,
            "SONARQUBE_TOKEN": token,
            "SONARQUBE_TOOLSETS": values.get(
                "SONARQUBE_TOOLSETS", "projects,analysis,issues,quality-gates"
            ),
            "SONARQUBE_BACKEND_PROJECT_KEY": values.get(
                "SONARQUBE_BACKEND_PROJECT_KEY", BACKEND_PROJECT_KEY
            ),
            "SONARQUBE_FRONTEND_PROJECT_KEY": values.get(
                "SONARQUBE_FRONTEND_PROJECT_KEY", FRONTEND_PROJECT_KEY
            ),
        },
        "Local SonarQube MCP user token.\n"
        "This file contains a local-only token and is ignored by git.",
    )
    print(f"Stored local SonarQube MCP token in {token_path.relative_to(repo_root)}.")
    export_path = write_mcp_export_env(repo_root, env)
    print(f"Updated local MCP env exports in {export_path.relative_to(repo_root)}.")


def server_entry(command: Path, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    entry: dict[str, Any] = {"command": str(command)}
    if env:
        entry["env"] = dict(env)
    return entry


def bob_http_server_entry(
    url: str,
    headers: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "type": "streamable-http",
        "url": url,
        "headers": dict(headers),
        "alwaysAllow": [],
        "disabled": False,
    }


def vscode_http_server_entry(
    url: str,
    headers: Mapping[str, str],
) -> dict[str, Any]:
    return {
        "type": "http",
        "url": url,
        "headers": dict(headers),
    }


def zap_bridge_server_entry(repo_root: Path) -> dict[str, Any]:
    return server_entry(
        Path(".mcp") / "scripts" / "run-zap-mcp.sh",
        {"ZAP_MCP_ENV_FILE": str(zap_env_path(repo_root))},
    )


def build_servers(
    repo_root: Path,
    env: Mapping[str, str],
    stream: TextIO,
) -> tuple[dict[str, Any], dict[str, Any]]:
    ensure_local_env(repo_root, env)
    values = merged_local_env(repo_root, env)
    scripts_dir = Path(".mcp") / "scripts"
    bob_servers: dict[str, Any] = {}
    vscode_servers: dict[str, Any] = {}

    sonar_token = values.get("SONARQUBE_TOKEN")
    sonar_env_file = sonarqube_mcp_env_path(repo_root)
    if is_available_secret(sonar_token) or sonar_env_file.exists():
        sonar_env: dict[str, str] = {"SONARQUBE_MCP_ENV_FILE": str(sonar_env_file)}
        if is_available_secret(env.get("SONARQUBE_TOKEN")):
            sonar_env["SONARQUBE_TOKEN"] = env_ref("SONARQUBE_TOKEN")
            sonar_env["SONARQUBE_URL"] = values.get("SONARQUBE_URL", DEFAULT_SONAR_URL)
        sonar_server = server_entry(scripts_dir / "run-sonarqube-mcp.sh", sonar_env)
        bob_servers["risktrace-sonarqube"] = sonar_server
        vscode_servers["risktrace-sonarqube"] = sonar_server
    else:
        print(
            "Skipping SonarQube MCP: run .mcp/scripts/setup-sonarqube.sh first "
            "or export SONARQUBE_TOKEN.",
            file=stream,
        )

    zap_mcp_url = values.get(
        "ZAP_MCP_URL",
        f"http://127.0.0.1:{values.get('ZAP_MCP_PORT', DEFAULT_ZAP_MCP_PORT)}",
    )
    zap_mcp_security_key = values.get("ZAP_MCP_SECURITY_KEY")
    if is_available_secret(zap_mcp_security_key):
        bob_servers["owaspZap"] = zap_bridge_server_entry(repo_root)
        vscode_servers["owaspZap"] = vscode_http_server_entry(
            zap_mcp_url,
            {"Authorization": env_ref("ZAP_MCP_SECURITY_KEY")},
        )
    else:
        print(
            "Skipping OWASP ZAP MCP: ZAP_MCP_SECURITY_KEY is not available in "
            ".mcp/local/zap-mcp.env.",
            file=stream,
        )

    if is_available_secret(env.get("SONATYPE_GUIDE_MCP_TOKEN")):
        sonatype_server = server_entry(
            scripts_dir / "run-sonatype-guide-mcp.sh",
            {"SONATYPE_GUIDE_MCP_TOKEN": env_ref("SONATYPE_GUIDE_MCP_TOKEN")},
        )
        bob_servers["sonatype-guide"] = sonatype_server
        vscode_servers["sonatype-guide"] = sonatype_server
    else:
        print(
            "Skipping Sonatype Guide MCP: SONATYPE_GUIDE_MCP_TOKEN is not set in "
            "the local environment.",
            file=stream,
        )

    return bob_servers, vscode_servers


def write_json(path: Path, payload: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def read_json_file(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"{path} is not valid JSON: {exc}") from exc
    if not isinstance(payload, dict):
        raise RuntimeError(f"{path} must contain a JSON object.")
    return payload


def merge_server_config(
    existing: Mapping[str, Any],
    *,
    server_key: str,
    servers: Mapping[str, Any],
) -> dict[str, Any]:
    merged = dict(existing)
    existing_servers = merged.get(server_key, {})
    if not isinstance(existing_servers, dict):
        raise RuntimeError(f"Existing {server_key} config must be a JSON object.")

    merged_servers = dict(existing_servers)
    for key in (
        "risktrace-sonarqube",
        "risktrace-zap",
        "owaspZap",
        "sonatype-guide",
    ):
        if key in servers:
            merged_servers[key] = servers[key]
        else:
            merged_servers.pop(key, None)

    merged[server_key] = merged_servers
    merged["_risktrace"] = {
        "generatedBy": ".mcp/scripts/generate-mcp-config.sh",
        "secretPolicy": "MCP config uses environment references and local launcher env files only.",
    }
    return merged


def generate_config(repo_root: Path, env: Mapping[str, str], stream: TextIO = sys.stdout) -> None:
    bob_servers, vscode_servers = build_servers(repo_root, env, stream)
    export_path = write_mcp_export_env(repo_root, env)
    bob_path = repo_root / ".bob" / "mcp.json"
    vscode_path = repo_root / ".vscode" / "mcp.json"

    bob_config = merge_server_config(
        read_json_file(bob_path),
        server_key="mcpServers",
        servers=bob_servers,
    )
    vscode_config = merge_server_config(
        read_json_file(vscode_path),
        server_key="servers",
        servers=vscode_servers,
    )
    write_json(bob_path, bob_config)
    write_json(vscode_path, vscode_config)

    print(f"Updated IBM Bob MCP config: {bob_path.relative_to(repo_root)}", file=stream)
    print(f"Updated VS Code MCP config: {vscode_path.relative_to(repo_root)}", file=stream)
    print(f"Updated MCP env exports: {export_path.relative_to(repo_root)}", file=stream)
    print(
        "IBM Bob config is safe to commit; secrets are loaded through env references "
        "or local launcher env files.",
        file=stream,
    )
    print("VS Code MCP config remains local-only and ignored by git.", file=stream)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RiskTrace local MCP tooling helper.")
    parser.add_argument("--repo-root", type=Path, default=default_repo_root())
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("init-local-env", help="Create gitignored local env files.")

    configure_parser = subparsers.add_parser(
        "configure-sonarqube",
        help="Wait for local SonarQube, create projects, and store a local MCP token.",
    )
    configure_parser.add_argument("--wait-timeout", type=int, default=300)

    subparsers.add_parser(
        "generate-config",
        help="Generate IBM Bob and VS Code MCP client configuration.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    repo_root = args.repo_root.resolve()

    try:
        if args.command == "init-local-env":
            for message in ensure_local_env(repo_root, os.environ):
                print(message)
            export_path = write_mcp_export_env(repo_root, os.environ)
            print(f"updated {export_path.relative_to(repo_root)}")
            return 0
        if args.command == "configure-sonarqube":
            configure_sonarqube(repo_root, os.environ, args.wait_timeout)
            return 0
        if args.command == "generate-config":
            generate_config(repo_root, os.environ)
            return 0
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
