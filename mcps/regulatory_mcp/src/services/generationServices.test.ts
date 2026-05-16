import { describe, expect, it } from "vitest";
import {
  explainControl,
  generateAcceptanceCriteria,
  generateAuditLogRequirements,
  generateDataLineageRequirements,
  generateRwaRunEvidenceRequirements,
  generateTestObligations,
} from "./generationServices.js";

describe("generation services", () => {
  it("deduplicates acceptance criteria and maps them to controls", () => {
    const result = generateAcceptanceCriteria({
      control_ids: ["RWA-DATA-001", "RWA-DATA-001", "RWA-AUDIT-001"],
    });
    const descriptions = result.criteria.map((criterion) => criterion.description);

    expect(new Set(descriptions).size).toBe(descriptions.length);
    expect(result.criteria.every((criterion) => criterion.control_id)).toBe(true);
  });

  it("generates required lineage fields", () => {
    const result = generateDataLineageRequirements();

    expect(result.required_fields).toEqual([
      "source_system",
      "source_record_id",
      "input_snapshot_id",
      "input_hash",
      "rule_version",
      "calculation_trace_id",
      "reporting_date",
    ]);
  });

  it("generates upload, validate, calculate, and export audit events", () => {
    const result = generateAuditLogRequirements();

    expect(result.required_events.map((event) => event.event)).toEqual([
      "upload",
      "validate",
      "calculate",
      "export",
    ]);
    expect(result.required_events.every((event) => event.fields.includes("event_id"))).toBe(true);
    expect(result.security_notes.join(" ")).toContain("PII");
  });

  it("generates Given/When/Then test obligations", () => {
    const result = generateTestObligations({
      control_ids: ["TEST-REG-001"],
    });

    expect(result.obligations.length).toBeGreaterThan(0);
    expect(result.obligations[0].given).toContain("Given");
    expect(result.obligations[0].when).toContain("When");
    expect(result.obligations[0].then).toContain("Then");
  });

  it("generates RWA run evidence package", () => {
    const result = generateRwaRunEvidenceRequirements();
    const ids = result.evidence_package.map((artifact) => artifact.id);

    expect(ids).toEqual([
      "input_snapshot",
      "validation_report",
      "applied_rules",
      "rule_version",
      "results",
      "lineage_report",
      "audit_extract",
      "reconciliation_summary",
    ]);
  });

  it("explains developer tasks and common mistakes for a control", () => {
    const result = explainControl("RWA-RULE-001");

    expect(result.developer_tasks.length).toBeGreaterThan(0);
    expect(result.common_mistakes.length).toBeGreaterThan(0);
  });
});
