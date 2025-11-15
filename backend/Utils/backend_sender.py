import json
import requests
import sys
import os
from backend.Settings.config import BACKEND_URL

BACKEND_URL = "http://localhost:8000/sensor"

def send_to_backend(data):
    """
    Gửi dữ liệu đã phân tích cú pháp đến backend qua HTTP POST request.
    Dữ liệu nên ở định dạng từ điển (dictionary).
    """
    try:
        response = requests.post(BACKEND_URL, json=data)
        print(f"Sent data: {data}, Response code: {response.status_code}")
    except Exception as e:
        print(f"Error sending data: {e}")

if __name__ == "__main__":
    # Chạy script với tệp JSON 
    if len(sys.argv) < 2:
        print("Usage: python backend_sender.py <data_file.json>")
        sys.exit(1)
    
    data_file = sys.argv[1]
    if not os.path.exists(data_file):
        print(f"File {data_file} does not exist.")
        sys.exit(1)
    
    with open(data_file, "r") as f:
        data = json.load(f)
    
    send_to_backend(data)
