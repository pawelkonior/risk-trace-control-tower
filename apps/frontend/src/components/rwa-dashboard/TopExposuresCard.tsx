import { useEffect, useState } from "react";

import type { ApiTopExposure } from "../../api/types";
import { Card } from "./Card";

type TopExposuresCardProps = {
  data: ApiTopExposure[];
};

export function TopExposuresCard({ data }: TopExposuresCardProps) {
  const [selectedId, setSelectedId] = useState(data[0]?.id ?? "");

  useEffect(() => {
    setSelectedId(data[0]?.id ?? "");
  }, [data]);

  return (
    <Card className="top-exposures-card side-card">
      <div className="side-title">
        <h3>Top Capital-Intensive Exposures</h3>
        <p>(by RWA)</p>
      </div>

      <div className="exposure-list">
        {data.map((item) => (
          <button
            className={`exposure-item${selectedId === item.id ? " active" : ""}`}
            key={item.id}
            type="button"
            onClick={() => {
              setSelectedId(item.id);
            }}
          >
            <div className="exposure-topline">
              <strong>{item.id}</strong>
              <span>{item.amount}</span>
              <em>{item.pct}</em>
            </div>
            <div className="exposure-name">{item.name}</div>
            <div className="mini-progress">
              <span style={{ width: `${item.bar}%` }} />
            </div>
          </button>
        ))}
      </div>
    </Card>
  );
}
