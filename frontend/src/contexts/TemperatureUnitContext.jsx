// Provides the active temperature unit ('celsius' | 'fahrenheit' | 'kelvin')
// to the whole app, persisted across reloads.
import { createContext, useEffect, useState } from "react";

// Context + Provider intentionally co-located (consumed across the app).
// eslint-disable-next-line react-refresh/only-export-components
export const TemperatureUnitContext = createContext();

const STORAGE_KEY = "tempcast.unit";
const VALID = ["celsius", "fahrenheit", "kelvin"];

export const TemperatureUnitProvider = ({ children }) => {
  const [unit, setUnit] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return VALID.includes(saved) ? saved : "celsius";
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, unit);
  }, [unit]);

  const toggleUnit = (newUnit) => {
    if (VALID.includes(newUnit)) setUnit(newUnit);
  };

  return (
    <TemperatureUnitContext.Provider value={{ unit, toggleUnit }}>
      {children}
    </TemperatureUnitContext.Provider>
  );
};
