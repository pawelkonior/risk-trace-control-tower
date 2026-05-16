import { Download } from "lucide-react";

import { AppShell } from "../components/rwa-dashboard/AppShell";
import { PageHeader } from "../components/rwa-dashboard/PageHeader";
import { Toast } from "../components/rwa-dashboard/Toast";
import { LineageFlowCard } from "../components/rwa-lineage/LineageFlowCard";
import { LineageSideRail } from "../components/rwa-lineage/LineageSideRail";
import { LineageSummaryCard } from "../components/rwa-lineage/LineageSummaryCard";
import { TransformationStepsCard } from "../components/rwa-lineage/TransformationStepsCard";
import { useAppContextData } from "../hooks/useAppContextData";
import { useRwaLineageData } from "../hooks/useRwaLineageData";
import { useToast } from "../hooks/useToast";
import { useUiActions } from "../hooks/useUiActions";
import type { AppView } from "../navigation";

type DataLineagePageProps = {
  onNavigate?: (view: AppView) => void;
};

export function DataLineagePage({ onNavigate }: DataLineagePageProps) {
  const { notify, toast } = useToast();
  const appContext = useAppContextData();
  const { runAction, runExport } = useUiActions(notify);
  const traceId = getTraceId();
  const lineage = useRwaLineageData(traceId);
  const { data } = lineage;

  return (
    <AppShell
      activeNav="Data Lineage"
      appContext={appContext.data}
      breadcrumbs={[
        { label: "Home", view: "home" },
        { label: "Data Lineage", active: true },
      ]}
      onAction={runAction}
      onNavigate={onNavigate}
      showSearch
    >
      <div className="rwa-page lineage-page">
        <PageHeader
          title="Data Lineage"
          description="End-to-end data flow and transformation for RWA calculation"
          actions={[
            {
              label: "Export Lineage Report",
              icon: Download,
              variant: "primary",
              onClick: () =>
                runExport("lineage-report", { traceId: data?.trace.traceId ?? traceId }),
            },
          ]}
        />

        {lineage.error ? (
          <div className="api-status api-status-error">
            <span>Data unavailable</span>
            <strong>{lineage.error}</strong>
          </div>
        ) : null}

        {data ? (
          <div className="lineage-layout">
            <div className="lineage-main-column">
              <LineageSummaryCard summary={data.summary} />
              <LineageFlowCard nodes={data.nodes} />
              <TransformationStepsCard steps={data.transformationSteps} totals={data.totals} />
            </div>
            <LineageSideRail
              artifacts={data.artifacts}
              directions={data.directions}
              onAction={runAction}
              onExport={runExport}
              trace={data.trace}
            />
          </div>
        ) : null}
        <Toast message={toast} />
      </div>
    </AppShell>
  );
}

function getTraceId() {
  const params = new URLSearchParams(window.location.search);
  return params.get("traceId") ?? "current";
}
