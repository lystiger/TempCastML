import React, { useEffect, useState } from "react";
import { getLatestSensorData, getPrediction } from "../services/api";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import { Row, Col, Card, Spinner, Alert } from "react-bootstrap";

export default function Dashboard() {
  const [latestData, setLatestData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);

        // Fetch both latest data and predictions
        const [latest, prediction] = await Promise.all([
          getLatestSensorData(),
          getPrediction(1, 24), // Using device_id=1 and horizon=24 as example
        ]);

        setLatestData(latest);
        setPredictionData(prediction);
      } catch (err) {
        setError(
          "Failed to fetch data. Please make sure the backend server is running."
        );
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
    // Set up an interval to fetch new data every 60 seconds
    const intervalId = setInterval(fetchData, 60000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const chartData = {
    labels: predictionData?.forecast.map((_, index) => `+${index + 1}h`),
    datasets: [
      {
        label: "Predicted Temperature (°C)",
        data: predictionData?.forecast,
        borderColor: "#0d6efd",
        backgroundColor: "rgba(13, 110, 253, 0.1)",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: "80vh" }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <h4 className="ms-3">Loading Dashboard...</h4>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <>
      <h1 className="mb-4">Dashboard</h1>
      <Row>
        <Col md={4} className="mb-4">
          <Card className="h-100">
            <Card.Body>
              <Card.Title>Latest Sensor Reading</Card.Title>
              {latestData ? (
                <>
                  <div className="display-4 fw-bold">
                    {latestData.temperature_c.toFixed(1)}°C
                  </div>
                  <Card.Text className="text-muted">
                    Last updated: {new Date(latestData.timestamp).toLocaleString()}
                  </Card.Text>
                </>
              ) : (
                <Card.Text>No latest data available.</Card.Text>
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col md={8} className="mb-4">
          <Card>
            <Card.Body>
              <Card.Title>24-Hour Temperature Forecast</Card.Title>
              {predictionData ? (
                <Line data={chartData} />
              ) : (
                <Card.Text>No prediction data available.</Card.Text>
              )}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}
