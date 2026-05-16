import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from '@modelcontextprotocol/sdk/types.js';
import { getConfig } from './config.js';

/**
 * Create and configure the MCP server
 */
export function createServer(): Server {
  const config = getConfig();
  
  const server = new Server(
    {
      name: config.serverName,
      version: config.serverVersion,
    },
    {
      capabilities: {
        tools: {},
      },
    }
  );

  // List available tools
  server.setRequestHandler(ListToolsRequestSchema, async () => {
    return {
      tools: [
        {
          name: 'get_server_info',
          description: 'Get information about the regulatory MCP server',
          inputSchema: {
            type: 'object',
            properties: {},
          },
        },
      ],
    };
  });

  // Handle tool calls
  server.setRequestHandler(CallToolRequestSchema, async (request) => {
    const { name } = request.params;

    if (name === 'get_server_info') {
      return {
        content: [
          {
            type: 'text',
            text: JSON.stringify(
              {
                serverName: config.serverName,
                serverVersion: config.serverVersion,
                projectRoot: config.projectRoot,
                dataDir: config.dataDir,
              },
              null,
              2
            ),
          },
        ],
      };
    }

    throw new Error(`Unknown tool: ${name}`);
  });

  return server;
}

// Made with Bob
