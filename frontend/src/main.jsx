import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import 'bootstrap/dist/css/bootstrap.min.css'; // Import Bootstrap CSS
import './index.css'
import App from './App.jsx'
import { TemperatureUnitProvider } from './contexts/TemperatureUnitContext.jsx';

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <TemperatureUnitProvider>
      <App />
    </TemperatureUnitProvider>
  </StrictMode>,
)
