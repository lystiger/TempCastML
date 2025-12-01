import React, { createContext, useState, useMemo } from "react";

export const TimeFormatContext = createContext();

export function TimeFormatProvider({ children }) {
  const [is24hFormat, setIs24hFormat] = useState(true);

  const value = useMemo(
    () => ({
      is24hFormat,
      setIs24hFormat,
    }),
    [is24hFormat]
  );

  return (
    <TimeFormatContext.Provider value={value}>
      {children}
    </TimeFormatContext.Provider>
  );
}
