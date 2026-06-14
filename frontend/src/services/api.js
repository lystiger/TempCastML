// API client for the TempCastML backend (FastAPI).
//
// Contract (see backend/Routes + backend/Database/models.py):
//   GET /                       -> { message }                         (health)
//   GET /sensor/latest          -> Reading { id, device_id, temperature_c, timestamp }
//   GET /sensor/history?limit=N -> Reading[]
//   GET /predict/?device_id&horizon -> { device_id, generated_at, horizon_hours, forecast: number[] }
//
// The backend returns 404 when a resource exists but holds no data yet
// (e.g. no readings collected). We surface that as an *empty* state, distinct
// from a connection/server failure, so the UI never hides real errors.

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export class ApiError extends Error {
  /** @param {number} status HTTP status, or 0 for a network/transport failure. */
  constructor(status, message) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function request(path, { signal } = {}) {
  let res;
  try {
    res = await fetch(`${API_BASE_URL}${path}`, { signal });
  } catch (err) {
    if (err?.name === "AbortError") throw err;
    // fetch only rejects on network/transport failure -> backend unreachable.
    throw new ApiError(0, "Cannot reach the backend.");
  }
  if (!res.ok) {
    throw new ApiError(res.status, `Request failed (${res.status}).`);
  }
  return res.json();
}

/** Lightweight liveness probe used for the connection badge. */
export const getHealth = async (signal) => {
  try {
    await request("/", { signal });
    return true;
  } catch (err) {
    if (err?.name === "AbortError") throw err;
    return false;
  }
};

/** Latest reading, or null when no readings have been collected yet. */
export const getLatestSensorData = async (signal) => {
  try {
    return await request("/sensor/latest", { signal });
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
};

/** Historical readings (newest first), or [] when none exist. */
export const getHistoricalSensorData = async (params = {}, signal) => {
  const query = new URLSearchParams(params).toString();
  try {
    return await request(`/sensor/history${query ? `?${query}` : ""}`, { signal });
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return [];
    throw err;
  }
};

/** Forecast for a device, or null when there isn't enough data to predict. */
export const getPrediction = async (device_id = 1, horizon = 24, signal) => {
  try {
    return await request(
      `/predict/?device_id=${device_id}&horizon=${horizon}`,
      { signal }
    );
  } catch (err) {
    if (err instanceof ApiError && err.status === 404) return null;
    throw err;
  }
};
