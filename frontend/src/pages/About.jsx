import React from "react";
import { Card } from "react-bootstrap";

export default function About() {
  return (
    <>
      <h1 className="mb-4">About TempCastML</h1>
      <Card>
        <Card.Body>
          <Card.Title>A Machine Learning Powered Temperature Forecasting Tool</Card.Title>
          <Card.Text>
            This application provides real-time temperature monitoring and future forecasting
            using a Long Short-Term Memory (LSTM) neural network.
          </Card.Text>
          <hr />
          <h5>Components:</h5>
          <ul>
            <li>
              <strong>Data Ingestion:</strong> A Python backend service collects temperature
              data, which can be sourced from hardware sensors like an Arduino.
            </li>
            <li>
              <strong>API:</strong> A FastAPI server provides RESTful endpoints for accessing
              the latest sensor readings, historical data, and ML-powered predictions.
            </li>
            <li>
              <strong>Frontend:</strong> A responsive user interface built with React and
              Bootstrap for visualizing data and forecasts.
            </li>
            <li>
              <strong>Machine Learning Model:</strong> An LSTM model trained on historical
              time-series data to predict future temperature trends.
            </li>
          </ul>
        </Card.Body>
      </Card>
    </>
  );
}
