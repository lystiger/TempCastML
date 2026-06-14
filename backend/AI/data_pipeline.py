import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from backend.AI.training_config import TrainingConfig


@dataclass(frozen=True)
class StandardizationStats:
    feature_columns: tuple[str, ...]
    feature_means: tuple[float, ...]
    feature_stds: tuple[float, ...]
    target_column: str
    target_mean: float
    target_std: float

    def transform_features(self, values: np.ndarray) -> np.ndarray:
        means = np.asarray(self.feature_means, dtype=np.float32)
        stds = np.asarray(self.feature_stds, dtype=np.float32)
        return (values.astype(np.float32) - means) / stds

    def transform_target(self, values: np.ndarray) -> np.ndarray:
        return (values.astype(np.float32) - self.target_mean) / self.target_std

    def inverse_target(self, values: np.ndarray) -> np.ndarray:
        return values.astype(np.float32) * self.target_std + self.target_mean

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_columns": list(self.feature_columns),
            "feature_means": list(self.feature_means),
            "feature_stds": list(self.feature_stds),
            "target_column": self.target_column,
            "target_mean": self.target_mean,
            "target_std": self.target_std,
        }


@dataclass(frozen=True)
class SequenceSplit:
    features: np.ndarray
    targets: np.ndarray
    timestamps: np.ndarray


@dataclass(frozen=True)
class PreparedDataset:
    train: SequenceSplit
    validation: SequenceSplit
    test: SequenceSplit
    scaler: StandardizationStats
    source_rows: int
    cleaned_rows: int
    dropped_rows: int
    date_start: str
    date_end: str


def load_and_clean_dataset(config: TrainingConfig) -> tuple[pd.DataFrame, int]:
    config.validate()
    frame = pd.read_csv(config.dataset_path)
    source_rows = len(frame)
    required = list(
        dict.fromkeys(
            [config.timestamp_column, *config.feature_columns, config.target_column]
        )
    )
    missing = sorted(set(required).difference(frame.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

    frame = frame.loc[:, required].copy()
    frame[config.timestamp_column] = pd.to_datetime(
        frame[config.timestamp_column], errors="coerce"
    )
    for column in set(config.feature_columns).union({config.target_column}):
        frame[column] = pd.to_numeric(frame[column], errors="coerce")

    frame = frame.dropna(subset=required)
    frame = frame[
        frame[config.target_column].between(
            config.min_temperature, config.max_temperature, inclusive="both"
        )
    ]
    frame = frame.sort_values(config.timestamp_column)
    frame = frame.drop_duplicates(subset=[config.timestamp_column], keep="last")
    frame = frame.reset_index(drop=True)

    minimum_rows = config.sequence_length + config.forecast_horizon + 2
    if len(frame) < minimum_rows:
        raise ValueError(
            f"Dataset has {len(frame)} usable rows; at least {minimum_rows} are required"
        )
    return frame, source_rows


def fit_scaler(
    frame: pd.DataFrame, config: TrainingConfig, train_end: int
) -> StandardizationStats:
    train_frame = frame.iloc[:train_end]
    feature_means = train_frame.loc[:, config.feature_columns].mean().to_numpy()
    feature_stds = train_frame.loc[:, config.feature_columns].std(ddof=0).to_numpy()
    feature_stds = np.where(feature_stds == 0, 1.0, feature_stds)
    target_mean = float(train_frame[config.target_column].mean())
    target_std = float(train_frame[config.target_column].std(ddof=0))
    if target_std == 0:
        target_std = 1.0

    return StandardizationStats(
        feature_columns=config.feature_columns,
        feature_means=tuple(float(value) for value in feature_means),
        feature_stds=tuple(float(value) for value in feature_stds),
        target_column=config.target_column,
        target_mean=target_mean,
        target_std=target_std,
    )


def _empty_split(config: TrainingConfig) -> SequenceSplit:
    return SequenceSplit(
        features=np.empty(
            (0, config.sequence_length, len(config.feature_columns)), dtype=np.float32
        ),
        targets=np.empty((0,), dtype=np.float32),
        timestamps=np.empty((0,), dtype="datetime64[ns]"),
    )


def _build_sequences(
    frame: pd.DataFrame,
    config: TrainingConfig,
    scaler: StandardizationStats,
    target_start: int,
    target_end: int,
) -> SequenceSplit:
    features = scaler.transform_features(
        frame.loc[:, config.feature_columns].to_numpy(dtype=np.float32)
    )
    targets = scaler.transform_target(
        frame[config.target_column].to_numpy(dtype=np.float32)
    )
    timestamps = frame[config.timestamp_column].to_numpy(dtype="datetime64[ns]")
    max_gap = np.timedelta64(int(config.max_gap_minutes * 60), "s")

    sequence_values: list[np.ndarray] = []
    target_values: list[float] = []
    target_timestamps: list[np.datetime64] = []

    first_target = max(
        target_start, config.sequence_length + config.forecast_horizon - 1
    )
    for target_index in range(first_target, target_end):
        sequence_end = target_index - config.forecast_horizon + 1
        sequence_start = sequence_end - config.sequence_length
        window_timestamps = timestamps[sequence_start : target_index + 1]
        if np.any(np.diff(window_timestamps) > max_gap):
            continue
        sequence_values.append(features[sequence_start:sequence_end])
        target_values.append(float(targets[target_index]))
        target_timestamps.append(timestamps[target_index])

    if not sequence_values:
        return _empty_split(config)

    return SequenceSplit(
        features=np.asarray(sequence_values, dtype=np.float32),
        targets=np.asarray(target_values, dtype=np.float32),
        timestamps=np.asarray(target_timestamps, dtype="datetime64[ns]"),
    )


def prepare_dataset(config: TrainingConfig) -> PreparedDataset:
    frame, source_rows = load_and_clean_dataset(config)
    train_end = int(len(frame) * config.train_fraction)
    validation_end = int(
        len(frame) * (config.train_fraction + config.validation_fraction)
    )
    scaler = fit_scaler(frame, config, train_end)

    prepared = PreparedDataset(
        train=_build_sequences(frame, config, scaler, 0, train_end),
        validation=_build_sequences(frame, config, scaler, train_end, validation_end),
        test=_build_sequences(frame, config, scaler, validation_end, len(frame)),
        scaler=scaler,
        source_rows=source_rows,
        cleaned_rows=len(frame),
        dropped_rows=source_rows - len(frame),
        date_start=frame[config.timestamp_column].iloc[0].isoformat(),
        date_end=frame[config.timestamp_column].iloc[-1].isoformat(),
    )
    for name in ("train", "validation", "test"):
        if len(getattr(prepared, name).targets) == 0:
            raise ValueError(f"No valid {name} sequences remain after preprocessing")
    return prepared


def save_preprocessing_metadata(
    path: Path, config: TrainingConfig, prepared: PreparedDataset
) -> None:
    payload = {
        "artifact_version": 1,
        "config": config.to_dict(),
        "scaler": prepared.scaler.to_dict(),
        "dataset": {
            "source_rows": prepared.source_rows,
            "cleaned_rows": prepared.cleaned_rows,
            "dropped_rows": prepared.dropped_rows,
            "date_start": prepared.date_start,
            "date_end": prepared.date_end,
            "sequence_counts": {
                "train": len(prepared.train.targets),
                "validation": len(prepared.validation.targets),
                "test": len(prepared.test.targets),
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
