// This file is responsible for making API calls to the backend.
// During development, it currently imports functions from `fakeApi.js` to simulate backend responses.
// In a production environment, these would typically be actual HTTP requests (e.g., using axios or the built-in fetch API)
// to a live backend server.

// Define the base URL for the API. It tries to use an environment variable `VITE_API_URL`
// (common in Vite projects) or defaults to `http://localhost:8000/api` for local development.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Fetches the latest sensor data.
 * @returns {Promise<Object>} A promise that resolves with the latest sensor data.
 */
export const getLatestSensorData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/sensor/latest`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch latest sensor data:", error);
    throw error;
  }
};

/**
 * Fetches predictions.
 * @param {number} device_id - The ID of the device.
 * @param {number} horizon - The prediction horizon (e.g., 24 hours).
 * @returns {Promise<Object>} A promise that resolves with prediction data.
 */
export const getPrediction = async (device_id = 1, horizon = 24) => {
  try {
    const response = await fetch(`${API_BASE_URL}/predict?device_id=${device_id}&horizon=${horizon}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch prediction:", error);
    throw error;
  }
};

/**
 * Fetches historical sensor data.
 * @param {Object} params - Parameters for filtering historical data (e.g., date range, device_id).
 * @returns {Promise<Object>} A promise that resolves with historical sensor data.
 */
export const getHistoricalSensorData = async (params = {}) => {
  try {
    const query = new URLSearchParams(params).toString();
    const response = await fetch(`${API_BASE_URL}/sensor/history?${query}`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch historical sensor data:", error);
    throw error;
  }
};
