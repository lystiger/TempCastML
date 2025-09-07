import serial
import serial.tools.list_ports
import logging # Thư viện để thu thập thông báo từ chương trình
import os
import csv
import sys
import time
from datetime import datetime
import requests
from config import SERIAL_PORT, BAUD_RATE, RAW_SENSOR_DATA, RAW_API_DATA, MERGED_DATA, LOG_FILE, API_KEY, CITY

# ========================LOGGING=========================
logging.basicConfig(
    level=logging.INFO, # Chỉnh mức độ log (DEBUG < INFO < WARNING < ERROR < CRITICAL)
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE), # Ghi log vào file
        logging.StreamHandler(sys.stdout) # Hiển thị log trên console
    ]
)
logger = logging.getLogger() #
logger.info("Logger đã được thiết lập.")

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
        with open(file_path, 'w', newline='') as csvfile: 
            writer = csv.writer(csvfile)
            writer.writerow(header)
        logger.info(f"CSV file đã được tạo: {file_path}")
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
        'temperature','humidity','day_of_week','hour_of_day',
        'outside_temp','outside_humidity','outside_pressure',
        'delta_temp','delta_humidity'
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
def get_weather():
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        response.raise_for_status()  # raise error for bad HTTP status
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        logger.info(f"Lấy dữ liệu thời tiết thành công: Nhiệt độ {temp}°C, Độ ẩm {humidity}%, Áp suất {pressure} hPa")
        return temp, humidity, pressure
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        return None, None, None #Trả về None nếu có lỗi

# =========================DATA COLLECTION LOOP=======================
def main():
    # Khởi tạo CSV
    csv_init()
    API_csv_init()
    merged_csv_init()

    # Kết nối ESP
    ser = connect_esp(SERIAL_PORT, BAUD_RATE)
    if ser is None:
        logger.error("Không thể kết nối ESP. Dừng chương trình.")
        return

    logger.info("Bắt đầu thu thập dữ liệu... Nhấn Ctrl+C để dừng.")

    try:
        while True:
            # 1. Đọc dữ liệu cảm biến từ ESP
            line = ser.readline().decode('utf-8').strip()
            if not line:
                continue
            # Giả sử ESP gửi dạng "temperature,humidity,label_id"
            try:
                temp, hum, label_id = line.split(',')
                temp = float(temp)
                hum = float(hum)
            except Exception as e:
                logger.warning(f"Dữ liệu nhận không hợp lệ: {line}")
                continue

            # 2. Lấy dữ liệu thời tiết ngoài trời
            outside_temp, outside_hum, outside_pressure = get_weather()

            # 3. Tính delta nếu API hợp lệ
            delta_temp = temp - outside_temp if outside_temp is not None else None
            delta_hum = hum - outside_hum if outside_hum is not None else None

            # 4. Tạo timestamp và thời gian
            now = datetime.now()
            day_of_week = now.strftime("%A")
            hour_of_day = now.hour
            timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
            session_id = now.strftime("%Y%m%d_%H%M%S")

            # 5. Ghi dữ liệu vào MERGED CSV
            with open(MERGED_DATA, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp, label_id, session_id,
                    temp, hum, day_of_week, hour_of_day,
                    outside_temp, outside_hum, outside_pressure,
                    delta_temp, delta_hum
                ])

            logger.info(f"Dữ liệu đã ghi: {line}")

            # 6. Chờ 1 giây trước khi đọc dòng tiếp theo
            time.sleep(1)

    except KeyboardInterrupt:
        logger.info("Dừng thu thập dữ liệu theo yêu cầu người dùng.")
    finally:
        if ser.is_open:
            ser.close()
        logger.info("Serial connection đã đóng.")

# =========================ENTRY POINT=======================
if __name__ == "__main__":
    main()
