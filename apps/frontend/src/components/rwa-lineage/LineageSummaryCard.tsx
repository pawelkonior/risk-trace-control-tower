import { Card } from "../rwa-dashboard/Card";

export function LineageSummaryCard({ summary }: { summary: Array<[string, string]> }) {
  return (
    <Card className="lineage-summary-card lineage-section-card">
      <h3>Lineage Summary</h3>
      <div className="lineage-summary-grid">
        {summary.map(([label, value]) => (
          <div className="lineage-kv" key={label}>
            <span>{label}</span>
            <strong>{value}</strong>
          </div>
        ))}
      </div>
    </Card>
  );
}
