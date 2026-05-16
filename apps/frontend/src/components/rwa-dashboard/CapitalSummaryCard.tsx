import { Info } from "lucide-react";

import type { ApiCapitalSummary } from "../../api/types";
import { Card } from "./Card";

type CapitalSummaryCardProps = {
  data: ApiCapitalSummary;
};

export function CapitalSummaryCard({ data }: CapitalSummaryCardProps) {
  return (
    <Card className="capital-summary-card side-card">
      <div className="side-title">
        <h3>
          Capital Summary <Info size={12} />
        </h3>
        <p>({data.currency})</p>
      </div>

      <div className="capital-section">
        {data.rowsTop.map(([label, value]) => (
          <div className="capital-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <div className="capital-section ratio-section">
        {data.ratios.map(([label, value]) => (
          <div className="capital-row" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>

      <div className="capital-row requirement">
        <span>Minimum Requirement</span>
        <strong>{data.minimumRequirement}</strong>
      </div>
      <div className="capital-progress" aria-hidden="true">
        <span />
      </div>
      <div className="capital-row buffer">
        <span>Capital Buffer</span>
        <strong>{data.capitalBuffer}</strong>
      </div>
    </Card>
  );
}
