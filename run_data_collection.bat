@echo off
REM ============================================================================
REM  TempCastML Data Collection Runner
REM ============================================================================
REM
REM  This script automates the process of starting the 24/7 data collection
REM  pipeline for the TempCastML project.
REM
REM  What it does:
REM  1. Sets the console window title for easy identification.
REM  2. Navigates to the directory where this script is located.
REM  3. Activates the Python virtual environment located in the 'backend' folder.
REM  4. Executes the main data collection script using Python.
REM  5. Keeps the window open after the script finishes to show final messages.
REM
REM  How to use:
REM  - Simply double-click this file to start collecting data.
REM  - To stop the collection, focus the command window and press Ctrl+C.
REM
REM ============================================================================

:: Set the window title
title TempCastML Data Collector

:: Use echo with a dot to print a blank line for spacing
echo.
echo  ====================================
echo   Starting TempCastML Data Collector 
echo  ====================================
echo.

:: Change directory to the location of this .bat file.
:: This ensures that all relative paths in the Python script work correctly.
cd /d "%~dp0"
echo  - Working Directory: %cd%

:: Activate the Python virtual environment.
echo  - Activating Python virtual environment...
call backend/venv/Scripts/activate

:: Check if the virtual environment was activated successfully.
:: 'errorlevel 1' means the previous command failed.
if errorlevel 1 (
    echo.
    echo  [ERROR] Failed to activate the virtual environment.
    echo          Please ensure a virtual environment exists at 'backend\venv'.
    echo.
    pause
    exit /b
)

:: Run the main data collection Python script.
echo  - Starting data collection script (backend/Ingestion/collect_data.py)...
echo.
echo  =========================================================================
echo   Data collection is now running. This window will show live logs.
echo   DO NOT CLOSE THIS WINDOW if you want to continue collecting data.
echo. 
echo   To stop collecting, press CTRL+C in this window.
echo  =========================================================================
echo.

python backend/Ingestion/collect_data.py

:: This part will only be reached when the script is stopped (e.g., with Ctrl+C).
echo.
echo  =========================================================================
echo   Data collection script has been stopped.
echo  =========================================================================
echo.

:: Deactivate the virtual environment.
echo  - Deactivating virtual environment...
call deactivate

echo.
echo  Process finished. Press any key to close this window.
pause >nul
