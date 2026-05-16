import { useState } from "react";
import { ArrowRight, CheckCircle2, CircleAlert, ClipboardList, Info } from "lucide-react";

import type { ManagementReviewPack } from "../../hooks/useRwaBriefingData";
import { Card } from "../rwa-dashboard/Card";
import { StatusBadge } from "../rwa-dashboard/StatusBadge";

type ManagementReviewPackCardProps = {
  data: ManagementReviewPack;
  onAction?: (actionId: string, payload?: Record<string, unknown>) => void;
};

export function ManagementReviewPackCard({ data, onAction }: ManagementReviewPackCardProps) {
  const [tab, setTab] = useState(data.tabs[0] ?? "Summary");

  return (
    <Card className="briefing-card review-pack-card">
      <div className="briefing-card-header review-pack-header">
        <div className="review-pack-title">
          <ClipboardList size={19} />
          <h3>Management Review Pack</h3>
          <Info size={13} />
        </div>
        <div aria-label="Review pack sections" className="review-pack-tabs" role="tablist">
          {data.tabs.map((item) => (
            <button
              aria-selected={tab === item}
              className={tab === item ? "active" : ""}
              key={item}
              role="tab"
              type="button"
              onClick={() => setTab(item)}
            >
              {item}
            </button>
          ))}
        </div>
      </div>

      <div className="review-pack-body">
        {tab === "Summary" ? (
          <>
            <div className="review-stat-grid">
              {data.stats.map(({ detail, label, tone, value }) => (
                <div className="review-stat-card" key={label}>
                  <span className={`review-status-dot review-tone-${tone}`} />
                  <span>{label}</span>
                  <strong>{value}</strong>
                  <em>{detail}</em>
                </div>
              ))}
            </div>
            <section className="review-panel variance-panel">
              <h4>Variance Review</h4>
              <p>Top movements requiring management review</p>
              <div className="variance-list">
                {data.varianceReviewItems.map(({ color, label, share, value, width }) => (
                  <div className="variance-row" key={label}>
                    <div className="variance-row-header">
                      <span>
                        <i style={{ backgroundColor: color }} />
                        {label}
                      </span>
                      <strong>{value}</strong>
                    </div>
                    <div className="variance-row-metric">
                      <span>
                        <b style={{ width: `${width}%`, backgroundColor: color }} />
                      </span>
                      <em>{share}</em>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        ) : null}

        {tab === "Controls" ? (
          <section className="review-panel controls-panel">
            <h4>Control Checklist</h4>
            <p>Rules and owner confirmations</p>
            <div className="control-list">
              {data.controlChecklist.map(({ label, status, tone }) => {
                const Icon = tone === "warning" || tone === "neutral" ? CircleAlert : CheckCircle2;

                return (
                  <div className="control-row" key={label}>
                    <Icon className={`control-icon control-icon-${tone}`} size={15} />
                    <span>{label}</span>
                    <StatusBadge tone={tone}>{status}</StatusBadge>
                  </div>
                );
              })}
            </div>
          </section>
        ) : null}

        {tab === "Sign-off" ? (
          <section className="review-panel signoff-panel">
            <h4>Sign-off Readiness</h4>
            <p>Inputs prepared for management review and board pack release</p>
            <div className="signoff-grid">
              {data.manualReviewInputs.map(({ label, tone }) => (
                <div className={`signoff-card manual-chip-${tone}`} key={label}>
                  <strong>{label}</strong>
                  <span>Ready for review</span>
                </div>
              ))}
            </div>
            <div className="signoff-control-list">
              {data.controlChecklist.map(({ label, status, tone }) => (
                <div className="control-row" key={label}>
                  <span>{label}</span>
                  <StatusBadge tone={tone}>{status}</StatusBadge>
                </div>
              ))}
            </div>
          </section>
        ) : null}

        <div className="manual-review-strip">
          <strong>{tab === "Sign-off" ? "Sign-off inputs" : "Manual review inputs"}</strong>
          <div className="manual-review-chips">
            {data.manualReviewInputs.map(({ actionId, label, tone }) => (
              <button
                className={`manual-chip manual-chip-${tone}`}
                key={label}
                type="button"
                onClick={() => onAction?.(actionId, { label, tab })}
              >
                {label}
              </button>
            ))}
          </div>
          <button
            className="button button-secondary review-open-button"
            type="button"
            onClick={() => onAction?.("briefing.review.open", { tab })}
          >
            <span>Open Review</span>
            <ArrowRight size={14} />
          </button>
        </div>
      </div>
    </Card>
  );
}
