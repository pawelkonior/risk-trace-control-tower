import { existsSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { fileURLToPath } from "node:url";
import { spawn } from "node:child_process";

const __dirname = dirname(fileURLToPath(import.meta.url));
const frontendDir = resolve(__dirname, "..");
const backendDir = resolve(frontendDir, "..", "backend");
const isWindows = process.platform === "win32";

const backendVenvUvicorn = join(
  backendDir,
  ".venv",
  isWindows ? "Scripts" : "bin",
  isWindows ? "uvicorn.exe" : "uvicorn",
);

const backendCommand = existsSync(backendVenvUvicorn)
  ? {
      command: backendVenvUvicorn,
      args: [
        "rwa_calculator.rwa_calculator.fastapi_app:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
      ],
    }
  : {
      command: isWindows ? "uv.cmd" : "uv",
      args: [
        "run",
        "uvicorn",
        "rwa_calculator.rwa_calculator.fastapi_app:app",
        "--host",
        "127.0.0.1",
        "--port",
        "8000",
      ],
    };

let shuttingDown = false;
const children = [];

function spawnManaged(command, args, cwd) {
  const child = spawn(command, args, {
    cwd,
    env: process.env,
    stdio: "inherit",
  });
  children.push(child);
  child.on("exit", (code) => {
    if (!shuttingDown && code !== null && code !== 0) {
      shutdown(code);
    }
  });
  child.on("error", (error) => {
    console.error(error);
    shutdown(1);
  });
  return child;
}

spawnManaged(backendCommand.command, backendCommand.args, backendDir);
await waitForBackend();
spawnManaged(
  isWindows ? "cmd.exe" : "npm",
  isWindows
    ? ["/d", "/s", "/c", "npm run dev -- --host 127.0.0.1 --port 5173"]
    : ["run", "dev", "--", "--host", "127.0.0.1", "--port", "5173"],
  frontendDir,
);

function stopChild(child) {
  if (!child.pid || child.killed) {
    return;
  }
  if (isWindows) {
    spawn("taskkill", ["/pid", String(child.pid), "/T", "/F"], { stdio: "ignore" });
    return;
  }
  child.kill("SIGTERM");
}

function shutdown(exitCode = 0) {
  if (shuttingDown) {
    return;
  }
  shuttingDown = true;
  for (const child of children) {
    stopChild(child);
  }
  setTimeout(() => process.exit(exitCode), 250);
}

async function waitForBackend() {
  const deadline = Date.now() + 90_000;
  while (Date.now() < deadline) {
    try {
      const response = await fetch("http://127.0.0.1:8000/health");
      if (response.ok) {
        return;
      }
    } catch {
      // Retry below.
    }
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  console.error("Backend did not become healthy before Playwright startup timeout.");
  shutdown(1);
  throw new Error("Backend startup timed out.");
}

process.on("SIGINT", () => shutdown());
process.on("SIGTERM", () => shutdown());
