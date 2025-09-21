#data_parser.py
#Parse data ( CSV/ key = value / JSON lines )
#Thiết bị gửi chuỗi thô: muốn tính toán lại ta cần phải chuyển thành số có nghĩa
#Định dạng dòng ổn định giúp bạn dễ dàng debug

#this is parser.py

import json
from typing import List, Dict, Tuple, Any

def parse_csv(s: str)-> List[float]: #caái này giúp ta có thể return type hint: mình muốn 1 list có phần tử là float
    parts = []
    raw = s.split(",")
    if len(raw) <2:
        raise ValueError ("CSV thiếu cột rồi con chó ngu")
    for part in s.split(","):  # này là hàm for chạy part ( là 1 item ) lặp lại thôi
        parts.append(float(part.strip()))
    return parts

    #ép 2 phần tử trong list thành số float

def parse_kv(s: str) -> Dict[str, float]: #Hàm này được viết để chuyển một chuỗi key=value (danh sách cặp) thành dictionary ,
                        # đồng thời ép giá trị (value) về kiểu float.
    out: Dict[str, float] ={}
    tokens = s.split(",")
    for item in tokens:
        if "=" not in item:
            raise ValueError ("Trong item đéo có = con chó ngu ơi")

        k,v = item.split("=", 1)

        k = k.strip() #cnay để loại bỏ khoảng trắng quanh key
        v = v.strip()  #cnay để loại bỏ khoảng trắng quanh value
        try:
            out[k] = float(v)
        except ValueError:
            raise ValueError (f"Giá trị của key:{k} là chữ mà dcm {v}")
    return out

def parse_json_lines(s: str): #Cnay để đọc chuỗi json từ ESP32
    # để chuyển 2 trị số "temp": 25, "humidity": 43% thaành (temp, humidity)
    obj = json.loads(s) # -> sau dòng này obj là 1 dict
    t = obj["temp"]
    h=obj["humidity"]
    return t,h



