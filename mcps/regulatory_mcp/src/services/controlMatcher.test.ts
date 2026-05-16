import { describe, expect, it } from "vitest";
import { matchControls } from "./controlMatcher.js";

describe("control matching service", () => {
  it("returns rule and calculation controls for risk weight calculation text", () => {
    const result = matchControls({
      text: "Implement risk weight calculation for RWA exposure classes.",
    });
    const ids = result.applicable_controls.map((match) => match.control.id);

    expect(ids).toContain("RWA-RULE-001");
    expect(ids).toContain("RWA-CALC-001");
    expect(result.source_references.length).toBeGreaterThan(0);
    expect(result.required_evidence.length).toBeGreaterThan(0);
  });

  it("returns lineage, data quality, audit, and secure input controls for CSV upload", () => {
    const result = matchControls({
      text: "CSV upload for exposures before RWA calculation",
      artifact_type: "feature",
    });
    const ids = result.applicable_controls.map((match) => match.control.id);

    expect(ids).toContain("RWA-DATA-001");
    expect(ids).toContain("RWA-DQ-001");
    expect(ids).toContain("RWA-AUDIT-001");
    expect(ids).toContain("SEC-INPUT-001");
  });

  it("sorts deterministically by score, severity, and id", () => {
    const result = matchControls({
      text: "security logging pii audit",
      explicit_control_ids: ["SEC-LOG-001", "RWA-AUDIT-001"],
    });
    const scores = result.applicable_controls.map((match) => match.score);

    expect(scores).toEqual([...scores].sort((a, b) => b - a));
  });
});
