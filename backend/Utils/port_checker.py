#port_checker.py
import serial #import module chinh cua Pyserial
from typing import Optional
from Settings.config import DEFAULT_BAUD, DEFAULT_TIMEOUT
from Settings.config import DEFAULT_WRITE_TIMEOUT


def open_serial(PORT: str,
                BAUD: int,
                timeout: float,
                write_timeout: float) -> Optional[serial.Serial]:
    """Open a serial port and return a serial object."""
    try:
        ser = serial.Serial(port=PORT, baudrate= BAUD, timeout=timeout, write_timeout=write_timeout)

        ser.reset_input_buffer() #reset lai buffer nhan
        ser.reset_output_buffer() # reset lai buffer output
        print("Opened serial port successfully !!")
        return ser

    except serial.SerialException as err:
        print(f"Failed to open serial port !!{err}")

        return None


if __name__ == "__main__":
    test_port = "COM7"
    test_baud = DEFAULT_BAUD
    test_timeout = DEFAULT_TIMEOUT
    s = open_serial(test_port,test_baud,test_timeout,DEFAULT_WRITE_TIMEOUT)
    if s is not None:
        s.close()
        print("Port opened successfully !!")


