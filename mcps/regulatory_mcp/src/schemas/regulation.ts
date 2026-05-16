import { z } from "zod";
import {
  CommonMetadataSchema,
  RegulatoryDomainSchema,
  StatusSchema,
} from "./common.js";

/**
 * Type of regulatory document.
 */
export const RegulationTypeSchema = z.enum([
  "directive",
  "regulation",
  "standard",
  "guideline",
  "policy",
  "framework",
  "technical_standard",
]);

export type RegulationType = z.infer<typeof RegulationTypeSchema>;

/**
 * Entity types that a regulation applies to.
 */
export const AppliesToSchema = z.enum([
  "credit_institution",
  "investment_firm",
  "financial_institution",
  "insurance_company",
  "all_financial_entities",
  "internal_policy",
]);

export type AppliesTo = z.infer<typeof AppliesToSchema>;

/**
 * Source reference for a regulation.
 */
export const SourceReferenceSchema = z.object({
  type: z.enum(["official_text", "guidance", "technical_standard", "internal"]),
  url: z.string().url().optional(),
  citation: z.string(),
  accessed_date: z.string().datetime().optional(),
});

export type SourceReference = z.infer<typeof SourceReferenceSchema>;

/**
 * Key requirement within a regulation.
 */
export const KeyRequirementSchema = z.object({
  id: z.string().describe("Unique identifier for this requirement"),
  article: z.string().optional().describe("Article or section reference"),
  title: z.string(),
  description: z.string(),
  mandatory: z.boolean(),
  deadline: z.string().datetime().optional(),
});

export type KeyRequirement = z.infer<typeof KeyRequirementSchema>;

/**
 * Engineering implications of a regulation.
 */
export const EngineeringImplicationSchema = z.object({
  area: z.enum([
    "data_model",
    "calculation_engine",
    "data_quality",
    "audit_logging",
    "reporting",
    "testing",
    "security",
    "performance",
    "architecture",
  ]),
  description: z.string(),
  priority: z.enum(["critical", "high", "medium", "low"]),
});

export type EngineeringImplication = z.infer<
  typeof EngineeringImplicationSchema
>;

/**
 * Complete regulation schema.
 */
export const RegulationSchema = z.object({
  id: z
    .string()
    .regex(/^[A-Z0-9_-]+$/)
    .describe("Unique regulation identifier (e.g., CRR3, DORA, BCBS239)"),
  title: z.string(),
  type: RegulationTypeSchema,
  jurisdiction: z.string().describe("Primary jurisdiction (e.g., EU, UK, CH, GLOBAL)"),
  status: StatusSchema,
  as_of: z.string().datetime().describe("Effective date or last update date"),
  applies_to: z
    .array(AppliesToSchema)
    .min(1)
    .describe("Entity types this regulation applies to"),
  domains: z
    .array(RegulatoryDomainSchema)
    .min(1)
    .describe("Regulatory domains covered"),
  summary: z.string().describe("Brief summary of the regulation"),
  key_requirements: z
    .array(KeyRequirementSchema)
    .min(1)
    .describe("Key requirements from this regulation"),
  engineering_implications: z
    .array(EngineeringImplicationSchema)
    .min(1)
    .describe("Engineering implications for implementation"),
  source_references: z
    .array(SourceReferenceSchema)
    .min(1)
    .describe("Official sources and references"),
  requires_human_review: z
    .boolean()
    .describe("Whether this regulation requires human expert review"),
});

export type Regulation = z.infer<typeof RegulationSchema>;

/**
 * Response schema for regulation queries.
 */
export const RegulationResponseSchema = z.object({
  metadata: CommonMetadataSchema,
  regulations: z.array(RegulationSchema),
});

export type RegulationResponse = z.infer<typeof RegulationResponseSchema>;

// Made with Bob
