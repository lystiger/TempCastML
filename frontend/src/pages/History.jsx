import React, { useEffect, useState, useContext } from "react";
import { getHistoricalSensorData } from "../services/fakeApi";
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
              <th>Timestamp</th>
              <th>Label ID</th>
              <th>Session</th>
              <th>Temperature ({getUnitSymbol()})</th>
              <th>Humidity</th>
              <th>Day of Week</th>
              <th>Hour of Day</th>
              <th>Outside Temp ({getUnitSymbol()})</th>
              <th>Outside Humidity</th>
              <th>Outside Pressure</th>
              <th>Delta Temp ({getUnitSymbol()})</th>
              <th>Delta Humidity</th>
            </tr>
          </thead>
          <tbody>
            {history.map((reading, index) => (
              <tr key={index}>
                <td>{new Date(reading.timestamp).toLocaleString([], { hour12: !is24hFormat })}</td>
                <td>{reading.label_id}</td>
                <td>{reading.session}</td>
                <td>{convertTemperature(reading.temperature)?.toFixed(2)}</td>
                <td>{reading.humidity?.toFixed(2)}</td>
                <td>{reading.day_of_week}</td>
                <td>{reading.hour_of_day}</td>
                <td>{convertTemperature(reading.outside_temp)?.toFixed(2)}</td>
                <td>{reading.outside_humidity?.toFixed(2)}</td>
                <td>{reading.outside_pressure?.toFixed(2)}</td>
                <td>{convertTemperature(reading.delta_temp)?.toFixed(2)}</td>
                <td>{reading.delta_humidity?.toFixed(2)}</td>
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
                <li><strong>Timestamp:</strong> The date and time when the sensor reading was recorded.</li>
                <li><strong>Label ID:</strong> A unique identifier for the specific data label.</li>
                <li><strong>Session:</strong> The identifier for the data collection session.</li>
                <li><strong>Temperature ({getUnitSymbol()}):</strong> The indoor temperature recorded by the sensor in {unit}.</li>
                <li><strong>Humidity:</strong> The indoor humidity recorded by the sensor.</li>
                <li><strong>Day of Week:</strong> The day of the week when the reading was taken.</li>
                <li><strong>Hour of Day:</strong> The hour of the day when the reading was taken.</li>
                <li><strong>Outside Temp ({getUnitSymbol()}):</strong> The outdoor temperature at the time of the reading, in {unit}.</li>
                <li><strong>Outside Humidity:</strong> The outdoor humidity at the time of the reading.</li>
                <li><strong>Outside Pressure:</strong> The outdoor atmospheric pressure at the time of the reading.</li>
                <li><strong>Delta Temp ({getUnitSymbol()}):</strong> The difference between indoor and outdoor temperature, in {unit}.</li>
                <li><strong>Delta Humidity:</strong> The difference between indoor and outdoor humidity.</li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  );
}
