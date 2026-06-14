import math
from typing import Iterable

import numpy as np


def regression_metrics(actual: np.ndarray, predicted: np.ndarray) -> dict[str, float]:
    actual = np.asarray(actual, dtype=np.float64).reshape(-1)
    predicted = np.asarray(predicted, dtype=np.float64).reshape(-1)
    if actual.shape != predicted.shape or actual.size == 0:
        raise ValueError("actual and predicted must be non-empty arrays of equal shape")

    errors = predicted - actual
    mae = float(np.mean(np.abs(errors)))
    rmse = float(math.sqrt(np.mean(np.square(errors))))
    denominator = float(np.sum(np.square(actual - np.mean(actual))))
    r_squared = 0.0 if denominator == 0 else 1.0 - float(np.sum(errors**2)) / denominator
    return {"mae": mae, "rmse": rmse, "r2": r_squared}


def naive_last_value(sequence_features: np.ndarray, target_feature_index: int) -> np.ndarray:
    sequences = np.asarray(sequence_features)
    if sequences.ndim != 3:
        raise ValueError("sequence_features must have shape (samples, steps, features)")
    return sequences[:, -1, target_feature_index]


def moving_average(
    sequence_features: np.ndarray, target_feature_index: int, window: int = 6
) -> np.ndarray:
    sequences = np.asarray(sequence_features)
    if sequences.ndim != 3:
        raise ValueError("sequence_features must have shape (samples, steps, features)")
    if window < 1:
        raise ValueError("window must be positive")
    return np.mean(sequences[:, -window:, target_feature_index], axis=1)


def all_finite(values: Iterable[float]) -> bool:
    return all(math.isfinite(float(value)) for value in values)
