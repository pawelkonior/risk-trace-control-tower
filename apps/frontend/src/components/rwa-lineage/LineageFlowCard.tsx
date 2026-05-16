import { Fragment, useState } from "react";
import { CircleCheck, Info, SlidersHorizontal } from "lucide-react";

import type { LineageNode } from "../../hooks/useRwaLineageData";
import { Card } from "../rwa-dashboard/Card";
import { StatusBadge } from "../rwa-dashboard/StatusBadge";

type LineageFlowCardProps = {
  nodes: LineageNode[];
};

const lineageToneLabels: Record<LineageNode["tone"], string> = {
  source: "Source",
  ingestion: "Ingestion",
  validation: "Validation",
  rule: "Rule",
  calculation: "Calculation",
  reporting: "Reporting",
};

const statusLegend = ["Success", "Warning", "Failed"] as const;

function statusTone(status: LineageNode["status"]): "success" | "warning" | "danger" {
  if (status === "Warning") {
    return "warning";
  }
  if (status === "Failed") {
    return "danger";
  }
  return "success";
}

export function LineageFlowCard({ nodes }: LineageFlowCardProps) {
  const [view, setView] = useState<"graph" | "table">("graph");
  const [showLegend, setShowLegend] = useState(false);
  const nodeTones = Array.from(new Set(nodes.map((node) => node.tone)));

  return (
    <Card className="lineage-flow-card">
      <div className="lineage-card-toolbar">
        <div className="lineage-title">
          <h3>Lineage Flow</h3>
          <Info size={13} />
        </div>
        <div className="lineage-view-controls">
          <span>View:</span>
          <div className="segmented-control">
            <button
              className={view === "graph" ? "active" : ""}
              type="button"
              onClick={() => setView("graph")}
            >
              Graph
            </button>
            <button
              className={view === "table" ? "active" : ""}
              type="button"
              onClick={() => setView("table")}
            >
              Table
            </button>
          </div>
          <button
            aria-expanded={showLegend}
            className={`button button-secondary lineage-legend-button${
              showLegend ? " active" : ""
            }`}
            type="button"
            onClick={() => setShowLegend((current) => !current)}
          >
            <SlidersHorizontal size={14} />
            <span>Legend</span>
          </button>
        </div>
      </div>

      {showLegend ? <LineageLegend nodeTones={nodeTones} /> : null}

      {view === "graph" ? <LineageGraph nodes={nodes} /> : <LineageNodeTable nodes={nodes} />}
    </Card>
  );
}

function LineageLegend({ nodeTones }: { nodeTones: Array<LineageNode["tone"]> }) {
  return (
    <div className="lineage-legend-panel" aria-label="Lineage flow legend">
      <div className="lineage-legend-group">
        <span>Node type</span>
        <div className="lineage-legend-items">
          {nodeTones.map((tone) => (
            <span className="lineage-legend-item" key={tone}>
              <i className={`lineage-legend-swatch lineage-legend-${tone}`} />
              {lineageToneLabels[tone]}
            </span>
          ))}
        </div>
      </div>
      <div className="lineage-legend-group">
        <span>Status</span>
        <div className="lineage-legend-items">
          {statusLegend.map((status) => (
            <span className="lineage-legend-item" key={status}>
              <StatusBadge tone={statusTone(status)}>{status}</StatusBadge>
            </span>
          ))}
        </div>
      </div>
    </div>
  );
}

function LineageGraph({ nodes }: { nodes: LineageNode[] }) {
  return (
    <div className="lineage-flow-grid" aria-label="Calculation lineage graph">
      {nodes.map((node, index) => (
        <Fragment key={node.id}>
          <LineageNodeCard node={node} />
          {index < nodes.length - 1 ? (
            <div className="flow-connector" aria-hidden="true">
              <span />
              <CircleCheck size={17} />
              <span />
            </div>
          ) : null}
        </Fragment>
      ))}
    </div>
  );
}

function LineageNodeCard({
  className = "",
  node,
}: {
  className?: string;
  node: LineageNode;
}) {
  const Icon = node.icon;

  return (
    <article className={`lineage-node lineage-node-${node.tone} ${className}`}>
      <div className="lineage-node-heading">
        <div className="lineage-node-icon">
          <Icon size={22} strokeWidth={1.8} />
        </div>
        <div>
          <span>{node.layer}</span>
          <strong>{node.title}</strong>
        </div>
      </div>
      <dl>
        {node.details.map(([label, value]) => (
          <div key={label}>
            <dt>{label}:</dt>
            <dd title={value}>{value}</dd>
          </div>
        ))}
      </dl>
      <StatusBadge tone={statusTone(node.status)}>{node.status}</StatusBadge>
    </article>
  );
}

function LineageNodeTable({ nodes }: { nodes: LineageNode[] }) {
  return (
    <div className="lineage-node-table-wrap">
      <table className="lineage-node-table">
        <thead>
          <tr>
            <th>Layer</th>
            <th>Service</th>
            <th>Status</th>
            <th>Primary Evidence</th>
          </tr>
        </thead>
        <tbody>
          {nodes.map((node) => (
            <tr key={node.id}>
              <td>{node.layer}</td>
              <td>{node.title}</td>
              <td>
                <StatusBadge tone={statusTone(node.status)}>{node.status}</StatusBadge>
              </td>
              <td>{node.details[0]?.[1]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
