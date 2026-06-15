import argparse
import json
from dataclasses import replace
from pathlib import Path

from backend.AI.evaluation import regression_metrics
from backend.AI.lstm_model import configure_tensorflow
from backend.AI.reporting import (
    export_charts,
    prediction_frame,
    segmented_metrics,
    write_report_summary,
)
from backend.AI.residual_pipeline import (
    ResidualTrainingConfig,
    prepare_residual_dataset,
    save_residual_metadata,
)


def build_residual_model(config: ResidualTrainingConfig):
    tf = configure_tensorflow(config.seed)
    model = tf.keras.Sequential(
        [
            tf.keras.layers.Input(
                shape=(config.sequence_length, len(config.feature_columns))
            ),
            tf.keras.layers.LSTM(config.lstm_units),
            tf.keras.layers.Dropout(config.dropout),
            tf.keras.layers.Dense(1),
        ],
        name="tempcast_direct_residual_lstm",
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model


def train_residual_model(config: ResidualTrainingConfig) -> dict:
    prepared = prepare_residual_dataset(config)
    config.model_output_dir.mkdir(parents=True, exist_ok=True)
    config.report_output_dir.mkdir(parents=True, exist_ok=True)
    save_residual_metadata(
        config.model_output_dir / "preprocessing.json", config, prepared
    )

    tf = configure_tensorflow(config.seed)
    model = build_residual_model(config)
    callbacks = [
        tf.keras.callbacks.EarlyStopping(
            monitor="val_loss", patience=config.patience, restore_best_weights=True
        ),
        tf.keras.callbacks.ModelCheckpoint(
            filepath=str(config.model_output_dir / "residual_lstm.keras"),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]
    history = model.fit(
        prepared.train.features,
        prepared.train.residual_targets,
        validation_data=(
            prepared.validation.features,
            prepared.validation.residual_targets,
        ),
        epochs=config.epochs,
        batch_size=config.batch_size,
        shuffle=False,
        callbacks=callbacks,
        verbose=2,
    )

    predicted_residuals = prepared.scaler.inverse_residuals(
        model.predict(prepared.test.features, verbose=0).reshape(-1)
    )
    predictions = prepared.test.anchor_temperatures + predicted_residuals
    frame = prediction_frame(
        prepared.test.timestamps,
        prepared.test.future_temperatures,
        prepared.test.anchor_temperatures,
        predictions,
    )
    metrics = segmented_metrics(frame)
    metrics["beats_persistence_mae"] = (
        metrics["all"]["model"]["mae"] < metrics["all"]["persistence"]["mae"]
    )
    history_values = {
        key: [float(value) for value in values] for key, values in history.history.items()
    }
    dataset = {
        "source_rows": prepared.source_rows,
        "cleaned_rows": prepared.cleaned_rows,
        "dropped_rows": prepared.dropped_rows,
        "date_start": prepared.date_start,
        "date_end": prepared.date_end,
        "examples": {
            "train": len(prepared.train.residual_targets),
            "validation": len(prepared.validation.residual_targets),
            "test": len(prepared.test.residual_targets),
        },
    }
    frame.to_csv(config.report_output_dir / "test_predictions.csv", index=False)
    export_charts(config.report_output_dir, history_values, frame, metrics)
    write_report_summary(
        config.report_output_dir, metrics, config.to_dict(), dataset
    )
    (config.report_output_dir / "history.json").write_text(
        json.dumps(history_values, indent=2), encoding="utf-8"
    )
    return metrics


def parse_args() -> argparse.Namespace:
    defaults = ResidualTrainingConfig()
    parser = argparse.ArgumentParser(
        description="Train a direct multivariate residual LSTM experiment."
    )
    parser.add_argument("--dataset", type=Path, default=defaults.dataset_path)
    parser.add_argument("--model-output-dir", type=Path, default=defaults.model_output_dir)
    parser.add_argument(
        "--report-output-dir", type=Path, default=defaults.report_output_dir
    )
    parser.add_argument("--epochs", type=int, default=defaults.epochs)
    parser.add_argument("--forecast-horizon", type=int, default=defaults.forecast_horizon)
    parser.add_argument("--seed", type=int, default=defaults.seed)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    config = replace(
        ResidualTrainingConfig(),
        dataset_path=args.dataset,
        model_output_dir=args.model_output_dir,
        report_output_dir=args.report_output_dir,
        epochs=args.epochs,
        forecast_horizon=args.forecast_horizon,
        seed=args.seed,
    )
    print(json.dumps(train_residual_model(config), indent=2))


if __name__ == "__main__":
    main()
