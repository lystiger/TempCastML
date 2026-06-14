import { useContext, useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import { getHistoricalSensorData, ApiError } from "../services/api";
import { TimeFormatContext } from "../contexts/TimeFormatContext";
import { TemperatureUnitContext } from "../contexts/TemperatureUnitContext";
import {
  formatDateTime,
  formatDelta,
  formatTemp,
  relativeTime,
  unitLabel,
  unitSymbol,
} from "../lib/format";

import { SegmentedControl } from "../components/SegmentedControl";
import { StatCard } from "../components/StatCard";
import { ErrorState, EmptyState, PageLoader } from "../components/States";
import { RefreshIcon } from "../components/icons";

export default function History() {
  const { is24hFormat } = useContext(TimeFormatContext);
  const { unit, toggleUnit } = useContext(TemperatureUnitContext);

  const [history, setHistory] = useState([]);
  const [limit, setLimit] = useState(50);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchHistory = async (n = limit, { silent = false } = {}) => {
    if (silent) setRefreshing(true);
    else setLoading(true);
    try {
      const data = await getHistoricalSensorData({ limit: n });
      setHistory(Array.isArray(data) ? data : []);
      setError(null);
      if (silent) toast.success("History refreshed");
    } catch (err) {
      const offline = err instanceof ApiError && err.status === 0;
      setError(
        offline
          ? "Can't reach the backend. Make sure the API is running on port 8000."
          : "Failed to load historical readings."
      );
      if (silent) toast.error("Refresh failed");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchHistory(limit);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [limit]);

  const sym = unitSymbol(unit);

  // Backend returns newest-first; compute per-row delta against the
  // chronologically previous reading, then present newest-first.
  const rows = useMemo(() => {
    const chrono = [...history].sort(
      (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
    );
    const withDelta = chrono.map((r, i) => ({
      ...r,
      delta: i === 0 ? null : r.temperature_c - chrono[i - 1].temperature_c,
    }));
    return withDelta.reverse();
  }, [history]);

  const summary = useMemo(() => {
    if (!history.length) return null;
    const temps = history.map((r) => r.temperature_c);
    return {
      count: history.length,
      min: Math.min(...temps),
      max: Math.max(...temps),
      avg: temps.reduce((a, b) => a + b, 0) / temps.length,
    };
  }, [history]);

  if (loading) return <PageLoader label="Loading history…" />;

  return (
    <>
      <div className="page-head">
        <div>
          <span className="eyebrow">
            <b>02</b> / Archive
          </span>
          <h1 className="page-title">Reading History</h1>
          <p className="page-sub">
            Recorded sensor readings, newest first. The current dataset captures
            indoor temperature per device.
          </p>
        </div>
        <div className="toolbar">
          <SegmentedControl
            ariaLabel="Row limit"
            value={limit}
            onChange={setLimit}
            options={[
              { value: 25, label: "25" },
              { value: 50, label: "50" },
              { value: 100, label: "100" },
              { value: 200, label: "200" },
            ]}
          />
          <SegmentedControl
            ariaLabel="Temperature unit"
            value={unit}
            onChange={(u) => {
              toggleUnit(u);
              toast.success(`Showing ${unitLabel(u)}`);
            }}
            options={[
              { value: "celsius", label: "°C" },
              { value: "fahrenheit", label: "°F" },
              { value: "kelvin", label: "K" },
            ]}
          />
          <button
            type="button"
            className="btn"
            onClick={() => fetchHistory(limit, { silent: true })}
            disabled={refreshing}
          >
            <RefreshIcon className={refreshing ? "spin" : ""} /> Refresh
          </button>
        </div>
      </div>

      {error ? (
        <div className="panel panel--pad">
          <ErrorState
            title="Backend unreachable"
            message={error}
            onRetry={() => fetchHistory(limit, { silent: true })}
          />
        </div>
      ) : !history.length ? (
        <div className="panel panel--pad">
          <EmptyState
            title="No readings recorded"
            message="Once the collector starts writing sensor data, it will appear here."
          />
        </div>
      ) : (
        <>
          <div className="grid dash-grid" style={{ marginBottom: 18 }}>
            <div className="col-3 rise rise-1">
              <StatCard label="Window · readings" value={String(summary.count)} sub="loaded rows" />
            </div>
            <div className="col-3 rise rise-1">
              <StatCard label="Window · low" value={formatTemp(summary.min, unit)} unit={sym} sub="minimum" />
            </div>
            <div className="col-3 rise rise-2">
              <StatCard label="Window · high" value={formatTemp(summary.max, unit)} unit={sym} sub="maximum" />
            </div>
            <div className="col-3 rise rise-2">
              <StatCard label="Window · average" value={formatTemp(summary.avg, unit)} unit={sym} sub="mean" />
            </div>
          </div>

          <div className="table-wrap rise rise-3">
            <table className="table">
              <thead>
                <tr>
                  <th>Timestamp</th>
                  <th>Age</th>
                  <th>Device</th>
                  <th className="num">Temp ({sym})</th>
                  <th className="num">Δ prev</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r) => (
                  <tr key={r.id ?? r.timestamp}>
                    <td className="num">{formatDateTime(r.timestamp, is24hFormat)}</td>
                    <td className="dim">{relativeTime(r.timestamp)}</td>
                    <td className="mono dim">#{r.device_id}</td>
                    <td className="num">{formatTemp(r.temperature_c, unit, 2)}</td>
                    <td className="num">
                      {r.delta == null ? (
                        <span className="faint">—</span>
                      ) : (
                        <DeltaCell deltaC={r.delta} unit={unit} />
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  );
}

function DeltaCell({ deltaC, unit }) {
  const color =
    deltaC > 0.05 ? "var(--accent)" : deltaC < -0.05 ? "var(--cool)" : "var(--text-3)";
  return <span style={{ color }}>{formatDelta(deltaC, unit, 2)}</span>;
}
