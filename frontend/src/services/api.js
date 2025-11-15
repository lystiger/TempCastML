import { getCurrentTemperature, getPredictions, getHistory } from './fakeApi';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// 
export const getLatestSensorData = async () => {
  try {
    const data = getCurrentTemperature();
    return data;
  } catch (error) {
    console.error("Failed to fetch latest sensor data:", error);
    throw error;
  }
};

export const getPrediction = async (device_id = 1, horizon = 24) => {
  try {
    const data = getPredictions();
    return data;
  } catch (error) {
    console.error("Failed to fetch prediction:", error);
    throw error;
  }
};

// You can add more API functions here as needed, e.g., for historical data
export const getHistoricalSensorData = async (params = {}) => {
  try {
    const data = getHistory();
    return data;
  } catch (error) {
    console.error("Failed to fetch historical sensor data:", error);
    throw error;
  }
};
