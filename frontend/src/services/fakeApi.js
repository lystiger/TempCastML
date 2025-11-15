export function getCurrentTemperature() {
    return {
        temperature_c: 30,
        timestamp: "2025-09-20T16:00:00Z"
    };
}
  
  export function getPredictions() {
    return {
        forecast: [31, 30, 29, 28, 27, 26, 25, 24, 23, 22, 21, 20, 19, 18, 17, 16, 15, 14, 13, 12, 11, 10, 9, 8]
    };
}
  
  export function getHistory() {
    return [
        { id: 1, timestamp: "2025-09-20T15:00:00Z", temperature_c: 29.5, device_id: 1 },
        { id: 2, timestamp: "2025-09-20T14:00:00Z", temperature_c: 30.1, device_id: 1 },
        { id: 3, timestamp: "2025-09-20T13:00:00Z", temperature_c: 31.2, device_id: 1 },
        { id: 4, timestamp: "2025-09-20T12:00:00Z", temperature_c: 30.8, device_id: 1 },
    ];
}
  