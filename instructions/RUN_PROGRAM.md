# How to Run TempCastML Frontend and Backend Simultaneously

This guide explains how to use the `run_all.bat` script (and its equivalent shell scripts for macOS/Linux) to start both the frontend and backend services of the TempCastML application concurrently.

## For Windows Users

The `run_all.bat` file is a Windows batch script designed to automate the startup process.

1.  **Navigate to the Project Root:**
    Open File Explorer and go to the main `TempCastML` directory where `run_all.bat` is located.

2.  **Execute the Script:**
    *   **Option 1 (Double-click):** Simply double-click on `run_all.bat`.
    *   **Option 2 (Command Prompt):** Open a Command Prompt, navigate to the `TempCastML` directory using `cd path\to\TempCastML`, and then type `run_all.bat` and press Enter.

3.  **Observe Startup:**
    Two new Command Prompt windows will open:
    *   One for the **Backend**: This window will display logs from the FastAPI server (running with Uvicorn).
    *   One for the **Frontend**: This window will display logs from the React development server (running with Vite).

4.  **Access the Application:**
    Once both servers have started (you'll see messages indicating they are running, typically with URLs like `http://localhost:8000` for the backend and `http://localhost:5173` for the frontend), you can access the frontend in your web browser, usually at `http://localhost:5173`.

5.  **Stopping the Applications:**
    To stop both the frontend and backend, simply close the two Command Prompt windows that were opened by the script.

## For macOS and Linux Users

For macOS and Linux, shell scripts (`.sh` files) are provided to perform the equivalent actions.

### Running Frontend and Backend Together (`run_all.sh`)

This script will start both the frontend and backend services in the background.

1.  **Make the Script Executable:**
    Open a terminal, navigate to the `TempCastML` directory, and make the script executable:
    ```bash
    chmod +x run_all.sh
    ```

2.  **Execute the Script:**
    Run the script from the terminal:
    ```bash
    ./run_all.sh
    ```

3.  **Observe Startup:**
    The script will start both the backend and frontend processes in the background. You will see messages in your terminal indicating their PIDs (Process IDs).

4.  **Access the Application:**
    Once both services have started, you can access the frontend in your web browser, usually at `http://localhost:5173`.

5.  **Stopping the Applications:**
    To stop the applications, you can use the `kill` command with the PIDs displayed when you started the script:
    ```bash
    kill <BACKEND_PID>
    kill <FRONTEND_PID>
    ```
    Alternatively, you can use `killall` if you want to stop all instances of `uvicorn` and `node` (which runs the frontend):
    ```bash
    killall uvicorn
    killall node
    ```
    Be cautious with `killall` as it will terminate all processes with that name, not just those related to this project.

### Running Data Collection (`run_data_collection.sh`)

This script will start the continuous data collection process.

1.  **Make the Script Executable:**
    Open a terminal, navigate to the `TempCastML` directory, and make the script executable:
    ```bash
    chmod +x run_data_collection.sh
    ```

2.  **Execute the Script:**
    Run the script from the terminal:
    ```bash
    ./run_data_collection.sh
    ```

3.  **Observe Startup:**
    The script will start the data collection process in the foreground within your terminal window. You will see live logs from the data collection script.

4.  **Stopping Data Collection:**
    To stop the data collection, press `Ctrl+C` in the terminal window where the script is running.
