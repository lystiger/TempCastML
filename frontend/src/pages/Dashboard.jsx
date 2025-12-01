import React, { useEffect, useState } from "react";
import { getLatestSensorData, getPrediction } from "../services/api";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import { Row, Col, Card, Spinner, Alert, Button } from "react-bootstrap";
import toast from "react-hot-toast";

export default function Dashboard() {
  const [latestData, setLatestData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = async (showToast = false) => {
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
      if (showToast) {
        toast.success("Data refreshed successfully!");
      }
    } catch (err) {
      setError(
        "Failed to fetch data. Please make sure the backend server is running."
      );
      console.error(err);
      if (showToast) {
        toast.error("Failed to refresh data.");
      }
      throw err; // Re-throw the error to be caught by the caller
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // Set up an interval to fetch new data every 60 seconds
    const intervalId = setInterval(fetchData, 60000);

    // Clean up the interval on component unmount
    return () => clearInterval(intervalId);
  }, []);

  const handleRefresh = () => {
    const toastId = toast.loading("Refreshing data...");

    const timeoutPromise = new Promise((_, reject) =>
      setTimeout(() => {
        reject(new Error("Request timed out"));
      }, 8000)
    );

    Promise.race([fetchData(true), timeoutPromise])
      .catch(error => {
        if (error.message === "Request timed out") {
          toast.error("Failed to fetch new data: request timed out.", { id: toastId });
        }
        // Errors from fetchData are already handled within the function
      })
      .finally(() => {
        toast.dismiss(toastId);
      });
  };

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
      <div className="d-flex justify-content-between align-items-center mb-4">
        <h1>Dashboard</h1>
        <Button onClick={handleRefresh}>
          Refresh
        </Button>
      </div>
      <Row>
        <Col md={4} className="mb-4">
          <Card className="h-100 card-hover">
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
          <Card className="card-hover">
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
