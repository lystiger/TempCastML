import { Area, AreaChart, ResponsiveContainer, YAxis } from "recharts";

/**
 * Tiny axis-less trend line for recent readings.
 * @param {{ data: {value:number}[], height?: number }} props
 */
export function Sparkline({ data, height = 44 }) {
  if (!data || data.length < 2) return null;
  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={data} margin={{ top: 4, right: 0, bottom: 0, left: 0 }}>
          <defs>
            <linearGradient id="sparkFill" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#38d6ff" stopOpacity={0.35} />
              <stop offset="100%" stopColor="#38d6ff" stopOpacity={0} />
            </linearGradient>
          </defs>
          <YAxis hide domain={["dataMin - 0.5", "dataMax + 0.5"]} />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#38d6ff"
            strokeWidth={2}
            fill="url(#sparkFill)"
            dot={false}
            isAnimationActive={false}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
