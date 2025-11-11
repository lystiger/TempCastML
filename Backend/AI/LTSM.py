
# import tensorflow as tf
# from tensorflow.keras.models import Sequential # type: ignore
# from tensorflow.keras.layers import LSTM, Dense # type: ignore
# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt

# # Cấu hình mô hình LSTM
# SEQ_LENGTH = 10  # Độ dài chuỗi thời gian
# BATCH_SIZE = 32
# EPOCHS = 20

# # Xử lí dữ liệu và các đường dẫn(raw vs processed)
# sensor_data_path = 'data/raw_sensor_data.csv'
# api_data_path = 'data/raw_api_data.csv'
# merged_data_path = 'data/merged_data.csv'

# processed_sensor_data_path = 'data/processed/processed_sensor_data.csv'
# processed_api_data_path = 'data/processed/processed_api_data.csv'
# processed_merged_data_path = 'data/processed/processed_merged_data.csv'

# save_model_path = 'AI/Model/lstm_model.h5'

# # Đọc dữ liệu từ file CSV

# df = pd.read_csv(merged_data_path)

# # Chia dữ liệu thành tập huấn luyện và kiểm tra
# feature_columns = [col for col in df.columns if col != 'label'] # Giả sử 'label' là cột nhãn  
# X_data = df[feature_columns].values # Đặc trưng
# y_data = df['label'].values # Nhãn

# # Chuẩn hóa dữ liệu
# def create_sequences(data, labels, seq_length):
#     xs, ys = [], []
#     for i in range(len(data) - seq_length):
#         xs.append(data[i:(i+seq_length)])
#         ys.append(labels[i+seq_length])
#     return np.array(xs), np.array(ys)

# X, y = create_sequences(X_data, y_data, SEQ_LENGTH)

# # X.shape = (samples, time_steps, features)
# num_features = X.shape[2]
# model = Sequential([
#     LSTM(50, input_shape=(SEQ_LENGTH, 1), return_sequences=False),
#     Dense(1)
# ])

# model.compile(optimizer='adam', loss='mse') # MSE: Mean Squared Error

# # Huấn luyện mô hình
# history = model.fit(X, y, epochs=EPOCHS, batch_size=BATCH_SIZE, validation_split=0.2)

# # Dự đoán
# prediction = model.predict(X)

# # Lưu mô hình
# plt.plot(history.history['loss'], label='train')
# plt.plot(history.history['val_loss'], label='validation')
# plt.legend()
# plt.show()

# # Lưu mô hình đã huấn luyện
# model.save(save_model_path)
# print(f"Mô hình đã được lưu tại {save_model_path}")
# Backend/AI/LSTM.py
import numpy as np
from tensorflow.keras.models import load_model

MODEL_PATH = "AI/Model/lstm_model.h5"

try:
    model = load_model(MODEL_PATH)
except Exception:
    model = None
    print("[Warning] LSTM model not found — using mock predictions")

def predict_temperature(history, horizon=24):
    if model is None:
        # fallback: simple average prediction
        avg = float(np.mean(history))
        return [avg] * horizon

    # preprocess (reshape for LSTM)
    input_seq = np.array(history[-24:]).reshape(1, -1, 1)
    preds = []
    for _ in range(horizon):
        pred = model.predict(input_seq)[0][0]
        preds.append(float(pred))
        input_seq = np.append(input_seq[:, 1:, :], [[[pred]]], axis=1)
    return preds
