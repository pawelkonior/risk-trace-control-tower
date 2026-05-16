# RCT-15 Technical Impact Analysis
**Epic:** RCT-13 - Deliver guarded, observable, multi-agent RWA executive commentary  
**Story:** RCT-14 - Implement optimized guarded multi-agent RWA executive commentary workflow  
**Task:** RCT-15 - Define optimized RWA commentary architecture, contracts, AgentState, and request validation  
**Branch:** `RCT-15_define_agentic_architecture`  
**Analysis Date:** 2026-05-16  

---

## Executive Summary

This task establishes the foundation for a **multi-agent LangGraph workflow** that generates safe, traceable, PII-protected executive commentary for RWA (Risk-Weighted Assets) analysis. The implementation will create:

1. **Architecture documentation** for an optimized compact graph with parallel worker agents
2. **Strongly-typed Pydantic v2 contracts** for request/response and AgentState
3. **Pre-graph validation layer** with PII rejection before LangGraph execution
4. **Backend API contract** at `POST /v1/agents/rwa-analysis/run`

**Critical Design Principle:** This task focuses on **contracts, validation, and architecture** - NOT implementation of agent logic, LLM Guard runtime, Langfuse integration, or dashboard UI.

---

## Current System Analysis

### Backend Structure
```
apps/backend/src/
├── rwa_agents/              # EMPTY - New package to create
├── rwa_calculator/          # Existing RWA calculation engine
│   └── rwa_calculator/
│       └── fastapi_app.py   # Main FastAPI app (port 8000)
├── rwa_dashboard/           # Existing dashboard data/API
│   ├── api.py              # Dashboard snapshot generation
│   ├── schemas.py          # Frontend-facing Pydantic schemas
│   └── service.py          # RiskTrace UI service
└── rwa_common/             # Shared database utilities
```

### Frontend Structure
```
apps/frontend/src/
├── pages/
│   └── RwaIntelligenceBriefingPage.tsx  # Target UI for commentary
├── components/
│   └── rwa-briefing/                    # Existing briefing components
└── api/
    ├── client.ts                        # API base URL configuration
    └── types.ts                         # TypeScript types
```

### Existing API Endpoints
- `GET /v1/dashboard/snapshot` - Dashboard data (existing)
- `GET /v1/briefing/snapshot` - Briefing data (existing, needs commentary extension)
- `POST /v1/rwa/calculate` - RWA calculation (existing)

### Key Findings
1. **No existing agent infrastructure** - `rwa_agents/` directory is empty
2. **FastAPI app exists** - Can extend with new agent endpoint
3. **Dashboard schemas exist** - Can extend for commentary response
4. **Frontend briefing page exists** - Ready for commentary component integration
5. **Database layer exists** - SQLAlchemy with Postgres/SQLite support

---

## Proposed Architecture

### Optimized Compact Graph Flow
```
RequestValidation (PII Guard)
    ↓
AgentStateBuilt
    ↓
AnalysisPhase (Fan-out)
    ├─→ DataAnalystAgent (parallel)
    └─→ RiskExpertAgent (parallel)
    ↓
AnalysisFanIn
    ↓
SupervisorAgent (Routing & Synthesis)
    ↓
FinalOutputGuard (LLM Guard scan)
    ↓
FinalStructuredResponse
```

**Key Architectural Decisions:**
- **ReAct stays internal** to worker nodes (not separate graph nodes)
- **Parallel execution** for independent DataAnalyst and RiskExpert workers
- **Compact design** - avoid unnecessary graph node expansion
- **Deterministic validation first** - Python tools before LLM interpretation
- **Guardrails at boundaries** - LLM Guard at every LLM-facing interaction

### Cross-Cutting Layers
1. **LLM Guard** - Input/output scanning at every LLM boundary
2. **Langfuse** - Optional observability (disabled-safe for local runs)
3. **Prompt Registry** - Langfuse + local fallback for prompts
4. **MemorySaver** - Checkpointing by thread_id

---

## Required AgentState Schema

```python
class AgentState(TypedDict):
    # Request context
    request_id: str
    rwa_input_data: list[RwaInputRecord]
    rwa_output_results: list[RwaOutputRecord]
    
    # Agent communication
    messages: list[BaseMessage]
    
    # Analysis results
    validation_flags: list[ValidationFlag]
    agent_findings: list[AgentFinding]
    recommended_actions: list[RecommendedAction]
    commentary_views: CommentaryViews
    
    # Guardrails
    guardrail_results: list[GuardrailResult]
    
    # Loop control
    loop_count: int
    loop_limit: int  # Default: 2
    consensus_reached: bool
    
    # Final output
    final_commentary: FinalCommentary | None
    
    # Routing
    next_agent: str | None
    guardrail_blocked: bool
```

---

## Data Contract Specifications

### Allowed Anonymized Fields
```python
ALLOWED_FIELDS = [
    "asset_id",           # e.g., "ASSET-001"
    "asset_class",
    "sector",
    "exposure_amount",
    "risk_weight",
    "rating",
    "pd",
    "lgd",
    "maturity_years",
    "rwa_amount",
    "approach",
]
```

### Rejected PII-Like Fields
```python
REJECTED_PII_FIELDS = [
    "customer_name",
    "client_name",
    "borrower_name",
    "counterparty_name",
    "first_name",
    "last_name",
    "email",
    "phone",
    "address",
    "account_number",
    "iban",
    "ssn",
    "pesel",
    "passport",
    "tax_id",
]
```

### Backend API Contract

**Endpoint:** `POST /v1/agents/rwa-analysis/run`

**Request:**
```json
{
  "request_id": "example-run",
  "loop_limit": 2,
  "materiality_threshold": "0.05",
  "rwa_input_data": [],
  "rwa_output_results": []
}
```

**Response:**
```json
{
  "api_version": "v1",
  "service_version": "0.1.0",
  "request_id": "example-run",
  "run_id": "example-run",
  "status": "COMPLETED",
  "graph_backend": "langgraph",
  "final_commentary": {
    "status": "COMPLETED",
    "consensus_reached": true,
    "loop_count": 1,
    "generated_at": "2026-05-16T00:00:00Z",
    "source_label": "RiskTrace Intelligence",
    "executive_summary": "",
    "cro_view": "",
    "cfo_view": "",
    "data_quality_observations": [],
    "risk_observations": [],
    "quantitative_validation": [],
    "recommended_actions": [],
    "validation_flags": [],
    "source_agents": []
  },
  "messages": [],
  "validation_flags": [],
  "agent_findings": [],
  "recommended_actions": [],
  "commentary_views": {
    "executive_summary": "",
    "cro_view": "",
    "cfo_view": ""
  },
  "observability": {
    "langfuse_enabled": false,
    "trace_id": null,
    "callback_handler_attached": false,
    "checkpointer": "MemorySaver",
    "thread_id": "example-run",
    "prompt_usages": [],
    "evaluation_scores": [],
    "guardrail_results": [],
    "guardrail_block_count": 0,
    "pii_detected": false,
    "prompt_injection_risk": 0.0,
    "node_transition_count": 0,
    "llm_call_count": 0,
    "tool_call_count": 0,
    "total_token_count": 0
  }
}
```

**Supported Statuses:**
- `COMPLETED` - Normal successful completion
- `LOOP_LIMIT_REACHED` - Reached max iterations without consensus
- `BLOCKED` - Guardrail blocked unsafe output

---

## Affected Files and Services

### New Files to Create

#### Backend - Agent Package
```
apps/backend/src/rwa_agents/
├── __init__.py
├── py.typed
├── schemas.py              # Pydantic v2 contracts
├── state.py                # AgentState TypedDict
├── validation.py           # Pre-graph validation & PII guard
├── api.py                  # FastAPI routes
└── docs/
    ├── architecture.md     # Architecture overview
    └── routing.md          # Graph routing diagram
```

#### Backend - Tests
```
apps/backend/tests/agents/
├── __init__.py
├── test_schemas.py         # Schema validation tests
├── test_validation.py      # PII guard tests
└── test_api.py            # API contract tests
```

#### Documentation
```
docs/
├── RCT-15_TECHNICAL_ANALYSIS.md  # This file
└── agents/
    ├── architecture.md
    ├── contracts.md
    └── validation.md
```

### Files to Modify

#### Backend Configuration
- `apps/backend/pyproject.toml` - Add `rwa_agents` to mypy packages, add LangGraph dependencies
- `apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py` - Mount agent routes

#### Frontend (Future Tasks)
- `apps/frontend/src/pages/RwaIntelligenceBriefingPage.tsx` - Add commentary component (RCT-18)
- `apps/frontend/src/api/types.ts` - Add TypeScript types for commentary API

---

## Implementation Steps

### Phase 1: Package Structure (Day 1)
1. Create `apps/backend/src/rwa_agents/` package structure
2. Add `py.typed` marker for type checking
3. Update `pyproject.toml` with new package in mypy config
4. Create test directory structure

### Phase 2: Pydantic Schemas (Day 1-2)
1. Define `RwaInputRecord` schema with allowed fields
2. Define `RwaOutputRecord` schema
3. Define `ValidationFlag`, `AgentFinding`, `RecommendedAction` schemas
4. Define `CommentaryViews` schema (executive_summary, cro_view, cfo_view)
5. Define `GuardrailResult` schema
6. Define `FinalCommentary` schema
7. Define `ObservabilityMetadata` schema
8. Define request/response schemas for API endpoint
9. Add comprehensive schema validation tests

### Phase 3: AgentState Definition (Day 2)
1. Create `state.py` with `AgentState` TypedDict
2. Define all required fields per Jira specification
3. Add type hints and documentation
4. Create state builder function
5. Add state validation tests

### Phase 4: Pre-Graph Validation (Day 2-3)
1. Implement PII field detection logic
2. Implement anonymized identifier validation
3. Create request validation function
4. Add validation error responses
5. Ensure rejected requests never enter graph execution
6. Add comprehensive validation tests

### Phase 5: API Contract (Day 3)
1. Create FastAPI router in `api.py`
2. Define `POST /v1/agents/rwa-analysis/run` endpoint
3. Wire up request validation
4. Return structured error responses for invalid requests
5. Add placeholder response for valid requests (no graph execution yet)
6. Add API integration tests

### Phase 6: Documentation (Day 3-4)
1. Write architecture overview document
2. Create routing diagram (Mermaid format)
3. Document data contracts
4. Document validation rules
5. Document API endpoint specification
6. Add implementation notes

### Phase 7: Integration (Day 4)
1. Mount agent router in main FastAPI app
2. Verify CORS configuration
3. Test endpoint accessibility
4. Verify request/response contract
5. Run full test suite

---

## Dependencies

### Python Packages to Add
```toml
[project.dependencies]
# Existing dependencies remain...
langgraph = ">=0.2,<1.0"
langchain-core = ">=0.3,<1.0"
langchain-openai = ">=0.2,<1.0"  # For LLM integration (future)
```

### Development Dependencies
```toml
[dependency-groups.dev]
# Existing dev dependencies remain...
langchain-community = ">=0.3,<1.0"  # For testing
```

### External Services (Optional, Future Tasks)
- **Langfuse** - Observability (RCT-17)
- **LLM Guard** - Safety scanning (RCT-17)
- **OpenAI API** - LLM provider (RCT-16)

---

## Risks and Mitigations

### Risk 1: PII Leakage
**Impact:** High - Regulatory violation  
**Probability:** Medium  
**Mitigation:**
- Pre-graph validation rejects PII-like fields
- Comprehensive field whitelist
- Automated tests for PII detection
- No PII fields in AgentState schema

### Risk 2: Schema Drift
**Impact:** Medium - Breaking changes  
**Probability:** Low  
**Mitigation:**
- Pydantic v2 strict validation
- Comprehensive schema tests
- API versioning (`/v1/`)
- Backward compatibility tests

### Risk 3: Performance Bottleneck
**Impact:** Medium - Slow response times  
**Probability:** Low (this task only defines contracts)  
**Mitigation:**
- Compact graph design
- Parallel worker execution (future)
- Default loop limit of 2
- Async FastAPI handlers

### Risk 4: Integration Complexity
**Impact:** Medium - Difficult to integrate with existing code  
**Probability:** Low  
**Mitigation:**
- Separate `rwa_agents` package
- Clean API boundaries
- Existing FastAPI app structure
- Comprehensive documentation

---

## Testing Strategy

### Unit Tests
- Schema validation (valid/invalid inputs)
- PII detection (positive/negative cases)
- Anonymized identifier validation
- State builder logic
- Request/response serialization

### Integration Tests
- API endpoint accessibility
- Request validation flow
- Error response formats
- CORS configuration
- Database session handling

### Test Coverage Requirements
- Minimum 70% coverage (per pyproject.toml)
- Branch coverage enabled
- All validation paths tested
- All PII rejection scenarios tested

---

## Acceptance Criteria Verification

### ✅ Scenario: Build typed graph state from valid anonymized request
- [ ] Request validation accepts valid anonymized fields
- [ ] AgentState is created with all required fields
- [ ] Default loop_limit is 2
- [ ] All schema fields are strongly typed

### ✅ Scenario: Reject PII before graph execution
- [ ] PII-like fields are detected
- [ ] Request is rejected with clear error message
- [ ] No AgentState is created
- [ ] LangGraph execution is not started

### ✅ Scenario: Preserve optimized architecture documentation
- [ ] Architecture document shows compact graph flow
- [ ] Routing diagram includes all nodes
- [ ] ReAct internal behavior is documented
- [ ] Cross-cutting layers are explained

### ✅ Scenario: Define stable backend contract
- [ ] Request schema is documented
- [ ] Response schema is documented
- [ ] All required fields are defined
- [ ] API endpoint is specified

---

## Out of Scope (Explicitly)

❌ **NOT in this task:**
- Implementing worker agent logic (RCT-16)
- Implementing LLM Guard runtime (RCT-17)
- Implementing Langfuse integration (RCT-17)
- Implementing dashboard UI component (RCT-18)
- Changing RWA calculator logic
- Implementing LangGraph execution
- Implementing actual LLM calls
- Implementing tool execution

---

## Definition of Done Checklist

- [ ] `apps/backend/src/rwa_agents/` package created
- [ ] All Pydantic v2 schemas defined in `schemas.py`
- [ ] `AgentState` TypedDict defined in `state.py`
- [ ] Pre-graph validation implemented in `validation.py`
- [ ] PII guard implemented and tested
- [ ] API endpoint defined in `api.py`
- [ ] Backend contract documented
- [ ] Architecture documentation created
- [ ] Routing documentation created
- [ ] Unit tests added for schemas
- [ ] Unit tests added for validation
- [ ] Integration tests added for API
- [ ] `ruff check .` passes
- [ ] `ruff format --check .` passes
- [ ] `mypy` passes for `rwa_agents` package
- [ ] `pytest` passes with 70%+ coverage
- [ ] All acceptance criteria verified

---

## Next Steps After RCT-15

1. **RCT-16** - Implement optimized compact LangGraph runtime and deterministic analysis tools
2. **RCT-17** - Add LLM Guard, Langfuse observability, Prompt Registry, scores, and checkpointing
3. **RCT-18** - Build React AI Executive Commentary dashboard component and end-to-end integration

---

## Execution Plan Summary

**Estimated Effort:** 3-4 days  
**Complexity:** Medium  
**Dependencies:** None (foundational task)  
**Blockers:** None identified  

**Recommended Approach:**
1. Start with package structure and schemas (solid foundation)
2. Implement validation layer with comprehensive tests
3. Create API endpoint with placeholder responses
4. Write documentation while implementation is fresh
5. Integrate with main FastAPI app
6. Verify all acceptance criteria

**Success Criteria:**
- All tests pass
- Documentation is complete
- API contract is stable
- PII protection is verified
- Ready for RCT-16 implementation

---

## Questions for Stakeholder Review

1. **LLM Provider:** Which LLM provider should be used? (OpenAI, Azure OpenAI, Anthropic, local?)
2. **Langfuse Credentials:** Will Langfuse credentials be available for development/testing?
3. **LLM Guard Configuration:** What safety thresholds should be configured?
4. **Loop Limit:** Is default loop_limit=2 acceptable, or should it be configurable?
5. **Materiality Threshold:** What is the business definition of materiality_threshold?
6. **Data Source:** How will dashboard-calculated RWA rows be mapped to agent input?

---

**Analysis Complete - Ready for Implementation Approval**