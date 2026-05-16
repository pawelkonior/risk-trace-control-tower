import { z } from "zod";

/**
 * Common metadata schema for all regulatory responses.
 * Ensures every output includes disclaimer, timestamp, jurisdiction, confidence, and human review flag.
 */
export const CommonMetadataSchema = z.object({
  disclaimer: z
    .string()
    .describe(
      "Legal disclaimer stating this is engineering control mapping only, not legal advice"
    ),
  as_of: z
    .string()
    .datetime()
    .describe("ISO 8601 timestamp when this data was generated or last validated"),
  jurisdiction: z
    .string()
    .describe("Regulatory jurisdiction (e.g., EU, UK, CH, US, GLOBAL)"),
  confidence: z
    .enum(["high", "medium", "low"])
    .describe("Confidence level in the mapping or analysis"),
  requires_human_review: z
    .boolean()
    .describe("Flag indicating whether human expert review is required"),
});

export type CommonMetadata = z.infer<typeof CommonMetadataSchema>;

/**
 * Standard disclaimer text for all regulatory outputs.
 */
export const STANDARD_DISCLAIMER =
  "This is an engineering control mapping tool only. It does not provide legal advice or compliance opinions. All regulatory interpretations must be validated by qualified legal and compliance professionals.";

/**
 * Severity levels for findings and controls.
 */
export const SeveritySchema = z.enum([
  "critical",
  "high",
  "medium",
  "low",
  "info",
]);

export type Severity = z.infer<typeof SeveritySchema>;

/**
 * Confidence level for mappings and analysis.
 */
export const ConfidenceSchema = z.enum(["high", "medium", "low"]);

export type Confidence = z.infer<typeof ConfidenceSchema>;

/**
 * Regulatory domains for categorization.
 */
export const RegulatoryDomainSchema = z.enum([
  "capital_adequacy",
  "credit_risk",
  "market_risk",
  "operational_risk",
  "liquidity_risk",
  "data_quality",
  "reporting",
  "audit_trail",
  "ict_security",
  "data_protection",
  "governance",
  "testing",
  "architecture",
  "performance",
]);

export type RegulatoryDomain = z.infer<typeof RegulatoryDomainSchema>;

/**
 * Status for regulations and controls.
 */
export const StatusSchema = z.enum([
  "active",
  "draft",
  "proposed",
  "superseded",
  "archived",
]);

export type Status = z.infer<typeof StatusSchema>;

// Made with Bob
