import { AlertIcon, InboxIcon, RefreshIcon } from "./icons";

/** Full-page branded loader for route-level loading. */
export function PageLoader({ label = "Loading telemetry…" }) {
  return (
    <div className="loader">
      <span className="spinner" />
      <span className="mono dim" style={{ letterSpacing: "0.05em" }}>
        {label}
      </span>
    </div>
  );
}

/** Inline error block with an optional retry action. */
export function ErrorState({
  title = "Something went wrong",
  message = "Please try again.",
  onRetry,
}) {
  return (
    <div className="state state--error">
      <div className="state__icon">
        <AlertIcon />
      </div>
      <div className="state__title">{title}</div>
      <p className="state__msg">{message}</p>
      {onRetry && (
        <button type="button" className="btn" onClick={onRetry}>
          <RefreshIcon /> Retry
        </button>
      )}
    </div>
  );
}

/** Inline empty state for "backend is up, but there's no data yet". */
export function EmptyState({
  title = "No data yet",
  message = "Nothing has been recorded so far.",
}) {
  return (
    <div className="state state--empty">
      <div className="state__icon">
        <InboxIcon />
      </div>
      <div className="state__title">{title}</div>
      <p className="state__msg">{message}</p>
    </div>
  );
}

/** Skeleton block — pass width/height for shimmer placeholders. */
export function Skeleton({ width = "100%", height = 16, radius = 8, style }) {
  return (
    <span
      className="sk"
      style={{ display: "block", width, height, borderRadius: radius, ...style }}
    />
  );
}
