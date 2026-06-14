import { TrendUp, TrendDown } from "./icons";

/**
 * A single telemetry metric tile.
 * @param {{
 *   label: string,
 *   value: string|number,
 *   unit?: string,
 *   sub?: React.ReactNode,
 *   trend?: { dir: 'up'|'down'|'flat', text: string } | null,
 *   muted?: boolean,
 *   className?: string,
 * }} props
 */
export function StatCard({ label, value, unit, sub, trend, muted, className = "" }) {
  return (
    <div className={`panel panel--pad panel--hover ${className}`}>
      <div className="stat">
        <div className="stat__label">{label}</div>
        <div className={`stat__value num ${muted ? "stat__value--muted" : ""}`}>
          {value}
          {unit && <small>{unit}</small>}
        </div>
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            justifyContent: "space-between",
          }}
        >
          {sub && <span className="stat__sub">{sub}</span>}
          {trend && <TrendChip {...trend} />}
        </div>
      </div>
    </div>
  );
}

export function TrendChip({ dir, text }) {
  if (dir === "up") {
    return (
      <span className="trend trend--up">
        <TrendUp style={{ width: 13, height: 13 }} /> {text}
      </span>
    );
  }
  if (dir === "down") {
    return (
      <span className="trend trend--down">
        <TrendDown style={{ width: 13, height: 13 }} /> {text}
      </span>
    );
  }
  return <span className="trend trend--flat">{text}</span>;
}
