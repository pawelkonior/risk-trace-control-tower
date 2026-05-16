import { Download } from "lucide-react";

import { BriefingKpiStrip } from "../components/rwa-briefing/BriefingKpiStrip";
import {
  DataQualityFindingsCard,
  ManagementActionSimulatorCard,
  RegulatoryWatchCard,
} from "../components/rwa-briefing/BriefingInsightCards";
import { EvidenceTraceabilityCard } from "../components/rwa-briefing/EvidenceTraceabilityCard";
import { ManagementReviewPackCard } from "../components/rwa-briefing/ManagementReviewPackCard";
import { RwaMovementAttributionCard } from "../components/rwa-briefing/RwaMovementAttributionCard";
import {
  AiExecutiveCommentaryCard,
  useExecutiveCommentary,
} from "../components/rwa-briefing/AiExecutiveCommentaryCard";
import { AppShell } from "../components/rwa-dashboard/AppShell";
import { PageHeader } from "../components/rwa-dashboard/PageHeader";
import { Toast } from "../components/rwa-dashboard/Toast";
import { useAppContextData } from "../hooks/useAppContextData";
import { useRwaBriefingData } from "../hooks/useRwaBriefingData";
import { useToast } from "../hooks/useToast";
import { useUiActions } from "../hooks/useUiActions";
import type { AppView } from "../navigation";

type RwaIntelligenceBriefingPageProps = {
  onNavigate?: (view: AppView) => void;
};

export function RwaIntelligenceBriefingPage({ onNavigate }: RwaIntelligenceBriefingPageProps) {
  const { notify, toast } = useToast();
  const appContext = useAppContextData();
  const { runAction, runExport } = useUiActions(notify);
  const briefing = useRwaBriefingData();
  const { data } = briefing;
  const commentary = useExecutiveCommentary(data);

  return (
    <AppShell
      activeNav="RWA Intelligence Briefing"
      appContext={appContext.data}
      breadcrumbs={[
        { label: "Home", view: "home" },
        { label: "RWA Dashboard", view: "dashboard" },
        { label: "RWA Intelligence Briefing", active: true },
      ]}
      comparisonLabel={appContext.data?.comparisonLabel}
      onAction={runAction}
      onNavigate={onNavigate}
    >
      <div className="rwa-page briefing-page">
        <PageHeader
          title="RWA Intelligence Briefing"
          description="RWA movement overview with traceable drivers, data quality and audit evidence"
          actions={[
            {
              label: "Export Board Pack",
              icon: Download,
              variant: "primary",
              onClick: () => runExport(data?.boardPack.exportType ?? "board-pack"),
            },
          ]}
        />

        {briefing.error ? (
          <div className="api-status api-status-error">
            <span>Data unavailable</span>
            <strong>{briefing.error}</strong>
          </div>
        ) : null}

        {data ? (
          <>
            <BriefingKpiStrip kpis={data.kpis} />
            <AiExecutiveCommentaryCard
              data={data}
              error={commentary.error}
              isLoading={commentary.isLoading}
              onRegenerate={commentary.regenerate}
              response={commentary.response}
            />
            <div className="briefing-top-grid">
              <RwaMovementAttributionCard
                movementDrivers={data.movementAttribution.movementDrivers}
                totalChange={data.movementAttribution.totalChange}
                totalChangePct={data.movementAttribution.totalChangePct}
                waterfallData={data.movementAttribution.waterfallData}
              />
              <ManagementReviewPackCard data={data.reviewPack} onAction={runAction} />
            </div>
            <div className="briefing-mid-grid">
              <RegulatoryWatchCard data={data.regulatoryWatch} onAction={runAction} />
              <DataQualityFindingsCard data={data.dataQualityFindings} onAction={runAction} />
              <ManagementActionSimulatorCard data={data.simulatorActions} onAction={runAction} />
            </div>
            <EvidenceTraceabilityCard
              boardPack={data.boardPack}
              evidenceItems={data.evidenceItems}
              onAction={runAction}
              onExport={runExport}
            />
          </>
        ) : null}
        <Toast message={toast} />
      </div>
    </AppShell>
  );
}
