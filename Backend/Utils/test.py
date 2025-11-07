import serial

try:
    ser = serial.Serial("COM7", 115200, timeout=1)
    print("Port opened!")
    ser.close()
except Exception as e:
    print("Failed:", e)
