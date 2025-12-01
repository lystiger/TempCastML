// Import React and necessary hooks for creating and managing context.
import React, { createContext, useState } from 'react';

// Create a new Context object. This will be used to provide and consume the temperature unit state.
// Components can subscribe to this Context to read the current unit and update it.
export const TemperatureUnitContext = createContext();

/**
 * TemperatureUnitProvider is a React component that makes the temperature unit state
 * and a function to toggle it available to any child component that consumes this context.
 *
 * @param {object} { children } - React children to be rendered within the provider's scope.
 */
export const TemperatureUnitProvider = ({ children }) => {
  // Declare a state variable 'unit' and its setter 'setUnit' using the useState hook.
  // The initial unit is set to 'celsius'.
  const [unit, setUnit] = useState('celsius'); // Possible values: 'celsius', 'fahrenheit', or 'kelvin'

  /**
   * Toggles the temperature unit to the specified new unit.
   * @param {string} newUnit - The new unit to set (e.g., 'celsius', 'fahrenheit').
   */
  const toggleUnit = (newUnit) => {
    setUnit(newUnit);
  };

  // The Provider component from the created context.
  // It takes a 'value' prop, which will be accessible to all consumers.
  return (
    <TemperatureUnitContext.Provider value={{ unit, toggleUnit }}>
      {children}
    </TemperatureUnitContext.Provider>
  );
};
