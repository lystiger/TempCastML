import { StrictMode } from "react";
import { createRoot } from "react-dom/client";

import "./index.css";
import App from "./App.jsx";
import { TemperatureUnitProvider } from "./contexts/TemperatureUnitContext.jsx";

createRoot(document.getElementById("root")).render(
  <StrictMode>
    <TemperatureUnitProvider>
      <App />
    </TemperatureUnitProvider>
  </StrictMode>
);
