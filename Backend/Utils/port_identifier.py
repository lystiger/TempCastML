#port_identifier.py
#dau tien minh muon thu xem la da cai pyserial chua
def identify():
    result=[]

    try:
        from serial.tools import list_ports #import 1 phan cua thu vien pyserial

    except ImportError:
        print("Chua install thu vien pyserial !!!")
    else:
        ports = list_ports.comports()

        if not ports:
            print("Khong tim thay cong dau huhuhu")
        else:
            for port in ports:

                device = getattr(port, "device", "Giá trị không tồn tại") #tên cổng COM, dev

                description = getattr(port, "description", "")
                print(f"{device} : {description}") # in ra ten cong va description cua tung cong
                result.append((device, description))
            return result

def main():
    identify()

if __name__ == "__main__":
    main()

