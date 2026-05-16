import { useState } from "react";
import { Cell, Pie, PieChart, ResponsiveContainer, Tooltip } from "recharts";

import type { ApiExposureClass } from "../../api/types";
import { Card, CardHeader } from "./Card";

type ExposureClassData = ApiExposureClass[];

type ExposureDonutCardProps = {
  data: ExposureClassData;
  totalAmount: string;
};

export function ExposureDonutCard({ data, totalAmount }: ExposureDonutCardProps) {
  const [activeIndex, setActiveIndex] = useState<number | null>(null);
  const activeItem = activeIndex === null ? null : data[activeIndex];

  return (
    <Card className="exposure-donut-card">
      <CardHeader title="RWA by Exposure Class" subtitle="(PLN)" />
      <div className="donut-layout">
        <DonutChart
          activeIndex={activeIndex}
          data={data}
          setActiveIndex={setActiveIndex}
          totalAmount={totalAmount}
        />
        <div className="donut-legend">
          {data.map((item, index) => (
            <button
              className={`legend-row legend-button${activeIndex === index ? " active" : ""}`}
              key={item.label}
              type="button"
              onBlur={() => setActiveIndex(null)}
              onClick={() => setActiveIndex(index)}
              onFocus={() => setActiveIndex(index)}
              onMouseEnter={() => setActiveIndex(index)}
              onMouseLeave={() => setActiveIndex(null)}
            >
              <span className="legend-label">
                <i style={{ backgroundColor: item.color }} />
                {item.label}
              </span>
              <span>{item.pct}</span>
              <strong>{item.amount}</strong>
            </button>
          ))}
          <div className="legend-row total">
            <span>Total</span>
            <span>100%</span>
            <strong>{totalAmount}</strong>
          </div>
        </div>
      </div>
      {activeItem ? (
        <div className="sr-live" aria-live="polite">
          {activeItem.label}: {activeItem.amount}, {activeItem.pct}
        </div>
      ) : null}
    </Card>
  );
}

function DonutChart({
  activeIndex,
  data,
  setActiveIndex,
  totalAmount,
}: {
  activeIndex: number | null;
  data: ExposureClassData;
  setActiveIndex: (index: number | null) => void;
  totalAmount: string;
}) {
  const activeItem = activeIndex === null ? null : data[activeIndex];

  return (
    <div className="donut-chart" onMouseLeave={() => setActiveIndex(null)}>
      <ResponsiveContainer width="100%" height="100%">
        <PieChart aria-label="RWA by exposure class donut chart">
          <Pie
            animationBegin={80}
            animationDuration={700}
            animationEasing="ease-out"
            cx="50%"
            cy="50%"
            data={data}
            dataKey="value"
            innerRadius={48}
            isAnimationActive
            nameKey="label"
            outerRadius={74}
            paddingAngle={0}
            stroke="#ffffff"
            strokeWidth={2}
            onMouseEnter={(_, index) => setActiveIndex(index)}
          >
            {data.map((item, index) => (
              <Cell
                className={`donut-segment${activeIndex === index ? " active" : ""}${
                  activeIndex !== null && activeIndex !== index ? " muted" : ""
                }`}
                fill={item.color}
                key={item.label}
              />
            ))}
          </Pie>
          <Tooltip content={<DonutTooltip />} cursor={false} />
        </PieChart>
      </ResponsiveContainer>
      <div className="donut-center">
        <strong>{activeItem?.amount ?? totalAmount}</strong>
        <span>{activeItem?.label ?? "Total RWA"}</span>
      </div>
    </div>
  );
}

function DonutTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{
    payload: ExposureClassData[number];
  }>;
}) {
  if (!active || !payload?.length) {
    return null;
  }

  const item = payload[0].payload;
  return (
    <div className="recharts-tooltip">
      <b>{item.label}</b>
      <span>{item.amount} RWA</span>
      <span>{item.pct} of total</span>
    </div>
  );
}
