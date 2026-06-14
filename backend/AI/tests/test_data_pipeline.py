from dataclasses import replace

import pandas as pd

from backend.AI.data_pipeline import prepare_dataset
from backend.AI.training_config import TrainingConfig


def _write_dataset(path, rows=120, gap_after=None):
    timestamps = pd.date_range("2025-12-01", periods=rows, freq="10min")
    if gap_after is not None:
        timestamps = timestamps.to_series()
        timestamps.iloc[gap_after:] += pd.Timedelta(hours=2)
        timestamps = timestamps.to_numpy()
    frame = pd.DataFrame(
        {
            "timestamp": timestamps,
            "temperature": [20.0 + index * 0.01 for index in range(rows)],
        }
    )
    frame.to_csv(path, index=False)


def test_prepare_dataset_splits_by_target_time_and_scales_from_train(tmp_path):
    dataset_path = tmp_path / "data.csv"
    _write_dataset(dataset_path)
    config = replace(
        TrainingConfig(),
        dataset_path=dataset_path,
        sequence_length=6,
        train_fraction=0.6,
        validation_fraction=0.2,
    )

    prepared = prepare_dataset(config)

    assert prepared.train.timestamps.max() < prepared.validation.timestamps.min()
    assert prepared.validation.timestamps.max() < prepared.test.timestamps.min()
    assert abs(float(prepared.train.features.mean())) < 0.2
    assert prepared.scaler.target_column == "temperature"


def test_prepare_dataset_does_not_create_sequences_across_large_gaps(tmp_path):
    dataset_path = tmp_path / "data.csv"
    _write_dataset(dataset_path, gap_after=60)
    config = replace(
        TrainingConfig(),
        dataset_path=dataset_path,
        sequence_length=6,
        train_fraction=0.6,
        validation_fraction=0.2,
        max_gap_minutes=20,
    )

    prepared = prepare_dataset(config)

    all_timestamps = (
        list(prepared.train.timestamps)
        + list(prepared.validation.timestamps)
        + list(prepared.test.timestamps)
    )
    first_after_gap = pd.Timestamp("2025-12-01") + pd.Timedelta(minutes=600) + pd.Timedelta(
        hours=2
    )
    assert first_after_gap.to_datetime64() not in all_timestamps
