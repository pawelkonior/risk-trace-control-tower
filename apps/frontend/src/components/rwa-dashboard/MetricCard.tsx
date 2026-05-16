import { Info } from "lucide-react";
import type { ComponentType } from "react";

import type { Accent, DeltaDirection } from "../../api/types";
import { Card } from "./Card";

type MetricCardProps = {
  label: string;
  value: string;
  unit?: string;
  compareLabel: string;
  delta: string;
  deltaDirection: DeltaDirection;
  accent: Accent;
  icon: ComponentType<{ size?: number; strokeWidth?: number }>;
  showInfoIcon?: boolean;
};

export function MetricCard({
  label,
  value,
  unit,
  compareLabel,
  delta,
  deltaDirection,
  accent,
  icon: Icon,
  showInfoIcon,
}: MetricCardProps) {
  const displayValue = compactMetricValue(value);
  const isCompacted = displayValue !== value;

  return (
    <Card className="metric-card">
      <div className={`metric-icon accent-${accent}`}>
        <Icon size={22} strokeWidth={1.9} />
      </div>
      <div className="metric-content">
        <div className="metric-label">
          <span>{label}</span>
          {showInfoIcon ? <Info size={11} /> : null}
        </div>
        <div
          aria-label={isCompacted && unit ? `${value} ${unit}` : value}
          className={`metric-value${isCompacted ? " compact" : ""}`}
          title={isCompacted && unit ? `${value} ${unit}` : isCompacted ? value : undefined}
        >
          {displayValue}
        </div>
        {unit ? <div className="metric-unit">{unit}</div> : <div className="metric-unit empty" />}
        <div className="metric-compare">
          <span>{compareLabel}</span>
          <strong className={deltaDirection === "up" ? "positive" : "negative"}>
            {deltaDirection === "up" ? "↑" : "↓"} {delta}
          </strong>
        </div>
      </div>
    </Card>
  );
}

function compactMetricValue(value: string) {
  const numericValue = Number(value.replace(/,/g, "").trim());

  if (!Number.isFinite(numericValue) || !/^-?[\d,]+(\.\d+)?$/.test(value.trim())) {
    return value;
  }

  const absoluteValue = Math.abs(numericValue);

  if (absoluteValue >= 1_000_000_000_000) {
    return `${formatCompactNumber(numericValue / 1_000_000_000_000)}T`;
  }

  if (absoluteValue >= 1_000_000_000) {
    return `${formatCompactNumber(numericValue / 1_000_000_000)}B`;
  }

  if (absoluteValue >= 1_000_000) {
    return `${formatCompactNumber(numericValue / 1_000_000)}M`;
  }

  return value;
}

function formatCompactNumber(value: number) {
  const absoluteValue = Math.abs(value);
  const precision = absoluteValue >= 100 ? 1 : 2;
  return value
    .toFixed(precision)
    .replace(/\.0+$/, "")
    .replace(/(\.\d*[1-9])0+$/, "$1");
}
