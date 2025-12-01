// Import React and necessary hooks for creating and managing context.
import React, { createContext, useState, useMemo } from "react";

// Create a new Context object. This will be used to provide and consume the time format state.
// Components can subscribe to this Context to read the current format and update it.
export const TimeFormatContext = createContext();

/**
 * TimeFormatProvider is a React component that makes the time format state
 * and its setter function available to any child component that consumes this context.
 *
 * @param {object} { children } - React children to be rendered within the provider's scope.
 */
export function TimeFormatProvider({ children }) {
  // Declare a state variable 'is24hFormat' and its setter 'setIs24hFormat' using the useState hook.
  // The initial format is set to 24-hour format (true).
  const [is24hFormat, setIs24hFormat] = useState(true);

  // useMemo is used to memoize the 'value' object. This prevents unnecessary re-renders
  // of consuming components if the 'value' object itself hasn't changed (i.e., is24hFormat is the same).
  const value = useMemo(
    () => ({
      is24hFormat,      // The current time format (true for 24h, false for 12h).
      setIs24hFormat, // Function to update the time format.
    }),
    [is24hFormat] // The memoized value will only re-calculate if 'is24hFormat' changes.
  );

  // The Provider component from the created context.
  // It takes a 'value' prop, which will be accessible to all consumers.
  return (
    <TimeFormatContext.Provider value={value}>
      {children}
    </TimeFormatContext.Provider>
  );
}
