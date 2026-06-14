import {
  Area,
  AreaChart,
  CartesianGrid,
  ReferenceDot,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

function ForecastTooltip({ active, payload, unitSym }) {
  if (!active || !payload?.length) return null;
  const p = payload[0].payload;
  return (
    <div className="chart-tooltip">
      <div className="chart-tooltip__k">{p.label}</div>
      <div className="chart-tooltip__v">
        {p.value?.toFixed(1)}
        {unitSym}
      </div>
    </div>
  );
}

/**
 * Forecast area chart. `data` = [{ label, value }] in the active unit, with the
 * first point being "Now" (the latest real reading) so the curve reads as a
 * continuation of measured data.
 */
export function ForecastChart({ data, unitSym = "°C" }) {
  return (
    <div className="chart">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 16, right: 14, bottom: 4, left: -8 }}>
          <defs>
            <linearGradient id="thermStroke" x1="0" y1="0" x2="1" y2="0">
              <stop offset="0%" stopColor="#38d6ff" />
              <stop offset="100%" stopColor="#ff8a3d" />
            </linearGradient>
            <linearGradient id="thermFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ff8a3d" stopOpacity={0.28} />
              <stop offset="100%" stopColor="#ff8a3d" stopOpacity={0} />
            </linearGradient>
          </defs>

          <CartesianGrid
            stroke="rgba(255,255,255,0.06)"
            vertical={false}
          />
          <XAxis
            dataKey="label"
            tick={{ fill: "#5b636e", fontSize: 11, fontFamily: "JetBrains Mono" }}
            tickLine={false}
            axisLine={{ stroke: "rgba(255,255,255,0.08)" }}
            minTickGap={24}
          />
          <YAxis
            width={48}
            tick={{ fill: "#5b636e", fontSize: 11, fontFamily: "JetBrains Mono" }}
            tickLine={false}
            axisLine={false}
            domain={["dataMin - 1", "dataMax + 1"]}
            tickFormatter={(v) => `${Math.round(v)}°`}
          />
          <Tooltip
            content={<ForecastTooltip unitSym={unitSym} />}
            cursor={{ stroke: "rgba(255,255,255,0.18)", strokeDasharray: "4 4" }}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="url(#thermStroke)"
            strokeWidth={2.5}
            fill="url(#thermFill)"
            dot={false}
            activeDot={{
              r: 4,
              fill: "#ff8a3d",
              stroke: "#0b0d11",
              strokeWidth: 2,
            }}
            isAnimationActive
            animationDuration={700}
          />
          {data?.length > 0 && (
            <ReferenceDot
              x={data[0].label}
              y={data[0].value}
              r={4}
              fill="#38d6ff"
              stroke="#0b0d11"
              strokeWidth={2}
            />
          )}
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
