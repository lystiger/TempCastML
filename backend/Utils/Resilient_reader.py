#resilient_reader.py
#Muc tieu cua phan nay la reconnect khi ket noi hong, tranh reo, crash va dong het cong truoc khi thu lai
import serial, time

from Settings.config import (
    DEFAULT_TIMEOUT,
    DEFAULT_WRITE_TIMEOUT,
    DEFAULT_BAUD,
    DEFAULT_IDLE_LIMIT)

from Utils.port_identifier import identify
from Utils.port_checker import open_serial
from Utils.data_reader import data_reader

def choose_port():
    ports = identify()
    if not ports:
        raise RuntimeError("No ports found")

    port = ports[0][0]
    return port

def resilient_reader(

    baud: int= DEFAULT_BAUD,
    timeout: float = DEFAULT_TIMEOUT,
    write_timeout: float = DEFAULT_WRITE_TIMEOUT,
    idle_limit: int = DEFAULT_IDLE_LIMIT,
    ):

    while True:
        device = choose_port()
        try :
            ser = open_serial(device, baud, timeout=timeout, write_timeout=write_timeout)
            if ser is None:
                print("No Serial port found")
                time.sleep(3)
                continue
            with ser:
                print(f"Serial port opened successfully !!{ser.port}")

                for line in data_reader(ser, idle_LIMIT= idle_limit, encoding = "utf-8"):
                    print(f"Received",line)

        except serial.SerialException as err:
            print(f"Serial port failed to execute {err}")
            time.sleep(3)
            continue
        except KeyboardInterrupt:
            print("User interruption xD")
            break




