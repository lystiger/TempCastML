import React, { useEffect, useState, useContext } from "react";
import { getHistoricalSensorData } from "../services/api";
import { Table, Spinner, Alert, Row, Col, Card } from "react-bootstrap";
import { TimeFormatContext } from "../contexts/TimeFormatContext";
import { TemperatureUnitContext } from "../contexts/TemperatureUnitContext";

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const { is24hFormat } = useContext(TimeFormatContext);
  const { unit } = useContext(TemperatureUnitContext);

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

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        setLoading(true);
        setError(null);
        // Fetch last 100 readings as an example
        const data = await getHistoricalSensorData({ limit: 100 });
        setHistory(data);
      } catch (err) {
        setError(
          "Failed to fetch historical data. Please make sure the backend server is running."
        );
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchHistory();
  }, []);

  if (loading) {
    return (
      <div className="d-flex justify-content-center align-items-center" style={{ height: "80vh" }}>
        <Spinner animation="border" role="status">
          <span className="visually-hidden">Loading...</span>
        </Spinner>
        <h4 className="ms-3">Loading History...</h4>
      </div>
    );
  }

  if (error) {
    return <Alert variant="danger">{error}</Alert>;
  }

  return (
    <>
      <h1 className="mb-4">Sensor Reading History</h1>
      {history.length > 0 ? (
        <Table striped bordered hover responsive className="card-hover">
          <thead>
            <tr>
              <th>ID</th>
              <th>Timestamp</th>
              <th>Temperature ({getUnitSymbol()})</th>
              <th>Device ID</th>
              <th>Forecast ({getUnitSymbol()})</th>
              <th>Real ({getUnitSymbol()})</th>
            </tr>
          </thead>
          <tbody>
            {history.map((reading) => (
              <tr key={reading.id}>
                <td>{reading.id}</td>
                <td>{new Date(reading.timestamp).toLocaleString([], { hour12: !is24hFormat })}</td>
                <td>{convertTemperature(reading.temperature_c)?.toFixed(2)}</td>
                <td>{reading.device_id}</td>
                <td>{reading.forecast && reading.forecast.length > 0 ? convertTemperature(reading.forecast[0]).toFixed(2) : "N/A"}</td>
                <td>{reading.real && reading.real.length > 0 ? convertTemperature(reading.real[0]).toFixed(2) : "N/A"}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      ) : (
        <Alert variant="info">No historical data available.</Alert>
      )}

      <Row>
        <Col md={12} className="mb-4">
          <Card className="card-hover">
            <Card.Body>
              <Card.Title>Glossary</Card.Title>
              <ul>
                <li><strong>ID:</strong> Unique identifier for each sensor reading.</li>
                <li><strong>Timestamp:</strong> The date and time when the sensor reading was recorded.</li>
                <li><strong>Temperature ({getUnitSymbol()}):</strong> The actual temperature recorded by the sensor in {unit}.</li>
                <li><strong>Device ID:</strong> The identifier of the sensor device.</li>
                <li><strong>Forecast ({getUnitSymbol()}):</strong> The predicted temperature for a future point in time, in {unit}.</li>
                <li><strong>Real ({getUnitSymbol()}):</strong> The actual temperature observed at a future point in time, in {unit}.</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}
