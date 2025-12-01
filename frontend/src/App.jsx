import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { Container, Navbar, Nav } from "react-bootstrap";
import { LinkContainer } from "react-router-bootstrap";
import { Toaster } from "react-hot-toast";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import About from "./pages/About";
import { TimeFormatProvider } from "./contexts/TimeFormatContext";

export default function App() {
  return (
    <Router>
      <Toaster position="top-right" reverseOrder={false} />
      <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
        <Container>
          <LinkContainer to="/">
            <Navbar.Brand>TempCastML</Navbar.Brand>
          </LinkContainer>
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              <LinkContainer to="/">
                <Nav.Link>Dashboard</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/history">
                <Nav.Link>History</Nav.Link>
              </LinkContainer>
              <LinkContainer to="/about">
                <Nav.Link>About</Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      <Container className="main-content-container mt-5 pt-3">
        <TimeFormatProvider>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/history" element={<History />} />
            <Route path="/about" element={<About />} />
          </Routes>
        </TimeFormatProvider>
      </Container>
    </Router>
  );
}
