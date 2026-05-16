import { describe, expect, it } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { createServer } from "../server.js";
import { getToolDefinitions } from "./registerTools.js";

async function withClient<T>(run: (client: Client) => Promise<T>): Promise<T> {
  const server = createServer();
  const client = new Client(
    { name: "regulatory-mcp-test-client", version: "1.0.0" },
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

describe("MCP tools", () => {
  it("registers health_check plus fourteen functional tools with schemas and read-only annotations", async () => {
    await withClient(async (client) => {
      const result = await client.listTools();

      expect(result.tools).toHaveLength(15);
      expect(result.tools.map((tool) => tool.name)).toContain("health_check");
      expect(result.tools.every((tool) => tool.inputSchema)).toBe(true);
      expect(result.tools.every((tool) => tool.outputSchema)).toBe(true);
      expect(result.tools.every((tool) => tool.annotations?.readOnlyHint)).toBe(true);
      expect(result.tools.every((tool) => tool.annotations?.destructiveHint === false)).toBe(true);
    });
  });

  it("supports a representative call for every registered tool", async () => {
    const examples: Record<string, Record<string, unknown>> = {
      health_check: { include_corpus: true },
      get_regulatory_profile: { domains: ["capital_adequacy"] },
      search_regulations: { query: "data lineage for RWA calculation", limit: 3 },
      match_controls: { text: "CSV upload for RWA calculation", artifact_type: "feature" },
      review_feature_description: {
        description: "CSV upload for exposures and RWA calculation.",
      },
      review_architecture_text: {
        architecture_text: "Architecture hardcoded risk weight values inside the service.",
      },
      review_code_diff: {
        diff: "+ const riskWeight = 0.35;\n+ logger.info(customer.email);\n+ return amount * riskWeight;",
      },
      generate_acceptance_criteria: { control_ids: ["RWA-DATA-001"] },
      generate_data_lineage_requirements: {},
      generate_audit_log_requirements: {},
      generate_test_obligations: { control_ids: ["TEST-REG-001"] },
      assess_release_readiness: { implemented_control_ids: ["RWA-CALC-001"], evidence: [] },
      generate_regulatory_mapping_report: {
        feature_text: "RWA CSV upload and calculation",
      },
      generate_rwa_run_evidence_requirements: {},
      explain_control: { control_id: "RWA-RULE-001" },
    };

    expect(Object.keys(examples).sort()).toEqual(
      getToolDefinitions()
        .map((tool) => tool.name)
        .sort()
    );

    await withClient(async (client) => {
      for (const [name, args] of Object.entries(examples)) {
        const result = await client.callTool({ name, arguments: args });
        expect(result.content.length, name).toBeGreaterThan(0);
        expect("structuredContent" in result, name).toBe(true);
      }
    });
  });
});
