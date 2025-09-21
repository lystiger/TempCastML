#data_reader.py
import serial

def data_reader(ser: serial.Serial,
                *,
                idle_LIMIT: int = 5,
                encoding: str = "utf-8:"):

    idle = 0
    try:
        print(f"Da mo cong: {ser.port}")
        while True:
                raw = ser.readline() #kieu doc lai du lieu duoc ghi ra boi cong Serial nay
                if not raw:
                    print(" Khong co byte received(timeout)")
                    idle +=1
                    if idle > idle_LIMIT:   #neu so lan timeout qua 5 lan thi se tu dong break
                        break
                    continue
                idle = 0

                text = raw.decode("utf-8", errors= "replace").strip()
                if text =="END":
                    break
                if not text:
                    print("Khong co text nao received")
                    continue
                try:
                    value = float(text)
                    print(f"Du lieu thu duoc la:{value}")
                except ValueError :
                    print(f"The deo nao lai thu duoc chu ?{text}")
                    value = None
                yield text, value

    except KeyboardInterrupt:
        print(" User doi bye bye")






