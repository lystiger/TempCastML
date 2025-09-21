import React from "react";
import { BrowserRouter as Router, Routes, Route, Link } from "react-router-dom";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import About from "./pages/About";
import "./App.css"; 

export default function App() {
  return (
    <Router>
      <nav className="nav-links">
        <Link to="/">Dashboard</Link>
        <Link to="/history">History</Link>
        <Link to="/about">About</Link>
      </nav>

      <div style={{ paddingTop: "64px" }}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/history" element={<History />} />
          <Route path="/about" element={<About />} />
        </Routes>
      </div>
    </Router>
  );
}
