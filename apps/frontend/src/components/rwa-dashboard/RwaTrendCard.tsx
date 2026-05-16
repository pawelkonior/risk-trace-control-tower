import {
  Area,
  AreaChart,
  CartesianGrid,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ApiRwaTrendPoint } from "../../api/types";
import { Card, CardHeader } from "./Card";

type RwaTrendData = ApiRwaTrendPoint[];

type RwaTrendCardProps = {
  data: RwaTrendData;
};

export function RwaTrendCard({ data }: RwaTrendCardProps) {
  const yMax = chartMax(data);
  const ticks = [0, yMax * 0.25, yMax * 0.5, yMax * 0.75, yMax].map((value) =>
    Number(value.toFixed(2)),
  );

  return (
    <Card className="trend-card">
      <CardHeader title="RWA Trend" subtitle="(PLN)" />
      <div className="trend-chart">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            accessibilityLayer
            data={data}
            margin={{ top: 14, right: 10, bottom: 4, left: 0 }}
          >
            <defs>
              <linearGradient id="rwaTrendFill" x1="0" x2="0" y1="0" y2="1">
                <stop offset="0%" stopColor="#0751d7" stopOpacity={0.2} />
                <stop offset="100%" stopColor="#0751d7" stopOpacity={0.03} />
              </linearGradient>
            </defs>
            <CartesianGrid stroke="#dde6f2" vertical={false} />
            <XAxis
              axisLine={false}
              dataKey="label"
              interval={0}
              minTickGap={8}
              tick={{ fill: "#31405f", fontSize: 11 }}
              tickFormatter={formatTrendTick}
              tickLine={false}
            />
            <YAxis
              axisLine={false}
              domain={[0, yMax]}
              tick={{ fill: "#31405f", fontSize: 11 }}
              tickFormatter={(value) => (value === 0 ? "0" : `${value}B`)}
              tickLine={false}
              ticks={ticks}
              width={36}
            />
            <Tooltip content={<TrendTooltip />} cursor={{ stroke: "#0751d7", strokeDasharray: "4 4" }} />
            <Area
              activeDot={{ r: 5, stroke: "#0751d7", strokeWidth: 3, fill: "#ffffff" }}
              animationBegin={80}
              animationDuration={720}
              animationEasing="ease-out"
              dataKey="value"
              dot={{ r: 4, strokeWidth: 0, fill: "#0751d7" }}
              fill="url(#rwaTrendFill)"
              fillOpacity={1}
              isAnimationActive
              stroke="#0751d7"
              strokeWidth={2.2}
              type="monotone"
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

function chartMax(data: RwaTrendData) {
  const maxValue = Math.max(...data.map((point) => point.value), 1);
  return Math.max(10, Math.ceil(maxValue / 5) * 5);
}

function formatTrendTick(value: string) {
  if (!value) {
    return "";
  }

  return value.split(" ")[0] ?? value;
}

function TrendTooltip({
  active,
  payload,
  label,
}: {
  active?: boolean;
  payload?: Array<{ value: number }>;
  label?: string;
}) {
  if (!active || !payload?.length) {
    return null;
  }

  return (
    <div className="recharts-tooltip">
      <b>{label || "Opening balance"}</b>
      <span>{payload[0].value.toFixed(2)}B PLN RWA</span>
    </div>
  );
}
