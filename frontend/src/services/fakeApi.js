export function getCurrentTemperature() {
    return { city: "Hanoi", temp: 30, unit: "°C", time: "2025-09-20 16:00" };
  }
  
  export function getPredictions() {
    return [
      { time: "17:00", temp: 31 },
      { time: "18:00", temp: 30 },
      { time: "19:00", temp: 29 },
      { time: "20:00", temp: 28 }
    ];
  }
  
  export function getHistory() {
    return [
      { date: "2025-09-18", avg: 29 },
      { date: "2025-09-19", avg: 30 },
      { date: "2025-09-20", avg: 31 }
    ];
  }
  