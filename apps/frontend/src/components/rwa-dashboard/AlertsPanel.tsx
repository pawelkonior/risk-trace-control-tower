import { Bell } from "lucide-react";

import type { DashboardAlert } from "../../hooks/useRwaDashboardData";
import { Card } from "./Card";

type AlertsPanelProps = {
  data: DashboardAlert[];
};

export function AlertsPanel({ data }: AlertsPanelProps) {
  return (
    <Card className="alerts-panel">
      <div className="alerts-heading">
        <Bell size={24} />
        <h3>Alerts & Notifications</h3>
      </div>
      <div className="alert-tiles">
        {data.map(({ count, label, tone, icon: Icon }) => (
          <div className={`alert-tile tone-${tone}`} key={label}>
            <Icon size={20} strokeWidth={1.8} />
            <strong>{count}</strong>
            <span>{label}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
