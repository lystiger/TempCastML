// This file provides mock API functions to simulate backend responses during development.
// This is useful for frontend development when the backend API might not be fully ready or accessible.

/**
 * Simulates fetching the current temperature data.
 * @returns {Object} An object containing a mock temperature in Celsius and a timestamp.
 */
export function getCurrentTemperature() {
    return {
        temperature_c: 30,
        timestamp: "2025-09-20T16:00:00Z"
    };
}
  
/**
 * Simulates fetching temperature predictions.
 * @returns {Object} An object containing mock forecast and real (historical) temperature arrays.
 */
  export function getPredictions() {
    return {
        forecast: [31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8],
        real: [30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8, 7]
    };
}
  
/**
 * Simulates fetching historical temperature data.
 * @returns {Array<Object>} An array of objects, each representing a historical temperature record
 *                          with id, timestamp, temperature, device_id, forecast, and real values.
 */
export function getHistory() {
  return [
    { id: 1, timestamp: "2025-12-01T15:00:00Z", temperature_c: 29.5, device_id: 1, forecast: [30], real: [29] },
    { id: 2, timestamp: "2025-12-01T14:00:00Z", temperature_c: 30.1, device_id: 1, forecast: [31], real: [30] },
    { id: 3, timestamp: "2025-12-01T13:00:00Z", temperature_c: 31.2, device_id: 1, forecast: [32], real: [31] },
    { id: 4, timestamp: "2025-12-01T12:00:00Z", temperature_c: 30.8, device_id: 1, forecast: [31], real: [30] },
    { id: 5, timestamp: "2025-09-20T11:00:00Z", temperature_c: 29.9, device_id: 1, forecast: [30], real: [29] },
  ];
}
  