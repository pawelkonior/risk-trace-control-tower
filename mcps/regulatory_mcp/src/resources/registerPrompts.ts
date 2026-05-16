import type { Server } from "@modelcontextprotocol/sdk/server/index.js";
import {
  GetPromptRequestSchema,
  ListPromptsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

interface PromptDefinition {
  name: string;
  title: string;
  description: string;
  arguments: Array<{
    name: string;
    description: string;
    required: boolean;
  }>;
  render: (args: Record<string, string>) => string;
}

const prompts: PromptDefinition[] = [
  {
    name: "feature_review",
    title: "Regulated Feature Review",
    description: "Review a regulated RWA feature before Jira or implementation output.",
    arguments: [{ name: "feature", description: "Feature description", required: true }],
    render: (args) =>
      `Use bankRegulatoryControls.review_feature_description before producing regulated output.\n\nFeature:\n${args.feature ?? ""}`,
  },
  {
    name: "architecture_review",
    title: "Regulated Architecture Review",
    description: "Review architecture text for RWA control gaps.",
    arguments: [{ name: "architecture", description: "Architecture text", required: true }],
    render: (args) =>
      `Use bankRegulatoryControls.review_architecture_text and identify blocking controls.\n\nArchitecture:\n${args.architecture ?? ""}`,
  },
  {
    name: "code_review",
    title: "Regulated Code Review",
    description: "Review code diff for hardcoded rules, traceability, validation, and logging risks.",
    arguments: [{ name: "diff", description: "Code diff", required: true }],
    render: (args) =>
      `Use bankRegulatoryControls.review_code_diff before GitHub output.\n\nDiff:\n${args.diff ?? ""}`,
  },
  {
    name: "data_lineage_design",
    title: "Data Lineage Design",
    description: "Generate RWA data lineage requirements.",
    arguments: [{ name: "context", description: "Feature or flow context", required: false }],
    render: (args) =>
      `Use bankRegulatoryControls.generate_data_lineage_requirements and map the output into Jira acceptance criteria.\n\nContext:\n${args.context ?? ""}`,
  },
  {
    name: "audit_log_design",
    title: "Audit Log Design",
    description: "Generate audit logging requirements without PII.",
    arguments: [{ name: "context", description: "Feature or flow context", required: false }],
    render: (args) =>
      `Use bankRegulatoryControls.generate_audit_log_requirements and include no-PII logging constraints.\n\nContext:\n${args.context ?? ""}`,
  },
  {
    name: "regulatory_mapping_report",
    title: "Regulatory Mapping Report",
    description: "Generate a release mapping report with controls, evidence, tests, and human review note.",
    arguments: [{ name: "feature", description: "Feature or release context", required: true }],
    render: (args) =>
      `Use bankRegulatoryControls.generate_regulatory_mapping_report and preserve the human review note.\n\nFeature:\n${args.feature ?? ""}`,
  },
];

export function listPromptDefinitions(): PromptDefinition[] {
  return prompts;
}

export function registerPrompts(server: Server): void {
  server.setRequestHandler(ListPromptsRequestSchema, async () => ({
    prompts: prompts.map((prompt) => ({
      name: prompt.name,
      title: prompt.title,
      description: prompt.description,
      arguments: prompt.arguments,
    })),
  }));

  server.setRequestHandler(GetPromptRequestSchema, async (request) => {
    const prompt = prompts.find((item) => item.name === request.params.name);
    if (!prompt) {
      throw new Error(`Unknown prompt: ${request.params.name}`);
    }
    return {
      description: prompt.description,
      messages: [
        {
          role: "user" as const,
          content: {
            type: "text" as const,
            text: prompt.render(request.params.arguments ?? {}),
          },
        },
      ],
    };
  });
}
