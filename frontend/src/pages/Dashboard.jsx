import React, { useEffect, useState } from "react";
import { getCurrentTemperature, getPredictions } from "../services/fakeApi";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import "./dashboard.css"; // import the CSS we will create

export default function Dashboard() {
  const [current, setCurrent] = useState(null);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    setCurrent(getCurrentTemperature());
    setPredictions(getPredictions());
  }, []);

  return (
    <div className="dashboard-wrapper">
      <div className="dashboard-container">
        <h1>Temperature Dashboard</h1>

        {current && (
          <div className="current-temp">
            <p>
              Current Temperature in {current.city}:{" "}
              <span className="temp-value">
                {current.temp}
                {current.unit}
              </span>
            </p>
            <p className="updated-time">Last updated: {current.time}</p>
          </div>
        )}

        <div className="predictions">
          <h2>Predictions</h2>
          <Line
            data={{
              labels: predictions.map((p) => p.time),
              datasets: [
                {
                  label: "Temperature (°C)",
                  data: predictions.map((p) => p.temp),
                  borderColor: "#3B82F6",
                  tension: 0.3,
                },
              ],
            }}
          />
        </div>
      </div>
    </div>
  );
}
