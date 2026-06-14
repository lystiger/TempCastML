import { useContext, useEffect, useMemo, useState } from "react";
import toast from "react-hot-toast";

import {
  getHealth,
  getHistoricalSensorData,
  getLatestSensorData,
  getPrediction,
  ApiError,
} from "../services/api";
import { TemperatureUnitContext } from "../contexts/TemperatureUnitContext";
import {
  convertTemp,
  formatDelta,
  formatTemp,
  freshness,
  relativeTime,
  unitLabel,
  unitSymbol,
} from "../lib/format";
import { useCountUp } from "../hooks/useCountUp";

import { SegmentedControl } from "../components/SegmentedControl";
import { ConnectionPill, FreshnessPill } from "../components/StatusPill";
import { StatCard } from "../components/StatCard";
import { ForecastChart } from "../components/ForecastChart";
import { Sparkline } from "../components/Sparkline";
import { ErrorState, EmptyState, PageLoader, Skeleton } from "../components/States";
import { RefreshIcon } from "../components/icons";

const HORIZON = 24;
const DEVICE_ID = 1;
const POLL_MS = 60000;

export default function Dashboard() {
  const { unit, toggleUnit } = useContext(TemperatureUnitContext);

  const [latest, setLatest] = useState(null);
  const [prediction, setPrediction] = useState(null);
  const [history, setHistory] = useState([]);
  const [connection, setConnection] = useState("checking");

  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [error, setError] = useState(null);

  const fetchAll = async ({ silent = false } = {}) => {
    if (silent) setRefreshing(true);
    else setLoading(true);
    try {
      const [online, latestData, predictionData, historyData] = await Promise.all([
        getHealth(),
        getLatestSensorData(),
        getPrediction(DEVICE_ID, HORIZON),
        getHistoricalSensorData({ limit: 48 }),
      ]);
      setConnection(online ? "online" : "offline");
      setLatest(latestData);
      setPrediction(predictionData);
      setHistory(Array.isArray(historyData) ? historyData : []);
      setError(null);
      if (silent) toast.success("Telemetry refreshed");
    } catch (err) {
      setConnection("offline");
      const offline = err instanceof ApiError && err.status === 0;
      setError(
        offline
          ? "Can't reach the backend. Make sure the API is running on port 8000."
          : "Failed to load telemetry from the backend."
      );
      if (silent) toast.error("Refresh failed");
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    fetchAll();
    const id = setInterval(() => fetchAll({ silent: false }), POLL_MS);
    return () => clearInterval(id);
  }, []);

  /* ---- derived telemetry -------------------------------------------- */
  // History arrives newest-first; sort ascending for trend visuals.
  const chrono = useMemo(
    () =>
      [...history].sort(
        (a, b) => new Date(a.timestamp) - new Date(b.timestamp)
      ),
    [history]
  );

  const spark = useMemo(
    () =>
      chrono.slice(-24).map((r) => ({ value: convertTemp(r.temperature_c, unit) })),
    [chrono, unit]
  );

  const todayAvg = useMemo(() => {
    const today = new Date().toDateString();
    const todays = chrono.filter(
      (r) => new Date(r.timestamp).toDateString() === today
    );
    if (!todays.length) return null;
    const mean =
      todays.reduce((acc, r) => acc + r.temperature_c, 0) / todays.length;
    return mean;
  }, [chrono]);

  const range = useMemo(() => {
    const cutoff = Date.now() - 24 * 3600 * 1000;
    const recent = chrono.filter((r) => new Date(r.timestamp).getTime() >= cutoff);
    if (!recent.length) return null;
    const temps = recent.map((r) => r.temperature_c);
    return { min: Math.min(...temps), max: Math.max(...temps) };
  }, [chrono]);

  const forecastData = useMemo(() => {
    if (!prediction?.forecast?.length) return [];
    const anchor =
      latest?.temperature_c ?? prediction.forecast[0];
    const points = [{ label: "Now", value: convertTemp(anchor, unit) }];
    prediction.forecast.forEach((v, i) => {
      points.push({ label: `+${i + 1}h`, value: convertTemp(v, unit) });
    });
    return points;
  }, [prediction, latest, unit]);

  const nextHour = useMemo(() => {
    if (!prediction?.forecast?.length || latest?.temperature_c == null) return null;
    const delta = prediction.forecast[0] - latest.temperature_c;
    return { value: prediction.forecast[0], delta };
  }, [prediction, latest]);

  const horizonTrend = useMemo(() => {
    if (!prediction?.forecast?.length || latest?.temperature_c == null) return null;
    const end = prediction.forecast[prediction.forecast.length - 1];
    return end - latest.temperature_c;
  }, [prediction, latest]);

  const forecastPeak = useMemo(() => {
    if (!prediction?.forecast?.length) return null;
    return Math.max(...prediction.forecast);
  }, [prediction]);

  const sym = unitSymbol(unit);
  const fresh = latest ? freshness(latest.timestamp) : null;
  const heroValue = useCountUp(convertTemp(latest?.temperature_c, unit), {
    digits: 1,
  });

  const trendChip = (deltaC) => {
    if (deltaC == null) return null;
    if (deltaC > 0.1)
      return { dir: "up", text: `${formatDelta(deltaC, unit)}${sym}` };
    if (deltaC < -0.1)
      return { dir: "down", text: `${formatDelta(deltaC, unit)}${sym}` };
    return { dir: "flat", text: "steady" };
  };

  /* ---- render ------------------------------------------------------- */
  if (loading && !latest && connection === "checking") {
    return <PageLoader />;
  }

  return (
    <>
      <div className="page-head">
        <div>
          <span className="eyebrow">
            <b>01</b> / Live telemetry
          </span>
          <h1 className="page-title">Dashboard</h1>
          <p className="page-sub">
            Real-time indoor temperature and an LSTM-powered {HORIZON}-hour forecast.
          </p>
        </div>
        <div className="toolbar">
          <ConnectionPill status={connection} />
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
            className="btn btn--accent"
            onClick={() => fetchAll({ silent: true })}
            disabled={refreshing}
          >
            <RefreshIcon className={refreshing ? "spin" : ""} />
            {refreshing ? "Refreshing" : "Refresh"}
          </button>
        </div>
      </div>

      {error ? (
        <div className="panel panel--pad">
          <ErrorState
            title={connection === "offline" ? "Backend unreachable" : "Couldn't load data"}
            message={error}
            onRetry={() => fetchAll({ silent: true })}
          />
        </div>
      ) : (
        <>
          <div className="grid dash-grid">
            {/* Hero: latest reading */}
            <section className="panel col-hero rise rise-1">
              <div className="hero">
                <div className="hero__top">
                  <span className="eyebrow">Latest reading</span>
                  {fresh && <FreshnessPill level={fresh.level} label={fresh.label} />}
                </div>

                {latest ? (
                  <>
                    <div className="hero__readout">
                      <span className="hero__value">{heroValue}</span>
                      <span className="hero__unit">{sym}</span>
                    </div>
                    <div style={{ marginTop: 16 }}>
                      {spark.length > 1 ? (
                        <Sparkline data={spark} />
                      ) : (
                        <span className="faint mono" style={{ fontSize: 12 }}>
                          collecting trend…
                        </span>
                      )}
                    </div>
                    <div className="hero__foot">
                      <span className="dim" style={{ fontSize: 13 }}>
                        Updated {relativeTime(latest.timestamp)}
                      </span>
                      <span className="mono faint" style={{ fontSize: 12 }}>
                        device #{latest.device_id}
                      </span>
                    </div>
                  </>
                ) : loading ? (
                  <div style={{ marginTop: "auto", display: "grid", gap: 14 }}>
                    <Skeleton width="60%" height={72} radius={12} />
                    <Skeleton width="100%" height={44} />
                  </div>
                ) : (
                  <EmptyState
                    title="No readings yet"
                    message="The backend is online but hasn't received any sensor data."
                  />
                )}
              </div>
            </section>

            {/* Forecast chart */}
            <section className="panel panel--pad col-chart rise rise-2">
              <div className="panel__head">
                <div>
                  <span className="eyebrow">Forecast</span>
                  <div className="panel__title" style={{ marginTop: 4 }}>
                    Next {HORIZON} hours
                  </div>
                </div>
                {prediction?.generated_at && (
                  <span className="mono faint" style={{ fontSize: 12 }}>
                    generated {relativeTime(prediction.generated_at)}
                  </span>
                )}
              </div>

              {forecastData.length > 1 ? (
                <>
                  <div style={{ height: 280 }}>
                    <ForecastChart data={forecastData} unitSym={sym} />
                  </div>
                  <div className="hero__foot" style={{ borderTop: "1px solid var(--line)" }}>
                    {nextHour && (
                      <div className="stat" style={{ minHeight: "auto", gap: 4 }}>
                        <span className="stat__label">Next hour</span>
                        <span className="stat__value num" style={{ fontSize: 22 }}>
                          {formatTemp(nextHour.value, unit)}
                          <small>{sym}</small>
                          {trendChip(nextHour.delta) && (
                            <span style={{ marginLeft: 8 }}>
                              <TrendInline {...trendChip(nextHour.delta)} />
                            </span>
                          )}
                        </span>
                      </div>
                    )}
                    {horizonTrend != null && (
                      <div className="stat" style={{ minHeight: "auto", gap: 4, alignItems: "flex-end" }}>
                        <span className="stat__label">Over {HORIZON}h</span>
                        <span className="stat__value num" style={{ fontSize: 22 }}>
                          <TrendInline {...trendChip(horizonTrend)} />
                        </span>
                      </div>
                    )}
                  </div>
                </>
              ) : loading ? (
                <Skeleton height={300} radius={12} />
              ) : (
                <EmptyState
                  title="No forecast available"
                  message="Not enough recent readings for this device to generate a prediction yet."
                />
              )}
            </section>
          </div>

          {/* Metric strip */}
          <div className="grid dash-grid" style={{ marginTop: 18 }}>
            <div className="col-3 rise rise-3">
              <StatCard
                label="Today · average"
                value={todayAvg != null ? formatTemp(todayAvg, unit) : "—"}
                unit={todayAvg != null ? sym : ""}
                sub={new Date().toLocaleDateString()}
                muted={todayAvg == null}
              />
            </div>
            <div className="col-3 rise rise-3">
              <StatCard
                label="24h · range"
                value={
                  range
                    ? `${formatTemp(range.min, unit, 0)}–${formatTemp(range.max, unit, 0)}`
                    : "—"
                }
                unit={range ? sym : ""}
                sub={range ? "low → high" : "awaiting data"}
                muted={!range}
              />
            </div>
            <div className="col-3 rise rise-4">
              <StatCard
                label="Forecast · peak"
                value={forecastPeak != null ? formatTemp(forecastPeak, unit) : "—"}
                unit={forecastPeak != null ? sym : ""}
                sub={forecastPeak != null ? `within ${HORIZON}h` : "no forecast"}
                muted={forecastPeak == null}
              />
            </div>
            <div className="col-3 rise rise-4">
              <StatCard
                label="Readings · logged"
                value={history.length ? String(history.length) : "—"}
                sub={history.length ? "most recent window" : "none yet"}
                muted={!history.length}
              />
            </div>
          </div>
        </>
      )}
    </>
  );
}

function TrendInline({ dir, text }) {
  const cls =
    dir === "up" ? "trend--up" : dir === "down" ? "trend--down" : "trend--flat";
  return <span className={`trend ${cls}`} style={{ fontSize: 13 }}>{text}</span>;
}
