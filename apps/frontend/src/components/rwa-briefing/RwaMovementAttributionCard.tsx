import { ArrowDownRight, ArrowUpRight, Gauge, Info, Target } from "lucide-react";
import type { LucideIcon } from "lucide-react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  LabelList,
  ReferenceLine,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import type { ApiMovementDriver, ApiWaterfallItem } from "../../api/types";
import { Card } from "../rwa-dashboard/Card";

type RwaMovementAttributionCardProps = {
  movementDrivers: ApiMovementDriver[];
  totalChange: string;
  totalChangePct: string;
  waterfallData: ApiWaterfallItem[];
};

export function RwaMovementAttributionCard({
  movementDrivers,
  totalChange,
  totalChangePct,
  waterfallData,
}: RwaMovementAttributionCardProps) {
  const analytics = movementAnalytics(movementDrivers, totalChange, totalChangePct);
  const closingLevel = waterfallData.find((item) => item.closing)?.closing ?? 0;

  return (
    <Card className="briefing-card movement-card">
      <div className="briefing-card-header">
        <h3>RWA Movement Attribution (Drivers)</h3>
        <Info size={13} />
      </div>
      <div className="movement-analytics-strip" aria-label="Movement attribution indicators">
        {analytics.map((item) => (
          <MovementAnalyticsCard item={item} key={item.label} />
        ))}
      </div>
      <div className="movement-content">
        <div className="waterfall-panel">
          <div className="waterfall-chart-toolbar">
            <div className="chart-unit">
              <span>PLN (Millions)</span>
              <strong>Quarter movement bridge</strong>
            </div>
            <div className="movement-chart-legend" aria-label="Chart legend">
              <span className="movement-legend-positive">Growth</span>
              <span className="movement-legend-offset">Offset</span>
              <span className="movement-legend-close">Closing</span>
            </div>
          </div>
          <div className="waterfall-chart">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                barCategoryGap="27%"
                data={waterfallData}
                margin={{ top: 28, right: 18, bottom: 8, left: 8 }}
                stackOffset="sign"
              >
                <defs>
                  <filter height="140%" id="waterfallShadow" width="140%" x="-20%" y="-20%">
                    <feDropShadow dx="0" dy="5" floodColor="#07142d" floodOpacity="0.14" stdDeviation="5" />
                  </filter>
                </defs>
                <CartesianGrid stroke="#dfe8f4" vertical={false} />
                <XAxis
                  dataKey="axisLabel"
                  height={46}
                  interval={0}
                  tick={<WaterfallTick />}
                  tickLine={false}
                />
                <YAxis
                  axisLine={false}
                  domain={[-600, 1200]}
                  tick={{ fill: "#31405f", fontSize: 10 }}
                  tickLine={false}
                  ticks={[-600, -300, 0, 300, 600, 900, 1200]}
                  width={34}
                />
                <ReferenceLine y={0} stroke="#a9b7cc" />
                <ReferenceLine
                  ifOverflow="extendDomain"
                  stroke="#0751d7"
                  strokeDasharray="5 5"
                  y={closingLevel}
                />
                <Tooltip content={<WaterfallTooltip />} cursor={{ fill: "rgba(7,81,215,0.04)" }} />
                <Bar dataKey="base" stackId="waterfall" fill="transparent" isAnimationActive={false} />
                <Bar
                  dataKey="opening"
                  filter="url(#waterfallShadow)"
                  isAnimationActive={false}
                  maxBarSize={58}
                  radius={[4, 4, 4, 4]}
                  stackId="waterfall"
                >
                  {waterfallData.map((entry) => (
                    <Cell fill={entry.color} key={`${entry.tableLabel}-opening`} />
                  ))}
                  <LabelList content={<WaterfallLabel valueKey="opening" />} />
                </Bar>
                <Bar
                  dataKey="increase"
                  filter="url(#waterfallShadow)"
                  isAnimationActive={false}
                  maxBarSize={58}
                  radius={[4, 4, 4, 4]}
                  stackId="waterfall"
                >
                  {waterfallData.map((entry) => (
                    <Cell fill={entry.color} key={`${entry.tableLabel}-increase`} />
                  ))}
                  <LabelList content={<WaterfallLabel valueKey="increase" />} />
                </Bar>
                <Bar
                  dataKey="decrease"
                  filter="url(#waterfallShadow)"
                  isAnimationActive={false}
                  maxBarSize={58}
                  radius={[4, 4, 4, 4]}
                  stackId="waterfall"
                >
                  {waterfallData.map((entry) => (
                    <Cell fill={entry.color} key={`${entry.tableLabel}-decrease`} />
                  ))}
                  <LabelList content={<WaterfallLabel valueKey="decrease" />} />
                </Bar>
                <Bar
                  dataKey="closing"
                  filter="url(#waterfallShadow)"
                  isAnimationActive={false}
                  maxBarSize={58}
                  radius={[4, 4, 4, 4]}
                  stackId="waterfall"
                >
                  {waterfallData.map((entry) => (
                    <Cell fill={entry.color} key={`${entry.tableLabel}-closing`} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
        <div className="movement-driver-table">
          <table>
            <thead>
              <tr>
                <th>Driver</th>
                <th>Impact (PLN)</th>
                <th>% Change</th>
              </tr>
            </thead>
            <tbody>
              {movementDrivers.map(({ changePct, color, driver, impact }) => {
                const impactValue = parseMoney(impact);
                const share = Math.min(Math.abs(parsePercent(changePct)), 100);

                return (
                  <tr key={driver}>
                    <td>
                      <span className="movement-driver-name" title={driver}>
                        <i style={{ backgroundColor: color }} />
                        <span>{driver}</span>
                      </span>
                    </td>
                    <td>
                      <span
                        className={`movement-impact-value ${
                          impactValue < 0 ? "movement-impact-offset" : "movement-impact-growth"
                        }`}
                      >
                        {impact}
                      </span>
                    </td>
                    <td>
                      <span className="movement-share-cell">
                        <strong>{changePct}</strong>
                        <span className="movement-share-track">
                          <i style={{ backgroundColor: color, width: `${share}%` }} />
                        </span>
                      </span>
                    </td>
                  </tr>
                );
              })}
              <tr className="total">
                <td>
                  <span className="movement-driver-name">Total Change</span>
                </td>
                <td>{totalChange}</td>
                <td>{totalChangePct}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </Card>
  );
}

type MovementAnalyticsItem = {
  detail: string;
  icon: LucideIcon;
  label: string;
  tone: "blue" | "green" | "orange" | "purple";
  value: string;
};

function MovementAnalyticsCard({ item }: { item: MovementAnalyticsItem }) {
  const Icon = item.icon;

  return (
    <div className={`movement-analytic-card movement-analytic-${item.tone}`}>
      <span className="movement-analytic-icon">
        <Icon size={16} strokeWidth={2.1} />
      </span>
      <div>
        <span>{item.label}</span>
        <strong>{item.value}</strong>
        <p>{item.detail}</p>
      </div>
    </div>
  );
}

function movementAnalytics(
  movementDrivers: ApiMovementDriver[],
  totalChange: string,
  totalChangePct: string,
): MovementAnalyticsItem[] {
  const driverAmounts = movementDrivers.map((driver) => ({
    ...driver,
    amount: parseMoney(driver.impact),
    pct: parsePercent(driver.changePct),
  }));
  const growthTotal = driverAmounts
    .filter((driver) => driver.amount > 0)
    .reduce((sum, driver) => sum + driver.amount, 0);
  const offsetTotal = driverAmounts
    .filter((driver) => driver.amount < 0)
    .reduce((sum, driver) => sum + driver.amount, 0);
  const leadDriver =
    driverAmounts.reduce<(typeof driverAmounts)[number] | null>(
      (winner, driver) => (!winner || Math.abs(driver.amount) > Math.abs(winner.amount) ? driver : winner),
      null,
    ) ?? driverAmounts[0];

  return [
    {
      detail: `${totalChangePct} reconciled to drivers`,
      icon: Target,
      label: "Net movement",
      tone: "blue",
      value: `${formatImpact(totalChange)} PLN`,
    },
    {
      detail: `${driverAmounts.filter((driver) => driver.amount > 0).length} upward drivers`,
      icon: ArrowUpRight,
      label: "Growth pressure",
      tone: "orange",
      value: `${formatImpact(growthTotal)} PLN`,
    },
    {
      detail: "Collateral improvement",
      icon: ArrowDownRight,
      label: "Offset impact",
      tone: "green",
      value: `${formatImpact(offsetTotal)} PLN`,
    },
    {
      detail: leadDriver?.driver ?? "No lead driver",
      icon: Gauge,
      label: "Lead driver share",
      tone: "purple",
      value: leadDriver?.changePct ?? "0.0%",
    },
  ];
}

function WaterfallTick({
  x,
  y,
  payload,
}: {
  x?: number;
  y?: number;
  payload?: { value?: string };
}) {
  return (
    <g transform={`translate(${x ?? 0},${(y ?? 0) + 13}) rotate(-32)`}>
      <text className="waterfall-axis-label" textAnchor="end" x={0} y={0}>
        {payload?.value}
      </text>
    </g>
  );
}

function parseMoney(value: string) {
  const parsed = Number(value.replace(/[,+\s]/g, ""));
  return Number.isFinite(parsed) ? parsed : 0;
}

function parsePercent(value: string) {
  const parsed = Number(value.replace(/[%+\s]/g, ""));
  return Number.isFinite(parsed) ? parsed : 0;
}

function formatImpact(value: string | number) {
  const amount = typeof value === "number" ? value : parseMoney(value);
  const abs = Math.abs(amount);
  const sign = amount > 0 ? "+" : amount < 0 ? "-" : "";

  if (abs >= 1_000_000_000) {
    return `${sign}${(abs / 1_000_000_000).toFixed(2)}B`;
  }

  return `${sign}${Math.round(abs / 1_000_000)}M`;
}

function WaterfallLabel(props: {
  payload?: ApiWaterfallItem;
  value?: number;
  valueKey: "opening" | "increase" | "decrease";
  x?: number;
  y?: number;
  width?: number;
  height?: number;
}) {
  const entry = props.payload;

  if (
    !entry?.display ||
    !entry[props.valueKey] ||
    props.x === undefined ||
    props.y === undefined ||
    props.width === undefined
  ) {
    return null;
  }

  const y = entry.display.startsWith("-") ? props.y + (props.height ?? 0) + 13 : props.y - 5;

  return (
    <text className="waterfall-label" textAnchor="middle" x={props.x + props.width / 2} y={y}>
      {entry.display}
    </text>
  );
}

function WaterfallTooltip({
  active,
  payload,
}: {
  active?: boolean;
  payload?: Array<{
    payload: ApiWaterfallItem;
  }>;
}) {
  if (!active || !payload?.length) {
    return null;
  }

  const item = payload[0].payload;
  return (
    <div className="recharts-tooltip">
      <b>{item.tableLabel}</b>
      <span>{item.display || "Closing balance"} PLN millions</span>
    </div>
  );
}
