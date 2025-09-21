import React, { useEffect, useState } from "react";
import { getCurrentTemperature, getPredictions } from "../services/fakeApi";
import { Line } from "react-chartjs-2";
import "chart.js/auto";

export default function Dashboard() {
  const [current, setCurrent] = useState(null);
  const [predictions, setPredictions] = useState([]);

  useEffect(() => {
    setCurrent(getCurrentTemperature());
    setPredictions(getPredictions());
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Temperature Dashboard</h1>

      {current && (
        <div className="mb-6 p-4 bg-white shadow rounded">
          <p className="text-lg">
            Current Temperature in {current.city}:{" "}
            <span className="font-bold">{current.temp}{current.unit}</span>
          </p>
          <p className="text-sm text-gray-500">Last updated: {current.time}</p>
        </div>
      )}

      <div className="bg-white p-4 shadow rounded">
        <h2 className="text-lg font-semibold mb-2">Predictions</h2>
        <Line
          data={{
            labels: predictions.map((p) => p.time),
            datasets: [
              {
                label: "Temperature (°C)",
                data: predictions.map((p) => p.temp),
                borderColor: "rgb(59,130,246)",
                tension: 0.3,
              },
            ],
          }}
        />
      </div>
    </div>
  );
}
