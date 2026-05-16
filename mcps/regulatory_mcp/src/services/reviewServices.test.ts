import { describe, expect, it } from "vitest";
import {
  reviewArchitectureText,
  reviewCodeDiff,
  reviewFeatureDescription,
} from "./reviewServices.js";

describe("review services", () => {
  it("marks CSV upload and RWA calculation feature without core controls as not ready", () => {
    const result = reviewFeatureDescription({
      description: "Build CSV upload for exposure data and RWA calculation.",
    });

    expect(result.readiness_status).toBe("not_ready");
    expect(result.findings.map((finding) => finding.id)).toContain("FEATURE-LINEAGE-001");
    expect(result.findings.map((finding) => finding.id)).toContain("FEATURE-RULE-001");
    expect(result.findings.map((finding) => finding.id)).toContain("FEATURE-AUDIT-001");
  });

  it("flags architecture with hardcoded risk weights as critical", () => {
    const result = reviewArchitectureText({
      architecture_text: "The RWA service uses hardcoded risk weight values in a calculator module.",
    });

    expect(result.findings.some((finding) => finding.severity === "critical")).toBe(true);
    expect(result.findings.map((finding) => finding.id)).toContain("ARCH-HARDCODED-RULE-001");
  });

  it("detects numeric risk weights, missing traceability fields, and PII-like logging", () => {
    const result = reviewCodeDiff({
      file_path: "calculator.ts",
      diff: `
+ const riskWeight = 0.35;
+ logger.info(customer.email);
+ export function calculateRwa(exposure) {
+   return exposure.amount * riskWeight;
+ }
`,
    });
    const ids = result.findings.map((finding) => finding.id);

    expect(ids).toContain("CODE-HARDCODED-RISK-WEIGHT-001");
    expect(ids).toContain("CODE-TRACEABILITY-FIELDS-001");
    expect(ids).toContain("CODE-PII-LOGGING-001");
  });
});
