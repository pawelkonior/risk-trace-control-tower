**User:**

<task>
use atlassian mcp and implement existing MCP-019: Prepare release evidence and human review package
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:45.605Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>


# Current Workspace Directory (/home/cezary/projects/risk-trace-control-tower) Files
.semgrepignore
.trivyignore
AGENTS.md
.agents/
.bob/
.codex/
.github/
apps/
apps/docker-compose.yml
apps/backend/.env.example
apps/backend/.gitignore
apps/backend/.python-version
apps/backend/Dockerfile
apps/backend/pyproject.toml
apps/backend/uv.lock
apps/backend/src/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/generate_preprod_rwa_dataset.py
apps/backend/src/rwa_calculator/nccr_mapping.csv
apps/backend/src/rwa_calculator/paths.py
apps/backend/src/rwa_calculator/preprod_core_info_1000.csv
apps/backend/src/rwa_calculator/preprod_country_info.csv
apps/backend/src/rwa_calculator/preprod_dataset_summary.json
apps/backend/src/rwa_calculator/py.typed
apps/backend/src/rwa_calculator/rwa_backend.py
apps/backend/src/rwa_calculator/rwa_pydantic_schemas.py
apps/backend/src/rwa_calculator/reference_data/manifest.json
apps/backend/src/rwa_calculator/reference_data/README.md
apps/backend/src/rwa_calculator/reference_data/bcbs/basel_iii_final_reforms_2017.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/CH_FINMA_BASEL_III_FINAL/overlay.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/EU_CRR3_EBA/overlay.json
apps/backend/src/rwa_calculator/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/rwa_calculator/api_schemas.py
apps/backend/src/rwa_calculator/rwa_calculator/calculator.py
apps/backend/src/rwa_calculator/rwa_calculator/capital_models.py
apps/backend/src/rwa_calculator/rwa_calculator/capital.py
apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py
apps/backend/src/rwa_calculator/rwa_calculator/models.py
apps/backend/src/rwa_calculator/rwa_calculator/normal_distribution.py
apps/backend/src/rwa_calculator/rwa_calculator/pandera_validation.py
apps/backend/src/rwa_calculator/rwa_calculator/reference.py
apps/backend/src/rwa_calculator/rwa_calculator/server.py
apps/backend/src/rwa_common/py.typed
apps/backend/src/rwa_projection_service/__init__.py
apps/backend/src/rwa_projection_service/calendar.py
apps/backend/src/rwa_projection_service/engine.py
apps/backend/src/rwa_projection_service/fastapi_app.py
apps/backend/src/rwa_projection_service/py.typed
apps/backend/src/rwa_projection_service/schemas.py
apps/backend/src/rwa_rats_service/py.typed
apps/backend/src/rwa_rats_service/schemas.py
apps/backend/src/rwa_steering/__init__.py
apps/backend/src/rwa_steering/cli.py
apps/backend/src/rwa_steering/engine.py
apps/backend/src/rwa_steering/errors.py
apps/backend/src/rwa_steering/fastapi_app.py
apps/backend/src/rwa_steering/input_package.py
apps/backend/src/rwa_steering/missing_inputs.py
apps/backend/src/rwa_steering/py.typed
apps/backend/src/rwa_steering/scenarios.py
apps/backend/src/rwa_steering/transformations.py
apps/backend/src/rwa_steering/generated_inputs/capital_positions.csv
apps/backend/src/rwa_steering/generated_inputs/cva_hedges.csv
apps/backend/src/rwa_steering/generated_inputs/cva_netting_sets.csv
apps/backend/src/rwa_steering/generated_inputs/cva_portfolio_inputs.csv
apps/backend/src/rwa_steering/generated_inputs/data_quality_flags.csv
apps/backend/src/rwa_steering/generated_inputs/dlgd_scenario_assumptions.csv
apps/backend/src/rwa_steering/generated_inputs/forecast_calendar.csv
apps/backend/src/rwa_steering/generated_inputs/fx_scenario_rates.csv
apps/backend/src/rwa_steering/generated_inputs/leverage_exposures.csv
apps/backend/src/rwa_steering/generated_inputs/leverage_off_balance_sheet_items.csv
apps/backend/src/rwa_steering/generated_inputs/macro_regime_indicators.csv
apps/backend/src/rwa_steering/generated_inputs/manifest.json
apps/backend/src/rwa_steering/generated_inputs/operational_risk_business_indicators.csv
apps/backend/src/rwa_steering/generated_inputs/operational_risk_losses.csv
apps/backend/src/rwa_steering/generated_inputs/portfolio_strategy_limits.csv
apps/backend/src/rwa_steering/generated_inputs/profitability_inputs.csv
apps/backend/src/rwa_steering/generated_inputs/rating_migration_matrix.csv
apps/backend/src/rwa_steering/generated_inputs/README.md
apps/backend/src/rwa_steering/generated_inputs/regulatory_overlay_selection.csv
apps/backend/src/rwa_steering/generated_inputs/scenario_definitions.csv
apps/backend/src/rwa_steering/generated_inputs/segment_growth_assumptions.csv
apps/backend/src/rwa_steering/generated_inputs/steering_action_constraints.csv
apps/backend/src/rwa_steering/generated_inputs/validation_report.json
apps/frontend/.dockerignore
apps/frontend/.env.example
apps/frontend/.gitignore
apps/frontend/Dockerfile
apps/frontend/index.html
apps/frontend/nginx.conf
apps/frontend/package.json
apps/frontend/playwright.config.ts
apps/frontend/README.md
apps/frontend/tsconfig.json
apps/frontend/tsconfig.node.json
apps/frontend/vite.config.ts
apps/frontend/public/risktrace-logo-sm.png
apps/frontend/public/risktrace-logo.png
apps/frontend/scripts/playwright-web-server.mjs
apps/frontend/src/App.tsx
apps/frontend/src/main.tsx
apps/frontend/src/navigation.ts
apps/frontend/src/vite-env.d.ts
apps/frontend/src/api/client.ts
apps/frontend/src/api/rwaApi.ts
apps/frontend/src/api/rwaDashboardApi.ts
apps/frontend/src/api/types.ts
apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx
apps/frontend/src/components/rwa-briefing/BriefingInsightCards.tsx
apps/frontend/src/components/rwa-briefing/BriefingKpiStrip.tsx
apps/frontend/src/components/rwa-briefing/EvidenceTraceabilityCard.tsx
apps/frontend/src/components/rwa-briefing/ManagementReviewPackCard.tsx
apps/frontend/src/components/rwa-briefing/RwaMovementAttributionCard.tsx
apps/frontend/src/components/rwa-dashboard/CapitalSummaryCard.tsx
apps/frontend/src/components/rwa-dashboard/ExposureDonutCard.tsx
apps/frontend/src/components/rwa-dashboard/FilterBar.tsx
apps/frontend/src/components/rwa-dashboard/PageHeader.tsx
apps/frontend/src/components/rwa-dashboard/Sidebar.tsx
apps/frontend/src/components/rwa-dashboard/Toast.tsx
apps/frontend/src/components/rwa-dashboard/TopBar.tsx
apps/frontend/src/components/rwa-dashboard/TopExposuresCard.tsx
apps/frontend/src/components/rwa-lineage/LineageFlowCard.tsx
apps/frontend/src/components/rwa-lineage/LineageSideRail.tsx
apps/frontend/src/components/rwa-lineage/LineageSummaryCard.tsx
apps/frontend/src/hooks/iconHydration.ts
apps/frontend/src/hooks/useApiResource.ts
apps/frontend/src/hooks/useAppContextData.ts
apps/frontend/src/hooks/useNotificationsData.ts
apps/frontend/src/hooks/useRwaBriefingData.ts
apps/frontend/src/hooks/useRwaLineageData.ts
apps/frontend/src/hooks/useToast.ts
apps/frontend/src/styles/rwa-dashboard.css
apps/frontend/tests/e2e/navigation.spec.ts
bob_sessions/
bob_sessions/bob_task_may-16-2026_5-49-33-pm.md
bob_sessions/bob_task_may-16-2026_6-24-03-pm.md
bob_sessions/bob_task_may-16-2026_6-24-03-pm.png
bob_sessions/bob_task_may-16-2026_6-44-37-pm.png
bob_sessions/bob_task_may-16-2026_7-26-23-pm.md
bob_sessions/bob_task_may-16-2026_7-26-23-pm.png
bob_sessions/bob_task_may-16-2026_9-41-56-pm.png
bob_sessions/bob_task_may-16-2026_10-44-03-pm.md
bob_sessions/bob_task_may-16-2026_11-27-12-pm.md
bob_sessions/bob_task_may-16-2026_11-54-41-pm.md
bob_sessions/bob_task_may-16-2026_11-54-41-pm.png
bob_sessions/bob_task_may-17-2026_1-03-09-am.md
bob_sessions/bob_task_may-17-2026_1-25-46-am.png
bob_sessions/bob_task_may-17-2026_2-22-21-am.md
bob_sessions/bob_task_may-17-2026_2-22-21-am.png
bob_sessions/bob_task_may-17-2026_3-06-50-am.md
bob_sessions/bob_task_may-17-2026_3-06-50-am.png
bob_sessions/bob_task_may-17-2026_10-47-14-am.md
bob_sessions/bob_task_may-17-2026_12-05-00-pm.md
bob_sessions/bob_task_may-17-2026_12-11-43-am.md
bob_sessions/bob_task_may-17-2026_12-11-43-am.png
bob_sessions/bob_task_may-17-2026_12-18-36-am.md
bob_sessions/bob_task_may-17-2026_12-18-36-am.png
bob_sessions/bob_task_may-17-2026_12-45-41-am.md
bob_sessions/bob_task_may-17-2026_12-45-41-am.png
docker/
docs/
docs/RCT-15_TECHNICAL_ANALYSIS.md
docs/RCT-17_IMPLEMENTATION_SUMMARY.md
docs/RCT-17_TECHNICAL_ANALYSIS.md
docs/RCT-18_IMPLEMENTATION_SUMMARY.md
docs/RCT-18_TECHNICAL_ANALYSIS.md
docs/RCT-18_VALIDATION_REPORT.md
docs/RCT-40_TECHNICAL_ANALYSIS.md
docs/RCT-40_WATSONX_FINALIZATION.md
docs/agents/monitoring.md
infra/
infra/helm/rwa-platform/Chart.yaml
infra/helm/rwa-platform/values-dev.yaml
infra/terraform/environments/prod/main.tf
infra/terraform/modules/ecr/main.tf
infra/terraform/modules/ecr/outputs.tf
infra/terraform/modules/ecr/variables.tf
infra/terraform/modules/elasticache/main.tf
infra/terraform/modules/elasticache/outputs.tf
infra/terraform/modules/elasticache/variables.tf
infra/terraform/modules/msk/main.tf
infra/terraform/modules/msk/outputs.tf
infra/terraform/modules/msk/variables.tf
infra/terraform/modules/networking/main.tf
infra/terraform/modules/networking/outputs.tf
infra/terraform/modules/networking/variables.tf
infra/terraform/modules/rds/main.tf
infra/terraform/modules/rds/outputs.tf
infra/terraform/modules/rds/README.md
infra/terraform/modules/rds/variables.tf
infra/terraform/modules/s3/main.tf
infra/terraform/modules/s3/outputs.tf
infra/terraform/modules/s3/variables.tf
k6/
k8s/
k8s/cert-manager/cluster-issuer-prod.yaml
k8s/cert-manager/cluster-issuer-staging.yaml
mcps/
observability/
observability/agents-alerts.yaml
scripts/

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll implement MCP-019: Prepare release evidence and human review package using the Atlassian MCP. Let me start by understanding the existing structure and then create the implementation.

<read_file>
<args>
<file>
<path>.codex</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for '.codex'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>.codex</path><error>File not found</error><notice>The file was not found. Consider using list_files to find available files before attempting to read them.</notice></file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:49.518Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.10

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<list_files>
<path>.codex</path>
<recursive>true</recursive>
</list_files>

---

**User:**

[list_files for '.codex'] Result:
No files found.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:51.649Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.20

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<list_files>
<path>.bob</path>
<recursive>true</recursive>
</list_files>

---

**User:**

[list_files for '.bob'] Result:
🛡️ custom_modes.yaml
🛡️ mcp.example.json
🛡️ mcp.json
🛡️ analysis/
🛡️ analysis/ai-agents-improvement-recommendations.md
🛡️ resources/
🛡️ resources/1779019867878-lf-events-export-cmp9mqwv205e6ad07fnqsh1ua.json
🛡️ rules-advanced/
🛡️ rules-advanced/AGENTS.md
🛡️ rules-ask/
🛡️ rules-ask/AGENTS.md
🛡️ rules-code/
🛡️ rules-code/AGENTS.md
🛡️ rules-plan/
🛡️ rules-plan/AGENTS.md
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:53.700Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.30

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<search_files>
<path>.</path>
<regex>MCP-019</regex>
<file_pattern>*.md</file_pattern>
</search_files>

---

**User:**

[search_files for 'MCP-019' in '*.md'] Result:
Found 5 results.

# bob_sessions/bob_task_may-17-2026_12-45-41-am.md
  8 | - RCT-37: MCP-018 Full test suite and quality gate
  9 | - RCT-38: MCP-019 Release evidence and human review package
 10 | - RCT-39: MCP-020 Optional CI workflow for build, test and Docker build
----
2228 | 
2229 | 2. **RCT-38 (MCP-019 Release evidence and human review package)**: Should the release evidence package be a single document or multiple files? What format is preferred (Markdown, JSON, or both)?
2230 | 
----
2258 | 
2259 | 2. **RCT-38 (MCP-019 Release evidence and human review package)**: Should the release evidence package be a single document or multiple files? What format is preferred (Markdown, JSON, or both)?
2260 | 
----
2473 | 
2474 | ### RCT-38: MCP-019 Release Evidence and Human Review Package
2475 | 
----
6724 | 
6725 | ### RCT-38: MCP-019 Release Evidence and Human Review Package ✅
6726 | 
----
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:55.773Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.40

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>bob_sessions/bob_task_may-17-2026_12-45-41-am.md</path>
<line_range>2470-2550</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'bob_sessions/bob_task_may-17-2026_12-45-41-am.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>bob_sessions/bob_task_may-17-2026_12-45-41-am.md</path>
<content lines="2470-2550">
2470 | ```
2471 | 
2472 | ---
2473 | 
2474 | ### RCT-38: MCP-019 Release Evidence and Human Review Package
2475 | 
2476 | **Objective**: Create comprehensive release evidence package with human review disclaimer.
2477 | 
2478 | **Directory Structure**:
2479 | ```
2480 | mcps/regulatory_mcp/docs/release-evidence/
2481 | ├── build-log.txt              # npm run build output
2482 | ├── test-results.txt           # npm test output with coverage
2483 | ├── docker-build.log           # Docker build output
2484 | ├── tool-contracts.json        # 15 MCP tools with schemas
2485 | ├── corpus-inventory.json      # Regulations, controls, mappings inventory
2486 | └── release-readiness.md       # Main evidence document
2487 | ```
2488 | 
2489 | **release-readiness.md Contents**:
2490 | 1. **Executive Summary**
2491 |    - Release version and date
2492 |    - Overall readiness status
2493 |    - Critical blockers (if any)
2494 | 
2495 | 2. **MCP Tool Contracts**
2496 |    - List of 15 tools with descriptions
2497 |    - Input/output schemas
2498 |    - Read-only/idempotent annotations
2499 | 
2500 | 3. **Corpus Inventory**
2501 |    - 9+ regulations (BCBS239, CRR3, DORA, EBA, GDPR, Internal policies)
2502 |    - 15+ engineering controls
2503 |    - Keyword, artifact, and domain mappings
2504 |    - Referential integrity validation status
2505 | 
2506 | 4. **Build and Test Evidence**
2507 |    - Build success confirmation
2508 |    - Test pass rate and coverage metrics
2509 |    - Docker build success
2510 | 
2511 | 5. **Known Limitations**
2512 |    - Local-only operation (no external APIs)
2513 |    - Deterministic corpus (not a legal research engine)
2514 |    - Requires Node.js 20+
2515 |    - STDIO transport only
2516 | 
2517 | 6. **Security and Privacy Notes**
2518 |    - No external API calls
2519 |    - No data exfiltration
2520 |    - Local corpus only
2521 |    - No authentication/authorization (client responsibility)
2522 | 
2523 | 7. **Human Review Required Disclaimer** ⚠️
2524 |    ```
2525 |    ⚠️ IMPORTANT: This MCP server provides engineering guidance only.
2526 |    
2527 |    All regulatory mappings, controls, evidence requirements, and 
2528 |    release readiness decisions MUST be reviewed by qualified 
2529 |    compliance, legal, or risk specialists before production use.
2530 |    
2531 |    This tool does NOT provide:
2532 |    - Legal advice
2533 |    - Regulatory compliance certification
2534 |    - Substitute for qualified compliance review
2535 |    ```
2536 | 
2537 | 8. **Release Readiness Assessment**
2538 |    - Implemented controls checklist
2539 |    - Evidence artifacts collected
2540 |    - Blocking gaps (if any)
2541 |    - Sign-off requirements
2542 | 
2543 | **Implementation Steps**:
2544 | 1. Create `docs/release-evidence/` directory
2545 | 2. Run build and capture output to `build-log.txt`
2546 | 3. Run tests and capture output to `test-results.txt`
2547 | 4. Build Docker image and capture output to `docker-build.log`
2548 | 5. Generate `tool-contracts.json` from tool definitions
2549 | 6. Generate `corpus-inventory.json` from corpus stats
2550 | 7. Write comprehensive `release-readiness.md`
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:36:58.211Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.50

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[ ] Explore regulatory_mcp directory structure
[ ] Create release-evidence directory
[ ] Generate tool-contracts.json from MCP tool definitions
[ ] Generate corpus-inventory.json from corpus data
[ ] Run build and capture output
[ ] Run tests and capture output
[ ] Build Docker image and capture output
[ ] Create comprehensive release-readiness.md
[ ] Use Atlassian MCP to create Confluence page with release evidence
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:37:01.671Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.61

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Pending |
| 2 | Create release-evidence directory | Pending |
| 3 | Generate tool-contracts.json from MCP tool definitions | Pending |
| 4 | Generate corpus-inventory.json from corpus data | Pending |
| 5 | Run build and capture output | Pending |
| 6 | Run tests and capture output | Pending |
| 7 | Build Docker image and capture output | Pending |
| 8 | Create comprehensive release-readiness.md | Pending |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<list_files>
<path>mcps</path>
<recursive>true</recursive>
</list_files>

---

**User:**

[list_files for 'mcps'] Result:
.env.example
.gitignore
docker-compose.yml
README.md
regulatory_mcp/
regulatory_mcp/.dockerignore
regulatory_mcp/.gitignore
regulatory_mcp/Dockerfile
regulatory_mcp/package-lock.json
regulatory_mcp/package.json
regulatory_mcp/README.md
regulatory_mcp/test-startup.sh
regulatory_mcp/tsconfig.json
regulatory_mcp/vitest.config.ts
regulatory_mcp/data/
regulatory_mcp/data/controls/
regulatory_mcp/data/controls/ARCH-ADR-001.json
regulatory_mcp/data/controls/DORA-ICT-001.json
regulatory_mcp/data/controls/PERF-RWA-001.json
regulatory_mcp/data/controls/REL-EVID-001.json
regulatory_mcp/data/controls/RWA-AUDIT-001.json
regulatory_mcp/data/controls/RWA-CALC-001.json
regulatory_mcp/data/controls/RWA-DATA-001.json
regulatory_mcp/data/controls/RWA-DQ-001.json
regulatory_mcp/data/controls/RWA-RECON-001.json
regulatory_mcp/data/controls/RWA-REPORT-001.json
regulatory_mcp/data/controls/RWA-RULE-001.json
regulatory_mcp/data/controls/SEC-ACCESS-001.json
regulatory_mcp/data/controls/SEC-INPUT-001.json
regulatory_mcp/data/controls/SEC-LOG-001.json
regulatory_mcp/data/controls/TEST-REG-001.json
regulatory_mcp/data/examples/
regulatory_mcp/data/examples/architecture-rwa-service.md
regulatory_mcp/data/examples/code-diff-risk-weight.patch
regulatory_mcp/data/examples/feature-rwa-csv-upload.md
regulatory_mcp/data/examples/release-evidence.json
regulatory_mcp/data/mappings/
regulatory_mcp/data/mappings/artifact-type-to-controls.json
regulatory_mcp/data/mappings/domain-to-regulations.json
regulatory_mcp/data/mappings/keywords-to-controls.json
regulatory_mcp/data/regulations/
regulatory_mcp/data/regulations/BCBS239.json
regulatory_mcp/data/regulations/CRR3.json
regulatory_mcp/data/regulations/DORA.json
regulatory_mcp/data/regulations/EBA_ICT_SECURITY.json
regulatory_mcp/data/regulations/EBA_REPORTING_4.json
regulatory_mcp/data/regulations/GDPR.json
regulatory_mcp/data/regulations/INTERNAL_AUDIT_EVIDENCE.json
regulatory_mcp/data/regulations/INTERNAL_RULE_GOVERNANCE.json
regulatory_mcp/data/regulations/INTERNAL_SDLC.json
regulatory_mcp/docs/
regulatory_mcp/docs/release-evidence/
regulatory_mcp/docs/release-evidence/build-log.txt
regulatory_mcp/docs/release-evidence/compose-build.txt
regulatory_mcp/docs/release-evidence/compose-run-output.txt
regulatory_mcp/docs/release-evidence/corpus-inventory.json
regulatory_mcp/docs/release-evidence/docker-build.txt
regulatory_mcp/docs/release-evidence/production-audit.txt
regulatory_mcp/docs/release-evidence/release-readiness.md
regulatory_mcp/docs/release-evidence/test-results.txt
regulatory_mcp/docs/release-evidence/tool-contracts.json
regulatory_mcp/src/
regulatory_mcp/src/config.test.ts
regulatory_mcp/src/config.ts
regulatory_mcp/src/index.ts
regulatory_mcp/src/server.ts
regulatory_mcp/src/resources/
regulatory_mcp/src/resources/registerPrompts.ts
regulatory_mcp/src/resources/registerResources.test.ts
regulatory_mcp/src/resources/registerResources.ts
regulatory_mcp/src/schemas/
regulatory_mcp/src/schemas/common.ts
regulatory_mcp/src/schemas/control.ts
regulatory_mcp/src/schemas/evidence.ts
regulatory_mcp/src/schemas/finding.ts
regulatory_mcp/src/schemas/regulation.ts
regulatory_mcp/src/schemas/schemas.test.ts
regulatory_mcp/src/services/
regulatory_mcp/src/services/controlMatcher.test.ts
regulatory_mcp/src/services/controlMatcher.ts
regulatory_mcp/src/services/corpusLoader.test.ts
regulatory_mcp/src/services/corpusLoader.ts
regulatory_mcp/src/services/corpusStore.test.ts
regulatory_mcp/src/services/corpusStore.ts
regulatory_mcp/src/services/generationServices.test.ts
regulatory_mcp/src/services/generationServices.ts
regulatory_mcp/src/services/regulationSearch.test.ts
regulatory_mcp/src/services/regulationSearch.ts
regulatory_mcp/src/services/releaseReadiness.test.ts
regulatory_mcp/src/services/releaseReadiness.ts
regulatory_mcp/src/services/reportGenerator.ts
regulatory_mcp/src/services/reviewServices.test.ts
regulatory_mcp/src/services/reviewServices.ts
regulatory_mcp/src/services/serviceUtils.ts
regulatory_mcp/src/tools/
regulatory_mcp/src/tools/registerTools.test.ts
regulatory_mcp/src/tools/registerTools.ts
sonarqube/
sonarqube/backend-project.properties
sonarqube/frontend-project.properties
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:37:03.977Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.72

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Pending |
| 2 | Create release-evidence directory | Pending |
| 3 | Generate tool-contracts.json from MCP tool definitions | Pending |
| 4 | Generate corpus-inventory.json from corpus data | Pending |
| 5 | Run build and capture output | Pending |
| 6 | Run tests and capture output | Pending |
| 7 | Build Docker image and capture output | Pending |
| 8 | Create comprehensive release-readiness.md | Pending |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>mcps/regulatory_mcp/docs/release-evidence/release-readiness.md</path>
</file>
<file>
<path>mcps/regulatory_mcp/docs/release-evidence/tool-contracts.json</path>
</file>
<file>
<path>mcps/regulatory_mcp/docs/release-evidence/corpus-inventory.json</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'mcps/regulatory_mcp/docs/release-evidence/release-readiness.md', 'mcps/regulatory_mcp/docs/release-evidence/tool-contracts.json', 'mcps/regulatory_mcp/docs/release-evidence/corpus-inventory.json'] Result:
<files>
<file><path>mcps/regulatory_mcp/docs/release-evidence/release-readiness.md</path>
<content lines="1-534">
  1 | # Release Evidence Package: Bank Regulatory Controls MCP
  2 | 
  3 | **Version:** 0.1.0  
  4 | **Release Date:** 2026-05-17  
  5 | **Package Generated:** 2026-05-17T00:42:00+02:00
  6 | 
  7 | ---
  8 | 
  9 | ## ⚠️ HUMAN REVIEW REQUIRED
 10 | 
 11 | **IMPORTANT: This MCP server provides engineering guidance only.**
 12 | 
 13 | All regulatory mappings, controls, evidence requirements, and release readiness decisions **MUST be reviewed by qualified compliance, legal, or risk specialists** before production use.
 14 | 
 15 | **This tool does NOT provide:**
 16 | - Legal advice
 17 | - Regulatory compliance certification
 18 | - Substitute for qualified compliance review
 19 | - Guarantee of regulatory compliance
 20 | 
 21 | **All outputs from this MCP server require human validation by:**
 22 | - Compliance officers
 23 | - Legal counsel
 24 | - Risk management specialists
 25 | - Internal audit teams
 26 | 
 27 | ---
 28 | 
 29 | ## Executive Summary
 30 | 
 31 | ### Release Status: ✅ READY FOR COMPLIANCE REVIEW
 32 | 
 33 | The Bank Regulatory Controls MCP server has successfully passed all technical quality gates:
 34 | 
 35 | - ✅ **Build:** Clean TypeScript compilation
 36 | - ✅ **Tests:** 94 tests passing (11 test files)
 37 | - ✅ **Docker:** Multi-stage build successful
 38 | - ✅ **Corpus:** 9 regulations, 15 controls, validated referential integrity
 39 | - ✅ **MCP Protocol:** 15 tools registered with schemas and annotations
 40 | - ✅ **Runtime Security:** No external API calls, local-only operation, production dependency audit clean
 41 | 
 42 | ### Critical Blockers: NONE
 43 | 
 44 | All technical requirements are met. The system is ready for compliance, legal, and risk review.
 45 | 
 46 | ---
 47 | 
 48 | ## 1. MCP Tool Contracts
 49 | 
 50 | ### Tool Count: 15
 51 | 
 52 | All tools are **read-only, non-destructive, and idempotent**.
 53 | 
 54 | #### Core Tools
 55 | 
 56 | 1. **health_check** - Server health and corpus statistics
 57 | 2. **get_regulatory_profile** - Regulations and controls by domain/jurisdiction
 58 | 3. **search_regulations** - Search regulatory corpus
 59 | 4. **match_controls** - Match engineering controls to artifacts
 60 | 
 61 | #### Review Tools
 62 | 
 63 | 5. **review_feature_description** - Review feature for missing controls
 64 | 6. **review_architecture_text** - Review architecture for regulatory gaps
 65 | 7. **review_code_diff** - Review code for hardcoded logic, PII, validation gaps
 66 | 
 67 | #### Generation Tools
 68 | 
 69 | 8. **generate_acceptance_criteria** - Generate acceptance criteria from controls
 70 | 9. **generate_data_lineage_requirements** - Generate RWA lineage requirements
 71 | 10. **generate_audit_log_requirements** - Generate audit event requirements
 72 | 11. **generate_test_obligations** - Generate Given/When/Then test obligations
 73 | 12. **generate_rwa_run_evidence_requirements** - Generate RWA run evidence package
 74 | 
 75 | #### Release Tools
 76 | 
 77 | 13. **assess_release_readiness** - Assess release readiness from controls and evidence
 78 | 14. **generate_regulatory_mapping_report** - Generate Markdown regulatory report
 79 | 15. **explain_control** - Explain control with tasks and common mistakes
 80 | 
 81 | **Full tool contracts:** See `tool-contracts.json`
 82 | 
 83 | ---
 84 | 
 85 | ## 2. Regulatory Corpus Inventory
 86 | 
 87 | ### Summary
 88 | 
 89 | - **Regulations:** 9 (5 EU, 1 Global, 3 Internal)
 90 | - **Controls:** 15 (7 critical, 6 high, 2 medium)
 91 | - **Mappings:** 3 (keywords, artifacts, domains)
 92 | - **Validation:** All referential integrity checks passed
 93 | 
 94 | ### Regulations
 95 | 
 96 | #### External Regulations (6 require human review)
 97 | 
 98 | 1. **BCBS239** - Principles for effective risk data aggregation and risk reporting (GLOBAL)
 99 | 2. **CRR3** - Capital Requirements Regulation III / CRD6 (EU)
100 | 3. **DORA** - Digital Operational Resilience Act (EU)
101 | 4. **EBA_ICT_SECURITY** - EBA Guidelines on ICT and Security Risk Management (EU)
102 | 5. **EBA_REPORTING_4** - EBA Reporting Framework 4.0 (EU)
103 | 6. **GDPR** - General Data Protection Regulation (EU)
104 | 
105 | #### Internal Policies (3, no external review required)
106 | 
107 | 7. **INTERNAL_AUDIT_EVIDENCE** - Internal Audit Evidence Collection Policy
108 | 8. **INTERNAL_RULE_GOVERNANCE** - Internal Rule Governance and Versioning Policy
109 | 9. **INTERNAL_SDLC** - Internal SDLC and Testing Policy
110 | 
111 | ### Controls by Severity
112 | 
113 | #### Critical (7 controls)
114 | 
115 | - **REL-EVID-001** - Release Evidence Package
116 | - **RWA-AUDIT-001** - Calculation Audit Trail and Traceability
117 | - **RWA-CALC-001** - RWA Calculation Accuracy and Traceability
118 | - **RWA-REPORT-001** - Regulatory Report Validation and Submission
119 | - **RWA-RULE-001** - Regulatory Rule Version Control and Change Management
120 | - **SEC-ACCESS-001** - Access Control and Authentication
121 | - **SEC-INPUT-001** - Input Validation and Sanitization
122 | 
123 | #### High (6 controls)
124 | 
125 | - **DORA-ICT-001** - ICT Resilience Testing
126 | - **RWA-DATA-001** - Input Data Completeness and Validation
127 | - **RWA-DQ-001** - Data Quality Flags and Error Handling
128 | - **RWA-RECON-001** - RWA Calculation Reconciliation
129 | - **SEC-LOG-001** - Secure Logging and Sensitive Data Protection
130 | - **TEST-REG-001** - Regulatory Test Coverage
131 | 
132 | #### Medium (2 controls)
133 | 
134 | - **ARCH-ADR-001** - Architecture Decision Records
135 | - **PERF-RWA-001** - RWA Calculation Performance
136 | 
137 | **Full corpus inventory:** See `corpus-inventory.json`
138 | 
139 | ---
140 | 
141 | ## 3. Build Evidence
142 | 
143 | ### Build Command
144 | 
145 | ```bash
146 | npm run build
147 | ```
148 | 
149 | ### Build Output
150 | 
151 | ```
152 | > @risk-trace/regulatory-mcp@0.1.0 build
153 | > tsc
154 | ```
155 | 
156 | **Status:** ✅ SUCCESS  
157 | **TypeScript Compilation:** Clean, no errors  
158 | **Output Directory:** `build/`
159 | 
160 | **Full build log:** See `build-log.txt`
161 | 
162 | ---
163 | 
164 | ## 4. Test Evidence
165 | 
166 | ### Test Command
167 | 
168 | ```bash
169 | npm test
170 | ```
171 | 
172 | ### Test Results
173 | 
174 | ```
175 | Test Files  11 passed (11)
176 |      Tests  94 passed (94)
177 |   Duration  455ms
178 | ```
179 | 
180 | ### Test Coverage by Module
181 | 
182 | - **config.test.ts** - 2 tests (server configuration)
183 | - **schemas.test.ts** - 13 tests (Zod schema validation)
184 | - **corpusLoader.test.ts** - 25 tests (corpus loading, validation, error handling)
185 | - **corpusStore.test.ts** - 32 tests (corpus queries, caching, search)
186 | - **controlMatcher.test.ts** - 3 tests (control matching logic)
187 | - **regulationSearch.test.ts** - 3 tests (regulation search and ranking)
188 | - **generationServices.test.ts** - 6 tests (acceptance criteria, lineage, audit, tests, evidence)
189 | - **reviewServices.test.ts** - 3 tests (feature, architecture, code review)
190 | - **releaseReadiness.test.ts** - 3 tests (release readiness assessment, gaps)
191 | - **registerTools.test.ts** - 2 tests (MCP tool registration, representative calls)
192 | - **registerResources.test.ts** - 2 tests (MCP resources and prompts)
193 | 
194 | ### Key Test Coverage
195 | 
196 | ✅ **Corpus Validation:**
197 | - Invalid JSON detection
198 | - Duplicate ID detection (regulations and controls)
199 | - Dangling reference detection (keywords, artifacts, domains, regulatory basis)
200 | - Schema validation for all corpus items
201 | - Deterministic loading order
202 | 
203 | ✅ **MCP Protocol:**
204 | - `listTools()` returns exactly 15 tools
205 | - Representative tool calls for all 15 tools
206 | - Input/output schemas validated
207 | - Read-only annotations verified
208 | 
209 | ✅ **Business Logic:**
210 | - Control matching with scoring
211 | - Regulation search with ranking
212 | - Review services (feature, architecture, code)
213 | - Generation services (criteria, lineage, audit, tests, evidence)
214 | - Release readiness assessment with gap detection
215 | 
216 | **Full test results:** See `test-results.txt`
217 | 
218 | ---
219 | 
220 | ## 5. Docker Build Evidence
221 | 
222 | ### Docker Build Command
223 | 
224 | ```bash
225 | docker build -t bank-regulatory-controls-mcp .
226 | ```
227 | 
228 | ### Build Strategy
229 | 
230 | - **Multi-stage build:** Build stage + Runtime stage
231 | - **Base Image:** node:20-alpine
232 | - **Build Stage:** Install deps, compile TypeScript, copy data
233 | - **Runtime Stage:** Production deps only, copy build artifacts and data
234 | - **Entry Point:** `node build/index.js`
235 | 
236 | ### Build Status
237 | 
238 | ✅ **SUCCESS** - Image built and tagged as `bank-regulatory-controls-mcp:latest`
239 | 
240 | **Full Docker build log:** See `docker-build.txt`
241 | 
242 | ---
243 | 
244 | ## 6. Docker Compose Evidence
245 | 
246 | ### Compose Build Command
247 | 
248 | ```bash
249 | docker compose -f mcps/docker-compose.yml build bank-regulatory-controls-mcp
250 | ```
251 | 
252 | ### Compose Run Command
253 | 
254 | ```bash
255 | docker compose -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp
256 | ```
257 | 
258 | **Status:** ✅ SUCCESS - Compose service builds and starts the STDIO MCP server.
259 | 
260 | **Compose build output:** See `compose-build.txt`
261 | **Compose smoke output:** See `compose-run-output.txt`
262 | 
263 | ---
264 | 
265 | ## 7. Known Limitations
266 | 
267 | ### Operational Limitations
268 | 
269 | 1. **Local-Only Operation**
270 |    - No external API calls
271 |    - No network connectivity required
272 |    - All data is local and deterministic
273 | 
274 | 2. **STDIO Transport Only**
275 |    - Uses MCP STDIO transport
276 |    - Not an HTTP API
277 |    - Requires MCP-compatible client
278 | 
279 | 3. **Node.js 20+ Required**
280 |    - Minimum Node.js version: 20.0.0
281 |    - Uses modern JavaScript features
282 | 
283 | 4. **Static Corpus**
284 |    - Regulations and controls are static JSON files
285 |    - Not a live regulatory database
286 |    - Updates require corpus file changes and redeployment
287 | 
288 | ### Functional Limitations
289 | 
290 | 1. **Not a Legal Research Engine**
291 |    - Curated engineering corpus only
292 |    - Not comprehensive regulatory coverage
293 |    - Focused on RWA/Basel III/DORA/GDPR domains
294 | 
295 | 2. **No Automated Compliance Decisions**
296 |    - Provides guidance, not decisions
297 |    - All outputs require human review
298 |    - Cannot certify compliance
299 | 
300 | 3. **No External Integrations**
301 |    - Does not call Jira, GitHub, SonarQube, or LLMs
302 |    - Does not write to external systems
303 |    - Read-only operations only
304 | 
305 | 4. **English Language Only**
306 |    - All corpus content in English
307 |    - No multi-language support
308 | 
309 | ---
310 | 
311 | ## 8. Security and Privacy Notes
312 | 
313 | ### Security Posture
314 | 
315 | ✅ **No External API Calls**
316 | - Server does not make outbound HTTP requests
317 | - No data exfiltration risk
318 | - No dependency on external services
319 | 
320 | ✅ **No Data Storage**
321 | - Server does not persist user data
322 | - No database connections
323 | - Stateless operation (corpus loaded at startup)
324 | 
325 | ✅ **Input Validation**
326 | - Tools advertise MCP JSON input schemas and handlers normalize simple input values
327 | - Corpus files are validated via Zod schemas at load time
328 | - Type-safe TypeScript implementation
329 | - No SQL injection or command injection vectors
330 | 
331 | ✅ **Secure Logging**
332 | - Startup logs to stderr (stdout reserved for MCP protocol)
333 | - No PII logging in corpus or tools
334 | - SEC-LOG-001 control enforces no-PII logging
335 | 
336 | ### Privacy Considerations
337 | 
338 | ✅ **No PII Collection**
339 | - Server does not collect or process personal data
340 | - No user tracking or analytics
341 | - Designed to avoid application-level personal data storage or telemetry
342 | 
343 | ⚠️ **Client Responsibility**
344 | - Authentication/authorization is client responsibility
345 | - Access control must be implemented by MCP client
346 | - Audit logging of MCP client usage recommended
347 | 
348 | ⚠️ **Corpus Content**
349 | - Corpus contains regulatory guidance, not sensitive data
350 | - No customer data, financial data, or PII in corpus
351 | - Corpus is public within organization
352 | 
353 | ### Dependency Security
354 | 
355 | ✅ **Production dependency audit:** `npm audit --omit=dev` reports 0 vulnerabilities.
356 | 
357 | ⚠️ **Development dependency audit:** full `npm audit` reports 5 moderate findings through the Vitest/Vite/esbuild development dependency tree.
358 | 
359 | **Recommendation:** Review the Vitest 4 upgrade path before production hardening. These findings are not present in the production dependency audit, but they should remain visible in release evidence.
360 | 
361 | ---
362 | 
363 | ## 9. Release Readiness Assessment
364 | 
365 | ### Baseline Controls for MCP Release Gate
366 | 
367 | The release readiness service uses the following 6 baseline controls for the MCP release gate:
368 | 
369 | 1. ✅ **RWA-RULE-001** - Rule Governance (BLOCKING)
370 | 2. ✅ **RWA-CALC-001** - Calculation Accuracy
371 | 3. ✅ **RWA-DATA-001** - Data Lineage
372 | 4. ✅ **RWA-AUDIT-001** - Audit Logging
373 | 5. ✅ **TEST-REG-001** - Regulatory Test Coverage
374 | 6. ✅ **REL-EVID-001** - Release Evidence Package
375 | 
376 | ### MCP Server Implementation Status
377 | 
378 | **For the MCP server itself:**
379 | 
380 | - ✅ **RWA-RULE-001** - Corpus includes rule governance regulation (INTERNAL_RULE_GOVERNANCE)
381 | - ✅ **RWA-CALC-001** - Not applicable (MCP provides guidance, does not calculate RWA)
382 | - ✅ **RWA-DATA-001** - Corpus includes data lineage regulation (BCBS239)
383 | - ✅ **RWA-DQ-001** - Corpus includes data quality controls
384 | - ✅ **RWA-AUDIT-001** - Corpus includes audit logging controls
385 | - ✅ **RWA-RECON-001** - Corpus includes reconciliation controls
386 | - ✅ **RWA-REPORT-001** - Corpus includes reporting controls
387 | 
388 | ### Evidence Collected
389 | 
390 | - ✅ Build log (clean compilation)
391 | - ✅ Test results (94 tests passing)
392 | - ✅ Docker build log (successful multi-stage build)
393 | - ✅ Compose smoke output (service starts STDIO MCP server)
394 | - ✅ Tool contracts (15 tools documented)
395 | - ✅ Corpus inventory (9 regulations, 15 controls)
396 | - ✅ Release readiness document (this file)
397 | 
398 | ### Blocking Gaps: NONE
399 | 
400 | All technical requirements are met. The MCP server is ready for:
401 | 
402 | 1. **Compliance Review** - Verify corpus content aligns with organizational policies
403 | 2. **Legal Review** - Confirm disclaimers and limitations are appropriate
404 | 3. **Risk Review** - Assess operational risk of deployment
405 | 4. **Security Review** - Validate security posture and dependency vulnerabilities
406 | 
407 | ---
408 | 
409 | ## 10. Sign-Off Requirements
410 | 
411 | Before production deployment, the following sign-offs are **REQUIRED:**
412 | 
413 | ### Technical Sign-Off
414 | 
415 | - [ ] **Engineering Lead** - Code quality, test coverage, build process
416 | - [ ] **Security Team** - Security posture, dependency vulnerabilities, access control
417 | - [ ] **DevOps/SRE** - Deployment process, monitoring, incident response
418 | 
419 | ### Regulatory Sign-Off
420 | 
421 | - [ ] **Compliance Officer** - Corpus content accuracy, regulatory alignment
422 | - [ ] **Legal Counsel** - Disclaimers, limitations, liability considerations
423 | - [ ] **Risk Management** - Operational risk assessment, control effectiveness
424 | - [ ] **Internal Audit** - Evidence collection, audit trail, control testing
425 | 
426 | ### Deployment Approval
427 | 
428 | - [ ] **Product Owner** - Business value, user acceptance
429 | - [ ] **CTO/CIO** - Strategic alignment, technical architecture
430 | 
431 | ---
432 | 
433 | ## 11. Deployment Checklist
434 | 
435 | ### Pre-Deployment
436 | 
437 | - [ ] All sign-offs obtained
438 | - [ ] npm audit findings reviewed and addressed
439 | - [ ] MCP client authentication/authorization configured
440 | - [ ] Access control policies defined
441 | - [ ] Monitoring and alerting configured
442 | - [ ] Incident response plan documented
443 | 
444 | ### Deployment
445 | 
446 | - [ ] Docker image pushed to registry
447 | - [ ] Deployment manifest reviewed
448 | - [ ] Rollback plan documented
449 | - [ ] Deployment executed
450 | - [ ] Health check verified
451 | 
452 | ### Post-Deployment
453 | 
454 | - [ ] MCP client integration tested
455 | - [ ] Tool calls validated end-to-end
456 | - [ ] Monitoring dashboards reviewed
457 | - [ ] User documentation published
458 | - [ ] Training materials provided
459 | 
460 | ---
461 | 
462 | ## 12. Contact Information
463 | 
464 | ### Technical Support
465 | 
466 | - **Repository:** `/Users/pawel/ai_projects/risk-trace-control-tower/mcps/regulatory_mcp`
467 | - **Documentation:** `README.md`, `docs/`
468 | - **Issues:** Internal issue tracker
469 | 
470 | ### Regulatory Support
471 | 
472 | - **Compliance Team:** [Contact compliance team]
473 | - **Legal Team:** [Contact legal team]
474 | - **Risk Team:** [Contact risk team]
475 | 
476 | ---
477 | 
478 | ## 13. Appendices
479 | 
480 | ### A. Quality Gate Commands
481 | 
482 | ```bash
483 | # Install dependencies
484 | npm ci
485 | 
486 | # Build TypeScript
487 | npm run build
488 | 
489 | # Run tests
490 | npm test
491 | 
492 | # Build Docker image
493 | docker build -t bank-regulatory-controls-mcp .
494 | 
495 | # Build with Docker Compose
496 | docker compose -f mcps/docker-compose.yml build bank-regulatory-controls-mcp
497 | 
498 | # Smoke run with Docker Compose
499 | docker compose -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp
500 | ```
501 | 
502 | ### B. Evidence Files
503 | 
504 | - `build-log.txt` - TypeScript compilation output
505 | - `test-results.txt` - Test execution results
506 | - `docker-build.txt` - Docker build output
507 | - `compose-build.txt` - Docker Compose build output
508 | - `compose-run-output.txt` - Docker Compose startup smoke output
509 | - `production-audit.txt` - Production dependency audit output
510 | - `tool-contracts.json` - MCP tool contracts (15 tools)
511 | - `corpus-inventory.json` - Regulatory corpus inventory
512 | - `release-readiness.md` - This document
513 | 
514 | ### C. References
515 | 
516 | - **MCP Protocol:** https://modelcontextprotocol.io/
517 | - **BCBS 239:** Basel Committee on Banking Supervision
518 | - **CRR3/CRD6:** EU Capital Requirements Regulation/Directive
519 | - **DORA:** EU Digital Operational Resilience Act
520 | - **GDPR:** EU General Data Protection Regulation
521 | 
522 | ---
523 | 
524 | **Document Version:** 1.1  
525 | **Last Updated:** 2026-05-17T00:42:00+02:00  
526 | **Next Review:** Before production deployment
527 | 
528 | ---
529 | 
530 | ## ⚠️ FINAL REMINDER
531 | 
532 | **This MCP server provides engineering guidance only. All regulatory mappings, controls, evidence requirements, and release readiness decisions MUST be reviewed by qualified compliance, legal, or risk specialists before production use.**
533 | 
534 | **Do not deploy to production without obtaining all required sign-offs.**
</content>
</file>
<file><path>mcps/regulatory_mcp/docs/release-evidence/tool-contracts.json</path>
<content lines="1-448">
  1 | {
  2 |   "mcp_server": {
  3 |     "name": "@risk-trace/regulatory-mcp",
  4 |     "version": "0.1.0",
  5 |     "description": "MCP server for Bank Regulatory Controls / RWA Control Tower"
  6 |   },
  7 |   "tool_count": 15,
  8 |   "tools": [
  9 |     {
 10 |       "name": "health_check",
 11 |       "title": "Health Check",
 12 |       "description": "Return MCP server health, metadata, and optional corpus stats.",
 13 |       "input_parameters": {
 14 |         "include_corpus": {
 15 |           "type": "boolean",
 16 |           "required": false,
 17 |           "description": "Include corpus statistics in response"
 18 |         }
 19 |       },
 20 |       "annotations": {
 21 |         "readOnlyHint": true,
 22 |         "destructiveHint": false,
 23 |         "idempotentHint": true
 24 |       }
 25 |     },
 26 |     {
 27 |       "name": "get_regulatory_profile",
 28 |       "title": "Regulatory Profile",
 29 |       "description": "Return regulations, controls, and corpus stats filtered by domain or jurisdiction.",
 30 |       "input_parameters": {
 31 |         "domains": {
 32 |           "type": "array",
 33 |           "items": "string",
 34 |           "required": false,
 35 |           "description": "Filter by regulatory domains"
 36 |         },
 37 |         "jurisdiction": {
 38 |           "type": "string",
 39 |           "required": false,
 40 |           "description": "Filter by jurisdiction (e.g., EU, GLOBAL, INTERNAL)"
 41 |         }
 42 |       },
 43 |       "annotations": {
 44 |         "readOnlyHint": true,
 45 |         "destructiveHint": false,
 46 |         "idempotentHint": true
 47 |       }
 48 |     },
 49 |     {
 50 |       "name": "search_regulations",
 51 |       "title": "Search Regulations",
 52 |       "description": "Search regulations by query, domain, jurisdiction, and applies-to filters.",
 53 |       "input_parameters": {
 54 |         "query": {
 55 |           "type": "string",
 56 |           "required": false,
 57 |           "description": "Search query text"
 58 |         },
 59 |         "domains": {
 60 |           "type": "array",
 61 |           "items": "string",
 62 |           "required": false,
 63 |           "description": "Filter by domains"
 64 |         },
 65 |         "applies_to": {
 66 |           "type": "array",
 67 |           "items": "string",
 68 |           "required": false,
 69 |           "description": "Filter by applies-to categories"
 70 |         },
 71 |         "jurisdiction": {
 72 |           "type": "string",
 73 |           "required": false,
 74 |           "description": "Filter by jurisdiction"
 75 |         },
 76 |         "include_internal_policies": {
 77 |           "type": "boolean",
 78 |           "required": false,
 79 |           "description": "Include internal policies in results"
 80 |         },
 81 |         "limit": {
 82 |           "type": "number",
 83 |           "required": false,
 84 |           "description": "Maximum number of results"
 85 |         }
 86 |       },
 87 |       "annotations": {
 88 |         "readOnlyHint": true,
 89 |         "destructiveHint": false,
 90 |         "idempotentHint": true
 91 |       }
 92 |     },
 93 |     {
 94 |       "name": "match_controls",
 95 |       "title": "Match Controls",
 96 |       "description": "Match engineering controls for feature text, architecture text, code diffs, or release artifacts.",
 97 |       "input_parameters": {
 98 |         "text": {
 99 |           "type": "string",
100 |           "required": false,
101 |           "description": "Text to match controls against"
102 |         },
103 |         "artifact_type": {
104 |           "type": "string",
105 |           "required": false,
106 |           "description": "Type of artifact (feature, architecture, code_diff, release_readiness)"
107 |         },
108 |         "domains": {
109 |           "type": "array",
110 |           "items": "string",
111 |           "required": false,
112 |           "description": "Filter by domains"
113 |         },
114 |         "explicit_control_ids": {
115 |           "type": "array",
116 |           "items": "string",
117 |           "required": false,
118 |           "description": "Explicitly include these control IDs"
119 |         },
120 |         "excluded_control_ids": {
121 |           "type": "array",
122 |           "items": "string",
123 |           "required": false,
124 |           "description": "Exclude these control IDs"
125 |         },
126 |         "limit": {
127 |           "type": "number",
128 |           "required": false,
129 |           "description": "Maximum number of results"
130 |         }
131 |       },
132 |       "annotations": {
133 |         "readOnlyHint": true,
134 |         "destructiveHint": false,
135 |         "idempotentHint": true
136 |       }
137 |     },
138 |     {
139 |       "name": "review_feature_description",
140 |       "title": "Review Feature Description",
141 |       "description": "Review a regulated feature description for missing RWA controls and evidence.",
142 |       "input_parameters": {
143 |         "description": {
144 |           "type": "string",
145 |           "required": true,
146 |           "description": "Feature description text to review"
147 |         },
148 |         "domains": {
149 |           "type": "array",
150 |           "items": "string",
151 |           "required": false,
152 |           "description": "Regulatory domains to consider"
153 |         }
154 |       },
155 |       "annotations": {
156 |         "readOnlyHint": true,
157 |         "destructiveHint": false,
158 |         "idempotentHint": true
159 |       }
160 |     },
161 |     {
162 |       "name": "review_architecture_text",
163 |       "title": "Review Architecture Text",
164 |       "description": "Review architecture text for regulatory architecture gaps.",
165 |       "input_parameters": {
166 |         "architecture_text": {
167 |           "type": "string",
168 |           "required": true,
169 |           "description": "Architecture text to review"
170 |         },
171 |         "domains": {
172 |           "type": "array",
173 |           "items": "string",
174 |           "required": false,
175 |           "description": "Regulatory domains to consider"
176 |         }
177 |       },
178 |       "annotations": {
179 |         "readOnlyHint": true,
180 |         "destructiveHint": false,
181 |         "idempotentHint": true
182 |       }
183 |     },
184 |     {
185 |       "name": "review_code_diff",
186 |       "title": "Review Code Diff",
187 |       "description": "Review code diff text for hardcoded RWA logic, missing traceability, PII logging, and validation gaps.",
188 |       "input_parameters": {
189 |         "diff": {
190 |           "type": "string",
191 |           "required": true,
192 |           "description": "Code diff text to review"
193 |         },
194 |         "file_path": {
195 |           "type": "string",
196 |           "required": false,
197 |           "description": "File path for context"
198 |         }
199 |       },
200 |       "annotations": {
201 |         "readOnlyHint": true,
202 |         "destructiveHint": false,
203 |         "idempotentHint": true
204 |       }
205 |     },
206 |     {
207 |       "name": "generate_acceptance_criteria",
208 |       "title": "Generate Acceptance Criteria",
209 |       "description": "Generate deduplicated acceptance criteria mapped to controls.",
210 |       "input_parameters": {
211 |         "text": {
212 |           "type": "string",
213 |           "required": false,
214 |           "description": "Context text for generating criteria"
215 |         },
216 |         "artifact_type": {
217 |           "type": "string",
218 |           "required": false,
219 |           "description": "Type of artifact"
220 |         },
221 |         "domains": {
222 |           "type": "array",
223 |           "items": "string",
224 |           "required": false,
225 |           "description": "Regulatory domains"
226 |         },
227 |         "control_ids": {
228 |           "type": "array",
229 |           "items": "string",
230 |           "required": false,
231 |           "description": "Control IDs to generate criteria for"
232 |         }
233 |       },
234 |       "annotations": {
235 |         "readOnlyHint": true,
236 |         "destructiveHint": false,
237 |         "idempotentHint": true
238 |       }
239 |     },
240 |     {
241 |       "name": "generate_data_lineage_requirements",
242 |       "title": "Generate Data Lineage Requirements",
243 |       "description": "Generate RWA lineage fields, flow, and acceptance criteria.",
244 |       "input_parameters": {
245 |         "text": {
246 |           "type": "string",
247 |           "required": false,
248 |           "description": "Context text"
249 |         },
250 |         "control_ids": {
251 |           "type": "array",
252 |           "items": "string",
253 |           "required": false,
254 |           "description": "Control IDs to consider"
255 |         }
256 |       },
257 |       "annotations": {
258 |         "readOnlyHint": true,
259 |         "destructiveHint": false,
260 |         "idempotentHint": true
261 |       }
262 |     },
263 |     {
264 |       "name": "generate_audit_log_requirements",
265 |       "title": "Generate Audit Log Requirements",
266 |       "description": "Generate audit event requirements and secure logging notes.",
267 |       "input_parameters": {
268 |         "text": {
269 |           "type": "string",
270 |           "required": false,
271 |           "description": "Context text"
272 |         },
273 |         "control_ids": {
274 |           "type": "array",
275 |           "items": "string",
276 |           "required": false,
277 |           "description": "Control IDs to consider"
278 |         }
279 |       },
280 |       "annotations": {
281 |         "readOnlyHint": true,
282 |         "destructiveHint": false,
283 |         "idempotentHint": true
284 |       }
285 |     },
286 |     {
287 |       "name": "generate_test_obligations",
288 |       "title": "Generate Test Obligations",
289 |       "description": "Generate Given/When/Then regulatory test obligations.",
290 |       "input_parameters": {
291 |         "text": {
292 |           "type": "string",
293 |           "required": false,
294 |           "description": "Context text"
295 |         },
296 |         "artifact_type": {
297 |           "type": "string",
298 |           "required": false,
299 |           "description": "Type of artifact"
300 |         },
301 |         "domains": {
302 |           "type": "array",
303 |           "items": "string",
304 |           "required": false,
305 |           "description": "Regulatory domains"
306 |         },
307 |         "control_ids": {
308 |           "type": "array",
309 |           "items": "string",
310 |           "required": false,
311 |           "description": "Control IDs to generate obligations for"
312 |         }
313 |       },
314 |       "annotations": {
315 |         "readOnlyHint": true,
316 |         "destructiveHint": false,
317 |         "idempotentHint": true
318 |       }
319 |     },
320 |     {
321 |       "name": "assess_release_readiness",
322 |       "title": "Assess Release Readiness",
323 |       "description": "Assess RWA release readiness from implemented controls, evidence, and known findings.",
324 |       "input_parameters": {
325 |         "implemented_control_ids": {
326 |           "type": "array",
327 |           "items": "string",
328 |           "required": false,
329 |           "description": "IDs of implemented controls"
330 |         },
331 |         "evidence": {
332 |           "type": "array",
333 |           "items": "object",
334 |           "required": false,
335 |           "description": "Evidence artifacts collected"
336 |         },
337 |         "known_findings": {
338 |           "type": "array",
339 |           "items": "object",
340 |           "required": false,
341 |           "description": "Known findings or issues"
342 |         }
343 |       },
344 |       "annotations": {
345 |         "readOnlyHint": true,
346 |         "destructiveHint": false,
347 |         "idempotentHint": true
348 |       }
349 |     },
350 |     {
351 |       "name": "generate_regulatory_mapping_report",
352 |       "title": "Generate Regulatory Mapping Report",
353 |       "description": "Generate a Markdown regulatory mapping report with controls, evidence, tests, Bob actions, and human review note.",
354 |       "input_parameters": {
355 |         "title": {
356 |           "type": "string",
357 |           "required": false,
358 |           "description": "Report title"
359 |         },
360 |         "feature_text": {
361 |           "type": "string",
362 |           "required": false,
363 |           "description": "Feature description"
364 |         },
365 |         "domains": {
366 |           "type": "array",
367 |           "items": "string",
368 |           "required": false,
369 |           "description": "Regulatory domains"
370 |         },
371 |         "artifact_type": {
372 |           "type": "string",
373 |           "required": false,
374 |           "description": "Type of artifact"
375 |         },
376 |         "implemented_control_ids": {
377 |           "type": "array",
378 |           "items": "string",
379 |           "required": false,
380 |           "description": "IDs of implemented controls"
381 |         },
382 |         "evidence": {
383 |           "type": "array",
384 |           "items": "object",
385 |           "required": false,
386 |           "description": "Evidence artifacts"
387 |         },
388 |         "known_findings": {
389 |           "type": "array",
390 |           "items": "object",
391 |           "required": false,
392 |           "description": "Known findings"
393 |         }
394 |       },
395 |       "annotations": {
396 |         "readOnlyHint": true,
397 |         "destructiveHint": false,
398 |         "idempotentHint": true
399 |       }
400 |     },
401 |     {
402 |       "name": "generate_rwa_run_evidence_requirements",
403 |       "title": "Generate RWA Run Evidence Requirements",
404 |       "description": "Generate the required evidence package for an RWA calculation run.",
405 |       "input_parameters": {
406 |         "text": {
407 |           "type": "string",
408 |           "required": false,
409 |           "description": "Context text"
410 |         },
411 |         "control_ids": {
412 |           "type": "array",
413 |           "items": "string",
414 |           "required": false,
415 |           "description": "Control IDs to consider"
416 |         }
417 |       },
418 |       "annotations": {
419 |         "readOnlyHint": true,
420 |         "destructiveHint": false,
421 |         "idempotentHint": true
422 |       }
423 |     },
424 |     {
425 |       "name": "explain_control",
426 |       "title": "Explain Control",
427 |       "description": "Explain a control with developer tasks, common mistakes, evidence, and source references.",
428 |       "input_parameters": {
429 |         "control_id": {
430 |           "type": "string",
431 |           "required": true,
432 |           "description": "Control ID to explain"
433 |         }
434 |       },
435 |       "annotations": {
436 |         "readOnlyHint": true,
437 |         "destructiveHint": false,
438 |         "idempotentHint": true
439 |       }
440 |     }
441 |   ],
442 |   "notes": [
443 |     "All tools are read-only, non-destructive, and idempotent",
444 |     "All tools return both text content and structured JSON content",
445 |     "All tools include metadata, source references, and recommended actions",
446 |     "Tools advertise MCP input and output schemas; corpus files are validated at load time"
447 |   ]
448 | }
</content>
</file>
<file><path>mcps/regulatory_mcp/docs/release-evidence/corpus-inventory.json</path>
<content lines="1-372">
  1 | {
  2 |   "corpus_version": "0.1.0",
  3 |   "generated_at": "2026-05-16T22:50:00.561Z",
  4 |   "summary": {
  5 |     "total_regulations": 9,
  6 |     "total_controls": 15,
  7 |     "total_mappings": 3,
  8 |     "referential_integrity": "validated by corpus loader tests"
  9 |   },
 10 |   "regulations": {
 11 |     "count": 9,
 12 |     "items": [
 13 |       {
 14 |         "id": "BCBS239",
 15 |         "title": "BCBS 239 - Principles for effective risk data aggregation and risk reporting",
 16 |         "jurisdiction": "GLOBAL",
 17 |         "domains": [
 18 |           "data_quality",
 19 |           "reporting",
 20 |           "governance",
 21 |           "audit_trail"
 22 |         ],
 23 |         "requires_human_review": true
 24 |       },
 25 |       {
 26 |         "id": "CRR3",
 27 |         "title": "Capital Requirements Regulation III (CRR3) / CRD6",
 28 |         "jurisdiction": "EU",
 29 |         "domains": [
 30 |           "capital_adequacy",
 31 |           "credit_risk",
 32 |           "market_risk",
 33 |           "operational_risk",
 34 |           "reporting"
 35 |         ],
 36 |         "requires_human_review": true
 37 |       },
 38 |       {
 39 |         "id": "DORA",
 40 |         "title": "Digital Operational Resilience Act (DORA)",
 41 |         "jurisdiction": "EU",
 42 |         "domains": [
 43 |           "ict_security",
 44 |           "operational_risk",
 45 |           "governance",
 46 |           "testing"
 47 |         ],
 48 |         "requires_human_review": true
 49 |       },
 50 |       {
 51 |         "id": "EBA_ICT_SECURITY",
 52 |         "title": "EBA Guidelines on ICT and Security Risk Management",
 53 |         "jurisdiction": "EU",
 54 |         "domains": [
 55 |           "ict_security",
 56 |           "operational_risk",
 57 |           "governance",
 58 |           "data_protection"
 59 |         ],
 60 |         "requires_human_review": true
 61 |       },
 62 |       {
 63 |         "id": "EBA_REPORTING_4",
 64 |         "title": "EBA Reporting Framework 4.0",
 65 |         "jurisdiction": "EU",
 66 |         "domains": [
 67 |           "reporting",
 68 |           "data_quality",
 69 |           "audit_trail"
 70 |         ],
 71 |         "requires_human_review": true
 72 |       },
 73 |       {
 74 |         "id": "GDPR",
 75 |         "title": "General Data Protection Regulation (GDPR)",
 76 |         "jurisdiction": "EU",
 77 |         "domains": [
 78 |           "data_protection",
 79 |           "governance",
 80 |           "audit_trail",
 81 |           "ict_security"
 82 |         ],
 83 |         "requires_human_review": true
 84 |       },
 85 |       {
 86 |         "id": "INTERNAL_AUDIT_EVIDENCE",
 87 |         "title": "Internal Audit Evidence and Retention Policy",
 88 |         "jurisdiction": "INTERNAL",
 89 |         "domains": [
 90 |           "audit_trail",
 91 |           "governance",
 92 |           "data_quality"
 93 |         ],
 94 |         "requires_human_review": false
 95 |       },
 96 |       {
 97 |         "id": "INTERNAL_RULE_GOVERNANCE",
 98 |         "title": "Internal Rule Governance and Change Management Policy",
 99 |         "jurisdiction": "INTERNAL",
100 |         "domains": [
101 |           "governance",
102 |           "audit_trail",
103 |           "data_quality"
104 |         ],
105 |         "requires_human_review": false
106 |       },
107 |       {
108 |         "id": "INTERNAL_SDLC",
109 |         "title": "Internal Secure Software Development Lifecycle Policy",
110 |         "jurisdiction": "INTERNAL",
111 |         "domains": [
112 |           "governance",
113 |           "testing",
114 |           "ict_security",
115 |           "audit_trail"
116 |         ],
117 |         "requires_human_review": false
118 |       }
119 |     ],
120 |     "by_jurisdiction": {
121 |       "GLOBAL": 1,
122 |       "EU": 5,
123 |       "INTERNAL": 3
124 |     },
125 |     "requiring_human_review": 6
126 |   },
127 |   "controls": {
128 |     "count": 15,
129 |     "items": [
130 |       {
131 |         "id": "ARCH-ADR-001",
132 |         "title": "Architecture Decision Records",
133 |         "severity": "medium",
134 |         "domains": [
135 |           "architecture",
136 |           "governance"
137 |         ],
138 |         "required_evidence_count": 1,
139 |         "acceptance_criteria_count": 1,
140 |         "test_obligations_count": 1
141 |       },
142 |       {
143 |         "id": "DORA-ICT-001",
144 |         "title": "ICT Resilience Testing",
145 |         "severity": "high",
146 |         "domains": [
147 |           "ict_security",
148 |           "testing",
149 |           "operational_risk"
150 |         ],
151 |         "required_evidence_count": 1,
152 |         "acceptance_criteria_count": 1,
153 |         "test_obligations_count": 1
154 |       },
155 |       {
156 |         "id": "PERF-RWA-001",
157 |         "title": "RWA Calculation Performance",
158 |         "severity": "medium",
159 |         "domains": [
160 |           "performance",
161 |           "capital_adequacy"
162 |         ],
163 |         "required_evidence_count": 1,
164 |         "acceptance_criteria_count": 1,
165 |         "test_obligations_count": 1
166 |       },
167 |       {
168 |         "id": "REL-EVID-001",
169 |         "title": "Release Evidence Package",
170 |         "severity": "critical",
171 |         "domains": [
172 |           "governance",
173 |           "audit_trail"
174 |         ],
175 |         "required_evidence_count": 3,
176 |         "acceptance_criteria_count": 1,
177 |         "test_obligations_count": 1
178 |       },
179 |       {
180 |         "id": "RWA-AUDIT-001",
181 |         "title": "Calculation Audit Trail and Traceability",
182 |         "severity": "critical",
183 |         "domains": [
184 |           "audit_trail",
185 |           "capital_adequacy"
186 |         ],
187 |         "required_evidence_count": 2,
188 |         "acceptance_criteria_count": 2,
189 |         "test_obligations_count": 1
190 |       },
191 |       {
192 |         "id": "RWA-CALC-001",
193 |         "title": "RWA Calculation Accuracy and Traceability",
194 |         "severity": "critical",
195 |         "domains": [
196 |           "capital_adequacy",
197 |           "credit_risk",
198 |           "audit_trail"
199 |         ],
200 |         "required_evidence_count": 3,
201 |         "acceptance_criteria_count": 3,
202 |         "test_obligations_count": 2
203 |       },
204 |       {
205 |         "id": "RWA-DATA-001",
206 |         "title": "Input Data Completeness and Validation",
207 |         "severity": "high",
208 |         "domains": [
209 |           "data_quality",
210 |           "credit_risk"
211 |         ],
212 |         "required_evidence_count": 2,
213 |         "acceptance_criteria_count": 2,
214 |         "test_obligations_count": 1
215 |       },
216 |       {
217 |         "id": "RWA-DQ-001",
218 |         "title": "Data Quality Flags and Error Handling",
219 |         "severity": "high",
220 |         "domains": [
221 |           "data_quality",
222 |           "audit_trail"
223 |         ],
224 |         "required_evidence_count": 1,
225 |         "acceptance_criteria_count": 1,
226 |         "test_obligations_count": 1
227 |       },
228 |       {
229 |         "id": "RWA-RECON-001",
230 |         "title": "RWA Calculation Reconciliation",
231 |         "severity": "high",
232 |         "domains": [
233 |           "capital_adequacy",
234 |           "data_quality",
235 |           "audit_trail"
236 |         ],
237 |         "required_evidence_count": 1,
238 |         "acceptance_criteria_count": 1,
239 |         "test_obligations_count": 1
240 |       },
241 |       {
242 |         "id": "RWA-REPORT-001",
243 |         "title": "Regulatory Report Validation and Submission",
244 |         "severity": "critical",
245 |         "domains": [
246 |           "reporting",
247 |           "audit_trail"
248 |         ],
249 |         "required_evidence_count": 2,
250 |         "acceptance_criteria_count": 1,
251 |         "test_obligations_count": 1
252 |       },
253 |       {
254 |         "id": "RWA-RULE-001",
255 |         "title": "Regulatory Rule Version Control and Change Management",
256 |         "severity": "critical",
257 |         "domains": [
258 |           "governance",
259 |           "audit_trail",
260 |           "data_quality"
261 |         ],
262 |         "required_evidence_count": 3,
263 |         "acceptance_criteria_count": 2,
264 |         "test_obligations_count": 1
265 |       },
266 |       {
267 |         "id": "SEC-ACCESS-001",
268 |         "title": "Access Control and Authentication",
269 |         "severity": "critical",
270 |         "domains": [
271 |           "ict_security",
272 |           "governance"
273 |         ],
274 |         "required_evidence_count": 1,
275 |         "acceptance_criteria_count": 1,
276 |         "test_obligations_count": 1
277 |       },
278 |       {
279 |         "id": "SEC-INPUT-001",
280 |         "title": "Input Validation and Sanitization",
281 |         "severity": "critical",
282 |         "domains": [
283 |           "ict_security",
284 |           "data_quality"
285 |         ],
286 |         "required_evidence_count": 2,
287 |         "acceptance_criteria_count": 2,
288 |         "test_obligations_count": 1
289 |       },
290 |       {
291 |         "id": "SEC-LOG-001",
292 |         "title": "Secure Logging and Sensitive Data Protection",
293 |         "severity": "high",
294 |         "domains": [
295 |           "ict_security",
296 |           "data_protection",
297 |           "audit_trail"
298 |         ],
299 |         "required_evidence_count": 2,
300 |         "acceptance_criteria_count": 1,
301 |         "test_obligations_count": 1
302 |       },
303 |       {
304 |         "id": "TEST-REG-001",
305 |         "title": "Regulatory Test Coverage",
306 |         "severity": "high",
307 |         "domains": [
308 |           "testing",
309 |           "governance"
310 |         ],
311 |         "required_evidence_count": 1,
312 |         "acceptance_criteria_count": 1,
313 |         "test_obligations_count": 1
314 |       }
315 |     ],
316 |     "by_severity": {
317 |       "medium": 2,
318 |       "high": 6,
319 |       "critical": 7
320 |     },
321 |     "by_domain": {
322 |       "architecture": 1,
323 |       "governance": 5,
324 |       "ict_security": 4,
325 |       "testing": 2,
326 |       "operational_risk": 1,
327 |       "performance": 1,
328 |       "capital_adequacy": 4,
329 |       "audit_trail": 8,
330 |       "credit_risk": 2,
331 |       "data_quality": 5,
332 |       "reporting": 1,
333 |       "data_protection": 1
334 |     }
335 |   },
336 |   "mappings": {
337 |     "count": 3,
338 |     "types": [
339 |       {
340 |         "file": "artifact-type-to-controls.json",
341 |         "description": "Maps artifact types (feature, code diff, architecture, release) to relevant engineering controls",
342 |         "mapping_count": 10,
343 |         "validated": true
344 |       },
345 |       {
346 |         "file": "domain-to-regulations.json",
347 |         "description": "Maps regulatory domains to relevant regulations",
348 |         "mapping_count": 14,
349 |         "validated": true
350 |       },
351 |       {
352 |         "file": "keywords-to-controls.json",
353 |         "description": "Maps keywords found in code, commits, or artifacts to relevant engineering controls",
354 |         "mapping_count": 32,
355 |         "validated": true
356 |       }
357 |     ]
358 |   },
359 |   "validation": {
360 |     "duplicate_ids_check": "covered by corpusLoader.test.ts",
361 |     "dangling_references_check": "covered by corpusLoader.test.ts",
362 |     "schema_validation": "covered by corpusLoader.test.ts and schemas.test.ts",
363 |     "referential_integrity": "passed in npm test"
364 |   },
365 |   "notes": [
366 |     "All regulations and controls are loaded and validated by the corpus loader.",
367 |     "Referential integrity is enforced for mappings and control regulatory basis references.",
368 |     "Duplicate regulation and control IDs are rejected during corpus loading.",
369 |     "6 out of 9 regulations require human review before production use.",
370 |     "7 out of 15 controls are marked critical in the corpus."
371 |   ]
372 | }
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:37:07.179Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.83

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Pending |
| 2 | Create release-evidence directory | Pending |
| 3 | Generate tool-contracts.json from MCP tool definitions | Pending |
| 4 | Generate corpus-inventory.json from corpus data | Pending |
| 5 | Run build and capture output | Pending |
| 6 | Run tests and capture output | Pending |
| 7 | Build Docker image and capture output | Pending |
| 8 | Create comprehensive release-readiness.md | Pending |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Explore regulatory_mcp directory structure
[x] Create release-evidence directory
[x] Generate tool-contracts.json from MCP tool definitions
[x] Generate corpus-inventory.json from corpus data
[x] Run build and capture output
[x] Run tests and capture output
[x] Build Docker image and capture output
[x] Create comprehensive release-readiness.md
[-] Use Atlassian MCP to create Confluence page with release evidence
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md,observability/agents-alerts.yaml,AGENTS.md,../../Pulpit/bob_task_may-17-2026_3-18-45-pm.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:37:10.424Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.99

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! I can see that MCP-019 has already been implemented with comprehensive release evidence. Now I need to use the Atlassian MCP to create a Confluence page with this release evidence. Let me first check what Confluence spaces are available.

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>getAccessibleAtlassianResources</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>

---

**User:**

[TASK RESUMPTION] Resuming task...
<environment_details>
# VSCode Visible Files
../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md

# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,../../Pulpit/bob tasks/bob_task_may-16-2026_11-54-41-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_2-54-23-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-00-03-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-04-34-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-08-40-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:43:33.936Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.15

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>


# Current Workspace Directory (/home/cezary/projects/risk-trace-control-tower) Files
.semgrepignore
.trivyignore
AGENTS.md
.agents/
.bob/
.codex/
.github/
apps/
apps/docker-compose.yml
apps/backend/.python-version
apps/backend/uv.lock
apps/backend/src/rwa_agents/observability.py
apps/backend/src/rwa_agents/py.typed
apps/backend/src/rwa_agents/schemas.py
apps/backend/src/rwa_agents/state.py
apps/backend/src/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/generate_preprod_rwa_dataset.py
apps/backend/src/rwa_calculator/nccr_mapping.csv
apps/backend/src/rwa_calculator/paths.py
apps/backend/src/rwa_calculator/preprod_core_info_1000.csv
apps/backend/src/rwa_calculator/preprod_country_info.csv
apps/backend/src/rwa_calculator/preprod_dataset_summary.json
apps/backend/src/rwa_calculator/py.typed
apps/backend/src/rwa_calculator/rwa_backend.py
apps/backend/src/rwa_calculator/rwa_pydantic_schemas.py
apps/backend/src/rwa_calculator/reference_data/manifest.json
apps/backend/src/rwa_calculator/reference_data/README.md
apps/backend/src/rwa_calculator/reference_data/bcbs/basel_iii_final_reforms_2017.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/CH_FINMA_BASEL_III_FINAL/overlay.json
apps/backend/src/rwa_calculator/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/rwa_calculator/api_schemas.py
apps/backend/src/rwa_calculator/rwa_calculator/calculator.py
apps/backend/src/rwa_calculator/rwa_calculator/capital_models.py
apps/backend/src/rwa_calculator/rwa_calculator/capital.py
apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py
apps/backend/src/rwa_calculator/rwa_calculator/models.py
apps/backend/src/rwa_calculator/rwa_calculator/normal_distribution.py
apps/backend/src/rwa_calculator/rwa_calculator/pandera_validation.py
apps/backend/src/rwa_calculator/rwa_calculator/reference.py
apps/backend/src/rwa_calculator/rwa_calculator/server.py
apps/backend/src/rwa_common/__init__.py
apps/backend/src/rwa_common/db.py
apps/backend/src/rwa_common/py.typed
apps/backend/src/rwa_dashboard/py.typed
apps/backend/src/rwa_dashboard/repositories.py
apps/backend/src/rwa_dashboard/schemas.py
apps/backend/src/rwa_forecast_service/__init__.py
apps/backend/src/rwa_forecast_service/cli.py
apps/backend/src/rwa_forecast_service/engine.py
apps/backend/src/rwa_forecast_service/fastapi_app.py
apps/backend/src/rwa_forecast_service/py.typed
apps/backend/src/rwa_forecast_service/schemas.py
apps/backend/src/rwa_projection_service/__init__.py
apps/backend/src/rwa_projection_service/calendar.py
apps/backend/src/rwa_projection_service/cli.py
apps/backend/src/rwa_projection_service/engine.py
apps/backend/src/rwa_projection_service/fastapi_app.py
apps/backend/src/rwa_projection_service/py.typed
apps/backend/src/rwa_projection_service/schemas.py
apps/backend/src/rwa_rats_service/__init__.py
apps/backend/src/rwa_rats_service/cli.py
apps/backend/src/rwa_rats_service/engine.py
apps/backend/src/rwa_rats_service/fastapi_app.py
apps/backend/src/rwa_rats_service/py.typed
apps/backend/src/rwa_rats_service/schemas.py
apps/backend/src/rwa_steering/cli.py
apps/backend/src/rwa_steering/input_package.py
apps/backend/src/rwa_steering/py.typed
apps/backend/src/rwa_steering/scenarios.py
apps/backend/src/rwa_steering/schemas.py
apps/backend/tests/dashboard/test_dashboard_data.py
apps/backend/tests/forecast/test_forecast_service.py
apps/backend/tests/rats/test_rats_service.py
apps/frontend/.dockerignore
apps/frontend/.env.example
apps/frontend/.gitignore
apps/frontend/Dockerfile
apps/frontend/index.html
apps/frontend/nginx.conf
apps/frontend/package.json
apps/frontend/playwright.config.ts
apps/frontend/README.md
apps/frontend/tsconfig.json
apps/frontend/tsconfig.node.json
apps/frontend/vite.config.ts
apps/frontend/scripts/playwright-web-server.mjs
apps/frontend/src/App.tsx
apps/frontend/src/main.tsx
apps/frontend/src/navigation.ts
apps/frontend/src/vite-env.d.ts
apps/frontend/src/api/client.ts
apps/frontend/src/api/rwaApi.ts
apps/frontend/src/api/rwaDashboardApi.ts
apps/frontend/src/api/types.ts
apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx
apps/frontend/src/components/rwa-briefing/BriefingInsightCards.tsx
apps/frontend/src/components/rwa-briefing/BriefingKpiStrip.tsx
apps/frontend/src/components/rwa-briefing/EvidenceTraceabilityCard.tsx
apps/frontend/src/components/rwa-briefing/ManagementReviewPackCard.tsx
apps/frontend/src/components/rwa-briefing/RwaMovementAttributionCard.tsx
apps/frontend/src/components/rwa-dashboard/AlertsPanel.tsx
apps/frontend/src/components/rwa-dashboard/AppShell.tsx
apps/frontend/src/components/rwa-dashboard/CapitalSummaryCard.tsx
apps/frontend/src/components/rwa-dashboard/Card.tsx
apps/frontend/src/components/rwa-dashboard/CountryMapCard.tsx
apps/frontend/src/components/rwa-dashboard/ExposureDonutCard.tsx
apps/frontend/src/components/rwa-dashboard/FilterBar.tsx
apps/frontend/src/components/rwa-dashboard/MetricCard.tsx
apps/frontend/src/components/rwa-dashboard/PageHeader.tsx
apps/frontend/src/components/rwa-dashboard/RatingBarsCard.tsx
apps/frontend/src/components/rwa-dashboard/RwaTrendCard.tsx
apps/frontend/src/components/rwa-dashboard/Sidebar.tsx
apps/frontend/src/components/rwa-dashboard/StatusBadge.tsx
apps/frontend/src/components/rwa-dashboard/Toast.tsx
apps/frontend/src/components/rwa-dashboard/TopBar.tsx
apps/frontend/src/components/rwa-dashboard/TopExposuresCard.tsx
apps/frontend/src/components/rwa-lineage/LineageFlowCard.tsx
apps/frontend/src/components/rwa-lineage/LineageSideRail.tsx
apps/frontend/src/components/rwa-lineage/LineageSummaryCard.tsx
apps/frontend/src/components/rwa-lineage/TransformationStepsCard.tsx
apps/frontend/src/hooks/iconHydration.ts
apps/frontend/src/hooks/useApiResource.ts
apps/frontend/src/hooks/useAppContextData.ts
apps/frontend/src/hooks/useNotificationsData.ts
apps/frontend/src/hooks/useRwaBriefingData.ts
apps/frontend/src/hooks/useRwaDashboardData.ts
apps/frontend/src/hooks/useRwaLineageData.ts
apps/frontend/src/hooks/useToast.ts
apps/frontend/src/hooks/useUiActions.ts
apps/frontend/src/pages/DataLineagePage.tsx
apps/frontend/src/pages/HomePage.tsx
apps/frontend/src/pages/RwaDashboardPage.tsx
apps/frontend/src/pages/RwaIntelligenceBriefingPage.tsx
apps/frontend/src/styles/rwa-dashboard.css
bob_sessions/
bob_sessions/bob_task_may-16-2026_3-42-58-pm.md
bob_sessions/bob_task_may-16-2026_3-42-58-pm.png
bob_sessions/bob_task_may-16-2026_5-49-33-pm.md
bob_sessions/bob_task_may-16-2026_5-49-33-pm.md.png
bob_sessions/bob_task_may-16-2026_6-24-03-pm.md
bob_sessions/bob_task_may-16-2026_6-24-03-pm.png
bob_sessions/bob_task_may-16-2026_6-44-37-pm.md
bob_sessions/bob_task_may-16-2026_6-44-37-pm.png
bob_sessions/bob_task_may-16-2026_7-26-23-pm.md
bob_sessions/bob_task_may-16-2026_7-26-23-pm.png
bob_sessions/bob_task_may-16-2026_9-41-56-pm.md
bob_sessions/bob_task_may-16-2026_9-41-56-pm.png
bob_sessions/bob_task_may-16-2026_10-44-03-pm.md
bob_sessions/bob_task_may-16-2026_10-44-03-pm.png
bob_sessions/bob_task_may-16-2026_11-27-12-pm.md
bob_sessions/bob_task_may-16-2026_11-27-12-pm.png
bob_sessions/bob_task_may-16-2026_11-54-41-pm.md
bob_sessions/bob_task_may-16-2026_11-54-41-pm.png
bob_sessions/bob_task_may-17-2026_1-03-09-am.md
bob_sessions/bob_task_may-17-2026_1-03-09-am.png
bob_sessions/bob_task_may-17-2026_1-25-46-am.md
bob_sessions/bob_task_may-17-2026_1-25-46-am.png
bob_sessions/bob_task_may-17-2026_2-19-23-am.md
bob_sessions/bob_task_may-17-2026_2-19-23-am.png
bob_sessions/bob_task_may-17-2026_2-22-21-am.md
bob_sessions/bob_task_may-17-2026_2-22-21-am.png
bob_sessions/bob_task_may-17-2026_3-06-50-am.md
bob_sessions/bob_task_may-17-2026_3-06-50-am.png
bob_sessions/bob_task_may-17-2026_10-47-14-am.md
bob_sessions/bob_task_may-17-2026_10-47-14-am.png
bob_sessions/bob_task_may-17-2026_12-05-00-pm.md
bob_sessions/bob_task_may-17-2026_12-05-00-pm.png
bob_sessions/bob_task_may-17-2026_12-11-43-am.md
bob_sessions/bob_task_may-17-2026_12-11-43-am.png
bob_sessions/bob_task_may-17-2026_12-18-36-am.md
bob_sessions/bob_task_may-17-2026_12-18-36-am.png
bob_sessions/bob_task_may-17-2026_12-45-41-am.md
bob_sessions/bob_task_may-17-2026_12-45-41-am.png
bob_sessions/bob_task_may-17-2026_12-50-45-am.md
bob_sessions/bob_task_may-17-2026_12-50-45-am.png
docker/
docs/
infra/
k6/
k6/load-test.js
k6/smoke-test.js
k6/stress-test.js
k8s/
k8s/cert-manager/cluster-issuer-prod.yaml
k8s/cert-manager/cluster-issuer-staging.yaml
k8s/external-secrets/backend-externalsecret.yaml
k8s/external-secrets/clustersecretstore.yaml
k8s/external-secrets/install.sh
k8s/ingress/cert-manager-install.sh
k8s/ingress/rwa-ingress.yaml
k8s/opa/constraints/deny-latest-tag-constraint.yaml
k8s/opa/constraints/deny-privileged-constraint.yaml
k8s/opa/constraints/require-non-root-constraint.yaml
k8s/opa/constraints/require-resource-limits-constraint.yaml
k8s/opa/templates/deny-latest-tag.yaml
k8s/opa/templates/deny-privileged.yaml
k8s/opa/templates/require-non-root.yaml
mcps/
observability/
scripts/

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I can see the release evidence has already been created. Now I'll use the Atlassian MCP to create a Confluence page with this release evidence. Let me first get accessible Atlassian resources.

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>getAccessibleAtlassianResources</tool_name>
<arguments>
{}
</arguments>
</use_mcp_tool>

---

**User:**

[use_mcp_tool for 'atlassian'] Result:
[{"id":"46a0a7e8-68c6-4d23-a8e6-3ef8e6234578","url":"https://azenoca.atlassian.net","name":"azenoca","scopes":["read:jira-work","write:jira-work"],"avatarUrl":"https://site-admin-avatar-cdn.prod.public.atl-paas.net/avatars/240/rocket.png"}]
<environment_details>
# VSCode Visible Files
../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md

# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,../../Pulpit/bob tasks/bob_task_may-16-2026_11-54-41-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_2-54-23-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-00-03-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-04-34-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-08-40-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:43:39.673Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.32

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Good! I have access to the Atlassian instance. Now let me get the available Confluence spaces.

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>getConfluenceSpaces</tool_name>
<arguments>
{
  "cloudId": "azenoca.atlassian.net"
}
</arguments>
</use_mcp_tool>

---

**User:**

[use_mcp_tool for 'atlassian'] Result:
Error:
{"error":true,"message":"Failed to get spaces: 404 Not Found. Details: {\n  \"timestamp\": \"2026-05-17T13:43:49.519938135Z\",\n  \"status\": 404,\n  \"error\": \"Not Found\",\n  \"message\": \"No message available\",\n  \"path\": \"/ex/confluence/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/wiki/api/v2/spaces\"\n}"}
<environment_details>
# VSCode Visible Files
../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md

# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,../../Pulpit/bob tasks/bob_task_may-16-2026_11-54-41-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_2-54-23-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-00-03-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-04-34-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-08-40-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:43:49.582Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.49

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

I see that the Atlassian instance doesn't have Confluence enabled (only Jira scopes are available). Let me create a Jira issue instead to document the release evidence, which is a common practice for release management.

First, let me search for available Jira projects:

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>getVisibleJiraProjects</tool_name>
<arguments>
{
  "cloudId": "azenoca.atlassian.net"
}
</arguments>
</use_mcp_tool>

---

**User:**

[use_mcp_tool for 'atlassian'] Result:
{
  "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/project/search?expand=issueTypes&maxResults=50&action=create&startAt=0",
  "maxResults": 50,
  "startAt": 0,
  "total": 1,
  "isLast": true,
  "values": [
    {
      "expand": "description,lead,issueTypes,url,projectKeys,permissions,insight",
      "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/project/10033",
      "id": "10033",
      "key": "RCT",
      "issueTypes": [
        {
          "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/issuetype/10039",
          "id": "10039",
          "description": "Mała, wyodrębniona część pracy.",
          "iconUrl": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/2/universal_avatar/view/type/issuetype/avatar/10318?size=medium",
          "name": "Zadanie",
          "subtask": false,
          "avatarId": 10318,
          "hierarchyLevel": 0
        },
        {
          "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/issuetype/10040",
          "id": "10040",
          "description": "Problem lub błąd.",
          "iconUrl": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/2/universal_avatar/view/type/issuetype/avatar/10303?size=medium",
          "name": "Błąd w programie",
          "subtask": false,
          "avatarId": 10303,
          "hierarchyLevel": 0
        },
        {
          "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/issuetype/10041",
          "id": "10041",
          "description": "Funkcja lub cecha wyrażona jako cel użytkownika.",
          "iconUrl": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/2/universal_avatar/view/type/issuetype/avatar/10315?size=medium",
          "name": "Story",
          "subtask": false,
          "avatarId": 10315,
          "hierarchyLevel": 0
        },
        {
          "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/issuetype/10042",
          "id": "10042",
          "description": "Epiki śledzą kolekcje powiązanych błędów, historii i zadań.",
          "iconUrl": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/2/universal_avatar/view/type/issuetype/avatar/10307?size=medium",
          "name": "Epik",
          "subtask": false,
          "avatarId": 10307,
          "hierarchyLevel": 1
        },
        {
          "self": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/issuetype/10043",
          "id": "10043",
          "description": "Podzadania śledzą małe elementy, które są częścią większego zadania.",
          "iconUrl": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/2/universal_avatar/view/type/issuetype/avatar/10316?size=medium",
          "name": "Podzadanie",
          "subtask": true,
          "avatarId": 10316,
          "hierarchyLevel": -1
        }
      ],
      "name": "RiskTrace Control Tower",
      "avatarUrls": {
        "48x48": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/universal_avatar/view/type/project/avatar/10410",
        "24x24": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/universal_avatar/view/type/project/avatar/10410?size=small",
        "16x16": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/universal_avatar/view/type/project/avatar/10410?size=xsmall",
        "32x32": "https://api.atlassian.com/ex/jira/46a0a7e8-68c6-4d23-a8e6-3ef8e6234578/rest/api/3/universal_avatar/view/type/project/avatar/10410?size=medium"
      },
      "projectTypeKey": "software",
      "simplified": true,
      "style": "next-gen",
      "isPrivate": false,
      "properties": {},
      "entityId": "a0dd8114-d131-4032-b515-1d644985b6bd",
      "uuid": "a0dd8114-d131-4032-b515-1d644985b6bd"
    }
  ]
}
<environment_details>
# VSCode Visible Files
../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md

# VSCode Open Tabs
apps/backend/src/rwa_agents/schemas.py,apps/backend/src/rwa_agents/guardrails.py,apps/backend/src/rwa_agents/retry.py,apps/backend/src/rwa_agents/prompts.py,apps/backend/src/rwa_agents/workflow.py,apps/backend/Dockerfile,apps/backend/src/rwa_agents/cache.py,apps/backend/src/rwa_agents/tools.py,apps/backend/tests/agents/test_chaos.py,apps/backend/tests/agents/test_performance.py,../../Pulpit/bob tasks/bob_task_may-16-2026_11-54-41-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_2-54-23-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-00-03-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-04-34-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-08-40-pm.md,../../Pulpit/bob tasks/bob_task_may-17-2026_3-18-28-pm.md,apps/backend/src/rwa_agents/observability.py,docs/agents/RCT-AGENTS-IMPROVEMENTS.md,docs/agents/architecture.md,docs/agents/monitoring.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:43:54.909Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.67

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Perfect! I found the "RiskTrace Control Tower" (RCT) project. Now let me read the release readiness document to create a comprehensive Jira issue with the release evidence.

<read_file>
<args>
<file>
<path>mcps/regulatory_mcp/docs/release-evidence/release-readiness.md</path>
<line_range>1-100</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 'mcps/regulatory_mcp/docs/release-evidence/release-readiness.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>mcps/regulatory_mcp/docs/release-evidence/release-readiness.md</path>
<content lines="1-100">
  1 | # Release Evidence Package: Bank Regulatory Controls MCP
  2 | 
  3 | **Version:** 0.1.0  
  4 | **Release Date:** 2026-05-17  
  5 | **Package Generated:** 2026-05-17T00:42:00+02:00
  6 | 
  7 | ---
  8 | 
  9 | ## ⚠️ HUMAN REVIEW REQUIRED
 10 | 
 11 | **IMPORTANT: This MCP server provides engineering guidance only.**
 12 | 
 13 | All regulatory mappings, controls, evidence requirements, and release readiness decisions **MUST be reviewed by qualified compliance, legal, or risk specialists** before production use.
 14 | 
 15 | **This tool does NOT provide:**
 16 | - Legal advice
 17 | - Regulatory compliance certification
 18 | - Substitute for qualified compliance review
 19 | - Guarantee of regulatory compliance
 20 | 
 21 | **All outputs from this MCP server require human validation by:**
 22 | - Compliance officers
 23 | - Legal counsel
 24 | - Risk management specialists
 25 | - Internal audit teams
 26 | 
 27 | ---
 28 | 
 29 | ## Executive Summary
 30 | 
 31 | ### Release Status: ✅ READY FOR COMPLIANCE REVIEW
 32 | 
 33 | The Bank Regulatory Controls MCP server has successfully passed all technical quality gates:
 34 | 
 35 | - ✅ **Build:** Clean TypeScript compilation
 36 | - ✅ **Tests:** 94 tests passing (11 test files)
 37 | - ✅ **Docker:** Multi-stage build successful
 38 | - ✅ **Corpus:** 9 regulations, 15 controls, validated referential integrity
 39 | - ✅ **MCP Protocol:** 15 tools registered with schemas and annotations
 40 | - ✅ **Runtime Security:** No external API calls, local-only operation, production dependency audit clean
 41 | 
 42 | ### Critical Blockers: NONE
 43 | 
 44 | All technical requirements are met. The system is ready for compliance, legal, and risk review.
 45 | 
 46 | ---
 47 | 
 48 | ## 1. MCP Tool Contracts
 49 | 
 50 | ### Tool Count: 15
 51 | 
 52 | All tools are **read-only, non-destructive, and idempotent**.
 53 | 
 54 | #### Core Tools
 55 | 
 56 | 1. **health_check** - Server health and corpus statistics
 57 | 2. **get_regulatory_profile** - Regulations and controls by domain/jurisdiction
 58 | 3. **search_regulations** - Search regulatory corpus
 59 | 4. **match_controls** - Match engineering controls to artifacts
 60 | 
 61 | #### Review Tools
 62 | 
 63 | 5. **review_feature_description** - Review feature for missing controls
 64 | 6. **review_architecture_text** - Review architecture for regulatory gaps
 65 | 7. **review_code_diff** - Review code for hardcoded logic, PII, validation gaps
 66 | 
 67 | #### Generation Tools
 68 | 
 69 | 8. **generate_acceptance_criteria** - Generate acceptance criteria from controls
 70 | 9. **generate_data_lineage_requirements** - Generate RWA lineage requirements
 71 | 10. **generate_audit_log_requirements** - Generate audit event requirements
 72 | 11. **generate_test_obligations** - Generate Given/When/Then test obligations
 73 | 12. **generate_rwa_run_evidence_requirements** - Generate RWA run evidence package
 74 | 
 75 | #### Release Tools
 76 | 
 77 | 13. **assess_release_readiness** - Assess release readiness from controls and evidence
 78 | 14. **generate_regulatory_mapping_report** - Generate Markdown regulatory report
 79 | 15. **explain_control** - Explain control with tasks and common mistakes
 80 | 
 81 | **Full tool contracts:** See `tool-contracts.json`
 82 | 
 83 | ---
 84 | 
 85 | ## 2. Regulatory Corpus Inventory
 86 | 
 87 | ### Summary
 88 | 
 89 | - **Regulations:** 9 (5 EU, 1 Global, 3 Internal)
 90 | - **Controls:** 15 (7 critical, 6 high, 2 medium)
 91 | - **Mappings:** 3 (keywords, artifacts, domains)
 92 | - **Validation:** All referential integrity checks passed
 93 | 
 94 | ### Regulations
 95 | 
 96 | #### External Regulations (6 require human review)
 97 | 
 98 | 1. **BCBS239** - Principles for effective risk data aggregation and risk reporting (GLOBAL)
 99 | 2. **CRR3** - Capital Requirements Regulation III / CRD6 (EU)
100 | 3. **DORA** - Digital Operational Resilience Act (EU)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
mcps/regulatory_mcp/docs/release-evidence/test-coverage-report.md

# VSCode Open Tabs
apps/backend/Dockerfile,apps/backend/tests/agents/test_performance.py,mcps/regulatory_mcp/test-docker-smoke.sh,mcps/regulatory_mcp/README.md,mcps/regulatory_mcp/docs/release-evidence/test-coverage-report.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:03:10.779Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.85

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>


# Current Workspace Directory (/home/cezary/projects/risk-trace-control-tower) Files
.agents/
.bob/
.codex/
.github/
apps/
apps/docker-compose.yml
apps/backend/.dockerignore
apps/backend/.env.example
apps/backend/.gitignore
apps/backend/.python-version
apps/backend/Dockerfile
apps/backend/pyproject.toml
apps/backend/README.md
apps/backend/uv.lock
apps/backend/src/rwa_agents/__init__.py
apps/backend/src/rwa_agents/api.py
apps/backend/src/rwa_agents/cache.py
apps/backend/src/rwa_agents/checkpointing.py
apps/backend/src/rwa_agents/config.py
apps/backend/src/rwa_agents/guardrails.py
apps/backend/src/rwa_agents/observability.py
apps/backend/src/rwa_agents/privacy.py
apps/backend/src/rwa_agents/prompts.py
apps/backend/src/rwa_agents/py.typed
apps/backend/src/rwa_agents/retry.py
apps/backend/src/rwa_agents/schemas.py
apps/backend/src/rwa_agents/state.py
apps/backend/src/rwa_agents/tools.py
apps/backend/src/rwa_agents/validation.py
apps/backend/src/rwa_agents/watsonx.py
apps/backend/src/rwa_agents/workflow.py
apps/backend/src/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/generate_preprod_rwa_dataset.py
apps/backend/src/rwa_calculator/nccr_mapping.csv
apps/backend/src/rwa_calculator/paths.py
apps/backend/src/rwa_calculator/preprod_core_info_1000.csv
apps/backend/src/rwa_calculator/preprod_country_info.csv
apps/backend/src/rwa_calculator/preprod_dataset_summary.json
apps/backend/src/rwa_calculator/py.typed
apps/backend/src/rwa_calculator/rwa_backend.py
apps/backend/src/rwa_calculator/rwa_pydantic_schemas.py
apps/backend/src/rwa_calculator/reference_data/manifest.json
apps/backend/src/rwa_calculator/reference_data/README.md
apps/backend/src/rwa_calculator/reference_data/bcbs/basel_iii_final_reforms_2017.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/CH_FINMA_BASEL_III_FINAL/overlay.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/EU_CRR3_EBA/overlay.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/UK_PRA_BASEL_3_1/overlay.json
apps/backend/src/rwa_calculator/rwa_calculator/__init__.py
apps/backend/src/rwa_calculator/rwa_calculator/api_schemas.py
apps/backend/src/rwa_calculator/rwa_calculator/calculator.py
apps/backend/src/rwa_calculator/rwa_calculator/capital_models.py
apps/backend/src/rwa_calculator/rwa_calculator/capital.py
apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py
apps/backend/src/rwa_calculator/rwa_calculator/models.py
apps/backend/src/rwa_calculator/rwa_calculator/normal_distribution.py
apps/backend/src/rwa_calculator/rwa_calculator/pandera_validation.py
apps/backend/src/rwa_calculator/rwa_calculator/reference.py
apps/backend/src/rwa_calculator/rwa_calculator/server.py
apps/backend/src/rwa_common/__init__.py
apps/backend/src/rwa_common/db.py
apps/backend/src/rwa_common/py.typed
apps/backend/src/rwa_dashboard/__init__.py
apps/backend/src/rwa_dashboard/api.py
apps/backend/src/rwa_dashboard/data.py
apps/backend/src/rwa_dashboard/models.py
apps/backend/src/rwa_dashboard/py.typed
apps/backend/src/rwa_dashboard/repositories.py
apps/backend/src/rwa_dashboard/schemas.py
apps/backend/src/rwa_dashboard/seed.py
apps/backend/src/rwa_dashboard/service.py
apps/backend/src/rwa_forecast_service/__init__.py
apps/backend/src/rwa_forecast_service/cli.py
apps/backend/src/rwa_forecast_service/engine.py
apps/backend/src/rwa_forecast_service/fastapi_app.py
apps/backend/src/rwa_forecast_service/py.typed
apps/backend/src/rwa_forecast_service/schemas.py
apps/backend/src/rwa_projection_service/__init__.py
apps/backend/src/rwa_projection_service/calendar.py
apps/backend/src/rwa_projection_service/cli.py
apps/backend/src/rwa_projection_service/engine.py
apps/backend/src/rwa_projection_service/fastapi_app.py
apps/backend/src/rwa_projection_service/py.typed
apps/backend/src/rwa_projection_service/schemas.py
apps/backend/src/rwa_rats_service/__init__.py
apps/backend/src/rwa_rats_service/cli.py
apps/backend/src/rwa_rats_service/engine.py
apps/backend/src/rwa_rats_service/fastapi_app.py
apps/backend/src/rwa_rats_service/py.typed
apps/backend/src/rwa_rats_service/schemas.py
apps/backend/src/rwa_steering/__init__.py
apps/backend/src/rwa_steering/cli.py
apps/backend/src/rwa_steering/engine.py
apps/backend/src/rwa_steering/errors.py
apps/backend/src/rwa_steering/fastapi_app.py
apps/backend/src/rwa_steering/input_package.py
apps/backend/src/rwa_steering/missing_inputs.py
apps/backend/src/rwa_steering/py.typed
apps/backend/src/rwa_steering/scenarios.py
apps/backend/src/rwa_steering/schemas.py
apps/backend/src/rwa_steering/transformations.py
apps/backend/src/rwa_steering/generated_inputs/capital_positions.csv
apps/backend/src/rwa_steering/generated_inputs/cva_hedges.csv
apps/backend/src/rwa_steering/generated_inputs/cva_netting_sets.csv
apps/backend/src/rwa_steering/generated_inputs/cva_portfolio_inputs.csv
apps/backend/src/rwa_steering/generated_inputs/data_quality_flags.csv
apps/backend/src/rwa_steering/generated_inputs/dlgd_scenario_assumptions.csv
apps/backend/src/rwa_steering/generated_inputs/forecast_calendar.csv
apps/backend/src/rwa_steering/generated_inputs/fx_scenario_rates.csv
apps/backend/src/rwa_steering/generated_inputs/leverage_exposures.csv
apps/backend/src/rwa_steering/generated_inputs/leverage_off_balance_sheet_items.csv
apps/backend/src/rwa_steering/generated_inputs/macro_regime_indicators.csv
apps/backend/src/rwa_steering/generated_inputs/manifest.json
apps/backend/src/rwa_steering/generated_inputs/operational_risk_business_indicators.csv
apps/backend/src/rwa_steering/generated_inputs/operational_risk_losses.csv
apps/backend/src/rwa_steering/generated_inputs/portfolio_strategy_limits.csv
apps/backend/src/rwa_steering/generated_inputs/profitability_inputs.csv
apps/backend/src/rwa_steering/generated_inputs/rating_migration_matrix.csv
apps/backend/src/rwa_steering/generated_inputs/README.md
apps/backend/src/rwa_steering/generated_inputs/regulatory_overlay_selection.csv
apps/backend/src/rwa_steering/generated_inputs/scenario_definitions.csv
apps/backend/src/rwa_steering/generated_inputs/segment_growth_assumptions.csv
apps/backend/src/rwa_steering/generated_inputs/steering_action_constraints.csv
apps/backend/src/rwa_steering/generated_inputs/validation_report.json
apps/backend/tests/agents/test_chaos.py
apps/backend/tests/agents/test_performance.py
apps/backend/tests/agents/test_validation.py
apps/backend/tests/calculator/test_golden_regression.py
apps/backend/tests/calculator/test_rwa_backend.py
apps/backend/tests/dashboard/test_dashboard_data.py
apps/backend/tests/dashboard/test_risktrace_rest_contract.py
apps/backend/tests/forecast/test_forecast_service.py
apps/backend/tests/projection/test_calendar.py
apps/backend/tests/projection/test_projection_service.py
apps/backend/tests/rats/test_rats_service.py
apps/backend/tests/steering/test_missing_inputs.py
apps/backend/tests/steering/test_steering_service.py
apps/frontend/.dockerignore
apps/frontend/.env.example
apps/frontend/.gitignore
apps/frontend/Dockerfile
apps/frontend/index.html
apps/frontend/nginx.conf
apps/frontend/package-lock.json
apps/frontend/package.json
apps/frontend/playwright.config.ts
apps/frontend/README.md
apps/frontend/public/risktrace-logo-sm.png
apps/frontend/public/risktrace-logo.png
apps/frontend/scripts/playwright-web-server.mjs
apps/frontend/src/App.tsx
apps/frontend/src/main.tsx
apps/frontend/src/navigation.ts
apps/frontend/src/api/client.ts
apps/frontend/src/api/rwaApi.ts
apps/frontend/src/api/rwaDashboardApi.ts
apps/frontend/src/api/types.ts
apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx
apps/frontend/src/components/rwa-briefing/BriefingInsightCards.tsx
apps/frontend/src/components/rwa-briefing/BriefingKpiStrip.tsx
apps/frontend/src/components/rwa-briefing/EvidenceTraceabilityCard.tsx
apps/frontend/src/components/rwa-briefing/ManagementReviewPackCard.tsx
apps/frontend/src/components/rwa-briefing/RwaMovementAttributionCard.tsx
apps/frontend/src/components/rwa-dashboard/AlertsPanel.tsx
apps/frontend/src/components/rwa-dashboard/AppShell.tsx
apps/frontend/src/components/rwa-dashboard/CapitalSummaryCard.tsx
apps/frontend/src/components/rwa-dashboard/Card.tsx
apps/frontend/src/components/rwa-dashboard/CountryMapCard.tsx
apps/frontend/src/components/rwa-dashboard/ExposureDonutCard.tsx
apps/frontend/src/components/rwa-dashboard/FilterBar.tsx
apps/frontend/src/components/rwa-dashboard/MetricCard.tsx
apps/frontend/src/components/rwa-dashboard/PageHeader.tsx
apps/frontend/src/components/rwa-dashboard/RatingBarsCard.tsx
apps/frontend/src/components/rwa-dashboard/RwaTrendCard.tsx
apps/frontend/src/components/rwa-dashboard/Sidebar.tsx
apps/frontend/src/components/rwa-dashboard/StatusBadge.tsx
apps/frontend/src/components/rwa-dashboard/Toast.tsx
apps/frontend/src/components/rwa-dashboard/TopBar.tsx
apps/frontend/src/components/rwa-dashboard/TopExposuresCard.tsx
apps/frontend/src/components/rwa-lineage/LineageFlowCard.tsx
apps/frontend/src/components/rwa-lineage/LineageSideRail.tsx
apps/frontend/src/components/rwa-lineage/LineageSummaryCard.tsx
apps/frontend/src/components/rwa-lineage/TransformationStepsCard.tsx
apps/frontend/src/hooks/iconHydration.ts
apps/frontend/src/hooks/useApiResource.ts
apps/frontend/src/hooks/useAppContextData.ts
apps/frontend/src/hooks/useNotificationsData.ts
apps/frontend/src/hooks/useRwaBriefingData.ts
apps/frontend/src/hooks/useRwaDashboardData.ts
apps/frontend/src/hooks/useRwaLineageData.ts
apps/frontend/src/hooks/useToast.ts
apps/frontend/src/hooks/useUiActions.ts
bob_sessions/
docker/
docs/
infra/
k6/
k8s/
mcps/
observability/
scripts/

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll create a comprehensive Jira issue documenting the MCP-019 release evidence package. Let me create it as a Task in the RCT project.

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>createJiraIssue</tool_name>
<arguments>
{
  "cloudId": "azenoca.atlassian.net",
  "projectKey": "RCT",
  "issueTypeName": "Zadanie",
  "summary": "MCP-019: Bank Regulatory Controls MCP - Release Evidence Package v0.1.0",
  "description": "# Release Evidence Package: Bank Regulatory Controls MCP\n\n**Version:** 0.1.0\n**Release Date:** 2026-05-17\n**Package Generated:** 2026-05-17T00:42:00+02:00\n\n---\n\n## ⚠️ HUMAN REVIEW REQUIRED\n\n**IMPORTANT: This MCP server provides engineering guidance only.**\n\nAll regulatory mappings, controls, evidence requirements, and release readiness decisions **MUST be reviewed by qualified compliance, legal, or risk specialists** before production use.\n\n**This tool does NOT provide:**\n- Legal advice\n- Regulatory compliance certification\n- Substitute for qualified compliance review\n- Guarantee of regulatory compliance\n\n**All outputs from this MCP server require human validation by:**\n- Compliance officers\n- Legal counsel\n- Risk management specialists\n- Internal audit teams\n\n---\n\n## Executive Summary\n\n### Release Status: ✅ READY FOR COMPLIANCE REVIEW\n\nThe Bank Regulatory Controls MCP server has successfully passed all technical quality gates:\n\n- ✅ **Build:** Clean TypeScript compilation\n- ✅ **Tests:** 94 tests passing (11 test files)\n- ✅ **Docker:** Multi-stage build successful\n- ✅ **Corpus:** 9 regulations, 15 controls, validated referential integrity\n- ✅ **MCP Protocol:** 15 tools registered with schemas and annotations\n- ✅ **Runtime Security:** No external API calls, local-only operation, production dependency audit clean\n\n### Critical Blockers: NONE\n\nAll technical requirements are met. The system is ready for compliance, legal, and risk review.\n\n---\n\n## 1. MCP Tool Contracts\n\n### Tool Count: 15\n\nAll tools are **read-only, non-destructive, and idempotent**.\n\n#### Core Tools\n1. **health_check** - Server health and corpus statistics\n2. **get_regulatory_profile** - Regulations and controls by domain/jurisdiction\n3. **search_regulations** - Search regulatory corpus\n4. **match_controls** - Match engineering controls to artifacts\n\n#### Review Tools\n5. **review_feature_description** - Review feature for missing controls\n6. **review_architecture_text** - Review architecture for regulatory gaps\n7. **review_code_diff** - Review code for hardcoded logic, PII, validation gaps\n\n#### Generation Tools\n8. **generate_acceptance_criteria** - Generate acceptance criteria from controls\n9. **generate_data_lineage_requirements** - Generate RWA lineage requirements\n10. **generate_audit_log_requirements** - Generate audit event requirements\n11. **generate_test_obligations** - Generate Given/When/Then test obligations\n12. **generate_rwa_run_evidence_requirements** - Generate RWA run evidence package\n\n#### Release Tools\n13. **assess_release_readiness** - Assess release readiness from controls and evidence\n14. **generate_regulatory_mapping_report** - Generate Markdown regulatory report\n15. **explain_control** - Explain control with tasks and common mistakes\n\n**Full tool contracts:** See `mcps/regulatory_mcp/docs/release-evidence/tool-contracts.json`\n\n---\n\n## 2. Regulatory Corpus Inventory\n\n### Summary\n- **Regulations:** 9 (5 EU, 1 Global, 3 Internal)\n- **Controls:** 15 (7 critical, 6 high, 2 medium)\n- **Mappings:** 3 (keywords, artifacts, domains)\n- **Validation:** All referential integrity checks passed\n\n### External Regulations (6 require human review)\n1. **BCBS239** - Principles for effective risk data aggregation and risk reporting (GLOBAL)\n2. **CRR3** - Capital Requirements Regulation III / CRD6 (EU)\n3. **DORA** - Digital Operational Resilience Act (EU)\n4. **EBA_ICT_SECURITY** - EBA Guidelines on ICT and Security Risk Management (EU)\n5. **EBA_REPORTING_4** - EBA Reporting Framework 4.0 (EU)\n6. **GDPR** - General Data Protection Regulation (EU)\n\n### Internal Policies (3)\n7. **INTERNAL_AUDIT_EVIDENCE** - Internal Audit Evidence Collection Policy\n8. **INTERNAL_RULE_GOVERNANCE** - Internal Rule Governance and Versioning Policy\n9. **INTERNAL_SDLC** - Internal SDLC and Testing Policy\n\n**Full corpus inventory:** See `mcps/regulatory_mcp/docs/release-evidence/corpus-inventory.json`\n\n---\n\n## 3. Evidence Files\n\nAll evidence files are located in `mcps/regulatory_mcp/docs/release-evidence/`:\n\n- `build-log.txt` - TypeScript compilation output\n- `test-results.txt` - Test execution results (94 tests passing)\n- `docker-build.txt` - Docker build output\n- `compose-build.txt` - Docker Compose build output\n- `compose-run-output.txt` - Docker Compose startup smoke output\n- `production-audit.txt` - Production dependency audit (0 vulnerabilities)\n- `tool-contracts.json` - MCP tool contracts (15 tools)\n- `corpus-inventory.json` - Regulatory corpus inventory\n- `release-readiness.md` - Complete release readiness document\n\n---\n\n## 4. Sign-Off Requirements\n\nBefore production deployment, the following sign-offs are **REQUIRED:**\n\n### Technical Sign-Off\n- [ ] **Engineering Lead** - Code quality, test

[Response interrupted by API Error]

---

**User:**

[read_file for 'mcps/regulatory_mcp/docs/release-evidence/release-readiness.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>mcps/regulatory_mcp/docs/release-evidence/release-readiness.md</path>
<content lines="1-100">
  1 | # Release Evidence Package: Bank Regulatory Controls MCP
  2 | 
  3 | **Version:** 0.1.0  
  4 | **Release Date:** 2026-05-17  
  5 | **Package Generated:** 2026-05-17T00:42:00+02:00
  6 | 
  7 | ---
  8 | 
  9 | ## ⚠️ HUMAN REVIEW REQUIRED
 10 | 
 11 | **IMPORTANT: This MCP server provides engineering guidance only.**
 12 | 
 13 | All regulatory mappings, controls, evidence requirements, and release readiness decisions **MUST be reviewed by qualified compliance, legal, or risk specialists** before production use.
 14 | 
 15 | **This tool does NOT provide:**
 16 | - Legal advice
 17 | - Regulatory compliance certification
 18 | - Substitute for qualified compliance review
 19 | - Guarantee of regulatory compliance
 20 | 
 21 | **All outputs from this MCP server require human validation by:**
 22 | - Compliance officers
 23 | - Legal counsel
 24 | - Risk management specialists
 25 | - Internal audit teams
 26 | 
 27 | ---
 28 | 
 29 | ## Executive Summary
 30 | 
 31 | ### Release Status: ✅ READY FOR COMPLIANCE REVIEW
 32 | 
 33 | The Bank Regulatory Controls MCP server has successfully passed all technical quality gates:
 34 | 
 35 | - ✅ **Build:** Clean TypeScript compilation
 36 | - ✅ **Tests:** 94 tests passing (11 test files)
 37 | - ✅ **Docker:** Multi-stage build successful
 38 | - ✅ **Corpus:** 9 regulations, 15 controls, validated referential integrity
 39 | - ✅ **MCP Protocol:** 15 tools registered with schemas and annotations
 40 | - ✅ **Runtime Security:** No external API calls, local-only operation, production dependency audit clean
 41 | 
 42 | ### Critical Blockers: NONE
 43 | 
 44 | All technical requirements are met. The system is ready for compliance, legal, and risk review.
 45 | 
 46 | ---
 47 | 
 48 | ## 1. MCP Tool Contracts
 49 | 
 50 | ### Tool Count: 15
 51 | 
 52 | All tools are **read-only, non-destructive, and idempotent**.
 53 | 
 54 | #### Core Tools
 55 | 
 56 | 1. **health_check** - Server health and corpus statistics
 57 | 2. **get_regulatory_profile** - Regulations and controls by domain/jurisdiction
 58 | 3. **search_regulations** - Search regulatory corpus
 59 | 4. **match_controls** - Match engineering controls to artifacts
 60 | 
 61 | #### Review Tools
 62 | 
 63 | 5. **review_feature_description** - Review feature for missing controls
 64 | 6. **review_architecture_text** - Review architecture for regulatory gaps
 65 | 7. **review_code_diff** - Review code for hardcoded logic, PII, validation gaps
 66 | 
 67 | #### Generation Tools
 68 | 
 69 | 8. **generate_acceptance_criteria** - Generate acceptance criteria from controls
 70 | 9. **generate_data_lineage_requirements** - Generate RWA lineage requirements
 71 | 10. **generate_audit_log_requirements** - Generate audit event requirements
 72 | 11. **generate_test_obligations** - Generate Given/When/Then test obligations
 73 | 12. **generate_rwa_run_evidence_requirements** - Generate RWA run evidence package
 74 | 
 75 | #### Release Tools
 76 | 
 77 | 13. **assess_release_readiness** - Assess release readiness from controls and evidence
 78 | 14. **generate_regulatory_mapping_report** - Generate Markdown regulatory report
 79 | 15. **explain_control** - Explain control with tasks and common mistakes
 80 | 
 81 | **Full tool contracts:** See `tool-contracts.json`
 82 | 
 83 | ---
 84 | 
 85 | ## 2. Regulatory Corpus Inventory
 86 | 
 87 | ### Summary
 88 | 
 89 | - **Regulations:** 9 (5 EU, 1 Global, 3 Internal)
 90 | - **Controls:** 15 (7 critical, 6 high, 2 medium)
 91 | - **Mappings:** 3 (keywords, artifacts, domains)
 92 | - **Validation:** All referential integrity checks passed
 93 | 
 94 | ### Regulations
 95 | 
 96 | #### External Regulations (6 require human review)
 97 | 
 98 | 1. **BCBS239** - Principles for effective risk data aggregation and risk reporting (GLOBAL)
 99 | 2. **CRR3** - Capital Requirements Regulation III / CRD6 (EU)
100 | 3. **DORA** - Digital Operational Resilience Act (EU)
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
mcps/regulatory_mcp/docs/release-evidence/test-coverage-report.md

# VSCode Open Tabs
apps/backend/Dockerfile,apps/backend/tests/agents/test_performance.py,mcps/regulatory_mcp/test-docker-smoke.sh,mcps/regulatory_mcp/README.md,mcps/regulatory_mcp/docs/release-evidence/test-coverage-report.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:04:12.944Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$2.05

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>advanced</slug>
<name>🛠️ Advanced</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Explore regulatory_mcp directory structure | Completed |
| 2 | Create release-evidence directory | Completed |
| 3 | Generate tool-contracts.json from MCP tool definitions | Completed |
| 4 | Generate corpus-inventory.json from corpus data | Completed |
| 5 | Run build and capture output | Completed |
| 6 | Run tests and capture output | Completed |
| 7 | Build Docker image and capture output | Completed |
| 8 | Create comprehensive release-readiness.md | Completed |
| 9 | Use Atlassian MCP to create Confluence page with release evidence | In Progress |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Let me create a more concise Jira issue with the key information and a link to the full documentation:

<use_mcp_tool>
<server_name>atlassian</server_name>
<tool_name>createJiraIssue</tool_name>
<arguments>
{
  "cloudId": "azenoca.atlassian.net",
  "projectKey": "RCT",
  "issueTypeName": "Zadanie",
  "summary": "MCP-019: Bank Regulatory Controls MCP - Release Evidence Package v0.1.0",
  "description": "# MCP-019: Release Evidence Package\n\n**Version:** 0.1.0 | **Release Date:** 2026-05-17 | **Status:** ✅ READY FOR COMPLIANCE REVIEW\n\n## ⚠️ HUMAN REVIEW REQUIRED\n\nThis MCP server provides engineering guidance only. All regulatory mappings, controls, and release decisions **MUST be reviewed by qualified compliance, legal, or risk specialists** before production use.\n\n## Executive Summary\n\nThe Bank Regulatory Controls MCP server has successfully passed all technical quality gates:\n\n✅ **Build:** Clean TypeScript compilation\n✅ **Tests:** 94 tests passing (11 test files)\n✅ **Docker:** Multi-stage build successful\n✅ **Corpus:** 9 regulations, 15 controls, validated referential integrity\n✅ **MCP Protocol:** 15 tools registered with schemas and annotations\n✅ **Runtime Security:** No external API calls, local-only operation, production dependency audit clean\n\n**Critical Blockers:** NONE\n\n## MCP Tool Contracts (15 Tools)\n\nAll tools are read-only, non-destructive, and idempotent:\n\n**Core Tools:** health_check, get_regulatory_profile, search_regulations, match_controls\n\n**Review Tools:** review_feature_description, review_architecture_text, review_code_diff\n\n**Generation Tools:** generate_acceptance_criteria, generate_data_lineage_requirements, generate_audit_log_requirements, generate_test_obligations, generate_rwa_run_evidence_requirements\n\n**Release Tools:** assess_release_readiness, generate_regulatory_mapping_report, explain_control\n\n## Regulatory Corpus\n\n**Regulations:** 9 (5 EU, 1 Global, 3 Internal)\n- BCBS239, CRR3, DORA, EBA_ICT_SECURITY, EBA_REPORTING_4, GDPR\n- INTERNAL_AUDIT_EVIDENCE, INTERNAL_RULE_GOVERNANCE, INTERNAL_SDLC\n\n**Controls:** 15 (7 critical, 6 high, 2 medium)\n\n**Mappings:** 3 (keywords, artifacts, domains)\n\n## Evidence Files Location\n\n`mcps/regulatory_mcp/docs/release-evidence/`\n\n- `release-readiness.md` - Complete release readiness document\n- `tool-contracts.json` - MCP tool contracts\n- `corpus-inventory.json` - Regulatory corpus inventory\n- `build-log.txt` - TypeScript compilation output\n- `test-results.txt` - Test execution results\n- `docker-build.txt` - Docker build output\n- `production-audit.txt` - Dependency audit (0 vulnerabilities)\n\n## Required Sign-Offs\n\n**Technical:**\n- [ ] Engineering Lead - Code quality, test coverage, build process\n- [ ] Security Team - Security posture, dependency vulnerabilities\n- [ ] DevOps/SRE - Deployment process, monitoring\n\n**Regulatory:**\n- [ ] Compliance Officer - Corpus content accuracy, regulatory alignment\n- [ ] Legal Counsel - Disclaimers, limitations, liability\n- [ ] Risk Management - Operational risk assessment\n- [ ] Internal Audit - Evidence collection, audit trail\n\n**Deployment:**\n- [ ] Product Owner - Business value, user acceptance\n- [ ] CTO/CIO - Strategic alignment, technical architecture\n\n## Next Steps\n\n1. Schedule compliance review meeting\n2. Distribute evidence package to stakeholders\n3. Collect sign-offs from all required parties\n4. Plan production deployment after all approvals\n\n## Documentation\n\nFull documentation: `mcps/regulatory_mcp/docs/release-evidence/release-readiness.md`",
  "contentFormat": "markdown"
}
</arguments>
</use_mcp_tool>

