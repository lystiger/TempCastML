import os
from datetime import datetime

#==================SERIAL CONFIG=========================
SERIAL_PORT = 'COM4' #Nhớ chỉnh cổng trước khi lấy data
BAUD_RATE = 115200
DHT_SENSOR = 1
TOTAL_SENSOR = DHT_SENSOR
SESSION_ID = datetime.now().strftime("%Y%m%d_%H%M%S") #Ngày nhập dữ liệu

#==================FILE PATH=============================

BASE_DIR = os.path.join(os.getcwd(), "Data") # Thư mục Data trong thư mục hiện tại
RAW_SENSOR_DATA = os.path.join(BASE_DIR, 'raw_data.csv') # Thư mục raw_data.csv trong thư mục Data
RAW_API_DATA = os.path.join(BASE_DIR, 'raw_data_api.csv') # Thư mục raw_data_api.csv trong thư mục Data
MERGED_DATA = os.path.join(BASE_DIR, 'merged_data.csv') # Thư mục merged_data.csv trong thư mục Data
JSON_DIR = os.path.join(BASE_DIR, 'data.json') # Thư mục data.json trong thư mục Data
PROCESSED_DIR = os.path.join(BASE_DIR, "Processed") # Thư mục Processed trong thư mục Data
PROCESSED_SENSOR_DATA = os.path.join(PROCESSED_DIR, 'processed_sensor_data.csv') # Thư mục processed_sensor_data.csv trong thư mục Processed
PROCESSED_API_DATA = os.path.join(PROCESSED_DIR, 'processed_api_data.csv') # Thư mục processed_api_data.csv trong thư mục Processed
PROCESSED_MERGED_DATA = os.path.join(PROCESSED_DIR, 'processed_merged_data.csv') # Thư mục processed_merged_data.csv trong thư mục Processed
MODEL_DIR = os.path.join(os.getcwd(), "AI", "Model") # Thư mục Model trong thư mục AI
MODEL_PATH = os.path.join(MODEL_DIR, 'lstm_model.h5') # Thư mục lstm_model.h5 trong thư mục Model
LOG_FILE = os.path.join(os.getcwd(), "Log", 'data_collection.log') # Thư mục log trong thư mục hiện tại

# ------------------ API ---------------------
API_KEY = ""  # Lên trang https://home.openweathermap.org/api_keys để lấy API key
CITY = "Hung Yen, VN"

#==================OTHER CONFIG=========================
DEFAULT_BAUD = 115200
DEFAULT_TIMEOUT = 1
DEFAULT_WRITE_TIMEOUT = 1
DEFAULT_READ_TIMEOUT = 1
DEFAULT_IDLE_LIMIT = 10

#==================BACKEND CONFIG=========================
BACKEND_URL = "http://localhost:8000/data"