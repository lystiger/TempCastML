// Shared formatting helpers. The backend speaks Celsius; everything the user
// sees flows through here so unit/time handling stays consistent app-wide.

/** Convert a Celsius value into the active unit. */
export function convertTemp(celsius, unit) {
  if (celsius == null || Number.isNaN(celsius)) return null;
  if (unit === "fahrenheit") return (celsius * 9) / 5 + 32;
  if (unit === "kelvin") return celsius + 273.15;
  return celsius;
}

export function unitSymbol(unit) {
  if (unit === "fahrenheit") return "°F";
  if (unit === "kelvin") return "K";
  return "°C";
}

export function unitLabel(unit) {
  return unit.charAt(0).toUpperCase() + unit.slice(1);
}

/** Convert + round a Celsius value for display. Returns a string (no symbol). */
export function formatTemp(celsius, unit, digits = 1) {
  const v = convertTemp(celsius, unit);
  if (v == null) return "—";
  return v.toFixed(digits);
}

/** Signed delta (already in the active unit's scale), e.g. "+1.2". */
export function formatDelta(celsiusDelta, unit, digits = 1) {
  if (celsiusDelta == null || Number.isNaN(celsiusDelta)) return "—";
  // Delta scaling: F multiplies by 9/5; C and K share the same step size.
  const scaled = unit === "fahrenheit" ? (celsiusDelta * 9) / 5 : celsiusDelta;
  const sign = scaled > 0 ? "+" : "";
  return `${sign}${scaled.toFixed(digits)}`;
}

export function formatDateTime(date, is24h = true) {
  const d = date instanceof Date ? date : new Date(date);
  if (Number.isNaN(d.getTime())) return "—";
  return d.toLocaleString([], { hour12: !is24h });
}

export function formatClock(date, is24h = true) {
  const d = date instanceof Date ? date : new Date(date);
  return d.toLocaleTimeString([], {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: !is24h,
  });
}

/** Human relative time: "just now", "3m ago", "2h ago", "5d ago". */
export function relativeTime(date) {
  const d = date instanceof Date ? date : new Date(date);
  if (Number.isNaN(d.getTime())) return "—";
  const secs = Math.round((Date.now() - d.getTime()) / 1000);
  if (secs < 10) return "just now";
  if (secs < 60) return `${secs}s ago`;
  const mins = Math.round(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.round(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  const days = Math.round(hrs / 24);
  return `${days}d ago`;
}

/**
 * Classify how fresh a reading is. Data is polled every ~60s, so anything
 * older than a few minutes signals a stalled sensor/collector.
 * @returns {{ level: 'good'|'warn'|'bad', label: string }}
 */
export function freshness(date) {
  const d = date instanceof Date ? date : new Date(date);
  if (Number.isNaN(d.getTime())) return { level: "bad", label: "no signal" };
  const mins = (Date.now() - d.getTime()) / 60000;
  if (mins < 5) return { level: "good", label: "live" };
  if (mins < 30) return { level: "warn", label: "delayed" };
  return { level: "bad", label: "stale" };
}
