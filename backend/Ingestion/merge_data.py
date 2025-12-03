import pandas as pd
import os
import logging
import sys

# Add the backend directory to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Settings.config import (
    PROCESSED_SENSOR_DATA,
    PROCESSED_API_DATA,
    MERGED_DATA,
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

# ========================DATA MERGING=========================

def merge_datasets(sensor_path, api_path, output_path):
    """
    Merges the cleaned sensor and API datasets based on timestamp.
    
    For each sensor reading, it finds the most recent API reading.
    """
    try:
        logger.info(f"Starting merging of sensor data from {sensor_path} and API data from {api_path}")

        if not os.path.exists(sensor_path) or not os.path.exists(api_path):
            logger.warning("One or both processed data files not found. Skipping merge.")
            return

        # Load datasets
        df_sensor = pd.read_csv(sensor_path)
        df_api = pd.read_csv(api_path)

        # Convert timestamps to datetime objects for merging
        df_sensor['timestamp'] = pd.to_datetime(df_sensor['timestamp'])
        df_api['timestamp'] = pd.to_datetime(df_api['timestamp'])

        # Sort by timestamp, which is required for merge_asof
        df_sensor.sort_values('timestamp', inplace=True)
        df_api.sort_values('timestamp', inplace=True)

        # Merge the dataframes
        # For each row in df_sensor, it finds the last row in df_api before or at the same time
        merged_df = pd.merge_asof(
            left=df_sensor,
            right=df_api,
            on='timestamp',
            direction='backward', # Finds the last matching API entry for each sensor entry
            tolerance=pd.Timedelta('15 minutes') # Optional: only consider API data within a 15-min window
        )

        # Calculate delta columns
        merged_df['delta_temp'] = merged_df['temperature'] - merged_df['outside_temp']
        merged_df['delta_humidity'] = merged_df['humidity'] - merged_df['outside_humidity']

        # Drop rows where merge was not possible (NaNs in API columns)
        original_rows = len(merged_df)
        merged_df.dropna(subset=['outside_temp', 'outside_humidity'], inplace=True)
        if len(merged_df) < original_rows:
            logger.info(f"Dropped {original_rows - len(merged_df)} rows that could not be merged.")

        # Reorder and select final columns
        final_columns = [
            'timestamp', 'label_id', 'session', 'temperature', 'humidity',
            'day_of_week', 'hour_of_day', 'outside_temp', 'outside_humidity',
            'outside_pressure', 'delta_temp', 'delta_humidity'
        ]
        # The 'session' column from the API data might be named differently, so we handle it
        if 'session_y' in merged_df.columns:
            merged_df.rename(columns={'session_x': 'session'}, inplace=True)
        
        merged_df = merged_df[final_columns]


        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        merged_df.to_csv(output_path, index=False)
        logger.info(f"Merged data saved to {output_path}")

    except Exception as e:
        logger.error(f"Error merging datasets: {e}")


def main():
    """Main function to run the data merging process."""
    logger.info("===== Starting Data Merging Process =====")
    merge_datasets(PROCESSED_SENSOR_DATA, PROCESSED_API_DATA, MERGED_DATA)
    logger.info("===== Data Merging Process Finished =====")

if __name__ == "__main__":
    main()
