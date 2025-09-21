import React, { useEffect, useState } from "react";
import { getHistory } from "../services/fakeApi";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    setHistory(getHistory());
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">History</h1>
      <ul className="bg-white p-4 shadow rounded">
        {history.map((h, idx) => (
          <li key={idx} className="py-2 border-b last:border-0">
            {h.date} — <span className="font-semibold">{h.avg}°C</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
