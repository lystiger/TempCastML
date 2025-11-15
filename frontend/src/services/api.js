const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

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
    // Depending on your error handling strategy, you might want to re-throw or return a specific error object
    throw error;
  }
};

export const getPrediction = async (device_id = 1, horizon = 24) => {
  try {
    // Note the trailing slash on /predict/ to match the backend router
    const response = await fetch(`${API_BASE_URL}/predict/?device_id=${device_id}&horizon=${horizon}`);
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

// You can add more API functions here as needed, e.g., for historical data
export const getHistoricalSensorData = async (params = {}) => {
  const query = new URLSearchParams(params).toString();
  try {
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
