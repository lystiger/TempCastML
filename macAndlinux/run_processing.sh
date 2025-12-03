#!/bin/bash

# This script automates the data cleaning and merging process.
# It runs in a loop every 30 minutes.

# Get the directory of the script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
# Navigate to the project root (assuming the script is in macAndlinux)
PROJECT_ROOT="$SCRIPT_DIR/.."

# Define paths to the raw data files
RAW_SENSOR_FILE="$PROJECT_ROOT/backend/Data/raw_data.csv"
RAW_API_FILE="$PROJECT_ROOT/backend/Data/raw_data_api.csv"

# Python scripts to execute
CLEAN_SCRIPT="$PROJECT_ROOT/backend/Ingestion/clean_data.py"
MERGE_SCRIPT="$PROJECT_ROOT/backend/Ingestion/merge_data.py"

echo "Starting automated data processing script..."

while true; do
    echo "-------------------------------------------"
    echo "Starting new processing cycle at $(date)"

    # Check if both raw data files exist
    if [ -f "$RAW_SENSOR_FILE" ] && [ -f "$RAW_API_FILE" ]; then
        echo "Found both raw sensor and API data files."

        # Run the cleaning script
        echo "Step 1: Running data cleaning script..."
        python3 "$CLEAN_SCRIPT"
        
        # Run the merging script
        echo "Step 2: Running data merging script..."
        python3 "$MERGE_SCRIPT"

        echo "Processing cycle completed successfully."

    else
        echo "Warning: Missing required data files. Cannot run processing."
        if [ ! -f "$RAW_SENSOR_FILE" ]; then
            echo " -> Missing sensor data file: $RAW_SENSOR_FILE"
        fi
        if [ ! -f "$RAW_API_FILE" ]; then
            echo " -> Missing API data file: $RAW_API_FILE"
        fi
        echo "Will check again in 30 minutes."
    fi

    echo "-------------------------------------------"
    echo "Sleeping for 30 minutes..."
    sleep 1800 # 1800 seconds = 30 minutes
done
