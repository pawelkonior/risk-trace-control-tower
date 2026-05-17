import {
  AlertTriangle,
  CheckCircle2,
  Info,
  LoaderCircle,
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
const MINIMUM_COMMENTARY_LOADING_MS = 900;
const LOADING_PHRASE_INTERVAL_MS = 2200;
const commentaryLoadingPhrases = [
  "Preparing anonymized RWA facts for the agent workflow.",
  "DataAnalystAgent is checking data-quality signals.",
  "RiskExpertAgent is reviewing RWA drivers and validation flags.",
  "Calling IBM watsonx.ai for stakeholder commentary synthesis.",
  "Running guardrails before anything reaches the dashboard.",
  "Assembling Executive Summary, CRO View, and CFO View.",
];

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
  const canRegenerate = hasCalculatedRows && !isLoading;
  const viewText = commentary ? commentary[activeTab] : "";
  const viewParagraphs = splitCommentary(viewText);
  const loadingPhrase = useLoadingPhrase(isLoading);

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
        {isLoading && !commentary ? (
          <CommentaryState
            caption={loadingPhrase}
            icon={<LoaderCircle className="ai-spinner" size={16} />}
            text="Generating AI Executive Commentary..."
          />
        ) : null}

        {!isLoading && error ? (
          <>
            <CommentaryState
              caption={error}
              icon={<AlertTriangle size={16} />}
              tone="danger"
              text="AI Executive Commentary is unavailable. No substitute commentary was displayed."
            />
            <CommentaryStateActions>
              <RegenerateButton
                disabled={!canRegenerate}
                isLoading={isLoading}
                onClick={onRegenerate}
              />
            </CommentaryStateActions>
          </>
        ) : null}

        {!isLoading && !error && !response ? (
          <>
            <CommentaryState
              icon={<Info size={16} />}
              text="AI Executive Commentary is not available for the selected inputs."
            />
            <CommentaryStateActions>
              <RegenerateButton
                disabled={!canRegenerate}
                isLoading={isLoading}
                onClick={onRegenerate}
              />
            </CommentaryStateActions>
          </>
        ) : null}

        {!isLoading && !error && isBlocked ? (
          <>
            <CommentaryState
              icon={<AlertTriangle size={16} />}
              tone="danger"
              text="AI Executive Commentary was blocked by safety controls and is not available for the selected inputs."
            />
            <CommentaryStateActions>
              <RegenerateButton
                disabled={!canRegenerate}
                isLoading={isLoading}
                onClick={onRegenerate}
              />
            </CommentaryStateActions>
          </>
        ) : null}

        {!error && commentary && !isBlocked ? (
          <div
            className={`ai-commentary-content ${
              isLoading ? "ai-commentary-content-loading" : ""
            }`}
          >
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
              <RegenerateButton
                disabled={!canRegenerate}
                isLoading={isLoading}
                onClick={onRegenerate}
              />
            </div>
          </div>
        ) : null}

        {isLoading && commentary ? (
          <div className="ai-commentary-loading-overlay" role="status" aria-live="polite">
            <LoaderCircle className="ai-spinner" size={20} />
            <span>Generating AI Executive Commentary...</span>
            <small>{loadingPhrase}</small>
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
    const startedAt = Date.now();
    setIsLoading(true);
    setError(null);
    postRwaExecutiveCommentary(request, controller.signal)
      .then(async (payload) => {
        await waitForMinimumDuration(startedAt);
        if (!controller.signal.aborted) {
          setResponse(payload);
        }
      })
      .catch(async (cause: unknown) => {
        await waitForMinimumDuration(startedAt);
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
    if (!request || isLoading) {
      return;
    }
    const startedAt = Date.now();
    setIsLoading(true);
    setError(null);
    postRwaExecutiveCommentary({
      ...request,
      request_id: `${request.request_id}-regen-${Date.now()}`,
    })
      .then(async (payload) => {
        await waitForMinimumDuration(startedAt);
        setResponse(payload);
      })
      .catch(async (cause: unknown) => {
        await waitForMinimumDuration(startedAt);
        setError(errorMessage(cause));
      })
      .finally(() => setIsLoading(false));
  };

  return { error, isLoading, regenerate, response };
}

function useLoadingPhrase(isLoading: boolean) {
  const [phraseIndex, setPhraseIndex] = useState(0);

  useEffect(() => {
    if (!isLoading) {
      setPhraseIndex(0);
      return;
    }

    const intervalId = window.setInterval(() => {
      setPhraseIndex((current) => (current + 1) % commentaryLoadingPhrases.length);
    }, LOADING_PHRASE_INTERVAL_MS);

    return () => window.clearInterval(intervalId);
  }, [isLoading]);

  return commentaryLoadingPhrases[phraseIndex];
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

function CommentaryStateActions({ children }: { children: ReactNode }) {
  return <div className="ai-commentary-state-actions">{children}</div>;
}

function RegenerateButton({
  disabled,
  isLoading,
  onClick,
}: {
  disabled: boolean;
  isLoading: boolean;
  onClick: () => void;
}) {
  return (
    <button
      className="button button-secondary compact-button"
      disabled={disabled}
      onClick={onClick}
      type="button"
    >
      {isLoading ? <LoaderCircle className="ai-spinner" size={14} /> : <RotateCcw size={14} />}
      <span>{isLoading ? "Thinking..." : "Regenerate"}</span>
    </button>
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

function waitForMinimumDuration(startedAt: number) {
  const remaining = MINIMUM_COMMENTARY_LOADING_MS - (Date.now() - startedAt);
  return remaining > 0
    ? new Promise((resolve) => window.setTimeout(resolve, remaining))
    : Promise.resolve();
}

function splitCommentary(value: string) {
  return value
    .split(/\n{2,}/)
    .map((paragraph) => paragraph.trim())
    .filter(Boolean);
}
