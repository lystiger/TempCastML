from dataclasses import replace

import numpy as np
import pandas as pd

from backend.AI.residual_pipeline import (
    ResidualTrainingConfig,
    prepare_residual_dataset,
)


def _write_dataset(path, rows=180, gap_after=None):
    timestamps = pd.date_range("2025-12-01", periods=rows, freq="10min")
    if gap_after is not None:
        timestamps = timestamps.to_series()
        timestamps.iloc[gap_after:] += pd.Timedelta(hours=2)
        timestamps = timestamps.to_numpy()
    base = np.arange(rows, dtype=float)
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "temperature": 20 + base * 0.01,
            "humidity": 60 + np.sin(base / 10),
            "outside_temp": 18 + np.sin(base / 20),
            "outside_humidity": 70 + np.cos(base / 10),
            "outside_pressure": 1015 + np.sin(base / 30),
        }
    )
    frame.to_csv(path, index=False)


def test_residual_targets_reconstruct_future_temperature(tmp_path):
    dataset_path = tmp_path / "data.csv"
    _write_dataset(dataset_path)
    config = replace(
        ResidualTrainingConfig(),
        dataset_path=dataset_path,
        sequence_length=12,
        forecast_horizon=6,
        train_fraction=0.6,
        validation_fraction=0.2,
    )

    prepared = prepare_residual_dataset(config)
    residuals = prepared.scaler.inverse_residuals(prepared.test.residual_targets)

    np.testing.assert_allclose(
        prepared.test.anchor_temperatures + residuals,
        prepared.test.future_temperatures,
        atol=1e-5,
    )
    assert prepared.train.timestamps.max() < prepared.validation.timestamps.min()
    assert prepared.validation.timestamps.max() < prepared.test.timestamps.min()


def test_residual_examples_do_not_cross_large_gaps(tmp_path):
    dataset_path = tmp_path / "data.csv"
    _write_dataset(dataset_path, gap_after=90)
    config = replace(
        ResidualTrainingConfig(),
        dataset_path=dataset_path,
        sequence_length=12,
        forecast_horizon=6,
        train_fraction=0.6,
        validation_fraction=0.2,
        max_gap_minutes=20,
    )

    prepared = prepare_residual_dataset(config)
    timestamps = np.concatenate(
        [
            prepared.train.timestamps,
            prepared.validation.timestamps,
            prepared.test.timestamps,
        ]
    )
    first_after_gap = (
        pd.Timestamp("2025-12-01")
        + pd.Timedelta(minutes=900)
        + pd.Timedelta(hours=2)
    )
    assert first_after_gap.to_datetime64() not in timestamps
