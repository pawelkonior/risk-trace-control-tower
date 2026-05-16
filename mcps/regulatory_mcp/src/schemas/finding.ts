import { z } from "zod";
import { SeveritySchema, ConfidenceSchema, CommonMetadataSchema } from "./common.js";
import { EvidenceTypeSchema } from "./evidence.js";

/**
 * Impact area for a finding.
 */
export const ImpactAreaSchema = z.enum([
  "regulatory_compliance",
  "data_quality",
  "audit_trail",
  "calculation_accuracy",
  "security",
  "performance",
  "maintainability",
  "testability",
]);

export type ImpactArea = z.infer<typeof ImpactAreaSchema>;

/**
 * Finding status.
 */
export const FindingStatusSchema = z.enum([
  "open",
  "in_progress",
  "resolved",
  "accepted_risk",
  "false_positive",
]);

export type FindingStatus = z.infer<typeof FindingStatusSchema>;

/**
 * Matched control reference.
 */
export const MatchedControlSchema = z.object({
  control_id: z.string(),
  relevance: z.enum(["direct", "indirect", "related"]),
  rationale: z.string(),
});

export type MatchedControl = z.infer<typeof MatchedControlSchema>;

/**
 * Required evidence for addressing a finding.
 */
export const RequiredEvidenceSchema = z.object({
  evidence_type: EvidenceTypeSchema,
  description: z.string(),
  priority: z.enum(["required", "recommended", "optional"]),
});

export type RequiredEvidence = z.infer<typeof RequiredEvidenceSchema>;

/**
 * Recommendation for addressing a finding.
 */
export const RecommendationSchema = z.object({
  priority: z.enum(["immediate", "high", "medium", "low"]),
  action: z.string(),
  rationale: z.string(),
  estimated_effort: z
    .string()
    .optional()
    .describe("Estimated effort (e.g., '2 hours', '1 day', '1 week')"),
  blocking_release: z.boolean(),
});

export type Recommendation = z.infer<typeof RecommendationSchema>;

/**
 * Complete finding schema.
 */
export const FindingSchema = z.object({
  id: z.string().describe("Unique finding identifier"),
  title: z.string(),
  description: z.string(),
  severity: SeveritySchema,
  confidence: ConfidenceSchema,
  status: FindingStatusSchema,
  impact_areas: z
    .array(ImpactAreaSchema)
    .min(1)
    .describe("Areas impacted by this finding"),
  impact_description: z
    .string()
    .describe("Detailed description of the regulatory impact"),
  matched_controls: z
    .array(MatchedControlSchema)
    .min(1)
    .describe("Controls that are relevant to this finding"),
  required_evidence: z
    .array(RequiredEvidenceSchema)
    .min(1)
    .describe("Evidence required to address this finding"),
  recommendations: z
    .array(RecommendationSchema)
    .min(1)
    .describe("Recommended actions to address this finding"),
  location: z
    .object({
      file_path: z.string().optional(),
      line_start: z.number().optional(),
      line_end: z.number().optional(),
      artifact_type: z.string().optional(),
    })
    .optional()
    .describe("Location in code or artifact where finding was detected"),
  detected_at: z.string().datetime(),
  detected_by: z.string().describe("Tool or process that detected this finding"),
  requires_human_review: z.boolean(),
});

export type Finding = z.infer<typeof FindingSchema>;

/**
 * Response schema for finding queries.
 */
export const FindingResponseSchema = z.object({
  metadata: CommonMetadataSchema,
  findings: z.array(FindingSchema),
  summary: z.object({
    total_findings: z.number(),
    by_severity: z.record(z.number()),
    blocking_release: z.number(),
    requires_human_review: z.number(),
  }),
});

export type FindingResponse = z.infer<typeof FindingResponseSchema>;

// Made with Bob
