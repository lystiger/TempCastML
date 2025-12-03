import logging
import os
import csv
import sys
import time
from datetime import datetime
import requests

# Import necessary functions and constants
from backend.Settings.config import RAW_API_DATA, LOG_FILE, API_KEY, CITY
from backend.Ingestion.collect_data import get_weather, API_csv_init

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
logger.info("Logger has been set up for API data collection.")

# =========================API DATA COLLECTION LOOP=======================
def main():
    # Initialize CSV for raw API data
    if not API_csv_init():
        logger.error("Failed to initialize raw API data CSV. Exiting.")
        sys.exit(1)

    logger.info("Starting API data collection loop... Press Ctrl+C to stop.")

    try:
        while True:
            outside_temp, outside_hum, outside_pressure = get_weather()

            if outside_temp is not None:
                now = datetime.now()
                day_of_week = now.strftime("%A")
                hour_of_day = now.hour
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                session_id = now.strftime("%Y%m%d_%H%M%S") # Using for session id

                # Write data to RAW_API_DATA
                with open(RAW_API_DATA, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        timestamp, "api_data", session_id,
                        None, None, # temperature and humidity are from sensor, not API
                        day_of_week, hour_of_day,
                        outside_temp, outside_hum, outside_pressure,
                        None, None # delta_temp, delta_humidity are not applicable for raw API data
                    ])
                logger.info(f"API data recorded: Temp={outside_temp}, Hum={outside_hum}, Pressure={outside_pressure}")
            else:
                logger.warning("No API data fetched. Skipping write to CSV.")

            time.sleep(600) # Fetch every 10 minutes (600 seconds)

    except KeyboardInterrupt:
        logger.info("API data collection stopped by user request.")
    except Exception as e:
        logger.error(f"An unexpected error occurred during API data collection: {e}")
    finally:
        logger.info("API data collection process finished.")

# =========================ENTRY POINT=======================
if __name__ == "__main__":
    main()
