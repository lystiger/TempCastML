// This file is responsible for making API calls to the backend.
// During development, it currently imports functions from `fakeApi.js` to simulate backend responses.
// In a production environment, these would typically be actual HTTP requests (e.g., using axios or the built-in fetch API)
// to a live backend server.
import { getCurrentTemperature, getPredictions, getHistory } from './fakeApi';

// Define the base URL for the API. It tries to use an environment variable `VITE_API_URL`
// (common in Vite projects) or defaults to `http://localhost:8000/api` for local development.
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

/**
 * Fetches the latest sensor data.
 * Currently, this calls a function from `fakeApi.js` to get mock data.
 * In a real application, this would make an HTTP GET request to an endpoint like `${API_BASE_URL}/sensor/latest`.
 * @returns {Promise<Object>} A promise that resolves with the latest sensor data.
 */
export const getLatestSensorData = async () => {
  try {
    // Simulate fetching data from a backend.
    const data = getCurrentTemperature();
    return data;
  } catch (error) {
    console.error("Failed to fetch latest sensor data:", error);
    throw error;
  }
};

/**
 * Fetches predictions.
 * Currently, this calls a function from `fakeApi.js` to get mock prediction data.
 * In a real application, this would make an HTTP GET request to an endpoint like `${API_BASE_URL}/predict`.
 * @param {number} device_id - The ID of the device (currently unused in fakeApi).
 * @param {number} horizon - The prediction horizon (e.g., 24 hours, currently unused in fakeApi).
 * @returns {Promise<Object>} A promise that resolves with prediction data.
 */
export const getPrediction = async (device_id = 1, horizon = 24) => {
  try {
    // Simulate fetching prediction data from a backend.
    const data = getPredictions();
    return data;
  } catch (error) {
    console.error("Failed to fetch prediction:", error);
    throw error;
  }
};

/**
 * Fetches historical sensor data.
 * Currently, this calls a function from `fakeApi.js` to get mock historical data.
 * In a real application, this would make an HTTP GET request to an endpoint like `${API_BASE_URL}/sensor/history`.
 * @param {Object} params - Parameters for filtering historical data (e.g., date range, device_id).
 * @returns {Promise<Object>} A promise that resolves with historical sensor data.
 */
export const getHistoricalSensorData = async (params = {}) => {
  try {
    // Simulate fetching historical data from a backend.
    const data = getHistory();
    return data;
  } catch (error) {
    console.error("Failed to fetch historical sensor data:", error);
    throw error;
  }
};
