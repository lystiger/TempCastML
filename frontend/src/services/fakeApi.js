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
 * Simulates fetching historical sensor data with new fields.
 * @param {object} options - Options for fetching data (e.g., limit).
 * @returns {Array<Object>} An array of objects, each representing a historical sensor record.
 */
export function getHistoricalSensorData({ limit = 10 } = {}) {
  const data = [];
  const now = new Date();

  for (let i = 0; i < limit; i++) {
    const timestamp = new Date(now.getTime() - i * 3600 * 1000); // Go back in time by hours
    const temperature = parseFloat((Math.random() * 10 + 20).toFixed(2)); // 20-30 C
    const humidity = parseFloat((Math.random() * 30 + 50).toFixed(2)); // 50-80%
    const outside_temp = parseFloat((Math.random() * 15 + 15).toFixed(2)); // 15-30 C
    const outside_humidity = parseFloat((Math.random() * 40 + 40).toFixed(2)); // 40-80%
    const outside_pressure = parseFloat((Math.random() * 10 + 1000).toFixed(2)); // 1000-1010 hPa

    data.push({
      timestamp: timestamp.toISOString(),
      label_id: `label_${Math.floor(Math.random() * 5) + 1}`,
      session: `session_${Math.floor(Math.random() * 3) + 1}`,
      temperature: temperature,
      humidity: humidity,
      day_of_week: timestamp.toLocaleString('en-US', { weekday: 'short' }),
      hour_of_day: timestamp.getHours(),
      outside_temp: outside_temp,
      outside_humidity: outside_humidity,
      outside_pressure: outside_pressure,
      delta_temp: parseFloat((temperature - outside_temp).toFixed(2)),
      delta_humidity: parseFloat((humidity - outside_humidity).toFixed(2)),
    });
  }
  return data;
}
  