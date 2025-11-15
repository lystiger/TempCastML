# Connecting the Backend and Frontend

This document outlines the strategy for connecting the React frontend to the Python backend for the TempCastML project. The connection will be established via a RESTful API.

## High-Level Architecture

The architecture follows a standard client-server model:

-   **Backend (Server):** A Python application (likely using a framework like Flask or FastAPI) will run on a specific port (e.g., `5000`). It will expose several API endpoints to provide data.
-   **Frontend (Client):** The React application, running on its own development server (e.g., `vite` on port `5173`), will make HTTP requests to the backend's API endpoints to fetch and display data.

```
+--------------------------------+      +--------------------------------+
|                                |      |                                |
|      React Frontend            |      |      Python Backend            |
| (localhost:5173)               |      | (localhost:5000)               |
|                                |      |                                |
+--------------------------------+      +--------------------------------+
           |                                          ^
           |           HTTP Requests                  |
           | (e.g., GET /api/sensors/latest)          |
           +----------------------------------------->+
           <-----------------------------------------+
                      JSON Responses
```

## Action Plan

### 1. Backend: Expose API Endpoints

The Python backend needs to provide endpoints for the frontend to consume. Based on the project structure, these routes should be defined in the `Backend/Routes/` directory and registered in `Backend/main.py`.

**Key Endpoints to Create:**

-   `GET /api/sensors/latest`: Returns the most recent sensor reading from `latest_data.json` or the database.
-   `GET /api/sensors/history`: Returns a list of historical sensor data, with optional pagination.
-   `GET /api/predict`: Returns the latest temperature prediction from the `LTSM.py` model.

**Important Consideration: CORS (Cross-Origin Resource Sharing)**

Since the frontend and backend are running on different ports (`5173` vs. `5000`), the browser will block HTTP requests by default. The backend must be configured to allow requests from the frontend's origin.

If using **Flask**, this can be done with the `flask-cors` library:

```python
# In Backend/main.py
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
# Allow requests from the default Vite dev server origin
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

# ... register routes ...
```

### 2. Frontend: Consume the API

The frontend will use the `fetch` API or a library like `axios` to make requests to the backend. The file `frontend/src/services/api.js` is the ideal place to centralize all API communication logic.

**Example `frontend/src/services/api.js`:**

```javascript
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000/api';

export const getLatestSensorData = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/sensors/latest`);
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Failed to fetch latest sensor data:", error);
    return null; // Or handle the error as needed
  }
};

export const getPrediction = async () => {
    // ... similar fetch logic for the /api/predict endpoint
};
```

**Using the service in a React Component (`Dashboard.jsx`):**

```jsx
import React, { useState, useEffect } from 'react';
import { getLatestSensorData } from '../services/api';

function Dashboard() {
  const [latestData, setLatestData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      const data = await getLatestSensorData();
      setLatestData(data);
      setLoading(false);
    };

    fetchData();
    // Optional: Poll for new data every 30 seconds
    const intervalId = setInterval(fetchData, 30000);

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  if (loading) {
    return <div>Loading data...</div>;
  }

  if (!latestData) {
    return <div>Could not load data. Is the backend running?</div>;
  }

  return (
    <div>
      <h2>Latest Sensor Reading</h2>
      <p>Temperature: {latestData.temperature}°C</p>
      <p>Humidity: {latestData.humidity}%</p>
      <p>Timestamp: {new Date(latestData.timestamp).toLocaleString()}</p>
    </div>
  );
}

export default Dashboard;
```

### 3. Configuration and Environment

To avoid hardcoding URLs, we should use environment variables.

-   **Frontend:** Create a `.env.local` file in the `frontend/` directory. Vite uses variables prefixed with `VITE_`.

    ```
    # frontend/.env.local
    VITE_API_URL=http://localhost:5000/api
    ```

This makes it easy to change the API endpoint for production vs. development environments.

## How to Run

1.  **Start the Backend:**
    ```bash
    cd Backend
    # Activate virtual environment if you have one
    # source venv/bin/activate
    pip install -r requirements.txt
    python main.py
    ```
    *(This assumes `main.py` is configured to run a web server)*

2.  **Start the Frontend:**
    ```bash
    cd frontend
    npm install
    npm run dev
    ```

Now, when you open the React application in your browser, it will fetch data from the running Python backend.
