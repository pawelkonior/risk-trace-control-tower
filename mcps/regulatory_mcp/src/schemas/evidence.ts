import { z } from "zod";

/**
 * Type of evidence artifact.
 */
export const EvidenceTypeSchema = z.enum([
  "test_result",
  "code_review",
  "architecture_decision",
  "audit_log",
  "calculation_trace",
  "data_quality_report",
  "reconciliation_report",
  "security_scan",
  "performance_benchmark",
  "documentation",
  "approval_record",
  "change_log",
]);

export type EvidenceType = z.infer<typeof EvidenceTypeSchema>;

/**
 * Evidence artifact schema.
 */
export const EvidenceArtifactSchema = z.object({
  type: EvidenceTypeSchema,
  description: z.string(),
  location: z
    .string()
    .optional()
    .describe("File path, URL, or reference to where evidence is stored"),
  required_for_release: z
    .boolean()
    .describe("Whether this evidence must exist before release"),
  automated: z
    .boolean()
    .describe("Whether this evidence can be automatically generated"),
  retention_period: z
    .string()
    .optional()
    .describe("How long this evidence must be retained (e.g., '7 years')"),
});

export type EvidenceArtifact = z.infer<typeof EvidenceArtifactSchema>;

/**
 * Evidence requirement schema.
 */
export const EvidenceRequirementSchema = z.object({
  control_id: z.string().describe("Control ID this evidence supports"),
  artifacts: z
    .array(EvidenceArtifactSchema)
    .min(1)
    .describe("Required evidence artifacts"),
  rationale: z
    .string()
    .describe("Why this evidence is required from a regulatory perspective"),
});

export type EvidenceRequirement = z.infer<typeof EvidenceRequirementSchema>;

/**
 * Evidence validation result.
 */
export const EvidenceValidationSchema = z.object({
  control_id: z.string(),
  evidence_type: EvidenceTypeSchema,
  present: z.boolean(),
  location: z.string().optional(),
  validated_at: z.string().datetime(),
  validator: z.string().optional(),
  notes: z.string().optional(),
});

export type EvidenceValidation = z.infer<typeof EvidenceValidationSchema>;

// Made with Bob
