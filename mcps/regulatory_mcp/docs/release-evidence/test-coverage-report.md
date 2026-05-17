# Test Coverage Report - RTC-37

**Date:** 2026-05-17  
**Branch:** RTC-37  
**Test Suite Version:** 1.0.0

## Executive Summary

✅ **All acceptance criteria met**  
✅ **94 tests passing**  
✅ **11 test files covering all services**  
✅ **Docker smoke test automated**

## Acceptance Criteria Verification

### ✅ AC1: npm test passes locally

```bash
$ npm test
Test Files  11 passed (11)
Tests       94 passed (94)
Duration    751ms
```

**Status:** PASSED

### ✅ AC2: Tests fail on invalid corpus

**Test:** `corpusLoader.test.ts` line 367-378

```typescript
it("should fail with CORPUS_LOAD_ERROR context when JSON cannot be parsed", () => {
  withTemporaryCorpus(
    (dataDir) => {
      writeFileSync(join(dataDir, "regulations", "BROKEN.json"), "{");
    },
    (dataDir) => {
      expect(() => loadCorpus(dataDir)).toThrow(CorpusValidationError);
      expect(() => loadCorpus(dataDir)).toThrow(/CORPUS_LOAD_ERROR/);
      expect(() => loadCorpus(dataDir)).toThrow(/BROKEN\.json/);
    }
  );
});
```

**Status:** PASSED - Invalid JSON throws `CorpusValidationError`

### ✅ AC3: Tests fail on dangling mapping IDs

**Tests:** `corpusLoader.test.ts` lines 292-365

Four comprehensive tests verify referential integrity:

1. **Keyword mapping with unknown control** (lines 292-308)
   - Creates mapping to non-existent `SEC-PRIVACY-001`
   - Expects `CorpusValidationError` with control ID in message

2. **Artifact mapping with unknown control** (lines 310-330)
   - Creates mapping to non-existent `UNKNOWN-CONTROL-001`
   - Expects `CorpusValidationError` with control ID in message

3. **Domain mapping with unknown regulation** (lines 332-348)
   - Creates mapping to non-existent `UNKNOWN_REGULATION`
   - Expects `CorpusValidationError` with regulation ID in message

4. **Control with unknown regulation reference** (lines 350-365)
   - Modifies control to reference non-existent `UNKNOWN_REGULATION`
   - Expects `CorpusValidationError` with regulation ID in message

**Status:** PASSED - All dangling references detected and rejected

### ✅ AC4: listTools() confirms 15 tools

**Test:** `registerTools.test.ts` line 44-54

```typescript
it("registers health_check plus fourteen functional tools with schemas and read-only annotations", async () => {
  await withClient(async (client) => {
    const result = await client.listTools();

    expect(result.tools).toHaveLength(15);
    expect(result.tools.map((tool) => tool.name)).toContain("health_check");
    expect(result.tools.every((tool) => tool.inputSchema)).toBe(true);
    expect(result.tools.every((tool) => tool.outputSchema)).toBe(true);
    expect(result.tools.every((tool) => tool.annotations?.readOnlyHint)).toBe(true);
    expect(result.tools.every((tool) => tool.annotations?.destructiveHint === false)).toBe(true);
  });
});
```

**Status:** PASSED - Exactly 15 tools registered with complete schemas and annotations

### ✅ AC5: Representative call for every tool returns disclaimer and human review flag

**Test:** `registerTools.test.ts` lines 57-97

```typescript
it("supports a representative call for every registered tool", async () => {
  const examples: Record<string, Record<string, unknown>> = {
    health_check: { include_corpus: true },
    get_regulatory_profile: { domains: ["capital_adequacy"] },
    search_regulations: { query: "data lineage for RWA calculation", limit: 3 },
    match_controls: { text: "CSV upload for RWA calculation", artifact_type: "feature" },
    review_feature_description: {
      description: "CSV upload for exposures and RWA calculation.",
    },
    review_architecture_text: {
      architecture_text: "Architecture hardcoded risk weight values inside the service.",
    },
    review_code_diff: {
      diff: "+ const riskWeight = 0.35;\n+ logger.info(customer.email);\n+ return amount * riskWeight;",
    },
    generate_acceptance_criteria: { control_ids: ["RWA-DATA-001"] },
    generate_data_lineage_requirements: {},
    generate_audit_log_requirements: {},
    generate_test_obligations: { control_ids: ["TEST-REG-001"] },
    assess_release_readiness: { implemented_control_ids: ["RWA-CALC-001"], evidence: [] },
    generate_regulatory_mapping_report: {
      feature_text: "RWA CSV upload and calculation",
    },
    generate_rwa_run_evidence_requirements: {},
    explain_control: { control_id: "RWA-RULE-001" },
  };

  expect(Object.keys(examples).sort()).toEqual(
    getToolDefinitions()
      .map((tool) => tool.name)
      .sort()
  );

  await withClient(async (client) => {
    for (const [name, args] of Object.entries(examples)) {
      const result = await client.callTool({ name, arguments: args });
      expect(result.content.length, name).toBeGreaterThan(0);
      expectHumanReviewMetadata(structuredContent(result, name), name);
    }
  });
});
```

Helper function validates metadata:

```typescript
function expectHumanReviewMetadata(
  content: Record<string, unknown>,
  name: string
): void {
  const metadata = content.metadata as Record<string, unknown> | undefined;
  expect(metadata, `${name} metadata`).toBeDefined();
  expect(metadata?.disclaimer, `${name} disclaimer`).toEqual(
    expect.stringContaining("engineering control mapping")
  );
  expect(metadata?.requires_human_review, `${name} human review flag`).toBe(true);
}
```

**Status:** PASSED - All 15 tools return disclaimer and `requires_human_review: true`

### ✅ AC6: Docker smoke is documented or automated

**Automated Script:** `test-docker-smoke.sh`

The script validates:
- ✓ Docker image builds successfully
- ✓ Container starts and runs
- ✓ Corpus loads (≥9 regulations, ≥15 controls)
- ✓ MCP server starts without errors
- ✓ Container stops cleanly

**Documentation:** `README.md` lines 298-330

Includes:
- Usage instructions
- Requirements
- Validation checklist
- Exit codes

**Status:** PASSED - Fully automated with comprehensive documentation

## Test Coverage by Category

### Corpus Loader (25 tests)
- ✅ Happy path loading
- ✅ Duplicate ID detection (regulations and controls)
- ✅ Schema validation (all regulations and controls)
- ✅ Referential integrity (4 dangling reference tests)
- ✅ Invalid JSON handling
- ✅ Deterministic ordering
- ✅ Expected corpus content verification

### Corpus Store (32 tests)
- ✅ Caching and reset
- ✅ Query methods (by ID, keyword, artifact type, domain, severity, jurisdiction)
- ✅ Search functionality
- ✅ Statistics

### Control Matcher (3 tests)
- ✅ Risk weight calculation matching
- ✅ CSV upload control matching
- ✅ Deterministic sorting

### Regulation Search (3 tests)
- ✅ BCBS 239 lineage ranking
- ✅ Domain filtering
- ✅ Internal policy filtering

### Review Services (3 tests)
- ✅ Weak feature detection
- ✅ Hardcoded architecture detection
- ✅ Hardcoded code diff detection (risk weights, PII logging, traceability)

### Generation Services (6 tests)
- ✅ Acceptance criteria deduplication
- ✅ Lineage field generation
- ✅ Audit event generation
- ✅ Test obligation generation
- ✅ RWA run evidence package
- ✅ Control explanation

### Release Readiness (3 tests)
- ✅ Missing control detection
- ✅ Blocking gap creation
- ✅ Mapping report generation with human review note

### MCP Tools (2 tests)
- ✅ 15 tools with schemas and annotations
- ✅ Representative calls with disclaimer and human review flag

### Resources (2 tests)
- ✅ Resource registration
- ✅ Resource retrieval

### Schemas (13 tests)
- ✅ Regulation schema validation
- ✅ Control schema validation
- ✅ Evidence schema validation
- ✅ Finding schema validation

### Configuration (2 tests)
- ✅ Default configuration
- ✅ Custom data directory

## Evidence Artifacts

### Build Log
```bash
$ npm run build
> @risk-trace/regulatory-mcp@0.1.0 build
> tsc

[Build completed successfully with no errors]
```

### Test Log
```bash
$ npm test
> @risk-trace/regulatory-mcp@0.1.0 test
> vitest run

 ✓ src/config.test.ts (2 tests) 4ms
 ✓ src/schemas/schemas.test.ts (13 tests) 29ms
 ✓ src/services/regulationSearch.test.ts (3 tests) 41ms
 ✓ src/services/releaseReadiness.test.ts (3 tests) 31ms
 ✓ src/services/controlMatcher.test.ts (3 tests) 45ms
 ✓ src/services/generationServices.test.ts (6 tests) 46ms
 ✓ src/services/reviewServices.test.ts (3 tests) 58ms
 ✓ src/services/corpusStore.test.ts (32 tests) 169ms
 ✓ src/services/corpusLoader.test.ts (25 tests) 225ms
 ✓ src/resources/registerResources.test.ts (2 tests) 36ms
 ✓ src/tools/registerTools.test.ts (2 tests) 73ms

Test Files  11 passed (11)
Tests       94 passed (94)
Duration    751ms
```

### MCP In-Memory Test Output
All 15 tools verified with in-memory MCP client:
- health_check
- get_regulatory_profile
- search_regulations
- match_controls
- review_feature_description
- review_architecture_text
- review_code_diff
- generate_acceptance_criteria
- generate_data_lineage_requirements
- generate_audit_log_requirements
- generate_test_obligations
- assess_release_readiness
- generate_regulatory_mapping_report
- generate_rwa_run_evidence_requirements
- explain_control

Each tool call verified:
- ✅ Returns content
- ✅ Includes disclaimer containing "engineering control mapping"
- ✅ Sets `requires_human_review: true`

## Controls Satisfied

### TEST-REG-001: Regulatory Test Coverage
- ✅ 94 tests covering all services
- ✅ Corpus validation tests
- ✅ MCP contract tests
- ✅ Referential integrity tests

### REL-EVID-001: Release Evidence Collection
- ✅ Build log captured
- ✅ Test log captured
- ✅ MCP tool inventory documented
- ✅ Docker smoke test automated

## Conclusion

All acceptance criteria for RTC-37 are **SATISFIED**:

1. ✅ npm test passes locally (94/94 tests)
2. ✅ Tests fail on invalid corpus (CorpusValidationError)
3. ✅ Tests fail on dangling mapping IDs (4 comprehensive tests)
4. ✅ listTools() confirms 15 tools (exact count verified)
5. ✅ Representative call for every tool returns disclaimer and human review flag
6. ✅ Docker smoke is documented and automated

**Quality Gate:** PASSED

---

*This is an engineering control mapping report. It is not legal advice and requires qualified compliance, legal, or risk review before production use.*