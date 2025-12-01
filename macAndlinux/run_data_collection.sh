#!/bin/bash

# ============================================================================
#  TempCastML Data Collection Runner (Shell Script)
# ============================================================================
#
#  This script automates the process of starting the 24/7 data collection
#  pipeline for the TempCastML project on macOS/Linux.
#
#  What it does:
#  1. Prints informative messages.
#  2. Navigates to the directory where this script is located.
#  3. Activates the Python virtual environment located in the 'backend' folder.
#  4. Executes the main data collection script using Python.
#  5. Deactivates the virtual environment upon script termination.
#
#  How to use:
#  - Make the script executable: chmod +x run_data_collection.sh
#  - Run it from your terminal: ./run_data_collection.sh
#  - To stop the collection, press Ctrl+C in the terminal window.
#
# ============================================================================

# Print decorative messages
echo ""
echo " ===================================="
echo "  Starting TempCastML Data Collector "
echo " ===================================="
echo ""

# Define the project root directory relative to this script.
SCRIPT_DIR="$(dirname "$0")"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Change to the project root directory
cd "$PROJECT_ROOT"

echo " - Working Directory: $(pwd)"

# Activate the Python virtual environment.
echo " - Activating Python virtual environment..."
source backend/venv/bin/activate

# Check if the virtual environment was activated successfully.
if [ $? -ne 0 ]; then
    echo ""
    echo " [ERROR] Failed to activate the virtual environment."
    echo "         Please ensure a virtual environment exists at 'backend/venv'."
    echo ""
    exit 1
fi

# Run the main data collection Python script.
echo " - Starting data collection script (backend/Ingestion/collect_data.py)..."
echo ""
echo " ========================================================================="
echo "  Data collection is now running. This window will show live logs."
echo "  DO NOT CLOSE THIS WINDOW if you want to continue collecting data."
echo ""
echo "  To stop collecting, press CTRL+C in this window."
echo " ========================================================================="
echo ""

# Run the python script from the project root
PYTHONPATH="$PROJECT_ROOT:$PYTHONPATH" python backend/Ingestion/collect_data.py

# This part will only be reached when the script is stopped (e.g., with Ctrl+C).
echo ""
echo " ========================================================================="
echo "  Data collection script has been stopped."
echo " ========================================================================="
echo ""

# Deactivate the virtual environment.
echo " - Deactivating virtual environment..."
deactivate

echo ""
echo " Process finished."
