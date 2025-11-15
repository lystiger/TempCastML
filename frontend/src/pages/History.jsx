import React, { useEffect, useState } from "react";
import { getHistoricalSensorData } from "../services/api";
import { Table, Spinner, Alert } from "react-bootstrap";

export default function History() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
        <Table striped bordered hover responsive>
          <thead>
            <tr>
              <th>#</th>
              <th>Timestamp</th>
              <th>Temperature (°C)</th>
              <th>Device ID</th>
            </tr>
          </thead>
          <tbody>
            {history.map((reading, index) => (
              <tr key={reading.id}>
                <td>{index + 1}</td>
                <td>{new Date(reading.timestamp).toLocaleString()}</td>
                <td>{reading.temperature_c.toFixed(2)}</td>
                <td>{reading.device_id}</td>
              </tr>
            ))}
          </tbody>
        </Table>
      ) : (
        <Alert variant="info">No historical data available.</Alert>
      )}
    </>
  );
}
