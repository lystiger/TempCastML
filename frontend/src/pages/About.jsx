import React, { useEffect, useState } from "react";
import { getHistory } from "../services/fakeApi";
import "./about.css"; // new CSS for this page

export default function About() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    setHistory(getHistory());
  }, []);

  return (
    <div className="about-wrapper">
      <div className="about-container">
        <h1>About</h1>
          <p>This website using the fake API, it will later be connected to the real backend later</p>
      </div>
    </div>
  );
}
