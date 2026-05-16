import {
  Bar,
  BarChart,
  CartesianGrid,
  LabelList,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ApiRatingRwa } from "../../api/types";
import { Card, CardHeader } from "./Card";

type RatingRwaData = ApiRatingRwa[];

type RatingBarsCardProps = {
  data: RatingRwaData;
};

export function RatingBarsCard({ data }: RatingBarsCardProps) {
  const ratingChartData = data.map((item) => ({
    ...item,
    value: parseCompactAmount(item.amount),
  }));
  const maxValue = Math.max(...ratingChartData.map((item) => item.value), 1);
  const xMax = Math.max(5, Math.ceil(maxValue / 5) * 5);

  return (
    <Card className="rating-card">
      <CardHeader title="RWA by Rating (Internal)" subtitle="(PLN)" />
      <div className="rating-chart recharts-rating-chart">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart
            accessibilityLayer
            data={ratingChartData}
            layout="vertical"
            margin={{ top: 2, right: 38, bottom: 12, left: 0 }}
          >
            <CartesianGrid horizontal={false} stroke="#dfe8f4" />
            <XAxis
              axisLine={false}
              domain={[0, xMax]}
              tick={{ fill: "#31405f", fontSize: 11 }}
              tickFormatter={(value) => (value === 0 ? "0" : `${value}B`)}
              tickLine={false}
              ticks={[0, xMax / 2, xMax]}
              type="number"
            />
            <YAxis
              axisLine={false}
              dataKey="rating"
              tick={{ fill: "#07142d", fontSize: 11 }}
              tickLine={false}
              type="category"
              width={82}
            />
            <Tooltip content={<RatingTooltip />} cursor={{ fill: "rgba(7,81,215,0.06)" }} />
            <Bar
              animationBegin={80}
              animationDuration={650}
              animationEasing="ease-out"
              background={false}
              dataKey="value"
              fill="#0751d7"
              isAnimationActive
              maxBarSize={8}
              name="RWA"
              radius={[3, 3, 3, 3]}
            >
              <LabelList
                className="rating-value-label"
                dataKey="amount"
                fill="#07142d"
                fontSize={11}
                fontWeight={800}
                position="right"
              />
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>
    </Card>
  );
}

function parseCompactAmount(value: string) {
  const normalized = value.trim().toUpperCase();
  const amount = Number.parseFloat(normalized);
  if (Number.isNaN(amount)) {
    return 0;
  }
  if (normalized.endsWith("M")) {
    return amount / 1000;
  }
  if (normalized.endsWith("K")) {
    return amount / 1_000_000;
  }
  return amount;
}

function RatingTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{
    payload: RatingRwaData[number] & { value: number };
  }>;
}) {
  if (!active || !payload?.length) {
    return null;
  }

  const item = payload[0].payload;
  return (
    <div className="recharts-tooltip">
      <b>{item.rating}</b>
      <span>{item.amount} RWA</span>
      <span>{item.pct} of portfolio</span>
    </div>
  );
}
