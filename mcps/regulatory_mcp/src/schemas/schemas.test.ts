import { describe, it, expect } from "vitest";
import {
  CommonMetadataSchema,
  SeveritySchema,
  RegulatoryDomainSchema,
} from "./common.js";
import { RegulationSchema } from "./regulation.js";
import { ControlSchema } from "./control.js";
import { FindingSchema } from "./finding.js";
import { EvidenceArtifactSchema } from "./evidence.js";

describe("Schema Validation", () => {
  describe("CommonMetadataSchema", () => {
    it("should validate valid metadata", () => {
      const valid = {
        disclaimer: "This is engineering control mapping only",
        as_of: "2025-01-15T00:00:00.000Z",
        jurisdiction: "EU",
        confidence: "high",
        requires_human_review: true,
      };
      expect(() => CommonMetadataSchema.parse(valid)).not.toThrow();
    });

    it("should reject invalid confidence level", () => {
      const invalid = {
        disclaimer: "Test",
        as_of: "2025-01-15T00:00:00.000Z",
        jurisdiction: "EU",
        confidence: "invalid",
        requires_human_review: true,
      };
      expect(() => CommonMetadataSchema.parse(invalid)).toThrow();
    });

    it("should reject invalid datetime", () => {
      const invalid = {
        disclaimer: "Test",
        as_of: "not-a-date",
        jurisdiction: "EU",
        confidence: "high",
        requires_human_review: true,
      };
      expect(() => CommonMetadataSchema.parse(invalid)).toThrow();
    });
  });

  describe("SeveritySchema", () => {
    it("should accept valid severity levels", () => {
      expect(() => SeveritySchema.parse("critical")).not.toThrow();
      expect(() => SeveritySchema.parse("high")).not.toThrow();
      expect(() => SeveritySchema.parse("medium")).not.toThrow();
      expect(() => SeveritySchema.parse("low")).not.toThrow();
      expect(() => SeveritySchema.parse("info")).not.toThrow();
    });

    it("should reject invalid severity", () => {
      expect(() => SeveritySchema.parse("invalid")).toThrow();
    });
  });

  describe("RegulationSchema", () => {
    it("should validate valid regulation", () => {
      const valid = {
        id: "TEST_REG",
        title: "Test Regulation",
        type: "regulation",
        jurisdiction: "EU",
        status: "active",
        as_of: "2025-01-15T00:00:00.000Z",
        applies_to: ["credit_institution"],
        domains: ["capital_adequacy"],
        summary: "Test summary",
        key_requirements: [
          {
            id: "REQ-1",
            title: "Test requirement",
            description: "Test description",
            mandatory: true,
          },
        ],
        engineering_implications: [
          {
            area: "calculation_engine",
            description: "Test implication",
            priority: "high",
          },
        ],
        source_references: [
          {
            type: "official_text",
            citation: "Test citation",
          },
        ],
        requires_human_review: true,
      };
      expect(() => RegulationSchema.parse(valid)).not.toThrow();
    });

    it("should reject regulation with invalid ID format", () => {
      const invalid = {
        id: "invalid id with spaces",
        title: "Test",
        type: "regulation",
        jurisdiction: "EU",
        status: "active",
        as_of: "2025-01-15T00:00:00.000Z",
        applies_to: ["credit_institution"],
        domains: ["capital_adequacy"],
        summary: "Test",
        key_requirements: [
          {
            id: "REQ-1",
            title: "Test",
            description: "Test",
            mandatory: true,
          },
        ],
        engineering_implications: [
          {
            area: "calculation_engine",
            description: "Test",
            priority: "high",
          },
        ],
        source_references: [{ type: "official_text", citation: "Test" }],
        requires_human_review: true,
      };
      expect(() => RegulationSchema.parse(invalid)).toThrow();
    });

    it("should require at least one key requirement", () => {
      const invalid = {
        id: "TEST_REG",
        title: "Test",
        type: "regulation",
        jurisdiction: "EU",
        status: "active",
        as_of: "2025-01-15T00:00:00.000Z",
        applies_to: ["credit_institution"],
        domains: ["capital_adequacy"],
        summary: "Test",
        key_requirements: [],
        engineering_implications: [
          {
            area: "calculation_engine",
            description: "Test",
            priority: "high",
          },
        ],
        source_references: [{ type: "official_text", citation: "Test" }],
        requires_human_review: true,
      };
      expect(() => RegulationSchema.parse(invalid)).toThrow();
    });
  });

  describe("ControlSchema", () => {
    it("should validate valid control", () => {
      const valid = {
        id: "TEST-CTRL-001",
        title: "Test Control",
        description: "Test description",
        severity: "high",
        domains: ["testing"],
        regulatory_basis: [
          {
            regulation_id: "TEST_REG",
            rationale: "Test rationale",
          },
        ],
        required_evidence: [
          {
            type: "test_result",
            description: "Test evidence",
            required_for_release: true,
            automated: true,
          },
        ],
        acceptance_criteria: [
          {
            id: "AC-1",
            description: "Test criterion",
            verification_method: "automated_test",
          },
        ],
        test_obligations: [
          {
            id: "TO-1",
            description: "Test obligation",
            test_type: "unit_test",
            frequency: "per_commit",
            automated: true,
            blocking: true,
          },
        ],
        implementation_hints: [],
        anti_patterns: [],
        bob_actions: [],
        tags: ["test"],
        created_at: "2025-01-15T00:00:00.000Z",
        updated_at: "2025-01-15T00:00:00.000Z",
      };
      expect(() => ControlSchema.parse(valid)).not.toThrow();
    });

    it("should reject control with invalid ID format", () => {
      const invalid = {
        id: "INVALID_FORMAT",
        title: "Test",
        description: "Test",
        severity: "high",
        domains: ["testing"],
        regulatory_basis: [
          { regulation_id: "TEST", rationale: "Test" },
        ],
        required_evidence: [
          {
            type: "test_result",
            description: "Test",
            required_for_release: true,
            automated: true,
          },
        ],
        acceptance_criteria: [
          {
            id: "AC-1",
            description: "Test",
            verification_method: "automated_test",
          },
        ],
        test_obligations: [
          {
            id: "TO-1",
            description: "Test",
            test_type: "unit_test",
            frequency: "per_commit",
            automated: true,
            blocking: true,
          },
        ],
        implementation_hints: [],
        anti_patterns: [],
        bob_actions: [],
        tags: [],
        created_at: "2025-01-15T00:00:00.000Z",
        updated_at: "2025-01-15T00:00:00.000Z",
      };
      expect(() => ControlSchema.parse(invalid)).toThrow();
    });

    it("should require at least one acceptance criterion", () => {
      const invalid = {
        id: "TEST-CTRL-001",
        title: "Test",
        description: "Test",
        severity: "high",
        domains: ["testing"],
        regulatory_basis: [
          { regulation_id: "TEST", rationale: "Test" },
        ],
        required_evidence: [
          {
            type: "test_result",
            description: "Test",
            required_for_release: true,
            automated: true,
          },
        ],
        acceptance_criteria: [],
        test_obligations: [
          {
            id: "TO-1",
            description: "Test",
            test_type: "unit_test",
            frequency: "per_commit",
            automated: true,
            blocking: true,
          },
        ],
        implementation_hints: [],
        anti_patterns: [],
        bob_actions: [],
        tags: [],
        created_at: "2025-01-15T00:00:00.000Z",
        updated_at: "2025-01-15T00:00:00.000Z",
      };
      expect(() => ControlSchema.parse(invalid)).toThrow();
    });
  });

  describe("FindingSchema", () => {
    it("should validate valid finding", () => {
      const valid = {
        id: "FIND-001",
        title: "Test Finding",
        description: "Test description",
        severity: "high",
        confidence: "medium",
        status: "open",
        impact_areas: ["regulatory_compliance"],
        impact_description: "Test impact",
        matched_controls: [
          {
            control_id: "TEST-CTRL-001",
            relevance: "direct",
            rationale: "Test rationale",
          },
        ],
        required_evidence: [
          {
            evidence_type: "test_result",
            description: "Test evidence",
            priority: "required",
          },
        ],
        recommendations: [
          {
            priority: "high",
            action: "Test action",
            rationale: "Test rationale",
            blocking_release: false,
          },
        ],
        detected_at: "2025-01-15T00:00:00.000Z",
        detected_by: "test-tool",
        requires_human_review: true,
      };
      expect(() => FindingSchema.parse(valid)).not.toThrow();
    });
  });

  describe("EvidenceArtifactSchema", () => {
    it("should validate valid evidence artifact", () => {
      const valid = {
        type: "test_result",
        description: "Test evidence",
        required_for_release: true,
        automated: true,
      };
      expect(() => EvidenceArtifactSchema.parse(valid)).not.toThrow();
    });
  });
});

// Made with Bob
