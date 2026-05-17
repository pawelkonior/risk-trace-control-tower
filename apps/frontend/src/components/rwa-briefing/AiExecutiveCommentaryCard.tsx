import {
  AlertTriangle,
  CheckCircle2,
  Info,
  ListChecks,
  RotateCcw,
  ShieldCheck,
} from "lucide-react";
import { useEffect, useMemo, useState, type ReactNode } from "react";

import { postRwaExecutiveCommentary } from "../../api/rwaApi";
import type {
  CalculatedRwaRow,
  RwaAnalysisRequest,
  RwaAnalysisResponse,
  RwaAnalysisStatus,
  RwaRecommendedAction,
} from "../../api/types";
import type { RwaBriefingData } from "../../hooks/useRwaBriefingData";
import { Card } from "../rwa-dashboard/Card";
import { StatusBadge } from "../rwa-dashboard/StatusBadge";

type CommentaryTab = "executive_summary" | "cro_view" | "cfo_view";

type AiExecutiveCommentaryCardProps = {
  data: RwaBriefingData;
  error: string | null;
  isLoading: boolean;
  onRegenerate: () => void;
  response: RwaAnalysisResponse | null;
};

const tabLabels: Record<CommentaryTab, string> = {
  executive_summary: "Executive Summary",
  cro_view: "CRO View",
  cfo_view: "CFO View",
};

export function AiExecutiveCommentaryCard({
  data,
  error,
  isLoading,
  onRegenerate,
  response,
}: AiExecutiveCommentaryCardProps) {
  const [activeTab, setActiveTab] = useState<CommentaryTab>("executive_summary");
  const commentary = response?.final_commentary ?? null;
  const status = response?.status ?? null;
  const isBlocked = status === "BLOCKED";
  const hasCalculatedRows = Boolean(data.calculatedRwaRows?.length);
  const viewText = commentary ? commentary[activeTab] : "";

  return (
    <Card className="briefing-card ai-commentary-card">
      <div className="ai-commentary-header">
        <div className="briefing-panel-title">
          <ShieldCheck size={15} />
          <h3>AI Executive Commentary</h3>
        </div>
        <div className="ai-commentary-actions">
          {status ? <StatusBadge tone={statusTone(status)}>{status}</StatusBadge> : null}
          <button
            className="button button-secondary compact-button"
            disabled={isLoading || !hasCalculatedRows}
            onClick={onRegenerate}
            type="button"
          >
            <RotateCcw size={14} />
            <span>Regenerate</span>
          </button>
        </div>
      </div>

      {commentary ? (
        <div className="ai-commentary-meta">
          <span>{commentary.source_label}</span>
          <span>{formatDate(commentary.generated_at)}</span>
          {response ? <span>{response.graph_backend}</span> : null}
        </div>
      ) : null}

      {isLoading ? (
        <CommentaryState icon={<Info size={16} />} text="Generating AI Executive Commentary..." />
      ) : null}

      {!isLoading && error ? (
        <CommentaryState
          caption={error}
          icon={<AlertTriangle size={16} />}
          tone="danger"
          text="AI Executive Commentary is unavailable. No substitute commentary was displayed."
        />
      ) : null}

      {!isLoading && !error && !response ? (
        <CommentaryState
          icon={<Info size={16} />}
          text="AI Executive Commentary is not available for the selected inputs."
        />
      ) : null}

      {!isLoading && !error && isBlocked ? (
        <CommentaryState
          icon={<AlertTriangle size={16} />}
          tone="danger"
          text="AI Executive Commentary was blocked by safety controls and is not available for the selected inputs."
        />
      ) : null}

      {!isLoading && !error && commentary && !isBlocked && response ? (
        <>
          <div className="ai-commentary-tabs" role="tablist" aria-label="Commentary views">
            {(Object.keys(tabLabels) as CommentaryTab[]).map((tab) => (
              <button
                aria-selected={activeTab === tab}
                className={activeTab === tab ? "active" : ""}
                key={tab}
                onClick={() => setActiveTab(tab)}
                role="tab"
                type="button"
              >
                {tabLabels[tab]}
              </button>
            ))}
          </div>
          <p className="ai-commentary-text">{viewText}</p>
          <SupportingEvidence commentary={commentary} tab={activeTab} />
          <RecommendedActions actions={commentary.recommended_actions} />
          <div className="ai-commentary-observability">
            <span>
              Guardrail blocks: <strong>{response.observability.guardrail_block_count}</strong>
            </span>
            <span>
              Tools: <strong>{response.observability.tool_call_count}</strong>
            </span>
            <span>
              Thread: <strong>{response.observability.thread_id}</strong>
            </span>
          </div>
        </>
      ) : null}
    </Card>
  );
}

export function useExecutiveCommentary(data: RwaBriefingData | null | undefined) {
  const [response, setResponse] = useState<RwaAnalysisResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const request = useMemo(() => (data ? buildCommentaryRequest(data) : null), [data]);
  const requestSignature = request ? JSON.stringify(request) : "";

  useEffect(() => {
    if (!request) {
      setResponse(null);
      setError(null);
      setIsLoading(false);
      return;
    }
    const controller = new AbortController();
    setIsLoading(true);
    setError(null);
    postRwaExecutiveCommentary(request, controller.signal)
      .then((payload) => {
        setResponse(payload);
      })
      .catch((cause: unknown) => {
        if (!controller.signal.aborted) {
          setError(errorMessage(cause));
        }
      })
      .finally(() => {
        if (!controller.signal.aborted) {
          setIsLoading(false);
        }
      });
    return () => controller.abort();
  }, [requestSignature]);

  const regenerate = () => {
    if (!request) {
      return;
    }
    setIsLoading(true);
    setError(null);
    postRwaExecutiveCommentary({
      ...request,
      request_id: `${request.request_id}-regen-${Date.now()}`,
    })
      .then((payload) => {
        setResponse(payload);
      })
      .catch((cause: unknown) => {
        setError(errorMessage(cause));
      })
      .finally(() => setIsLoading(false));
  };

  return { error, isLoading, regenerate, response };
}

export function buildCommentaryRequest(data: RwaBriefingData): RwaAnalysisRequest | null {
  const calculatedRows = data.calculatedRwaRows ?? [];

  if (!calculatedRows.length) {
    return null;
  }

  const rows = calculatedRows.map((row: CalculatedRwaRow, index) => {
    const assetId = `ASSET-${String(index + 1).padStart(3, "0")}`;
    return {
      input: {
        asset_id: assetId,
        asset_class: row.entityClass,
        sector: row.sector,
        exposure_amount: row.exposureAmount,
        risk_weight: row.riskWeight,
        rating: row.rating ?? undefined,
        pd: row.pd ?? undefined,
        lgd: row.lgd ?? undefined,
        maturity_years: row.maturityYears ?? undefined,
        approach: row.approach,
      },
      output: {
        asset_id: assetId,
        rwa_amount: row.rwaAmount,
        exposure_amount: row.exposureAmount,
        risk_weight: row.riskWeight,
        approach: row.approach,
      },
    };
  });

  return {
    request_id: `briefing-${new Date(data.generatedAt).getTime() || Date.now()}`,
    loop_limit: 2,
    materiality_threshold: "0.05",
    rwa_input_data: rows.map((row) => row.input),
    rwa_output_results: rows.map((row) => row.output),
  };
}

function SupportingEvidence({
  commentary,
  tab,
}: {
  commentary: RwaAnalysisResponse["final_commentary"];
  tab: CommentaryTab;
}) {
  if (tab === "executive_summary") {
    return (
      <div className="ai-commentary-grid">
        <ObservationList items={commentary.data_quality_observations} title="Data Quality" />
        <QuantitativeValidationList items={commentary.quantitative_validation} />
      </div>
    );
  }

  if (tab === "cro_view") {
    return (
      <div className="ai-commentary-grid">
        <ObservationList items={commentary.risk_observations} title="Risk and Validation" />
        <QuantitativeValidationList items={commentary.quantitative_validation} />
      </div>
    );
  }

  return (
    <div className="ai-commentary-grid">
      <QuantitativeValidationList items={commentary.quantitative_validation} />
    </div>
  );
}

function ObservationList({
  items,
  title,
}: {
  items: RwaAnalysisResponse["final_commentary"]["data_quality_observations"];
  title: string;
}) {
  return (
    <div className="ai-observation-list">
      <strong>{title}</strong>
      {items.slice(0, 3).map((item) => (
        <div className="ai-observation-row" key={`${item.agent}-${item.title}`}>
          <StatusBadge tone={findingTone(item.severity)}>{item.severity}</StatusBadge>
          <span>{item.title}</span>
        </div>
      ))}
    </div>
  );
}

function QuantitativeValidationList({
  items,
}: {
  items: RwaAnalysisResponse["final_commentary"]["quantitative_validation"];
}) {
  return (
    <div className="ai-observation-list">
      <strong>Quantitative Validation</strong>
      {items.slice(0, 3).map((item) => (
        <div className="ai-observation-row" key={item.asset_id}>
          <StatusBadge tone={item.passed ? "success" : "danger"}>
            {item.passed ? "passed" : "variance"}
          </StatusBadge>
          <span>{item.asset_id}</span>
        </div>
      ))}
    </div>
  );
}

function RecommendedActions({ actions }: { actions: RwaRecommendedAction[] }) {
  if (!actions.length) {
    return (
      <div className="ai-actions-empty">
        <CheckCircle2 size={16} />
        <span>No open recommended actions</span>
      </div>
    );
  }
  return (
    <div className="ai-actions-list">
      <div className="briefing-panel-title">
        <ListChecks size={14} />
        <h3>Recommended Actions</h3>
      </div>
      {actions.map((action) => (
        <label className="ai-action-row" key={action.id}>
          <input checked={action.completed} readOnly type="checkbox" />
          <span>{action.label}</span>
          <StatusBadge tone={action.priority === "high" ? "danger" : "warning"}>
            {action.owner}
          </StatusBadge>
        </label>
      ))}
    </div>
  );
}

function CommentaryState({
  caption,
  icon,
  text,
  tone = "neutral",
}: {
  caption?: string;
  icon: ReactNode;
  text: string;
  tone?: "danger" | "neutral";
}) {
  return (
    <div className={`ai-commentary-state ai-commentary-state-${tone}`}>
      {icon}
      <span>
        {text}
        {caption ? <small>{caption}</small> : null}
      </span>
    </div>
  );
}

function statusTone(status: RwaAnalysisStatus) {
  if (status === "BLOCKED") {
    return "danger";
  }
  if (status === "LOOP_LIMIT_REACHED") {
    return "warning";
  }
  return "success";
}

function findingTone(severity: "info" | "warning" | "critical") {
  if (severity === "critical") {
    return "danger";
  }
  if (severity === "warning") {
    return "warning";
  }
  return "neutral";
}

function formatDate(value: string) {
  return new Intl.DateTimeFormat(undefined, {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(new Date(value));
}

function errorMessage(cause: unknown) {
  return cause instanceof Error ? cause.message : "Request failed";
}
