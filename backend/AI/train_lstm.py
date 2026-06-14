import argparse
import json
from dataclasses import replace
from pathlib import Path

import numpy as np

from backend.AI.data_pipeline import prepare_dataset, save_preprocessing_metadata
from backend.AI.evaluation import moving_average, naive_last_value, regression_metrics
from backend.AI.lstm_model import build_lstm_model, configure_tensorflow
from backend.AI.training_config import TrainingConfig


def _physical_values(values: np.ndarray, mean: float, std: float) -> np.ndarray:
    return np.asarray(values, dtype=np.float32) * std + mean


def _evaluate_baselines(prepared, target_feature_index: int) -> dict[str, dict[str, float]]:
    actual = prepared.scaler.inverse_target(prepared.test.targets)
    naive = _physical_values(
        naive_last_value(prepared.test.features, target_feature_index),
        prepared.scaler.target_mean,
        prepared.scaler.target_std,
    )
    average = _physical_values(
        moving_average(prepared.test.features, target_feature_index),
        prepared.scaler.target_mean,
        prepared.scaler.target_std,
    )
    return {
        "naive_last_value": regression_metrics(actual, naive),
        "moving_average": regression_metrics(actual, average),
    }


def train(config: TrainingConfig) -> dict:
    config.validate()
    prepared = prepare_dataset(config)
    config.output_dir.mkdir(parents=True, exist_ok=True)
    save_preprocessing_metadata(
        config.output_dir / "preprocessing.json", config, prepared
    )

    tf = configure_tensorflow(config.seed)
    model = build_lstm_model(config)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss",
            patience=config.patience,
            restore_best_weights=True,
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(config.output_dir / "lstm_model.keras"),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]
    history = model.fit(
        prepared.train.features,
        prepared.train.targets,
        validation_data=(prepared.validation.features, prepared.validation.targets),
        epochs=config.epochs,
        batch_size=config.batch_size,
        shuffle=False,
        callbacks=callbacks,
        verbose=2,
    )

    predictions_scaled = model.predict(prepared.test.features, verbose=0).reshape(-1)
    predictions = prepared.scaler.inverse_target(predictions_scaled)
    actual = prepared.scaler.inverse_target(prepared.test.targets)
    target_feature_index = config.feature_columns.index(config.target_column)
    metrics = {
        "model": regression_metrics(actual, predictions),
        "baselines": _evaluate_baselines(prepared, target_feature_index),
        "beats_naive_mae": False,
    }
    metrics["beats_naive_mae"] = (
        metrics["model"]["mae"] < metrics["baselines"]["naive_last_value"]["mae"]
    )

    (config.output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    (config.output_dir / "history.json").write_text(
        json.dumps(
            {key: [float(value) for value in values] for key, values in history.history.items()},
            indent=2,
        ),
        encoding="utf-8",
    )
    return metrics


def parse_args() -> argparse.Namespace:
    defaults = TrainingConfig()
    parser = argparse.ArgumentParser(
        description="Train the TempCastML LSTM on chronological sensor data."
    )
    parser.add_argument("--dataset", type=Path, default=defaults.dataset_path)
    parser.add_argument("--output-dir", type=Path, default=defaults.output_dir)
    parser.add_argument("--epochs", type=int, default=defaults.epochs)
    parser.add_argument("--batch-size", type=int, default=defaults.batch_size)
    parser.add_argument("--sequence-length", type=int, default=defaults.sequence_length)
    parser.add_argument("--forecast-horizon", type=int, default=defaults.forecast_horizon)
    parser.add_argument("--seed", type=int, default=defaults.seed)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = replace(
        TrainingConfig(),
        dataset_path=args.dataset,
        output_dir=args.output_dir,
        epochs=args.epochs,
        batch_size=args.batch_size,
        sequence_length=args.sequence_length,
        forecast_horizon=args.forecast_horizon,
        seed=args.seed,
    )
    metrics = train(config)
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
