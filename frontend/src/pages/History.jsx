import React, { useEffect, useState } from "react";
import { getHistory } from "../services/fakeApi";
import "./history.css"; // new CSS for this page

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    setHistory(getHistory());
  }, []);

  return (
    <div className="history-wrapper">
      <div className="history-container">
        <h1>History</h1>
        <ul className="history-list">
          {history.map((h, idx) => (
            <li key={idx}>
              {h.date} — <span className="avg-temp">{h.avg}°C</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
