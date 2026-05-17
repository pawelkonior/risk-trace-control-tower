export type Accent = "blue" | "purple" | "teal" | "green" | "amber";
export type DeltaDirection = "up" | "down";
export type AlertTone = "red" | "orange" | "amber" | "blue";
export type BriefingTone = "blue" | "purple" | "green" | "red" | "amber" | "teal";
export type LineageNodeTone =
  | "source"
  | "ingestion"
  | "validation"
  | "rule"
  | "calculation"
  | "reporting";

export type IconName =
  | "AlertCircle"
  | "BarChart3"
  | "Bell"
  | "BookOpenCheck"
  | "Calculator"
  | "CheckCircle2"
  | "ClipboardCheck"
  | "ClipboardList"
  | "CloudUpload"
  | "Database"
  | "FileArchive"
  | "FileClock"
  | "FileText"
  | "FolderDown"
  | "GitBranch"
  | "Layers3"
  | "LineChart"
  | "ListChecks"
  | "Network"
  | "Scale"
  | "ShieldCheck"
  | "Target"
  | "WalletCards";

export type AppUser = {
  initials: string;
  name: string;
  role: string;
  lastLogin: string;
};

export type SystemStatusItem = {
  label: string;
  value: string;
};

export type HomeCard = {
  view: "dashboard" | "lineage" | "briefing";
  description: string;
  metric: string;
  status: string;
  tone: "blue" | "teal" | "purple";
};

export type AppContext = {
  appName: string;
  environment: string;
  reportingDate: string;
  user: AppUser;
  systemStatus: SystemStatusItem[];
  notificationCount: number;
  comparisonLabel?: string;
  homeCards: HomeCard[];
  reportingCalendar: ReportingCalendar;
  helpItems: HelpItem[];
  userMenu: UserMenuItem[];
  notifications: NotificationItem[];
};

export type ReportingCalendar = {
  reportingDate: string;
  monthLabel: string;
  lockedReason: string;
  availableDates: string[];
};

export type HelpItem = {
  id: string;
  title: string;
  detail: string;
  actionId: string;
};

export type UserMenuItem = {
  id: string;
  label: string;
  detail: string;
  actionId: string;
};

export type NotificationItem = {
  id: string;
  title: string;
  detail: string;
  tone: "blue" | "amber" | "red" | "green";
  createdAt: string;
  read: boolean;
};

export type DashboardFilters = {
  period: string;
  scenario: string;
  businessUnit: string;
  currency: string;
};

export type DashboardFilterOptions = {
  periods: string[];
  scenarios: string[];
  businessUnits: string[];
  currencies: string[];
};

export type ApiMetric = {
  label: string;
  value: string;
  unit?: string;
  compareLabel: string;
  delta: string;
  deltaDirection: DeltaDirection;
  accent: Accent;
  icon: IconName;
  showInfoIcon?: boolean;
};

export type ApiCapitalSummary = {
  currency: string;
  rowsTop: Array<[string, string]>;
  ratios: Array<[string, string]>;
  minimumRequirement: string;
  capitalBuffer: string;
};

export type ApiTopExposure = {
  id: string;
  name: string;
  amount: string;
  pct: string;
  bar: number;
};

export type ApiExposureClass = {
  label: string;
  pct: string;
  amount: string;
  value: number;
  color: string;
};

export type ApiRwaTrendPoint = {
  label: string;
  value: number;
};

export type ApiRatingRwa = {
  rating: string;
  amount: string;
  pct: string;
  bar: number;
};

export type ApiCountryRwa = {
  country: string;
  amount: string;
  pct: string;
  color: string;
};

export type ApiAlert = {
  count: number;
  label: string;
  tone: AlertTone;
  icon: IconName;
};

export type RwaDashboardSnapshot = {
  generatedAt: string;
  asOfDate: string;
  currency: string;
  totalRwaAmount: string;
  filters: DashboardFilters;
  filterOptions: DashboardFilterOptions;
  metrics: ApiMetric[];
  capitalSummary: ApiCapitalSummary;
  topExposures: ApiTopExposure[];
  exposureClass: ApiExposureClass[];
  rwaTrend: ApiRwaTrendPoint[];
  ratingRwa: ApiRatingRwa[];
  countryRwa: ApiCountryRwa[];
  alerts: ApiAlert[];
};

export type ApiLineageTrace = {
  traceId: string;
  exposureId: string;
  sourceSystem: string;
  sourceRecordId: string;
  inputHash: string;
  ruleVersion: string;
  regulationReference: string;
  reportingDate: string;
  timestamp: string;
  rwaAmount: string;
};

export type ApiLineageNode = {
  id: string;
  layer: string;
  title: string;
  icon: IconName;
  tone: LineageNodeTone;
  details: Array<[string, string]>;
  status: "Success" | "Warning" | "Failed";
};

export type ApiTransformationStep = {
  step: number;
  service: string;
  description: string;
  inputRecords: string;
  outputRecords: string;
  duration: string;
  status: "Success" | "Warning" | "Failed";
  executedAt: string;
};

export type ApiLineageArtifact = {
  label: string;
  count: number;
  icon: IconName;
};

export type ApiLineageTotals = {
  duration: string;
  totalInputRecords: string;
  totalOutputRecords: string;
};

export type ApiLineageDirection = {
  title: string;
  value: string;
  meta: string[];
  buttonLabel: string;
  icon: IconName;
  actionId: string;
};

export type LineageTraceSnapshot = {
  trace: ApiLineageTrace;
  nodes: ApiLineageNode[];
  summary: Array<[string, string]>;
  transformationSteps: ApiTransformationStep[];
  artifacts: ApiLineageArtifact[];
  totals: ApiLineageTotals;
  directions: ApiLineageDirection[];
};

export type ApiBriefingKpi = {
  label: string;
  value: string;
  detail: string;
  icon: IconName;
  tone: BriefingTone;
};

export type ApiWaterfallItem = {
  label: string;
  axisLabel: string;
  tableLabel: string;
  base: number;
  opening: number;
  increase: number;
  decrease: number;
  closing: number;
  display: string;
  color: string;
};

export type ApiMovementDriver = {
  driver: string;
  impact: string;
  changePct: string;
  color: string;
};

export type ApiReviewPackStat = {
  label: string;
  value: string;
  detail: string;
  tone: "blue" | "red" | "amber" | "green" | "purple" | "teal";
};

export type ApiVarianceReviewItem = {
  label: string;
  value: string;
  share: string;
  width: number;
  color: string;
};

export type ApiControlChecklistItem = {
  label: string;
  status: string;
  tone: "success" | "warning" | "neutral";
};

export type ApiManualReviewInput = {
  label: string;
  tone: "blue" | "amber" | "purple" | "green" | "teal";
  actionId: string;
};

export type ApiManagementReviewPack = {
  tabs: string[];
  stats: ApiReviewPackStat[];
  varianceReviewItems: ApiVarianceReviewItem[];
  controlChecklist: ApiControlChecklistItem[];
  manualReviewInputs: ApiManualReviewInput[];
};

export type ApiRegulatoryWatchItem = {
  label: string;
  value: string;
  status: string;
};

export type ApiDataQualityFinding = {
  label: string;
  value: string;
  tone?: "negative" | "warning" | "neutral";
};

export type ApiSimulatorAction = {
  action: string;
  impact: string;
  confidence: "Low" | "Medium" | "High";
  owner: string;
  actionId: string;
};

export type ApiEvidenceItem = {
  label: string;
  value: string;
  icon: IconName;
  tone: BriefingTone;
  actionId: string;
};

export type ApiBoardPack = {
  title: string;
  description: string;
  icon: IconName;
  exportType: string;
};

export type CalculatedRwaRow = {
  assetId: string;
  entityClass: string;
  sector: string;
  exposureAmount: string;
  riskWeight: string;
  rating?: string | null;
  pd?: string | null;
  lgd?: string | null;
  maturityYears?: string | null;
  rwaAmount: string;
  approach: string;
};

export type BriefingSnapshot = {
  generatedAt: string;
  calculatedRwaRows?: CalculatedRwaRow[];
  kpis: ApiBriefingKpi[];
  movementAttribution: {
    waterfallData: ApiWaterfallItem[];
    movementDrivers: ApiMovementDriver[];
    totalChange: string;
    totalChangePct: string;
  };
  reviewPack: ApiManagementReviewPack;
  regulatoryWatch: ApiRegulatoryWatchItem[];
  dataQualityFindings: ApiDataQualityFinding[];
  simulatorActions: ApiSimulatorAction[];
  evidenceItems: ApiEvidenceItem[];
  boardPack: ApiBoardPack;
};

export type RwaAnalysisStatus = "COMPLETED" | "LOOP_LIMIT_REACHED" | "BLOCKED";

export type RwaAnalysisInputRecord = {
  asset_id: string;
  asset_class: string;
  sector: string;
  exposure_amount: string;
  risk_weight?: string;
  rating?: string;
  pd?: string;
  lgd?: string;
  maturity_years?: string;
  approach?: string;
};

export type RwaAnalysisOutputRecord = {
  asset_id: string;
  rwa_amount: string;
  exposure_amount?: string;
  risk_weight?: string;
  approach?: string;
};

export type RwaAnalysisRequest = {
  request_id: string;
  loop_limit?: number;
  materiality_threshold?: string;
  rwa_input_data: RwaAnalysisInputRecord[];
  rwa_output_results: RwaAnalysisOutputRecord[];
};

export type RwaReactStep = {
  phase: "inspect_state" | "select_tool" | "execute_tool" | "observe_result" | "emit_finding";
  tool_name?: string | null;
  action: string;
  observation: string;
};

export type RwaAgentFinding = {
  agent: string;
  kind: "data_quality" | "risk" | "validation" | "guardrail" | "observability";
  severity: "info" | "warning" | "critical";
  title: string;
  detail: string;
  evidence: string[];
  react_steps: RwaReactStep[];
};

export type RwaValidationFlag = {
  code: string;
  severity: "info" | "warning" | "critical";
  message: string;
  asset_id?: string | null;
  source_agent: string;
  requires_human_intervention: boolean;
};

export type RwaRecommendedAction = {
  id: string;
  label: string;
  owner: string;
  priority: "low" | "medium" | "high";
  completed: boolean;
  source_agent: string;
};

export type RwaQuantitativeValidation = {
  asset_id: string;
  expected_rwa_amount: string;
  reported_rwa_amount: string;
  variance_amount: string;
  variance_pct: string;
  passed: boolean;
};

export type RwaGuardrailResult = {
  stage: string;
  scanner: string;
  passed: boolean;
  blocked: boolean;
  risk_score: number;
  categories: string[];
  message: string;
};

export type RwaObservability = {
  langfuse_enabled: boolean;
  trace_id: string | null;
  callback_handler_attached: boolean;
  checkpointer: string;
  thread_id: string;
  prompt_usages: Array<{
    prompt_name: string;
    prompt_version: string;
    source: "local_fallback" | "langfuse";
    label: string | null;
    fetch_status: string;
    fetch_latency_ms: number | null;
  }>;
  evaluation_scores: Array<{
    name: string;
    value: number;
    comment: string;
  }>;
  guardrail_results: RwaGuardrailResult[];
  guardrail_block_count: number;
  pii_detected: boolean;
  prompt_injection_risk: number;
  node_transition_count: number;
  llm_call_count: number;
  tool_call_count: number;
  total_token_count: number;
};

export type RwaFinalCommentary = {
  status: RwaAnalysisStatus;
  consensus_reached: boolean;
  loop_count: number;
  generated_at: string;
  source_label: string;
  executive_summary: string;
  cro_view: string;
  cfo_view: string;
  data_quality_observations: RwaAgentFinding[];
  risk_observations: RwaAgentFinding[];
  quantitative_validation: RwaQuantitativeValidation[];
  recommended_actions: RwaRecommendedAction[];
  validation_flags: RwaValidationFlag[];
  source_agents: string[];
  observability: RwaObservability | null;
  messages: string[];
};

export type RwaCommentaryViews = {
  executive_summary: string;
  cro_view: string;
  cfo_view: string;
};

export type RwaAnalysisResponse = {
  api_version: "v1";
  service_version: string;
  request_id: string;
  run_id: string;
  status: RwaAnalysisStatus;
  graph_backend: string;
  final_commentary: RwaFinalCommentary;
  messages: string[];
  validation_flags: RwaValidationFlag[];
  agent_findings: RwaAgentFinding[];
  recommended_actions: RwaRecommendedAction[];
  commentary_views: RwaCommentaryViews;
  observability: RwaObservability;
};

export type UiActionPayload = Record<string, unknown>;

export type UiActionResult = {
  actionId: string;
  status: "accepted" | "completed" | "failed";
  message: string;
  category: string;
  jobId?: string | null;
  payload?: Record<string, unknown>;
  createdAt?: string;
};

export type ExportResult = {
  exportType: string;
  status: "queued" | "completed" | "failed";
  jobId: string;
  message: string;
  createdAt?: string;
  downloadUrl?: string;
};

export type SearchResult = {
  id: string;
  title: string;
  category: string;
  description: string;
  route: string;
};

export type SearchResponse = {
  query: string;
  results: SearchResult[];
};
