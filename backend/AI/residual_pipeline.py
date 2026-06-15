import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from backend.AI.training_config import AI_DIR, BACKEND_DIR


ENGINEERED_FEATURES = (
    "temperature",
    "humidity",
    "outside_temp",
    "outside_humidity",
    "outside_pressure",
    "temp_delta_outside",
    "hour_sin",
    "hour_cos",
    "day_sin",
    "day_cos",
)


@dataclass(frozen=True)
class ResidualTrainingConfig:
    dataset_path: Path = BACKEND_DIR / "Data" / "merged_data.csv"
    model_output_dir: Path = AI_DIR / "Model" / "residual_60min"
    report_output_dir: Path = AI_DIR / "Reports" / "residual_60min"
    feature_columns: tuple[str, ...] = ENGINEERED_FEATURES
    sequence_length: int = 24
    forecast_horizon: int = 6
    train_fraction: float = 0.70
    validation_fraction: float = 0.15
    max_gap_minutes: float = 20.0
    min_temperature: float = 15.0
    max_temperature: float = 45.0
    lstm_units: int = 32
    dropout: float = 0.10
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 50
    patience: int = 8
    seed: int = 42

    @property
    def horizon_minutes(self) -> int:
        return self.forecast_horizon * 10

    def validate(self) -> None:
        if self.sequence_length < 1 or self.forecast_horizon < 1:
            raise ValueError("sequence_length and forecast_horizon must be positive")
        if not 0 < self.train_fraction < 1 or not 0 < self.validation_fraction < 1:
            raise ValueError("split fractions must be between 0 and 1")
        if self.train_fraction + self.validation_fraction >= 1:
            raise ValueError("train and validation fractions must leave a test split")

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["dataset_path"] = str(self.dataset_path)
        values["model_output_dir"] = str(self.model_output_dir)
        values["report_output_dir"] = str(self.report_output_dir)
        values["feature_columns"] = list(self.feature_columns)
        values["horizon_minutes"] = self.horizon_minutes
        return values


@dataclass(frozen=True)
class ResidualScaler:
    feature_columns: tuple[str, ...]
    feature_means: tuple[float, ...]
    feature_stds: tuple[float, ...]
    residual_mean: float
    residual_std: float

    def transform_features(self, values: np.ndarray) -> np.ndarray:
        means = np.asarray(self.feature_means, dtype=np.float32)
        stds = np.asarray(self.feature_stds, dtype=np.float32)
        return (values.astype(np.float32) - means) / stds

    def transform_residuals(self, values: np.ndarray) -> np.ndarray:
        return (values.astype(np.float32) - self.residual_mean) / self.residual_std

    def inverse_residuals(self, values: np.ndarray) -> np.ndarray:
        return values.astype(np.float32) * self.residual_std + self.residual_mean

    def to_dict(self) -> dict[str, Any]:
        return {
            "feature_columns": list(self.feature_columns),
            "feature_means": list(self.feature_means),
            "feature_stds": list(self.feature_stds),
            "residual_mean": self.residual_mean,
            "residual_std": self.residual_std,
        }


@dataclass(frozen=True)
class ResidualSplit:
    features: np.ndarray
    residual_targets: np.ndarray
    anchor_temperatures: np.ndarray
    future_temperatures: np.ndarray
    timestamps: np.ndarray


@dataclass(frozen=True)
class PreparedResidualDataset:
    train: ResidualSplit
    validation: ResidualSplit
    test: ResidualSplit
    scaler: ResidualScaler
    source_rows: int
    cleaned_rows: int
    dropped_rows: int
    date_start: str
    date_end: str


def load_feature_frame(config: ResidualTrainingConfig) -> tuple[pd.DataFrame, int]:
    config.validate()
    frame = pd.read_csv(config.dataset_path)
    source_rows = len(frame)
    required = [
        "timestamp",
        "temperature",
        "humidity",
        "outside_temp",
        "outside_humidity",
        "outside_pressure",
    ]
    missing = sorted(set(required).difference(frame.columns))
    if missing:
        raise ValueError(f"Dataset is missing required columns: {', '.join(missing)}")

    frame = frame.loc[:, required].copy()
    frame["timestamp"] = pd.to_datetime(frame["timestamp"], errors="coerce")
    for column in required[1:]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame = frame.dropna(subset=required)
    frame = frame[
        frame["temperature"].between(
            config.min_temperature, config.max_temperature, inclusive="both"
        )
    ]
    frame = frame.sort_values("timestamp").drop_duplicates("timestamp", keep="last")

    hour = frame["timestamp"].dt.hour + frame["timestamp"].dt.minute / 60.0
    day = frame["timestamp"].dt.dayofweek
    frame["temp_delta_outside"] = frame["temperature"] - frame["outside_temp"]
    frame["hour_sin"] = np.sin(2 * np.pi * hour / 24)
    frame["hour_cos"] = np.cos(2 * np.pi * hour / 24)
    frame["day_sin"] = np.sin(2 * np.pi * day / 7)
    frame["day_cos"] = np.cos(2 * np.pi * day / 7)
    frame = frame.reset_index(drop=True)

    missing_features = sorted(set(config.feature_columns).difference(frame.columns))
    if missing_features:
        raise ValueError(
            f"Engineered frame is missing features: {', '.join(missing_features)}"
        )
    return frame, source_rows


def _valid_examples(
    frame: pd.DataFrame, config: ResidualTrainingConfig
) -> list[tuple[int, int, int]]:
    timestamps = frame["timestamp"].to_numpy(dtype="datetime64[ns]")
    max_gap = np.timedelta64(int(config.max_gap_minutes * 60), "s")
    examples = []
    for target_index in range(
        config.sequence_length + config.forecast_horizon - 1, len(frame)
    ):
        sequence_end = target_index - config.forecast_horizon + 1
        sequence_start = sequence_end - config.sequence_length
        if np.any(np.diff(timestamps[sequence_start : target_index + 1]) > max_gap):
            continue
        examples.append((sequence_start, sequence_end, target_index))
    return examples


def fit_residual_scaler(
    frame: pd.DataFrame,
    config: ResidualTrainingConfig,
    examples: list[tuple[int, int, int]],
    train_end: int,
) -> ResidualScaler:
    train_frame = frame.iloc[:train_end]
    means = train_frame.loc[:, config.feature_columns].mean().to_numpy()
    stds = train_frame.loc[:, config.feature_columns].std(ddof=0).to_numpy()
    stds = np.where(stds == 0, 1.0, stds)
    residuals = np.asarray(
        [
            frame["temperature"].iloc[target] - frame["temperature"].iloc[end - 1]
            for _, end, target in examples
            if target < train_end
        ],
        dtype=np.float32,
    )
    residual_std = float(residuals.std())
    return ResidualScaler(
        feature_columns=config.feature_columns,
        feature_means=tuple(float(value) for value in means),
        feature_stds=tuple(float(value) for value in stds),
        residual_mean=float(residuals.mean()),
        residual_std=residual_std if residual_std else 1.0,
    )


def _build_split(
    frame: pd.DataFrame,
    config: ResidualTrainingConfig,
    scaler: ResidualScaler,
    examples: list[tuple[int, int, int]],
    target_start: int,
    target_end: int,
) -> ResidualSplit:
    features = scaler.transform_features(
        frame.loc[:, config.feature_columns].to_numpy(dtype=np.float32)
    )
    temperatures = frame["temperature"].to_numpy(dtype=np.float32)
    timestamps = frame["timestamp"].to_numpy(dtype="datetime64[ns]")
    selected = [item for item in examples if target_start <= item[2] < target_end]
    sequences = np.asarray(
        [features[start:end] for start, end, _ in selected], dtype=np.float32
    )
    anchors = np.asarray(
        [temperatures[end - 1] for _, end, _ in selected], dtype=np.float32
    )
    future = np.asarray(
        [temperatures[target] for _, _, target in selected], dtype=np.float32
    )
    residuals = scaler.transform_residuals(future - anchors)
    return ResidualSplit(
        features=sequences,
        residual_targets=residuals,
        anchor_temperatures=anchors,
        future_temperatures=future,
        timestamps=np.asarray(
            [timestamps[target] for _, _, target in selected], dtype="datetime64[ns]"
        ),
    )


def prepare_residual_dataset(config: ResidualTrainingConfig) -> PreparedResidualDataset:
    frame, source_rows = load_feature_frame(config)
    train_end = int(len(frame) * config.train_fraction)
    validation_end = int(
        len(frame) * (config.train_fraction + config.validation_fraction)
    )
    examples = _valid_examples(frame, config)
    scaler = fit_residual_scaler(frame, config, examples, train_end)
    prepared = PreparedResidualDataset(
        train=_build_split(frame, config, scaler, examples, 0, train_end),
        validation=_build_split(
            frame, config, scaler, examples, train_end, validation_end
        ),
        test=_build_split(frame, config, scaler, examples, validation_end, len(frame)),
        scaler=scaler,
        source_rows=source_rows,
        cleaned_rows=len(frame),
        dropped_rows=source_rows - len(frame),
        date_start=frame["timestamp"].iloc[0].isoformat(),
        date_end=frame["timestamp"].iloc[-1].isoformat(),
    )
    for name in ("train", "validation", "test"):
        if len(getattr(prepared, name).residual_targets) == 0:
            raise ValueError(f"No valid {name} examples remain after preprocessing")
    return prepared


def save_residual_metadata(
    path: Path, config: ResidualTrainingConfig, prepared: PreparedResidualDataset
) -> None:
    payload = {
        "artifact_version": 1,
        "model_type": "direct_residual_lstm",
        "config": config.to_dict(),
        "scaler": prepared.scaler.to_dict(),
        "dataset": {
            "source_rows": prepared.source_rows,
            "cleaned_rows": prepared.cleaned_rows,
            "dropped_rows": prepared.dropped_rows,
            "date_start": prepared.date_start,
            "date_end": prepared.date_end,
            "example_counts": {
                "train": len(prepared.train.residual_targets),
                "validation": len(prepared.validation.residual_targets),
                "test": len(prepared.test.residual_targets),
            },
        },
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
