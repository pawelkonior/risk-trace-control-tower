# RCT-16 Technical Analysis

**Task:** Implement compact parallel LangGraph RWA analysis runtime with deterministic tools  
**Story:** Optimized guarded multi-agent RWA executive commentary workflow  
**Epic:** RWA Executive Commentary Control Tower  
**Updated:** 2026-05-17

## Implementation Summary

RCT-16 is implemented in `apps/backend/src/rwa_agents/` as a compact LangGraph workflow
with deterministic worker tools and structured fan-in.

The implemented runtime is:

```text
AgentStateBuilt
  -> AnalysisPhase
       -> DataAnalystAgent
       -> RiskExpertAgent
  -> AnalysisFanIn
  -> SupervisorAgent
  -> FinalOutputGuard
  -> FinalStructuredResponse
```

`DataAnalystAgent` and `RiskExpertAgent` are graph fan-out branches after
`AnalysisPhase`. They write separate worker result fields and LangGraph joins them at
`AnalysisFanIn`, where structured findings, validation flags, quantitative validations,
and recommended actions are merged.

## Key Delivery Points

- `workflow.py` now builds a real `StateGraph` with the required compact nodes.
- `MemorySaver`/`InMemorySaver` checkpointing is configured through the workflow compile step.
- Worker ReAct behavior remains internal to deterministic Python tools and is exposed through
  structured `react_steps`.
- `analyze_data_quality` detects duplicate asset IDs, missing outputs, missing risk parameters,
  non-positive exposures, missing ratings, invalid PD/LGD values, and exposure concentration.
- `analyze_risk` performs deterministic RWA validation with
  `expected_rwa = exposure_amount * risk_weight`.
- Critical deterministic validation failures produce machine-readable flags with
  `source_agent` and `requires_human_intervention`.
- `SupervisorAgent` enforces consensus and the default loop limit of 2.
- Final commentary remains structured and passes through `FinalOutputGuard` before response.

## Verification Coverage

Backend tests cover:

- successful one-round completion,
- fan-out/fan-in worker execution,
- internal ReAct step traces,
- duplicate asset ID detection,
- missing output detection,
- missing risk parameter detection,
- non-positive exposure detection,
- exposure concentration analysis,
- deterministic RWA variance validation,
- consensus completion,
- loop-limit completion,
- API response shape and stable validation flag names.

Frontend API types were updated so validation flags and agent findings match the backend
response contract.

## Notes

Langfuse and full LLM Guard runtime behavior are intentionally outside RCT-16 and belong to
the next linked task. This implementation keeps the RCT-16 runtime deterministic, compact,
and ready for those cross-cutting layers.
