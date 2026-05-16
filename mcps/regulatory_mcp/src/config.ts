import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * Configuration for the Regulatory MCP Server
 */
export interface ServerConfig {
  /** Root directory of the project */
  projectRoot: string;
  /** Directory for local data storage */
  dataDir: string;
  /** Server name */
  serverName: string;
  /** Server version */
  serverVersion: string;
}

/**
 * Get the server configuration
 */
export function getConfig(): ServerConfig {
  const projectRoot = join(__dirname, '..');
  const dataDir = join(projectRoot, 'data');

  return {
    projectRoot,
    dataDir,
    serverName: 'regulatory-mcp',
    serverVersion: '0.1.0',
  };
}

// Made with Bob
