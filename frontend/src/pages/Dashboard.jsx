import React, { useEffect, useState, useContext } from "react";
import { getLatestSensorData, getPrediction, getHistoricalSensorData } from "../services/api";
import { Line } from "react-chartjs-2";
import "chart.js/auto";
import { Row, Col, Card, Spinner, Alert, Button, Form } from "react-bootstrap";
import toast from "react-hot-toast";
import { TimeFormatContext } from "../contexts/TimeFormatContext";
import { TemperatureUnitContext } from "../contexts/TemperatureUnitContext";

export default function Dashboard() {
  const [latestData, setLatestData] = useState(null);
  const [predictionData, setPredictionData] = useState(null);
  const [historicalData, setHistoricalData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { is24hFormat, setIs24hFormat } = useContext(TimeFormatContext);
  const { unit, toggleUnit } = useContext(TemperatureUnitContext);

  const convertTemperature = (temp) => {
    if (unit === 'fahrenheit') {
      return (temp * 9/5) + 32;
    }
    if (unit === 'kelvin') {
      return temp + 273.15;
    }
    return temp;
  };

  const getUnitSymbol = () => {
    if (unit === 'fahrenheit') {
      return '°F';
    }
    if (unit === 'kelvin') {
      return 'K';
    }
    return '°C';
  };

  const fetchData = async (showToast = false) => {
    try {
      setLoading(true);
      setError(null);

      // Fetch all data
      const [latest, prediction, history] = await Promise.all([
        getLatestSensorData(),
        getPrediction(1, 24), // Using device_id=1 and horizon=24 as example
        getHistoricalSensorData(),
      ]);

      setLatestData(latest);
      setPredictionData(prediction);
      setHistoricalData(history);

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

  const getTodayAverage = () => {
    if (!historicalData) return 0;
    const today = new Date().toLocaleDateString();
    const todayData = historicalData.filter(
      (d) => new Date(d.timestamp).toLocaleDateString() === today
    );
    if (todayData.length === 0) return 0;
    const total = todayData.reduce((acc, curr) => acc + curr.temperature_c, 0);
    return convertTemperature(total / todayData.length).toFixed(1);
  };

  const chartData = {
    labels: predictionData?.forecast.map((_, index) => `+${index + 1}h`),
    datasets: [
      {
        label: `Predicted Temperature (${getUnitSymbol()})`,
        data: predictionData?.forecast.map(convertTemperature),
        borderColor: "#0d6efd",
        backgroundColor: "rgba(13, 110, 253, 0.1)",
        fill: true,
        tension: 0.4,
      },
      {
        label: `Real Temperature (${getUnitSymbol()})`,
        data: predictionData?.real.map(convertTemperature),
        borderColor: "#fd7e14",
        backgroundColor: "rgba(253, 126, 20, 0.1)",
        fill: true,
        tension: 0.4,
      },
    ],
  };

  const handleTimeFormatToggle = () => {
    setIs24hFormat(!is24hFormat);
    toast.success(`Switched to ${!is24hFormat ? "24h" : "12h"} format`);
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
        <div className="d-flex align-items-center">
          <Form.Group as={Row} className="mb-0 me-3">
            <Col sm={12}>
              <Form.Select onChange={(e) => {
                toggleUnit(e.target.value);
                toast.success(`Switched to ${e.target.value.charAt(0).toUpperCase() + e.target.value.slice(1)}`);
              }} value={unit}>
                <option value="celsius">Celsius</option>
                <option value="fahrenheit">Fahrenheit</option>
                <option value="kelvin">Kelvin</option>
              </Form.Select>
            </Col>
          </Form.Group>
          <Button onClick={handleTimeFormatToggle} className="me-2">
            {is24hFormat ? "Switch to 12h" : "Switch to 24h"}
          </Button>
          <Button onClick={handleRefresh}>
            Refresh
          </Button>
        </div>
      </div>
      <Row>
        <Col md={4} className="d-flex flex-column">
          <Row>
            <Col className="mb-4">
              <Card className="h-100 card-hover">
                <Card.Body>
                  <Card.Title>Latest Sensor Prediction</Card.Title>
                  {latestData ? (
                    <>
                      <div className="display-4 fw-bold">
                        {convertTemperature(latestData.temperature_c).toFixed(1)}{getUnitSymbol()}
                      </div>
                      <Card.Text className="text-muted">
                        Last updated: {new Date(latestData.timestamp).toLocaleString([], { hour12: !is24hFormat })}
                      </Card.Text>
                    </>
                  ) : (
                    <Card.Text>No latest data available.</Card.Text>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
          <Row>
            <Col className="mb-4">
              <Card className="h-100 card-hover">
                <Card.Body>
                  <Card.Title>Today's Temperature</Card.Title>
                  {historicalData ? (
                    <>
                      <div className="display-4 fw-bold">
                        {getTodayAverage()}{getUnitSymbol()}
                      </div>
                      <Card.Text className="text-muted">
                        {new Date().toLocaleDateString()}
                      </Card.Text>
                    </>
                  ) : (
                    <Card.Text>No historical data available.</Card.Text>
                  )}
                </Card.Body>
              </Card>
            </Col>
          </Row>
        </Col>
        <Col md={8} className="mb-4">
          <Card className="h-100 card-hover">
            <Card.Body>
              <Card.Title>{is24hFormat ? "24-Hour" : "12-Hour"} Temperature Forecast</Card.Title>
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
