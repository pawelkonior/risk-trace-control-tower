# RWA Executive Commentary Contracts

Endpoint:

```text
POST /v1/agents/rwa-analysis/run
```

Request fields:

- `request_id`
- `loop_limit`, default `2`, maximum `2`
- `materiality_threshold`
- `rwa_input_data`
- `rwa_output_results`

Allowed graph-state record fields:

- `asset_id`
- `asset_class`
- `sector`
- `exposure_amount`
- `risk_weight`
- `rating`
- `pd`
- `lgd`
- `maturity_years`
- `rwa_amount`
- `approach`

Supported final workflow statuses:

- `COMPLETED`
- `LOOP_LIMIT_REACHED`
- `BLOCKED`

Invalid schema, PII-like input, authentication, authorization, or transport failures are
normal API errors before graph execution. They are not represented as invented
`final_commentary.status` values.

The backend returns structured commentary fields for Executive Summary, CRO View, CFO View,
data-quality observations, risk observations, quantitative validation, recommended actions,
validation flags, source agents, messages, and observability metadata.

The React briefing endpoint exposes `calculatedRwaRows` from real calculator output so the
AI Executive Commentary component can build the agent request without synthetic movement-driver
rows. The frontend maps those rows to the agent contract with newly generated anonymized
`ASSET-###` identifiers and excludes PII-like fields before calling
`POST /v1/agents/rwa-analysis/run`. If no calculated rows are available, the UI shows the
unavailable state and does not synthesize substitute commentary or request data.

Prompt registry metadata uses the production prompt names:

- `rwa-data-analyst-agent-system`
- `rwa-risk-expert-agent-system`
- `rwa-supervisor-agent-system`

When Langfuse is disabled, prompt usages report `source: local_fallback`; when enabled and
configured, prompt usages report `source: langfuse` with label, fetch status, and latency.
