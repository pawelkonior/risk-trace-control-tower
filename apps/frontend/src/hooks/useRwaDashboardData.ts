import { fetchRwaDashboardSnapshot } from "../api/rwaApi";
import type {
  Accent,
  AlertTone,
  ApiCapitalSummary,
  ApiCountryRwa,
  ApiExposureClass,
  ApiRatingRwa,
  ApiRwaTrendPoint,
  ApiTopExposure,
  DashboardFilterOptions,
  DashboardFilters,
  DeltaDirection,
  RwaDashboardSnapshot,
} from "../api/types";
import { hydrateIcon, type HydratedIcon } from "./iconHydration";
import { useApiResource } from "./useApiResource";

export type DashboardMetric = {
  label: string;
  value: string;
  unit?: string;
  compareLabel: string;
  delta: string;
  deltaDirection: DeltaDirection;
  accent: Accent;
  icon: HydratedIcon;
  showInfoIcon?: boolean;
};

export type DashboardAlert = {
  count: number;
  label: string;
  tone: AlertTone;
  icon: HydratedIcon;
};

export type RwaDashboardData = {
  metrics: DashboardMetric[];
  capitalSummary: ApiCapitalSummary;
  topExposures: ApiTopExposure[];
  exposureClass: ApiExposureClass[];
  rwaTrend: ApiRwaTrendPoint[];
  ratingRwa: ApiRatingRwa[];
  countryRwa: ApiCountryRwa[];
  alerts: DashboardAlert[];
  asOfDate: string;
  filters: DashboardFilters;
  filterOptions: DashboardFilterOptions;
  generatedAt?: string;
  totalRwaAmount: string;
};

export function useRwaDashboardData(filters?: DashboardFilters) {
  return useApiResource<RwaDashboardData>(
    (signal) =>
      Promise.all([
        fetchRwaDashboardSnapshot(filters, signal).then(hydrateDashboardSnapshot),
        waitForDashboardFilterDelay(filters, signal),
      ]).then(([data]) => data),
    [filters?.period, filters?.scenario, filters?.businessUnit, filters?.currency],
  );
}

function waitForDashboardFilterDelay(filters: DashboardFilters | undefined, signal: AbortSignal) {
  if (!filters) {
    return Promise.resolve();
  }

  const delayMs = 1_000 + Math.floor(Math.random() * 2_001);
  return new Promise<void>((resolve, reject) => {
    const timeoutId = window.setTimeout(resolve, delayMs);

    signal.addEventListener(
      "abort",
      () => {
        window.clearTimeout(timeoutId);
        reject(new DOMException("Dashboard refresh aborted", "AbortError"));
      },
      { once: true },
    );
  });
}

function hydrateDashboardSnapshot(snapshot: RwaDashboardSnapshot): RwaDashboardData {
  return {
    metrics: snapshot.metrics.map((metric) => ({
      ...metric,
      icon: hydrateIcon(metric.icon),
    })),
    capitalSummary: snapshot.capitalSummary,
    topExposures: snapshot.topExposures,
    exposureClass: snapshot.exposureClass,
    rwaTrend: snapshot.rwaTrend,
    ratingRwa: snapshot.ratingRwa,
    countryRwa: snapshot.countryRwa,
    alerts: snapshot.alerts.map((alert) => ({
      ...alert,
      icon: hydrateIcon(alert.icon),
    })),
    asOfDate: snapshot.asOfDate,
    filters: snapshot.filters,
    filterOptions: snapshot.filterOptions,
    generatedAt: snapshot.generatedAt,
    totalRwaAmount: snapshot.totalRwaAmount,
  };
}
