import { Suspense, lazy, useContext } from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { Toaster } from "react-hot-toast";

import { TopNav } from "./components/TopNav";
import { Footer } from "./components/Footer";
import { PageLoader } from "./components/States";

import { TimeFormatProvider, TimeFormatContext } from "./contexts/TimeFormatContext";

// Route-level code splitting keeps the chart library (recharts) out of the
// initial bundle — it loads with the Dashboard / History routes that use it.
const Dashboard = lazy(() => import("./pages/Dashboard"));
const History = lazy(() => import("./pages/History"));
const About = lazy(() => import("./pages/About"));

function Shell() {
  const { is24hFormat } = useContext(TimeFormatContext);
  return (
    <div className="app">
      <TopNav is24h={is24hFormat} />
      <main className="main">
        <div className="container">
          <Suspense fallback={<PageLoader />}>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/history" element={<History />} />
              <Route path="/about" element={<About />} />
            </Routes>
          </Suspense>
        </div>
      </main>
      <Footer />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <TimeFormatProvider>
        <Toaster
          position="top-right"
          toastOptions={{
            style: {
              background: "#0f1217",
              color: "#eef1f5",
              border: "1px solid rgba(255,255,255,0.14)",
              borderRadius: "12px",
              fontSize: "13.5px",
              boxShadow: "0 24px 48px -28px rgba(0,0,0,0.9)",
            },
            success: { iconTheme: { primary: "#46e08a", secondary: "#0f1217" } },
            error: { iconTheme: { primary: "#ff5c5c", secondary: "#0f1217" } },
          }}
        />
        <Shell />
      </TimeFormatProvider>
    </BrowserRouter>
  );
}
