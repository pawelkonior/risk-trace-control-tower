import { describe, expect, it } from "vitest";
import { searchRegulations } from "./regulationSearch.js";

describe("regulation search service", () => {
  it("ranks BCBS 239 highly for RWA data lineage search", () => {
    const result = searchRegulations({
      query: "data lineage for RWA calculation",
      limit: 3,
    });

    expect(result.status).toBe("ok");
    expect(result.matches.map((match) => match.regulation.id)).toContain("BCBS239");
    expect(result.matches.findIndex((match) => match.regulation.id === "BCBS239")).toBeLessThan(3);
    expect(result.matches.find((match) => match.regulation.id === "BCBS239")?.confidence).not.toBe("low");
  });

  it("returns CRR3 and internal rule governance for rule versioning domain", () => {
    const result = searchRegulations({
      domains: ["rule_versioning"],
      include_internal_policies: true,
      limit: 10,
    });
    const ids = result.matches.map((match) => match.regulation.id);

    expect(ids).toContain("CRR3");
    expect(ids).toContain("INTERNAL_RULE_GOVERNANCE");
  });

  it("can exclude internal policies", () => {
    const result = searchRegulations({
      domains: ["rule_versioning"],
      include_internal_policies: false,
      limit: 10,
    });

    expect(result.matches.every((match) => match.regulation.jurisdiction !== "INTERNAL")).toBe(true);
    expect(result.matches.map((match) => match.regulation.id)).not.toContain("INTERNAL_RULE_GOVERNANCE");
  });
});
