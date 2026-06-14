import { WifiIcon, WifiOffIcon } from "./icons";

const CONN = {
  online: { cls: "pill--good", label: "Backend online", Icon: WifiIcon, pulse: true },
  offline: { cls: "pill--bad", label: "Backend offline", Icon: WifiOffIcon, pulse: false },
  checking: { cls: "", label: "Connecting…", Icon: WifiIcon, pulse: false },
};

/** Glanceable backend connection status. */
export function ConnectionPill({ status = "checking" }) {
  const { cls, label, Icon, pulse } = CONN[status] ?? CONN.checking;
  return (
    <span className={`pill ${cls}`} title={label}>
      <span className={`dot ${pulse ? "dot--pulse" : ""}`} />
      <Icon style={{ width: 14, height: 14 }} />
      {label}
    </span>
  );
}

/** Data-freshness chip driven by lib/format → freshness(). */
export function FreshnessPill({ level = "good", label = "live" }) {
  const cls =
    level === "good" ? "pill--good" : level === "warn" ? "pill--warn" : "pill--bad";
  return (
    <span className={`pill ${cls}`}>
      <span className={`dot ${level === "good" ? "dot--pulse" : ""}`} />
      {label}
    </span>
  );
}
