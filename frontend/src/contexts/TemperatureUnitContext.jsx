import React, { createContext, useState } from 'react';

export const TemperatureUnitContext = createContext();

export const TemperatureUnitProvider = ({ children }) => {
  const [unit, setUnit] = useState('celsius'); // 'celsius', 'fahrenheit', or 'kelvin'

  const toggleUnit = (newUnit) => {
    setUnit(newUnit);
  };

  return (
    <TemperatureUnitContext.Provider value={{ unit, toggleUnit }}>
      {children}
    </TemperatureUnitContext.Provider>
  );
};
