import { ArrowRight, Copy, Download } from "lucide-react";

import type { ApiLineageTrace } from "../../api/types";
import type { LineageArtifact, LineageDirection } from "../../hooks/useRwaLineageData";
import { Card } from "../rwa-dashboard/Card";

type LineageSideRailProps = {
  artifacts: LineageArtifact[];
  directions: LineageDirection[];
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onExport?: (exportType: string, payload?: Record<string, unknown>) => void;
  trace: ApiLineageTrace;
};

export function LineageSideRail({
  artifacts,
  directions,
  onAction,
  onExport,
  trace,
}: LineageSideRailProps) {
  return (
    <aside className="lineage-side-rail">
      <LineageDetailsCard onAction={onAction} trace={trace} />
      <LineageArtifactsCard
        artifacts={artifacts}
        onAction={onAction}
        onExport={onExport}
        traceId={trace.traceId}
      />
      {directions.map((direction) => (
        <LineageDirectionCard direction={direction} key={direction.title} onAction={onAction} />
      ))}
    </aside>
  );
}

function LineageDetailsCard({
  onAction,
  trace,
}: {
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  trace: ApiLineageTrace;
}) {
  const rows = [
    ["Calculation Trace ID", trace.traceId, true],
    ["Exposure ID", trace.exposureId, true],
    ["Source System", trace.sourceSystem],
    ["Source Record ID", trace.sourceRecordId],
    ["Input Hash (SHA-256)", trace.inputHash, true],
    ["Rule Version", trace.ruleVersion],
    ["Regulation Reference", trace.regulationReference],
    ["Reporting Date", trace.reportingDate],
    ["Calculation Timestamp", trace.timestamp],
    ["RWA Amount", trace.rwaAmount],
  ] as const;

  return (
    <Card className="lineage-side-card">
      <h3>Lineage Details</h3>
      <dl className="lineage-details-list">
        {rows.map(([label, value, copyable]) => (
          <div key={label}>
            <dt>{label}</dt>
            <dd>
              <span title={value}>{value}</span>
              {copyable ? (
                <button
                  aria-label={`Copy ${label}`}
                  className="copy-button"
                  type="button"
                  onClick={() => {
                    void navigator.clipboard?.writeText(value).catch(() => undefined);
                    onAction?.("clipboard.copy", { label, value });
                  }}
                >
                  <Copy size={13} />
                </button>
              ) : null}
            </dd>
          </div>
        ))}
      </dl>
    </Card>
  );
}

function LineageArtifactsCard({
  artifacts,
  onAction,
  onExport,
  traceId,
}: {
  artifacts: LineageArtifact[];
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onExport?: (exportType: string, payload?: Record<string, unknown>) => void;
  traceId: string;
}) {
  return (
    <Card className="lineage-side-card artifacts-card">
      <h3>Data Lineage Artifacts</h3>
      <div className="artifact-list">
        {artifacts.map(({ count, icon: Icon, label }) => (
          <button
            className="artifact-row"
            key={label}
            type="button"
            onClick={() => onAction?.("lineage.artifact.open", { label, traceId })}
          >
            <span>
              <Icon size={14} />
              {label}
            </span>
            <strong>{count}</strong>
          </button>
        ))}
      </div>
      <button
        className="button button-secondary full-width-button"
        type="button"
        onClick={() => onExport?.("lineage-artifacts", { traceId })}
      >
        <Download size={14} />
        <span>Download All Artifacts</span>
      </button>
    </Card>
  );
}

function LineageDirectionCard({
  direction,
  onAction,
}: {
  direction: LineageDirection;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
}) {
  const Icon = direction.icon;

  return (
    <Card className="lineage-side-card direction-card">
      <h3>{direction.title}</h3>
      <div className="direction-entity">
        <div className="direction-icon">
          <Icon size={22} strokeWidth={1.8} />
        </div>
        <div>
          <strong>{direction.value}</strong>
          {direction.meta.map((item) => (
            <span key={item}>{item}</span>
          ))}
        </div>
      </div>
      <button
        className="button button-secondary full-width-button"
        type="button"
        onClick={() => onAction?.(direction.actionId, { title: direction.title })}
      >
        <span>{direction.buttonLabel}</span>
        <ArrowRight size={14} />
      </button>
    </Card>
  );
}
