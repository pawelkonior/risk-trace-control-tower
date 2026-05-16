import type { BriefingKpi } from "../../hooks/useRwaBriefingData";
import { Card } from "../rwa-dashboard/Card";

export function BriefingKpiStrip({ kpis }: { kpis: BriefingKpi[] }) {
  return (
    <Card className="briefing-kpi-strip">
      {kpis.map(({ detail, icon: Icon, label, tone, value }) => (
        <div className="briefing-kpi" key={label}>
          <div className={`briefing-kpi-icon briefing-tone-${tone}`}>
            <Icon size={22} strokeWidth={1.8} />
          </div>
          <div>
            <span>{label}</span>
            <strong className={tone === "red" ? "negative" : tone === "green" ? "positive" : ""}>
              {value}
            </strong>
            {detail.split("\n").map((line) => (
              <em
                className={line.startsWith("+") ? "positive" : line.startsWith("-") ? "negative" : ""}
                key={line}
              >
                {line}
              </em>
            ))}
          </div>
        </div>
      ))}
    </Card>
  );
}
