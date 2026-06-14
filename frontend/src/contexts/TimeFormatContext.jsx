// Provides the 12h/24h time-format preference to the whole app, persisted
// across reloads.
import { createContext, useEffect, useMemo, useState } from "react";

// Context + Provider intentionally co-located (consumed across the app).
// eslint-disable-next-line react-refresh/only-export-components
export const TimeFormatContext = createContext();

const STORAGE_KEY = "tempcast.time24h";

export function TimeFormatProvider({ children }) {
  const [is24hFormat, setIs24hFormat] = useState(() => {
    const saved = localStorage.getItem(STORAGE_KEY);
    return saved == null ? true : saved === "true";
  });

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, String(is24hFormat));
  }, [is24hFormat]);

  const value = useMemo(
    () => ({ is24hFormat, setIs24hFormat }),
    [is24hFormat]
  );

  return (
    <TimeFormatContext.Provider value={value}>
      {children}
    </TimeFormatContext.Provider>
  );
}
