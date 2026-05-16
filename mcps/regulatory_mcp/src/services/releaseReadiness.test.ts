import { describe, expect, it } from "vitest";
import { generateRegulatoryMappingReport } from "./reportGenerator.js";
import { assessReleaseReadiness } from "./releaseReadiness.js";

describe("release readiness and report generator", () => {
  it("fails when RWA-RULE-001 is missing", () => {
    const result = assessReleaseReadiness({
      implemented_control_ids: ["RWA-CALC-001", "RWA-DATA-001", "RWA-AUDIT-001"],
      evidence: [],
    });

    expect(result.status).toBe("fail");
    expect(result.missing_controls).toContain("RWA-RULE-001");
    expect(result.score).toBeLessThan(100);
  });

  it("creates blocking gaps for missing evidence on blocking controls", () => {
    const result = assessReleaseReadiness({
      implemented_control_ids: [
        "RWA-RULE-001",
        "RWA-CALC-001",
        "RWA-DATA-001",
        "RWA-AUDIT-001",
        "TEST-REG-001",
        "REL-EVID-001",
      ],
      evidence: [{ id: "rule_version", type: "approval_record" }],
    });

    expect(result.status).toBe("fail");
    expect(result.gaps.some((gap) => gap.blocking)).toBe(true);
  });

  it("generates a mapping report with required sections and human review note", () => {
    const result = generateRegulatoryMappingReport({
      feature_text: "RWA CSV upload and calculation with audit evidence",
      domains: ["capital_adequacy", "audit_trail"],
    });

    expect(result.markdown).toContain("## Applicable Regulations");
    expect(result.markdown).toContain("## Required Evidence");
    expect(result.markdown).toContain("## Acceptance Criteria");
    expect(result.markdown).toContain("## Test Obligations");
    expect(result.markdown).toContain("## Bob Actions");
    expect(result.markdown).toContain("not legal advice");
  });
});
