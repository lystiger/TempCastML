from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


AI_DIR = Path(__file__).resolve().parent
BACKEND_DIR = AI_DIR.parent


@dataclass(frozen=True)
class TrainingConfig:
    dataset_path: Path = BACKEND_DIR / "Data" / "merged_data.csv"
    output_dir: Path = AI_DIR / "Model"
    timestamp_column: str = "timestamp"
    target_column: str = "temperature"
    feature_columns: tuple[str, ...] = ("temperature",)
    sequence_length: int = 24
    forecast_horizon: int = 1
    train_fraction: float = 0.70
    validation_fraction: float = 0.15
    max_gap_minutes: float = 20.0
    min_temperature: float = 10.0
    max_temperature: float = 45.0
    lstm_units: int = 32
    dropout: float = 0.10
    learning_rate: float = 0.001
    batch_size: int = 32
    epochs: int = 50
    patience: int = 8
    seed: int = 42

    def validate(self) -> None:
        if not self.feature_columns:
            raise ValueError("feature_columns must contain at least one column")
        if self.target_column not in self.feature_columns:
            raise ValueError("target_column must be included in feature_columns")
        if self.sequence_length < 1 or self.forecast_horizon < 1:
            raise ValueError("sequence_length and forecast_horizon must be positive")
        if not 0 < self.train_fraction < 1:
            raise ValueError("train_fraction must be between 0 and 1")
        if not 0 < self.validation_fraction < 1:
            raise ValueError("validation_fraction must be between 0 and 1")
        if self.train_fraction + self.validation_fraction >= 1:
            raise ValueError("train and validation fractions must leave a test split")

    def to_dict(self) -> dict[str, Any]:
        values = asdict(self)
        values["dataset_path"] = str(self.dataset_path)
        values["output_dir"] = str(self.output_dir)
        values["feature_columns"] = list(self.feature_columns)
        return values
