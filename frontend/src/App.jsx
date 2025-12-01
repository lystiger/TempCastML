// Import React library.
import React from "react";
// Import routing components from react-router-dom for navigation.
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
// Import Bootstrap components for layout and navigation.
import { Container, Navbar, Nav } from "react-bootstrap";
// LinkContainer integrates react-router with react-bootstrap Nav.Link components.
import { LinkContainer } from "react-router-bootstrap";
// Toaster is used for displaying notifications (e.g., success or error messages).
import { Toaster } from "react-hot-toast";

// Import page components that will be rendered based on the route.
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import About from "./pages/About";

// Import the TimeFormatProvider to manage time format state across the application.
import { TimeFormatProvider } from "./contexts/TimeFormatContext";

// The main App component, serving as the root of the application's UI.
export default function App() {
  return (
    // Router enables client-side routing for the application.
    <Router>
      {/* Toaster component for displaying notifications. Positioned at top-right. */}
      <Toaster position="top-right" reverseOrder={false} />

      {/* Navbar component for application navigation. */}
      <Navbar bg="dark" variant="dark" expand="lg" fixed="top">
        <Container>
          {/* Brand logo/name that links to the home page. */}
          <LinkContainer to="/">
            <Navbar.Brand>TempCastML</Navbar.Brand>
          </LinkContainer>
          {/* Toggler for responsive navigation on smaller screens. */}
          <Navbar.Toggle aria-controls="basic-navbar-nav" />
          {/* Collapsible navigation links. */}
          <Navbar.Collapse id="basic-navbar-nav">
            <Nav className="me-auto">
              {/* Navigation link to the Dashboard page. */}
              <LinkContainer to="/">
                <Nav.Link>Dashboard</Nav.Link>
              </LinkContainer>
              {/* Navigation link to the History page. */}
              <LinkContainer to="/history">
                <Nav.Link>History</Nav.Link>
              </LinkContainer>
              {/* Navigation link to the About page. */}
              <LinkContainer to="/about">
                <Nav.Link>About</Nav.Link>
              </LinkContainer>
            </Nav>
          </Navbar.Collapse>
        </Container>
      </Navbar>

      {/* Main content container with top margin and padding to account for fixed navbar. */}
      <Container className="main-content-container mt-5 pt-3">
        {/* TimeFormatProvider makes the time format state available to all child components within this section. */}
        <TimeFormatProvider>
          {/* Routes define which component to render based on the URL path. */}
          <Routes>
            {/* Route for the home page, rendering the Dashboard component. */}
            <Route path="/" element={<Dashboard />} />
            {/* Route for the /history path, rendering the History component. */}
            <Route path="/history" element={<History />} />
            {/* Route for the /about path, rendering the About component. */}
            <Route path="/about" element={<About />} />
          </Routes>
        </TimeFormatProvider>
      </Container>
    </Router>
  );
}
