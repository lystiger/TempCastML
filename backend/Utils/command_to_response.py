#command_to_response.py
import serial, time

PORT =  'COM7'  # Thay đổi theo cổng của bạn
BAUD = 115200
TIMEOUT = 2

try:
    with serial.Serial(PORT, BAUD, timeout = TIMEOUT, write_timeout= 2) as ser:
        print("Da mo PORT thanh cong !!!")
        for c in range(3): #Gửi 3 lệnh, thiết bị sẽ echo hoặc trả lời
            line = f"Ping cai con cac {c}\n"
            ser.write(line.encode("utf-8"))
            ser.flush()
            print(f"Command:{line.strip()}")

            raw_response = ser.readline()
            response = raw_response.decode("utf-8").strip()
            print(response)

            time.sleep(1)


except serial.SerialTimeoutException:
    print("Không thể ghi xuống cổng trong thời gian cho phép à con chó ngu")
except KeyboardInterrupt:
    print("User tu thoat roi dcm")
except serial.SerialException as e:
    print(f"Co mo duoc cong dau dcm: {e}")





