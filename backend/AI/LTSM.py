import json
from pathlib import Path

import numpy as np


MODEL_DIR = Path(__file__).resolve().parent / "Model"
MODEL_PATH = MODEL_DIR / "lstm_model.keras"
LEGACY_MODEL_PATH = MODEL_DIR / "lstm_model.h5"
PREPROCESSING_PATH = MODEL_DIR / "preprocessing.json"


def _load_artifacts():
    model_path = MODEL_PATH if MODEL_PATH.exists() else LEGACY_MODEL_PATH
    if not model_path.exists() or not PREPROCESSING_PATH.exists():
        return None, None

    try:
        from tensorflow.keras.models import load_model

        loaded_model = load_model(model_path)
        metadata = json.loads(PREPROCESSING_PATH.read_text(encoding="utf-8"))
        return loaded_model, metadata
    except Exception as exc:
        print(f"[Warning] Could not load LSTM artifacts: {exc}")
        return None, None


model, preprocessing = _load_artifacts()
if model is None:
    print("[Warning] LSTM model not found - using average predictions")


def predict_temperature(history, horizon=24):
    """Generate recursive temperature predictions from a temperature history."""
    if not history:
        raise ValueError("history must contain at least one temperature")
    if horizon < 1:
        raise ValueError("horizon must be positive")
    if model is None or preprocessing is None:
        average = float(np.mean(history))
        return [average] * horizon

    config = preprocessing["config"]
    scaler = preprocessing["scaler"]
    if int(config["forecast_horizon"]) != 1:
        raise ValueError("Route inference requires a one-step training artifact")
    feature_columns = scaler["feature_columns"]
    if feature_columns != [scaler["target_column"]]:
        raise ValueError(
            "Route inference currently supports temperature-only training artifacts"
        )

    sequence_length = int(config["sequence_length"])
    if len(history) < sequence_length:
        raise ValueError(
            f"history must contain at least {sequence_length} readings for this model"
        )

    mean = float(scaler["target_mean"])
    std = float(scaler["target_std"])
    sequence = (np.asarray(history[-sequence_length:], dtype=np.float32) - mean) / std
    input_sequence = sequence.reshape(1, sequence_length, 1)
    predictions = []

    for _ in range(horizon):
        prediction_scaled = float(model.predict(input_sequence, verbose=0)[0][0])
        predictions.append(prediction_scaled * std + mean)
        input_sequence = np.append(
            input_sequence[:, 1:, :],
            np.asarray([[[prediction_scaled]]], dtype=np.float32),
            axis=1,
        )
    return predictions
