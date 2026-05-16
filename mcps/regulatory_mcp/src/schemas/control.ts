import { z } from "zod";
import { SeveritySchema, RegulatoryDomainSchema } from "./common.js";
import { EvidenceArtifactSchema } from "./evidence.js";

/**
 * Acceptance criterion for a control.
 */
export const AcceptanceCriterionSchema = z.object({
  id: z.string().describe("Unique identifier for this criterion"),
  description: z.string(),
  verification_method: z.enum([
    "automated_test",
    "code_review",
    "manual_inspection",
    "audit_review",
    "calculation_verification",
    "security_test",
  ]),
  pass_threshold: z.string().optional().describe("Quantitative threshold if applicable"),
});

export type AcceptanceCriterion = z.infer<typeof AcceptanceCriterionSchema>;

/**
 * Test obligation for a control.
 */
export const TestObligationSchema = z.object({
  id: z.string().describe("Unique identifier for this test obligation"),
  description: z.string(),
  test_type: z.enum([
    "unit_test",
    "integration_test",
    "regression_test",
    "performance_test",
    "security_test",
    "audit_test",
  ]),
  frequency: z.enum(["per_commit", "per_release", "monthly", "quarterly", "annually"]),
  automated: z.boolean(),
  blocking: z
    .boolean()
    .describe("Whether failure blocks release or deployment"),
});

export type TestObligation = z.infer<typeof TestObligationSchema>;

/**
 * Implementation hint for a control.
 */
export const ImplementationHintSchema = z.object({
  category: z.enum([
    "architecture",
    "code_pattern",
    "library",
    "tool",
    "process",
    "documentation",
  ]),
  description: z.string(),
  example: z.string().optional(),
});

export type ImplementationHint = z.infer<typeof ImplementationHintSchema>;

/**
 * Anti-pattern to avoid.
 */
export const AntiPatternSchema = z.object({
  description: z.string(),
  risk: z.string().describe("Why this is problematic from a regulatory perspective"),
  alternative: z.string().describe("What to do instead"),
});

export type AntiPattern = z.infer<typeof AntiPatternSchema>;

/**
 * Bob action that can be triggered by this control.
 */
export const BobActionSchema = z.object({
  action_type: z.enum([
    "block_merge",
    "require_review",
    "generate_evidence",
    "run_test",
    "create_ticket",
    "notify_compliance",
  ]),
  trigger_condition: z.string().describe("When this action should be triggered"),
  description: z.string(),
  automated: z.boolean(),
});

export type BobAction = z.infer<typeof BobActionSchema>;

/**
 * Regulatory basis for a control.
 */
export const RegulatoryBasisSchema = z.object({
  regulation_id: z.string().describe("ID of the regulation this control implements"),
  article: z.string().optional().describe("Specific article or section reference"),
  requirement_id: z.string().optional().describe("Specific requirement ID if applicable"),
  rationale: z.string().describe("How this control addresses the regulatory requirement"),
});

export type RegulatoryBasis = z.infer<typeof RegulatoryBasisSchema>;

/**
 * Complete engineering control schema.
 */
export const ControlSchema = z.object({
  id: z
    .string()
    .regex(/^[A-Z]+-[A-Z]+-\d{3}$/)
    .describe("Unique control identifier (e.g., RWA-CALC-001, SEC-INPUT-001)"),
  title: z.string(),
  description: z.string(),
  severity: SeveritySchema,
  domains: z
    .array(RegulatoryDomainSchema)
    .min(1)
    .describe("Regulatory domains this control addresses"),
  regulatory_basis: z
    .array(RegulatoryBasisSchema)
    .min(1)
    .describe("Regulatory requirements this control implements"),
  required_evidence: z
    .array(EvidenceArtifactSchema)
    .min(1)
    .describe("Evidence artifacts required to demonstrate compliance"),
  acceptance_criteria: z
    .array(AcceptanceCriterionSchema)
    .min(1)
    .describe("Criteria to verify control effectiveness"),
  test_obligations: z
    .array(TestObligationSchema)
    .min(1)
    .describe("Testing requirements for this control"),
  implementation_hints: z
    .array(ImplementationHintSchema)
    .describe("Guidance for implementing this control"),
  anti_patterns: z
    .array(AntiPatternSchema)
    .describe("Common mistakes to avoid"),
  bob_actions: z
    .array(BobActionSchema)
    .describe("Actions Bob can take related to this control"),
  tags: z.array(z.string()).describe("Additional tags for categorization"),
  created_at: z.string().datetime(),
  updated_at: z.string().datetime(),
});

export type Control = z.infer<typeof ControlSchema>;

/**
 * Response schema for control queries.
 */
export const ControlResponseSchema = z.object({
  controls: z.array(ControlSchema),
  total_count: z.number(),
  filtered_count: z.number(),
});

export type ControlResponse = z.infer<typeof ControlResponseSchema>;

// Made with Bob
