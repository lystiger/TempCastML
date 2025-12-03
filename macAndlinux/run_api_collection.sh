#!/bin/bash

echo ""
echo " ===================================="
echo "  Starting TempCastML API Collector "
echo " ===================================="
echo ""

(
    # Move to project root
    cd "$(dirname "$0")/.." || exit

    PYTHON_EXEC="backend/venv/bin/python3"

    if [ ! -f "$PYTHON_EXEC" ]; then
        echo "Error: $PYTHON_EXEC not found!"
        exit 1
    fi

    echo "Using Python executable: $PYTHON_EXEC"

    # Run as module so "backend" imports work
    "$PYTHON_EXEC" -m backend.Ingestion.collect_api_data
)

echo ""
echo " ========================================================================="
echo "   TempCastML API Collector finished or stopped by user."
echo " ========================================================================="
echo ""
