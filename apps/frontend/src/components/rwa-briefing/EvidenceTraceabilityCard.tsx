import { Download } from "lucide-react";

import type { BoardPack, EvidenceItem } from "../../hooks/useRwaBriefingData";
import { Card } from "../rwa-dashboard/Card";

type EvidenceTraceabilityCardProps = {
  boardPack: BoardPack;
  evidenceItems: EvidenceItem[];
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
  onExport?: (exportType: string, payload?: Record<string, unknown>) => void;
};

export function EvidenceTraceabilityCard({
  boardPack,
  evidenceItems,
  onAction,
  onExport,
}: EvidenceTraceabilityCardProps) {
  const BoardIcon = boardPack.icon;

  return (
    <div className="briefing-bottom-grid">
      <Card className="briefing-card evidence-card">
        <h3>Evidence & Traceability</h3>
        <div className="evidence-list">
          {evidenceItems.map(({ actionId, icon: Icon, label, tone, value }) => (
            <button
              className="evidence-item"
              key={label}
              type="button"
              onClick={() => onAction?.(actionId, { label })}
            >
              <span className={`briefing-kpi-icon briefing-tone-${tone}`}>
                <Icon size={18} />
              </span>
              <span>
                <strong>{label}</strong>
                <em>{value}</em>
              </span>
            </button>
          ))}
        </div>
      </Card>

      <Card className="briefing-card board-pack-card">
        <div className="board-pack-heading">
          <span className="briefing-kpi-icon briefing-tone-purple">
            <BoardIcon size={18} />
          </span>
          <div>
            <h3>{boardPack.title}</h3>
            <p>{boardPack.description}</p>
          </div>
        </div>
        <button
          className="button button-secondary full-width-button"
          type="button"
          onClick={() => onExport?.(boardPack.exportType)}
        >
          <Download size={14} />
          <span>Export Board Pack</span>
        </button>
      </Card>
    </div>
  );
}
