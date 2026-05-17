import {
  AlertTriangle,
  CheckCircle2,
  Info,
  RotateCcw,
  Sparkles,
} from "lucide-react";
import { useEffect, useMemo, useState, type ReactNode } from "react";

import { postRwaExecutiveCommentary } from "../../api/rwaApi";
import type {
  CalculatedRwaRow,
  RwaAnalysisRequest,
  RwaAnalysisResponse,
  RwaRecommendedAction,
} from "../../api/types";
import type { RwaBriefingData } from "../../hooks/useRwaBriefingData";
import { Card } from "../rwa-dashboard/Card";

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
  const viewParagraphs = splitCommentary(viewText);

  return (
    <Card className="briefing-card ai-commentary-card">
      <div className="ai-commentary-header">
        <div className="briefing-panel-title ai-commentary-title">
          <Sparkles size={15} />
          <h3>AI Executive Commentary</h3>
        </div>
        <div className="ai-commentary-tabs" role="tablist" aria-label="Commentary views">
          {(Object.keys(tabLabels) as CommentaryTab[]).map((tab) => (
            <button
              aria-selected={activeTab === tab}
              className={activeTab === tab ? "active" : ""}
              disabled={!commentary || isBlocked || isLoading}
              key={tab}
              onClick={() => setActiveTab(tab)}
              role="tab"
              type="button"
            >
              {tabLabels[tab]}
            </button>
          ))}
        </div>
      </div>

      <div className="ai-commentary-panel">
        {isLoading ? (
          <CommentaryState
            icon={<Info size={16} />}
            text="Generating AI Executive Commentary..."
          />
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

        {!isLoading && !error && commentary && !isBlocked ? (
          <div className="ai-commentary-content">
            <div className="ai-commentary-copy">
              {viewParagraphs.map((paragraph) => (
                <p className="ai-commentary-text" key={paragraph}>
                  {paragraph}
                </p>
              ))}
            </div>
            <RecommendedActions actions={commentary.recommended_actions} />
            <div className="ai-commentary-footer">
              <span>
                Commentary generated on {formatGeneratedAt(commentary.generated_at)} by{" "}
                {commentary.source_label}
              </span>
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
        ) : null}
      </div>
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
      <strong>Recommended Actions</strong>
      {actions.map((action) => (
        <div className="ai-action-row" key={action.id}>
          <CheckCircle2 size={14} />
          <span>{action.label}</span>
        </div>
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

function formatGeneratedAt(value: string) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) {
    return value;
  }
  const day = new Intl.DateTimeFormat("en-CA", {
    day: "2-digit",
    month: "2-digit",
    year: "numeric",
  }).format(date);
  const time = new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    hour12: false,
    minute: "2-digit",
  }).format(date);
  return `${day} ${time}`;
}

function errorMessage(cause: unknown) {
  return cause instanceof Error ? cause.message : "Request failed";
}

function splitCommentary(value: string) {
  return value
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
}
