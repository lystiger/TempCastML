// Import necessary modules from React and ReactDOM.
// StrictMode is a tool for highlighting potential problems in an application.
// createRoot is used to create a root for concurrent mode, which enables new features.
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'

// Import Bootstrap CSS for styling the application.
import 'bootstrap/dist/css/bootstrap.min.css'; 
// Import the main CSS file for global styles.
import './index.css'
// Import the main App component, which is the root of our application's component tree.
import App from './App.jsx'
// Import the TemperatureUnitProvider to manage temperature unit state across the application.
import { TemperatureUnitProvider } from './contexts/TemperatureUnitContext.jsx';

// Get the root DOM element where the React application will be mounted.
// The 'root' element is typically defined in public/index.html.
createRoot(document.getElementById('root')).render(
  // StrictMode activates additional checks and warnings for its descendants.
  <StrictMode>
    {/* TemperatureUnitProvider makes the temperature unit state available to all child components. */}
    <TemperatureUnitProvider>
      {/* The main application component is rendered here. */}
      <App />
    </TemperatureUnitProvider>
  </StrictMode>,
)
