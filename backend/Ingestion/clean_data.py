import pandas as pd
import os
import logging
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Settings.config import (
    RAW_SENSOR_DATA,
    RAW_API_DATA,
    PROCESSED_SENSOR_DATA,
    PROCESSED_API_DATA,
    LOG_FILE
)

# ========================LOGGING=========================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger()

# ========================DATA CLEANING=========================

def clean_sensor_data(input_path, output_path):
    """
    Cleans the raw sensor data.
    - Converts timestamp to datetime objects.
    - Ensures numeric columns are of the correct type.
    - Handles missing values.
    """
    try:
        logger.info(f"Starting cleaning of sensor data from {input_path}")
        if not os.path.exists(input_path):
            logger.warning(f"Sensor data file not found at {input_path}. Skipping.")
            return

        df = pd.read_csv(input_path)

        # 1. Timestamp conversion
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # 2. Data type conversion
        df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce')
        df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce')

        # 3. Handle missing values (e.g., drop rows with null temperature/humidity)
        original_rows = len(df)
        df.dropna(subset=['temperature', 'humidity'], inplace=True)
        if len(df) < original_rows:
            logger.info(f"Dropped {original_rows - len(df)} rows with missing sensor data.")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Cleaned sensor data saved to {output_path}")

    except Exception as e:
        logger.error(f"Error cleaning sensor data: {e}")

def clean_api_data(input_path, output_path):
    """
    Cleans the raw API data.
    - Converts timestamp to datetime objects.
    - Ensures numeric columns are of the correct type.
    - Handles missing values.
    """
    try:
        logger.info(f"Starting cleaning of API data from {input_path}")
        if not os.path.exists(input_path):
            logger.warning(f"API data file not found at {input_path}. Skipping.")
            return

        df = pd.read_csv(input_path)

        # 1. Timestamp conversion
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # 2. Data type conversion
        numeric_cols = ['outside_temp', 'outside_humidity', 'outside_pressure']
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        # 3. Handle missing values
        original_rows = len(df)
        df.dropna(subset=numeric_cols, inplace=True)
        if len(df) < original_rows:
            logger.info(f"Dropped {original_rows - len(df)} rows with missing API data.")

        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        logger.info(f"Cleaned API data saved to {output_path}")

    except Exception as e:
        logger.error(f"Error cleaning API data: {e}")


def main():
    """Main function to run the data cleaning process."""
    logger.info("===== Starting Data Cleaning Process =====")
    clean_sensor_data(RAW_SENSOR_DATA, PROCESSED_SENSOR_DATA)
    clean_api_data(RAW_API_DATA, PROCESSED_API_DATA)
    logger.info("===== Data Cleaning Process Finished =====")

if __name__ == "__main__":
    main()
