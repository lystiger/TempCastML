import serial
import serial.tools.list_ports
import logging
import os
import csv
import sys
import time
from datetime import datetime
import requests
import threading
from backend.Settings.config import BAUD_RATE, RAW_SENSOR_DATA, RAW_API_DATA, MERGED_DATA, LOG_FILE, API_KEY, CITY

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

class WeatherUpdater(threading.Thread):
    """Thread để cập nhật dữ liệu thời tiết định kỳ mà không block vòng lặp chính."""
    def __init__(self, interval_seconds=600): # Mặc định 10 phút
        super().__init__()
        self.daemon = True # Thread sẽ tự tắt khi chương trình chính kết thúc
        self.interval = interval_seconds
        self.latest_weather_data = (None, None, None)
        self.lock = threading.Lock()
        self.stopped = threading.Event()

    def run(self):
        logger.info("Thread cập nhật thời tiết đã bắt đầu.")
        while not self.stopped.is_set():
            temp, humidity, pressure = get_weather()
            if temp is not None:
                with self.lock:
                    self.latest_weather_data = (temp, humidity, pressure)
                logger.info("Dữ liệu thời tiết đã được cập nhật trong thread.")
            # Chờ cho đến lần cập nhật tiếp theo
            self.stopped.wait(self.interval)

    def get_latest_data(self):
        with self.lock:
            return self.latest_weather_data

    def stop(self):
        self.stopped.set()

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
        response = requests.get(url, timeout=10) # Thêm timeout
        response.raise_for_status()  # raise error for bad HTTP status
        data = response.json()
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        logger.info(f"Lấy dữ liệu thời tiết thành công: Nhiệt độ {temp}°C, Độ ẩm {humidity}%, Áp suất {pressure} hPa")
        return temp, humidity, pressure
    except requests.exceptions.RequestException as e:
        logger.error(f"Lỗi khi lấy dữ liệu thời tiết (network): {e}")
        return None, None, None
    except Exception as e:
        logger.error(f"Lỗi khi lấy dữ liệu thời tiết: {e}")
        return None, None, None #Trả về None nếu có lỗi

# =========================DATA COLLECTION LOOP=======================
def main():
    # Khởi tạo CSV (chỉ cần merged)
    merged_csv_init()

    # Khởi động thread cập nhật thời tiết
    weather_thread = WeatherUpdater(interval_seconds=600) # 10 phút
    weather_thread.start()

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
                # 1. Đọc dữ liệu cảm biến từ ESP
                line = ser.readline().decode('utf-8').strip()
                if not line:
                    continue
                # Giả sử ESP gửi dạng "temperature,humidity,label_id"
                try:
                    temp, hum, label_id = line.split(',')
                    temp = float(temp)
                    hum = float(hum)
                except (ValueError, IndexError) as e:
                    logger.warning(f"Dữ liệu nhận không hợp lệ: '{line}'. Lỗi: {e}")
                    continue

                # 2. Lấy dữ liệu thời tiết ngoài trời từ thread
                outside_temp, outside_hum, outside_pressure = weather_thread.get_latest_data()

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

                logger.info(f"Dữ liệu đã ghi: Temp={temp}, Hum={hum}, Label={label_id}")

                # 6. Chờ 1 giây trước khi đọc dòng tiếp theo
                time.sleep(1)

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
        weather_thread.stop()
        weather_thread.join() # Đợi thread kết thúc
        logger.info("Weather update thread đã dừng.")

# =========================ENTRY POINT=======================
if __name__ == "__main__":
    main()
