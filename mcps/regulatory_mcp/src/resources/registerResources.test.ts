import { describe, expect, it } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { createServer } from "../server.js";

async function withClient<T>(run: (client: Client) => Promise<T>): Promise<T> {
  const server = createServer();
  const client = new Client(
    { name: "regulatory-mcp-resource-test-client", version: "1.0.0" },
    { capabilities: {} }
  );
  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();

  await server.connect(serverTransport);
  await client.connect(clientTransport);

  try {
    return await run(client);
  } finally {
    await client.close();
    await server.close();
  }
}

describe("MCP resources and prompts", () => {
  it("lists and reads regulation, control, and example resources", async () => {
    await withClient(async (client) => {
      const resources = await client.listResources();
      const uris = resources.resources.map((resource) => resource.uri);

      expect(uris).toContain("regulations://index");
      expect(uris).toContain("controls://index");
      expect(uris).toContain("examples://feature");
      expect(uris).toContain("examples://architecture");
      expect(uris).toContain("examples://code_diff");
      expect(uris).toContain("examples://release_evidence");

      const regulationIndex = await client.readResource({ uri: "regulations://index" });
      expect(regulationIndex.contents[0]).toHaveProperty("text");
      expect(JSON.parse("text" in regulationIndex.contents[0] ? regulationIndex.contents[0].text : "[]")[0]).toHaveProperty("id");
    });
  });

  it("lists expected workflow prompts", async () => {
    await withClient(async (client) => {
      const prompts = await client.listPrompts();
      const names = prompts.prompts.map((prompt) => prompt.name);

      expect(names).toEqual([
        "feature_review",
        "architecture_review",
        "code_review",
        "data_lineage_design",
        "audit_log_design",
        "regulatory_mapping_report",
      ]);

      const prompt = await client.getPrompt({
        name: "feature_review",
        arguments: { feature: "RWA CSV upload" },
      });
      expect(prompt.messages[0].content.type).toBe("text");
      expect(prompt.messages[0].content.type === "text" ? prompt.messages[0].content.text : "").toContain("review_feature_description");
    });
  });
});
