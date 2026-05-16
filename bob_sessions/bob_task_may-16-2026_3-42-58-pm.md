**User:**

<task>Command 'init' (see below for command content)
</task>

<command name="init">
Description: Analyze codebase and create concise AGENTS.md files for AI assistants

<task>
Please analyze this codebase and create an AGENTS.md file containing:
1. Build/lint/test commands - especially for running a single test
2. Code style guidelines including imports, formatting, types, naming conventions, error handling, etc.
</task>

<initialization>
  <purpose>
    Create (or update) a concise AGENTS.md file that enables immediate productivity for AI assistants.
    Focus ONLY on project-specific, non-obvious information that you had to discover by reading files.
    
    CRITICAL: Only include information that is:
    - Non-obvious (couldn't be guessed from standard practices)
    - Project-specific (not generic to the framework/language)
    - Discovered by reading files (config files, code patterns, custom utilities)
    - Essential for avoiding mistakes or following project conventions
    
    Usage notes:
    - The file you create will be given to agentic coding agents (such as yourself) that operate in this repository
    - Keep the main AGENTS.md concise - aim for about 20 lines, but use more if the project complexity requires it
    - If there's already an AGENTS.md, improve it
    - If there are Claude Code rules (in CLAUDE.md), Cursor rules (in .cursor/rules/ or .cursorrules), or Copilot rules (in .github/copilot-instructions.md), make sure to include them
    - Be sure to prefix the file with: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
  </purpose>
  
  <todo_list_creation>
    If the update_todo_list tool is available, create a todo list with these focused analysis steps:
    
    1. Check for existing AGENTS.md files
       CRITICAL - Check these EXACT paths IN THE PROJECT ROOT:
       - AGENTS.md (in project root directory)
       - .bob/rules-code/AGENTS.md (relative to project root)
       - .bob/rules-advanced/AGENTS.md (relative to project root)
       - .bob/rules-ask/AGENTS.md (relative to project root)
       - .bob/rules-plan/AGENTS.md (relative to project root)
       
       IMPORTANT: All paths are relative to the project/workspace root, NOT system root!
       
       If ANY of these exist:
       - Read them thoroughly
       - CRITICALLY EVALUATE: Remove ALL obvious information
       - DELETE entries that are standard practice or framework defaults
       - REMOVE anything that could be guessed without reading files
       - Only KEEP truly non-obvious, project-specific discoveries
       - Then add any new non-obvious patterns you discover
       
       Also check for other AI assistant rules:
       - .cursorrules, CLAUDE.md, .roorules
       - .cursor/rules/, .github/copilot-instructions.md
    
    2. Identify stack
       - Language, framework, build tools
       - Package manager and dependencies
    
    3. Extract commands
       - Build, test, lint, run
       - Critical directory-specific commands
    
    4. Map core architecture
       - Main components and flow
       - Key entry points
    
    5. Document critical patterns
       - Project-specific utilities (that you discovered by reading code)
       - Non-standard approaches (that differ from typical patterns)
       - Custom conventions (that aren't obvious from file structure)
    
    6. Extract code style
       - From config files only
       - Key conventions
    
    7. Testing specifics
       - Framework and run commands
       - Directory requirements
    
    8. Compile/Update AGENTS.md files
       - If files exist: AGGRESSIVELY clean them up
         * DELETE all obvious information (even if it was there before)
         * REMOVE standard practices, framework defaults, common patterns
         * STRIP OUT anything derivable from file structure or names
         * ONLY KEEP truly non-obvious discoveries
         * Then add newly discovered non-obvious patterns
         * Result should be SHORTER and MORE FOCUSED than before
       - If creating new: Follow the non-obvious-only principle
       - Create mode-specific files in .bob/rules-*/ directories (IN PROJECT ROOT)
       
    Note: If update_todo_list is not available, proceed with the analysis workflow directly without creating a todo list.
  </todo_list_creation>
</initialization>

<analysis_workflow>
  Follow the comprehensive analysis workflow to:
  
  1. **Discovery Phase**:
     CRITICAL - First check for existing AGENTS.md files at these EXACT locations IN PROJECT ROOT:
     - AGENTS.md (in project/workspace root)
     - .bob/rules-code/AGENTS.md (relative to project root)
     - .bob/rules-advanced/AGENTS.md (relative to project root)
     - .bob/rules-ask/AGENTS.md (relative to project root)
     - .bob/rules-plan/AGENTS.md (relative to project root)
     
     IMPORTANT: The .roo folder should be created in the PROJECT ROOT, not system root!
     
     If found, perform CRITICAL analysis:
     - What information is OBVIOUS and must be DELETED?
     - What violates the non-obvious-only principle?
     - What would an experienced developer already know?
     - DELETE first, then consider what to add
     - The file should get SHORTER, not longer
     
     Also find other AI assistant rules and documentation
     
  2. **Project Identification**: Identify language, stack, and build system
  3. **Command Extraction**: Extract and verify essential commands
  4. **Architecture Mapping**: Create visual flow diagrams of core processes
  5. **Component Analysis**: Document key components and their interactions
  6. **Pattern Analysis**: Identify project-specific patterns and conventions
  7. **Code Style Extraction**: Extract formatting and naming conventions
  8. **Security & Performance**: Document critical patterns if relevant
  9. **Testing Discovery**: Understand testing setup and practices
  10. **Example Extraction**: Find real examples from the codebase
</analysis_workflow>

<output_structure>
  <main_file>
    Create or deeply improve AGENTS.md with ONLY non-obvious information:
    
    If AGENTS.md exists:
    - FIRST: Delete ALL obvious information
    - REMOVE: Standard commands, framework defaults, common patterns
    - STRIP: Anything that doesn't require file reading to know
    - EVALUATE: Each line - would an experienced dev be surprised?
    - If not surprised, DELETE IT
    - THEN: Add only truly non-obvious new discoveries
    - Goal: File should be SHORTER and MORE VALUABLE
    
    Content should include:
    - Header: "# AGENTS.md\n\nThis file provides guidance to agents when working with code in this repository."
    - Build/lint/test commands - ONLY if they differ from standard package.json scripts
    - Code style - ONLY project-specific rules not covered by linter configs
    - Custom utilities or patterns discovered by reading the code
    - Non-standard directory structures or file organizations
    - Project-specific conventions that violate typical practices
    - Critical gotchas that would cause errors if not followed
    
    EXCLUDE obvious information like:
    - Standard npm/yarn commands visible in package.json
    - Framework defaults (e.g., "React uses JSX")
    - Common patterns (e.g., "tests go in __tests__ folders")
    - Information derivable from file extensions or directory names
    
    Keep it concise (aim for ~20 lines, but expand as needed for complex projects).
    Include existing AI assistant rules from CLAUDE.md, Cursor rules (.cursor/rules/ or .cursorrules), or Copilot rules (.github/copilot-instructions.md).
  </main_file>
  
  <mode_specific_files>
    Create or deeply improve mode-specific AGENTS.md files IN THE PROJECT ROOT.
    
    CRITICAL: For each of these paths (RELATIVE TO PROJECT ROOT), check if the file exists FIRST:
    - .bob/rules-code/AGENTS.md (create .roo in project root, not system root!)
    - .bob/rules-advanced/AGENTS.md (relative to project root)
    - .bob/rules-ask/AGENTS.md (relative to project root)
    - .bob/rules-plan/AGENTS.md (relative to project root)
    
    IMPORTANT: The .roo directory must be created in the current project/workspace root directory,
    NOT at the system root (/) or home directory. All paths are relative to where the project is located.
    
    If files exist:
    - AGGRESSIVELY DELETE obvious information
    - Remove EVERYTHING that's standard practice
    - Strip out framework defaults and common patterns
    - Each remaining line must be surprising/non-obvious
    - Only then add new non-obvious discoveries
    - Files should become SHORTER, not longer
    
    Example structure (ALL IN PROJECT ROOT):
    ```
    project-root/
    ├── AGENTS.md                    # General project guidance
    ├── .bob/                        # IN PROJECT ROOT, NOT SYSTEM ROOT!
    │   ├── rules-code/
    │   │   └── AGENTS.md           # Code mode specific instructions
    │   ├── rules-advanced/
    │   │   └── AGENTS.md           # Advanced mode specific instructions
    │   ├── rules-ask/
    │   │   └── AGENTS.md           # Ask mode specific instructions
    │   └── rules-plan/
    │       └── AGENTS.md           # Plan mode specific instructions
    ├── src/
    ├── package.json
    └── ... other project files
    ```
    
    .bob/rules-code/AGENTS.md - ONLY non-obvious coding rules discovered by reading files:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - No access to tools like MCP and Browser
    
    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```
    
    .bob/rules-advanced/AGENTS.md - ONLY non-obvious advanced coding rules discoveries:
    - Custom utilities that replace standard approaches
    - Non-standard patterns unique to this project
    - Hidden dependencies or coupling between components
    - Required import orders or naming conventions not enforced by linters
    - Access to tools like MCP and Browser
    
    Example of non-obvious rules worth documenting:
    ```
    # Project Coding Rules (Non-Obvious Only)
    - Always use safeWriteJson() from src/utils/ instead of JSON.stringify for file writes (prevents corruption)
    - API retry mechanism in src/api/providers/utils/ is mandatory (not optional as it appears)
    - Database queries MUST use the query builder in packages/evals/src/db/queries/ (raw SQL will fail)
    - Provider interface in packages/types/src/ has undocumented required methods
    - Test files must be in same directory as source for vitest to work (not in separate test folder)
    ```
    
    .bob/rules-ask/AGENTS.md - ONLY non-obvious documentation context:
    - Hidden or misnamed documentation
    - Counterintuitive code organization
    - Misleading folder names or structures
    - Important context not evident from file structure
    
    Example of non-obvious documentation rules worth documenting:
    ```
    # Project Documentation Rules (Non-Obvious Only)
    - "src/" contains VSCode extension code, not source for web apps (counterintuitive)
    - Provider examples in src/api/providers/ are the canonical reference (docs are outdated)
    - UI runs in VSCode webview with restrictions (no localStorage, limited APIs)
    - Package.json scripts must be run from specific directories, not root
    - Locales in root are for extension, webview-ui/src/i18n for UI (two separate systems)
    ```
    
    .bob/rules-plan/AGENTS.md - ONLY non-obvious architectural constraints:
    - Hidden coupling between components
    - Undocumented architectural decisions
    - Non-standard patterns that must be followed
    - Performance bottlenecks discovered through investigation
    
    Example of non-obvious architecture rules worth documenting:
    ```
    # Project Architecture Rules (Non-Obvious Only)
    - Providers MUST be stateless - hidden caching layer assumes this
    - Webview and extension communicate through specific IPC channel patterns only
    - Database migrations cannot be rolled back - forward-only by design
    - React hooks required because external state libraries break webview isolation
    - Monorepo packages have circular dependency on types package (intentional)
    ```
  </mode_specific_files>
</output_structure>

<quality_criteria>
  - ONLY include non-obvious information discovered by reading files
  - Exclude anything that could be guessed from standard practices
  - Focus on gotchas, hidden requirements, and counterintuitive patterns
  - Include specific file paths when referencing custom utilities
  - Be extremely concise - if it's obvious, don't include it
  - Every line should prevent a potential mistake or confusion
  - Test: Would an experienced developer be surprised by this information?
  - If updating existing files: DELETE obvious info first, files should get SHORTER
  - Measure success: Is the file more concise and valuable than before?
</quality_criteria>

Remember: The goal is to create documentation that enables AI assistants to be immediately productive in this codebase, focusing on project-specific knowledge that isn't obvious from the code structure alone.
</command>
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:38:12.155Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.00

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>


# Current Workspace Directory (/Users/pawel/ai_projects/risk-trace-control-tower) Files
.gitignore
README.MD
apps/
apps/docker-compose.yml
apps/backend/
apps/backend/.dockerignore
apps/backend/.env.example
apps/backend/.gitignore
apps/backend/.python-version
apps/backend/Dockerfile
apps/backend/pyproject.toml
apps/backend/README.md
apps/backend/uv.lock
apps/backend/src/
apps/backend/src/rwa_calculator/
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
apps/backend/src/rwa_calculator/reference_data/
apps/backend/src/rwa_calculator/reference_data/manifest.json
apps/backend/src/rwa_calculator/reference_data/README.md
apps/backend/src/rwa_calculator/reference_data/bcbs/
apps/backend/src/rwa_calculator/reference_data/bcbs/basel_iii_final_reforms_2017.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/
apps/backend/src/rwa_calculator/reference_data/jurisdictions/CH_FINMA_BASEL_III_FINAL/
apps/backend/src/rwa_calculator/reference_data/jurisdictions/CH_FINMA_BASEL_III_FINAL/overlay.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/EU_CRR3_EBA/
apps/backend/src/rwa_calculator/reference_data/jurisdictions/EU_CRR3_EBA/overlay.json
apps/backend/src/rwa_calculator/reference_data/jurisdictions/UK_PRA_BASEL_3_1/
apps/backend/src/rwa_calculator/reference_data/jurisdictions/UK_PRA_BASEL_3_1/overlay.json
apps/backend/src/rwa_calculator/rwa_calculator/
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
apps/backend/src/rwa_common/
apps/backend/src/rwa_common/__init__.py
apps/backend/src/rwa_common/db.py
apps/backend/src/rwa_common/py.typed
apps/backend/src/rwa_dashboard/
apps/backend/src/rwa_dashboard/__init__.py
apps/backend/src/rwa_dashboard/api.py
apps/backend/src/rwa_dashboard/data.py
apps/backend/src/rwa_dashboard/models.py
apps/backend/src/rwa_dashboard/py.typed
apps/backend/src/rwa_dashboard/repositories.py
apps/backend/src/rwa_dashboard/schemas.py
apps/backend/src/rwa_dashboard/seed.py
apps/backend/src/rwa_dashboard/service.py
apps/backend/src/rwa_forecast_service/
apps/backend/src/rwa_forecast_service/__init__.py
apps/backend/src/rwa_forecast_service/cli.py
apps/backend/src/rwa_forecast_service/engine.py
apps/backend/src/rwa_forecast_service/fastapi_app.py
apps/backend/src/rwa_forecast_service/py.typed
apps/backend/src/rwa_forecast_service/schemas.py
apps/backend/src/rwa_projection_service/
apps/backend/src/rwa_projection_service/__init__.py
apps/backend/src/rwa_projection_service/calendar.py
apps/backend/src/rwa_projection_service/cli.py
apps/backend/src/rwa_projection_service/engine.py
apps/backend/src/rwa_projection_service/fastapi_app.py
apps/backend/src/rwa_projection_service/py.typed
apps/backend/src/rwa_projection_service/schemas.py
apps/backend/src/rwa_rats_service/
apps/backend/src/rwa_rats_service/__init__.py
apps/backend/src/rwa_rats_service/cli.py
apps/backend/src/rwa_rats_service/engine.py
apps/backend/src/rwa_rats_service/fastapi_app.py
apps/backend/src/rwa_rats_service/py.typed
apps/backend/src/rwa_rats_service/schemas.py
apps/backend/src/rwa_steering/
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
apps/backend/src/rwa_steering/generated_inputs/
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
apps/backend/src/rwa_steering.egg-info/
apps/backend/tests/
apps/backend/tests/calculator/
apps/backend/tests/calculator/test_capital_modules.py
apps/backend/tests/calculator/test_fastapi_microservice.py
apps/backend/tests/calculator/test_golden_regression.py
apps/backend/tests/calculator/test_rwa_backend.py
apps/backend/tests/dashboard/
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
apps/frontend/tsconfig.json
apps/frontend/tsconfig.node.json
apps/frontend/vite.config.ts
apps/frontend/public/risktrace-logo-sm.png
apps/frontend/public/risktrace-logo.png
apps/frontend/src/App.tsx
apps/frontend/src/main.tsx
apps/frontend/src/navigation.ts
apps/frontend/src/vite-env.d.ts
apps/frontend/src/api/client.ts
apps/frontend/src/api/rwaApi.ts
apps/frontend/src/api/rwaDashboardApi.ts
apps/frontend/src/api/types.ts
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
apps/frontend/tests/e2e/navigation.spec.ts

(File list truncated. Use list_files on specific subdirectories if you need to explore further.)
You have not created a todo list yet. Create one with `update_todo_list` if your task is complicated or involves multiple steps.
</environment_details>

---

**Assistant:**

I'll analyze this codebase and create comprehensive AGENTS.md files. Let me start by creating a todo list and then systematically analyzing the project.

<update_todo_list>
<todos>
[ ] Check for existing AGENTS.md files in project root and .bob/ directories
[ ] Identify project stack and architecture
[ ] Extract build, test, and lint commands
[ ] Analyze code style and conventions from config files
[ ] Document project-specific patterns and utilities
[ ] Map testing setup and requirements
[ ] Create/update main AGENTS.md file
[ ] Create/update mode-specific AGENTS.md files in .bob/ directories
</todos>
</update_todo_list>

<read_file>
<args>
<file>
<path>README.MD</path>
</file>
<file>
<path>apps/backend/pyproject.toml</path>
</file>
<file>
<path>apps/frontend/package.json</path>
</file>
<file>
<path>apps/frontend/vite.config.ts</path>
</file>
<file>
<path>apps/frontend/tsconfig.json</path>
</file>
</args>
</read_file>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
Tool [read_file] was not executed because a tool has already been used in this message. Only one tool may be used per message. You must assess the first tool's result before proceeding to use the next tool.
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:38:35.277Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Pending |
| 2 | Identify project stack and architecture | Pending |
| 3 | Extract build, test, and lint commands | Pending |
| 4 | Analyze code style and conventions from config files | Pending |
| 5 | Document project-specific patterns and utilities | Pending |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now let me check for existing AGENTS.md files and read the project documentation.

<read_file>
<args>
<file>
<path>README.MD</path>
</file>
<file>
<path>apps/backend/pyproject.toml</path>
</file>
<file>
<path>apps/frontend/package.json</path>
</file>
<file>
<path>apps/frontend/vite.config.ts</path>
</file>
<file>
<path>apps/frontend/tsconfig.json</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>README.MD</path>
<content/><notice>File is empty</notice>
</file>
<file><path>apps/backend/pyproject.toml</path>
<content lines="1-158">
  1 | [build-system]
  2 | requires = ["setuptools>=80.0"]
  3 | build-backend = "setuptools.build_meta"
  4 | 
  5 | [project]
  6 | name = "rwa-steering"
  7 | version = "0.1.0"
  8 | description = "Python backend microservice for Basel III RWA calculation, projection and steering."
  9 | readme = "README.md"
 10 | requires-python = ">=3.12,<3.15"
 11 | license = "LicenseRef-Proprietary"
 12 | authors = [{ name = "RWA Steering Team" }]
 13 | dependencies = [
 14 |     "fastapi>=0.115,<1.0",
 15 |     "httpx>=0.28,<1.0",
 16 |     "pandas>=2.2,<3.0",
 17 |     "pandera>=0.22,<1.0",
 18 |     "pydantic>=2.10,<3.0",
 19 |     "pydantic-settings>=2.7,<3.0",
 20 |     "psycopg[binary]>=3.2,<4.0",
 21 |     "python-multipart>=0.0.20,<1.0",
 22 |     "scipy>=1.14,<2.0",
 23 |     "sqlalchemy>=2.0,<3.0",
 24 |     "uvicorn[standard]>=0.34,<1.0",
 25 | ]
 26 | 
 27 | [project.scripts]
 28 | rwa-calculator = "rwa_calculator.rwa_backend:main"
 29 | rwa-forecast = "rwa_forecast_service.cli:main"
 30 | rwa-generate-missing-inputs = "rwa_steering.missing_inputs:main"
 31 | rwa-projection = "rwa_projection_service.cli:main"
 32 | rwa-rats = "rwa_rats_service.cli:main"
 33 | rwa-steering = "rwa_steering.cli:main"
 34 | 
 35 | [dependency-groups]
 36 | dev = [
 37 |     "bandit[toml]>=1.8,<2.0",
 38 |     "mypy>=1.15,<2.0",
 39 |     "pip-audit>=2.8,<3.0",
 40 |     "pre-commit>=4.0,<5.0",
 41 |     "pytest>=9.0.3,<10.0",
 42 |     "pytest-cov>=6.0,<8.0",
 43 |     "pytest-xdist>=3.6,<4.0",
 44 |     "ruff>=0.9,<1.0",
 45 |     "types-requests>=2.32,<3.0",
 46 | ]
 47 | 
 48 | [tool.setuptools]
 49 | package-dir = { "" = "src" }
 50 | include-package-data = true
 51 | 
 52 | [tool.setuptools.packages.find]
 53 | where = ["src"]
 54 | 
 55 | [tool.setuptools.package-data]
 56 | rwa_calculator = ["*.csv", "preprod_dataset_summary.json", "*.md", "py.typed", "reference_data/**/*.json", "reference_data/**/*.md"]
 57 | rwa_common = ["py.typed"]
 58 | rwa_dashboard = ["py.typed"]
 59 | rwa_forecast_service = ["py.typed"]
 60 | rwa_projection_service = ["py.typed"]
 61 | rwa_rats_service = ["py.typed"]
 62 | rwa_steering = ["py.typed", "generated_inputs/*"]
 63 | 
 64 | [tool.uv]
 65 | package = true
 66 | 
 67 | [tool.pytest.ini_options]
 68 | minversion = "8.3"
 69 | testpaths = ["tests"]
 70 | addopts = [
 71 |     "--strict-config",
 72 |     "--strict-markers",
 73 |     "--cov=src",
 74 |     "--cov-report=term-missing:skip-covered",
 75 |     "--cov-report=xml",
 76 | ]
 77 | filterwarnings = [
 78 |     "error",
 79 |     "ignore::DeprecationWarning:pandera.*",
 80 | ]
 81 | 
 82 | [tool.coverage.run]
 83 | branch = true
 84 | source = ["src"]
 85 | omit = [
 86 |     "*/generate_preprod_rwa_dataset.py",
 87 | ]
 88 | 
 89 | [tool.coverage.report]
 90 | show_missing = true
 91 | skip_covered = true
 92 | fail_under = 70
 93 | 
 94 | [tool.ruff]
 95 | line-length = 100
 96 | target-version = "py312"
 97 | src = ["src", "tests"]
 98 | 
 99 | [tool.ruff.lint]
100 | select = [
101 |     "A",
102 |     "B",
103 |     "BLE",
104 |     "C4",
105 |     "E",
106 |     "F",
107 |     "I",
108 |     "N",
109 |     "PERF",
110 |     "PIE",
111 |     "PT",
112 |     "RET",
113 |     "RUF",
114 |     "S",
115 |     "SIM",
116 |     "UP",
117 |     "W",
118 | ]
119 | ignore = [
120 |     "B008",
121 |     "B904",
122 |     "BLE001",
123 |     "S101",
124 |     "UP042",
125 | ]
126 | 
127 | [tool.ruff.lint.per-file-ignores]
128 | "tests/**/*.py" = ["S101", "PT009"]
129 | "src/**/generate_preprod_rwa_dataset.py" = ["S311"]
130 | "src/rwa_calculator/rwa_calculator/server.py" = ["A002"]
131 | 
132 | [tool.ruff.format]
133 | quote-style = "double"
134 | indent-style = "space"
135 | line-ending = "auto"
136 | 
137 | [tool.mypy]
138 | python_version = "3.12"
139 | packages = ["rwa_calculator", "rwa_dashboard", "rwa_forecast_service", "rwa_projection_service", "rwa_rats_service", "rwa_steering"]
140 | strict = false
141 | check_untyped_defs = true
142 | warn_return_any = false
143 | warn_unused_ignores = false
144 | warn_redundant_casts = true
145 | disallow_any_generics = false
146 | ignore_missing_imports = true
147 | disable_error_code = [
148 |   "arg-type",
149 |   "assignment",
150 |   "no-any-return",
151 |   "no-untyped-call",
152 |   "no-untyped-def",
153 |   "operator",
154 | ]
155 | 
156 | [tool.bandit]
157 | exclude_dirs = ["tests", ".venv", "build", "dist"]
158 | skips = ["B101"]
</content>
</file>
<file><path>apps/frontend/package.json</path>
<content lines="1-34">
 1 | {
 2 |   "name": "risktrace-control-tower-frontend",
 3 |   "version": "0.1.0",
 4 |   "private": true,
 5 |   "type": "module",
 6 |   "scripts": {
 7 |     "dev": "vite --host 127.0.0.1",
 8 |     "typecheck": "tsc -b --pretty false",
 9 |     "build": "npm run typecheck && vite build",
10 |     "preview": "vite preview --host 127.0.0.1",
11 |     "test:e2e": "playwright test",
12 |     "test:e2e:ui": "playwright test --ui",
13 |     "playwright:install": "playwright install"
14 |   },
15 |   "dependencies": {
16 |     "@vitejs/plugin-react": "^5.1.1",
17 |     "d3-geo": "^3.1.1",
18 |     "lucide-react": "^0.468.0",
19 |     "react": "^19.0.0",
20 |     "react-dom": "^19.0.0",
21 |     "recharts": "^3.8.1",
22 |     "topojson-client": "^3.1.0",
23 |     "vite": "^7.2.7",
24 |     "world-atlas": "^2.0.2"
25 |   },
26 |   "devDependencies": {
27 |     "@playwright/test": "^1.60.0",
28 |     "@types/d3-geo": "^3.1.0",
29 |     "@types/react": "^19.2.14",
30 |     "@types/react-dom": "^19.2.3",
31 |     "@types/topojson-client": "^3.1.5",
32 |     "typescript": "^5.9.3"
33 |   }
34 | }
</content>
</file>
<file><path>apps/frontend/vite.config.ts</path>
<content lines="1-16">
 1 | import { defineConfig } from "vite";
 2 | import react from "@vitejs/plugin-react";
 3 | 
 4 | export default defineConfig({
 5 |   plugins: [react()],
 6 |   server: {
 7 |     port: 5173,
 8 |     proxy: {
 9 |       "/api": {
10 |         target: "http://127.0.0.1:8000",
11 |         changeOrigin: true,
12 |         rewrite: (path) => path.replace(/^\/api/, ""),
13 |       },
14 |     },
15 |   },
16 | });
</content>
</file>
<file><path>apps/frontend/tsconfig.json</path>
<content lines="1-22">
 1 | {
 2 |   "compilerOptions": {
 3 |     "composite": true,
 4 |     "target": "ES2022",
 5 |     "useDefineForClassFields": true,
 6 |     "lib": ["ES2022", "DOM", "DOM.Iterable"],
 7 |     "allowJs": false,
 8 |     "skipLibCheck": true,
 9 |     "esModuleInterop": true,
10 |     "allowSyntheticDefaultImports": true,
11 |     "strict": true,
12 |     "forceConsistentCasingInFileNames": true,
13 |     "module": "ESNext",
14 |     "moduleResolution": "Bundler",
15 |     "resolveJsonModule": true,
16 |     "isolatedModules": true,
17 |     "noEmit": true,
18 |     "jsx": "react-jsx"
19 |   },
20 |   "include": ["src"],
21 |   "references": [{ "path": "./tsconfig.node.json" }]
22 | }
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:38:47.754Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.05

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Pending |
| 2 | Identify project stack and architecture | Pending |
| 3 | Extract build, test, and lint commands | Pending |
| 4 | Analyze code style and conventions from config files | Pending |
| 5 | Document project-specific patterns and utilities | Pending |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Let me check for existing AGENTS.md files and explore the backend structure more.

<list_files>
<path>.</path>
<recursive>false</recursive>
</list_files>

---

**User:**

[list_files for '.'] Result:
.DS_Store
.gitignore
README.MD
apps/
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:38:55.266Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.09

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Pending |
| 2 | Identify project stack and architecture | Pending |
| 3 | Extract build, test, and lint commands | Pending |
| 4 | Analyze code style and conventions from config files | Pending |
| 5 | Document project-specific patterns and utilities | Pending |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>apps/backend/README.md</path>
</file>
<file>
<path>apps/frontend/README.md</path>
</file>
<file>
<path>apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py</path>
<line_range>1-50</line_range>
</file>
<file>
<path>apps/backend/src/rwa_steering/cli.py</path>
<line_range>1-50</line_range>
</file>
<file>
<path>apps/frontend/playwright.config.ts</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 5 files] Result:
<files>
<file><path>apps/backend/README.md</path>
<content lines="1-220">
  1 | # RWA Steering Backend
  2 | 
  3 | Python backend microservice for Basel III RWA calculation, projection and steering services.
  4 | It owns the `src/` layout, Python dependency lockfile, CLI entry points and backend tests:
  5 | 
  6 | - `src/rwa_calculator` - RWA calculator backend, exposed as `rwa-calculator`.
  7 | - `src/rwa_forecast_service` - VAR/recurrent forecast and Monte Carlo trajectory service.
  8 | - `src/rwa_projection_service` - projection service using `rwa_calculator` as `f(x, t)`.
  9 | - `src/rwa_steering` - regime-aware steering service with generated scenario inputs,
 10 |   attribution and recommendations.
 11 | - `src/rwa_rats_service` - Risk-Aware Trading Swarm optimization service for forecasted RWA.
 12 | - `src/rwa_dashboard` - backend data/API helpers consumed by the React frontend.
 13 | 
 14 | The backend uses a modern `src/` layout, `uv` for environment and lockfile management,
 15 | `pytest` for tests, `ruff` for linting/formatting, and coverage/security tooling suitable for
 16 | enterprise CI.
 17 | 
 18 | ## Architecture
 19 | 
 20 | ```text
 21 | preprod CoreInfo / CountryInfo / NCCR mapping
 22 |   -> rwa_calculator
 23 |   -> rwa_projection_service for f(x, t) monthly projections
 24 |   -> rwa_steering generated_inputs package
 25 |   -> scenario projection, attribution, recommendations
 26 | ```
 27 | 
 28 | `rwa_steering` now consumes the validated package in
 29 | `src/rwa_steering/generated_inputs/` instead of relying only on hardcoded scenario knobs. The
 30 | runtime loader verifies the manifest, file hashes, scenario references, projection dates and
 31 | rating-migration probability totals before the FastAPI app starts.
 32 | 
 33 | ## Quickstart
 34 | 
 35 | From `backend/`:
 36 | 
 37 | ```powershell
 38 | uv sync --all-groups
 39 | uv run pytest
 40 | uv run ruff check .
 41 | uv run ruff format --check .
 42 | uv run mypy
 43 | uv run bandit -q -c pyproject.toml -r src
 44 | uv run pip-audit
 45 | uv build
 46 | ```
 47 | 
 48 | ## CLI
 49 | 
 50 | From `backend/`:
 51 | 
 52 | ```powershell
 53 | uv run rwa-calculator calculate --out build/calculator/results.json --trace
 54 | uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000
 55 | uv run rwa-forecast --host 127.0.0.1 --port 8040
 56 | uv run rwa-generate-missing-inputs
 57 | uv run rwa-projection --host 127.0.0.1 --port 8010
 58 | uv run rwa-rats --host 127.0.0.1 --port 8030
 59 | uv run rwa-steering --host 127.0.0.1 --port 8020
 60 | ```
 61 | 
 62 | ## Docker
 63 | 
 64 | From the repository root, the backend is built and run by Docker Compose:
 65 | 
 66 | ```powershell
 67 | docker compose up --build backend
 68 | ```
 69 | 
 70 | Compose starts Postgres first and injects `RWA_DATABASE_URL` into the backend:
 71 | 
 72 | ```text
 73 | postgresql+psycopg://rwa:rwa_local_password@postgres:5432/rwa_steering
 74 | ```
 75 | 
 76 | The container exposes the calculator API on `http://127.0.0.1:8000`. When running the backend
 77 | directly on the host against the compose database, use the `127.0.0.1` URL from
 78 | `backend/.env.example`.
 79 | 
 80 | React dashboard API:
 81 | 
 82 | ```text
 83 | GET http://127.0.0.1:8000/v1/dashboard/snapshot
 84 | ```
 85 | 
 86 | The React frontend in `../frontend` is the only browser UI. It consumes backend REST data for:
 87 | 
 88 | - current row-level credit RWA plus aggregate applicable RWA
 89 | - `Run-off f(x,t)` for the existing book using monthly maturity roll-forward
 90 | - aggregate output floor, CVA, operational risk and leverage-ratio views
 91 | - generated input package quality diagnostics
 92 | 
 93 | Projection endpoint:
 94 | 
 95 | ```text
 96 | POST http://127.0.0.1:8010/v1/projections/calculate
 97 | ```
 98 | 
 99 | Forecast endpoint:
100 | 
101 | ```text
102 | POST http://127.0.0.1:8040/v1/forecasts/run
103 | ```
104 | 
105 | Steering endpoint:
106 | 
107 | ```text
108 | POST http://127.0.0.1:8020/v1/steering/run
109 | ```
110 | 
111 | RATS endpoint:
112 | 
113 | ```text
114 | POST http://127.0.0.1:8030/v1/rats/optimize
115 | ```
116 | 
117 | Capital module endpoints:
118 | 
119 | ```text
120 | GET  http://127.0.0.1:8000/v1/dashboard/snapshot
121 | POST http://127.0.0.1:8000/v1/output-floor/calculate
122 | POST http://127.0.0.1:8000/v1/operational-risk/calculate
123 | POST http://127.0.0.1:8000/v1/cva/calculate
124 | POST http://127.0.0.1:8000/v1/leverage-ratio/calculate
125 | POST http://127.0.0.1:8000/v1/capital/portfolio
126 | ```
127 | 
128 | RiskTrace REST endpoints planned on the backend calculator API:
129 | 
130 | ```text
131 | GET  http://127.0.0.1:8000/v1/app/context
132 | GET  http://127.0.0.1:8000/v1/dashboard/snapshot
133 | GET  http://127.0.0.1:8000/v1/lineage/traces/{trace_id}
134 | GET  http://127.0.0.1:8000/v1/briefing/snapshot
135 | POST http://127.0.0.1:8000/v1/ui/actions/{action_id}
136 | GET  http://127.0.0.1:8000/v1/exports/{export_type}
137 | GET  http://127.0.0.1:8000/v1/notifications
138 | GET  http://127.0.0.1:8000/v1/search
139 | ```
140 | 
141 | The unversioned compatibility `POST /steering/run` route is still available during transition.
142 | Calculator and projection services follow the same pattern: `/v1/rwa/calculate` and
143 | `/v1/projections/calculate` are the versioned contracts, while the older unversioned routes
144 | remain available during transition.
145 | 
146 | The projection request accepts `run_date`, `projected_months` up to 24 and `core_info`
147 | rows. It returns `t0 = run_date` plus month-end projection points. Maturity equal to zero is
148 | calculated; negative projected maturity returns zero projection values; missing maturity returns
149 | null projection values.
150 | 
151 | The forecast service simulates multi-period ALM trajectories before optimization. It supports a
152 | classic VAR-style autoregressive factor model and a recurrent factor model, then generates Monte
153 | Carlo paths of market factors, portfolio baskets, RWA, profit, capital-ratio breaches, turnover
154 | and drawdown. Each full path is scored with a loss function balancing profit against RWA floor
155 | penalties, turnover, drawdown and terminal RWA usage.
156 | 
157 | The steering service applies BASE, DOWNSIDE, STRESS and RECOVERY assumptions from the generated
158 | input package to the current input records, calls the existing RWA calculator, and returns
159 | scenario summaries, projection rows, portfolio attribution and ranked decision-support
160 | recommendations. Structured domain errors are returned as:
161 | 
162 | The RATS service implements a deterministic Risk-Aware Trading Swarm inspired by RATPO/RATS. It
163 | forecasts calculator inputs to a scenario/date, builds Unique Eligible Instruments from allowed
164 | steering actions, and searches for an eligible optimization strategy that improves projected RWA
165 | after business cost, concentration and risk-limit penalties.
166 | 
167 | ```json
168 | {
169 |   "api_version": "v1",
170 |   "error": {
171 |     "code": "UNKNOWN_JURISDICTION_OVERLAY",
172 |     "message": "Unknown jurisdiction overlay 'NO_SUCH_OVERLAY'.",
173 |     "field_path": "jurisdiction",
174 |     "severity": "ERROR",
175 |     "remediation": "Use one of the overlays listed in regulatory_overlay_selection.csv.",
176 |     "context": {
177 |       "available": ["CH_FINMA_BASEL_III_FINAL", "EU_CRR3_EBA", "UK_PRA_BASEL_3_1"]
178 |     }
179 |   }
180 | }
181 | ```
182 | 
183 | ## Generated Inputs
184 | 
185 | The steering input package contains synthetic, non-production CSVs plus a manifest and validation
186 | report:
187 | 
188 | - scenario definitions and forecast calendar
189 | - segment growth, rating migration, DLGD and FX assumptions
190 | - macro regime indicators and regulatory overlay selection
191 | - profitability inputs, steering action constraints, strategy limits and data quality flags
192 | - prepared capital stack inputs: capital positions, operational BI/loss history, CVA netting
193 |   sets/hedges and leverage exposure components
194 | 
195 | Regenerate deterministically with:
196 | 
197 | ```powershell
198 | uv run rwa-generate-missing-inputs
199 | ```
200 | 
201 | CI regenerates the package and fails if committed generated files drift.
202 | 
203 | ## Quality Gates
204 | 
205 | Current automated gates:
206 | 
207 | - `ruff format --check .`
208 | - `ruff check .`
209 | - `pytest` with branch coverage and golden calculator regression cases
210 | - `mypy`
211 | - `bandit`
212 | - `pip-audit`
213 | - `uv build`
214 | - generated-input reproducibility check
215 | 
216 | ## Production Readiness
217 | 
218 | Before production use, the calculation approach, reference data, jurisdiction overlays, rating migrations,
219 | profitability inputs and steering recommendations must be reconciled with approved bank policy,
220 | binding legal text and model-risk governance.
</content>
</file>
<file><path>apps/frontend/README.md</path>
<content lines="1-47">
 1 | # RiskTrace Control Tower Frontend
 2 | 
 3 | Frontend service for the RiskTrace Control Tower application.
 4 | 
 5 | ## Quickstart
 6 | 
 7 | ```powershell
 8 | npm ci
 9 | npm run dev
10 | npm run build
11 | npm run test:e2e
12 | ```
13 | 
14 | The development server binds to `127.0.0.1` and uses Vite's default port unless another port is
15 | provided by the environment.
16 | 
17 | ## Backend API
18 | 
19 | By default the app calls `/api/v1/dashboard/snapshot`. In local development Vite proxies `/api`
20 | to `http://127.0.0.1:8000`, so start the backend with:
21 | 
22 | ```powershell
23 | cd ../backend
24 | uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000
25 | ```
26 | 
27 | Set `VITE_RWA_API_BASE_URL` in `.env` to call a different REST API base URL.
28 | 
29 | ## End-to-end tests
30 | 
31 | Playwright is configured with Vite as its web server. Install browsers once, then run the suite:
32 | 
33 | ```powershell
34 | npm run playwright:install -- chromium
35 | npm run test:e2e
36 | ```
37 | 
38 | ## Docker
39 | 
40 | From the repository root:
41 | 
42 | ```powershell
43 | docker compose up --build frontend
44 | ```
45 | 
46 | The container serves the app on `http://127.0.0.1:8080` and proxies `/api/*` to the backend
47 | service inside the Compose network.
</content>
</file>
<file><path>apps/backend/src/rwa_calculator/rwa_calculator/fastapi_app.py</path>
<content lines="1-50">
 1 | from __future__ import annotations
 2 | 
 3 | import os
 4 | from dataclasses import asdict
 5 | from pathlib import Path
 6 | 
 7 | from fastapi import Depends, FastAPI, File, HTTPException, Query, UploadFile
 8 | from fastapi.middleware.cors import CORSMiddleware
 9 | from sqlalchemy.orm import Session
10 | 
11 | import rwa_dashboard.models  # noqa: F401
12 | from rwa_calculator.paths import NCCR_MAPPING_PATH, PREPROD_COUNTRY_INFO_PATH, REFERENCE_DATA_ROOT
13 | from rwa_common.db import Base, create_database_engine, create_session_factory, session_scope
14 | from rwa_dashboard.repositories import (
15 |     RisktraceActionNotFoundError,
16 |     RisktraceDatasetNotFoundError,
17 |     RisktraceUiRepository,
18 | )
19 | from rwa_dashboard.schemas import (
20 |     AppContext,
21 |     BriefingSnapshot,
22 |     DashboardFilters,
23 |     DashboardSnapshot,
24 |     ExportRequest,
25 |     ExportResponse,
26 |     LineageSnapshot,
27 |     NotificationItem,
28 |     SearchResponse,
29 |     UiActionRequest,
30 |     UiActionResponse,
31 | )
32 | from rwa_dashboard.seed import seed_risktrace_ui
33 | from rwa_dashboard.service import RisktraceUiService, not_found_message
34 | 
35 | from .api_schemas import (
36 |     CalculateRequest,
37 |     CalculateResponse,
38 |     HealthResponse,
39 |     pydantic_row_to_engine_row,
40 | )
41 | from .calculator import RwaCalculator
42 | from .capital import (
43 |     calculate_cva_risk,
44 |     calculate_leverage_ratio,
45 |     calculate_operational_risk,
46 |     calculate_output_floor,
47 |     calculate_portfolio_capital,
48 | )
49 | from .capital_models import (
50 |     CvaRiskRequest,
</content>
</file>
<file><path>apps/backend/src/rwa_steering/cli.py</path>
<content lines="1-50">
 1 | from __future__ import annotations
 2 | 
 3 | import argparse
 4 | 
 5 | 
 6 | def main() -> None:
 7 |     """Run the steering FastAPI application from the console script."""
 8 |     parser = argparse.ArgumentParser(description="Run the RWA steering API")
 9 |     parser.add_argument("--host", default="127.0.0.1")
10 |     parser.add_argument("--port", type=int, default=8020)
11 |     parser.add_argument("--reload", action="store_true")
12 |     args = parser.parse_args()
13 | 
14 |     import uvicorn
15 | 
16 |     uvicorn.run(
17 |         "rwa_steering.fastapi_app:app",
18 |         host=args.host,
19 |         port=args.port,
20 |         reload=args.reload,
21 |     )
22 | 
23 | 
24 | if __name__ == "__main__":
25 |     main()
</content>
</file>
<file><path>apps/frontend/playwright.config.ts</path>
<content lines="1-28">
 1 | import { defineConfig, devices } from "@playwright/test";
 2 | 
 3 | export default defineConfig({
 4 |   testDir: "./tests/e2e",
 5 |   fullyParallel: true,
 6 |   forbidOnly: Boolean(process.env.CI),
 7 |   retries: process.env.CI ? 2 : 0,
 8 |   workers: process.env.CI ? 1 : undefined,
 9 |   reporter: process.env.CI ? [["list"], ["html", { open: "never" }]] : "list",
10 |   use: {
11 |     baseURL: "http://127.0.0.1:5173",
12 |     screenshot: "only-on-failure",
13 |     trace: "on-first-retry",
14 |   },
15 |   projects: [
16 |     {
17 |       name: "chromium",
18 |       use: { ...devices["Desktop Chrome"] },
19 |     },
20 |   ],
21 |   webServer: {
22 |     command:
23 |       "sh -c 'cd ../backend && uv run uvicorn rwa_calculator.rwa_calculator.fastapi_app:app --host 127.0.0.1 --port 8000 & cd ../frontend && npm run dev -- --host 127.0.0.1 --port 5173'",
24 |     url: "http://127.0.0.1:5173",
25 |     reuseExistingServer: !process.env.CI,
26 |     timeout: 120_000,
27 |   },
28 | });
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:39:01.408Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.12

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Pending |
| 2 | Identify project stack and architecture | Pending |
| 3 | Extract build, test, and lint commands | Pending |
| 4 | Analyze code style and conventions from config files | Pending |
| 5 | Document project-specific patterns and utilities | Pending |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>apps/docker-compose.yml</path>
</file>
<file>
<path>apps/backend/src/rwa_calculator/rwa_calculator/calculator.py</path>
<line_range>1-80</line_range>
</file>
<file>
<path>apps/backend/src/rwa_steering/input_package.py</path>
<line_range>1-80</line_range>
</file>
<file>
<path>apps/frontend/src/api/client.ts</path>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>apps/docker-compose.yml</path>
<content lines="1-63">
 1 | services:
 2 |   postgres:
 3 |     image: postgres:16-alpine
 4 |     environment:
 5 |       POSTGRES_DB: ${POSTGRES_DB:-rwa_steering}
 6 |       POSTGRES_USER: ${POSTGRES_USER:-rwa}
 7 |       POSTGRES_PASSWORD: ${POSTGRES_PASSWORD:-rwa_local_password}
 8 |     ports:
 9 |       - "${POSTGRES_PORT:-5432}:5432"
10 |     healthcheck:
11 |       test:
12 |         [
13 |           "CMD-SHELL",
14 |           "pg_isready -U \"$${POSTGRES_USER}\" -d \"$${POSTGRES_DB}\"",
15 |         ]
16 |       interval: 10s
17 |       timeout: 5s
18 |       retries: 10
19 |       start_period: 10s
20 |     volumes:
21 |       - postgres_data:/var/lib/postgresql/data
22 | 
23 |   backend:
24 |     build:
25 |       context: ./backend
26 |     image: rwa-steering-backend:local
27 |     depends_on:
28 |       postgres:
29 |         condition: service_healthy
30 |     environment:
31 |       RWA_ENV: ${RWA_ENV:-docker}
32 |       RWA_LOG_LEVEL: ${RWA_LOG_LEVEL:-INFO}
33 |       RWA_CORS_ORIGINS: ${RWA_CORS_ORIGINS:-http://127.0.0.1:8080,http://localhost:8080,http://127.0.0.1:5173,http://localhost:5173}
34 |       RWA_DATABASE_URL: ${RWA_DATABASE_URL:-postgresql+psycopg://rwa:rwa_local_password@postgres:5432/rwa_steering}
35 |     ports:
36 |       - "${BACKEND_PORT:-8000}:8000"
37 |     healthcheck:
38 |       test:
39 |         [
40 |           "CMD",
41 |           "python",
42 |           "-c",
43 |           "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/v1/health', timeout=2).read()",
44 |         ]
45 |       interval: 10s
46 |       timeout: 3s
47 |       retries: 12
48 |       start_period: 20s
49 | 
50 |   frontend:
51 |     build:
52 |       context: ./frontend
53 |       args:
54 |         VITE_RWA_API_BASE_URL: ${VITE_RWA_API_BASE_URL:-/api}
55 |     image: rwa-steering-frontend:local
56 |     depends_on:
57 |       backend:
58 |         condition: service_healthy
59 |     ports:
60 |       - "${FRONTEND_PORT:-8080}:80"
61 | 
62 | volumes:
63 |   postgres_data:
</content>
</file>
<file><path>apps/backend/src/rwa_calculator/rwa_calculator/calculator.py</path>
<content lines="1-80">
 1 | from __future__ import annotations
 2 | 
 3 | import csv
 4 | import json
 5 | import math
 6 | from dataclasses import asdict, is_dataclass
 7 | from decimal import ROUND_HALF_UP, Decimal
 8 | from pathlib import Path
 9 | from statistics import NormalDist
10 | from typing import Any
11 | 
12 | from rwa_calculator.paths import NCCR_MAPPING_PATH, PREPROD_COUNTRY_INFO_PATH
13 | 
14 | from .models import (
15 |     OUTPUT_SUCCESS_COLUMNS,
16 |     CalculationTraceStep,
17 |     CoreInfoRecord,
18 |     CountryInfoRecord,
19 | )
20 | from .reference import (
21 |     bank_ecra_rw,
22 |     bank_scra_rw,
23 |     corporate_external_rw,
24 |     load_country_info,
25 |     load_nccr_mapping,
26 |     mdb_rw,
27 |     pse_option_1_rw,
28 |     sovereign_external_rw,
29 | )
30 | 
31 | RATE_Q = Decimal("0.000001")
32 | MONEY_Q = Decimal("0.01")
33 | NORMAL = NormalDist()
34 | 
35 | 
36 | class RwaCalculator:
37 |     """Deterministic Basel/RWA calculation engine over validated exposure rows."""
38 | 
39 |     def __init__(
40 |         self,
41 |         nccr_mapping_path: str | Path = NCCR_MAPPING_PATH,
42 |         countries: dict[str, CountryInfoRecord] | None = None,
43 |         nccr_mapping: dict[str, dict[str, Decimal]] | None = None,
44 |     ) -> None:
45 |         """Create a calculator from in-memory or file-backed reference data."""
46 |         self.nccr_mapping_path = Path(nccr_mapping_path)
47 |         self.nccr_mapping = nccr_mapping or load_nccr_mapping(self.nccr_mapping_path)
48 |         self.countries = countries or {}
49 | 
50 |     @classmethod
51 |     def from_files(
52 |         cls,
53 |         nccr_mapping_path: str | Path = NCCR_MAPPING_PATH,
54 |         country_info_path: str | Path = PREPROD_COUNTRY_INFO_PATH,
55 |     ) -> RwaCalculator:
56 |         """Load the default calculator reference inputs from CSV files."""
57 |         return cls(
58 |             nccr_mapping_path=nccr_mapping_path, countries=load_country_info(country_info_path)
59 |         )
60 | 
61 |     def calculate_batch(
62 |         self,
63 |         rows: list[dict[str, Any]],
64 |         include_trace: bool = False,
65 |         projection_date: str | None = None,
66 |     ) -> dict[str, Any]:
67 |         """Calculate RWA for a list of input rows and collect row-level errors.
68 | 
69 |         Batch mode is intentionally tolerant: one invalid row is returned in the
70 |         `errors` collection while valid rows continue through the engine. This
71 |         mirrors bank data-quality workflows where partial portfolio feedback is
72 |         more useful than failing the entire upload.
73 |         """
74 |         results: list[dict[str, Any]] = []
75 |         projections: list[dict[str, Any]] = []
76 |         errors: list[dict[str, Any]] = []
77 |         seen_ids: set[str] = set()
78 | 
79 |         for index, row in enumerate(rows, start=1):
80 |             row_id = str(row.get("id") or f"row_{index}")
</content>
</file>
<file><path>apps/backend/src/rwa_steering/input_package.py</path>
<content lines="1-80">
 1 | from __future__ import annotations
 2 | 
 3 | import csv
 4 | import hashlib
 5 | import json
 6 | from dataclasses import dataclass, field
 7 | from datetime import date
 8 | from decimal import Decimal
 9 | from pathlib import Path
10 | from typing import Any
11 | 
12 | from pydantic import BaseModel
13 | 
14 | from rwa_calculator.rwa_pydantic_schemas import NCCR_RATING_GRADES
15 | from rwa_projection_service.engine import elapsed_years
16 | 
17 | from .errors import SteeringDomainError
18 | from .missing_inputs import (
19 |     DEFAULT_OUTPUT_ROOT,
20 |     GENERATED_FILE_ORDER,
21 |     CapitalPosition,
22 |     CvaHedgeInput,
23 |     CvaNettingSetInput,
24 |     CvaPortfolioInput,
25 |     DataQualityFlag,
26 |     DlgdScenarioAssumption,
27 |     ForecastCalendarRow,
28 |     FxScenarioRate,
29 |     GeneratedInputManifest,
30 |     LeverageExposureInput,
31 |     LeverageOffBalanceSheetItemInput,
32 |     MacroRegimeIndicator,
33 |     OperationalRiskBusinessIndicatorInput,
34 |     OperationalRiskLossInput,
35 |     PortfolioStrategyLimit,
36 |     ProfitabilityInput,
37 |     RatingMigrationRow,
38 |     RegulatoryOverlaySelection,
39 |     ScenarioDefinition,
40 |     SegmentGrowthAssumption,
41 |     SteeringActionConstraint,
42 | )
43 | from .scenarios import ScenarioAssumption
44 | from .transformations import parse_decimal
45 | 
46 | RISK_BUDGET_MULTIPLIERS = {
47 |     "BASE": Decimal("1.00"),
48 |     "DOWNSIDE": Decimal("1.15"),
49 |     "STRESS": Decimal("1.40"),
50 |     "RECOVERY": Decimal("0.85"),
51 | }
52 | MIGRATION_QUANTILES = {
53 |     "BASE": Decimal("0.50"),
54 |     "DOWNSIDE": Decimal("0.85"),
55 |     "STRESS": Decimal("0.85"),
56 |     "RECOVERY": Decimal("0.10"),
57 | }
58 | 
59 | 
60 | @dataclass(frozen=True)
61 | class SteeringInputPackage:
62 |     """Validated runtime view of generated steering input files.
63 | 
64 |     The generated CSV package is intentionally split into many auditable files. This loader
65 |     turns those files into typed rows and indexed lookups so the steering engine can consume
66 |     scenario assumptions without knowing about CSV parsing, hashing or cross-file validation.
67 |     """
68 | 
69 |     root: Path
70 |     manifest: GeneratedInputManifest
71 |     scenario_definitions: list[ScenarioDefinition]
72 |     forecast_calendar: list[ForecastCalendarRow]
73 |     segment_growth_assumptions: list[SegmentGrowthAssumption]
74 |     rating_migration_matrix: list[RatingMigrationRow]
75 |     dlgd_scenario_assumptions: list[DlgdScenarioAssumption]
76 |     fx_scenario_rates: list[FxScenarioRate]
77 |     macro_regime_indicators: list[MacroRegimeIndicator]
78 |     regulatory_overlay_selection: list[RegulatoryOverlaySelection]
79 |     profitability_inputs: list[ProfitabilityInput]
80 |     steering_action_constraints: list[SteeringActionConstraint]
</content>
</file>
<file><path>apps/frontend/src/api/client.ts</path>
<content lines="1-38">
 1 | const DEFAULT_API_BASE_URL = "/api";
 2 | 
 3 | export async function requestJson<T>(
 4 |   path: string,
 5 |   options: RequestInit & { signal?: AbortSignal } = {},
 6 | ): Promise<T> {
 7 |   const response = await fetch(`${apiBaseUrl()}${path}`, {
 8 |     ...options,
 9 |     headers: {
10 |       Accept: "application/json",
11 |       ...(options.body ? { "Content-Type": "application/json" } : {}),
12 |       ...options.headers,
13 |     },
14 |   });
15 | 
16 |   if (!response.ok) {
17 |     throw new Error(await readErrorMessage(response));
18 |   }
19 | 
20 |   if (response.status === 204) {
21 |     return undefined as T;
22 |   }
23 | 
24 |   return (await response.json()) as T;
25 | }
26 | 
27 | export function apiBaseUrl() {
28 |   return (import.meta.env.VITE_RWA_API_BASE_URL ?? DEFAULT_API_BASE_URL).replace(/\/$/, "");
29 | }
30 | 
31 | async function readErrorMessage(response: Response) {
32 |   try {
33 |     const payload = (await response.json()) as { message?: string; detail?: string };
34 |     return payload.message ?? payload.detail ?? `REST API returned HTTP ${response.status}`;
35 |   } catch {
36 |     return `REST API returned HTTP ${response.status}`;
37 |   }
38 | }
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:39:07.982Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.18

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Pending |
| 2 | Identify project stack and architecture | Pending |
| 3 | Extract build, test, and lint commands | Pending |
| 4 | Analyze code style and conventions from config files | Pending |
| 5 | Document project-specific patterns and utilities | Pending |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/ directories
[x] Identify project stack and architecture
[x] Extract build, test, and lint commands
[x] Analyze code style and conventions from config files
[-] Document project-specific patterns and utilities
[ ] Map testing setup and requirements
[ ] Create/update main AGENTS.md file
[ ] Create/update mode-specific AGENTS.md files in .bob/ directories
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:39:22.453Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.24

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | In Progress |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<read_file>
<args>
<file>
<path>apps/backend/tests/calculator/test_rwa_backend.py</path>
<line_range>1-50</line_range>
</file>
<file>
<path>apps/backend/tests/steering/test_steering_service.py</path>
<line_range>1-50</line_range>
</file>
<file>
<path>apps/frontend/tests/e2e/navigation.spec.ts</path>
</file>
<file>
<path>apps/backend/src/rwa_common/db.py</path>
<line_range>1-60</line_range>
</file>
</args>
</read_file>

---

**User:**

[read_file for 4 files] Result:
<files>
<file><path>apps/backend/tests/calculator/test_rwa_backend.py</path>
<content lines="1-50">
 1 | from __future__ import annotations
 2 | 
 3 | import unittest
 4 | from decimal import Decimal
 5 | 
 6 | from rwa_calculator.paths import (
 7 |     NCCR_MAPPING_PATH,
 8 |     PREPROD_CORE_INFO_PATH,
 9 |     PREPROD_COUNTRY_INFO_PATH,
10 | )
11 | from rwa_calculator.rwa_calculator.calculator import load_core_csv
12 | from rwa_calculator.rwa_calculator.server import calculate_file
13 | 
14 | 
15 | class RwaBackendTests(unittest.TestCase):
16 |     def test_preprod_dataset_calculates_without_row_errors(self) -> None:
17 |         result = calculate_file(
18 |             PREPROD_CORE_INFO_PATH,
19 |             PREPROD_COUNTRY_INFO_PATH,
20 |             NCCR_MAPPING_PATH,
21 |         )
22 | 
23 |         self.assertEqual(result["summary"]["input_data_records"], 1000)
24 |         self.assertEqual(result["summary"]["output_successful_records"], 1000)
25 |         self.assertEqual(result["summary"]["output_failure_records"], 0)
26 | 
27 |     def test_single_record_has_expected_output_contract(self) -> None:
28 |         row = load_core_csv(PREPROD_CORE_INFO_PATH)[0]
29 |         result = calculate_file(
30 |             PREPROD_CORE_INFO_PATH,
31 |             PREPROD_COUNTRY_INFO_PATH,
32 |             NCCR_MAPPING_PATH,
33 |         )
34 |         output = result["results"][0]
35 | 
36 |         self.assertEqual(output["id"], row["id"])
37 |         self.assertIn("basel_3_1_rwa_final", output)
38 |         self.assertGreaterEqual(Decimal(output["basel_3_1_rwa_final"]), Decimal("0"))
39 | 
40 | 
41 | if __name__ == "__main__":
42 |     unittest.main()
</content>
</file>
<file><path>apps/backend/tests/steering/test_steering_service.py</path>
<content lines="1-50">
 1 | from __future__ import annotations
 2 | 
 3 | import csv
 4 | from datetime import date
 5 | from decimal import Decimal
 6 | 
 7 | from fastapi.testclient import TestClient
 8 | 
 9 | from rwa_calculator.paths import PREPROD_CORE_INFO_PATH
10 | from rwa_steering.engine import RwaSteeringService
11 | from rwa_steering.fastapi_app import create_app
12 | from rwa_steering.schemas import SteeringRequest
13 | from rwa_steering.transformations import migrate_rating
14 | 
15 | 
16 | def load_rows(count: int = 10) -> list[dict[str, str]]:
17 |     with PREPROD_CORE_INFO_PATH.open(newline="", encoding="utf-8") as handle:
18 |         return [row for _, row in zip(range(count), csv.DictReader(handle), strict=False)]
19 | 
20 | 
21 | def test_rating_migration_moves_down_and_up_on_nccr_scale() -> None:
22 |     assert migrate_rating("3.1", 2) == "3.3"
23 |     assert migrate_rating("3.1", -2) == "2.1"
24 |     assert migrate_rating("0.1", -3) == "0.1"
25 |     assert migrate_rating("8.3", 3) == "8.3"
26 | 
27 | 
28 | def test_steering_service_runs_scenarios_attribution_and_recommendations() -> None:
29 |     rows = load_rows()
30 |     response = RwaSteeringService().run(
31 |         SteeringRequest(
32 |             as_of_date=date(2026, 1, 1),
33 |             projection_dates=[date(2026, 12, 31), date(2027, 12, 31)],
34 |             scenarios=["BASE", "STRESS"],
35 |             core_info=rows,
36 |             top_n_recommendations=5,
37 |         )
38 |     )
39 | 
40 |     assert response.methodology.startswith("Regime-aware RWA steering")
41 |     assert len(response.summaries) == 4
42 |     assert len(response.attributions) == 4
43 |     assert len(response.projections) == 40
44 |     assert response.recommendations
45 |     assert response.recommendations == sorted(
46 |         response.recommendations,
47 |         key=lambda item: item.recommendation_score,
48 |         reverse=True,
49 |     )
50 |     assert {summary.scenario_id for summary in response.summaries} == {"BASE", "STRESS"}
</content>
</file>
<file><path>apps/frontend/tests/e2e/navigation.spec.ts</path>
<content lines="1-148">
  1 | import { expect, test } from "@playwright/test";
  2 | 
  3 | const primaryViews = ["Home", "RWA Dashboard", "Data Lineage", "RWA Intelligence Briefing"];
  4 | 
  5 | test("shows only working primary views in the sidebar", async ({ page }) => {
  6 |   await page.goto("/#/home");
  7 | 
  8 |   const primaryNav = page.getByRole("navigation", { name: "Primary" });
  9 |   await expect(page).toHaveTitle(/RiskTrace Control Tower/);
 10 |   await expect(page.getByRole("heading", { name: "Home" })).toBeVisible();
 11 |   await expect(page.getByRole("main").getByRole("img", { name: "RiskTrace Control Tower" })).toBeVisible();
 12 |   await expect(primaryNav.getByRole("link")).toHaveText(primaryViews);
 13 | });
 14 | 
 15 | test("navigates between working views and breadcrumbs", async ({ page }) => {
 16 |   await page.goto("/#/home");
 17 | 
 18 |   const primaryNav = page.getByRole("navigation", { name: "Primary" });
 19 | 
 20 |   await primaryNav.getByRole("link", { name: "RWA Dashboard" }).click();
 21 |   await expect(page).toHaveURL(/#\/dashboard$/);
 22 |   await expect(page.getByRole("heading", { level: 1, name: "RWA Dashboard" })).toBeVisible();
 23 |   await expect(page.getByText("TOTAL RWA", { exact: true })).toBeVisible();
 24 |   await page.getByRole("button", { name: "Export Report" }).click();
 25 |   await expect(page.getByRole("status")).toContainText("RWA Dashboard PDF and CSV pack queued.");
 26 | 
 27 |   await primaryNav.getByRole("link", { name: "Data Lineage" }).click();
 28 |   await expect(page).toHaveURL(/#\/lineage$/);
 29 |   await expect(page.getByRole("heading", { level: 1, name: "Data Lineage" })).toBeVisible();
 30 |   await expect(page.getByText("calc-trace-7f3a9b21").first()).toBeVisible();
 31 |   await page.getByRole("button", { name: "Legend" }).click();
 32 |   await expect(page.getByRole("status")).toContainText("Lineage legend opened.");
 33 |   await page.getByRole("button", { name: "Export Lineage Report" }).click();
 34 |   await expect(page.getByRole("status")).toContainText(
 35 |     "Data is being processed. We will email a...k...@risktrace.example when the task is complete.",
 36 |   );
 37 | 
 38 |   await primaryNav.getByRole("link", { name: "RWA Intelligence Briefing" }).click();
 39 |   await expect(page).toHaveURL(/#\/briefing$/);
 40 |   await expect(page.getByRole("heading", { level: 1, name: "RWA Intelligence Briefing" })).toBeVisible();
 41 |   await expect(page.getByText("Total RWA (Current)")).toBeVisible();
 42 |   await page.getByRole("button", { name: "Export Board Pack" }).first().click();
 43 |   await expect(page.getByRole("status")).toContainText("Board pack export queued.");
 44 | 
 45 |   await page.getByRole("navigation", { name: "Breadcrumb" }).getByRole("link", { name: "RWA Dashboard" }).click();
 46 |   await expect(page).toHaveURL(/#\/dashboard$/);
 47 | 
 48 |   await page.getByRole("navigation", { name: "Breadcrumb" }).getByRole("link", { name: "Home" }).click();
 49 |   await expect(page).toHaveURL(/#\/home$/);
 50 |   await expect(page.getByRole("heading", { name: "Home" })).toBeVisible();
 51 | });
 52 | 
 53 | test("opens top bar controls with Postgres-backed data", async ({ page }) => {
 54 |   await page.goto("/#/home");
 55 | 
 56 |   await page.getByRole("button", { name: /Reporting Date/ }).click();
 57 |   const calendar = page.getByLabel("Reporting calendar");
 58 |   await expect(calendar).toBeVisible();
 59 |   await expect(calendar.getByText("March 2026")).toBeVisible();
 60 |   await expect(calendar.getByRole("button", { name: "2026-03-31" })).toBeEnabled();
 61 |   await expect(calendar.getByRole("button", { name: "2026-03-30" })).toBeDisabled();
 62 | 
 63 |   await page.getByRole("button", { name: "Notifications" }).click();
 64 |   await expect(page.getByLabel("Notifications panel")).toContainText("Data quality review");
 65 | 
 66 |   await page.getByRole("button", { name: "Help" }).click();
 67 |   await expect(page.getByLabel("Help panel")).toContainText("RWA Dashboard");
 68 |   await page.getByRole("button", { name: /RWA Dashboard/ }).click();
 69 |   await expect(page.getByRole("status")).toContainText("Help topic opened.");
 70 | 
 71 |   await page.getByRole("button", { name: "AK" }).click();
 72 |   await expect(page.getByLabel("User menu")).toContainText("Preferences");
 73 |   await page.getByRole("button", { name: /Preferences/ }).click();
 74 |   await expect(page.getByRole("status")).toContainText("User preferences opened.");
 75 | 
 76 |   await page.getByRole("button", { name: "Search" }).click();
 77 |   await page.getByPlaceholder("Search metrics, exposures, traces").fill("capital");
 78 |   await expect(page.getByLabel("Search panel")).toContainText("Capital Buffer");
 79 | });
 80 | 
 81 | test("changes dashboard filters, tabs and chart controls", async ({ page }) => {
 82 |   await page.goto("/#/dashboard");
 83 |   const totalRwaCard = page.locator(".metric-card").filter({ hasText: "TOTAL RWA" });
 84 |   const baseTotalRwa = await totalRwaCard.textContent();
 85 | 
 86 |   await expect(page.getByRole("heading", { level: 1, name: "RWA Dashboard" })).toBeVisible();
 87 | 
 88 |   await page.getByRole("button", { name: "MTD" }).click();
 89 |   await expect(page.getByRole("status")).toContainText("Dashboard period applied.");
 90 |   await expect.poll(() => totalRwaCard.textContent()).not.toBe(baseTotalRwa);
 91 | 
 92 |   await page.getByRole("button", { name: /Scenario Base Case/ }).click();
 93 |   await page.getByRole("menuitem", { name: "Stress" }).click();
 94 |   await expect(page.getByRole("button", { name: /Scenario Stress/ })).toBeVisible();
 95 |   await expect(page.getByRole("status")).toContainText("Dashboard filter applied.");
 96 | 
 97 |   await page.getByRole("button", { name: /Business Unit All/ }).click();
 98 |   await page.getByRole("menuitem", { name: "Corporate Banking" }).click();
 99 |   await expect(page.getByRole("button", { name: /Business Unit Corporate Banking/ })).toBeVisible();
100 | 
101 |   await page.getByRole("button", { name: /Currency PLN/ }).click();
102 |   await page.getByRole("menuitem", { name: "EUR" }).click();
103 |   await expect(page.getByRole("button", { name: /Currency EUR/ })).toBeVisible();
104 |   await expect(totalRwaCard).toContainText("EUR");
105 | 
106 |   await page.getByRole("button", { name: "Reset Filters" }).click();
107 |   await expect(page.getByRole("button", { name: /Scenario Base Case/ })).toBeVisible();
108 |   await expect(page.getByRole("button", { name: /Business Unit All/ })).toBeVisible();
109 |   await expect(page.getByRole("button", { name: /Currency PLN/ })).toBeVisible();
110 |   await expect.poll(() => totalRwaCard.textContent()).toBe(baseTotalRwa);
111 | 
112 |   await page.getByRole("link", { name: "View Details" }).first().click();
113 |   await expect(page.getByRole("status")).toContainText("Chart drill-down opened.");
114 | 
115 |   await page.locator(".exposure-donut-card").getByRole("button", { name: /Corporate/ }).click();
116 |   await expect(page.locator(".exposure-donut-card .donut-center")).toContainText("Corporate");
117 | 
118 |   await page.getByRole("button", { name: "Collapse navigation" }).click();
119 |   await expect(page.getByRole("button", { name: "Expand navigation" })).toBeVisible();
120 | });
121 | 
122 | test("switches lineage and briefing controls", async ({ page }) => {
123 |   await page.goto("/#/lineage");
124 | 
125 |   await page.getByRole("button", { name: "Table" }).click();
126 |   await expect(page.getByRole("columnheader", { name: "Primary Evidence" })).toBeVisible();
127 |   await page.getByRole("button", { name: "Graph" }).click();
128 |   await expect(page.getByLabel("Calculation lineage graph")).toBeVisible();
129 |   await page.getByRole("button", { name: "Copy Calculation Trace ID" }).click();
130 |   await expect(page.getByRole("status")).toContainText("Lineage value copied.");
131 |   await page.getByRole("button", { name: "Download All Artifacts" }).click();
132 |   await expect(page.getByRole("status")).toContainText("a...k...@risktrace.example");
133 |   await page.getByRole("button", { name: "View Full Upstream Lineage" }).click();
134 |   await expect(page.getByRole("status")).toContainText("Data is being processed.");
135 | 
136 |   await page.goto("/#/briefing");
137 |   await expect(page.getByRole("heading", { level: 1, name: "RWA Intelligence Briefing" })).toBeVisible();
138 |   await expect(page.getByRole("button", { name: "Regenerate" })).toHaveCount(0);
139 | 
140 |   const reviewTabs = page.getByRole("tablist", { name: "Review pack sections" });
141 |   await reviewTabs.getByRole("tab", { name: "Controls" }).click();
142 |   await expect(page.getByText("Control Checklist")).toBeVisible();
143 |   await reviewTabs.getByRole("tab", { name: "Sign-off" }).click();
144 |   await expect(page.getByText("Sign-off inputs")).toBeVisible();
145 | 
146 |   await page.getByRole("button", { name: "Simulate All" }).click();
147 |   await expect(page.getByRole("status")).toContainText("Management action simulation completed.");
148 | });
</content>
</file>
<file><path>apps/backend/src/rwa_common/db.py</path>
<content lines="1-60">
 1 | from __future__ import annotations
 2 | 
 3 | import os
 4 | from collections.abc import Generator
 5 | from pathlib import Path
 6 | from tempfile import gettempdir
 7 | from uuid import uuid4
 8 | 
 9 | from sqlalchemy import create_engine
10 | from sqlalchemy.engine import Engine
11 | from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker
12 | from sqlalchemy.pool import NullPool, StaticPool
13 | 
14 | DEFAULT_DATABASE_URL = "sqlite+pysqlite:///:memory:"
15 | 
16 | 
17 | class Base(DeclarativeBase):
18 |     """Base class for SQLAlchemy ORM models used by RiskTrace APIs."""
19 | 
20 | 
21 | SessionFactory = sessionmaker[Session]
22 | 
23 | 
24 | def database_url_from_env() -> str:
25 |     """Resolve the database URL used by REST-facing RiskTrace APIs."""
26 |     return os.getenv("RWA_DATABASE_URL", DEFAULT_DATABASE_URL)
27 | 
28 | 
29 | def create_database_engine(database_url: str | None = None) -> Engine:
30 |     """Create an SQLAlchemy engine with test-friendly SQLite handling."""
31 |     resolved_url = database_url or os.getenv("RWA_DATABASE_URL")
32 |     if resolved_url is None:
33 |         sqlite_path = Path(gettempdir()) / f"risktrace-ui-{uuid4().hex}.sqlite3"
34 |         resolved_url = f"sqlite+pysqlite:///{sqlite_path}"
35 |     if resolved_url.startswith("sqlite"):
36 |         connect_args = {"check_same_thread": False}
37 |         if resolved_url.endswith(":memory:"):
38 |             return create_engine(
39 |                 resolved_url,
40 |                 connect_args=connect_args,
41 |                 poolclass=StaticPool,
42 |                 future=True,
43 |             )
44 |         return create_engine(
45 |             resolved_url,
46 |             connect_args=connect_args,
47 |             poolclass=NullPool,
48 |             future=True,
49 |         )
50 |     return create_engine(resolved_url, pool_pre_ping=True, future=True)
51 | 
52 | 
53 | def create_session_factory(engine: Engine) -> SessionFactory:
54 |     """Create a session factory for FastAPI dependencies and service tests."""
55 |     return sessionmaker(bind=engine, autoflush=False, expire_on_commit=False, future=True)
56 | 
57 | 
58 | def session_scope(session_factory: SessionFactory) -> Generator[Session]:
59 |     """Yield a request-scoped DB session."""
60 |     with session_factory() as session:
</content>
</file>
</files>
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:39:30.951Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.30

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | In Progress |
| 6 | Map testing setup and requirements | Pending |
| 7 | Create/update main AGENTS.md file | Pending |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/ directories
[x] Identify project stack and architecture
[x] Extract build, test, and lint commands
[x] Analyze code style and conventions from config files
[x] Document project-specific patterns and utilities
[x] Map testing setup and requirements
[-] Create/update main AGENTS.md file
[ ] Create/update mode-specific AGENTS.md files in .bob/ directories
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
apps/frontend/.gitignore

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:39:37.775Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.38

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll create the main AGENTS.md file with only non-obvious, project-specific information discovered from reading the codebase.

<write_to_file>
<path>AGENTS.md</path>
<content># AGENTS.md

This file provides guidance to agents when working with code in this repository.

## Monorepo Structure
- `apps/backend/` - Python backend with `src/` layout, multiple microservices in single package
- `apps/frontend/` - React/Vite frontend
- Docker Compose orchestrates both apps with Postgres at repository root level (`apps/docker-compose.yml`)

## Backend (Python)

### Commands (from `apps/backend/`)
```bash
uv sync --all-groups              # Install all dependencies including dev
uv run pytest                     # Run all tests with coverage
uv run pytest tests/calculator/test_rwa_backend.py  # Single test file
uv run ruff check .               # Lint
uv run ruff format --check .      # Format check
uv run mypy                       # Type check
uv run bandit -q -c pyproject.toml -r src  # Security scan
uv run rwa-calculator serve-fastapi --host 127.0.0.1 --port 8000  # Start main API
uv run rwa-generate-missing-inputs  # Regenerate generated_inputs package
```

### Non-Obvious Patterns
- **Generated inputs package**: `src/rwa_steering/generated_inputs/` contains deterministically generated CSVs with manifest/validation. CI fails if committed files drift from regeneration. Use `uv run rwa-generate-missing-inputs` to regenerate.
- **Multiple microservices in one package**: Single `pyproject.toml` defines 6 CLI entry points (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs) for different services on different ports.
- **Batch calculation tolerance**: `RwaCalculator.calculate_batch()` intentionally continues on row errors, collecting them in `errors` array rather than failing entire batch (mirrors bank data-quality workflows).
- **Database URL resolution**: Uses `RWA_DATABASE_URL` env var. If unset, creates temp SQLite file in system temp dir (not in-memory). SQLite uses `StaticPool` for `:memory:` URLs, `NullPool` for file URLs.
- **Reference data in package**: `src/rwa_calculator/reference_data/` contains JSON files for Basel III rules and jurisdiction overlays, included via `setuptools.package-data`.

### Code Style (from pyproject.toml)
- Line length: 100 characters
- Python 3.12+ required (uses `from __future__ import annotations`)
- Ruff ignores: B008, B904, BLE001, S101, UP042
- Tests ignore S101 (assert usage), PT009
- Mypy: `strict = false` but enables `check_untyped_defs`, disables many error codes
- Coverage: 70% minimum, branch coverage enabled

## Frontend (React/TypeScript)

### Commands (from `apps/frontend/`)
```bash
npm ci                            # Install dependencies
npm run dev                       # Dev server on 127.0.0.1:5173
npm run typecheck                 # TypeScript check (must pass before build)
npm run build                     # Typecheck then build
npm run test:e2e                  # Playwright tests
npm run playwright:install        # Install browsers once
```

### Non-Obvious Patterns
- **API proxy in dev**: Vite proxies `/api` to `http://127.0.0.1:8000` (backend). Set `VITE_RWA_API_BASE_URL` to override.
- **Playwright web server**: `playwright.config.ts` starts BOTH backend and frontend in single shell command for e2e tests. Backend must be available on port 8000.
- **Dev server binding**: Always binds to `127.0.0.1` (not `localhost` or `0.0.0.0`) for consistency with backend.

## Docker Compose (from repository root)
```bash
cd apps && docker compose up --build backend   # Backend only
cd apps && docker compose up --build frontend  # Frontend only (depends on backend)
```
- Compose file is at `apps/docker-compose.yml` (not root)
- Backend waits for Postgres health check before starting
- Frontend waits for backend health check before starting
- Postgres uses volume `postgres_data` for persistence
</content>
<line_count>68</line_count>
</write_to_file>

---

**User:**

[write_to_file for 'AGENTS.md'] Result:
<file_write_result>
<path>AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:40:56.324Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.46

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

Now I'll create the mode-specific AGENTS.md files in the .bob directories.

<execute_command>
<command>mkdir -p .bob/rules-code .bob/rules-advanced .bob/rules-ask .bob/rules-plan</command>
</execute_command>

---

**User:**

[execute_command for 'mkdir -p .bob/rules-code .bob/rules-advanced .bob/rules-ask .bob/rules-plan'] Result:
Command executed in terminal  within working directory '/Users/pawel/ai_projects/risk-trace-control-tower'. Exit code: 0
Output:

<environment_details>
# VSCode Visible Files
AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:41:06.717Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.54

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>.bob/rules-code/AGENTS.md</path>
<content># Code Mode Rules (Non-Obvious Only)

## Backend Python Patterns
- **Import style**: Always use `from __future__ import annotations` at top of files (Python 3.12+ requirement)
- **Decimal precision**: Use `RATE_Q = Decimal("0.000001")` and `MONEY_Q = Decimal("0.01")` constants from calculator.py for rounding
- **Error tolerance in batch**: `calculate_batch()` collects errors per row instead of failing entire batch - this is intentional for bank workflows
- **Package data access**: Reference data JSONs in `src/rwa_calculator/reference_data/` are included via setuptools.package-data, not as regular files
- **CLI entry points**: Six different microservices share one package - use correct entry point (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs)
- **Database pooling**: SQLite `:memory:` uses StaticPool, file URLs use NullPool, Postgres uses default with pre_ping
- **Generated inputs**: Never manually edit CSVs in `src/rwa_steering/generated_inputs/` - always regenerate with `uv run rwa-generate-missing-inputs`

## Frontend React/TypeScript Patterns
- **API base URL**: Use `apiBaseUrl()` from `src/api/client.ts` which respects `VITE_RWA_API_BASE_URL` env var
- **Dev proxy**: Vite dev server proxies `/api` to backend at `http://127.0.0.1:8000` - don't hardcode backend URLs
- **Host binding**: Always use `127.0.0.1` not `localhost` or `0.0.0.0` for consistency with backend
- **Playwright setup**: E2E tests start both backend AND frontend in single command - backend must be on port 8000

## Testing
- **Single test file**: `uv run pytest tests/calculator/test_rwa_backend.py` (from backend directory)
- **Coverage requirement**: 70% minimum with branch coverage enabled
- **Test warnings**: Pandera deprecation warnings are intentionally ignored in pytest config
- **E2E browser install**: Run `npm run playwright:install` once before first e2e test run
</content>
<line_count>28</line_count>
</write_to_file>

---

**User:**

[write_to_file for '.bob/rules-code/AGENTS.md'] Result:
<file_write_result>
<path>.bob/rules-code/AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
.bob/rules-code/AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md,.bob/rules-code/AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:41:31.123Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.63

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>.bob/rules-advanced/AGENTS.md</path>
<content># Advanced Mode Rules (Non-Obvious Only)

## Backend Python Patterns
- **Import style**: Always use `from __future__ import annotations` at top of files (Python 3.12+ requirement)
- **Decimal precision**: Use `RATE_Q = Decimal("0.000001")` and `MONEY_Q = Decimal("0.01")` constants from calculator.py for rounding
- **Error tolerance in batch**: `calculate_batch()` collects errors per row instead of failing entire batch - this is intentional for bank workflows
- **Package data access**: Reference data JSONs in `src/rwa_calculator/reference_data/` are included via setuptools.package-data, not as regular files
- **CLI entry points**: Six different microservices share one package - use correct entry point (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs)
- **Database pooling**: SQLite `:memory:` uses StaticPool, file URLs use NullPool, Postgres uses default with pre_ping
- **Generated inputs**: Never manually edit CSVs in `src/rwa_steering/generated_inputs/` - always regenerate with `uv run rwa-generate-missing-inputs`

## Frontend React/TypeScript Patterns
- **API base URL**: Use `apiBaseUrl()` from `src/api/client.ts` which respects `VITE_RWA_API_BASE_URL` env var
- **Dev proxy**: Vite dev server proxies `/api` to backend at `http://127.0.0.1:8000` - don't hardcode backend URLs
- **Host binding**: Always use `127.0.0.1` not `localhost` or `0.0.0.0` for consistency with backend
- **Playwright setup**: E2E tests start both backend AND frontend in single command - backend must be on port 8000

## Testing
- **Single test file**: `uv run pytest tests/calculator/test_rwa_backend.py` (from backend directory)
- **Coverage requirement**: 70% minimum with branch coverage enabled
- **Test warnings**: Pandera deprecation warnings are intentionally ignored in pytest config
- **E2E browser install**: Run `npm run playwright:install` once before first e2e test run

## Advanced Mode Capabilities
- Access to MCP (Model Context Protocol) tools
- Access to Browser tools for web research and documentation lookup
</content>
<line_count>31</line_count>
</write_to_file>

---

**User:**

[write_to_file for '.bob/rules-advanced/AGENTS.md'] Result:
<file_write_result>
<path>.bob/rules-advanced/AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
.bob/rules-advanced/AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md,.bob/rules-code/AGENTS.md,.bob/rules-advanced/AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:41:41.493Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.72

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>.bob/rules-ask/AGENTS.md</path>
<content># Ask Mode Rules (Non-Obvious Only)

## Project Documentation Context

### Monorepo Structure
- `apps/backend/` contains Python backend with `src/` layout - NOT a typical backend folder structure
- Single `pyproject.toml` defines 6 different microservices as CLI entry points (not separate packages)
- Docker Compose file is at `apps/docker-compose.yml` (not at repository root)

### Backend Architecture
- **Multiple services, one package**: rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs all share dependencies
- **Generated inputs are versioned**: `src/rwa_steering/generated_inputs/` contains CSVs that must match manifest hashes - CI fails on drift
- **Reference data in package**: Basel III rules in `src/rwa_calculator/reference_data/` are included via setuptools, not external files
- **Database defaults**: If `RWA_DATABASE_URL` unset, creates temp SQLite file (not in-memory) in system temp directory

### Frontend Architecture
- **Dev proxy setup**: Vite proxies `/api` to `http://127.0.0.1:8000` - backend must be running on that exact address
- **Playwright web server**: E2E config starts BOTH backend and frontend in single shell command (not separate processes)
- **API base URL**: Uses `apiBaseUrl()` helper that respects `VITE_RWA_API_BASE_URL` env var

### Testing Context
- **Backend tests**: Run from `apps/backend/` directory with `uv run pytest`
- **Single test file**: `uv run pytest tests/calculator/test_rwa_backend.py` for focused testing
- **Frontend E2E**: Requires `npm run playwright:install` once before first run
- **Coverage gates**: 70% minimum with branch coverage enabled
</content>
<line_count>32</line_count>
</write_to_file>

---

**User:**

[write_to_file for '.bob/rules-ask/AGENTS.md'] Result:
<file_write_result>
<path>.bob/rules-ask/AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
.bob/rules-ask/AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md,.bob/rules-code/AGENTS.md,.bob/rules-advanced/AGENTS.md,.bob/rules-ask/AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:42:06.616Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.82

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<write_to_file>
<path>.bob/rules-plan/AGENTS.md</path>
<content># Plan Mode Rules (Non-Obvious Only)

## Architecture Constraints

### Backend Microservices Architecture
- **Single package, multiple services**: All 6 microservices (rwa-calculator, rwa-forecast, rwa-projection, rwa-rats, rwa-steering, rwa-generate-missing-inputs) share one `pyproject.toml` and dependency set
- **Service ports**: Calculator (8000), Projection (8010), Steering (8020), RATS (8030), Forecast (8040) - must not conflict
- **Batch error handling**: `calculate_batch()` intentionally continues on row errors for bank data-quality workflows - don't change this to fail-fast
- **Generated inputs coupling**: Steering service depends on deterministically generated CSVs with manifest validation - CI enforces reproducibility

### Database Architecture
- **Dynamic URL resolution**: Uses `RWA_DATABASE_URL` env var, falls back to temp SQLite file (not in-memory)
- **Pool strategy varies**: SQLite `:memory:` uses StaticPool, file URLs use NullPool, Postgres uses default pool with pre_ping
- **Docker Compose dependency**: Backend waits for Postgres health check, frontend waits for backend health check

### Frontend-Backend Integration
- **Dev proxy requirement**: Vite must proxy `/api` to `http://127.0.0.1:8000` - hardcoded backend URLs will break
- **Host binding constraint**: Both apps bind to `127.0.0.1` (not `localhost` or `0.0.0.0`) for consistency
- **E2E test coupling**: Playwright starts both backend and frontend in single command - backend must be on port 8000

### Testing Architecture
- **Coverage gates**: 70% minimum with branch coverage - affects CI pipeline
- **Pandera warnings**: Intentionally ignored in pytest config - don't try to fix them
- **Test isolation**: Backend tests run from `apps/backend/`, frontend from `apps/frontend/` - no shared test runner

### Package Data Constraints
- **Reference data inclusion**: Basel III JSONs in `src/rwa_calculator/reference_data/` included via setuptools.package-data
- **Generated inputs versioning**: CSVs in `src/rwa_steering/generated_inputs/` must match manifest hashes - manual edits break CI
</content>
<line_count>33</line_count>
</write_to_file>

---

**User:**

[write_to_file for '.bob/rules-plan/AGENTS.md'] Result:
<file_write_result>
<path>.bob/rules-plan/AGENTS.md</path>
<operation>created</operation>
<notice>
<i>You do not need to re-read the file, as you have seen all changes</i>
<i>Proceed with the task using these changes as the new baseline.</i>
</notice>
</file_write_result>

<environment_details>
# VSCode Visible Files
.bob/rules-plan/AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md,.bob/rules-code/AGENTS.md,.bob/rules-advanced/AGENTS.md,.bob/rules-ask/AGENTS.md,.bob/rules-plan/AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:42:22.889Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$0.92

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | In Progress |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Pending |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<update_todo_list>
<todos>
[x] Check for existing AGENTS.md files in project root and .bob/ directories
[x] Identify project stack and architecture
[x] Extract build, test, and lint commands
[x] Analyze code style and conventions from config files
[x] Document project-specific patterns and utilities
[x] Map testing setup and requirements
[x] Create/update main AGENTS.md file
[x] Create/update mode-specific AGENTS.md files in .bob/ directories
</todos>
</update_todo_list>

---

**User:**

[update_todo_list] Result:
Todo list updated successfully.
<environment_details>
# VSCode Visible Files
.bob/rules-plan/AGENTS.md

# VSCode Open Tabs
.gitignore,apps/backend/.gitignore,apps/frontend/.gitignore,AGENTS.md,.bob/rules-code/AGENTS.md,.bob/rules-advanced/AGENTS.md,.bob/rules-ask/AGENTS.md,.bob/rules-plan/AGENTS.md

# Current Time
Current time in ISO 8601 UTC format: 2026-05-16T13:42:50.046Z
User time zone: Europe/Warsaw, UTC+2:00

# Current Cost
$1.02

# Review Exclusions
The following file patterns are excluded from code reviews:
- .vscode/**

# Current Mode
<slug>code</slug>
<name>💻 Code</name>
====

REMINDERS

Below is your current list of reminders for this task. Keep them updated as you progress.

| # | Content | Status |
|---|---------|--------|
| 1 | Check for existing AGENTS.md files in project root and .bob/ directories | Completed |
| 2 | Identify project stack and architecture | Completed |
| 3 | Extract build, test, and lint commands | Completed |
| 4 | Analyze code style and conventions from config files | Completed |
| 5 | Document project-specific patterns and utilities | Completed |
| 6 | Map testing setup and requirements | Completed |
| 7 | Create/update main AGENTS.md file | Completed |
| 8 | Create/update mode-specific AGENTS.md files in .bob/ directories | Completed |


IMPORTANT: When task status changes, remember to call the `update_todo_list` tool to update your progress.

</environment_details>

---

**Assistant:**

<attempt_completion>
<result>
Created comprehensive AGENTS.md documentation for the RiskTrace Control Tower monorepo:

**Main AGENTS.md** (project root)
- Monorepo structure with backend/frontend apps
- Backend commands using `uv` package manager
- Frontend commands using `npm`
- Docker Compose orchestration details
- Non-obvious patterns discovered:
  - Generated inputs package with CI validation
  - 6 microservices in single Python package
  - Batch calculation error tolerance for bank workflows
  - Database URL resolution with temp SQLite fallback
  - Reference data included via setuptools.package-data

**Mode-Specific Files** (.bob/rules-*/AGENTS.md)
- **rules-code**: Coding patterns including Decimal precision constants, import requirements, database pooling strategies, API proxy setup
- **rules-advanced**: Same as code mode plus MCP and Browser tool access
- **rules-ask**: Documentation context about monorepo structure, multiple services in one package, generated inputs versioning
- **rules-plan**: Architecture constraints including service ports, batch error handling philosophy, database pool strategies, frontend-backend integration requirements

All files focus exclusively on non-obvious, project-specific information discovered by reading the codebase, excluding standard practices and framework defaults.
</result>
</attempt_completion>

