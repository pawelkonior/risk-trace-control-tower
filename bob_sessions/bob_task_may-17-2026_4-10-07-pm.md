**User:**

<task>
I need you to conduct a comprehensive enterprise-level analysis of recent changes to this project. The user is concerned about modifications that were made and wants a thorough review.

Please analyze:

1. **Recent Session History**: Review the bob_sessions directory, particularly the most recent sessions (bob_task_may-17-2026_2-31-18-pm.md and other recent files) to understand what changes were made.

2. **Documentation Files**: Examine these recently modified/created documentation files:
   - docs/PERFORMANCE_OPTIMIZATION_PLAN.md
   - docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md
   - docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md
   - mcps/EXECUTION_PLAN.md
   - mcps/README.md

3. **Enterprise-Level Quality Assessment**:
   - Check if documentation follows enterprise standards (clear structure, proper versioning, traceability)
   - Verify technical accuracy and completeness
   - Identify any inconsistencies, contradictions, or gaps
   - Assess if changes align with the project's architecture (monorepo structure, Python backend, React frontend)
   - Check if changes respect AGENTS.md guidelines

4. **Specific Concerns to Address**:
   - Are there any breaking changes or regressions?
   - Do the changes maintain backward compatibility?
   - Are there any security, performance, or architectural concerns?
   - Is the documentation actionable and implementable?
   - Are there any placeholder content or incomplete sections?

Provide a detailed analysis report covering:
- Summary of what changes were made
- List of specific issues found (categorized by severity: critical, major, minor)
- Assessment of each documentation file
- Recommendations for improvements
- Any red flags or concerns that need immediate attention

Focus on being thorough and critical - this is an enterprise-level review where quality and accuracy are paramount.

Use the attempt_completion tool when done with your comprehensive analysis report.
</task>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:41:44.246Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/home/mateusz/project/risk-trace-control-tower) Files
.gitignore
.gitleaks.toml
.semgrepignore
AGENTS.md
.bob/
.github/
apps/
apps/docker-compose.yml
apps/backend/.dockerignore
apps/backend/.python-version
apps/backend/pyproject.toml
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
apps/backend/src/rwa_steering/generated_inputs/cva_hedges.csv
apps/backend/src/rwa_steering/generated_inputs/cva_netting_sets.csv
apps/backend/src/rwa_steering/generated_inputs/cva_portfolio_inputs.csv
apps/backend/src/rwa_steering/generated_inputs/forecast_calendar.csv
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
apps/frontend/.dockerignore
apps/frontend/nginx.conf
apps/frontend/package-lock.json
apps/frontend/package.json
apps/frontend/playwright.config.ts
apps/frontend/README.md
apps/frontend/tsconfig.json
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
apps/frontend/src/hooks/useAppContextData.ts
apps/frontend/src/hooks/useNotificationsData.ts
apps/frontend/src/hooks/useRwaDashboardData.ts
apps/frontend/src/hooks/useToast.ts
apps/frontend/src/hooks/useUiActions.ts
apps/frontend/src/pages/DataLineagePage.tsx
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
bob_sessions/bob_task_may-17-2026_2-31-18-pm.md
bob_sessions/bob_task_may-17-2026_2-31-18-pm.png
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
docker/docker-compose.prod.yml
docker/docker-compose.yml
docker/nginx-host/rwa.conf
docs/
docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md
docs/RCT-15_TECHNICAL_ANALYSIS.md
docs/RCT-17_IMPLEMENTATION_SUMMARY.md
docs/RCT-18_IMPLEMENTATION_SUMMARY.md
docs/RCT-18_VALIDATION_REPORT.md
infra/
infra/helm/rwa-backend/Chart.yaml
infra/helm/rwa-backend/values.yaml
infra/helm/rwa-backend/templates/_helpers.tpl
infra/helm/rwa-backend/templates/deployment.yaml
infra/helm/rwa-backend/templates/hpa.yaml
infra/helm/rwa-backend/templates/pdb.yaml
infra/helm/rwa-backend/templates/service.yaml
infra/helm/rwa-frontend/Chart.yaml
infra/helm/rwa-frontend/values.yaml
infra/helm/rwa-frontend/templates/_helpers.tpl
infra/helm/rwa-frontend/templates/deployment.yaml
infra/helm/rwa-frontend/templates/hpa.yaml
infra/helm/rwa-frontend/templates/service.yaml
infra/helm/rwa-platform/Chart.lock
infra/helm/rwa-platform/Chart.yaml
infra/helm/rwa-platform/values-dev.yaml
infra/helm/rwa-platform/values-prod.yaml
infra/helm/rwa-platform/values-staging.yaml
infra/helm/rwa-platform/values.yaml
infra/helm/rwa-platform/charts/rwa-backend-0.1.0.tgz
infra/helm/rwa-platform/charts/rwa-frontend-0.1.0.tgz
infra/kubernetes/namespaces/rwa-dev.yaml
infra/kubernetes/namespaces/rwa-prod.yaml
infra/kubernetes/network-policies/rwa-prod-allow.yaml
infra/kubernetes/network-policies/rwa-prod-default-deny.yaml
infra/kubernetes/rbac/rwa-prod-rolebindings.yaml
infra/terraform/modules/networking/main.tf
infra/terraform/modules/networking/outputs.tf
infra/terraform/modules/networking/variables.tf
infra/terraform/modules/s3/main.tf
infra/terraform/modules/s3/outputs.tf
infra/terraform/modules/s3/variables.tf
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
mcps/
mcps/.env.example
mcps/.gitignore
mcps/docker-compose.yml
mcps/EXECUTION_PLAN.md
mcps/README.md
mcps/regulatory_mcp/.gitignore
mcps/regulatory_mcp/test-startup.sh
mcps/sonarqube/backend-project.properties
mcps/sonarqube/frontend-project.properties
observability/
observability/alertmanager.yaml
observability/grafana/dashboards/dora-metrics.json
observability/grafana/dashboards/kafka.json
observability/grafana/dashboards/rwa-application.json
scripts/

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll conduct a comprehensive enterprise-level analysis of the recent changes to this project. Let me start by examining the session history and documentation files.

<read_file>
<args>
  <file>
    <path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'bob_sessions/bob_task_may-17-2026_2-31-18-pm.md'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
<files>
<file><path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path><file_outline>File: bob_task_may-17-2026_2-31-18-pm.md (6366 lines)

</file_outline>
<notice>This file is large (6365 lines). You will use the following strategy to understand this file:
- Inform the user you are going to use large file strategy, to efficiently understand the file
- Use the file_outline provided to get an overview of the file structure to help decide next action. This is not the full file. It is not the full depth of the contents.
- If you read the file, use precise file reads with line ranges for specific sections of interest
- Consider if other commands/tools are better suited for extracting information from that file type
- Use ask_followup_question tool if needed to identify the best next action
</notice></file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:41:47.511Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.04

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll use a large file strategy to efficiently analyze this comprehensive review. Let me read the key sections of the session file and all documentation files together.

<read_file>
<args>
  <file>
    <path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path>
    <line_range>1-100</line_range>
    <line_range>6300-6366</line_range>
  </file>
  <file>
    <path>docs/PERFORMANCE_OPTIMIZATION_PLAN.md</path>
  </file>
  <file>
    <path>docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md</path>
  </file>
  <file>
    <path>docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md</path>
  </file>
  <file>
    <path>mcps/EXECUTION_PLAN.md</path>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path>
<content lines="1-100">
  1 | **User:**
  2 | 
  3 | <task>
  4 | You are working on the RiskTrace Control Tower hackathon application.
  5 | 
  6 | Goal:
  7 | Analyze the attached performance dataset and improve the codebase to reduce latency, increase throughput, and lower error rate without changing the business behavior.
  8 | 
  9 | Use the dataset columns from performance folder (*.csv/*.json):
 10 | - service
 11 | - endpoint
 12 | - scenario
 13 | - avg_latency_ms
 14 | - p95_latency_ms
 15 | - p99_latency_ms
 16 | - throughput_rps
 17 | - error_rate_pct
 18 | - cpu_avg_pct
 19 | - memory_avg_mb
 20 | - db_queries_per_request
 21 | - external_calls_per_request
 22 | - suspected_bottleneck
 23 | - optimization_hint
 24 | - target_p95_latency_ms
 25 | 
 26 | Tasks:
 27 | 1. Identify the top 3 performance bottlenecks by p95_latency_ms and error_rate_pct.
 28 | 2. Inspect the repository and map each bottleneck to the likely source files.
 29 | 3. Propose a minimal, safe performance optimization plan.
 30 | 4. Implement the improvements using small, reviewable commits.
 31 | 5. Add or update tests to prove that behavior did not change.
 32 | 6. Add lightweight performance instrumentation where missing.
 33 | 7. Prepare a summary with:
 34 |    - what was slow,
 35 |    - what was changed,
 36 |    - expected performance impact,
 37 |    - risk and rollback plan.
 38 | 
 39 | Important constraints:
 40 | - Do not remove validation, audit logging, regulatory checks, or security controls.
 41 | - Prefer async I/O, batching, caching, timeouts, retries, and payload reduction.
 42 | - Keep the application enterprise-ready and observable.
 43 | - Do not hardcode hackathon-only shortcuts into production paths.
 44 | </task>
 45 | <environment_details>
 46 | # VSCode Visible Files
 47 | 
 48 | 
 49 | # VSCode Open Tabs
 50 | 
 51 | 
 52 | # Current Time
 53 | Current time in ISO 8601 UTC format: 2026-05-17T12:26:30.596Z
 54 | User time zone: Europe/Warsaw, UTC+2:00
 55 | 
 56 | # Current Cost
 57 | $0.00
 58 | 
 59 | # Review Exclusions
 60 | The following file patterns are excluded from code reviews:
 61 | - .vscode/**
 62 | 
 63 | # Current Mode
 64 | <slug>plan</slug>
 65 | <name>📝 Plan</name>
 66 | 
 67 | 
 68 | # Current Workspace Directory (/home/mateusz/project/risk-trace-control-tower) Files
 69 | .gitignore
 70 | .semgrepignore
 71 | AGENTS.md
 72 | .bob/
 73 | .github/
 74 | apps/
 75 | apps/docker-compose.yml
 76 | apps/backend/.dockerignore
 77 | apps/backend/.python-version
 78 | apps/backend/Dockerfile
 79 | apps/backend/pyproject.toml
 80 | apps/backend/README.md
 81 | apps/backend/src/rwa_agents/__init__.py
 82 | apps/backend/src/rwa_agents/checkpointing.py
 83 | apps/backend/src/rwa_agents/config.py
 84 | apps/backend/src/rwa_agents/guardrails.py
 85 | apps/backend/src/rwa_agents/observability.py
 86 | apps/backend/src/rwa_agents/py.typed
 87 | apps/backend/src/rwa_agents/schemas.py
 88 | apps/backend/src/rwa_agents/state.py
 89 | apps/backend/src/rwa_calculator/paths.py
 90 | apps/backend/src/rwa_common/__init__.py
 91 | apps/backend/src/rwa_common/db.py
 92 | apps/backend/src/rwa_common/py.typed
 93 | apps/backend/src/rwa_dashboard/__init__.py
 94 | apps/backend/src/rwa_dashboard/api.py
 95 | apps/backend/src/rwa_dashboard/data.py
 96 | apps/backend/src/rwa_dashboard/models.py
 97 | apps/backend/src/rwa_dashboard/py.typed
 98 | apps/backend/src/rwa_dashboard/repositories.py
 99 | apps/backend/src/rwa_dashboard/schemas.py
100 | apps/backend/src/rwa_dashboard/seed.py
</content>
<content lines="6300-6366">
6300 | | 3 | Optimize database queries and add connection pooling | Pending |
6301 | | 4 | Implement caching layer for expensive calculations | Pending |
6302 | | 5 | Add async I/O for external service calls | Pending |
6303 | | 6 | Optimize data processing pipelines (pandas operations) | Pending |
6304 | | 7 | Add request/response compression | Pending |
6305 | | 8 | Implement batch processing optimizations | Pending |
6306 | | 9 | Add performance monitoring and instrumentation | Pending |
6307 | | 10 | Create performance test suite | Pending |
6308 | | 11 | Document optimization changes and expected impact | Completed |
6309 | | 12 | Prepare rollback plan and risk assessment | Completed |
6310 | 
6311 | 
6312 | IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.
6313 | 
6314 | </environment_details>
6315 | 
6316 | ---
6317 | 
6318 | **Assistant:**
6319 | 
6320 | <attempt_completion>
6321 | <result>
6322 | Performance optimization plan completed for RiskTrace Control Tower. Created comprehensive documentation:
6323 | 
6324 | **📊 Analysis Complete:**
6325 | - Identified top 3 bottlenecks: expensive RWA calculations (no caching), synchronous database operations, inefficient pandas processing
6326 | - Mapped bottlenecks to source files with line numbers
6327 | - Estimated 75-85% latency reduction potential
6328 | 
6329 | **📋 Deliverables:**
6330 | 1. **PERFORMANCE_OPTIMIZATION_PLAN.md** - Detailed 438-line strategy document covering:
6331 |    - 5 major bottlenecks with impact analysis
6332 |    - 3-phase optimization roadmap (12 improvements)
6333 |    - Performance monitoring infrastructure
6334 |    - Risk assessment and rollback plan
6335 |    - Expected improvements: p95 latency <500ms (75-85% reduction)
6336 | 
6337 | 2. **PERFORMANCE_IMPLEMENTATION_GUIDE.md** - 700-line technical guide with:
6338 |    - Complete code examples for all optimizations
6339 |    - TTL caching, response compression, async DB operations
6340 |    - Pandas vectorization, parallel processing, Redis integration
6341 |    - Performance test suite and deployment checklist
6342 | 
6343 | 3. **PERFORMANCE_OPTIMIZATION_SUMMARY.md** - Executive summary with:
6344 |    - Key findings and architecture changes
6345 |    - Implementation roadmap (4-week timeline)
6346 |    - Success criteria and monitoring strategy
6347 |    - Compliance verification (all controls maintained)
6348 | 
6349 | **🎯 Key Optimizations Planned:**
6350 | - Response caching (80-90% latency reduction)
6351 | - Database connection pooling (30-40% overhead reduction)
6352 | - Async I/O operations (50-70% throughput increase)
6353 | - Pandas vectorization (40-60% processing speedup)
6354 | - Request compression (60-70% payload reduction)
6355 | 
6356 | **✅ Enterprise-Ready:**
6357 | - All validation, audit logging, and security controls preserved
6358 | - Feature flags for safe rollback
6359 | - Gradual deployment strategy (dev → staging → 10% → 100%)
6360 | - Comprehensive monitoring with Prometheus metrics
6361 | 
6362 | **Next Step:** Switch to Code mode to implement Phase 1 optimizations
6363 | </result>
6364 | </attempt_completion>
6365 | 
</content>
</file>
<file><path>docs/PERFORMANCE_OPTIMIZATION_PLAN.md</path>
<content lines="1-365">
  1 | # RiskTrace Control Tower - Performance Optimization Plan
  2 | 
  3 | **Date:** 2026-05-17  
  4 | **Version:** 1.0  
  5 | **Status:** Planning Phase
  6 | 
  7 | ## Executive Summary
  8 | 
  9 | This document outlines a comprehensive performance optimization strategy for the RiskTrace Control Tower application, focusing on reducing latency, increasing throughput, and lowering error rates while maintaining all regulatory compliance, audit logging, and security controls.
 10 | 
 11 | ## Identified Performance Bottlenecks
 12 | 
 13 | ### 1. **Database Operations (HIGH PRIORITY)**
 14 | 
 15 | **Location:** `apps/backend/src/rwa_dashboard/repositories.py`, `apps/backend/src/rwa_common/db.py`
 16 | 
 17 | **Issues:**
 18 | - No connection pooling for production Postgres (uses default pool)
 19 | - SQLite NullPool for file-based databases prevents connection reuse
 20 | - No query result caching for frequently accessed datasets
 21 | - Synchronous database operations block request threads
 22 | - Deep copy operations on large payloads (`deepcopy(self.repository.get_payload())`)
 23 | 
 24 | **Impact:**
 25 | - High p95 latency on dashboard endpoints
 26 | - Database connection overhead on every request
 27 | - Memory pressure from payload duplication
 28 | 
 29 | ### 2. **Heavy Data Processing (HIGH PRIORITY)**
 30 | 
 31 | **Location:** `apps/backend/src/rwa_dashboard/data.py`, `apps/backend/src/rwa_dashboard/api.py`
 32 | 
 33 | **Issues:**
 34 | - `current_rwa_snapshot()` loads entire portfolio and calculates RWA on every request (line 127-145)
 35 | - No caching of calculation results
 36 | - Pandas operations on large DataFrames without optimization
 37 | - Multiple groupby/aggregation operations per request
 38 | - CSV file loading on every calculation (`load_core_csv()`)
 39 | 
 40 | **Impact:**
 41 | - Dashboard endpoints likely >2s p95 latency
 42 | - High CPU usage during peak load
 43 | - Memory allocation spikes
 44 | 
 45 | ### 3. **Synchronous Service Calls (MEDIUM PRIORITY)**
 46 | 
 47 | **Location:** `apps/backend/src/rwa_steering/engine.py`, `apps/backend/src/rwa_forecast_service/engine.py`
 48 | 
 49 | **Issues:**
 50 | - Sequential calculator batch calls in loops (lines 85, 105, 325)
 51 | - No parallelization of independent calculations
 52 | - Attribution driver calculations run sequentially (lines 263-277)
 53 | - Recommendation generation processes rows one-by-one (lines 347-373)
 54 | 
 55 | **Impact:**
 56 | - Linear scaling with portfolio size
 57 | - Underutilized CPU cores
 58 | - Long request times for large portfolios
 59 | 
 60 | ### 4. **Frontend API Calls (MEDIUM PRIORITY)**
 61 | 
 62 | **Location:** `apps/frontend/src/api/client.ts`, `apps/frontend/src/hooks/useApiResource.ts`
 63 | 
 64 | **Issues:**
 65 | - No request deduplication
 66 | - No response caching
 67 | - Sequential API calls in hooks
 68 | - No request timeout configuration
 69 | - No retry logic for transient failures
 70 | 
 71 | **Impact:**
 72 | - Redundant backend calls
 73 | - Poor user experience on slow networks
 74 | - Cascading failures
 75 | 
 76 | ### 5. **Data Serialization (LOW-MEDIUM PRIORITY)**
 77 | 
 78 | **Location:** Multiple FastAPI endpoints
 79 | 
 80 | **Issues:**
 81 | - No response compression (gzip/brotli)
 82 | - Large JSON payloads without pagination
 83 | - Decimal/date serialization overhead
 84 | - No streaming for large responses
 85 | 
 86 | **Impact:**
 87 | - High network bandwidth usage
 88 | - Slow response times on limited bandwidth
 89 | - Memory pressure on serialization
 90 | 
 91 | ## Optimization Strategy
 92 | 
 93 | ### Phase 1: Quick Wins (Week 1)
 94 | 
 95 | #### 1.1 Add Response Caching
 96 | - **File:** `apps/backend/src/rwa_dashboard/service.py`
 97 | - **Change:** Implement in-memory LRU cache for dashboard snapshots
 98 | - **Expected Impact:** 80-90% latency reduction for cached requests
 99 | - **Risk:** Low - cache invalidation on data updates
100 | 
101 | #### 1.2 Enable Response Compression
102 | - **File:** `apps/backend/src/rwa_dashboard/api.py` (FastAPI middleware)
103 | - **Change:** Add GZipMiddleware with compression level 6
104 | - **Expected Impact:** 60-70% payload size reduction, 20-30% latency improvement
105 | - **Risk:** Very Low - standard middleware
106 | 
107 | #### 1.3 Optimize Database Connection Pooling
108 | - **File:** `apps/backend/src/rwa_common/db.py`
109 | - **Change:** Configure proper pool size (10-20), max_overflow (5-10), pool_pre_ping
110 | - **Expected Impact:** 30-40% reduction in connection overhead
111 | - **Risk:** Low - standard SQLAlchemy configuration
112 | 
113 | #### 1.4 Add Request Timeouts
114 | - **File:** `apps/frontend/src/api/client.ts`
115 | - **Change:** Add 30s timeout with AbortController
116 | - **Expected Impact:** Prevent hung requests, improve error handling
117 | - **Risk:** Very Low - defensive programming
118 | 
119 | ### Phase 2: Core Optimizations (Week 2-3)
120 | 
121 | #### 2.1 Implement Calculation Result Caching
122 | - **File:** `apps/backend/src/rwa_dashboard/data.py`
123 | - **Change:** Cache `current_rwa_snapshot()` results with TTL (5-15 minutes)
124 | - **Expected Impact:** 90%+ latency reduction for repeated calculations
125 | - **Risk:** Medium - requires cache invalidation strategy
126 | 
127 | #### 2.2 Optimize Pandas Operations
128 | - **File:** `apps/backend/src/rwa_dashboard/data.py`
129 | - **Changes:**
130 |   - Use categorical dtypes for entity_class, sub_class, country codes
131 |   - Vectorize operations instead of iterrows()
132 |   - Pre-allocate DataFrames where possible
133 |   - Use query() instead of boolean indexing
134 | - **Expected Impact:** 40-60% reduction in data processing time
135 | - **Risk:** Low - performance optimization only
136 | 
137 | #### 2.3 Add Async Database Operations
138 | - **File:** `apps/backend/src/rwa_dashboard/repositories.py`
139 | - **Change:** Use SQLAlchemy async engine with asyncpg
140 | - **Expected Impact:** 50-70% throughput increase under load
141 | - **Risk:** Medium - requires async/await refactoring
142 | 
143 | #### 2.4 Implement Batch Processing
144 | - **File:** `apps/backend/src/rwa_steering/engine.py`
145 | - **Change:** Parallelize independent calculator calls using ProcessPoolExecutor
146 | - **Expected Impact:** 3-4x speedup on multi-core systems
147 | - **Risk:** Medium - requires careful state management
148 | 
149 | ### Phase 3: Advanced Optimizations (Week 4)
150 | 
151 | #### 3.1 Add Redis Caching Layer
152 | - **Files:** New `apps/backend/src/rwa_common/cache.py`
153 | - **Change:** Distributed cache for calculation results, dashboard snapshots
154 | - **Expected Impact:** Horizontal scalability, 95%+ cache hit rate
155 | - **Risk:** Medium - requires Redis infrastructure
156 | 
157 | #### 3.2 Implement Query Result Pagination
158 | - **File:** `apps/backend/src/rwa_dashboard/api.py`
159 | - **Change:** Add limit/offset pagination for large result sets
160 | - **Expected Impact:** 70-80% reduction in response size
161 | - **Risk:** Low - standard REST pattern
162 | 
163 | #### 3.3 Add Frontend Request Deduplication
164 | - **File:** `apps/frontend/src/hooks/useApiResource.ts`
165 | - **Change:** Implement request deduplication and response caching
166 | - **Expected Impact:** 50-60% reduction in redundant API calls
167 | - **Risk:** Low - client-side optimization
168 | 
169 | #### 3.4 Optimize CSV Loading
170 | - **File:** `apps/backend/src/rwa_dashboard/data.py`
171 | - **Change:** Load and cache CSV files at startup, not per-request
172 | - **Expected Impact:** 100-200ms reduction per request
173 | - **Risk:** Low - one-time load with refresh mechanism
174 | 
175 | ## Performance Monitoring & Instrumentation
176 | 
177 | ### Metrics to Track
178 | 
179 | 1. **Latency Metrics:**
180 |    - p50, p95, p99 response times per endpoint
181 |    - Database query duration
182 |    - Calculation engine duration
183 |    - External service call duration
184 | 
185 | 2. **Throughput Metrics:**
186 |    - Requests per second (RPS)
187 |    - Concurrent request handling
188 |    - Queue depth
189 | 
190 | 3. **Resource Metrics:**
191 |    - CPU utilization
192 |    - Memory usage
193 |    - Database connection pool stats
194 |    - Cache hit/miss rates
195 | 
196 | 4. **Error Metrics:**
197 |    - Error rate by endpoint
198 |    - Timeout rate
199 |    - Database connection errors
200 |    - Cache failures
201 | 
202 | ### Implementation
203 | 
204 | **File:** New `apps/backend/src/rwa_common/monitoring.py`
205 | 
206 | ```python
207 | # Prometheus metrics integration
208 | from prometheus_client import Counter, Histogram, Gauge
209 | 
210 | request_duration = Histogram(
211 |     'rwa_request_duration_seconds',
212 |     'Request duration in seconds',
213 |     ['endpoint', 'method', 'status']
214 | )
215 | 
216 | calculation_duration = Histogram(
217 |     'rwa_calculation_duration_seconds',
218 |     'RWA calculation duration',
219 |     ['calculation_type']
220 | )
221 | 
222 | cache_hits = Counter(
223 |     'rwa_cache_hits_total',
224 |     'Cache hit count',
225 |     ['cache_type']
226 | )
227 | 
228 | db_pool_size = Gauge(
229 |     'rwa_db_pool_size',
230 |     'Database connection pool size'
231 | )
232 | ```
233 | 
234 | ## Testing Strategy
235 | 
236 | ### 1. Performance Baseline
237 | - Run k6 load tests before optimizations
238 | - Capture baseline metrics for all endpoints
239 | - Document current p95/p99 latencies
240 | 
241 | ### 2. Regression Testing
242 | - Ensure all existing tests pass
243 | - Add performance regression tests
244 | - Validate calculation results unchanged
245 | 
246 | ### 3. Load Testing
247 | - Gradually increase load to 2x, 5x, 10x baseline
248 | - Monitor resource utilization
249 | - Identify new bottlenecks
250 | 
251 | ### 4. Chaos Testing
252 | - Test cache failures
253 | - Test database connection loss
254 | - Validate graceful degradation
255 | 
256 | ## Risk Assessment & Rollback Plan
257 | 
258 | ### Risks
259 | 
260 | | Risk | Probability | Impact | Mitigation |
261 | |------|------------|--------|------------|
262 | | Cache invalidation bugs | Medium | High | Comprehensive testing, TTL safety net |
263 | | Async/await refactoring errors | Medium | High | Gradual rollout, feature flags |
264 | | Memory leaks from caching | Low | Medium | Memory monitoring, cache size limits |
265 | | Database pool exhaustion | Low | High | Pool monitoring, circuit breakers |
266 | | Breaking changes to API contracts | Low | Critical | Contract testing, versioning |
267 | 
268 | ### Rollback Strategy
269 | 
270 | 1. **Feature Flags:** All optimizations behind feature flags
271 | 2. **Gradual Rollout:** Deploy to dev → staging → 10% prod → 100% prod
272 | 3. **Monitoring:** Real-time alerts on latency/error rate increases
273 | 4. **Quick Rollback:** One-command rollback via feature flag toggle
274 | 5. **Database Migrations:** Reversible migrations only
275 | 
276 | ### Rollback Triggers
277 | 
278 | - p95 latency increases >20% from baseline
279 | - Error rate increases >1%
280 | - Memory usage increases >50%
281 | - Any calculation result discrepancies
282 | 
283 | ## Expected Performance Impact
284 | 
285 | ### Conservative Estimates
286 | 
287 | | Metric | Current (Estimated) | Target | Improvement |
288 | |--------|-------------------|--------|-------------|
289 | | Dashboard p95 latency | 2000-3000ms | <500ms | 75-85% |
290 | | Calculation p95 latency | 1500-2500ms | <300ms | 80-88% |
291 | | Throughput (RPS) | 10-20 | 50-100 | 250-500% |
292 | | Error rate | 1-2% | <0.1% | 90-95% |
293 | | Memory usage | Baseline | +20% | Acceptable |
294 | | CPU efficiency | 30-40% | 60-80% | 50-100% |
295 | 
296 | ### Aggressive Estimates (with all optimizations)
297 | 
298 | | Metric | Target | Improvement |
299 | |--------|--------|-------------|
300 | | Dashboard p95 latency | <200ms | 90-93% |
301 | | Calculation p95 latency | <150ms | 93-95% |
302 | | Throughput (RPS) | 100-200 | 500-1000% |
303 | | Cache hit rate | >95% | N/A |
304 | 
305 | ## Implementation Timeline
306 | 
307 | ### Week 1: Quick Wins
308 | - Day 1-2: Response caching + compression
309 | - Day 3-4: Database pooling + timeouts
310 | - Day 5: Testing and monitoring
311 | 
312 | ### Week 2-3: Core Optimizations
313 | - Day 6-8: Calculation caching
314 | - Day 9-11: Pandas optimizations
315 | - Day 12-14: Async database operations
316 | - Day 15: Batch processing
317 | 
318 | ### Week 4: Advanced & Polish
319 | - Day 16-18: Redis integration
320 | - Day 19-20: Pagination + deduplication
321 | - Day 21-22: CSV loading optimization
322 | - Day 23-24: Performance testing
323 | - Day 25: Documentation and handoff
324 | 
325 | ## Compliance & Security Notes
326 | 
327 | ### Maintained Controls
328 | 
329 | ✅ All validation logic preserved  
330 | ✅ Audit logging unchanged  
331 | ✅ Regulatory checks intact  
332 | ✅ Security controls maintained  
333 | ✅ Data integrity guarantees preserved  
334 | 
335 | ### New Security Considerations
336 | 
337 | - Cache encryption for sensitive data
338 | - Redis authentication and TLS
339 | - Rate limiting to prevent abuse
340 | - Cache poisoning prevention
341 | 
342 | ## Success Criteria
343 | 
344 | 1. ✅ p95 latency <500ms for all dashboard endpoints
345 | 2. ✅ p99 latency <1000ms for all endpoints
346 | 3. ✅ Error rate <0.1%
347 | 4. ✅ Throughput >50 RPS sustained
348 | 5. ✅ All existing tests pass
349 | 6. ✅ No calculation result changes
350 | 7. ✅ Memory usage increase <30%
351 | 8. ✅ Zero security regressions
352 | 
353 | ## Next Steps
354 | 
355 | 1. **Approve Plan:** Review and approve optimization strategy
356 | 2. **Create Performance Dataset:** Generate baseline metrics
357 | 3. **Set Up Monitoring:** Deploy Prometheus/Grafana dashboards
358 | 4. **Begin Phase 1:** Implement quick wins
359 | 5. **Measure & Iterate:** Continuous measurement and refinement
360 | 
361 | ---
362 | 
363 | **Document Owner:** Performance Engineering Team  
364 | **Last Updated:** 2026-05-17  
365 | **Next Review:** After Phase 1 completion
</content>
</file>
<file><path>docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md</path>
<content lines="1-735">
  1 | # Performance Optimization Implementation Guide
  2 | 
  3 | This guide provides detailed implementation steps for each optimization in the performance plan.
  4 | 
  5 | ## Table of Contents
  6 | 
  7 | 1. [Phase 1: Quick Wins](#phase-1-quick-wins)
  8 | 2. [Phase 2: Core Optimizations](#phase-2-core-optimizations)
  9 | 3. [Phase 3: Advanced Optimizations](#phase-3-advanced-optimizations)
 10 | 4. [Testing & Validation](#testing--validation)
 11 | 
 12 | ---
 13 | 
 14 | ## Phase 1: Quick Wins
 15 | 
 16 | ### 1.1 Response Caching with LRU Cache
 17 | 
 18 | **File:** `apps/backend/src/rwa_common/cache.py` (new)
 19 | 
 20 | ```python
 21 | from __future__ import annotations
 22 | 
 23 | from functools import lru_cache, wraps
 24 | from typing import Any, Callable, TypeVar
 25 | from datetime import datetime, timedelta
 26 | import hashlib
 27 | import json
 28 | 
 29 | T = TypeVar("T")
 30 | 
 31 | class TTLCache:
 32 |     """Time-based LRU cache with automatic expiration."""
 33 |     
 34 |     def __init__(self, ttl_seconds: int = 300, maxsize: int = 128):
 35 |         self.ttl_seconds = ttl_seconds
 36 |         self.maxsize = maxsize
 37 |         self._cache: dict[str, tuple[Any, datetime]] = {}
 38 |     
 39 |     def get(self, key: str) -> Any | None:
 40 |         if key not in self._cache:
 41 |             return None
 42 |         value, expires_at = self._cache[key]
 43 |         if datetime.utcnow() > expires_at:
 44 |             del self._cache[key]
 45 |             return None
 46 |         return value
 47 |     
 48 |     def set(self, key: str, value: Any) -> None:
 49 |         if len(self._cache) >= self.maxsize:
 50 |             # Remove oldest entry
 51 |             oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
 52 |             del self._cache[oldest_key]
 53 |         expires_at = datetime.utcnow() + timedelta(seconds=self.ttl_seconds)
 54 |         self._cache[key] = (value, expires_at)
 55 |     
 56 |     def clear(self) -> None:
 57 |         self._cache.clear()
 58 | 
 59 | # Global cache instances
 60 | dashboard_cache = TTLCache(ttl_seconds=300, maxsize=100)
 61 | calculation_cache = TTLCache(ttl_seconds=600, maxsize=50)
 62 | 
 63 | def cache_key(*args: Any, **kwargs: Any) -> str:
 64 |     """Generate cache key from function arguments."""
 65 |     key_data = json.dumps({"args": args, "kwargs": kwargs}, sort_keys=True, default=str)
 66 |     return hashlib.sha256(key_data.encode()).hexdigest()
 67 | 
 68 | def cached(cache: TTLCache) -> Callable[[Callable[..., T]], Callable[..., T]]:
 69 |     """Decorator for caching function results with TTL."""
 70 |     def decorator(func: Callable[..., T]) -> Callable[..., T]:
 71 |         @wraps(func)
 72 |         def wrapper(*args: Any, **kwargs: Any) -> T:
 73 |             key = f"{func.__name__}:{cache_key(*args, **kwargs)}"
 74 |             cached_value = cache.get(key)
 75 |             if cached_value is not None:
 76 |                 return cached_value
 77 |             result = func(*args, **kwargs)
 78 |             cache.set(key, result)
 79 |             return result
 80 |         return wrapper
 81 |     return decorator
 82 | ```
 83 | 
 84 | **File:** `apps/backend/src/rwa_dashboard/data.py` (modify)
 85 | 
 86 | ```python
 87 | # Add at top of file
 88 | from rwa_common.cache import cached, calculation_cache
 89 | 
 90 | # Modify current_rwa_snapshot function
 91 | @cached(calculation_cache)
 92 | def current_rwa_snapshot(as_of_date: date, row_limit: int | None = None) -> CurrentRwaSnapshot:
 93 |     """Calculate current Basel RWA and aggregate it for the dashboard.
 94 |     
 95 |     Results are cached for 10 minutes to avoid redundant calculations.
 96 |     """
 97 |     # ... existing implementation
 98 | ```
 99 | 
100 | **Expected Impact:** 80-90% latency reduction for cached requests
101 | 
102 | ---
103 | 
104 | ### 1.2 Response Compression
105 | 
106 | **File:** `apps/backend/src/rwa_dashboard/api.py` (modify)
107 | 
108 | ```python
109 | from fastapi import FastAPI
110 | from fastapi.middleware.gzip import GZIPMiddleware
111 | 
112 | def create_dashboard_app() -> FastAPI:
113 |     app = FastAPI(title="RWA Dashboard API")
114 |     
115 |     # Add compression middleware
116 |     app.add_middleware(
117 |         GZIPMiddleware,
118 |         minimum_size=1000,  # Only compress responses > 1KB
119 |         compresslevel=6     # Balance between speed and compression ratio
120 |     )
121 |     
122 |     # ... rest of app setup
123 | ```
124 | 
125 | **Expected Impact:** 60-70% payload size reduction, 20-30% latency improvement
126 | 
127 | ---
128 | 
129 | ### 1.3 Database Connection Pooling
130 | 
131 | **File:** `apps/backend/src/rwa_common/db.py` (modify)
132 | 
133 | ```python
134 | def create_database_engine(database_url: str | None = None) -> Engine:
135 |     """Create an SQLAlchemy engine with optimized connection pooling."""
136 |     resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
137 |     if resolved_url is None:
138 |         sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
139 |         resolved_url = f"sqlite+pysqlite:///{sqlite_path}"
140 |     
141 |     if resolved_url.startswith("sqlite"):
142 |         connect_args = {"check_same_thread": False}
143 |         if resolved_url.endswith(":memory:"):
144 |             return create_engine(
145 |                 resolved_url,
146 |                 connect_args=connect_args,
147 |                 poolclass=StaticPool,
148 |                 future=True,
149 |             )
150 |         return create_engine(
151 |             resolved_url,
152 |             connect_args=connect_args,
153 |             poolclass=NullPool,
154 |             future=True,
155 |         )
156 |     
157 |     # Production Postgres configuration with optimized pooling
158 |     return create_engine(
159 |         resolved_url,
160 |         pool_size=20,              # Increased from default 5
161 |         max_overflow=10,           # Allow burst capacity
162 |         pool_pre_ping=True,        # Verify connections before use
163 |         pool_recycle=3600,         # Recycle connections after 1 hour
164 |         echo_pool=False,           # Disable pool logging in production
165 |         future=True,
166 |     )
167 | ```
168 | 
169 | **Expected Impact:** 30-40% reduction in connection overhead
170 | 
171 | ---
172 | 
173 | ### 1.4 Request Timeouts
174 | 
175 | **File:** `apps/frontend/src/api/client.ts` (modify)
176 | 
177 | ```typescript
178 | const DEFAULT_API_BASE_URL = "/api";
179 | const DEFAULT_TIMEOUT_MS = 30000; // 30 seconds
180 | 
181 | export async function requestJson<T>(
182 |   path: string,
183 |   options: RequestInit & { signal?: AbortSignal; timeout?: number } = {},
184 | ): Promise<T> {
185 |   const timeout = options.timeout ?? DEFAULT_TIMEOUT_MS;
186 |   const controller = new AbortController();
187 |   const timeoutId = setTimeout(() => controller.abort(), timeout);
188 |   
189 |   try {
190 |     const response = await fetch(`${apiBaseUrl()}${path}`, {
191 |       ...options,
192 |       signal: options.signal ?? controller.signal,
193 |       headers: {
194 |         Accept: "application/json",
195 |         ...(options.body ? { "Content-Type": "application/json" } : {}),
196 |         ...options.headers,
197 |       },
198 |     });
199 | 
200 |     clearTimeout(timeoutId);
201 | 
202 |     if (!response.ok) {
203 |       throw new Error(await readErrorMessage(response));
204 |     }
205 | 
206 |     if (response.status === 204) {
207 |       return undefined as T;
208 |     }
209 | 
210 |     return (await response.json()) as T;
211 |   } catch (error) {
212 |     clearTimeout(timeoutId);
213 |     if (error instanceof Error && error.name === 'AbortError') {
214 |       throw new Error('Request timeout - please try again');
215 |     }
216 |     throw error;
217 |   }
218 | }
219 | ```
220 | 
221 | **Expected Impact:** Prevent hung requests, improve error handling
222 | 
223 | ---
224 | 
225 | ## Phase 2: Core Optimizations
226 | 
227 | ### 2.1 Pandas Optimization
228 | 
229 | **File:** `apps/backend/src/rwa_dashboard/data.py` (modify)
230 | 
231 | ```python
232 | def _calculator_results_frame(
233 |     source_rows: list[dict[str, Any]],
234 |     results: list[dict[str, Any]],
235 | ) -> pd.DataFrame:
236 |     """Join calculator output with input metadata and convert numeric values for charts.
237 |     
238 |     Optimized version using categorical dtypes and vectorized operations.
239 |     """
240 |     if not results:
241 |         return pd.DataFrame(columns=[*CORE_METADATA_COLUMNS, *RWA_FIELDS])
242 |     
243 |     # Use categorical dtypes for low-cardinality columns
244 |     metadata = pd.DataFrame(source_rows)[list(CORE_METADATA_COLUMNS)]
245 |     metadata['entity_class'] = metadata['entity_class'].astype('category')
246 |     metadata['sub_class'] = metadata['sub_class'].astype('category')
247 |     metadata['exposure_ccy'] = metadata['exposure_ccy'].astype('category')
248 |     metadata['incorporation_country'] = metadata['incorporation_country'].astype('category')
249 |     
250 |     output = pd.DataFrame(results)
251 |     frame = metadata.merge(output, on="id", how="inner")
252 |     
253 |     # Vectorized numeric conversion (faster than map)
254 |     numeric_cols = [*("exposure_amount", "residual_maturity", "counterparty_dlgd"), 
255 |                     *RWA_FIELDS, *RISK_WEIGHT_FIELDS]
256 |     for col in numeric_cols:
257 |         if col in frame.columns:
258 |             frame[col] = pd.to_numeric(frame[col], errors='coerce')
259 |     
260 |     # Vectorized ratio calculation
261 |     frame["rwa_density"] = frame[RWA_FINAL_FIELD].div(
262 |         frame["exposure_amount"].where(frame["exposure_amount"] != 0)
263 |     )
264 |     
265 |     return frame
266 | ```
267 | 
268 | **Expected Impact:** 40-60% reduction in data processing time
269 | 
270 | ---
271 | 
272 | ### 2.2 Async Database Operations
273 | 
274 | **File:** `apps/backend/src/rwa_common/db_async.py` (new)
275 | 
276 | ```python
277 | from __future__ import annotations
278 | 
279 | import os
280 | from collections.abc import AsyncGenerator
281 | from pathlib import Path
282 | from tempfile import gettempdir
283 | from uuid import uuid4
284 | 
285 | from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
286 | from sqlalchemy.orm import sessionmaker
287 | 
288 | DEFAULT_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
289 | 
290 | async def create_async_database_engine(database_url: str | None = None) -> AsyncEngine:
291 |     """Create an async SQLAlchemy engine for non-blocking database operations."""
292 |     resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
293 |     
294 |     if resolved_url is None:
295 |         sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
296 |         resolved_url = f"sqlite+aiosqlite:///{sqlite_path}"
297 |     
298 |     # Convert sync URLs to async
299 |     if resolved_url.startswith("sqlite+pysqlite"):
300 |         resolved_url = resolved_url.replace("sqlite+pysqlite", "sqlite+aiosqlite")
301 |     elif resolved_url.startswith("postgresql://"):
302 |         resolved_url = resolved_url.replace("postgresql://", "postgresql+asyncpg://")
303 |     
304 |     return create_async_engine(
305 |         resolved_url,
306 |         pool_size=20,
307 |         max_overflow=10,
308 |         pool_pre_ping=True,
309 |         pool_recycle=3600,
310 |         echo=False,
311 |         future=True,
312 |     )
313 | 
314 | def create_async_session_factory(engine: AsyncEngine) -> sessionmaker[AsyncSession]:
315 |     """Create an async session factory."""
316 |     return sessionmaker(
317 |         bind=engine,
318 |         class_=AsyncSession,
319 |         autoflush=False,
320 |         expire_on_commit=False,
321 |         future=True,
322 |     )
323 | 
324 | async def async_session_scope(
325 |     session_factory: sessionmaker[AsyncSession],
326 | ) -> AsyncGenerator[AsyncSession, None]:
327 |     """Yield an async request-scoped DB session."""
328 |     async with session_factory() as session:
329 |         yield session
330 | ```
331 | 
332 | **File:** `apps/backend/src/rwa_dashboard/repositories_async.py` (new)
333 | 
334 | ```python
335 | from __future__ import annotations
336 | 
337 | from datetime import UTC, date, datetime
338 | from typing import Any
339 | 
340 | from sqlalchemy import select
341 | from sqlalchemy.ext.asyncio import AsyncSession
342 | 
343 | from .models import RisktraceUiDataset
344 | 
345 | class AsyncRisktraceUiRepository:
346 |     """Async persistence gateway for frontend-facing RiskTrace data."""
347 | 
348 |     def __init__(self, session: AsyncSession) -> None:
349 |         self.session = session
350 | 
351 |     async def get_payload(self, dataset_key: str) -> dict[str, Any]:
352 |         """Fetch dataset payload asynchronously."""
353 |         result = await self.session.execute(
354 |             select(RisktraceUiDataset).where(RisktraceUiDataset.dataset_key == dataset_key)
355 |         )
356 |         dataset = result.scalar_one_or_none()
357 |         if dataset is None:
358 |             raise RisktraceDatasetNotFoundError(dataset_key)
359 |         return dict(dataset.payload)
360 | ```
361 | 
362 | **Expected Impact:** 50-70% throughput increase under load
363 | 
364 | ---
365 | 
366 | ### 2.3 Parallel Batch Processing
367 | 
368 | **File:** `apps/backend/src/rwa_steering/engine.py` (modify)
369 | 
370 | ```python
371 | from concurrent.futures import ProcessPoolExecutor, as_completed
372 | from typing import Any
373 | 
374 | class RwaSteeringService:
375 |     def __init__(self, *args, max_workers: int = 4, **kwargs):
376 |         super().__init__(*args, **kwargs)
377 |         self.max_workers = max_workers
378 |     
379 |     def _parallel_driver_deltas(
380 |         self,
381 |         request: SteeringRequest,
382 |         scenario: ScenarioAssumption,
383 |         projection_date: date,
384 |         current_total: Decimal,
385 |     ) -> dict[str, Decimal]:
386 |         """Calculate all attribution drivers in parallel."""
387 |         
388 |         drivers = [
389 |             ("volume_delta", {"apply_volume": True}),
390 |             ("maturity_delta", {"apply_maturity": True}),
391 |             ("rating_delta", {"apply_rating": True}),
392 |             ("dlgd_delta", {"apply_dlgd": True}),
393 |             ("fx_delta", {"apply_fx": True}),
394 |         ]
395 |         
396 |         with ProcessPoolExecutor(max_workers=self.max_workers) as executor:
397 |             futures = {
398 |                 executor.submit(
399 |                     self._driver_delta,
400 |                     request,
401 |                     scenario,
402 |                     projection_date,
403 |                     current_total,
404 |                     **flags
405 |                 ): name
406 |                 for name, flags in drivers
407 |             }
408 |             
409 |             results = {}
410 |             for future in as_completed(futures):
411 |                 driver_name = futures[future]
412 |                 results[driver_name] = future.result()
413 |         
414 |         return results
415 | ```
416 | 
417 | **Expected Impact:** 3-4x speedup on multi-core systems
418 | 
419 | ---
420 | 
421 | ## Phase 3: Advanced Optimizations
422 | 
423 | ### 3.1 Redis Caching Layer
424 | 
425 | **File:** `apps/backend/src/rwa_common/redis_cache.py` (new)
426 | 
427 | ```python
428 | from __future__ import annotations
429 | 
430 | import json
431 | import pickle
432 | from typing import Any
433 | from datetime import timedelta
434 | 
435 | try:
436 |     import redis
437 |     from redis import Redis
438 |     REDIS_AVAILABLE = True
439 | except ImportError:
440 |     REDIS_AVAILABLE = False
441 | 
442 | class RedisCache:
443 |     """Distributed cache using Redis for horizontal scalability."""
444 |     
445 |     def __init__(
446 |         self,
447 |         host: str = "localhost",
448 |         port: int = 6379,
449 |         db: int = 0,
450 |         password: str | None = None,
451 |         default_ttl: int = 300,
452 |     ):
453 |         if not REDIS_AVAILABLE:
454 |             raise RuntimeError("Redis not available - install redis-py")
455 |         
456 |         self.client: Redis = redis.Redis(
457 |             host=host,
458 |             port=port,
459 |             db=db,
460 |             password=password,
461 |             decode_responses=False,
462 |             socket_connect_timeout=5,
463 |             socket_timeout=5,
464 |         )
465 |         self.default_ttl = default_ttl
466 |     
467 |     def get(self, key: str) -> Any | None:
468 |         """Get value from cache."""
469 |         try:
470 |             value = self.client.get(key)
471 |             if value is None:
472 |                 return None
473 |             return pickle.loads(value)
474 |         except Exception:
475 |             return None
476 |     
477 |     def set(self, key: str, value: Any, ttl: int | None = None) -> bool:
478 |         """Set value in cache with TTL."""
479 |         try:
480 |             serialized = pickle.dumps(value)
481 |             ttl_seconds = ttl or self.default_ttl
482 |             return self.client.setex(key, timedelta(seconds=ttl_seconds), serialized)
483 |         except Exception:
484 |             return False
485 |     
486 |     def delete(self, key: str) -> bool:
487 |         """Delete key from cache."""
488 |         try:
489 |             return bool(self.client.delete(key))
490 |         except Exception:
491 |             return False
492 |     
493 |     def clear_pattern(self, pattern: str) -> int:
494 |         """Clear all keys matching pattern."""
495 |         try:
496 |             keys = self.client.keys(pattern)
497 |             if keys:
498 |                 return self.client.delete(*keys)
499 |             return 0
500 |         except Exception:
501 |             return 0
502 | ```
503 | 
504 | **Expected Impact:** Horizontal scalability, 95%+ cache hit rate
505 | 
506 | ---
507 | 
508 | ### 3.2 Request Deduplication
509 | 
510 | **File:** `apps/frontend/src/hooks/useApiResource.ts` (modify)
511 | 
512 | ```typescript
513 | import { useEffect, useState, useRef } from "react";
514 | 
515 | // Global request cache
516 | const requestCache = new Map<string, Promise<any>>();
517 | const responseCache = new Map<string, { data: any; timestamp: number }>();
518 | const CACHE_TTL_MS = 60000; // 1 minute
519 | 
520 | export function useApiResource<T>(
521 |   load: (signal: AbortSignal) => Promise<T>,
522 |   deps: unknown[] = [],
523 |   options: { enabled?: boolean; cacheKey?: string; cacheTTL?: number } = {},
524 | ) {
525 |   const enabled = options.enabled ?? true;
526 |   const cacheKey = options.cacheKey;
527 |   const cacheTTL = options.cacheTTL ?? CACHE_TTL_MS;
528 |   
529 |   const [state, setState] = useState<ApiResourceState<T>>({
530 |     data: null,
531 |     error: null,
532 |     isLoading: enabled,
533 |   });
534 | 
535 |   useEffect(() => {
536 |     if (!enabled) {
537 |       setState((current) => ({ ...current, isLoading: false }));
538 |       return;
539 |     }
540 | 
541 |     // Check response cache first
542 |     if (cacheKey) {
543 |       const cached = responseCache.get(cacheKey);
544 |       if (cached && Date.now() - cached.timestamp < cacheTTL) {
545 |         setState({ data: cached.data, error: null, isLoading: false });
546 |         return;
547 |       }
548 |     }
549 | 
550 |     const controller = new AbortController();
551 |     setState((current) => ({ ...current, error: null, isLoading: true }));
552 | 
553 |     // Deduplicate in-flight requests
554 |     const executeLoad = async () => {
555 |       if (cacheKey && requestCache.has(cacheKey)) {
556 |         return requestCache.get(cacheKey)!;
557 |       }
558 | 
559 |       const promise = load(controller.signal);
560 |       if (cacheKey) {
561 |         requestCache.set(cacheKey, promise);
562 |       }
563 | 
564 |       try {
565 |         const result = await promise;
566 |         if (cacheKey) {
567 |           responseCache.set(cacheKey, { data: result, timestamp: Date.now() });
568 |           requestCache.delete(cacheKey);
569 |         }
570 |         return result;
571 |       } catch (error) {
572 |         if (cacheKey) {
573 |           requestCache.delete(cacheKey);
574 |         }
575 |         throw error;
576 |       }
577 |     };
578 | 
579 |     executeLoad()
580 |       .then((data) => {
581 |         if (!controller.signal.aborted) {
582 |           setState({ data, error: null, isLoading: false });
583 |         }
584 |       })
585 |       .catch((error: unknown) => {
586 |         if (controller.signal.aborted) {
587 |           return;
588 |         }
589 |         setState({
590 |           data: null,
591 |           error: error instanceof Error ? error.message : "REST API unavailable",
592 |           isLoading: false,
593 |         });
594 |       });
595 | 
596 |     return () => controller.abort();
597 |   }, [enabled, cacheKey, cacheTTL, ...deps]);
598 | 
599 |   return state;
600 | }
601 | ```
602 | 
603 | **Expected Impact:** 50-60% reduction in redundant API calls
604 | 
605 | ---
606 | 
607 | ## Testing & Validation
608 | 
609 | ### Performance Test Suite
610 | 
611 | **File:** `apps/backend/tests/performance/test_dashboard_performance.py` (new)
612 | 
613 | ```python
614 | import pytest
615 | import time
616 | from datetime import date
617 | 
618 | from rwa_dashboard.data import current_rwa_snapshot
619 | 
620 | @pytest.mark.performance
621 | def test_dashboard_snapshot_latency():
622 |     """Verify dashboard snapshot completes within SLO."""
623 |     start = time.perf_counter()
624 |     snapshot = current_rwa_snapshot(date(2026, 1, 1))
625 |     duration_ms = (time.perf_counter() - start) * 1000
626 |     
627 |     assert duration_ms < 500, f"Dashboard snapshot took {duration_ms:.0f}ms (SLO: 500ms)"
628 |     assert not snapshot.results.empty
629 | 
630 | @pytest.mark.performance
631 | def test_dashboard_snapshot_cached():
632 |     """Verify cached requests are fast."""
633 |     # First call (cache miss)
634 |     current_rwa_snapshot(date(2026, 1, 1))
635 |     
636 |     # Second call (cache hit)
637 |     start = time.perf_counter()
638 |     current_rwa_snapshot(date(2026, 1, 1))
639 |     duration_ms = (time.perf_counter() - start) * 1000
640 |     
641 |     assert duration_ms < 50, f"Cached snapshot took {duration_ms:.0f}ms (expected <50ms)"
642 | ```
643 | 
644 | ### Load Test Enhancement
645 | 
646 | **File:** `k6/performance-test.js` (new)
647 | 
648 | ```javascript
649 | import http from "k6/http";
650 | import { check, sleep } from "k6";
651 | import { Rate, Trend } from "k6/metrics";
652 | 
653 | const errorRate = new Rate("errors");
654 | const dashboardLatency = new Trend("dashboard_p95_latency", true);
655 | const cacheHitRate = new Rate("cache_hits");
656 | 
657 | export const options = {
658 |   scenarios: {
659 |     performance_test: {
660 |       executor: "ramping-vus",
661 |       startVUs: 0,
662 |       stages: [
663 |         { duration: "1m", target: 20 },
664 |         { duration: "3m", target: 50 },
665 |         { duration: "1m", target: 0 },
666 |       ],
667 |     },
668 |   },
669 |   thresholds: {
670 |     "dashboard_p95_latency": ["p(95)<500"],
671 |     "http_req_duration": ["p(95)<1000"],
672 |     "errors": ["rate<0.001"],
673 |     "cache_hits": ["rate>0.80"],
674 |   },
675 | };
676 | 
677 | const BASE_URL = __ENV.TARGET_URL || "http://localhost:8000";
678 | 
679 | export default function () {
680 |   const res = http.get(`${BASE_URL}/v1/dashboard/snapshot`);
681 |   
682 |   check(res, {
683 |     "status 200": (r) => r.status === 200,
684 |     "latency <500ms": (r) => r.timings.duration < 500,
685 |   });
686 |   
687 |   dashboardLatency.add(res.timings.duration);
688 |   errorRate.add(res.status !== 200);
689 |   
690 |   // Check for cache hit header
691 |   const cacheHit = res.headers["X-Cache-Hit"] === "true";
692 |   cacheHitRate.add(cacheHit);
693 |   
694 |   sleep(1);
695 | }
696 | ```
697 | 
698 | ---
699 | 
700 | ## Deployment Checklist
701 | 
702 | - [ ] Run full test suite
703 | - [ ] Run performance benchmarks
704 | - [ ] Deploy to dev environment
705 | - [ ] Validate metrics in dev
706 | - [ ] Deploy to staging
707 | - [ ] Run load tests in staging
708 | - [ ] Deploy to 10% production
709 | - [ ] Monitor for 24 hours
710 | - [ ] Deploy to 100% production
711 | - [ ] Document results
712 | 
713 | ## Monitoring Alerts
714 | 
715 | ```yaml
716 | # Prometheus alert rules
717 | groups:
718 |   - name: performance
719 |     rules:
720 |       - alert: HighLatency
721 |         expr: histogram_quantile(0.95, rwa_request_duration_seconds) > 0.5
722 |         for: 5m
723 |         annotations:
724 |           summary: "p95 latency above SLO"
725 |       
726 |       - alert: LowCacheHitRate
727 |         expr: rate(rwa_cache_hits_total[5m]) / rate(rwa_cache_requests_total[5m]) < 0.80
728 |         for: 10m
729 |         annotations:
730 |           summary: "Cache hit rate below 80%"
731 | ```
732 | 
733 | ---
734 | 
735 | **Next:** Switch to Code mode to implement these optimizations
</content>
</file>
<file><path>docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md</path>
<content lines="1-282">
  1 | # Performance Optimization Summary
  2 | 
  3 | **Project:** RiskTrace Control Tower  
  4 | **Date:** 2026-05-17  
  5 | **Status:** Ready for Implementation
  6 | 
  7 | ## Overview
  8 | 
  9 | This document summarizes the performance optimization analysis and provides a roadmap for implementation.
 10 | 
 11 | ## Key Findings
 12 | 
 13 | ### Top 3 Performance Bottlenecks Identified
 14 | 
 15 | #### 1. **Expensive RWA Calculations Without Caching** (CRITICAL)
 16 | - **Location:** [`apps/backend/src/rwa_dashboard/data.py:127-145`](../apps/backend/src/rwa_dashboard/data.py)
 17 | - **Issue:** `current_rwa_snapshot()` recalculates entire portfolio on every dashboard request
 18 | - **Impact:** Estimated 2000-3000ms p95 latency
 19 | - **Solution:** Implement TTL-based caching with 5-10 minute expiration
 20 | - **Expected Improvement:** 80-90% latency reduction
 21 | 
 22 | #### 2. **Synchronous Database Operations** (HIGH)
 23 | - **Location:** [`apps/backend/src/rwa_dashboard/repositories.py`](../apps/backend/src/rwa_dashboard/repositories.py)
 24 | - **Issue:** Blocking database calls, no connection pooling optimization
 25 | - **Impact:** Connection overhead, limited concurrency
 26 | - **Solution:** Async database operations + optimized connection pool
 27 | - **Expected Improvement:** 50-70% throughput increase
 28 | 
 29 | #### 3. **Inefficient Pandas Operations** (HIGH)
 30 | - **Location:** [`apps/backend/src/rwa_dashboard/data.py:373-521`](../apps/backend/src/rwa_dashboard/data.py)
 31 | - **Issue:** Non-vectorized operations, missing categorical dtypes, deep copies
 32 | - **Impact:** High CPU usage, memory pressure
 33 | - **Solution:** Vectorize operations, use categorical dtypes, eliminate copies
 34 | - **Expected Improvement:** 40-60% processing time reduction
 35 | 
 36 | ## Optimization Strategy
 37 | 
 38 | ### Phase 1: Quick Wins (Week 1)
 39 | **Estimated Impact:** 75-85% latency reduction
 40 | 
 41 | 1. ✅ **Response Caching** - TTL-based LRU cache for calculations
 42 | 2. ✅ **Response Compression** - GZip middleware for API responses
 43 | 3. ✅ **Database Pooling** - Optimize connection pool configuration
 44 | 4. ✅ **Request Timeouts** - Add timeout handling to prevent hung requests
 45 | 
 46 | ### Phase 2: Core Optimizations (Week 2-3)
 47 | **Estimated Impact:** Additional 10-15% improvement
 48 | 
 49 | 5. ✅ **Calculation Caching** - Cache expensive RWA calculations
 50 | 6. ✅ **Pandas Optimization** - Vectorize operations, categorical dtypes
 51 | 7. ✅ **Async Database** - Non-blocking database operations
 52 | 8. ✅ **Batch Processing** - Parallelize independent calculations
 53 | 
 54 | ### Phase 3: Advanced (Week 4)
 55 | **Estimated Impact:** Horizontal scalability
 56 | 
 57 | 9. ✅ **Redis Cache** - Distributed caching for multi-instance deployments
 58 | 10. ✅ **Pagination** - Limit response sizes for large datasets
 59 | 11. ✅ **Request Deduplication** - Eliminate redundant frontend calls
 60 | 12. ✅ **CSV Preloading** - Load reference data at startup
 61 | 
 62 | ## Expected Performance Improvements
 63 | 
 64 | ### Conservative Estimates
 65 | 
 66 | | Metric | Baseline | Target | Improvement |
 67 | |--------|----------|--------|-------------|
 68 | | Dashboard p95 latency | 2000-3000ms | <500ms | **75-85%** |
 69 | | Calculation p95 latency | 1500-2500ms | <300ms | **80-88%** |
 70 | | Throughput (RPS) | 10-20 | 50-100 | **250-500%** |
 71 | | Error rate | 1-2% | <0.1% | **90-95%** |
 72 | 
 73 | ### Aggressive Estimates (All Phases)
 74 | 
 75 | | Metric | Target | Improvement |
 76 | |--------|--------|-------------|
 77 | | Dashboard p95 latency | <200ms | **90-93%** |
 78 | | Calculation p95 latency | <150ms | **93-95%** |
 79 | | Throughput (RPS) | 100-200 | **500-1000%** |
 80 | | Cache hit rate | >95% | N/A |
 81 | 
 82 | ## Architecture Changes
 83 | 
 84 | ### New Components
 85 | 
 86 | ```
 87 | apps/backend/src/rwa_common/
 88 | ├── cache.py              # TTL-based caching utilities
 89 | ├── redis_cache.py        # Redis distributed cache
 90 | ├── db_async.py           # Async database engine
 91 | └── monitoring.py         # Prometheus metrics
 92 | 
 93 | apps/backend/src/rwa_dashboard/
 94 | └── repositories_async.py # Async repository layer
 95 | 
 96 | apps/backend/tests/performance/
 97 | ├── test_dashboard_performance.py
 98 | ├── test_caching.py
 99 | └── test_database_pool.py
100 | 
101 | k6/
102 | └── performance-test.js   # Enhanced load tests
103 | ```
104 | 
105 | ### Modified Components
106 | 
107 | - [`apps/backend/src/rwa_common/db.py`](../apps/backend/src/rwa_common/db.py) - Optimized pooling
108 | - [`apps/backend/src/rwa_dashboard/data.py`](../apps/backend/src/rwa_dashboard/data.py) - Caching + pandas optimization
109 | - [`apps/backend/src/rwa_dashboard/service.py`](../apps/backend/src/rwa_dashboard/service.py) - Remove deep copies
110 | - [`apps/backend/src/rwa_steering/engine.py`](../apps/backend/src/rwa_steering/engine.py) - Parallel processing
111 | - [`apps/frontend/src/api/client.ts`](../apps/frontend/src/api/client.ts) - Timeouts
112 | - [`apps/frontend/src/hooks/useApiResource.ts`](../apps/frontend/src/hooks/useApiResource.ts) - Deduplication
113 | 
114 | ## Compliance & Security
115 | 
116 | ### ✅ Maintained Controls
117 | 
118 | - All validation logic preserved
119 | - Audit logging unchanged
120 | - Regulatory checks intact
121 | - Security controls maintained
122 | - Data integrity guarantees preserved
123 | 
124 | ### 🔒 New Security Considerations
125 | 
126 | - Cache encryption for sensitive data
127 | - Redis authentication and TLS
128 | - Rate limiting to prevent abuse
129 | - Cache poisoning prevention
130 | 
131 | ## Risk Assessment
132 | 
133 | ### Low Risk Changes
134 | - Response compression (standard middleware)
135 | - Request timeouts (defensive programming)
136 | - Database pooling (configuration only)
137 | - Pandas optimization (performance only)
138 | 
139 | ### Medium Risk Changes
140 | - Response caching (requires invalidation strategy)
141 | - Async database operations (requires refactoring)
142 | - Batch processing (state management complexity)
143 | 
144 | ### Mitigation Strategy
145 | - Feature flags for all optimizations
146 | - Gradual rollout (dev → staging → 10% prod → 100%)
147 | - Real-time monitoring with automatic rollback
148 | - Comprehensive testing at each stage
149 | 
150 | ## Implementation Roadmap
151 | 
152 | ### Week 1: Quick Wins
153 | - **Day 1-2:** Implement caching infrastructure
154 | - **Day 3:** Add compression and timeouts
155 | - **Day 4:** Optimize database pooling
156 | - **Day 5:** Testing and validation
157 | 
158 | ### Week 2-3: Core Optimizations
159 | - **Day 6-8:** Calculation caching
160 | - **Day 9-11:** Pandas optimizations
161 | - **Day 12-14:** Async database layer
162 | - **Day 15:** Batch processing
163 | 
164 | ### Week 4: Advanced & Polish
165 | - **Day 16-18:** Redis integration
166 | - **Day 19-20:** Pagination and deduplication
167 | - **Day 21-22:** CSV preloading
168 | - **Day 23-24:** Performance testing
169 | - **Day 25:** Documentation and handoff
170 | 
171 | ## Success Criteria
172 | 
173 | 1. ✅ p95 latency <500ms for all dashboard endpoints
174 | 2. ✅ p99 latency <1000ms for all endpoints
175 | 3. ✅ Error rate <0.1%
176 | 4. ✅ Throughput >50 RPS sustained
177 | 5. ✅ All existing tests pass
178 | 6. ✅ No calculation result changes
179 | 7. ✅ Memory usage increase <30%
180 | 8. ✅ Zero security regressions
181 | 
182 | ## Monitoring & Observability
183 | 
184 | ### Key Metrics
185 | 
186 | **Latency:**
187 | - `rwa_request_duration_seconds{endpoint, method, status}` - Request duration histogram
188 | - `rwa_calculation_duration_seconds{calculation_type}` - Calculation duration
189 | 
190 | **Throughput:**
191 | - `rwa_requests_total{endpoint}` - Total request counter
192 | - `rwa_concurrent_requests` - Active request gauge
193 | 
194 | **Caching:**
195 | - `rwa_cache_hits_total{cache_type}` - Cache hit counter
196 | - `rwa_cache_misses_total{cache_type}` - Cache miss counter
197 | - `rwa_cache_size{cache_type}` - Cache size gauge
198 | 
199 | **Database:**
200 | - `rwa_db_pool_size` - Connection pool size
201 | - `rwa_db_pool_overflow` - Overflow connections
202 | - `rwa_db_query_duration_seconds` - Query duration
203 | 
204 | ### Alerts
205 | 
206 | ```yaml
207 | - alert: HighLatency
208 |   expr: histogram_quantile(0.95, rwa_request_duration_seconds) > 0.5
209 |   for: 5m
210 | 
211 | - alert: LowCacheHitRate
212 |   expr: rate(rwa_cache_hits_total[5m]) / rate(rwa_cache_requests_total[5m]) < 0.80
213 |   for: 10m
214 | 
215 | - alert: DatabasePoolExhaustion
216 |   expr: rwa_db_pool_overflow > 5
217 |   for: 5m
218 | ```
219 | 
220 | ## Testing Strategy
221 | 
222 | ### 1. Unit Tests
223 | - Cache behavior validation
224 | - Pandas optimization correctness
225 | - Async operation handling
226 | 
227 | ### 2. Integration Tests
228 | - End-to-end request flows
229 | - Database connection pooling
230 | - Cache invalidation
231 | 
232 | ### 3. Performance Tests
233 | - Baseline measurement
234 | - Load testing (k6)
235 | - Stress testing
236 | - Soak testing (24h)
237 | 
238 | ### 4. Regression Tests
239 | - Calculation result validation
240 | - API contract compliance
241 | - Security control verification
242 | 
243 | ## Rollback Plan
244 | 
245 | ### Triggers
246 | - p95 latency increases >20% from baseline
247 | - Error rate increases >1%
248 | - Memory usage increases >50%
249 | - Any calculation result discrepancies
250 | 
251 | ### Procedure
252 | 1. Toggle feature flag to disable optimization
253 | 2. Monitor metrics for 5 minutes
254 | 3. If stable, investigate root cause
255 | 4. If unstable, full rollback via deployment
256 | 
257 | ### Recovery Time Objective
258 | - **RTO:** <5 minutes (feature flag toggle)
259 | - **RPO:** 0 (no data loss)
260 | 
261 | ## Next Steps
262 | 
263 | 1. ✅ **Review and approve plan** - Stakeholder sign-off
264 | 2. 🔄 **Switch to Code mode** - Begin implementation
265 | 3. ⏳ **Phase 1 implementation** - Quick wins
266 | 4. ⏳ **Measure and validate** - Confirm improvements
267 | 5. ⏳ **Phase 2 implementation** - Core optimizations
268 | 6. ⏳ **Phase 3 implementation** - Advanced features
269 | 7. ⏳ **Production deployment** - Gradual rollout
270 | 8. ⏳ **Post-deployment monitoring** - Validate success
271 | 
272 | ## Documentation
273 | 
274 | - ✅ [`PERFORMANCE_OPTIMIZATION_PLAN.md`](./PERFORMANCE_OPTIMIZATION_PLAN.md) - Detailed strategy
275 | - ✅ [`PERFORMANCE_IMPLEMENTATION_GUIDE.md`](./PERFORMANCE_IMPLEMENTATION_GUIDE.md) - Code examples
276 | - ✅ [`PERFORMANCE_OPTIMIZATION_SUMMARY.md`](./PERFORMANCE_OPTIMIZATION_SUMMARY.md) - This document
277 | 
278 | ---
279 | 
280 | **Prepared by:** Performance Engineering Team  
281 | **Approved by:** _Pending_  
282 | **Implementation Start:** _Pending approval_
</content>
</file>
<file><path>mcps/EXECUTION_PLAN.md</path>
<content lines="1-561">
  1 | # MCP Infrastructure Execution Plan
  2 | 
  3 | **Version:** 1.0  
  4 | **Last Updated:** 2026-05-17  
  5 | **Status:** Production Ready
  6 | 
  7 | ---
  8 | 
  9 | ## ⚠️ CRITICAL SAFETY DISCLAIMERS
 10 | 
 11 | **READ THIS FIRST - LEGAL AND COMPLIANCE NOTICE**
 12 | 
 13 | This MCP infrastructure provides **engineering controls and technical guidance only**. It is **NOT**:
 14 | 
 15 | - ❌ A source of legal advice or regulatory interpretation
 16 | - ❌ A regulatory compliance certification tool
 17 | - ❌ A substitute for qualified legal, compliance, or risk review
 18 | - ❌ A guarantee of regulatory compliance
 19 | 
 20 | **MANDATORY REQUIREMENTS:**
 21 | 
 22 | 1. **All regulatory mappings, controls, evidence requirements, and release readiness decisions MUST be reviewed by qualified compliance, legal, or risk specialists before production use.**
 23 | 2. **The regulatory corpus is for reference only and may not be complete, current, or applicable to your specific jurisdiction or circumstances.**
 24 | 3. **Users are solely responsible for ensuring compliance with all applicable regulations.**
 25 | 4. **Always consult qualified legal and compliance professionals for regulatory matters.**
 26 | 5. **This tool does not replace human judgment, legal expertise, or regulatory consultation.**
 27 | 
 28 | **Control Reference:** This execution plan supports control **REL-EVID-001** (Release Evidence Package) by providing structured guidance for evidence collection and release readiness assessment.
 29 | 
 30 | ---
 31 | 
 32 | ## Table of Contents
 33 | 
 34 | 1. [Executive Summary](#executive-summary)
 35 | 2. [MVP Scope - What's Included](#mvp-scope---whats-included)
 36 | 3. [Non-Goals - Explicitly Out of Scope](#non-goals---explicitly-out-of-scope)
 37 | 4. [Step-by-Step Execution Plan](#step-by-step-execution-plan)
 38 | 5. [Demo Commands and Smoke Tests](#demo-commands-and-smoke-tests)
 39 | 6. [Troubleshooting Guide](#troubleshooting-guide)
 40 | 7. [Integration with CI/CD](#integration-with-cicd)
 41 | 8. [Maintenance and Updates](#maintenance-and-updates)
 42 | 9. [Decision Trees](#decision-trees)
 43 | 10. [Additional Resources](#additional-resources)
 44 | 
 45 | ---
 46 | 
 47 | ## Executive Summary
 48 | 
 49 | ### Purpose
 50 | 
 51 | The RiskTrace Control Tower MCP infrastructure provides a **local-first, deterministic, privacy-focused** suite of tools for regulatory compliance checking, code quality analysis, security scanning, and dependency vulnerability assessment. It enables developers, compliance officers, and auditors to integrate regulatory controls directly into the software development lifecycle.
 52 | 
 53 | ### Business Value Proposition
 54 | 
 55 | **For Developers:**
 56 | - Catch regulatory compliance issues during development, not in production
 57 | - Get instant feedback on code changes against 15+ engineering controls
 58 | - Automate evidence collection for audit trails
 59 | - Reduce rework by identifying issues early
 60 | 
 61 | **For Compliance Officers:**
 62 | - Automated mapping of code changes to regulatory requirements
 63 | - Structured evidence packages for audit readiness
 64 | - Consistent application of controls across all development work
 65 | - Traceability from regulation to implementation
 66 | 
 67 | **For Auditors:**
 68 | - Complete audit trail of regulatory decisions
 69 | - Evidence packages linked to specific releases
 70 | - Automated test results and approval records
 71 | - Clear mapping between regulations, controls, and implementations
 72 | 
 73 | ### Target Audience
 74 | 
 75 | - **Primary:** Software engineers working on RWA calculation and banking systems
 76 | - **Secondary:** Compliance officers, risk managers, and internal auditors
 77 | - **Tertiary:** Technical leads, architects, and release managers
 78 | 
 79 | ### Key Capabilities
 80 | 
 81 | - **15 regulatory compliance tools** for feature review, code review, and release readiness
 82 | - **9 regulations** covering EU banking (CRR3, EBA), data protection (GDPR), operational resilience (DORA), and internal policies
 83 | - **15+ engineering controls** for RWA calculations, data quality, security, and audit trails
 84 | - **4 MCP services** orchestrated via Docker Compose
 85 | - **IBM Bob AI integration** for conversational compliance checking
 86 | 
 87 | ---
 88 | 
 89 | ## MVP Scope - What's Included
 90 | 
 91 | ### Core Capabilities
 92 | 
 93 | #### 1. Regulatory Compliance Checking (15 Tools)
 94 | 
 95 | The `bank-regulatory-controls-mcp` service provides:
 96 | 
 97 | | Tool | Purpose | Use Case |
 98 | |------|---------|----------|
 99 | | `health_check` | Verify MCP connectivity and corpus status | Smoke testing, troubleshooting |
100 | | `get_regulatory_profile` | Get applicable regulations for a domain | Initial project setup |
101 | | `search_regulations` | Find regulations by keyword or domain | Research, planning |
102 | | `match_controls` | Match engineering controls to artifacts | Feature planning, code review |
103 | | `review_feature_description` | Review feature specs for compliance | Story creation, sprint planning |
104 | | `review_architecture_text` | Review architecture for regulatory gaps | Design reviews, ADRs |
105 | | `review_code_diff` | Review code changes for compliance issues | Pull requests, code review |
106 | | `generate_acceptance_criteria` | Generate regulatory acceptance criteria | Story refinement |
107 | | `generate_data_lineage_requirements` | Generate data lineage requirements | Data architecture |
108 | | `generate_audit_log_requirements` | Generate audit logging requirements | Security design |
109 | | `generate_test_obligations` | Generate regulatory test requirements | Test planning |
110 | | `assess_release_readiness` | Assess if release meets regulatory requirements | Release gates |
111 | | `generate_regulatory_mapping_report` | Generate compliance mapping report | Audit preparation |
112 | | `generate_rwa_run_evidence_requirements` | Generate RWA calculation evidence requirements | Production runs |
113 | | `explain_control` | Get detailed explanation of a control | Learning, training |
114 | 
115 | #### 2. Code Quality Analysis (SonarQube)
116 | 
117 | - **Local SonarQube instance** with Postgres backend
118 | - **Two pre-configured projects:**
119 |   - `risktrace-control-tower-backend` (Python)
120 |   - `risktrace-control-tower-frontend` (TypeScript/React)
121 | - **Automated token management** via `sonarqube-init` service
122 | - **MCP integration** via `sonarqube-mcp` for Bob queries
123 | - **Quality gates** for code coverage, bugs, vulnerabilities, code smells
124 | 
125 | #### 3. Security Scanning (OWASP ZAP)
126 | 
127 | - **ZAP daemon** running at `http://127.0.0.1:8090`
128 | - **MCP Integration add-on** exposed at `http://127.0.0.1:8282`
129 | - **Manual scan control** - no automated background scanning
130 | - **Target configuration** via `ZAP_MCP_TARGET_URL` (default: `http://127.0.0.1:5173`)
131 | - **Security key authentication** for MCP access
132 | 
133 | #### 4. Dependency Vulnerability Scanning (Sonatype Guide)
134 | 
135 | - **Remote MCP service** via `mcp-remote`
136 | - **Token-based authentication**
137 | - **Dependency vulnerability analysis**
138 | - **License compliance checking**
139 | - **Remediation guidance**
140 | 
141 | ### Regulatory Coverage
142 | 
143 | #### EU Banking Regulations
144 | 
145 | 1. **CRR3 / CRD6** - Capital Requirements Regulation III
146 | 2. **EBA Reporting Framework 4.0**
147 | 3. **BCBS 239** - Principles for Effective Risk Data Aggregation
148 | 
149 | #### Operational Resilience
150 | 
151 | 4. **DORA** - Digital Operational Resilience Act
152 | 5. **EBA ICT and Security Risk Management**
153 | 
154 | #### Data Protection
155 | 
156 | 6. **GDPR** - General Data Protection Regulation
157 | 
158 | #### Internal Policies
159 | 
160 | 7. **INTERNAL_SDLC** - Software Development Lifecycle Policy
161 | 8. **INTERNAL_AUDIT_EVIDENCE** - Audit Evidence Policy
162 | 9. **INTERNAL_RULE_GOVERNANCE** - Rule Governance Policy
163 | 
164 | ### Integration Points
165 | 
166 | - **IBM Bob AI Assistant** via `.bob/mcp.json`
167 | - **GitHub Copilot** context-aware suggestions
168 | - **Docker Compose** orchestration with profiles
169 | - **Local development workflow** integration
170 | 
171 | ---
172 | 
173 | ## Non-Goals - Explicitly Out of Scope
174 | 
175 | ### ❌ Jira API Integration
176 | - **Not included:** Automated ticket creation or tracking
177 | - **Alternative:** Bob generates Jira-ready content for manual copy-paste
178 | 
179 | ### ❌ LLM Inside MCP
180 | - **Not included:** AI inference or natural language generation
181 | - **Architecture:** MCP provides data/tools, Bob provides intelligence
182 | 
183 | ### ❌ Automated Background Scanners
184 | - **Not included:** Continuous scanning or scheduled analysis
185 | - **Alternative:** Developer-initiated scans via Docker Compose
186 | 
187 | ### ❌ Kubernetes Deployment
188 | - **Not included:** Production orchestration
189 | - **Scope:** Local development tool only
190 | 
191 | ### ❌ Legal Research Capabilities
192 | - **Not included:** Legal document search or regulatory interpretation
193 | - **Critical:** Engineering controls ≠ legal advice
194 | 
195 | ### ❌ Real-Time Compliance Monitoring
196 | - **Not included:** Production monitoring or runtime alerting
197 | - **Scope:** Pre-production compliance checking only
198 | 
199 | ---
200 | 
201 | ## Step-by-Step Execution Plan
202 | 
203 | ### Phase 1: Initial Setup (15 minutes)
204 | 
205 | #### Prerequisites Check
206 | 
207 | ```bash
208 | # Check Docker
209 | docker --version
210 | # Required: Docker 20.10+
211 | 
212 | # Check Docker Compose
213 | docker compose version
214 | # Required: Docker Compose v2.0+
215 | 
216 | # Check Node.js
217 | node --version
218 | # Required: Node.js 20+
219 | 
220 | # Check disk space
221 | df -h
222 | # Required: 5GB+ free
223 | ```
224 | 
225 | #### Step 1.1: Navigate to MCP Directory
226 | 
227 | ```bash
228 | cd risk-trace-control-tower/mcps
229 | ```
230 | 
231 | #### Step 1.2: Configure Environment Secrets
232 | 
233 | ```bash
234 | # Copy example file
235 | cp .env.example .env
236 | 
237 | # Generate secure keys
238 | openssl rand -hex 32
239 | 
240 | # Edit .env and replace all <placeholder> values
241 | nano .env
242 | ```
243 | 
244 | **Required secrets:**
245 | - `SONARQUBE_ADMIN_PASSWORD`
246 | - `SONAR_POSTGRES_PASSWORD`
247 | - `ZAP_API_KEY`
248 | - `ZAP_MCP_SECURITY_KEY`
249 | - `SONATYPE_GUIDE_MCP_TOKEN`
250 | 
251 | #### Step 1.3: Start SonarQube
252 | 
253 | ```bash
254 | # Start SonarQube and database
255 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d sonarqube
256 | 
257 | # Wait for healthy status (2-3 minutes)
258 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml ps sonarqube
259 | ```
260 | 
261 | #### Step 1.4: Initialize SonarQube
262 | 
263 | ```bash
264 | # Create projects and generate token
265 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile setup run --rm -T sonarqube-init
266 | ```
267 | 
268 | **Expected output:**
269 | ```
270 | SonarQube is UP.
271 | Created SonarQube project: risktrace-control-tower-backend
272 | Created SonarQube project: risktrace-control-tower-frontend
273 | Wrote SonarQube MCP credentials to /run/risktrace-mcp/sonarqube.env.
274 | ```
275 | 
276 | #### Step 1.5: Verify SonarQube
277 | 
278 | ```bash
279 | # Open in browser
280 | open http://127.0.0.1:9000
281 | 
282 | # Login: admin / <your password>
283 | ```
284 | 
285 | ---
286 | 
287 | ### Phase 2: MCP Service Startup (5 minutes)
288 | 
289 | #### Step 2.1: Build Regulatory MCP
290 | 
291 | ```bash
292 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml build bank-regulatory-controls-mcp
293 | ```
294 | 
295 | #### Step 2.2: Test MCP Standalone
296 | 
297 | ```bash
298 | echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | \
299 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp
300 | ```
301 | 
302 | ---
303 | 
304 | ### Phase 3: Bob Integration (10 minutes)
305 | 
306 | #### Step 3.1: Configure Bob MCP
307 | 
308 | ```bash
309 | cd ..
310 | cp .bob/mcp.example.json .bob/mcp.json
311 | ```
312 | 
313 | See [mcps/README.md](README.md) for complete `.bob/mcp.json` configuration.
314 | 
315 | #### Step 3.2: Test Bob Connection
316 | 
317 | ```
318 | Bob, call bankRegulatoryControls.health_check with include_corpus: true
319 | ```
320 | 
321 | ---
322 | 
323 | ### Phase 4: Development Workflow (Ongoing)
324 | 
325 | #### Feature Planning Workflow
326 | 
327 | 1. Review feature description with Bob
328 | 2. Generate acceptance criteria
329 | 3. Generate test obligations
330 | 4. Document in ticket system
331 | 
332 | #### Code Review Workflow
333 | 
334 | 1. Review code diff with Bob
335 | 2. Run SonarQube scan
336 | 3. Address blocking findings
337 | 4. Approve PR
338 | 
339 | #### Release Workflow
340 | 
341 | 1. Assess release readiness
342 | 2. Generate regulatory mapping report
343 | 3. Collect evidence package
344 | 4. Submit for compliance review
345 | 
346 | ---
347 | 
348 | ## Demo Commands and Smoke Tests
349 | 
350 | ### Smoke Test 1: Health Check
351 | 
352 | ```bash
353 | echo '{
354 |   "jsonrpc": "2.0",
355 |   "id": 1,
356 |   "method": "tools/call",
357 |   "params": {
358 |     "name": "health_check",
359 |     "arguments": {"include_corpus": true}
360 |   }
361 | }' | docker compose --env-file mcps/.env -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp
362 | ```
363 | 
364 | ### Smoke Test 2: Search Regulations
365 | 
366 | ```bash
367 | echo '{
368 |   "jsonrpc": "2.0",
369 |   "id": 2,
370 |   "method": "tools/call",
371 |   "params": {
372 |     "name": "search_regulations",
373 |     "arguments": {
374 |       "query": "capital adequacy",
375 |       "domains": ["capital_adequacy"]
376 |     }
377 |   }
378 | }' | docker compose --env-file mcps/.env -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp
379 | ```
380 | 
381 | ### Smoke Test 3: SonarQube Scan
382 | 
383 | ```bash
384 | # Backend
385 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
386 | 
387 | # Frontend
388 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
389 | ```
390 | 
391 | ---
392 | 
393 | ## Troubleshooting Guide
394 | 
395 | ### Issue 1: SonarQube Not Starting
396 | 
397 | **Diagnosis:**
398 | ```bash
399 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml logs sonarqube
400 | ```
401 | 
402 | **Solutions:**
403 | 1. Verify database password in `.env`
404 | 2. Increase Docker memory to 2GB+
405 | 3. Check port 9000 availability
406 | 
407 | ### Issue 2: ZAP Connection Failures
408 | 
409 | **Solutions:**
410 | 1. Wait for health check (2 minutes)
411 | 2. Verify `ZAP_MCP_SECURITY_KEY` in `.env`
412 | 3. Check MCP add-on installation
413 | 
414 | ### Issue 3: Token Configuration Errors
415 | 
416 | **Solutions:**
417 | 1. Ensure `.env` exists
418 | 2. Replace all `<placeholder>` values
419 | 3. Re-run `sonarqube-init`
420 | 
421 | ### Issue 4: Bob Cannot Find Tools
422 | 
423 | **Solutions:**
424 | 1. Create `.bob/mcp.json` from example
425 | 2. Restart Bob/VS Code
426 | 3. Test MCP connection manually
427 | 
428 | ---
429 | 
430 | ## Integration with CI/CD
431 | 
432 | ### GitHub Actions Example
433 | 
434 | ```yaml
435 | name: Regulatory Compliance
436 | 
437 | on: [pull_request]
438 | 
439 | jobs:
440 |   compliance:
441 |     runs-on: ubuntu-latest
442 |     steps:
443 |       - uses: actions/checkout@v4
444 |       
445 |       - name: Setup environment
446 |         run: |
447 |           cp mcps/.env.example mcps/.env
448 |           echo "SONARQUBE_ADMIN_PASSWORD=${{ secrets.SONARQUBE_ADMIN_PASSWORD }}" >> mcps/.env
449 |       
450 |       - name: Run compliance check
451 |         run: |
452 |           docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d sonarqube
453 |           docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
454 | ```
455 | 
456 | ---
457 | 
458 | ## Maintenance and Updates
459 | 
460 | ### Update Regulatory Corpus
461 | 
462 | ```bash
463 | # Edit regulation/control files
464 | cd mcps/regulatory_mcp/data
465 | 
466 | # Validate changes
467 | cd mcps/regulatory_mcp
468 | npm test
469 | 
470 | # Rebuild image
471 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml build bank-regulatory-controls-mcp
472 | ```
473 | 
474 | ### Rotate Secrets
475 | 
476 | ```bash
477 | # Generate new keys
478 | openssl rand -hex 32
479 | 
480 | # Update .env
481 | nano mcps/.env
482 | 
483 | # Restart services
484 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml restart
485 | ```
486 | 
487 | ### Backup SonarQube
488 | 
489 | ```bash
490 | # Backup database
491 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml exec sonarqube-db \
492 |   pg_dump -U risktrace_sonar risktrace_sonarqube > backup.sql
493 | ```
494 | 
495 | ---
496 | 
497 | ## Decision Trees
498 | 
499 | ### When to Use Which Tool?
500 | 
501 | ```mermaid
502 | graph TD
503 |     A[Start] --> B{What stage?}
504 |     B -->|Planning| C[Feature Description]
505 |     B -->|Design| D[Architecture Review]
506 |     B -->|Development| E[Code Review]
507 |     B -->|Release| F[Release Readiness]
508 |     
509 |     C --> C1[review_feature_description]
510 |     C --> C2[generate_acceptance_criteria]
511 |     C --> C3[match_controls]
512 |     
513 |     D --> D1[review_architecture_text]
514 |     D --> D2[generate_data_lineage_requirements]
515 |     D --> D3[generate_audit_log_requirements]
516 |     
517 |     E --> E1[review_code_diff]
518 |     E --> E2[SonarQube scan]
519 |     E --> E3[OWASP ZAP scan]
520 |     
521 |     F --> F1[assess_release_readiness]
522 |     F --> F2[generate_regulatory_mapping_report]
523 |     F --> F3[generate_rwa_run_evidence_requirements]
524 | ```
525 | 
526 | ### Which MCP Service to Use?
527 | 
528 | - **Regulatory compliance** → `bank-regulatory-controls-mcp`
529 | - **Code quality** → `sonarqube-mcp`
530 | - **Security scanning** → `owasp-zap-mcp`
531 | - **Dependency vulnerabilities** → `sonatype-guide-mcp`
532 | 
533 | ---
534 | 
535 | ## Additional Resources
536 | 
537 | ### Documentation
538 | 
539 | - [MCP README](README.md) - Service configuration and usage
540 | - [Regulatory MCP README](regulatory_mcp/README.md) - Tool details and corpus structure
541 | - [AGENTS.md](../AGENTS.md) - Repository-level agent rules
542 | 
543 | ### External References
544 | 
545 | - [Model Context Protocol Specification](https://modelcontextprotocol.io/)
546 | - [SonarQube Documentation](https://docs.sonarqube.org/)
547 | - [OWASP ZAP Documentation](https://www.zaproxy.org/docs/)
548 | 
549 | ### Support
550 | 
551 | For issues or questions:
552 | 1. Check this execution plan
553 | 2. Review troubleshooting guide
554 | 3. Consult team documentation
555 | 4. Contact compliance team for regulatory questions
556 | 
557 | ---
558 | 
559 | **Document Version:** 1.0  
560 | **Last Updated:** 2026-05-17  
561 | **Next Review:** 2026-08-17
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:41:51.960Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.07

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll now read the mcps/README.md file and examine more of the session history to complete my comprehensive analysis.

<read_file>
<args>
  <file>
    <path>mcps/README.md</path>
  </file>
  <file>
    <path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path>
    <line_range>100-500</line_range>
    <line_range>3000-3500</line_range>
  </file>
</args>
</read_file>

---

**User:**

[read_file for 'mcps/README.md', 'bob_sessions/bob_task_may-17-2026_2-31-18-pm.md'] Result:
<files>
<file><path>mcps/README.md</path>
<content lines="1-236">
  1 | # Local MCP Tooling
  2 | 
  3 | ## ⚠️ Important Safety Disclaimer
  4 | 
  5 | **This MCP infrastructure provides engineering controls and technical guidance only.**
  6 | 
  7 | - ❌ Does NOT provide legal advice or regulatory interpretation
  8 | - ❌ Does NOT replace qualified legal and compliance review  
  9 | - ✅ Provides technical controls for engineering teams
 10 | - ✅ References regulatory requirements for context
 11 | 
 12 | **Always consult qualified legal and compliance professionals for regulatory matters.**
 13 | 
 14 | The regulatory corpus is provided for reference and may not be complete, current, or applicable to your specific jurisdiction. Users are solely responsible for ensuring compliance with all applicable regulations.
 15 | 
 16 | *Control Reference: REL-EVID-001*
 17 | 
 18 | For detailed operational guidance, see [`EXECUTION_PLAN.md`](EXECUTION_PLAN.md).
 19 | 
 20 | ## Documentation Structure
 21 | 
 22 | This directory contains multiple MCP servers for quality assurance, security scanning, and regulatory compliance:
 23 | 
 24 | - **[`README.md`](README.md)** (this file) - Quick reference and setup commands
 25 | - **[`EXECUTION_PLAN.md`](EXECUTION_PLAN.md)** - Comprehensive operational guide with step-by-step setup (START HERE for new developers)
 26 | - **[`regulatory_mcp/README.md`](regulatory_mcp/README.md)** - Detailed regulatory MCP tool documentation
 27 | 
 28 | **New developers:** Read [`EXECUTION_PLAN.md`](EXECUTION_PLAN.md) first for complete setup workflow.
 29 | 
 30 | ## Quick Start (5 Minutes)
 31 | 
 32 | ```bash
 33 | # 1. Prerequisites check
 34 | docker --version  # Requires Docker 20.10+
 35 | node --version    # Requires Node.js 18+
 36 | 
 37 | # 2. Configure secrets
 38 | cd mcps
 39 | cp .env.example .env
 40 | # Edit .env with your passwords/tokens
 41 | 
 42 | # 3. Build regulatory MCP
 43 | docker compose build bank-regulatory-controls-mcp
 44 | 
 45 | # 4. Start SonarQube (one-time setup)
 46 | docker compose --profile setup up
 47 | 
 48 | # 5. Test regulatory MCP
 49 | docker compose run --rm -T bank-regulatory-controls-mcp node build/index.js <<< '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"health_check","arguments":{}}}'
 50 | ```
 51 | 
 52 | For detailed setup, see [`EXECUTION_PLAN.md`](EXECUTION_PLAN.md).
 53 | 
 54 | ## Overview
 55 | 
 56 | This directory owns repository-local MCP tooling for RiskTrace Control Tower. It stays separate
 57 | from `apps/docker-compose.yml` so quality and security assistant tooling does not change backend
 58 | or frontend application runtime behavior.
 59 | 
 60 | ## What Is Included
 61 | 
 62 | - `mcps/docker-compose.yml` starts local SonarQube, its Postgres database, and OWASP ZAP.
 63 | - `sonarqube-init` is a one-shot Compose service with the `setup` profile. It creates the backend
 64 |   and frontend SonarQube projects, refreshes a local token, and stores it in the
 65 |   `risktrace_mcp_secrets` Docker volume.
 66 | - `sonarqube-mcp`, `owasp-zap-mcp`, and `sonatype-guide-mcp` are stdio MCP services intended to
 67 |   be started by IBM Bob through local `.bob/mcp.json`. They are hidden behind the `mcp` profile so a
 68 |   plain Compose `up` does not start them.
 69 | - `sonar-scan-backend` and `sonar-scan-frontend` publish analysis to the local SonarQube. They
 70 |   are hidden behind the `scan` profile.
 71 | 
 72 | 
 73 | ### Bank Regulatory Controls MCP
 74 | 
 75 | The core of this infrastructure is the **bank-regulatory-controls-mcp**, a Model Context Protocol server that provides 15 specialized tools for regulatory compliance checking:
 76 | 
 77 | **Regulatory Tools:**
 78 | 1. `health_check` - Server health and corpus statistics
 79 | 2. `get_regulatory_profile` - Regulations and controls by domain/jurisdiction
 80 | 3. `search_regulations` - Full-text regulation search with filters
 81 | 4. `match_controls` - Control matching for artifacts
 82 | 5. `review_feature_description` - Feature compliance review
 83 | 6. `review_architecture_text` - Architecture compliance review
 84 | 7. `review_code_diff` - Code change compliance review
 85 | 8. `generate_acceptance_criteria` - AC generation from controls
 86 | 9. `generate_data_lineage_requirements` - Lineage field generation
 87 | 10. `generate_audit_log_requirements` - Audit event generation
 88 | 11. `generate_test_obligations` - Test case generation
 89 | 12. `assess_release_readiness` - Release gate assessment
 90 | 13. `generate_regulatory_mapping_report` - Markdown report generation
 91 | 14. `generate_rwa_run_evidence_requirements` - RWA execution evidence
 92 | 15. `explain_control` - Control explanation and guidance
 93 | 
 94 | **Regulatory Coverage:**
 95 | - 9 regulations (CRR3, EBA_REPORTING_4, BCBS239, DORA, EBA_ICT_SECURITY, GDPR, plus 3 internal policies)
 96 | - 15+ controls (RWA-CALC-001, RWA-DATA-001, SEC-INPUT-001, etc.)
 97 | - Complete regulatory corpus with mappings and examples
 98 | 
 99 | For detailed tool documentation, see [`regulatory_mcp/README.md`](regulatory_mcp/README.md).
100 | 
101 | ## Secret Handling
102 | 
103 | Do not put real tokens or passwords in committed files. Copy the template and edit local values:
104 | 
105 | ```bash
106 | cp mcps/.env.example mcps/.env
107 | ```
108 | 
109 | `mcps/.env` is ignored by git. The generated SonarQube token is stored in the
110 | `risktrace_mcp_secrets` Docker volume, not in the repository.
111 | 
112 | 
113 | ## Build Regulatory MCP
114 | 
115 | Build the bank-regulatory-controls-mcp Docker image:
116 | 
117 | ```bash
118 | # From repository root
119 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml build bank-regulatory-controls-mcp
120 | ```
121 | 
122 | Verify the build:
123 | 
124 | ```bash
125 | # Test with health check
126 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml run --rm -T bank-regulatory-controls-mcp node build/index.js <<< '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"health_check","arguments":{}}}'
127 | ```
128 | 
129 | 
130 | ## Development Commands
131 | 
132 | ### Regulatory MCP (Node.js/TypeScript)
133 | 
134 | ```bash
135 | cd mcps/regulatory_mcp
136 | 
137 | # Install dependencies
138 | npm install
139 | 
140 | # Build TypeScript
141 | npm run build
142 | 
143 | # Run tests
144 | npm test
145 | 
146 | # Development mode (watch)
147 | npm run dev
148 | 
149 | # Start server (STDIO mode)
150 | npm start
151 | # or
152 | node build/index.js
153 | ```
154 | 
155 | For detailed development instructions, see [`regulatory_mcp/README.md`](regulatory_mcp/README.md).
156 | 
157 | 
158 | ## Start SonarQube
159 | 
160 | From the repository root:
161 | 
162 | ```bash
163 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d sonarqube
164 | ```
165 | 
166 | Then initialize the local projects and token:
167 | 
168 | ```bash
169 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile setup run --rm -T sonarqube-init
170 | ```
171 | 
172 | The initializer:
173 | 
174 | 1. Waits for `http://sonarqube:9000` inside the Compose network.
175 | 2. Creates these projects when missing:
176 |    - `risktrace-control-tower-backend`
177 |    - `risktrace-control-tower-frontend`
178 | 3. Revokes and regenerates the token named by `SONARQUBE_TOKEN_NAME`.
179 | 4. Writes the MCP/scanner environment to the shared Docker volume.
180 | 
181 | If you changed the local SonarQube admin password in the UI, update `mcps/.env` with the matching
182 | `SONARQUBE_ADMIN_USER` and `SONARQUBE_ADMIN_PASSWORD` before running `sonarqube-init`.
183 | 
184 | ## Analyze Backend And Frontend
185 | 
186 | The local project settings are committed under `mcps/sonarqube/` and contain no secrets.
187 | 
188 | Run scans from the repository root:
189 | 
190 | ```bash
191 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-backend
192 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml --profile scan run --rm -T sonar-scan-frontend
193 | ```
194 | 
195 | These services read the SonarQube token from the shared Docker volume. Run `sonarqube-init` again
196 | if the token is missing or should be rotated.
197 | 
198 | ## Start OWASP ZAP
199 | 
200 | From the repository root:
201 | 
202 | ```bash
203 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml up -d zap
204 | ```
205 | 
206 | This starts the ZAP daemon at `http://127.0.0.1:8090`, installs the official ZAP MCP Integration
207 | add-on inside that same container, and exposes the add-on at `http://127.0.0.1:8282` by default.
208 | It does not start a spider, AJAX spider, passive wait, or active scan. Any active scan must be
209 | requested explicitly by a developer against an authorized local target.
210 | 
211 | The default target hint is:
212 | 
213 | ```bash
214 | ZAP_MCP_TARGET_URL=http://127.0.0.1:5173
215 | ```
216 | 
217 | Change it in `mcps/.env` if the MCP workflow should target a different local URL.
218 | 
219 | ## IBM Bob MCP
220 | 
221 | `.bob/mcp.example.json` is committed as the shared template. Copy it to local `.bob/mcp.json`,
222 | which is ignored by git and is the source of truth for IBM Bob on each workstation. Local
223 | RiskTrace MCP entries start Compose services directly with the `mcp` profile:
224 | 
225 | - `risktrace-sonarqube` -> `sonarqube-mcp`
226 | - `owaspZap` -> `owasp-zap-mcp`
227 | - `sonatype-guide` -> `sonatype-guide-mcp`
228 | 
229 | Atlassian MCP stays as a direct remote MCP entry because it is not part of the local RiskTrace
230 | tooling runtime.
231 | 
232 | ## Stop Local Tooling
233 | 
234 | ```bash
235 | docker compose --env-file mcps/.env -f mcps/docker-compose.yml down
236 | ```
</content>
</file>
<file><path>bob_sessions/bob_task_may-17-2026_2-31-18-pm.md</path>
<content lines="100-500">
100 | apps/backend/src/rwa_dashboard/seed.py
101 | apps/backend/src/rwa_dashboard/service.py
102 | apps/backend/src/rwa_forecast_service/__init__.py
103 | apps/backend/src/rwa_forecast_service/cli.py
104 | apps/backend/src/rwa_forecast_service/engine.py
105 | apps/backend/src/rwa_forecast_service/fastapi_app.py
106 | apps/backend/src/rwa_forecast_service/py.typed
107 | apps/backend/src/rwa_forecast_service/schemas.py
108 | apps/backend/src/rwa_steering/__init__.py
109 | apps/backend/src/rwa_steering/cli.py
110 | apps/backend/src/rwa_steering/engine.py
111 | apps/backend/src/rwa_steering/errors.py
112 | apps/backend/src/rwa_steering/fastapi_app.py
113 | apps/backend/src/rwa_steering/input_package.py
114 | apps/backend/src/rwa_steering/missing_inputs.py
115 | apps/backend/src/rwa_steering/py.typed
116 | apps/backend/src/rwa_steering/scenarios.py
117 | apps/backend/src/rwa_steering/schemas.py
118 | apps/backend/src/rwa_steering/transformations.py
119 | apps/backend/src/rwa_steering/generated_inputs/cva_hedges.csv
120 | apps/frontend/.dockerignore
121 | apps/frontend/.env.example
122 | apps/frontend/.gitignore
123 | apps/frontend/Dockerfile
124 | apps/frontend/index.html
125 | apps/frontend/nginx.conf
126 | apps/frontend/package-lock.json
127 | apps/frontend/package.json
128 | apps/frontend/playwright.config.ts
129 | apps/frontend/README.md
130 | apps/frontend/tsconfig.json
131 | apps/frontend/tsconfig.node.json
132 | apps/frontend/vite.config.ts
133 | apps/frontend/public/risktrace-logo-sm.png
134 | apps/frontend/public/risktrace-logo.png
135 | apps/frontend/scripts/playwright-web-server.mjs
136 | apps/frontend/src/App.tsx
137 | apps/frontend/src/main.tsx
138 | apps/frontend/src/navigation.ts
139 | apps/frontend/src/vite-env.d.ts
140 | apps/frontend/src/api/client.ts
141 | apps/frontend/src/api/rwaApi.ts
142 | apps/frontend/src/api/rwaDashboardApi.ts
143 | apps/frontend/src/api/types.ts
144 | apps/frontend/src/components/rwa-briefing/AiExecutiveCommentaryCard.tsx
145 | apps/frontend/src/components/rwa-briefing/BriefingInsightCards.tsx
146 | apps/frontend/src/components/rwa-briefing/BriefingKpiStrip.tsx
147 | apps/frontend/src/components/rwa-briefing/EvidenceTraceabilityCard.tsx
148 | apps/frontend/src/components/rwa-briefing/ManagementReviewPackCard.tsx
149 | apps/frontend/src/components/rwa-briefing/RwaMovementAttributionCard.tsx
150 | apps/frontend/src/components/rwa-dashboard/AlertsPanel.tsx
151 | apps/frontend/src/components/rwa-dashboard/AppShell.tsx
152 | apps/frontend/src/components/rwa-dashboard/CapitalSummaryCard.tsx
153 | apps/frontend/src/components/rwa-dashboard/Card.tsx
154 | apps/frontend/src/components/rwa-dashboard/CountryMapCard.tsx
155 | apps/frontend/src/components/rwa-dashboard/ExposureDonutCard.tsx
156 | apps/frontend/src/components/rwa-dashboard/FilterBar.tsx
157 | apps/frontend/src/components/rwa-dashboard/MetricCard.tsx
158 | apps/frontend/src/components/rwa-dashboard/PageHeader.tsx
159 | apps/frontend/src/components/rwa-dashboard/RatingBarsCard.tsx
160 | apps/frontend/src/components/rwa-dashboard/RwaTrendCard.tsx
161 | apps/frontend/src/components/rwa-dashboard/Sidebar.tsx
162 | apps/frontend/src/components/rwa-dashboard/StatusBadge.tsx
163 | apps/frontend/src/components/rwa-dashboard/Toast.tsx
164 | apps/frontend/src/components/rwa-dashboard/TopBar.tsx
165 | apps/frontend/src/components/rwa-dashboard/TopExposuresCard.tsx
166 | apps/frontend/src/components/rwa-lineage/LineageFlowCard.tsx
167 | apps/frontend/src/components/rwa-lineage/LineageSideRail.tsx
168 | apps/frontend/src/components/rwa-lineage/LineageSummaryCard.tsx
169 | apps/frontend/src/components/rwa-lineage/TransformationStepsCard.tsx
170 | apps/frontend/src/hooks/iconHydration.ts
171 | apps/frontend/src/hooks/useApiResource.ts
172 | apps/frontend/src/hooks/useAppContextData.ts
173 | apps/frontend/src/hooks/useNotificationsData.ts
174 | apps/frontend/src/hooks/useRwaBriefingData.ts
175 | apps/frontend/src/hooks/useRwaDashboardData.ts
176 | apps/frontend/src/hooks/useRwaLineageData.ts
177 | apps/frontend/src/hooks/useToast.ts
178 | apps/frontend/src/hooks/useUiActions.ts
179 | apps/frontend/src/pages/DataLineagePage.tsx
180 | apps/frontend/src/pages/HomePage.tsx
181 | apps/frontend/src/pages/RwaDashboardPage.tsx
182 | apps/frontend/src/pages/RwaIntelligenceBriefingPage.tsx
183 | apps/frontend/src/styles/rwa-dashboard.css
184 | apps/frontend/tests/e2e/navigation.spec.ts
185 | bob_sessions/
186 | bob_sessions/bob_task_may-16-2026_3-42-58-pm.md
187 | bob_sessions/bob_task_may-16-2026_3-42-58-pm.png
188 | bob_sessions/bob_task_may-16-2026_5-49-33-pm.md
189 | bob_sessions/bob_task_may-16-2026_5-49-33-pm.md.png
190 | bob_sessions/bob_task_may-16-2026_6-24-03-pm.md
191 | bob_sessions/bob_task_may-16-2026_6-24-03-pm.png
192 | bob_sessions/bob_task_may-16-2026_6-44-37-pm.md
193 | bob_sessions/bob_task_may-16-2026_6-44-37-pm.png
194 | bob_sessions/bob_task_may-16-2026_7-26-23-pm.md
195 | bob_sessions/bob_task_may-16-2026_7-26-23-pm.png
196 | bob_sessions/bob_task_may-16-2026_9-41-56-pm.md
197 | bob_sessions/bob_task_may-16-2026_9-41-56-pm.png
198 | bob_sessions/bob_task_may-16-2026_10-44-03-pm.md
199 | bob_sessions/bob_task_may-16-2026_10-44-03-pm.png
200 | bob_sessions/bob_task_may-16-2026_11-27-12-pm.md
201 | bob_sessions/bob_task_may-16-2026_11-27-12-pm.png
202 | bob_sessions/bob_task_may-16-2026_11-54-41-pm.md
203 | bob_sessions/bob_task_may-16-2026_11-54-41-pm.png
204 | bob_sessions/bob_task_may-17-2026_1-03-09-am.md
205 | bob_sessions/bob_task_may-17-2026_1-03-09-am.png
206 | bob_sessions/bob_task_may-17-2026_1-25-46-am.md
207 | bob_sessions/bob_task_may-17-2026_1-25-46-am.png
208 | bob_sessions/bob_task_may-17-2026_2-19-23-am.md
209 | bob_sessions/bob_task_may-17-2026_2-19-23-am.png
210 | bob_sessions/bob_task_may-17-2026_2-22-21-am.md
211 | bob_sessions/bob_task_may-17-2026_2-22-21-am.png
212 | bob_sessions/bob_task_may-17-2026_3-06-50-am.md
213 | bob_sessions/bob_task_may-17-2026_3-06-50-am.png
214 | bob_sessions/bob_task_may-17-2026_10-47-14-am.md
215 | bob_sessions/bob_task_may-17-2026_10-47-14-am.png
216 | bob_sessions/bob_task_may-17-2026_12-11-43-am.md
217 | bob_sessions/bob_task_may-17-2026_12-11-43-am.png
218 | bob_sessions/bob_task_may-17-2026_12-18-36-am.md
219 | bob_sessions/bob_task_may-17-2026_12-18-36-am.png
220 | bob_sessions/bob_task_may-17-2026_12-45-41-am.md
221 | bob_sessions/bob_task_may-17-2026_12-45-41-am.png
222 | bob_sessions/bob_task_may-17-2026_12-50-45-am.md
223 | bob_sessions/bob_task_may-17-2026_12-50-45-am.png
224 | docker/
225 | docker/docker-compose.prod.yml
226 | docker/docker-compose.yml
227 | docker/nginx-host/rwa.conf
228 | docs/
229 | docs/RCT-15_TECHNICAL_ANALYSIS.md
230 | docs/RCT-16_TECHNICAL_ANALYSIS.md
231 | docs/RCT-17_IMPLEMENTATION_SUMMARY.md
232 | docs/RCT-17_TECHNICAL_ANALYSIS.md
233 | docs/RCT-18_IMPLEMENTATION_SUMMARY.md
234 | docs/RCT-18_TECHNICAL_ANALYSIS.md
235 | docs/RCT-18_VALIDATION_REPORT.md
236 | docs/agents/architecture.md
237 | docs/agents/contracts.md
238 | docs/agents/validation.md
239 | infra/
240 | k6/
241 | k6/load-test.js
242 | k6/smoke-test.js
243 | k6/stress-test.js
244 | k8s/
245 | k8s/cert-manager/cluster-issuer-prod.yaml
246 | k8s/cert-manager/cluster-issuer-staging.yaml
247 | k8s/external-secrets/backend-externalsecret.yaml
248 | k8s/external-secrets/clustersecretstore.yaml
249 | k8s/external-secrets/install.sh
250 | k8s/ingress/cert-manager-install.sh
251 | k8s/ingress/rwa-ingress.yaml
252 | k8s/opa/constraints/deny-latest-tag-constraint.yaml
253 | k8s/opa/constraints/deny-privileged-constraint.yaml
254 | k8s/opa/constraints/require-non-root-constraint.yaml
255 | k8s/opa/constraints/require-resource-limits-constraint.yaml
256 | k8s/opa/templates/deny-latest-tag.yaml
257 | k8s/opa/templates/deny-privileged.yaml
258 | k8s/opa/templates/require-non-root.yaml
259 | k8s/opa/templates/require-resource-limits.yaml
260 | mcps/
261 | mcps/.env.example
262 | mcps/.gitignore
263 | mcps/docker-compose.yml
264 | mcps/README.md
265 | mcps/regulatory_mcp/.dockerignore
266 | mcps/sonarqube/backend-project.properties
267 | observability/
268 | scripts/
269 | 
270 | (File list truncated. Use list_files on specific subdirectories if you need to explore further.)
271 | You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
272 | </environment_details>
273 | 
274 | ---
275 | 
276 | **Assistant:**
277 | 
278 | I'll analyze the performance dataset and create a comprehensive plan to optimize the RiskTrace Control Tower application. Let me start by exploring the performance data.
279 | 
280 | <read_file>
281 | <args>
282 |   <file>
283 |     <path>.</path>
284 |   </file>
285 | </args>
286 | </read_file>
287 | 
288 | ---
289 | 
290 | **User:**
291 | 
292 | [read_file for '.'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
293 | <files>
294 | <file><path>.</path><error>File not found</error><notice>The file was not found. Consider using list_files to find available files before attempting to read them.</notice></file>
295 | </files>
296 | <environment_details>
297 | # VSCode Visible Files
298 | 
299 | 
300 | # VSCode Open Tabs
301 | 
302 | 
303 | # Current Time
304 | Current time in ISO 8601 UTC format: 2026-05-17T12:26:34.151Z
305 | User time zone: Europe/Warsaw, UTC+2:00
306 | 
307 | # Current Cost
308 | $0.04
309 | 
310 | # Review Exclusions
311 | The following file patterns are excluded from code reviews:
312 | - .vscode/**
313 | 
314 | # Current Mode
315 | <slug>plan</slug>
316 | <name>📝 Plan</name>
317 | You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
318 | </environment_details>
319 | 
320 | ---
321 | 
322 | **Assistant:**
323 | 
324 | <list_files>
325 | <path>.</path>
326 | <recursive>false</recursive>
327 | </list_files>
328 | 
329 | ---
330 | 
331 | **User:**
332 | 
333 | [list_files for '.'] Result:
334 | .gitignore
335 | .gitleaks.toml
336 | .semgrepignore
337 | .trivyignore
338 | 🛡️ AGENTS.md
339 | README.MD
340 | sonar-project.properties
341 | .bob/
342 | .github/
343 | apps/
344 | bob_sessions/
345 | docker/
346 | docs/
347 | infra/
348 | k6/
349 | k8s/
350 | mcps/
351 | observability/
352 | scripts/
353 | <environment_details>
354 | # VSCode Visible Files
355 | 
356 | 
357 | # VSCode Open Tabs
358 | 
359 | 
360 | # Current Time
361 | Current time in ISO 8601 UTC format: 2026-05-17T12:26:38.538Z
362 | User time zone: Europe/Warsaw, UTC+2:00
363 | 
364 | # Current Cost
365 | $0.08
366 | 
367 | # Review Exclusions
368 | The following file patterns are excluded from code reviews:
369 | - .vscode/**
370 | 
371 | # Current Mode
372 | <slug>plan</slug>
373 | <name>📝 Plan</name>
374 | You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
375 | </environment_details>
376 | 
377 | ---
378 | 
379 | **Assistant:**
380 | 
381 | <list_files>
382 | <path>.</path>
383 | <recursive>true</recursive>
384 | </list_files>
385 | 
386 | ---
387 | 
388 | **User:**
389 | 
390 | [list_files for '.'] Result:
391 | .gitignore
392 | .semgrepignore
393 | 🛡️ AGENTS.md
394 | .bob/
395 | .github/
396 | apps/
397 | apps/docker-compose.yml
398 | apps/backend/.dockerignore
399 | apps/backend/.env.example
400 | apps/backend/.gitignore
401 | apps/backend/.python-version
402 | apps/backend/Dockerfile
403 | apps/backend/pyproject.toml
404 | apps/backend/README.md
405 | apps/backend/uv.lock
406 | apps/backend/src/rwa_steering/__init__.py
407 | apps/backend/src/rwa_steering/cli.py
408 | apps/backend/src/rwa_steering/engine.py
409 | apps/backend/src/rwa_steering/errors.py
410 | apps/backend/src/rwa_steering/fastapi_app.py
411 | apps/backend/src/rwa_steering/input_package.py
412 | apps/backend/src/rwa_steering/missing_inputs.py
413 | apps/backend/src/rwa_steering/py.typed
414 | apps/backend/src/rwa_steering/scenarios.py
415 | apps/backend/src/rwa_steering/schemas.py
416 | apps/backend/src/rwa_steering/transformations.py
417 | apps/backend/src/rwa_steering/generated_inputs/capital_positions.csv
418 | apps/backend/src/rwa_steering/generated_inputs/cva_hedges.csv
419 | apps/backend/src/rwa_steering/generated_inputs/cva_netting_sets.csv
420 | apps/backend/src/rwa_steering/generated_inputs/cva_portfolio_inputs.csv
421 | apps/backend/src/rwa_steering/generated_inputs/data_quality_flags.csv
422 | apps/backend/src/rwa_steering/generated_inputs/dlgd_scenario_assumptions.csv
423 | apps/backend/src/rwa_steering/generated_inputs/forecast_calendar.csv
424 | apps/backend/src/rwa_steering/generated_inputs/fx_scenario_rates.csv
425 | apps/backend/src/rwa_steering/generated_inputs/leverage_exposures.csv
426 | apps/backend/src/rwa_steering/generated_inputs/leverage_off_balance_sheet_items.csv
427 | apps/backend/src/rwa_steering/generated_inputs/macro_regime_indicators.csv
428 | apps/backend/src/rwa_steering/generated_inputs/manifest.json
429 | apps/backend/src/rwa_steering/generated_inputs/operational_risk_business_indicators.csv
430 | apps/backend/src/rwa_steering/generated_inputs/operational_risk_losses.csv
431 | apps/backend/src/rwa_steering/generated_inputs/portfolio_strategy_limits.csv
432 | apps/backend/src/rwa_steering/generated_inputs/profitability_inputs.csv
433 | apps/backend/src/rwa_steering/generated_inputs/rating_migration_matrix.csv
434 | apps/backend/src/rwa_steering/generated_inputs/README.md
435 | apps/backend/src/rwa_steering/generated_inputs/regulatory_overlay_selection.csv
436 | apps/backend/src/rwa_steering/generated_inputs/scenario_definitions.csv
437 | apps/backend/src/rwa_steering/generated_inputs/segment_growth_assumptions.csv
438 | apps/backend/src/rwa_steering/generated_inputs/steering_action_constraints.csv
439 | apps/backend/src/rwa_steering/generated_inputs/validation_report.json
440 | apps/backend/tests/calculator/test_capital_modules.py
441 | apps/backend/tests/calculator/test_fastapi_microservice.py
442 | apps/backend/tests/calculator/test_golden_regression.py
443 | apps/backend/tests/calculator/test_rwa_backend.py
444 | apps/backend/tests/projection/test_calendar.py
445 | apps/backend/tests/projection/test_projection_service.py
446 | apps/frontend/.dockerignore
447 | apps/frontend/.gitignore
448 | apps/frontend/index.html
449 | apps/frontend/nginx.conf
450 | apps/frontend/package-lock.json
451 | apps/frontend/package.json
452 | apps/frontend/playwright.config.ts
453 | apps/frontend/README.md
454 | apps/frontend/tsconfig.node.json
455 | apps/frontend/vite.config.ts
456 | apps/frontend/public/risktrace-logo-sm.png
457 | apps/frontend/public/risktrace-logo.png
458 | apps/frontend/scripts/playwright-web-server.mjs
459 | apps/frontend/src/App.tsx
460 | apps/frontend/src/navigation.ts
461 | apps/frontend/src/api/rwaApi.ts
462 | apps/frontend/src/api/rwaDashboardApi.ts
463 | apps/frontend/src/styles/rwa-dashboard.css
464 | bob_sessions/
465 | bob_sessions/bob_task_may-16-2026_3-42-58-pm.md
466 | bob_sessions/bob_task_may-16-2026_3-42-58-pm.png
467 | bob_sessions/bob_task_may-16-2026_5-49-33-pm.md
468 | bob_sessions/bob_task_may-16-2026_5-49-33-pm.md.png
469 | bob_sessions/bob_task_may-16-2026_6-24-03-pm.md
470 | bob_sessions/bob_task_may-16-2026_6-24-03-pm.png
471 | bob_sessions/bob_task_may-16-2026_6-44-37-pm.md
472 | bob_sessions/bob_task_may-16-2026_6-44-37-pm.png
473 | bob_sessions/bob_task_may-16-2026_7-26-23-pm.md
474 | bob_sessions/bob_task_may-16-2026_7-26-23-pm.png
475 | bob_sessions/bob_task_may-16-2026_9-41-56-pm.md
476 | bob_sessions/bob_task_may-16-2026_9-41-56-pm.png
477 | bob_sessions/bob_task_may-16-2026_10-44-03-pm.md
478 | bob_sessions/bob_task_may-16-2026_10-44-03-pm.png
479 | bob_sessions/bob_task_may-16-2026_11-27-12-pm.md
480 | bob_sessions/bob_task_may-16-2026_11-27-12-pm.png
481 | bob_sessions/bob_task_may-16-2026_11-54-41-pm.md
482 | bob_sessions/bob_task_may-16-2026_11-54-41-pm.png
483 | bob_sessions/bob_task_may-17-2026_1-03-09-am.md
484 | bob_sessions/bob_task_may-17-2026_1-03-09-am.png
485 | bob_sessions/bob_task_may-17-2026_1-25-46-am.md
486 | bob_sessions/bob_task_may-17-2026_1-25-46-am.png
487 | bob_sessions/bob_task_may-17-2026_2-19-23-am.md
488 | bob_sessions/bob_task_may-17-2026_2-19-23-am.png
489 | bob_sessions/bob_task_may-17-2026_2-22-21-am.md
490 | bob_sessions/bob_task_may-17-2026_2-22-21-am.png
491 | bob_sessions/bob_task_may-17-2026_3-06-50-am.md
492 | bob_sessions/bob_task_may-17-2026_3-06-50-am.png
493 | bob_sessions/bob_task_may-17-2026_10-47-14-am.md
494 | bob_sessions/bob_task_may-17-2026_10-47-14-am.png
495 | bob_sessions/bob_task_may-17-2026_12-11-43-am.md
496 | bob_sessions/bob_task_may-17-2026_12-11-43-am.png
497 | bob_sessions/bob_task_may-17-2026_12-18-36-am.md
498 | bob_sessions/bob_task_may-17-2026_12-18-36-am.png
499 | bob_sessions/bob_task_may-17-2026_12-45-41-am.md
500 | bob_sessions/bob_task_may-17-2026_12-45-41-am.png
</content>
<content lines="3000-3500">
3000 |  62 | 
3001 |  63 |         self.calculator = RwaCalculator.from_files(nccr_mapping_path, country_info_path)
3002 |  64 |         if input_package is not None:
3003 |  65 |             self.input_package = input_package
3004 |  66 |         elif generated_inputs_root is not None:
3005 |  67 |             self.input_package = load_steering_input_package(generated_inputs_root)
3006 |  68 |         else:
3007 |  69 |             self.input_package = load_steering_input_package()
3008 |  70 | 
3009 |  71 |     def run(self, request: SteeringRequest) -> SteeringResponse:
3010 |  72 |         """Execute a full steering run for all requested scenarios and dates.
3011 |  73 | 
3012 |  74 |         Args:
3013 |  75 |             request: Validated steering request containing current calculator input rows,
3014 |  76 |                 projection dates and scenario ids.
3015 |  77 | 
3016 |  78 |         Returns:
3017 |  79 |             A dashboard-ready response with scenario summaries, exposure projections,
3018 |  80 |             sequential attribution and ranked recommendations.
3019 |  81 |         """
3020 |  82 | 
3021 |  83 |         self.input_package.ensure_jurisdiction(request.jurisdiction)
3022 |  84 | 
3023 |  85 |         current_payload = self.calculator.calculate_batch(request.core_info)
3024 |  86 |         if current_payload["errors"]:
3025 |  87 |             raise SteeringDomainError.from_calculator_errors(current_payload["errors"])
3026 |  88 |         current_by_id = results_by_id(current_payload["results"])
3027 |  89 |         current_total = portfolio_rwa(current_payload["results"])
3028 |  90 | 
3029 |  91 |         summaries: list[ScenarioRunSummary] = []
3030 |  92 |         projections: list[ProjectionRow] = []
3031 |  93 |         attributions: list[AttributionRow] = []
3032 |  94 |         recommendations: list[RecommendationRow] = []
3033 |  95 | 
3034 |  96 |         for scenario_id in request.scenarios:
3035 |  97 |             for projection_date in request.projection_dates:
3036 |  98 |                 scenario = self.input_package.scenario_assumption(str(scenario_id), projection_date)
3037 |  99 |                 projected_rows = [
3038 | 100 |                     self.input_package.project_row(
3039 | 101 |                         row, str(scenario_id), request.as_of_date, projection_date
3040 | 102 |                     )
3041 | 103 |                     for row in request.core_info
3042 | 104 |                 ]
3043 | 105 |                 projected_payload = self.calculator.calculate_batch(projected_rows)
3044 | 106 |                 if projected_payload["errors"]:
3045 | 107 |                     raise SteeringDomainError.from_calculator_errors(
3046 | 108 |                         projected_payload["errors"],
3047 | 109 |                         scenario_id=str(scenario_id),
3048 | 110 |                         projection_date=projection_date.isoformat(),
3049 | 111 |                     )
3050 | 112 |                 projected_by_id = results_by_id(projected_payload["results"])
3051 | 113 |                 projected_total = portfolio_rwa(projected_payload["results"])
3052 | 114 | 
3053 | 115 |                 summaries.append(
3054 | 116 |                     self._summary(scenario, projection_date, current_total, projected_total)
3055 | 117 |                 )
3056 | 118 |                 projections.extend(
3057 | 119 |                     self._projection_rows(
3058 | 120 |                         request=request,
3059 | 121 |                         scenario=scenario,
3060 | 122 |                         projection_date=projection_date,
3061 | 123 |                         current_rows=request.core_info,
3062 | 124 |                         projected_rows=projected_rows,
3063 | 125 |                         current_by_id=current_by_id,
3064 | 126 |                         projected_by_id=projected_by_id,
3065 | 127 |                     )
3066 | 128 |                 )
3067 | 129 |                 attributions.append(
3068 | 130 |                     self._attribution(
3069 | 131 |                         request=request,
3070 | 132 |                         scenario=scenario,
3071 | 133 |                         projection_date=projection_date,
3072 | 134 |                         current_total=current_total,
3073 | 135 |                         projected_total=projected_total,
3074 | 136 |                     )
3075 | 137 |                 )
3076 | 138 |                 recommendations.extend(
3077 | 139 |                     self._recommendations(
3078 | 140 |                         scenario=scenario,
3079 | 141 |                         projection_date=projection_date,
3080 | 142 |                         projected_rows=projected_rows,
3081 | 143 |                         projected_by_id=projected_by_id,
3082 | 144 |                         current_rows=request.core_info,
3083 | 145 |                         top_n=request.top_n_recommendations,
3084 | 146 |                     )
3085 | 147 |                 )
3086 | 148 | 
3087 | 149 |         recommendations = sorted(
3088 | 150 |             recommendations,
3089 | 151 |             key=lambda item: item.recommendation_score,
3090 | 152 |             reverse=True,
3091 | 153 |         )[: request.top_n_recommendations]
3092 | 154 | 
3093 | 155 |         return SteeringResponse(
3094 | 156 |             methodology=METHODOLOGY,
3095 | 157 |             jurisdiction=request.jurisdiction,
3096 | 158 |             summaries=summaries,
3097 | 159 |             projections=projections,
3098 | 160 |             attributions=attributions,
3099 | 161 |             recommendations=recommendations,
3100 | 162 |             limitations=[
3101 | 163 |                 "Uses validated prepared generated inputs, not production customer data.",
3102 | 164 |                 (
3103 | 165 |                     "Scenario assumptions are deterministic input-package values, "
3104 | 166 |                     "not calibrated ML forecasts."
3105 | 167 |                 ),
3106 | 168 |                 "Recommendations are decision-support proposals and require risk/finance review.",
3107 | 169 |             ],
3108 | 170 |             input_package_version=self.input_package.manifest.version_id,
3109 | 171 |             input_package_validation_status=self.input_package.manifest.validation_status,
3110 | 172 |         )
3111 | 173 | 
3112 | 174 |     def _summary(
3113 | 175 |         self,
3114 | 176 |         scenario: ScenarioAssumption,
3115 | 177 |         projection_date: date,
3116 | 178 |         current_total: Decimal,
3117 | 179 |         projected_total: Decimal,
3118 | 180 |     ) -> ScenarioRunSummary:
3119 | 181 |         """Build portfolio-level RWA delta metrics for one scenario/date."""
3120 | 182 | 
3121 | 183 |         delta = projected_total - current_total
3122 | 184 |         return ScenarioRunSummary(
3123 | 185 |             scenario_id=scenario.scenario_id,
3124 | 186 |             scenario_name=scenario.scenario_name,
3125 | 187 |             regime_label=scenario.regime_label,
3126 | 188 |             regime_score=scenario.regime_score,
3127 | 189 |             risk_budget_multiplier=scenario.risk_budget_multiplier,
3128 | 190 |             projection_date=projection_date,
3129 | 191 |             current_rwa=current_total,
3130 | 192 |             projected_rwa=projected_total,
3131 | 193 |             rwa_delta=delta,
3132 | 194 |             rwa_delta_pct=safe_pct(delta, current_total),
3133 | 195 |         )
3134 | 196 | 
3135 | 197 |     def _projection_rows(
3136 | 198 |         self,
3137 | 199 |         request: SteeringRequest,
3138 | 200 |         scenario: ScenarioAssumption,
3139 | 201 |         projection_date: date,
3140 | 202 |         current_rows: list[dict[str, Any]],
3141 | 203 |         projected_rows: list[dict[str, Any]],
3142 | 204 |         current_by_id: dict[str, dict[str, Any]],
3143 | 205 |         projected_by_id: dict[str, dict[str, Any]],
3144 | 206 |     ) -> list[ProjectionRow]:
3145 | 207 |         """Build exposure-level current-versus-projected RWA rows.
3146 | 208 | 
3147 | 209 |         ``current_rows`` and ``projected_rows`` are zipped with ``strict=True`` because order is
3148 | 210 |         expected to be preserved by the projection loop. A mismatch means the steering layer is
3149 | 211 |         about to report deltas against the wrong asset and should fail loudly.
3150 | 212 |         """
3151 | 213 | 
3152 | 214 |         rows: list[ProjectionRow] = []
3153 | 215 |         for current_row, projected_row in zip(current_rows, projected_rows, strict=True):
3154 | 216 |             row_id = str(current_row["id"])
3155 | 217 |             current_rwa = parse_decimal(current_by_id[row_id][RWA_FIELD], default=Decimal("0"))
3156 | 218 |             projected_rwa = parse_decimal(projected_by_id[row_id][RWA_FIELD], default=Decimal("0"))
3157 | 219 |             delta = projected_rwa - current_rwa
3158 | 220 |             rows.append(
3159 | 221 |                 ProjectionRow(
3160 | 222 |                     scenario_id=scenario.scenario_id,
3161 | 223 |                     scenario_name=scenario.scenario_name,
3162 | 224 |                     jurisdiction=request.jurisdiction,
3163 | 225 |                     as_of_date=request.as_of_date,
3164 | 226 |                     projection_date=projection_date,
3165 | 227 |                     id=row_id,
3166 | 228 |                     counterparty_gid=str(current_row["counterparty_gid"]),
3167 | 229 |                     entity_class=str(current_row["entity_class"]),
3168 | 230 |                     sub_class=str(current_row["sub_class"]),
3169 | 231 |                     exposure_ccy=str(current_row["exposure_ccy"]),
3170 | 232 |                     current_exposure_amount=parse_decimal(current_row["exposure_amount"]),
3171 | 233 |                     projected_exposure_amount=parse_decimal(projected_row["exposure_amount"]),
3172 | 234 |                     current_rating=str(current_row["counterparty_fcy_internal_rating"]),
3173 | 235 |                     projected_rating=str(projected_row["counterparty_fcy_internal_rating"]),
3174 | 236 |                     current_dlgd=parse_decimal(current_row["counterparty_dlgd"]),
3175 | 237 |                     projected_dlgd=parse_decimal(projected_row["counterparty_dlgd"]),
3176 | 238 |                     current_rwa=current_rwa,
3177 | 239 |                     projected_rwa=projected_rwa,
3178 | 240 |                     rwa_delta=delta,
3179 | 241 |                     rwa_delta_pct=safe_pct(delta, current_rwa),
3180 | 242 |                 )
3181 | 243 |             )
3182 | 244 |         return rows
3183 | 245 | 
3184 | 246 |     def _attribution(
3185 | 247 |         self,
3186 | 248 |         request: SteeringRequest,
3187 | 249 |         scenario: ScenarioAssumption,
3188 | 250 |         projection_date: date,
3189 | 251 |         current_total: Decimal,
3190 | 252 |         projected_total: Decimal,
3191 | 253 |     ) -> AttributionRow:
3192 | 254 |         """Compute first-order portfolio attribution by sequential revaluation.
3193 | 255 | 
3194 | 256 |         Each driver is isolated by applying exactly one projection transformation and re-running
3195 | 257 |         the full portfolio through the calculator. This keeps attribution explainable and aligned
3196 | 258 |         with the calculator, while the residual discloses interaction effects between
3197 | 259 |         volume, maturity, ratings, DLGD and FX.
3198 | 260 |         """
3199 | 261 | 
3200 | 262 |         driver_totals = {
3201 | 263 |             "volume_delta": self._driver_delta(
3202 | 264 |                 request, scenario, projection_date, current_total, apply_volume=True
3203 | 265 |             ),
3204 | 266 |             "maturity_delta": self._driver_delta(
3205 | 267 |                 request, scenario, projection_date, current_total, apply_maturity=True
3206 | 268 |             ),
3207 | 269 |             "rating_delta": self._driver_delta(
3208 | 270 |                 request, scenario, projection_date, current_total, apply_rating=True
3209 | 271 |             ),
3210 | 272 |             "dlgd_delta": self._driver_delta(
3211 | 273 |                 request, scenario, projection_date, current_total, apply_dlgd=True
3212 | 274 |             ),
3213 | 275 |             "fx_delta": self._driver_delta(
3214 | 276 |                 request, scenario, projection_date, current_total, apply_fx=True
3215 | 277 |             ),
3216 | 278 |         }
3217 | 279 |         regulatory_delta = Decimal("0")
3218 | 280 |         explained = sum(driver_totals.values(), regulatory_delta)
3219 | 281 |         return AttributionRow(
3220 | 282 |             scenario_id=scenario.scenario_id,
3221 | 283 |             projection_date=projection_date,
3222 | 284 |             rwa_current=current_total,
3223 | 285 |             volume_delta=driver_totals["volume_delta"],
3224 | 286 |             maturity_delta=driver_totals["maturity_delta"],
3225 | 287 |             rating_delta=driver_totals["rating_delta"],
3226 | 288 |             dlgd_delta=driver_totals["dlgd_delta"],
3227 | 289 |             fx_delta=driver_totals["fx_delta"],
3228 | 290 |             regulatory_delta=regulatory_delta,
3229 | 291 |             interaction_or_residual_delta=projected_total - current_total - explained,
3230 | 292 |             rwa_projected=projected_total,
3231 | 293 |         )
3232 | 294 | 
3233 | 295 |     def _driver_delta(
3234 | 296 |         self,
3235 | 297 |         request: SteeringRequest,
3236 | 298 |         scenario: ScenarioAssumption,
3237 | 299 |         projection_date: date,
3238 | 300 |         current_total: Decimal,
3239 | 301 |         **driver_flag: bool,
3240 | 302 |     ) -> Decimal:
3241 | 303 |         """Calculate one first-order RWA driver delta.
3242 | 304 | 
3243 | 305 |         ``driver_flag`` contains exactly one enabled transformation in normal use. The method
3244 | 306 |         still accepts keyword flags to keep the call site explicit and to make future multi-driver
3245 | 307 |         sensitivity tests easy to add.
3246 | 308 |         """
3247 | 309 | 
3248 | 310 |         projected_rows = [
3249 | 311 |             self.input_package.project_row(
3250 | 312 |                 row,
3251 | 313 |                 scenario.scenario_id,
3252 | 314 |                 request.as_of_date,
3253 | 315 |                 projection_date,
3254 | 316 |                 apply_volume=driver_flag.get("apply_volume", False),
3255 | 317 |                 apply_maturity=driver_flag.get("apply_maturity", False),
3256 | 318 |                 apply_rating=driver_flag.get("apply_rating", False),
3257 | 319 |                 apply_dlgd=driver_flag.get("apply_dlgd", False),
3258 | 320 |                 apply_fx=driver_flag.get("apply_fx", False),
3259 | 321 |             )
3260 | 322 |             for row in request.core_info
3261 | 323 |         ]
3262 | 324 |         return (
3263 | 325 |             portfolio_rwa(self.calculator.calculate_batch(projected_rows)["results"])
3264 | 326 |             - current_total
3265 | 327 |         )
3266 | 328 | 
3267 | 329 |     def _recommendations(
3268 | 330 |         self,
3269 | 331 |         scenario: ScenarioAssumption,
3270 | 332 |         projection_date: date,
3271 | 333 |         projected_rows: list[dict[str, Any]],
3272 | 334 |         projected_by_id: dict[str, dict[str, Any]],
3273 | 335 |         current_rows: list[dict[str, Any]],
3274 | 336 |         top_n: int,
3275 | 337 |     ) -> list[RecommendationRow]:
3276 | 338 |         """Generate and score first-version steering recommendations.
3277 | 339 | 
3278 | 340 |         Candidate assets are the top projected RWA contributors. The selected action, maximum
3279 | 341 |         reduction, business cost and implementation complexity come from generated steering
3280 | 342 |         constraints and profitability inputs. This is decision support, not automated action.
3281 | 343 |         """
3282 | 344 | 
3283 | 345 |         candidates: list[RecommendationRow] = []
3284 | 346 |         current_by_id = {str(row["id"]): row for row in current_rows}
3285 | 347 |         ranked_rows = sorted(
3286 | 348 |             projected_rows,
3287 | 349 |             key=lambda row: parse_decimal(projected_by_id[str(row["id"])][RWA_FIELD]),
3288 | 350 |             reverse=True,
3289 | 351 |         )[: top_n * 2]
3290 | 352 | 
3291 | 353 |         for row in ranked_rows:
3292 | 354 |             before = parse_decimal(projected_by_id[str(row["id"])][RWA_FIELD])
3293 | 355 |             if before <= Decimal("0"):
3294 | 356 |                 continue
3295 | 357 |             current_row = current_by_id[str(row["id"])]
3296 | 358 |             constraint = self.input_package.best_reduction_constraint(current_row)
3297 | 359 |             if constraint is None or constraint.max_exposure_reduction_pct <= Decimal("0"):
3298 | 360 |                 continue
3299 | 361 |             reduction_pct = min(Decimal("0.50"), constraint.max_exposure_reduction_pct)
3300 | 362 |             action_row = dict(row)
3301 | 363 |             action_row["exposure_amount"] = parse_decimal(row["exposure_amount"]) * (
3302 | 364 |                 Decimal("1") - reduction_pct
3303 | 365 |             )
3304 | 366 |             action_payload = self.calculator.calculate_batch([action_row])
3305 | 367 |             if action_payload["errors"]:
3306 | 368 |                 raise SteeringDomainError.from_calculator_errors(
3307 | 369 |                     action_payload["errors"],
3308 | 370 |                     scenario_id=scenario.scenario_id,
3309 | 371 |                     projection_date=projection_date.isoformat(),
3310 | 372 |                 )
3311 | 373 |             after = portfolio_rwa(action_payload["results"])
3312 | 374 |             saving = max(Decimal("0"), before - after)
3313 | 375 |             profitability = self.input_package.profitability_for(str(row["id"]))
3314 | 376 |             relationship_penalty = (
3315 | 377 |                 Decimal(
3316 | 378 |                     profitability.relationship_value_score
3317 | 379 |                     + profitability.strategic_importance_score
3318 | 380 |                 )
3319 | 381 |                 / Decimal("200")
3320 | 382 |                 if profitability is not None
3321 | 383 |                 else Decimal("0.50")
3322 | 384 |             )
3323 | 385 |             cost = parse_decimal(row["exposure_amount"]) * constraint.business_cost_factor
3324 | 386 |             complexity = constraint.implementation_complexity
3325 | 387 |             score = (
3326 | 388 |                 saving * scenario.risk_budget_multiplier
3327 | 389 |                 - cost * Decimal("0.10")
3328 | 390 |                 - Decimal(complexity)
3329 | 391 |                 - relationship_penalty * Decimal("1000")
3330 | 392 |             )
3331 | 393 |             candidates.append(
3332 | 394 |                 RecommendationRow(
3333 | 395 |                     scenario_id=scenario.scenario_id,
3334 | 396 |                     projection_date=projection_date,
3335 | 397 |                     id=str(row["id"]),
3336 | 398 |                     counterparty_gid=str(row["counterparty_gid"]),
3337 | 399 |                     entity_class=str(row["entity_class"]),
3338 | 400 |                     sub_class=str(row["sub_class"]),
3339 | 401 |                     recommended_action=constraint.action_code,
3340 | 402 |                     action_description=(
3341 | 403 |                         f"Simulate {reduction_pct:.0%} exposure reduction under generated "
3342 | 404 |                         f"{constraint.action_code} constraint."
3343 | 405 |                     ),
3344 | 406 |                     rwa_before_action=before,
3345 | 407 |                     rwa_after_action=after,
3346 | 408 |                     estimated_rwa_saving=saving,
3347 | 409 |                     estimated_business_cost=cost,
3348 | 410 |                     implementation_complexity=complexity,
3349 | 411 |                     recommendation_score=score,
3350 | 412 |                     reason_code="CONSTRAINT_AWARE_TOP_PROJECTED_RWA_CONTRIBUTOR",
3351 | 413 |                 )
3352 | 414 |             )
3353 | 415 | 
3354 | 416 |         return candidates
3355 | 417 | 
3356 | 418 | 
3357 | 419 | def results_by_id(results: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
3358 | 420 |     """Index calculator output rows by exposure id."""
3359 | 421 | 
3360 | 422 |     return {str(row["id"]): row for row in results}
3361 | 423 | 
3362 | 424 | 
3363 | 425 | def portfolio_rwa(results: list[dict[str, Any]]) -> Decimal:
3364 | 426 |     """Aggregate Basel 3.1 final RWA from calculator output rows."""
3365 | 427 | 
3366 | 428 |     return sum(
3367 | 429 |         (parse_decimal(row[RWA_FIELD], default=Decimal("0")) for row in results),
3368 | 430 |         Decimal("0"),
3369 | 431 |     )
3370 | 432 | 
3371 | 433 | 
3372 | 434 | def safe_pct(delta: Decimal, base: Decimal) -> Decimal | None:
3373 | 435 |     """Return ``delta / base`` while preserving ``None`` for zero denominators."""
3374 | 436 | 
3375 | 437 |     if base == Decimal("0"):
3376 | 438 |         return None
3377 | 439 |     return delta / base
3378 | </content>
3379 | </file>
3380 | <file><path>apps/backend/src/rwa_forecast_service/engine.py</path>
3381 | <content lines="1-741">
3382 |   1 | from __future__ import annotations
3383 |   2 | 
3384 |   3 | import calendar
3385 |   4 | import random
3386 |   5 | from dataclasses import dataclass
3387 |   6 | from datetime import date
3388 |   7 | from decimal import Decimal
3389 |   8 | from pathlib import Path
3390 |   9 | from statistics import mean
3391 |  10 | from typing import Any
3392 |  11 | 
3393 |  12 | from rwa_calculator.paths import NCCR_MAPPING_PATH, PREPROD_COUNTRY_INFO_PATH
3394 |  13 | from rwa_calculator.rwa_calculator.calculator import RwaCalculator
3395 |  14 | from rwa_steering.engine import portfolio_rwa
3396 |  15 | from rwa_steering.errors import SteeringDomainError
3397 |  16 | from rwa_steering.input_package import SteeringInputPackage, load_steering_input_package
3398 |  17 | from rwa_steering.transformations import migrate_rating, parse_decimal
3399 |  18 | 
3400 |  19 | from .schemas import (
3401 |  20 |     ForecastRequest,
3402 |  21 |     ForecastResponse,
3403 |  22 |     ForecastSummary,
3404 |  23 |     MarketFactorStep,
3405 |  24 |     PathScore,
3406 |  25 |     PortfolioPathStep,
3407 |  26 | )
3408 |  27 | 
3409 |  28 | FORECAST_ENGINE_VERSION = "RWA-FORECAST-2026.2.0"
3410 |  29 | METHODOLOGY = (
3411 |  30 |     "Autoregressive VAR/recurrent market-factor forecast with Monte Carlo portfolio "
3412 |  31 |     "trajectory generation and multi-period path scoring for RWA-aware ALM simulation."
3413 |  32 | )
3414 |  33 | MONEY_Q = Decimal("0.01")
3415 |  34 | RATE_Q = Decimal("0.000001")
3416 |  35 | MONTHS_PER_YEAR = Decimal("12")
3417 |  36 | FACTOR_NAMES = (
3418 |  37 |     "volatility_index",
3419 |  38 |     "credit_spread_bps",
3420 |  39 |     "yield_curve_slope_bps",
3421 |  40 |     "liquidity_index",
3422 |  41 |     "unemployment_indicator",
3423 |  42 |     "gdp_growth_indicator",
3424 |  43 | )
3425 |  44 | 
3426 |  45 | 
3427 |  46 | @dataclass(frozen=True)
3428 |  47 | class MacroState:
3429 |  48 |     """Market-factor vector used by the autoregressive forecast engine."""
3430 |  49 | 
3431 |  50 |     volatility_index: Decimal
3432 |  51 |     credit_spread_bps: Decimal
3433 |  52 |     yield_curve_slope_bps: Decimal
3434 |  53 |     liquidity_index: Decimal
3435 |  54 |     unemployment_indicator: Decimal
3436 |  55 |     gdp_growth_indicator: Decimal
3437 |  56 | 
3438 |  57 | 
3439 |  58 | @dataclass(frozen=True)
3440 |  59 | class Calibration:
3441 |  60 |     """Calibrated long-run mean, volatility and initial state for a forecast run."""
3442 |  61 | 
3443 |  62 |     long_run_mean: MacroState
3444 |  63 |     volatility: MacroState
3445 |  64 |     initial_state: MacroState
3446 |  65 | 
3447 |  66 | 
3448 |  67 | @dataclass
3449 |  68 | class PathAccumulator:
3450 |  69 |     """Mutable trajectory state accumulated while simulating one Monte Carlo path."""
3451 |  70 | 
3452 |  71 |     rows: list[dict[str, Any]]
3453 |  72 |     own_funds: Decimal
3454 |  73 |     cumulative_profit: Decimal = Decimal("0")
3455 |  74 |     cumulative_turnover: Decimal = Decimal("0")
3456 |  75 |     profit_peak: Decimal = Decimal("0")
3457 |  76 |     max_drawdown: Decimal = Decimal("0")
3458 |  77 |     rwa_breach_penalty: Decimal = Decimal("0")
3459 |  78 | 
3460 |  79 | 
3461 |  80 | class RwaForecastService:
3462 |  81 |     """Forecast market parameters, generate Monte Carlo paths and score trajectories.
3463 |  82 | 
3464 |  83 |     The service is deliberately independent from the optimizer services. It produces simulated
3465 |  84 |     paths that can be handed to steering or RATS, while still calculating every RWA point through
3466 |  85 |     ``rwa_calculator``.
3467 |  86 |     """
3468 |  87 | 
3469 |  88 |     def __init__(
3470 |  89 |         self,
3471 |  90 |         nccr_mapping_path: str | Path = NCCR_MAPPING_PATH,
3472 |  91 |         country_info_path: str | Path = PREPROD_COUNTRY_INFO_PATH,
3473 |  92 |         input_package: SteeringInputPackage | None = None,
3474 |  93 |         generated_inputs_root: str | Path | None = None,
3475 |  94 |     ) -> None:
3476 |  95 |         """Initialize forecast service with calculator and generated input package."""
3477 |  96 |         self.calculator = RwaCalculator.from_files(nccr_mapping_path, country_info_path)
3478 |  97 |         if input_package is not None:
3479 |  98 |             self.input_package = input_package
3480 |  99 |         elif generated_inputs_root is not None:
3481 | 100 |             self.input_package = load_steering_input_package(generated_inputs_root)
3482 | 101 |         else:
3483 | 102 |             self.input_package = load_steering_input_package()
3484 | 103 | 
3485 | 104 |     def run(self, request: ForecastRequest) -> ForecastResponse:
3486 | 105 |         """Run autoregressive forecast, Monte Carlo simulation and path scoring."""
3487 | 106 |         self.input_package.ensure_jurisdiction(request.jurisdiction)
3488 | 107 |         calibration = self._calibrate(request)
3489 | 108 |         current_payload = self.calculator.calculate_batch(request.core_info)
3490 | 109 |         if current_payload["errors"]:
3491 | 110 |             raise SteeringDomainError.from_calculator_errors(current_payload["errors"])
3492 | 111 | 
3493 | 112 |         current_rwa = portfolio_rwa(current_payload["results"])
3494 | 113 |         own_funds = current_rwa * request.initial_capital_ratio
3495 | 114 |         market_paths: list[MarketFactorStep] = []
3496 | 115 |         portfolio_paths: list[PortfolioPathStep] = []
3497 | 116 |         scores: list[PathScore] = []
3498 | 117 | 
3499 | 118 |         for path_id in range(request.path_count):
3500 | 119 |             rng = random.Random(request.random_seed + path_id * 1009)  # noqa: S311 # nosec B311
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:41:56.810Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.18

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# Enterprise-Level Analysis Report: RiskTrace Control Tower Recent Changes

## Executive Summary

This comprehensive analysis reviews recent modifications to the RiskTrace Control Tower project, focusing on performance optimization documentation and MCP infrastructure. The review identifies **critical issues requiring immediate attention** alongside several areas for improvement.

---

## 1. Summary of Changes Made

### Session: bob_task_may-17-2026_2-31-18-pm.md (May 17, 2026)

**Task:** Performance optimization analysis for hackathon application
**Mode:** Plan mode
**Deliverables Created:**

1. **PERFORMANCE_OPTIMIZATION_PLAN.md** (365 lines)
   - Detailed performance bottleneck analysis
   - 3-phase optimization roadmap
   - Risk assessment and rollback strategy

2. **PERFORMANCE_IMPLEMENTATION_GUIDE.md** (735 lines)
   - Complete code examples for all optimizations
   - Testing and validation procedures
   - Deployment checklist

3. **PERFORMANCE_OPTIMIZATION_SUMMARY.md** (282 lines)
   - Executive summary of findings
   - Implementation roadmap
   - Success criteria

4. **mcps/EXECUTION_PLAN.md** (561 lines)
   - MCP infrastructure operational guide
   - Step-by-step setup procedures
   - Comprehensive safety disclaimers

5. **mcps/README.md** (236 lines)
   - Quick reference for MCP tooling
   - Service configuration details

---

## 2. Issues Found (Categorized by Severity)

### 🔴 CRITICAL ISSUES

#### C1: **NO ACTUAL CODE CHANGES IMPLEMENTED**
- **Location:** All documentation files
- **Issue:** The session created **only planning documents** with no actual code modifications
- **Impact:** Zero performance improvement delivered despite 6,366-line session
- **Evidence:** Session ended with "Next Step: Switch to Code mode to implement Phase 1 optimizations"
- **Risk:** Stakeholders may believe optimizations are complete when they haven't started
- **Recommendation:** **IMMEDIATELY** clarify that this was planning-only work; no performance improvements exist yet

#### C2: **Hypothetical Performance Data**
- **Location:** All performance documents
- **Issue:** All performance metrics are **estimated/assumed**, not measured
- **Examples:**
  - "Estimated 2000-3000ms p95 latency" (line 18, SUMMARY)
  - "Expected Impact: 80-90% latency reduction" (line 98, PLAN)
  - No actual performance dataset referenced despite task mentioning "performance folder (*.csv/*.json)"
- **Impact:** Optimization plan built on assumptions, not data
- **Risk:** Proposed solutions may not address actual bottlenecks
- **Recommendation:** **MUST** collect baseline performance metrics before proceeding

#### C3: **Code Examples Reference Non-Existent Files**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Code examples reference files that don't exist in the repository:
  - `apps/backend/src/rwa_common/cache.py` (new file, line 18)
  - `apps/backend/src/rwa_common/redis_cache.py` (new file, line 426)
  - `apps/backend/src/rwa_common/db_async.py` (new file, line 274)
  - `apps/backend/src/rwa_common/monitoring.py` (mentioned in PLAN, line 204)
  - `apps/backend/src/rwa_dashboard/repositories_async.py` (new file, line 334)
- **Impact:** Implementation guide cannot be followed without creating these files first
- **Risk:** Developers may waste time trying to import non-existent modules
- **Recommendation:** Clearly mark all code as **proposed/example** code, not existing code

### 🟠 MAJOR ISSUES

#### M1: **Inconsistent File Path References**
- **Location:** PERFORMANCE_OPTIMIZATION_SUMMARY.md, lines 16-31
- **Issue:** Uses markdown link syntax `[path](../path)` but links are broken
- **Examples:**
  - `[apps/backend/src/rwa_dashboard/data.py:127-145](../apps/backend/src/rwa_dashboard/data.py)` - line numbers in link text but not in URL
  - Links won't work in GitHub or most markdown viewers
- **Impact:** Navigation between documents is broken
- **Recommendation:** Use standard relative paths or remove line number references from link text

#### M2: **Contradictory Scope Statements**
- **Location:** Multiple documents
- **Issue:** Task says "do not hardcode hackathon-only shortcuts" but documents are labeled for "hackathon application"
- **Evidence:**
  - Task line 43: "Do not hardcode hackathon-only shortcuts into production paths"
  - Session line 4: "RiskTrace Control Tower hackathon application"
- **Impact:** Unclear whether this is production or hackathon work
- **Risk:** Production systems may receive hackathon-quality code
- **Recommendation:** Clarify scope and remove contradictory statements

#### M3: **Missing Validation Against AGENTS.md**
- **Location:** All documentation
- **Issue:** Documents don't reference or validate against repository's AGENTS.md guidelines
- **Evidence:** AGENTS.md specifies:
  - Backend tests run from `apps/backend/` with `uv run pytest`
  - Single test file: `uv run pytest tests/calculator/test_rwa_backend.py`
  - Coverage gates: 70% minimum
- **Impact:** Proposed changes may violate established patterns
- **Recommendation:** Add section validating compliance with AGENTS.md

#### M4: **Incomplete MCP Safety Disclaimers**
- **Location:** mcps/EXECUTION_PLAN.md, mcps/README.md
- **Issue:** While safety disclaimers exist, they're buried in documentation
- **Evidence:** Critical disclaimer at line 9-29 of EXECUTION_PLAN.md
- **Impact:** Users may miss legal/compliance warnings
- **Recommendation:** Add prominent warning banner at top of README.md

#### M5: **No Rollback Testing Procedures**
- **Location:** PERFORMANCE_OPTIMIZATION_PLAN.md, lines 256-282
- **Issue:** Rollback strategy defined but no testing procedures
- **Evidence:** "Quick Rollback: One-command rollback via feature flag toggle" (line 274) but no test plan
- **Impact:** Rollback may fail when needed
- **Recommendation:** Add rollback testing to deployment checklist

### 🟡 MINOR ISSUES

#### m1: **Inconsistent Terminology**
- **Location:** Multiple files
- **Issue:** Mixes "RiskTrace Control Tower" and "RWA Calculator"
- **Impact:** Confusing for new developers
- **Recommendation:** Standardize on one project name

#### m2: **Placeholder Values in Examples**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Some code examples have placeholder comments like "# ... existing implementation" (line 97)
- **Impact:** Developers may not know what to fill in
- **Recommendation:** Either provide complete examples or clearly mark as pseudocode

#### m3: **Missing Version Control Strategy**
- **Location:** All documentation files
- **Issue:** No version numbers or change tracking in documents
- **Evidence:** PLAN has "Version: 1.0" but no changelog
- **Impact:** Hard to track document evolution
- **Recommendation:** Add changelog section to each document

#### m4: **Inconsistent Code Style in Examples**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Python examples don't consistently follow project's Ruff configuration
- **Evidence:** Line length varies, some examples exceed 100 chars
- **Impact:** Copy-paste code may fail linting
- **Recommendation:** Run all examples through `ruff format`

#### m5: **No Performance Regression Test Suite**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md, lines 610-642
- **Issue:** Performance tests defined but not integrated with existing test suite
- **Evidence:** Uses `@pytest.mark.performance` but no pytest.ini configuration shown
- **Impact:** Tests may not run in CI/CD
- **Recommendation:** Add pytest configuration for performance markers

---

## 3. Assessment of Each Documentation File

### 📄 docs/PERFORMANCE_OPTIMIZATION_PLAN.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Comprehensive bottleneck analysis with specific file locations
- Well-structured 3-phase approach
- Detailed risk assessment with mitigation strategies
- Clear success criteria and monitoring plan

**Weaknesses:**
- All metrics are estimated, not measured
- No baseline performance data referenced
- Missing integration with existing test infrastructure
- No mention of AGENTS.md compliance

**Actionability:** Medium - Good structure but needs actual data

**Completeness:** 85% - Missing baseline measurements and validation

---

### 📄 docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md

**Quality:** ⭐⭐⭐ (3/5)

**Strengths:**
- Detailed code examples for each optimization
- Comprehensive testing strategy
- Clear deployment checklist
- Good separation of concerns (Phase 1/2/3)

**Weaknesses:**
- References non-existent files without clarification
- Code examples not validated against actual codebase
- Missing integration with existing backend structure
- No validation that examples follow project conventions

**Actionability:** Low - Cannot be followed without creating new files first

**Completeness:** 70% - Code examples present but not validated

---

### 📄 docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Excellent executive summary format
- Clear roadmap with timeline
- Good compliance section
- Well-organized metrics tables

**Weaknesses:**
- Broken markdown links
- All improvements are "expected" not "achieved"
- Missing actual performance data
- Status shows "Ready for Implementation" but nothing implemented

**Actionability:** Medium - Good overview but misleading status

**Completeness:** 80% - Good structure, missing actual results

---

### 📄 mcps/EXECUTION_PLAN.md

**Quality:** ⭐⭐⭐⭐⭐ (5/5)

**Strengths:**
- **Excellent** safety disclaimers and legal notices
- Comprehensive step-by-step procedures
- Clear scope definition (MVP vs non-goals)
- Detailed troubleshooting guide
- Good decision trees and workflow diagrams

**Weaknesses:**
- Very long (561 lines) - could benefit from modularization
- Some commands assume specific directory structure
- No automated validation scripts

**Actionability:** High - Can be followed step-by-step

**Completeness:** 95% - Comprehensive operational guide

---

### 📄 mcps/README.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Good quick-start section
- Clear documentation structure
- Proper secret handling guidance
- Links to detailed documentation

**Weaknesses:**
- Safety disclaimer less prominent than in EXECUTION_PLAN
- Could benefit from architecture diagram
- Missing prerequisites section

**Actionability:** High - Quick start is clear

**Completeness:** 85% - Good overview, could add more context

---

## 4. Recommendations for Improvements

### Immediate Actions (Within 24 Hours)

1. **Add Prominent Disclaimer to All Performance Docs:**
   ```markdown
   ⚠️ **PLANNING DOCUMENT ONLY - NO CODE CHANGES IMPLEMENTED**
   
   This document contains proposed optimizations. No actual code modifications
   have been made. All performance metrics are estimates, not measurements.
   ```

2. **Collect Actual Performance Baseline:**
   - Run k6 load tests against current system
   - Document actual p95/p99 latencies
   - Measure actual throughput and error rates
   - Update documents with real data

3. **Validate Code Examples:**
   - Test all code snippets in isolated environment
   - Verify imports work with existing codebase
   - Run through Ruff linter
   - Check against AGENTS.md patterns

### Short-Term Actions (Within 1 Week)

4. **Fix Documentation Issues:**
   - Correct all broken markdown links
   - Add version control and changelogs
   - Standardize terminology
   - Add AGENTS.md compliance section

5. **Create Missing Infrastructure:**
   - Implement `rwa_common/cache.py` module
   - Add performance test markers to pytest.ini
   - Create baseline performance test suite
   - Set up monitoring infrastructure

6. **Enhance MCP Documentation:**
   - Add architecture diagram to README.md
   - Create automated validation scripts
   - Add prerequisites checklist
   - Include troubleshooting flowcharts

### Long-Term Actions (Within 1 Month)

7. **Implement Phase 1 Optimizations:**
   - Switch to Code mode
   - Implement quick wins with feature flags
   - Add comprehensive tests
   - Measure actual improvements

8. **Establish Performance Governance:**
   - Add performance regression tests to CI/CD
   - Set up continuous performance monitoring
   - Create performance review process
   - Document performance SLOs

9. **Complete Documentation Lifecycle:**
   - Add review and approval workflow
   - Implement document versioning
   - Create maintenance schedule
   - Establish ownership and accountability

---

## 5. Red Flags and Concerns Requiring Immediate Attention

### 🚨 RED FLAG #1: Misleading Completion Status

**Issue:** Session marked as "completed" with `attempt_completion` but delivered only planning documents

**Evidence:**
- Session line 6320: "Performance optimization plan completed"
- Session line 6362: "Next Step: Switch to Code mode to implement Phase 1 optimizations"

**Impact:** Stakeholders may believe work is done when it hasn't started

**Action Required:** Immediately communicate that this was Phase 0 (planning) only

---

### 🚨 RED FLAG #2: No Performance Data Exists

**Issue:** Task mentions "performance dataset" and "performance folder (*.csv/*.json)" but no such data found

**Evidence:**
- Task line 9: "Use the dataset columns from performance folder"
- No `performance/` directory in repository
- All metrics in documents are estimates

**Impact:** Entire optimization plan may be solving wrong problems

**Action Required:** Locate or create actual performance dataset before proceeding

---

### 🚨 RED FLAG #3: Architectural Misalignment Risk

**Issue:** Proposed changes (async DB, Redis, parallel processing) are significant architectural changes not validated against existing patterns

**Evidence:**
- AGENTS.md specifies specific patterns (e.g., `uv run pytest`)
- Proposed async changes require major refactoring
- No mention of compatibility with existing microservices architecture

**Impact:** Implementation may break existing functionality

**Action Required:** Conduct architectural review before implementation

---

### 🚨 RED FLAG #4: Compliance and Security Gaps

**Issue:** Performance optimizations may impact regulatory controls but no compliance review mentioned

**Evidence:**
- Task line 40: "Do not remove validation, audit logging, regulatory checks"
- No validation that caching preserves audit trails
- No assessment of cache encryption requirements

**Impact:** May violate regulatory requirements

**Action Required:** Conduct compliance review with legal/risk team

---

## 6. Alignment with Project Architecture

### ✅ Positive Alignments:

1. **Respects Monorepo Structure:** Documents correctly reference `apps/backend/` and `apps/frontend/`
2. **Follows Python Patterns:** Uses type hints, dataclasses, proper imports
3. **Maintains Testing Standards:** Proposes 70% coverage threshold matching AGENTS.md
4. **Preserves Docker Compose:** MCP infrastructure properly separated from application runtime

### ❌ Misalignments:

1. **Database Pooling:** Proposes changes to `db.py` but doesn't account for SQLite vs Postgres differences documented in AGENTS.md
2. **Test Execution:** Performance tests don't follow `uv run pytest` pattern from AGENTS.md
3. **Frontend Dev Server:** Proposes changes but doesn't mention `127.0.0.1` binding requirement from AGENTS.md
4. **Generated Inputs:** No mention of `rwa-generate-missing-inputs` manifest validation requirement

---

## 7. Final Assessment

### Overall Quality Score: ⭐⭐⭐ (3/5)

**Reasoning:**
- **Planning Quality:** Excellent (5/5) - Comprehensive, well-structured
- **Implementation Readiness:** Poor (1/5) - No code changes, no baseline data
- **Documentation Quality:** Good (4/5) - Well-written but has critical gaps
- **Enterprise Readiness:** Fair (2/5) - Missing compliance validation, actual measurements

### Verdict:

This work represents **high-quality planning** but **zero implementation**. The documentation is well-structured and comprehensive, but suffers from critical issues:

1. **No actual performance improvements delivered**
2. **All metrics are hypothetical**
3. **Code examples reference non-existent files**
4. **No validation against actual codebase**

### Recommended Next Steps:

1. ✅ **Accept** the planning documents as Phase 0 deliverables
2. ⚠️ **Clarify** that no code changes were made
3. 📊 **Collect** actual performance baseline data
4. 🔍 **Validate** proposed solutions against real bottlenecks
5. 👥 **Review** with compliance/legal before implementation
6. 💻 **Implement** Phase 1 in Code mode with proper testing
7. 📈 **Measure** actual improvements vs. estimates

---

**Report Prepared:** 2026-05-17  
**Analysis Scope:** Session bob_task_may-17-2026_2-31-18-pm.md + 5 documentation files  
**Reviewer Mode:** Enterprise-level critical analysis  
**Confidence Level:** High (based on comprehensive document review)
</result>
</attempt_completion>

---

**User:**

[TASK RESUMPTION] Resuming task...
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:51:53.542Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.35

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>


# Current Workspace Directory (/home/mateusz/project/risk-trace-control-tower) Files
.gitignore
.semgrepignore
AGENTS.md
.bob/
.github/
apps/
apps/docker-compose.yml
apps/backend/.dockerignore
apps/backend/.env.example
apps/backend/.gitignore
apps/backend/.python-version
apps/backend/Dockerfile
apps/backend/README.md
apps/backend/tests/agents/__init__.py
apps/backend/tests/agents/conftest.py
apps/backend/tests/agents/test_api.py
apps/backend/tests/agents/test_observability.py
apps/backend/tests/agents/test_tools.py
apps/backend/tests/agents/test_validation.py
apps/backend/tests/agents/test_watsonx.py
apps/backend/tests/agents/test_workflow.py
apps/backend/tests/calculator/test_capital_modules.py
apps/backend/tests/calculator/test_fastapi_microservice.py
apps/backend/tests/calculator/test_golden_regression.py
apps/backend/tests/calculator/test_rwa_backend.py
apps/backend/tests/forecast/test_forecast_service.py
apps/backend/tests/projection/test_calendar.py
apps/backend/tests/rats/test_rats_service.py
apps/backend/tests/steering/test_missing_inputs.py
apps/backend/tests/steering/test_steering_service.py
apps/frontend/.env.example
apps/frontend/.gitignore
apps/frontend/Dockerfile
apps/frontend/nginx.conf
apps/frontend/package-lock.json
apps/frontend/package.json
apps/frontend/scripts/playwright-web-server.mjs
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
bob_sessions/bob_task_may-17-2026_2-31-18-pm.md
bob_sessions/bob_task_may-17-2026_2-31-18-pm.png
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
docker/docker-compose.prod.yml
docker/docker-compose.yml
docker/nginx-host/rwa.conf
docs/
docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md
docs/PERFORMANCE_OPTIMIZATION_PLAN.md
docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md
docs/RCT-15_TECHNICAL_ANALYSIS.md
docs/RCT-16_TECHNICAL_ANALYSIS.md
docs/RCT-17_IMPLEMENTATION_SUMMARY.md
docs/RCT-17_TECHNICAL_ANALYSIS.md
docs/RCT-18_IMPLEMENTATION_SUMMARY.md
docs/RCT-18_TECHNICAL_ANALYSIS.md
docs/RCT-18_VALIDATION_REPORT.md
docs/RCT-40_TECHNICAL_ANALYSIS.md
docs/RCT-40_WATSONX_FINALIZATION.md
docs/agents/architecture.md
docs/agents/contracts.md
docs/agents/validation.md
infra/
infra/helm/rwa-backend/templates/_helpers.tpl
infra/helm/rwa-backend/templates/deployment.yaml
infra/helm/rwa-backend/templates/hpa.yaml
infra/helm/rwa-backend/templates/pdb.yaml
infra/helm/rwa-backend/templates/service.yaml
infra/helm/rwa-frontend/templates/_helpers.tpl
infra/helm/rwa-frontend/templates/deployment.yaml
infra/helm/rwa-frontend/templates/hpa.yaml
infra/helm/rwa-frontend/templates/service.yaml
infra/helm/rwa-platform/Chart.lock
infra/helm/rwa-platform/values-dev.yaml
infra/helm/rwa-platform/values-staging.yaml
infra/kubernetes/namespaces/rwa-dev.yaml
infra/kubernetes/namespaces/rwa-prod.yaml
infra/kubernetes/network-policies/rwa-dev-allow.yaml
infra/kubernetes/network-policies/rwa-dev-default-deny.yaml
infra/kubernetes/network-policies/rwa-prod-allow.yaml
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
k8s/opa/templates/require-resource-limits.yaml
mcps/
mcps/.env.example
mcps/docker-compose.yml
mcps/EXECUTION_PLAN.md
mcps/README.md
mcps/regulatory_mcp/.dockerignore
mcps/regulatory_mcp/.gitignore
mcps/regulatory_mcp/Dockerfile
mcps/regulatory_mcp/package-lock.json
mcps/regulatory_mcp/package.json
mcps/regulatory_mcp/README.md
mcps/regulatory_mcp/test-startup.sh
mcps/regulatory_mcp/tsconfig.json
mcps/regulatory_mcp/vitest.config.ts
mcps/regulatory_mcp/data/regulations/BCBS239.json
mcps/regulatory_mcp/data/regulations/CRR3.json
mcps/regulatory_mcp/data/regulations/DORA.json
mcps/regulatory_mcp/data/regulations/EBA_ICT_SECURITY.json
mcps/regulatory_mcp/data/regulations/EBA_REPORTING_4.json
mcps/regulatory_mcp/data/regulations/GDPR.json
mcps/regulatory_mcp/data/regulations/INTERNAL_AUDIT_EVIDENCE.json
mcps/regulatory_mcp/data/regulations/INTERNAL_RULE_GOVERNANCE.json
mcps/regulatory_mcp/data/regulations/INTERNAL_SDLC.json
mcps/regulatory_mcp/src/config.test.ts
mcps/regulatory_mcp/src/config.ts
mcps/regulatory_mcp/src/index.ts
mcps/regulatory_mcp/src/server.ts
mcps/regulatory_mcp/src/resources/registerPrompts.ts
mcps/regulatory_mcp/src/resources/registerResources.test.ts
mcps/regulatory_mcp/src/resources/registerResources.ts
mcps/regulatory_mcp/src/schemas/common.ts
mcps/regulatory_mcp/src/schemas/control.ts
mcps/regulatory_mcp/src/schemas/evidence.ts
mcps/regulatory_mcp/src/schemas/finding.ts
mcps/regulatory_mcp/src/schemas/regulation.ts
mcps/regulatory_mcp/src/schemas/schemas.test.ts
mcps/regulatory_mcp/src/services/controlMatcher.test.ts
mcps/regulatory_mcp/src/services/controlMatcher.ts
mcps/regulatory_mcp/src/services/corpusLoader.test.ts
mcps/regulatory_mcp/src/services/corpusLoader.ts
mcps/regulatory_mcp/src/services/corpusStore.test.ts
mcps/regulatory_mcp/src/services/corpusStore.ts
mcps/regulatory_mcp/src/services/generationServices.test.ts
mcps/regulatory_mcp/src/services/generationServices.ts
mcps/regulatory_mcp/src/services/regulationSearch.test.ts
mcps/regulatory_mcp/src/services/regulationSearch.ts
mcps/regulatory_mcp/src/services/releaseReadiness.test.ts
mcps/regulatory_mcp/src/services/releaseReadiness.ts
mcps/regulatory_mcp/src/services/reportGenerator.ts
mcps/regulatory_mcp/src/services/reviewServices.test.ts
mcps/regulatory_mcp/src/services/reviewServices.ts
mcps/regulatory_mcp/src/services/serviceUtils.ts
mcps/regulatory_mcp/src/tools/registerTools.test.ts
mcps/regulatory_mcp/src/tools/registerTools.ts
mcps/sonarqube/backend-project.properties
mcps/sonarqube/frontend-project.properties
observability/
observability/alertmanager.yaml
observability/grafana/dashboards/dora-metrics.json
observability/grafana/dashboards/kafka.json
observability/grafana/dashboards/rwa-application.json
scripts/

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I have completed the comprehensive enterprise-level analysis of the recent changes to the RiskTrace Control Tower project. The analysis report has been delivered and covers:

## Key Findings Summary:

### Critical Issues Identified:
1. **No actual code changes were implemented** - only planning documents were created
2. **All performance metrics are hypothetical** - no baseline data exists
3. **Code examples reference non-existent files** - implementation guide cannot be followed as-is
4. **Misleading completion status** - work appears complete but hasn't started

### Documentation Quality:
- **PERFORMANCE_OPTIMIZATION_PLAN.md**: ⭐⭐⭐⭐ (4/5) - Excellent planning structure
- **PERFORMANCE_IMPLEMENTATION_GUIDE.md**: ⭐⭐⭐ (3/5) - Good examples but not validated
- **PERFORMANCE_OPTIMIZATION_SUMMARY.md**: ⭐⭐⭐⭐ (4/5) - Well-organized but misleading status
- **mcps/EXECUTION_PLAN.md**: ⭐⭐⭐⭐⭐ (5/5) - Outstanding operational guide
- **mcps/README.md**: ⭐⭐⭐⭐ (4/5) - Clear and actionable

### Overall Assessment:
**Quality Score: ⭐⭐⭐ (3/5)**

The work represents high-quality planning but zero implementation. The documentation is comprehensive and well-structured, but suffers from critical gaps including lack of actual performance data, unvalidated code examples, and potential architectural misalignments.

### Immediate Recommendations:
1. Add prominent disclaimers that this is planning-only work
2. Collect actual performance baseline data
3. Validate all code examples against the existing codebase
4. Conduct compliance review before implementation
5. Switch to Code mode to begin actual implementation

The analysis provides detailed categorization of issues (Critical, Major, Minor), specific line-by-line references, and actionable recommendations for each concern identified.

---

**User:**

[ERROR] You did not use a tool in your previous response! Please retry with a tool use.

# Reminder: Instructions for Tool Use

Tool uses are formatted using XML-style tags. The tool name itself becomes the XML tag name. Each parameter is enclosed within its own set of tags. Here's the structure:

<actual_tool_name>
<parameter1_name>value1</parameter1_name>
<parameter2_name>value2</parameter2_name>
...
</actual_tool_name>

For example, to use the attempt_completion tool:

<attempt_completion>
<result>
I have completed the task...
</result>
</attempt_completion>

Always use the actual tool name as the XML tag name for proper parsing and execution.

# Next Steps

If you have completed the user's task, use the attempt_completion tool.
If you require additional information from the user, use the ask_followup_question tool.
Otherwise, if you have not completed the task and do not need additional information, then proceed with the next step of the task.
(This is an automated message, so do not respond to it conversationally.)
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T13:52:04.447Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.52

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>ask</slug>
<name>❓ Ask</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# Enterprise-Level Analysis Report: RiskTrace Control Tower Recent Changes

## Executive Summary

This comprehensive analysis reviews recent modifications to the RiskTrace Control Tower project, focusing on performance optimization documentation and MCP infrastructure. The review identifies **critical issues requiring immediate attention** alongside several areas for improvement.

---

## 1. Summary of Changes Made

### Session: bob_task_may-17-2026_2-31-18-pm.md (May 17, 2026)

**Task:** Performance optimization analysis for hackathon application
**Mode:** Plan mode
**Deliverables Created:**

1. **PERFORMANCE_OPTIMIZATION_PLAN.md** (365 lines)
   - Detailed performance bottleneck analysis
   - 3-phase optimization roadmap
   - Risk assessment and rollback strategy

2. **PERFORMANCE_IMPLEMENTATION_GUIDE.md** (735 lines)
   - Complete code examples for all optimizations
   - Testing and validation procedures
   - Deployment checklist

3. **PERFORMANCE_OPTIMIZATION_SUMMARY.md** (282 lines)
   - Executive summary of findings
   - Implementation roadmap
   - Success criteria

4. **mcps/EXECUTION_PLAN.md** (561 lines)
   - MCP infrastructure operational guide
   - Step-by-step setup procedures
   - Comprehensive safety disclaimers

5. **mcps/README.md** (236 lines)
   - Quick reference for MCP tooling
   - Service configuration details

---

## 2. Issues Found (Categorized by Severity)

### 🔴 CRITICAL ISSUES

#### C1: **NO ACTUAL CODE CHANGES IMPLEMENTED**
- **Location:** All documentation files
- **Issue:** The session created **only planning documents** with no actual code modifications
- **Impact:** Zero performance improvement delivered despite 6,366-line session
- **Evidence:** Session ended with "Next Step: Switch to Code mode to implement Phase 1 optimizations"
- **Risk:** Stakeholders may believe optimizations are complete when they haven't started
- **Recommendation:** **IMMEDIATELY** clarify that this was planning-only work; no performance improvements exist yet

#### C2: **Hypothetical Performance Data**
- **Location:** All performance documents
- **Issue:** All performance metrics are **estimated/assumed**, not measured
- **Examples:**
  - "Estimated 2000-3000ms p95 latency" (line 18, SUMMARY)
  - "Expected Impact: 80-90% latency reduction" (line 98, PLAN)
  - No actual performance dataset referenced despite task mentioning "performance folder (*.csv/*.json)"
- **Impact:** Optimization plan built on assumptions, not data
- **Risk:** Proposed solutions may not address actual bottlenecks
- **Recommendation:** **MUST** collect baseline performance metrics before proceeding

#### C3: **Code Examples Reference Non-Existent Files**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Code examples reference files that don't exist in the repository:
  - `apps/backend/src/rwa_common/cache.py` (new file, line 18)
  - `apps/backend/src/rwa_common/redis_cache.py` (new file, line 426)
  - `apps/backend/src/rwa_common/db_async.py` (new file, line 274)
  - `apps/backend/src/rwa_common/monitoring.py` (mentioned in PLAN, line 204)
  - `apps/backend/src/rwa_dashboard/repositories_async.py` (new file, line 334)
- **Impact:** Implementation guide cannot be followed without creating these files first
- **Risk:** Developers may waste time trying to import non-existent modules
- **Recommendation:** Clearly mark all code as **proposed/example** code, not existing code

### 🟠 MAJOR ISSUES

#### M1: **Inconsistent File Path References**
- **Location:** PERFORMANCE_OPTIMIZATION_SUMMARY.md, lines 16-31
- **Issue:** Uses markdown link syntax `[path](../path)` but links are broken
- **Examples:**
  - `[apps/backend/src/rwa_dashboard/data.py:127-145](../apps/backend/src/rwa_dashboard/data.py)` - line numbers in link text but not in URL
  - Links won't work in GitHub or most markdown viewers
- **Impact:** Navigation between documents is broken
- **Recommendation:** Use standard relative paths or remove line number references from link text

#### M2: **Contradictory Scope Statements**
- **Location:** Multiple documents
- **Issue:** Task says "do not hardcode hackathon-only shortcuts" but documents are labeled for "hackathon application"
- **Evidence:**
  - Task line 43: "Do not hardcode hackathon-only shortcuts into production paths"
  - Session line 4: "RiskTrace Control Tower hackathon application"
- **Impact:** Unclear whether this is production or hackathon work
- **Risk:** Production systems may receive hackathon-quality code
- **Recommendation:** Clarify scope and remove contradictory statements

#### M3: **Missing Validation Against AGENTS.md**
- **Location:** All documentation
- **Issue:** Documents don't reference or validate against repository's AGENTS.md guidelines
- **Evidence:** AGENTS.md specifies:
  - Backend tests run from `apps/backend/` with `uv run pytest`
  - Single test file: `uv run pytest tests/calculator/test_rwa_backend.py`
  - Coverage gates: 70% minimum
- **Impact:** Proposed changes may violate established patterns
- **Recommendation:** Add section validating compliance with AGENTS.md

#### M4: **Incomplete MCP Safety Disclaimers**
- **Location:** mcps/EXECUTION_PLAN.md, mcps/README.md
- **Issue:** While safety disclaimers exist, they're buried in documentation
- **Evidence:** Critical disclaimer at line 9-29 of EXECUTION_PLAN.md
- **Impact:** Users may miss legal/compliance warnings
- **Recommendation:** Add prominent warning banner at top of README.md

#### M5: **No Rollback Testing Procedures**
- **Location:** PERFORMANCE_OPTIMIZATION_PLAN.md, lines 256-282
- **Issue:** Rollback strategy defined but no testing procedures
- **Evidence:** "Quick Rollback: One-command rollback via feature flag toggle" (line 274) but no test plan
- **Impact:** Rollback may fail when needed
- **Recommendation:** Add rollback testing to deployment checklist

### 🟡 MINOR ISSUES

#### m1: **Inconsistent Terminology**
- **Location:** Multiple files
- **Issue:** Mixes "RiskTrace Control Tower" and "RWA Calculator"
- **Impact:** Confusing for new developers
- **Recommendation:** Standardize on one project name

#### m2: **Placeholder Values in Examples**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Some code examples have placeholder comments like "# ... existing implementation" (line 97)
- **Impact:** Developers may not know what to fill in
- **Recommendation:** Either provide complete examples or clearly mark as pseudocode

#### m3: **Missing Version Control Strategy**
- **Location:** All documentation files
- **Issue:** No version numbers or change tracking in documents
- **Evidence:** PLAN has "Version: 1.0" but no changelog
- **Impact:** Hard to track document evolution
- **Recommendation:** Add changelog section to each document

#### m4: **Inconsistent Code Style in Examples**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md
- **Issue:** Python examples don't consistently follow project's Ruff configuration
- **Evidence:** Line length varies, some examples exceed 100 chars
- **Impact:** Copy-paste code may fail linting
- **Recommendation:** Run all examples through `ruff format`

#### m5: **No Performance Regression Test Suite**
- **Location:** PERFORMANCE_IMPLEMENTATION_GUIDE.md, lines 610-642
- **Issue:** Performance tests defined but not integrated with existing test suite
- **Evidence:** Uses `@pytest.mark.performance` but no pytest.ini configuration shown
- **Impact:** Tests may not run in CI/CD
- **Recommendation:** Add pytest configuration for performance markers

---

## 3. Assessment of Each Documentation File

### 📄 docs/PERFORMANCE_OPTIMIZATION_PLAN.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Comprehensive bottleneck analysis with specific file locations
- Well-structured 3-phase approach
- Detailed risk assessment with mitigation strategies
- Clear success criteria and monitoring plan

**Weaknesses:**
- All metrics are estimated, not measured
- No baseline performance data referenced
- Missing integration with existing test infrastructure
- No mention of AGENTS.md compliance

**Actionability:** Medium - Good structure but needs actual data

**Completeness:** 85% - Missing baseline measurements and validation

---

### 📄 docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md

**Quality:** ⭐⭐⭐ (3/5)

**Strengths:**
- Detailed code examples for each optimization
- Comprehensive testing strategy
- Clear deployment checklist
- Good separation of concerns (Phase 1/2/3)

**Weaknesses:**
- References non-existent files without clarification
- Code examples not validated against actual codebase
- Missing integration with existing backend structure
- No validation that examples follow project conventions

**Actionability:** Low - Cannot be followed without creating new files first

**Completeness:** 70% - Code examples present but not validated

---

### 📄 docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Excellent executive summary format
- Clear roadmap with timeline
- Good compliance section
- Well-organized metrics tables

**Weaknesses:**
- Broken markdown links
- All improvements are "expected" not "achieved"
- Missing actual performance data
- Status shows "Ready for Implementation" but nothing implemented

**Actionability:** Medium - Good overview but misleading status

**Completeness:** 80% - Good structure, missing actual results

---

### 📄 mcps/EXECUTION_PLAN.md

**Quality:** ⭐⭐⭐⭐⭐ (5/5)

**Strengths:**
- **Excellent** safety disclaimers and legal notices
- Comprehensive step-by-step procedures
- Clear scope definition (MVP vs non-goals)
- Detailed troubleshooting guide
- Good decision trees and workflow diagrams

**Weaknesses:**
- Very long (561 lines) - could benefit from modularization
- Some commands assume specific directory structure
- No automated validation scripts

**Actionability:** High - Can be followed step-by-step

**Completeness:** 95% - Comprehensive operational guide

---

### 📄 mcps/README.md

**Quality:** ⭐⭐⭐⭐ (4/5)

**Strengths:**
- Good quick-start section
- Clear documentation structure
- Proper secret handling guidance
- Links to detailed documentation

**Weaknesses:**
- Safety disclaimer less prominent than in EXECUTION_PLAN
- Could benefit from architecture diagram
- Missing prerequisites section

**Actionability:** High - Quick start is clear

**Completeness:** 85% - Good overview, could add more context

---

## 4. Recommendations for Improvements

### Immediate Actions (Within 24 Hours)

1. **Add Prominent Disclaimer to All Performance Docs:**
   ```markdown
   ⚠️ **PLANNING DOCUMENT ONLY - NO CODE CHANGES IMPLEMENTED**
   
   This document contains proposed optimizations. No actual code modifications
   have been made. All performance metrics are estimates, not measurements.
   ```

2. **Collect Actual Performance Baseline:**
   - Run k6 load tests against current system
   - Document actual p95/p99 latencies
   - Measure actual throughput and error rates
   - Update documents with real data

3. **Validate Code Examples:**
   - Test all code snippets in isolated environment
   - Verify imports work with existing codebase
   - Run through Ruff linter
   - Check against AGENTS.md patterns

### Short-Term Actions (Within 1 Week)

4. **Fix Documentation Issues:**
   - Correct all broken markdown links
   - Add version control and changelogs
   - Standardize terminology
   - Add AGENTS.md compliance section

5. **Create Missing Infrastructure:**
   - Implement `rwa_common/cache.py` module
   - Add performance test markers to pytest.ini
   - Create baseline performance test suite
   - Set up monitoring infrastructure

6. **Enhance MCP Documentation:**
   - Add architecture diagram to README.md
   - Create automated validation scripts
   - Add prerequisites checklist
   - Include troubleshooting flowcharts

### Long-Term Actions (Within 1 Month)

7. **Implement Phase 1 Optimizations:**
   - Switch to Code mode
   - Implement quick wins with feature flags
   - Add comprehensive tests
   - Measure actual improvements

8. **Establish Performance Governance:**
   - Add performance regression tests to CI/CD
   - Set up continuous performance monitoring
   - Create performance review process
   - Document performance SLOs

9. **Complete Documentation Lifecycle:**
   - Add review and approval workflow
   - Implement document versioning
   - Create maintenance schedule
   - Establish ownership and accountability

---

## 5. Red Flags and Concerns Requiring Immediate Attention

### 🚨 RED FLAG #1: Misleading Completion Status

**Issue:** Session marked as "completed" with `attempt_completion` but delivered only planning documents

**Evidence:**
- Session line 6320: "Performance optimization plan completed"
- Session line 6362: "Next Step: Switch to Code mode to implement Phase 1 optimizations"

**Impact:** Stakeholders may believe work is done when it hasn't started

**Action Required:** Immediately communicate that this was Phase 0 (planning) only

---

### 🚨 RED FLAG #2: No Performance Data Exists

**Issue:** Task mentions "performance dataset" and "performance folder (*.csv/*.json)" but no such data found

**Evidence:**
- Task line 9: "Use the dataset columns from performance folder"
- No `performance/` directory in repository
- All metrics in documents are estimates

**Impact:** Entire optimization plan may be solving wrong problems

**Action Required:** Locate or create actual performance dataset before proceeding

---

### 🚨 RED FLAG #3: Architectural Misalignment Risk

**Issue:** Proposed changes (async DB, Redis, parallel processing) are significant architectural changes not validated against existing patterns

**Evidence:**
- AGENTS.md specifies specific patterns (e.g., `uv run pytest`)
- Proposed async changes require major refactoring
- No mention of compatibility with existing microservices architecture

**Impact:** Implementation may break existing functionality

**Action Required:** Conduct architectural review before implementation

---

### 🚨 RED FLAG #4: Compliance and Security Gaps

**Issue:** Performance optimizations may impact regulatory controls but no compliance review mentioned

**Evidence:**
- Task line 40: "Do not remove validation, audit logging, regulatory checks"
- No validation that caching preserves audit trails
- No assessment of cache encryption requirements

**Impact:** May violate regulatory requirements

**Action Required:** Conduct compliance review with legal/risk team

---

## 6. Alignment with Project Architecture

### ✅ Positive Alignments:

1. **Respects Monorepo Structure:** Documents correctly reference `apps/backend/` and `apps/frontend/`
2. **Follows Python Patterns:** Uses type hints, dataclasses, proper imports
3. **Maintains Testing Standards:** Proposes 70% coverage threshold matching AGENTS.md
4. **Preserves Docker Compose:** MCP infrastructure properly separated from application runtime

### ❌ Misalignments:

1. **Database Pooling:** Proposes changes to `db.py` but doesn't account for SQLite vs Postgres differences documented in AGENTS.md
2. **Test Execution:** Performance tests don't follow `uv run pytest` pattern from AGENTS.md
3. **Frontend Dev Server:** Proposes changes but doesn't mention `127.0.0.1` binding requirement from AGENTS.md
4. **Generated Inputs:** No mention of `rwa-generate-missing-inputs` manifest validation requirement

---

## 7. Final Assessment

### Overall Quality Score: ⭐⭐⭐ (3/5)

**Reasoning:**
- **Planning Quality:** Excellent (5/5) - Comprehensive, well-structured
- **Implementation Readiness:** Poor (1/5) - No code changes, no baseline data
- **Documentation Quality:** Good (4/5) - Well-written but has critical gaps
- **Enterprise Readiness:** Fair (2/5) - Missing compliance validation, actual measurements

### Verdict:

This work represents **high-quality planning** but **zero implementation**. The documentation is well-structured and comprehensive, but suffers from critical issues:

1. **No actual performance improvements delivered**
2. **All metrics are hypothetical**
3. **Code examples reference non-existent files**
4. **No validation against actual codebase**

### Recommended Next Steps:

1. ✅ **Accept** the planning documents as Phase 0 deliverables
2. ⚠️ **Clarify** that no code changes were made
3. 📊 **Collect** actual performance baseline data
4. 🔍 **Validate** proposed solutions against real bottlenecks
5. 👥 **Review** with compliance/legal before implementation
6. 💻 **Implement** Phase 1 in Code mode with proper testing
7. 📈 **Measure** actual improvements vs. estimates

---

**Report Prepared:** 2026-05-17  
**Analysis Scope:** Session bob_task_may-17-2026_2-31-18-pm.md + 5 documentation files  
**Reviewer Mode:** Enterprise-level critical analysis  
**Confidence Level:** High (based on comprehensive document review)
</result>
</attempt_completion>

---

**User:**

[attempt_completion] Result:
The user has provided feedback on the results. Consider their input to continue the task, and then attempt completion again.
<feedback>
i don't like yours answer
</feedback>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:01:16.680Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.71

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I understand you're not satisfied with my analysis. Let me ask some clarifying questions to better understand what you're looking for.

<ask_followup_question>
<question>What specific aspects of the analysis would you like me to improve or change? Please select what's most important to you:</question>
<follow_up>
<suggest>Focus more on what was actually accomplished and less on criticisms - I want to see the positive aspects highlighted</suggest>
<suggest>Provide a shorter, more concise summary - the report is too long and detailed</suggest>
<suggest>Focus specifically on technical accuracy of the code examples and whether they would actually work</suggest>
<suggest>Analyze whether the MCP infrastructure documentation is production-ready and what's missing</suggest>
</follow_up>
</ask_followup_question>

---

**User:**

[ask_followup_question for 'What specific aspects of the analysis would you like me to improve or change? Please select what's most important to you:'] Result:
<answer>
Analyze whether the MCP infrastructure documentation is production-ready and what's missing
</answer>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:01:34.764Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.90

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

Thank you for clarifying. Let me conduct a focused analysis on whether the MCP infrastructure documentation is production-ready. I'll examine the actual MCP implementation files and configuration.

<read_file>
<args>
  <file>
    <path>mcps/docker-compose.yml</path>
  </file>
  <file>
    <path>mcps/regulatory_m

[Response interrupted by a tool use result. Only one tool may be used at a time and should be placed at the end of the message.]

---

**User:**

[read_file for 'mcps/docker-compose.yml'. Reading multiple files at once is more efficient for the LLM. If other files are relevant to your current task, please read them simultaneously.] Result:
The tool execution failed with the following error:
<error>
Tool "read_file" is not allowed in orchestrator mode.
</error>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:01:41.108Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.08

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I need to switch to a mode that can read files to analyze the MCP infrastructure. Let me delegate this to Ask mode which has the appropriate tools.

<new_task>
<mode>ask</mode>
<message>Conduct a focused production-readiness analysis of the MCP infrastructure documentation and implementation. Specifically analyze:

1. **MCP Infrastructure Files:**
   - mcps/docker-compose.yml
   - mcps/regulatory_mcp/package.json
   - mcps/regulatory_mcp/Dockerfile
   - mcps/regulatory_mcp/src/index.ts
   - mcps/regulatory_mcp/src/server.ts

2. **Production Readiness Assessment:**
   - Are all dependencies properly versioned and locked?
   - Is error handling comprehensive?
   - Are security configurations production-grade?
   - Is the Docker configuration optimized for production?
   - Are there health checks and monitoring?
   - Is the TypeScript code properly typed and tested?

3. **Documentation Completeness:**
   - Does EXECUTION_PLAN.md cover all production scenarios?
   - Are there gaps in operational procedures?
   - Is disaster recovery documented?
   - Are scaling considerations addressed?

4. **What's Missing for Production:**
   - List specific gaps that would prevent production deployment
   - Identify security vulnerabilities or concerns
   - Note missing operational procedures
   - Highlight any hardcoded values or secrets

Provide a concise, actionable report focused on production readiness, not general criticism. Focus on what works well and what specific items need to be added for production use.</message>
</new_task>

---

**User:**

[new_task completed] Result: # MCP Infrastructure Production Readiness Analysis

## Executive Summary

The MCP infrastructure demonstrates **strong foundational architecture** with good separation of concerns and comprehensive documentation. However, several **critical production gaps** exist that must be addressed before deployment. The infrastructure is currently **development-ready but not production-ready**.

**Overall Assessment:** 🟡 **60% Production Ready** - Solid foundation, needs hardening

---

## 1. Dependency Management & Versioning

### ✅ What Works Well

- **Locked dependencies**: [`package-lock.json`](mcps/regulatory_mcp/package-lock.json:1-50) exists with lockfileVersion 3
- **Engine constraints**: Node.js >=20.0.0 specified in [`package.json`](mcps/regulatory_mcp/package.json:36-38)
- **Minimal dependency surface**: Only 2 runtime dependencies (@modelcontextprotocol/sdk, zod)
- **Docker multi-stage builds**: Proper separation of build and runtime stages in [`Dockerfile`](mcps/regulatory_mcp/Dockerfile:1-24)

### ❌ Critical Gaps

1. **Unversioned Docker base images**
   - [`Dockerfile`](mcps/regulatory_mcp/Dockerfile:1) uses `node:20-alpine` (floating tag)
   - **Risk**: Breaking changes in Node.js 20.x updates
   - **Fix Required**: Pin to specific digest or patch version (e.g., `node:20.18.1-alpine`)

2. **Unversioned third-party images in docker-compose**
   - [`docker-compose.yml`](mcps/docker-compose.yml:15) uses `postgres:16-alpine` (floating)
   - [`docker-compose.yml`](mcps/docker-compose.yml:34) uses `sonarqube:community` (latest)
   - [`docker-compose.yml`](mcps/docker-compose.yml:271) uses `ghcr.io/zaproxy/zaproxy:stable` (floating)
   - **Risk**: Unpredictable behavior across environments
   - **Fix Required**: Pin all images to specific versions with SHA256 digests

3. **No dependency vulnerability scanning**
   - No automated checks for npm package vulnerabilities
   - **Fix Required**: Add `npm audit` to CI/CD pipeline

---

## 2. Error Handling & Resilience

### ✅ What Works Well

- **Top-level error handler**: [`index.ts`](mcps/regulatory_mcp/src/index.ts:23-26) catches fatal errors
- **Health checks**: Comprehensive health checks for SonarQube and ZAP in [`docker-compose.yml`](mcps/docker-compose.yml:20-29)
- **Retry logic**: SonarQube init has 60-attempt retry loop with 5s intervals
- **Graceful degradation**: Services use `depends_on` with health conditions

### ❌ Critical Gaps

1. **No error recovery in MCP server**
   - [`server.ts`](mcps/regulatory_mcp/src/server.ts:10-32) has no try-catch around tool registration
   - **Risk**: Single tool registration failure crashes entire server
   - **Fix Required**: Wrap each registration in try-catch, log errors, continue

2. **No timeout configuration**
   - MCP server has no request timeout limits
   - **Risk**: Hung requests can exhaust resources
   - **Fix Required**: Add configurable timeouts (default 30s)

3. **No circuit breaker pattern**
   - No protection against cascading failures
   - **Fix Required**: Implement circuit breakers for external service calls

4. **Insufficient logging**
   - Only startup logs in [`index.ts`](mcps/regulatory_mcp/src/index.ts:14-18)
   - No structured logging (JSON format)
   - No log levels (debug, info, warn, error)
   - **Fix Required**: Add structured logging library (e.g., pino)

---

## 3. Security Configuration

### ✅ What Works Well

- **Secret management**: Secrets in `.env` file, not committed (`.env.example` provided)
- **Required secrets validation**: [`docker-compose.yml`](mcps/docker-compose.yml:19) uses `?` syntax to enforce secrets
- **Least privilege**: Docker containers run as non-root where possible
- **Network isolation**: Services use internal Docker networks
- **API key authentication**: ZAP requires API key and MCP security key

### ❌ Critical Gaps

1. **Hardcoded localhost bindings**
   - [`docker-compose.yml`](mcps/docker-compose.yml:43) binds to `127.0.0.1` (good for dev, bad for production)
   - **Risk**: Cannot access from other containers in production
   - **Fix Required**: Make bind address configurable via environment variable

2. **No secrets rotation mechanism**
   - Manual rotation process documented but not automated
   - **Fix Required**: Add automated secret rotation with grace periods

3. **No TLS/SSL configuration**
   - All services communicate over HTTP
   - **Risk**: Credentials and data transmitted in plaintext
   - **Fix Required**: Add TLS termination for production deployments

4. **Weak password requirements**
   - No validation of password strength in `.env.example`
   - **Fix Required**: Document minimum password requirements (length, complexity)

5. **No rate limiting**
   - MCP server has no request rate limits
   - **Risk**: DoS attacks or resource exhaustion
   - **Fix Required**: Add rate limiting middleware

6. **No input validation documentation**
   - Tool schemas exist but validation approach unclear
   - **Fix Required**: Document input sanitization strategy

---

## 4. Docker Configuration Optimization

### ✅ What Works Well

- **Multi-stage builds**: Separates build and runtime in [`Dockerfile`](mcps/regulatory_mcp/Dockerfile:1-24)
- **Cache optimization**: `npm ci` before copying source code
- **Minimal runtime**: Uses Alpine Linux base
- **Cache cleanup**: `npm cache clean --force` in production stage
- **Health checks**: Comprehensive health check definitions

### ❌ Critical Gaps

1. **No resource limits**
   - No CPU or memory limits defined
   - **Risk**: Container can consume all host resources
   - **Fix Required**: Add resource limits to all services:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 512M
       reservations:
         cpus: '0.5'
         memory: 256M
   ```

2. **No restart policies**
   - Services don't auto-restart on failure
   - **Fix Required**: Add `restart: unless-stopped` to production services

3. **No security options**
   - Missing security hardening (read-only root filesystem, no new privileges)
   - **Fix Required**: Add security options:
   ```yaml
   security_opt:
     - no-new-privileges:true
   read_only: true
   ```

4. **Volume permissions not documented**
   - No guidance on volume ownership/permissions
   - **Fix Required**: Document required volume permissions

---

## 5. Health Checks & Monitoring

### ✅ What Works Well

- **Comprehensive health checks**: SonarQube, ZAP, and Postgres all have health checks
- **Appropriate intervals**: 10-15s intervals with reasonable retries
- **Start periods**: Services have grace periods for initialization
- **Health check tool**: `health_check` MCP tool for connectivity verification

### ❌ Critical Gaps

1. **No health check for regulatory MCP**
   - [`docker-compose.yml`](mcps/docker-compose.yml:4-12) has no health check for main service
   - **Fix Required**: Add HTTP or TCP health check endpoint

2. **No metrics collection**
   - No Prometheus metrics or similar
   - **Risk**: Cannot monitor performance or detect issues
   - **Fix Required**: Add metrics endpoint (request count, latency, errors)

3. **No distributed tracing**
   - No correlation IDs across service calls
   - **Fix Required**: Add OpenTelemetry or similar

4. **No alerting configuration**
   - No guidance on alert thresholds
   - **Fix Required**: Document recommended alerts (error rate, latency, availability)

5. **No readiness vs liveness distinction**
   - Health checks don't distinguish between startup and runtime health
   - **Fix Required**: Implement separate readiness and liveness probes

---

## 6. TypeScript Code Quality

### ✅ What Works Well

- **Strict TypeScript**: [`tsconfig.json`](mcps/regulatory_mcp/tsconfig.json:9) enables strict mode
- **Modern target**: ES2022 with NodeNext modules
- **Comprehensive compiler checks**: noUnusedLocals, noImplicitReturns, etc.
- **Type safety**: Proper type definitions in [`server.ts`](mcps/regulatory_mcp/src/server.ts:1-34)
- **Test configuration**: Vitest configured with coverage in [`vitest.config.ts`](mcps/regulatory_mcp/vitest.config.ts:1-16)

### ❌ Critical Gaps

1. **No test coverage requirements**
   - [`vitest.config.ts`](mcps/regulatory_mcp/vitest.config.ts:8-12) configures coverage but no thresholds
   - **Fix Required**: Add minimum coverage thresholds (80% lines, 70% branches)

2. **Tests not visible in analysis**
   - Only one test file mentioned: `registerResources.test.ts`
   - **Risk**: Insufficient test coverage
   - **Fix Required**: Add comprehensive unit and integration tests

3. **No type exports**
   - Public types not exported from package
   - **Fix Required**: Export key types for consumers

4. **No API documentation**
   - No JSDoc comments on public interfaces
   - **Fix Required**: Add comprehensive JSDoc comments

---

## 7. Documentation Completeness

### ✅ What Works Well

- **Comprehensive execution plan**: [`EXECUTION_PLAN.md`](mcps/EXECUTION_PLAN.md:1-561) covers setup, workflows, troubleshooting
- **Clear safety disclaimers**: Legal and compliance warnings prominent
- **Step-by-step guides**: Detailed setup instructions with expected outputs
- **Decision trees**: Visual guides for tool selection
- **Multiple documentation levels**: README for quick start, EXECUTION_PLAN for details

### ❌ Critical Gaps

1. **No disaster recovery procedures**
   - Backup mentioned but no restore procedure
   - No RTO/RPO definitions
   - **Fix Required**: Add complete DR runbook

2. **No scaling guidance**
   - No horizontal scaling strategy
   - No load testing results
   - **Fix Required**: Document scaling limits and strategies

3. **No production deployment guide**
   - All documentation assumes local development
   - **Fix Required**: Add production deployment checklist

4. **No incident response procedures**
   - No runbook for common failures
   - **Fix Required**: Add incident response playbook

5. **No SLA/SLO definitions**
   - No performance targets documented
   - **Fix Required**: Define availability, latency, and error rate targets

6. **No change management process**
   - No guidance on updating regulatory corpus
   - **Fix Required**: Document corpus update and validation process

---

## 8. Production Deployment Blockers

### 🚫 Must Fix Before Production

1. **Pin all Docker image versions** (HIGH PRIORITY)
   - Use SHA256 digests for reproducibility
   - Estimated effort: 2 hours

2. **Add resource limits to all containers** (HIGH PRIORITY)
   - Prevent resource exhaustion
   - Estimated effort: 1 hour

3. **Implement structured logging** (HIGH PRIORITY)
   - Enable production debugging
   - Estimated effort: 4 hours

4. **Add TLS/SSL configuration** (CRITICAL)
   - Encrypt all communications
   - Estimated effort: 8 hours

5. **Implement health checks for regulatory MCP** (HIGH PRIORITY)
   - Enable orchestration and monitoring
   - Estimated effort: 2 hours

6. **Add metrics and monitoring** (HIGH PRIORITY)
   - Enable observability
   - Estimated effort: 8 hours

7. **Create disaster recovery procedures** (MEDIUM PRIORITY)
   - Enable business continuity
   - Estimated effort: 4 hours

8. **Add comprehensive test suite** (HIGH PRIORITY)
   - Ensure reliability
   - Estimated effort: 16 hours

### ⚠️ Security Vulnerabilities

1. **Plaintext communication** - All HTTP, no TLS
2. **No rate limiting** - Vulnerable to DoS
3. **Floating Docker tags** - Supply chain risk
4. **No secrets rotation** - Long-lived credentials
5. **No input validation docs** - Potential injection risks

### 📋 Missing Operational Procedures

1. **Backup and restore procedures**
2. **Incident response runbook**
3. **Change management process**
4. **Capacity planning guide**
5. **Performance tuning guide**
6. **Security audit checklist**

### 🔧 Hardcoded Values to Externalize

1. **Port numbers** - Should be configurable
2. **Timeout values** - Should be tunable
3. **Retry counts** - Should be adjustable
4. **Health check intervals** - Should be environment-specific
5. **Log levels** - Should be runtime-configurable

---

## Recommendations Priority Matrix

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| P0 | Pin Docker images | 2h | High |
| P0 | Add TLS/SSL | 8h | Critical |
| P0 | Add resource limits | 1h | High |
| P1 | Structured logging | 4h | High |
| P1 | Health checks | 2h | High |
| P1 | Metrics/monitoring | 8h | High |
| P1 | Test coverage | 16h | High |
| P2 | DR procedures | 4h | Medium |
| P2 | Rate limiting | 4h | Medium |
| P2 | Secrets rotation | 6h | Medium |
| P3 | API documentation | 8h | Low |
| P3 | Performance tuning | 8h | Low |

**Total estimated effort to production-ready: ~71 hours (9 days)**

---

## Conclusion

The MCP infrastructure has a **solid architectural foundation** with good separation of concerns, comprehensive documentation, and thoughtful design. However, it requires **significant hardening** before production deployment.

**Key Strengths:**
- Clean architecture with proper separation
- Comprehensive documentation
- Good security awareness (secrets management)
- Proper health checks for dependencies

**Key Weaknesses:**
- Insufficient production hardening
- Missing observability infrastructure
- No disaster recovery procedures
- Floating dependency versions

**Recommendation:** Allocate 2 weeks for production hardening before any production deployment.

---

**User:**

[new_task in ❓ Ask mode: 'Conduct a focused production-readiness analysis of the MCP infrastructure documentation and implementation. Specifically analyze:

1. **MCP Infrastructure Files:**
   - mcps/docker-compose.yml
   - mcps/regulatory_mcp/package.json
   - mcps/regulatory_mcp/Dockerfile
   - mcps/regulatory_mcp/src/index.ts
   - mcps/regulatory_mcp/src/server.ts

2. **Production Readiness Assessment:**
   - Are all dependencies properly versioned and locked?
   - Is error handling comprehensive?
   - Are security configurations production-grade?
   - Is the Docker configuration optimized for production?
   - Are there health checks and monitoring?
   - Is the TypeScript code properly typed and tested?

3. **Documentation Completeness:**
   - Does EXECUTION_PLAN.md cover all production scenarios?
   - Are there gaps in operational procedures?
   - Is disaster recovery documented?
   - Are scaling considerations addressed?

4. **What's Missing for Production:**
   - List specific gaps that would prevent production deployment
   - Identify security vulnerabilities or concerns
   - Note missing operational procedures
   - Highlight any hardcoded values or secrets

Provide a concise, actionable report focused on production readiness, not general criticism. Focus on what works well and what specific items need to be added for production use.'] Result:
Successfully created new task in ❓ Ask mode with message: Conduct a focused production-readiness analysis of the MCP infrastructure documentation and implementation. Specifically analyze:

1. **MCP Infrastructure Files:**
   - mcps/docker-compose.yml
   - mcps/regulatory_mcp/package.json
   - mcps/regulatory_mcp/Dockerfile
   - mcps/regulatory_mcp/src/index.ts
   - mcps/regulatory_mcp/src/server.ts

2. **Production Readiness Assessment:**
   - Are all dependencies properly versioned and locked?
   - Is error handling comprehensive?
   - Are security configurations production-grade?
   - Is the Docker configuration optimized for production?
   - Are there health checks and monitoring?
   - Is the TypeScript code properly typed and tested?

3. **Documentation Completeness:**
   - Does EXECUTION_PLAN.md cover all production scenarios?
   - Are there gaps in operational procedures?
   - Is disaster recovery documented?
   - Are scaling considerations addressed?

4. **What's Missing for Production:**
   - List specific gaps that would prevent production deployment
   - Identify security vulnerabilities or concerns
   - Note missing operational procedures
   - Highlight any hardcoded values or secrets

Provide a concise, actionable report focused on production readiness, not general criticism. Focus on what works well and what specific items need to be added for production use. and 0 todo items
[new_task in ❓ Ask mode: 'Conduct a focused production-readiness analysis of the MCP infrastructure documentation and implementation. Specifically analyze:

1. **MCP Infrastructure Files:**
   - mcps/docker-compose.yml
   - mcps/regulatory_mcp/package.json
   - mcps/regulatory_mcp/Dockerfile
   - mcps/regulatory_mcp/src/index.ts
   - mcps/regulatory_mcp/src/server.ts

2. **Production Readiness Assessment:**
   - Are all dependencies properly versioned and locked?
   - Is error handling comprehensive?
   - Are security configurations production-grade?
   - Is the Docker configuration optimized for production?
   - Are there health checks and monitoring?
   - Is the TypeScript code properly typed and tested?

3. **Documentation Completeness:**
   - Does EXECUTION_PLAN.md cover all production scenarios?
   - Are there gaps in operational procedures?
   - Is disaster recovery documented?
   - Are scaling considerations addressed?

4. **What's Missing for Production:**
   - List specific gaps that would prevent production deployment
   - Identify security vulnerabilities or concerns
   - Note missing operational procedures
   - Highlight any hardcoded values or secrets

Provide a concise, actionable report focused on production readiness, not general criticism. Focus on what works well and what specific items need to be added for production use.'] Result:
Successfully created new task in ❓ Ask mode with message: Conduct a focused production-readiness analysis of the MCP infrastructure documentation and implementation. Specifically analyze:

1. **MCP Infrastructure Files:**
   - mcps/docker-compose.yml
   - mcps/regulatory_mcp/package.json
   - mcps/regulatory_mcp/Dockerfile
   - mcps/regulatory_mcp/src/index.ts
   - mcps/regulatory_mcp/src/server.ts

2. **Production Readiness Assessment:**
   - Are all dependencies properly versioned and locked?
   - Is error handling comprehensive?
   - Are security configurations production-grade?
   - Is the Docker configuration optimized for production?
   - Are there health checks and monitoring?
   - Is the TypeScript code properly typed and tested?

3. **Documentation Completeness:**
   - Does EXECUTION_PLAN.md cover all production scenarios?
   - Are there gaps in operational procedures?
   - Is disaster recovery documented?
   - Are scaling considerations addressed?

4. **What's Missing for Production:**
   - List specific gaps that would prevent production deployment
   - Identify security vulnerabilities or concerns
   - Note missing operational procedures
   - Highlight any hardcoded values or secrets

Provide a concise, actionable report focused on production readiness, not general criticism. Focus on what works well and what specific items need to be added for production use. and 0 todo items
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:03:37.070Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.27

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# MCP Infrastructure Production Readiness Analysis

## Executive Summary

The MCP infrastructure demonstrates **strong foundational architecture** with good separation of concerns and comprehensive documentation. However, several **critical production gaps** exist that must be addressed before deployment. The infrastructure is currently **development-ready but not production-ready**.

**Overall Assessment:** 🟡 **60% Production Ready** - Solid foundation, needs hardening

---

## 1. Dependency Management & Versioning

### ✅ What Works Well

- **Locked dependencies**: `package-lock.json` exists with lockfileVersion 3
- **Engine constraints**: Node.js >=20.0.0 specified in `package.json`
- **Minimal dependency surface**: Only 2 runtime dependencies (@modelcontextprotocol/sdk, zod)
- **Docker multi-stage builds**: Proper separation of build and runtime stages in `Dockerfile`

### ❌ Critical Gaps

1. **Unversioned Docker base images**
   - `Dockerfile` uses `node:20-alpine` (floating tag)
   - **Risk**: Breaking changes in Node.js 20.x updates
   - **Fix Required**: Pin to specific digest or patch version (e.g., `node:20.18.1-alpine`)

2. **Unversioned third-party images in docker-compose**
   - Uses `postgres:16-alpine` (floating)
   - Uses `sonarqube:community` (latest)
   - Uses `ghcr.io/zaproxy/zaproxy:stable` (floating)
   - **Risk**: Unpredictable behavior across environments
   - **Fix Required**: Pin all images to specific versions with SHA256 digests

3. **No dependency vulnerability scanning**
   - No automated checks for npm package vulnerabilities
   - **Fix Required**: Add `npm audit` to CI/CD pipeline

---

## 2. Error Handling & Resilience

### ✅ What Works Well

- **Top-level error handler**: `index.ts` catches fatal errors
- **Health checks**: Comprehensive health checks for SonarQube and ZAP in `docker-compose.yml`
- **Retry logic**: SonarQube init has 60-attempt retry loop with 5s intervals
- **Graceful degradation**: Services use `depends_on` with health conditions

### ❌ Critical Gaps

1. **No error recovery in MCP server**
   - `server.ts` has no try-catch around tool registration
   - **Risk**: Single tool registration failure crashes entire server
   - **Fix Required**: Wrap each registration in try-catch, log errors, continue

2. **No timeout configuration**
   - MCP server has no request timeout limits
   - **Risk**: Hung requests can exhaust resources
   - **Fix Required**: Add configurable timeouts (default 30s)

3. **No circuit breaker pattern**
   - No protection against cascading failures
   - **Fix Required**: Implement circuit breakers for external service calls

4. **Insufficient logging**
   - Only startup logs in `index.ts`
   - No structured logging (JSON format)
   - No log levels (debug, info, warn, error)
   - **Fix Required**: Add structured logging library (e.g., pino)

---

## 3. Security Configuration

### ✅ What Works Well

- **Secret management**: Secrets in `.env` file, not committed (`.env.example` provided)
- **Required secrets validation**: `docker-compose.yml` uses `?` syntax to enforce secrets
- **Least privilege**: Docker containers run as non-root where possible
- **Network isolation**: Services use internal Docker networks
- **API key authentication**: ZAP requires API key and MCP security key

### ❌ Critical Gaps

1. **Hardcoded localhost bindings**
   - `docker-compose.yml` binds to `127.0.0.1` (good for dev, bad for production)
   - **Risk**: Cannot access from other containers in production
   - **Fix Required**: Make bind address configurable via environment variable

2. **No secrets rotation mechanism**
   - Manual rotation process documented but not automated
   - **Fix Required**: Add automated secret rotation with grace periods

3. **No TLS/SSL configuration**
   - All services communicate over HTTP
   - **Risk**: Credentials and data transmitted in plaintext
   - **Fix Required**: Add TLS termination for production deployments

4. **Weak password requirements**
   - No validation of password strength in `.env.example`
   - **Fix Required**: Document minimum password requirements (length, complexity)

5. **No rate limiting**
   - MCP server has no request rate limits
   - **Risk**: DoS attacks or resource exhaustion
   - **Fix Required**: Add rate limiting middleware

6. **No input validation documentation**
   - Tool schemas exist but validation approach unclear
   - **Fix Required**: Document input sanitization strategy

---

## 4. Docker Configuration Optimization

### ✅ What Works Well

- **Multi-stage builds**: Separates build and runtime in `Dockerfile`
- **Cache optimization**: `npm ci` before copying source code
- **Minimal runtime**: Uses Alpine Linux base
- **Cache cleanup**: `npm cache clean --force` in production stage
- **Health checks**: Comprehensive health check definitions

### ❌ Critical Gaps

1. **No resource limits**
   - No CPU or memory limits defined
   - **Risk**: Container can consume all host resources
   - **Fix Required**: Add resource limits to all services:
   ```yaml
   deploy:
     resources:
       limits:
         cpus: '1.0'
         memory: 512M
       reservations:
         cpus: '0.5'
         memory: 256M
   ```

2. **No restart policies**
   - Services don't auto-restart on failure
   - **Fix Required**: Add `restart: unless-stopped` to production services

3. **No security options**
   - Missing security hardening (read-only root filesystem, no new privileges)
   - **Fix Required**: Add security options:
   ```yaml
   security_opt:
     - no-new-privileges:true
   read_only: true
   ```

4. **Volume permissions not documented**
   - No guidance on volume ownership/permissions
   - **Fix Required**: Document required volume permissions

---

## 5. Health Checks & Monitoring

### ✅ What Works Well

- **Comprehensive health checks**: SonarQube, ZAP, and Postgres all have health checks
- **Appropriate intervals**: 10-15s intervals with reasonable retries
- **Start periods**: Services have grace periods for initialization
- **Health check tool**: `health_check` MCP tool for connectivity verification

### ❌ Critical Gaps

1. **No health check for regulatory MCP**
   - `docker-compose.yml` has no health check for main service
   - **Fix Required**: Add HTTP or TCP health check endpoint

2. **No metrics collection**
   - No Prometheus metrics or similar
   - **Risk**: Cannot monitor performance or detect issues
   - **Fix Required**: Add metrics endpoint (request count, latency, errors)

3. **No distributed tracing**
   - No correlation IDs across service calls
   - **Fix Required**: Add OpenTelemetry or similar

4. **No alerting configuration**
   - No guidance on alert thresholds
   - **Fix Required**: Document recommended alerts (error rate, latency, availability)

5. **No readiness vs liveness distinction**
   - Health checks don't distinguish between startup and runtime health
   - **Fix Required**: Implement separate readiness and liveness probes

---

## 6. TypeScript Code Quality

### ✅ What Works Well

- **Strict TypeScript**: `tsconfig.json` enables strict mode
- **Modern target**: ES2022 with NodeNext modules
- **Comprehensive compiler checks**: noUnusedLocals, noImplicitReturns, etc.
- **Type safety**: Proper type definitions in `server.ts`
- **Test configuration**: Vitest configured with coverage in `vitest.config.ts`

### ❌ Critical Gaps

1. **No test coverage requirements**
   - `vitest.config.ts` configures coverage but no thresholds
   - **Fix Required**: Add minimum coverage thresholds (80% lines, 70% branches)

2. **Tests not comprehensive**
   - Limited test files visible
   - **Risk**: Insufficient test coverage
   - **Fix Required**: Add comprehensive unit and integration tests

3. **No type exports**
   - Public types not exported from package
   - **Fix Required**: Export key types for consumers

4. **No API documentation**
   - No JSDoc comments on public interfaces
   - **Fix Required**: Add comprehensive JSDoc comments

---

## 7. Documentation Completeness

### ✅ What Works Well

- **Comprehensive execution plan**: `EXECUTION_PLAN.md` covers setup, workflows, troubleshooting
- **Clear safety disclaimers**: Legal and compliance warnings prominent
- **Step-by-step guides**: Detailed setup instructions with expected outputs
- **Decision trees**: Visual guides for tool selection
- **Multiple documentation levels**: README for quick start, EXECUTION_PLAN for details

### ❌ Critical Gaps

1. **No disaster recovery procedures**
   - Backup mentioned but no restore procedure
   - No RTO/RPO definitions
   - **Fix Required**: Add complete DR runbook

2. **No scaling guidance**
   - No horizontal scaling strategy
   - No load testing results
   - **Fix Required**: Document scaling limits and strategies

3. **No production deployment guide**
   - All documentation assumes local development
   - **Fix Required**: Add production deployment checklist

4. **No incident response procedures**
   - No runbook for common failures
   - **Fix Required**: Add incident response playbook

5. **No SLA/SLO definitions**
   - No performance targets documented
   - **Fix Required**: Define availability, latency, and error rate targets

6. **No change management process**
   - No guidance on updating regulatory corpus
   - **Fix Required**: Document corpus update and validation process

---

## 8. Production Deployment Blockers

### 🚫 Must Fix Before Production

1. **Pin all Docker image versions** (HIGH PRIORITY)
   - Use SHA256 digests for reproducibility
   - Estimated effort: 2 hours

2. **Add resource limits to all containers** (HIGH PRIORITY)
   - Prevent resource exhaustion
   - Estimated effort: 1 hour

3. **Implement structured logging** (HIGH PRIORITY)
   - Enable production debugging
   - Estimated effort: 4 hours

4. **Add TLS/SSL configuration** (CRITICAL)
   - Encrypt all communications
   - Estimated effort: 8 hours

5. **Implement health checks for regulatory MCP** (HIGH PRIORITY)
   - Enable orchestration and monitoring
   - Estimated effort: 2 hours

6. **Add metrics and monitoring** (HIGH PRIORITY)
   - Enable observability
   - Estimated effort: 8 hours

7. **Create disaster recovery procedures** (MEDIUM PRIORITY)
   - Enable business continuity
   - Estimated effort: 4 hours

8. **Add comprehensive test suite** (HIGH PRIORITY)
   - Ensure reliability
   - Estimated effort: 16 hours

### ⚠️ Security Vulnerabilities

1. **Plaintext communication** - All HTTP, no TLS
2. **No rate limiting** - Vulnerable to DoS
3. **Floating Docker tags** - Supply chain risk
4. **No secrets rotation** - Long-lived credentials
5. **No input validation docs** - Potential injection risks

### 📋 Missing Operational Procedures

1. **Backup and restore procedures**
2. **Incident response runbook**
3. **Change management process**
4. **Capacity planning guide**
5. **Performance tuning guide**
6. **Security audit checklist**

### 🔧 Hardcoded Values to Externalize

1. **Port numbers** - Should be configurable
2. **Timeout values** - Should be tunable
3. **Retry counts** - Should be adjustable
4. **Health check intervals** - Should be environment-specific
5. **Log levels** - Should be runtime-configurable

---

## Recommendations Priority Matrix

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| P0 | Pin Docker images | 2h | High |
| P0 | Add TLS/SSL | 8h | Critical |
| P0 | Add resource limits | 1h | High |
| P1 | Structured logging | 4h | High |
| P1 | Health checks | 2h | High |
| P1 | Metrics/monitoring | 8h | High |
| P1 | Test coverage | 16h | High |
| P2 | DR procedures | 4h | Medium |
| P2 | Rate limiting | 4h | Medium |
| P2 | Secrets rotation | 6h | Medium |
| P3 | API documentation | 8h | Low |
| P3 | Performance tuning | 8h | Low |

**Total estimated effort to production-ready: ~71 hours (9 days)**

---

## Conclusion

The MCP infrastructure has a **solid architectural foundation** with good separation of concerns, comprehensive documentation, and thoughtful design. However, it requires **significant hardening** before production deployment.

**Key Strengths:**
- Clean architecture with proper separation
- Comprehensive documentation
- Good security awareness (secrets management)
- Proper health checks for dependencies

**Key Weaknesses:**
- Insufficient production hardening
- Missing observability infrastructure
- No disaster recovery procedures
- Floating dependency versions

**Recommendation:** Allocate 2 weeks for production hardening before any production deployment.
</result>
</attempt_completion>

---

**User:**

[attempt_completion] Result:
The user has provided feedback on the results. Consider their input to continue the task, and then attempt completion again.
<feedback>
try to add OWASP MCP server
</feedback>
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:07:03.162Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.48

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I understand you want me to analyze the OWASP ZAP MCP server as part of the production readiness assessment. Let me delegate this to Ask mode to examine the ZAP MCP configuration and implementation.

<new_task>
<mode>ask</mode>
<message>Expand the MCP infrastructure production readiness analysis to include the OWASP ZAP MCP server. Analyze:

1. **OWASP ZAP MCP Configuration:**
   - How is ZAP MCP configured in mcps/docker-compose.yml?
   - What is the ZAP MCP Integration add-on setup?
   - How does it integrate with the regulatory MCP?

2. **ZAP MCP Production Readiness:**
   - Is the ZAP daemon properly configured for production?
   - Are security controls (API keys, authentication) adequate?
   - Is the MCP add-on version pinned?
   - Are there health checks for ZAP?
   - What are the security implications of running ZAP in production?

3. **ZAP MCP Operational Concerns:**
   - How are scans triggered and controlled?
   - Is there protection against unauthorized scans?
   - Are scan results properly secured?
   - What's the resource impact of running ZAP?

4. **Integration with Bob:**
   - How does Bob interact with ZAP MCP?
   - What tools are exposed?
   - Are there rate limits or scan quotas?

5. **Production Gaps for ZAP MCP:**
   - What specific issues prevent production deployment?
   - Security vulnerabilities in the ZAP setup?
   - Missing operational procedures?
   - Configuration hardening needed?

Provide a focused analysis on OWASP ZAP MCP production readiness, highlighting what works well and what critical gaps exist. Include specific recommendations with effort estimates.</message>
</new_task>

---

**User:**

[new_task completed] Result: # OWASP ZAP MCP Production Readiness Analysis

I've completed a comprehensive analysis of the OWASP ZAP MCP server's production readiness. Here are the key findings:

## 1. OWASP ZAP MCP Configuration

**Current Setup:**
- **Image:** `ghcr.io/zaproxy/zaproxy:stable` (unpinned)
- **Network:** Host mode, localhost-only binding (`127.0.0.1`)
- **Ports:** ZAP API on 8090, MCP endpoint on 8282
- **Authentication:** Dual-layer (ZAP API key + MCP security key)
- **MCP Add-on:** Installed dynamically without version pinning
- **Integration:** Standalone service accessed by Bob via [`mcp-remote`](.bob/mcp.example.json:36-51)

**Key Configuration Issues:**
- MCP add-on version not pinned (line 282 in [`docker-compose.yml`](mcps/docker-compose.yml:282))
- HTTP-only communication (`mcp.secureOnly=false` at line 299)
- No resource limits defined
- Base image uses `stable` tag instead of specific version

## 2. ZAP MCP Production Readiness: ❌ NOT READY

### ✅ What Works Well

1. **Localhost-Only Binding** - Good security posture for development
2. **Dual Authentication** - Separate keys for API and MCP
3. **Robust Health Checks** - 5-minute startup tolerance with API validation
4. **Persistent Storage** - Scan results and configs survive restarts
5. **Manual Scan Control** - No automated background scanning

### ❌ Critical Blockers (12 hours to fix)

| Issue | Severity | Impact | Effort |
|-------|----------|--------|--------|
| Unpinned MCP add-on version | HIGH | Non-deterministic builds, security risk | 2h |
| Unpinned base image (`stable` tag) | HIGH | Breaking changes without warning | 1h |
| No resource limits | HIGH | Can exhaust host resources | 1h |
| HTTP-only MCP communication | MEDIUM-HIGH | Security key transmitted in plaintext | 8h |

### ⚠️ Major Production Gaps (48 hours to fix)

1. **No Scan Authorization Controls** (16h)
   - Any authenticated user can scan any target
   - No approval workflow for sensitive targets
   - Risk of accidental production scans

2. **No Scan Result Security** (12h)
   - Results stored unencrypted in Docker volume
   - No access controls or audit trail
   - Potential compliance violations

3. **No Rate Limiting/Quotas** (12h)
   - Unlimited scans per user
   - No protection against resource exhaustion
   - No scan queue management

4. **Missing Operational Procedures** (8h)
   - No incident response plan
   - No scan result triage process
   - No documented escalation paths

## 3. ZAP MCP Operational Concerns

**Scan Triggering:**
- Currently: Manual via Bob MCP interface
- Missing: Rate limits, scan queues, timeout enforcement
- Risk: Resource exhaustion, unauthorized scans

**Scan Result Protection:**
- Currently: Stored in Docker volume without encryption
- Missing: Access controls, audit logging, automatic cleanup
- Risk: Sensitive vulnerability data exposure

**Resource Impact:**
- CPU: 50-200% during active scans
- Memory: 1-4GB depending on target
- Recommendation: Dedicated host or strict resource limits

## 4. Integration with Bob

**Current Setup:**
- Bob starts [`owasp-zap-mcp`](mcps/docker-compose.yml:314-343) via Docker Compose
- Uses `mcp-remote` to connect to `http://127.0.0.1:8282`
- Authentication via `Authorization` header with `ZAP_MCP_SECURITY_KEY`

**Exposed Tools:**
- Spider, AJAX spider, active/passive scanning
- Alert retrieval, report generation

**Missing:**
- ❌ No rate limits or scan quotas
- ❌ No per-user tracking
- ❌ No scan duration limits

## 5. Security Implications of Running ZAP in Production

### ⚠️ Critical Security Considerations

1. **ZAP is an Attack Tool** - Designed to exploit vulnerabilities, can cause DoS
2. **Localhost-Only ≠ Production-Safe** - Multi-tenant environments need stronger isolation
3. **Scan Results = Sensitive Data** - Contains vulnerability details, must be protected
4. **No Audit Trail** - Cannot track who scanned what, when, or why

## 6. Specific Recommendations

### Phase 1: Blockers (12 hours)
1. Pin ZAP image to specific version (1h)
2. Pin MCP add-on version (2h)
3. Add resource limits (1h)
4. Enable HTTPS for MCP (8h)

### Phase 2: Critical Gaps (48 hours)
5. Implement scan authorization controls (16h)
6. Secure scan results with encryption (12h)
7. Add rate limiting and quotas (12h)
8. Create operational runbook (8h)

### Phase 3: Production Hardening (56 hours)
9. Implement scan queue management (20h)
10. Add comprehensive audit logging (8h)
11. Setup monitoring and alerting (16h)
12. Additional result encryption (12h)

**Total Effort for Production:** 116 hours (~3 weeks)

## 7. Production Deployment Decision

### ❌ **NOT PRODUCTION READY**

**Verdict:** Current setup is **suitable for local development only**. Critical gaps prevent production deployment.

### Recommended Path Forward

**Option A: Keep as Development Tool (Recommended)**
- Fix blockers only (12 hours)
- Document as local-only tool
- Use managed DAST service for production (e.g., OWASP ZAP Cloud, Burp Suite Enterprise)

**Option B: Full Production Deployment**
- Complete all phases (116 hours)
- Requires dedicated security review
- Ongoing operational overhead
- Evaluate if value justifies cost vs. managed alternatives

### Immediate Action Items (10 hours)
1. Pin ZAP image and MCP add-on versions (3h)
2. Add resource limits (1h)
3. Document as development-only tool (2h)
4. Evaluate managed DAST alternatives (4h)

## Conclusion

The OWASP ZAP MCP provides valuable security scanning for local development but requires **116 hours of hardening** for production use. The **12-hour blocker fixes** are recommended to stabilize the development environment, while production scanning should leverage managed DAST services to avoid the operational burden and security risks of self-hosting an attack tool.

---

**User:**

[new_task in ❓ Ask mode: 'Expand the MCP infrastructure production readiness analysis to include the OWASP ZAP MCP server. Analyze:

1. **OWASP ZAP MCP Configuration:**
   - How is ZAP MCP configured in mcps/docker-compose.yml?
   - What is the ZAP MCP Integration add-on setup?
   - How does it integrate with the regulatory MCP?

2. **ZAP MCP Production Readiness:**
   - Is the ZAP daemon properly configured for production?
   - Are security controls (API keys, authentication) adequate?
   - Is the MCP add-on version pinned?
   - Are there health checks for ZAP?
   - What are the security implications of running ZAP in production?

3. **ZAP MCP Operational Concerns:**
   - How are scans triggered and controlled?
   - Is there protection against unauthorized scans?
   - Are scan results properly secured?
   - What's the resource impact of running ZAP?

4. **Integration with Bob:**
   - How does Bob interact with ZAP MCP?
   - What tools are exposed?
   - Are there rate limits or scan quotas?

5. **Production Gaps for ZAP MCP:**
   - What specific issues prevent production deployment?
   - Security vulnerabilities in the ZAP setup?
   - Missing operational procedures?
   - Configuration hardening needed?

Provide a focused analysis on OWASP ZAP MCP production readiness, highlighting what works well and what critical gaps exist. Include specific recommendations with effort estimates.'] Result:
Successfully created new task in ❓ Ask mode with message: Expand the MCP infrastructure production readiness analysis to include the OWASP ZAP MCP server. Analyze:

1. **OWASP ZAP MCP Configuration:**
   - How is ZAP MCP configured in mcps/docker-compose.yml?
   - What is the ZAP MCP Integration add-on setup?
   - How does it integrate with the regulatory MCP?

2. **ZAP MCP Production Readiness:**
   - Is the ZAP daemon properly configured for production?
   - Are security controls (API keys, authentication) adequate?
   - Is the MCP add-on version pinned?
   - Are there health checks for ZAP?
   - What are the security implications of running ZAP in production?

3. **ZAP MCP Operational Concerns:**
   - How are scans triggered and controlled?
   - Is there protection against unauthorized scans?
   - Are scan results properly secured?
   - What's the resource impact of running ZAP?

4. **Integration with Bob:**
   - How does Bob interact with ZAP MCP?
   - What tools are exposed?
   - Are there rate limits or scan quotas?

5. **Production Gaps for ZAP MCP:**
   - What specific issues prevent production deployment?
   - Security vulnerabilities in the ZAP setup?
   - Missing operational procedures?
   - Configuration hardening needed?

Provide a focused analysis on OWASP ZAP MCP production readiness, highlighting what works well and what critical gaps exist. Include specific recommendations with effort estimates. and 0 todo items
[new_task in ❓ Ask mode: 'Expand the MCP infrastructure production readiness analysis to include the OWASP ZAP MCP server. Analyze:

1. **OWASP ZAP MCP Configuration:**
   - How is ZAP MCP configured in mcps/docker-compose.yml?
   - What is the ZAP MCP Integration add-on setup?
   - How does it integrate with the regulatory MCP?

2. **ZAP MCP Production Readiness:**
   - Is the ZAP daemon properly configured for production?
   - Are security controls (API keys, authentication) adequate?
   - Is the MCP add-on version pinned?
   - Are there health checks for ZAP?
   - What are the security implications of running ZAP in production?

3. **ZAP MCP Operational Concerns:**
   - How are scans triggered and controlled?
   - Is there protection against unauthorized scans?
   - Are scan results properly secured?
   - What's the resource impact of running ZAP?

4. **Integration with Bob:**
   - How does Bob interact with ZAP MCP?
   - What tools are exposed?
   - Are there rate limits or scan quotas?

5. **Production Gaps for ZAP MCP:**
   - What specific issues prevent production deployment?
   - Security vulnerabilities in the ZAP setup?
   - Missing operational procedures?
   - Configuration hardening needed?

Provide a focused analysis on OWASP ZAP MCP production readiness, highlighting what works well and what critical gaps exist. Include specific recommendations with effort estimates.'] Result:
Successfully created new task in ❓ Ask mode with message: Expand the MCP infrastructure production readiness analysis to include the OWASP ZAP MCP server. Analyze:

1. **OWASP ZAP MCP Configuration:**
   - How is ZAP MCP configured in mcps/docker-compose.yml?
   - What is the ZAP MCP Integration add-on setup?
   - How does it integrate with the regulatory MCP?

2. **ZAP MCP Production Readiness:**
   - Is the ZAP daemon properly configured for production?
   - Are security controls (API keys, authentication) adequate?
   - Is the MCP add-on version pinned?
   - Are there health checks for ZAP?
   - What are the security implications of running ZAP in production?

3. **ZAP MCP Operational Concerns:**
   - How are scans triggered and controlled?
   - Is there protection against unauthorized scans?
   - Are scan results properly secured?
   - What's the resource impact of running ZAP?

4. **Integration with Bob:**
   - How does Bob interact with ZAP MCP?
   - What tools are exposed?
   - Are there rate limits or scan quotas?

5. **Production Gaps for ZAP MCP:**
   - What specific issues prevent production deployment?
   - Security vulnerabilities in the ZAP setup?
   - Missing operational procedures?
   - Configuration hardening needed?

Provide a focused analysis on OWASP ZAP MCP production readiness, highlighting what works well and what critical gaps exist. Include specific recommendations with effort estimates. and 0 todo items
<environment_details>
# VSCode Visible Files


# VSCode Open Tabs
docs/PERFORMANCE_OPTIMIZATION_PLAN.md,docs/PERFORMANCE_IMPLEMENTATION_GUIDE.md,docs/PERFORMANCE_OPTIMIZATION_SUMMARY.md,bob_sessions/bob_task_may-17-2026_2-31-18-pm.md,mcps/EXECUTION_PLAN.md,mcps/README.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-17T14:09:08.519Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.69

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>orchestrator</slug>
<name>🔀 Orchestrator</name>
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
# Complete MCP Infrastructure Production Readiness Analysis
## Including OWASP ZAP MCP Server

---

## Executive Summary

The MCP infrastructure consists of **three main services**: Regulatory Controls MCP, SonarQube MCP, and OWASP ZAP MCP. While the architecture is well-designed for development, **none of the services are production-ready** without significant hardening.

**Overall Production Readiness:**
- **Regulatory MCP:** 🟡 60% Ready (9 days to production)
- **SonarQube MCP:** 🟡 65% Ready (6 days to production)
- **OWASP ZAP MCP:** 🔴 30% Ready (15 days to production)

**Combined Assessment:** 🟡 **52% Production Ready** - Requires 4-6 weeks of hardening

---

## Part 1: Regulatory & SonarQube MCP Analysis

*(See previous analysis for detailed findings)*

**Key Gaps:**
- Unpinned Docker images
- No resource limits
- Missing TLS/SSL
- Insufficient logging and monitoring
- No disaster recovery procedures

**Estimated Effort:** 71 hours (9 days)

---

## Part 2: OWASP ZAP MCP Deep Dive

### 1. OWASP ZAP MCP Configuration

**Current Setup:**
- **Image:** `ghcr.io/zaproxy/zaproxy:stable` (unpinned floating tag)
- **Network:** Host mode with localhost-only binding (`127.0.0.1:8090`, `127.0.0.1:8282`)
- **Ports:** 
  - 8090: ZAP API endpoint
  - 8282: MCP Integration add-on endpoint
- **Authentication:** Dual-layer security
  - `ZAP_API_KEY` for ZAP daemon access
  - `ZAP_MCP_SECURITY_KEY` for MCP endpoint access
- **MCP Add-on:** Installed dynamically without version pinning
- **Integration:** Standalone service accessed by Bob via `mcp-remote`

**Configuration Issues:**
- MCP add-on version not pinned (dynamic installation)
- HTTP-only communication (`mcp.secureOnly=false`)
- No resource limits defined
- Base image uses `stable` tag instead of specific version
- Target URL configurable but defaults to frontend dev server

### 2. ZAP MCP Production Readiness: ❌ NOT READY

#### ✅ What Works Well

1. **Localhost-Only Binding**
   - Good security posture for development
   - Prevents external access by default
   - Suitable for single-developer workstations

2. **Dual Authentication**
   - Separate keys for API and MCP layers
   - Defense in depth approach
   - Keys stored in `.env` (not committed)

3. **Robust Health Checks**
   - 5-minute startup tolerance
   - API validation via `/JSON/core/view/version/`
   - Proper retry logic (30 attempts, 10s intervals)

4. **Persistent Storage**
   - Scan results survive container restarts
   - Configuration persists in Docker volume
   - Session management maintained

5. **Manual Scan Control**
   - No automated background scanning
   - Developer-initiated scans only
   - Reduces accidental production scans

#### ❌ Critical Production Blockers (12 hours to fix)

| Issue | Severity | Impact | Effort | Fix |
|-------|----------|--------|--------|-----|
| Unpinned MCP add-on version | HIGH | Non-deterministic builds, security risk | 2h | Pin to specific version in install command |
| Unpinned base image (`stable` tag) | HIGH | Breaking changes without warning | 1h | Use `ghcr.io/zaproxy/zaproxy:2.14.0@sha256:...` |
| No resource limits | HIGH | Can exhaust host resources during scans | 1h | Add CPU/memory limits |
| HTTP-only MCP communication | MEDIUM-HIGH | Security key transmitted in plaintext | 8h | Enable HTTPS with self-signed cert |

#### ⚠️ Major Production Gaps (48 hours to fix)

1. **No Scan Authorization Controls** (16 hours)
   - **Issue:** Any authenticated user can scan any target
   - **Risk:** Accidental production scans, unauthorized testing
   - **Missing:** 
     - Approval workflow for sensitive targets
     - Target whitelist/blacklist
     - Scan request validation
   - **Fix:** Implement pre-scan authorization service

2. **No Scan Result Security** (12 hours)
   - **Issue:** Results stored unencrypted in Docker volume
   - **Risk:** Sensitive vulnerability data exposure
   - **Missing:**
     - Encryption at rest
     - Access controls on results
     - Audit trail of result access
     - Automatic result expiration
   - **Fix:** Implement encrypted storage with access controls

3. **No Rate Limiting/Quotas** (12 hours)
   - **Issue:** Unlimited scans per user
   - **Risk:** Resource exhaustion, DoS
   - **Missing:**
     - Per-user scan quotas
     - Concurrent scan limits
     - Scan queue management
     - Timeout enforcement
   - **Fix:** Add rate limiting middleware

4. **Missing Operational Procedures** (8 hours)
   - **Issue:** No documented incident response
   - **Risk:** Delayed response to security incidents
   - **Missing:**
     - Scan result triage process
     - False positive handling
     - Escalation procedures
     - Compliance reporting
   - **Fix:** Create operational runbook

### 3. ZAP MCP Operational Concerns

#### Scan Triggering & Control

**Current State:**
- Manual triggering via Bob MCP interface
- No scan scheduling or automation
- No scan templates or profiles

**Missing Controls:**
- ❌ Rate limits (scans per hour/day)
- ❌ Scan queues (concurrent scan management)
- ❌ Timeout enforcement (max scan duration)
- ❌ Resource quotas (CPU/memory per scan)
- ❌ Scan approval workflow

**Risk Assessment:**
- **Resource Exhaustion:** High - Aggressive scans can consume 200% CPU
- **Unauthorized Scans:** Medium - Authentication exists but no authorization
- **Accidental Production Scans:** High - No target validation

#### Scan Result Protection

**Current State:**
- Results stored in Docker volume `zap_data`
- No encryption at rest
- No access controls beyond container isolation
- No automatic cleanup

**Security Gaps:**
- ❌ Unencrypted vulnerability data
- ❌ No audit trail of result access
- ❌ No result retention policy
- ❌ No compliance controls (GDPR, SOC2)

**Compliance Risk:** HIGH - Vulnerability data may contain PII or sensitive business information

#### Resource Impact

**Observed Resource Usage:**
- **CPU:** 50-200% during active scans (depends on target complexity)
- **Memory:** 1-4GB (depends on spider depth and target size)
- **Network:** 10-100 Mbps (depends on scan aggressiveness)
- **Disk:** 100MB-1GB per scan session

**Recommendations:**
- Dedicated host or strict resource limits
- Scan scheduling during off-peak hours
- Resource monitoring and alerting

### 4. Integration with Bob

**Current Architecture:**
- Bob starts `owasp-zap-mcp` service via Docker Compose
- Uses `mcp-remote` to connect to `http://127.0.0.1:8282`
- Authentication via `Authorization` header with `ZAP_MCP_SECURITY_KEY`

**Exposed Tools:**
- Spider (traditional and AJAX)
- Active scanning
- Passive scanning
- Alert retrieval
- Report generation

**Integration Gaps:**
- ❌ No rate limits or scan quotas
- ❌ No per-user tracking or attribution
- ❌ No scan duration limits
- ❌ No scan result filtering (all alerts returned)
- ❌ No scan status monitoring

**Bob Configuration Issues:**
- MCP endpoint URL hardcoded in `.bob/mcp.json`
- No fallback if ZAP service unavailable
- No timeout configuration for long-running scans

### 5. Security Implications of Running ZAP in Production

#### ⚠️ Critical Security Considerations

1. **ZAP is an Attack Tool**
   - Designed to exploit vulnerabilities
   - Can cause denial of service
   - May trigger security alerts/IDS
   - Legal implications if misused

2. **Localhost-Only ≠ Production-Safe**
   - Multi-tenant environments need stronger isolation
   - Container escape could expose ZAP to network
   - Shared Docker daemon is a risk

3. **Scan Results = Sensitive Data**
   - Contains detailed vulnerability information
   - May include credentials or PII
   - Must be protected under compliance frameworks
   - Retention policies required

4. **No Audit Trail**
   - Cannot track who scanned what
   - No evidence for compliance audits
   - Difficult to investigate incidents

#### Security Hardening Requirements

**Phase 1: Critical (12 hours)**
1. Pin all versions (ZAP image + MCP add-on)
2. Add resource limits
3. Enable HTTPS for MCP endpoint
4. Implement basic audit logging

**Phase 2: Essential (48 hours)**
5. Add scan authorization controls
6. Encrypt scan results at rest
7. Implement rate limiting
8. Create operational runbook

**Phase 3: Production-Grade (56 hours)**
9. Implement scan queue management
10. Add comprehensive audit logging
11. Setup monitoring and alerting
12. Integrate with SIEM

### 6. Specific Production Gaps for ZAP MCP

#### Configuration Hardening Needed

```yaml
# Required additions to docker-compose.yml
zap:
  image: ghcr.io/zaproxy/zaproxy:2.14.0@sha256:abc123...  # Pin version
  deploy:
    resources:
      limits:
        cpus: '2.0'
        memory: 4G
      reservations:
        cpus: '1.0'
        memory: 2G
  restart: unless-stopped
  security_opt:
    - no-new-privileges:true
  environment:
    - ZAP_MCP_SECURE_ONLY=true  # Enable HTTPS
    - ZAP_MCP_RATE_LIMIT=10     # Scans per hour
    - ZAP_MCP_MAX_DURATION=3600 # 1 hour max
```

#### Missing Operational Procedures

1. **Scan Request Approval**
   - Target validation process
   - Risk assessment checklist
   - Approval authority matrix

2. **Scan Result Triage**
   - False positive identification
   - Severity classification
   - Remediation prioritization

3. **Incident Response**
   - Accidental production scan
   - Scan causing service disruption
   - Unauthorized scan detection

4. **Compliance Reporting**
   - Scan frequency requirements
   - Result retention policies
   - Audit trail generation

### 7. Production Deployment Decision

#### ❌ **NOT PRODUCTION READY**

**Verdict:** Current ZAP MCP setup is **suitable for local development only**. Critical security and operational gaps prevent production deployment.

**Risk Level:** 🔴 **HIGH** - Running ZAP in production without proper controls poses significant security and compliance risks.

### 8. Recommended Path Forward

#### Option A: Keep as Development Tool (Recommended)

**Effort:** 12 hours
**Approach:**
1. Fix critical blockers (version pinning, resource limits)
2. Document as local-only tool
3. Use managed DAST service for production

**Pros:**
- Low effort and maintenance
- Reduced security risk
- Professional support for production scanning

**Cons:**
- Additional cost for managed service
- Less control over scanning process

#### Option B: Full Production Deployment

**Effort:** 116 hours (~3 weeks)
**Approach:**
1. Complete all security hardening phases
2. Implement operational procedures
3. Conduct security review and penetration testing
4. Ongoing operational overhead

**Pros:**
- Full control over scanning infrastructure
- No external dependencies
- Customizable to specific needs

**Cons:**
- Significant development effort
- Ongoing maintenance burden
- Security and compliance responsibility

### 9. Immediate Action Items (Priority Order)

#### P0: Critical Blockers (12 hours)
1. **Pin ZAP image version** (1h)
   - Use specific version with SHA256 digest
   - Test compatibility with MCP add-on

2. **Pin MCP add-on version** (2h)
   - Identify stable add-on version
   - Update installation command
   - Verify functionality

3. **Add resource limits** (1h)
   - Set CPU and memory limits
   - Test under load
   - Document resource requirements

4. **Enable HTTPS for MCP** (8h)
   - Generate self-signed certificate
   - Configure ZAP for HTTPS
   - Update Bob configuration
   - Test end-to-end

#### P1: Essential Security (48 hours)
5. **Implement scan authorization** (16h)
6. **Secure scan results** (12h)
7. **Add rate limiting** (12h)
8. **Create operational runbook** (8h)

#### P2: Production Hardening (56 hours)
9. **Scan queue management** (20h)
10. **Comprehensive audit logging** (8h)
11. **Monitoring and alerting** (16h)
12. **SIEM integration** (12h)

---

## Combined MCP Infrastructure Assessment

### Overall Production Readiness Matrix

| Service | Current State | Blockers | Effort to Production | Recommendation |
|---------|---------------|----------|---------------------|----------------|
| Regulatory MCP | 60% Ready | Version pinning, TLS, monitoring | 71h (9 days) | Proceed with hardening |
| SonarQube MCP | 65% Ready | Version pinning, resource limits | 48h (6 days) | Proceed with hardening |
| OWASP ZAP MCP | 30% Ready | Security controls, authorization | 116h (15 days) | Keep as dev tool |

### Total Effort Estimate

**Minimum Viable Production (All Services):**
- Regulatory MCP: 71 hours
- SonarQube MCP: 48 hours
- ZAP MCP (dev-only): 12 hours
- **Total: 131 hours (16 days)**

**Full Production Deployment (Including ZAP):**
- Regulatory MCP: 71 hours
- SonarQube MCP: 48 hours
- ZAP MCP (production): 116 hours
- **Total: 235 hours (30 days)**

### Strategic Recommendation

**Recommended Approach:**
1. **Harden Regulatory & SonarQube MCPs** for production (16 days)
2. **Keep ZAP MCP as development tool** (12 hours for stability)
3. **Evaluate managed DAST services** for production security scanning
4. **Reassess ZAP production deployment** after 6 months if managed services inadequate

**Rationale:**
- Regulatory and SonarQube MCPs provide high value with manageable hardening effort
- ZAP MCP production deployment has high security risk and operational overhead
- Managed DAST services offer better ROI for production security scanning
- Development teams still benefit from local ZAP integration

---

## Conclusion

The MCP infrastructure demonstrates **strong architectural design** but requires **significant production hardening**. The Regulatory and SonarQube MCPs are viable for production with 16 days of effort, while the OWASP ZAP MCP should remain a development tool unless there's a compelling business case for self-hosted production security scanning.

**Next Steps:**
1. Approve production hardening plan for Regulatory & SonarQube MCPs
2. Allocate 16 days for implementation
3. Stabilize ZAP MCP for development use (12 hours)
4. Evaluate managed DAST alternatives for production
</result>
</attempt_completion>

