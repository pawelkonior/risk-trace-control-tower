import { ArrowRight, CheckCircle2, Info } from "lucide-react";
import type { ReactNode } from "react";

import type {
  ApiDataQualityFinding,
  ApiRegulatoryWatchItem,
  ApiSimulatorAction,
} from "../../api/types";
import { Card } from "../rwa-dashboard/Card";
import { StatusBadge } from "../rwa-dashboard/StatusBadge";

const approvalTooltip = "Requires approval";

type BriefingInsightCardsProps = {
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
};

export function RegulatoryWatchCard({
  data,
}: BriefingInsightCardsProps & { data: ApiRegulatoryWatchItem[] }) {
  return (
    <Card className="briefing-card briefing-small-card">
      <BriefingPanelHeader title="Regulatory Watch" />
      <div className="reg-watch-list">
        {data.map(({ label, value, status }) => (
          <div className="reg-watch-row" key={label}>
            <CheckCircle2 size={15} />
            <span>{label}</span>
            <strong>{value}</strong>
            <StatusBadge>{status}</StatusBadge>
          </div>
        ))}
      </div>
      <ApprovalTooltip block>
        <button className="button button-secondary briefing-card-action" disabled type="button">
          <span>View Regulatory Context</span>
          <ArrowRight size={14} />
        </button>
      </ApprovalTooltip>
    </Card>
  );
}

export function DataQualityFindingsCard({
  data,
}: BriefingInsightCardsProps & { data: ApiDataQualityFinding[] }) {
  return (
    <Card className="briefing-card briefing-small-card">
      <BriefingPanelHeader title="Data Quality Findings" />
      <div className="dq-list">
        {data.map(({ label, tone, value }, index) => (
          <div className="dq-row" key={label}>
            <span>{label}</span>
            <strong className={toneClass(tone, index)}>{value}</strong>
          </div>
        ))}
      </div>
      <ApprovalTooltip block>
        <button className="button button-secondary briefing-card-action" disabled type="button">
          <span>View Data Quality Report</span>
          <ArrowRight size={14} />
        </button>
      </ApprovalTooltip>
    </Card>
  );
}

export function ManagementActionSimulatorCard({
  data,
}: BriefingInsightCardsProps & { data: ApiSimulatorAction[] }) {
  return (
    <Card className="briefing-card action-simulator-card">
      <div className="briefing-card-header">
        <BriefingPanelHeader title="Management Action Simulator" />
        <ApprovalTooltip>
          <button className="button button-secondary compact-button" disabled type="button">
            Simulate All
          </button>
        </ApprovalTooltip>
      </div>
      <div className="simulator-table-wrap">
        <table className="simulator-table">
          <thead>
            <tr>
              <th>Action</th>
              <th>Estimated RWA Impact</th>
              <th>Confidence</th>
              <th>Owner</th>
            </tr>
          </thead>
          <tbody>
            {data.map(({ action, confidence, impact, owner }) => (
              <tr key={action}>
                <td>
                  <ApprovalTooltip inline>
                    <button className="table-link-button" disabled type="button">
                      {action}
                    </button>
                  </ApprovalTooltip>
                </td>
                <td>{impact}</td>
                <td>
                  <span className={`confidence-pill confidence-${confidence.toLowerCase()}`}>
                    {confidence}
                  </span>
                </td>
                <td>{owner}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <ApprovalTooltip block>
        <button className="button button-secondary briefing-card-action" disabled type="button">
          <span>Create Action Items</span>
          <ArrowRight size={14} />
        </button>
      </ApprovalTooltip>
    </Card>
  );
}

function ApprovalTooltip({
  block = false,
  children,
  inline = false,
}: {
  block?: boolean;
  children: ReactNode;
  inline?: boolean;
}) {
  const className = `approval-tooltip${block ? " approval-tooltip-block" : ""}${
    inline ? " approval-tooltip-inline" : ""
  }`;

  return (
    <span className={className} data-tooltip={approvalTooltip} tabIndex={0}>
      {children}
    </span>
  );
}

function toneClass(tone: ApiDataQualityFinding["tone"], index: number) {
  if (tone === "negative") {
    return "negative";
  }
  if (tone === "warning") {
    return "warning-text";
  }
  return index === 0 ? "negative" : index < 4 ? "warning-text" : "negative";
}

function BriefingPanelHeader({ title }: { title: string }) {
  return (
    <div className="briefing-panel-title">
      <h3>{title}</h3>
      <Info size={13} />
    </div>
  );
}
