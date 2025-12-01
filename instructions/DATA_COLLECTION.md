# Data Collection

This document outlines the process for collecting sensor and weather data for the TempCastML application.

## Current Process

The data collection is handled by a standalone Python script: `backend/Ingestion/collect_data.py`. This script performs the following steps:

1.  Connects to a serial device (like an Arduino or ESP) based on a port specified in the configuration.
2.  Enters an infinite loop to continuously:
    a. Read sensor data (temperature, humidity) from the serial device.
    b. Fetch current weather data from the OpenWeatherMap API.
    c. Combine the sensor and weather data into a single record.
    d. Append the record to a CSV file located at `backend/Data/merged_data.csv`.

## How to Run Data Collection

To run the data collection script, follow these steps:

1.  **Connect the hardware:** Ensure your sensor device (Arduino, ESP, etc.) is connected to your computer via USB.

2.  **Install dependencies:** Open a terminal and install the required Python packages:
    ```bash
    pip install -r backend/requirements.txt
    ```

3.  **Find the serial port:** Run the `port_identifier.py` script to find the name of the serial port your device is connected to:
    ```bash
    python backend/Utils/port_identifier.py
    ```
    This will output a list of available serial ports. Look for the one corresponding to your device (e.g., `COM3` on Windows, `/dev/ttyUSB0` or `/dev/tty.usbmodemXXXX` on Linux/macOS).

4.  **Configure the script:**
    a. Open the configuration file: `backend/Settings/config.py`.
    b. Set the `SERIAL_PORT` variable to the port name you identified in the previous step.
    c. Set the `API_KEY` variable to your valid OpenWeatherMap API key.

5.  **Run the script:** Execute the `collect_data.py` script from the project's root directory:
    ```bash
    python backend/Ingestion/collect_data.py
    ```

6.  **Stop the script:** The script will run indefinitely. To stop it, press `Ctrl+C` in the terminal.

## Limitations and Proposed Improvements

The current data collection process has several limitations that make it inefficient and not robust.

| Limitation | Description | Proposed Improvement |
| :--- | :--- | :--- |
| **Manual Configuration** | You have to manually find the serial port and edit the configuration file every time the port changes. | **Automate Port Detection:** Integrate the port identification logic directly into the `collect_data.py` script to automatically find and use the correct serial port. |
| **Blocking API Calls** | The script waits for the OpenWeatherMap API to respond before reading the next sensor value. A slow API response will cause the script to miss sensor readings. | **Use Asynchronous Requests:** Perform the API call in a separate, non-blocking thread or using an asynchronous library (`asyncio` with `httpx`) to allow continuous sensor data collection. |
| **No Resilience** | If the serial device is disconnected, the script will crash and data collection will stop. | **Add Error Handling:** Implement error handling and a reconnection loop to allow the script to automatically try to reconnect to the serial device if the connection is lost. |
| **Code Quality** | The script contains unused functions and variables. | **Refactor and Clean Up:** Remove the dead code to improve readability and maintainability. |

Implementing these improvements would create a more efficient, reliable, and "hands-off" data collection system.
