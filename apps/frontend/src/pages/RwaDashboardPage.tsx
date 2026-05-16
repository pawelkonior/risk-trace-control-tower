import { Download, ShieldCheck } from "lucide-react";
import { useState } from "react";

import type { DashboardFilters } from "../api/types";
import { AppShell } from "../components/rwa-dashboard/AppShell";
import { AlertsPanel } from "../components/rwa-dashboard/AlertsPanel";
import { CapitalSummaryCard } from "../components/rwa-dashboard/CapitalSummaryCard";
import { CountryMapCard } from "../components/rwa-dashboard/CountryMapCard";
import { ExposureDonutCard } from "../components/rwa-dashboard/ExposureDonutCard";
import { FilterBar } from "../components/rwa-dashboard/FilterBar";
import { MetricCard } from "../components/rwa-dashboard/MetricCard";
import { PageHeader } from "../components/rwa-dashboard/PageHeader";
import { RatingBarsCard } from "../components/rwa-dashboard/RatingBarsCard";
import { RwaTrendCard } from "../components/rwa-dashboard/RwaTrendCard";
import { Toast } from "../components/rwa-dashboard/Toast";
import { TopExposuresCard } from "../components/rwa-dashboard/TopExposuresCard";
import { useAppContextData } from "../hooks/useAppContextData";
import { useRwaDashboardData } from "../hooks/useRwaDashboardData";
import { useToast } from "../hooks/useToast";
import { useUiActions } from "../hooks/useUiActions";
import type { AppView } from "../navigation";

type RwaDashboardPageProps = {
  onNavigate?: (view: AppView) => void;
};

export function RwaDashboardPage({ onNavigate }: RwaDashboardPageProps) {
  const { notify, toast } = useToast();
  const appContext = useAppContextData();
  const { runAction, runExport } = useUiActions(notify);
  const [filters, setFilters] = useState<DashboardFilters | undefined>();
  const dashboard = useRwaDashboardData(filters);
  const { data } = dashboard;
  const activeFilters = filters ?? data?.filters;
  const dashboardRenderKey = data
    ? [
        data.generatedAt,
        data.filters.period,
        data.filters.scenario,
        data.filters.businessUnit,
        data.filters.currency,
      ].join("|")
    : "dashboard-empty";
  const isRefreshingDashboard = dashboard.isLoading && Boolean(data);

  return (
    <AppShell
      activeNav="RWA Dashboard"
      appContext={appContext.data}
      breadcrumbs={[
        { label: "Home", view: "home" },
        { label: "RWA Dashboard", active: true },
      ]}
      onAction={runAction}
      onNavigate={onNavigate}
    >
      <div className="rwa-page">
        <PageHeader
          title="RWA Dashboard"
          description="Overview of Risk-Weighted Assets and key capital metrics"
          actions={[
            {
              label: "Export Report",
              icon: Download,
              onClick: () => runExport("dashboard-report", { asOfDate: data?.asOfDate }),
            },
            {
              label: "Request Evidence Pack",
              icon: ShieldCheck,
              variant: "primary",
              onClick: () =>
                runAction("dashboard.evidence-pack.open", { asOfDate: data?.asOfDate }),
            },
          ]}
        />
        {data && activeFilters ? (
          <FilterBar
            filterOptions={data.filterOptions}
            filters={activeFilters}
            onAction={runAction}
            onFiltersChange={setFilters}
          />
        ) : null}
        {dashboard.error ? (
          <div className="api-status api-status-error">
            <span>Data unavailable</span>
            <strong>{dashboard.error}</strong>
          </div>
        ) : null}
        {dashboard.isLoading && !data ? <DashboardLoadingState /> : null}
        {data ? (
          <div
            aria-busy={dashboard.isLoading}
            className={`dashboard-data-shell${isRefreshingDashboard ? " is-refreshing" : ""}`}
          >
            <div className="dashboard-grid" key={dashboardRenderKey}>
              <div className="dashboard-left">
                <div className="metrics-row">
                  {data.metrics.map((metric) => (
                    <MetricCard key={metric.label} {...metric} />
                  ))}
                </div>
                <div className="chart-row-primary">
                  <ExposureDonutCard data={data.exposureClass} totalAmount={data.totalRwaAmount} />
                  <RwaTrendCard data={data.rwaTrend} />
                </div>
                <div className="chart-row-secondary">
                  <RatingBarsCard data={data.ratingRwa} />
                  <CountryMapCard data={data.countryRwa} totalAmount={data.totalRwaAmount} />
                </div>
                <AlertsPanel data={data.alerts} />
              </div>
              <aside className="side-rail">
                <CapitalSummaryCard data={data.capitalSummary} />
                <TopExposuresCard data={data.topExposures} />
              </aside>
            </div>
            {isRefreshingDashboard ? <DashboardRefreshOverlay /> : null}
          </div>
        ) : null}
        <Toast message={toast} />
      </div>
    </AppShell>
  );
}

function DashboardLoadingState() {
  return (
    <div className="dashboard-loading-state" aria-live="polite">
      <span className="dashboard-loader" aria-hidden="true" />
      <strong>Loading dashboard data</strong>
    </div>
  );
}

function DashboardRefreshOverlay() {
  return (
    <div className="dashboard-refresh-overlay" aria-live="polite">
      <div className="dashboard-refresh-indicator">
        <span className="dashboard-loader" aria-hidden="true" />
        <strong>Updating dashboard</strong>
      </div>
    </div>
  );
}
