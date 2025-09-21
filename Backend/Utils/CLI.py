#final CLI :D

import serial, time
from typing import List, Tuple, Optional, Dict, Any
import argparse
from config import (
    DEFAULT_TIMEOUT,
    DEFAULT_WRITE_TIMEOUT,
    DEFAULT_BAUD,
    DEFAULT_IDLE_LIMIT)
from port_identifier import identify
from port_checker import open_serial
from data_reader import data_reader
from Resilient_reader import choose_port, resilient_reader


def main():
    parser = argparse.ArgumentParser(description="DHT11 project parser của bé Ly và anh Hùng đẹp trai")
    parser.add_argument("-port", default= "",required=False, help="Serial port name (Tu dien di con cho ngu/hoac khong thi dung identifier kia dcm")
    parser.add_argument("--baud", type = int, default = 115200, required = False, help = "Serial baud rate (kien nghi 115200)")
    parser.add_argument("--timeout", type = float, default = DEFAULT_TIMEOUT, required = False, help = "Serial timeout (s)")
    parser.add_argument("--write_timeout", type = float, default = DEFAULT_WRITE_TIMEOUT, required = False, help = "Serial write_timeout (s)")
    parser.add_argument("__idle_limit", type = int, default = DEFAULT_IDLE_LIMIT, help = "Serial idle limit (s)"
                        )
    args = parser.parse_args()

    if args.port and args.timeout and args.write_timeout:
        print(f"Mo cong do user nhap:{args.port}")
        device = args.port
        idle_limit = args.idle_limit
        while True:

            try:
                ser = serial.Serial(device, baudrate = args.baud, timeout = args.timeout)
                if ser is None:
                    print("Serial port error")
                    time.sleep(5)
                    continue
                with open_serial(device, args.baud, args.timeout, args.write_timeout) as ser:
                    print(f"Serial port opened successfully !!{ser.port}")

                    for line in data_reader(ser, idle_LIMIT=idle_limit, encoding="utf-8"):
                        print(f"Received",line)


            except serial.SerialException as err:
                print(f"Serial port failed to execute {err}")
                time.sleep(3)
                continue
            except KeyboardInterrupt:
                print("User interruption xD")
                break

    else:
        print(f"Lam deo gi nhap port con cho ngu ? tu tim port di")
        resilient_reader(DEFAULT_BAUD, DEFAULT_TIMEOUT, DEFAULT_WRITE_TIMEOUT, DEFAULT_IDLE_LIMIT)

if __name__ == "__main__":
    main()
