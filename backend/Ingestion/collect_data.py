import serial
import serial.tools.list_ports
import logging.handlers
import os
import csv
import sys
import time
from datetime import datetime
import requests
import threading
from backend.Settings.config import BAUD_RATE, RAW_SENSOR_DATA, RAW_API_DATA, MERGED_DATA, LOG_FILE, API_KEY, CITY

# ========================LOGGING=========================
# Set up a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create a formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a rotating file handler
# This will create a new log file when the current one reaches 5MB
# It will keep up to 5 old log files.
file_handler = logging.handlers.RotatingFileHandler(
    LOG_FILE, maxBytes=5*1024*1024, backupCount=5
)
file_handler.setFormatter(formatter)

# Create a stream handler to also log to console
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

logger.info("Logger has been set up with log rotation.")

# ========================IMPROVEMENTS==================
def find_serial_port():
    """Tự động tìm cổng serial có vẻ là thiết bị ESP/Arduino."""
    ports = serial.tools.list_ports.comports()
    for port in ports:
        # Tiêu chí tìm kiếm: mô tả chứa 'USB', 'CH340', 'CP210x' (phổ biến cho ESP)
        if 'USB' in port.description or 'CH340' in port.description or 'CP210x' in port.description:
            logger.info(f"Tìm thấy cổng phù hợp: {port.device} - {port.description}")
            return port.device
    logger.warning("Không tìm thấy cổng serial phù hợp tự động. Sẽ thử cổng mặc định.")
    return None

def is_data_valid(temp, humidity):
    """
    Validates if the sensor readings are within a reasonable range.
    
    Args:
        temp (float): The temperature reading.
        humidity (float): The humidity reading.
        
    Returns:
        bool: True if data is valid, False otherwise.
    """
    if not (-40 <= temp <= 60):
        logger.warning(f"Invalid temperature reading: {temp}°C. Out of range (-40 to 60).")
        return False
    if not (0 <= humidity <= 100):
        logger.warning(f"Invalid humidity reading: {humidity}%. Out of range (0 to 100).")
        return False
    return True



# ========================CONNECT==================
def get_ports():
    ports = serial.tools.list_ports.comports() #Tìm tất cả các cổng available trên máy
    ports_list = []
    for port in ports:
        print(f"Đã tìm thấy cổng: {port.device} - {port.description}") #In ra cổng và mô tả
        ports_list.append(port.device) #Lấy tên cổng
    if not ports_list:
        logger.warning("Không tìm thấy cổng nào.")
    return ports_list

def connect_esp(port, baudrate):
    try:
        ser = serial.Serial(port, baudrate, timeout=2) #Tạo kết nối serial
        time.sleep(2) #Chờ 2s để kết nối ổn định
        if ser.is_open:
            logger.info(f"Kết nối thành công với {port} ở tốc độ {baudrate}.")
            return ser
        else:
            logger.error(f"Không thể mở cổng {port}.")
            return None
    except serial.SerialException as e:
        logger.error(f"Lỗi kết nối với {port}: {e}")
        return None
    except Exception as e:
        logger.error(f"Lỗi không xác định: {e}")
        return None

# ========================CSV=============================
def init_csv(file_path, header):
    try:
        # Check xem folder này có tồn tại ko, nếu ko thì tạo
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        # Nếu file trong folder ko tồn tại, tạo và viết header
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(header)
            logger.info(f"CSV file đã được tạo: {file_path}")
        else:
            logger.info(f"CSV file đã tồn tại: {file_path}")
        return True
    except Exception as e:
        logger.error(f"Lỗi tạo file .csv: {e}")
        return False

def csv_init():
    header = [
        'timestamp','label_id','session',
        'temperature','humidity','day_of_week',
        'hour_of_day'
    ]
    return init_csv(RAW_SENSOR_DATA, header)

def API_csv_init():
    header = [
        'timestamp','label_id','session',
        'day_of_week','hour_of_day',
        'outside_temp','outside_humidity','outside_pressure'
    ]
    return init_csv(RAW_API_DATA, header)

def merged_csv_init():
    header = [
        'timestamp','label_id','session',
        'temperature','humidity','day_of_week','hour_of_day',
        'outside_temp','outside_humidity','outside_pressure',
        'delta_temp','delta_humidity'
    ]
    return init_csv(MERGED_DATA, header)

# =========================API Fetch=======================
def get_weather(retries=3, backoff_factor=2):
    """
    Fetches weather data from OpenWeatherMap with a retry mechanism.
    
    Args:
        retries (int): The maximum number of retries.
        backoff_factor (int): The factor to increase delay by for each retry.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    delay = backoff_factor
    for i in range(retries):
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # Raise an exception for bad status codes (4xx or 5xx)
            data = response.json()
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            logger.info(f"Successfully fetched weather data: Temp {temp}°C, Humidity {humidity}%, Pressure {pressure} hPa")
            return temp, humidity, pressure
        except requests.exceptions.RequestException as e:
            logger.warning(f"Network error fetching weather data (attempt {i+1}/{retries}): {e}")
            if i < retries - 1:
                logger.info(f"Retrying in {delay} seconds...")
                time.sleep(delay)
                delay *= backoff_factor
            else:
                logger.error("Failed to fetch weather data after multiple retries.")
                return None, None, None
    return None, None, None

# =========================DATA COLLECTION LOOP=======================
def main():
    # Khởi tạo CSV (chỉ cần merged)
    merged_csv_init()

    ser = None

    logger.info("Bắt đầu vòng lặp thu thập dữ liệu... Nhấn Ctrl+C để dừng.")

    try:
        while True:
            if ser is None or not ser.is_open:
                # Cố gắng kết nối hoặc kết nối lại
                port = find_serial_port()
                if port:
                    ser = connect_esp(port, BAUD_RATE)
                if ser is None:
                    logger.error("Không thể kết nối ESP. Thử lại sau 5 giây.")
                    time.sleep(5)
                    continue # Quay lại đầu vòng lặp

            try:
                # 1. Yêu cầu dữ liệu mới từ ESP
                ser.reset_input_buffer() # Xóa buffer để đảm bảo dữ liệu mới
                ser.write(b'R') # Gửi ký tự 'R' để yêu cầu dữ liệu
                time.sleep(0.5) # Đợi ESP phản hồi

                # 2. Đọc dữ liệu cảm biến từ ESP
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    logger.warning("Không nhận được dữ liệu từ ESP sau khi yêu cầu.")
                    time.sleep(5)
                    continue
                
                # Giả sử ESP gửi dạng "temperature,humidity"
                try:
                    temp, hum = line.split(',')
                    temp = float(temp)
                    hum = float(hum)
                except (ValueError, IndexError) as e:
                    logger.warning(f"Dữ liệu nhận không hợp lệ: '{line}'. Lỗi: {e}")
                    continue

                # Validate sensor data
                if not is_data_valid(temp, hum):
                    continue

                # 3. Lấy dữ liệu thời tiết ngoài trời trực tiếp
                outside_temp, outside_hum, outside_pressure = get_weather()

                # 4. Tạo timestamp và IDs
                now = datetime.now()
                day_of_week = now.strftime("%A")
                hour_of_day = now.hour
                timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
                session_id = now.strftime("%Y%m%d_%H%M%S")
                label_id = session_id # Sử dụng session_id làm label_id

                # 5. Tính delta nếu API hợp lệ
                delta_temp = temp - outside_temp if outside_temp is not None else None
                delta_hum = hum - outside_hum if outside_hum is not None else None

                # 6. Ghi dữ liệu vào MERGED CSV
                with open(MERGED_DATA, 'a', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow([
                        timestamp, label_id, session_id,
                        temp, hum, day_of_week, hour_of_day,
                        outside_temp, outside_hum, outside_pressure,
                        delta_temp, delta_hum
                    ])

                logger.info(f"Dữ liệu đã ghi: Temp={temp}, Hum={hum}, Label={label_id}")

                # 7. Chờ 10 phút trước khi yêu cầu tiếp theo
                time.sleep(600)

            except serial.SerialException as e:
                logger.error(f"Lỗi kết nối serial: {e}. Đang thử kết nối lại...")
                if ser and ser.is_open:
                    ser.close()
                ser = None # Đặt lại để vòng lặp thử kết nối lại
                time.sleep(5) # Chờ trước khi thử lại
            except Exception as e:
                logger.error(f"Lỗi không mong muốn trong vòng lặp chính: {e}")
                time.sleep(5)


    except KeyboardInterrupt:
        logger.info("Dừng thu thập dữ liệu theo yêu cầu người dùng.")
    finally:
        if ser and ser.is_open:
            ser.close()
            logger.info("Serial connection đã đóng.")

# =========================ENTRY POINT=======================
if __name__ == "__main__":
    main()
