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
LOG_FILE = os.path.join(os.getcwd(), "Log", 'data_collection.log') # Thư mục log trong thư mục hiện tại

# ------------------ API ---------------------
API_KEY = ""  # Lên trang https://home.openweathermap.org/api_keys để lấy API key
CITY = "Hung Yen, VN"