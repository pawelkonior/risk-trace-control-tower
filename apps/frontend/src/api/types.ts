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

export type BriefingSnapshot = {
  generatedAt: string;
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
