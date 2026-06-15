import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from backend.AI.evaluation import regression_metrics


def prediction_frame(
    timestamps: np.ndarray,
    actual: np.ndarray,
    anchors: np.ndarray,
    predictions: np.ndarray,
) -> pd.DataFrame:
    frame = pd.DataFrame(
        {
            "timestamp": pd.to_datetime(timestamps),
            "actual": actual,
            "persistence": anchors,
            "prediction": predictions,
        }
    )
    frame["actual_change"] = frame["actual"] - frame["persistence"]
    frame["model_error"] = frame["prediction"] - frame["actual"]
    frame["model_absolute_error"] = frame["model_error"].abs()
    frame["persistence_absolute_error"] = (
        frame["persistence"] - frame["actual"]
    ).abs()
    return frame


def segmented_metrics(frame: pd.DataFrame) -> dict:
    changed = frame["actual_change"].abs() >= 0.1
    segments = {
        "all": frame,
        "unchanged": frame[~changed],
        "changed": frame[changed],
    }
    metrics = {}
    for name, segment in segments.items():
        if segment.empty:
            continue
        metrics[name] = {
            "samples": len(segment),
            "model": regression_metrics(segment["actual"], segment["prediction"]),
            "persistence": regression_metrics(
                segment["actual"], segment["persistence"]
            ),
            "model_bias": float(segment["model_error"].mean()),
        }
    return metrics


def export_charts(
    output_dir: Path,
    history: dict[str, list[float]],
    frame: pd.DataFrame,
    metrics: dict,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(history["loss"], label="train loss")
    ax.plot(history["val_loss"], label="validation loss")
    ax.set(title="Residual LSTM Training Loss", xlabel="Epoch", ylabel="MSE")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "training_loss.png", dpi=160)
    plt.close(fig)

    plot_frame = frame.copy()
    gap_starts = plot_frame["timestamp"].diff() > pd.Timedelta(minutes=20)
    plot_frame.loc[
        gap_starts, ["actual", "persistence", "prediction"]
    ] = np.nan

    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(
        plot_frame["timestamp"], plot_frame["actual"], label="actual", linewidth=1.5
    )
    ax.plot(
        plot_frame["timestamp"],
        plot_frame["persistence"],
        label="persistence",
        linewidth=1,
        alpha=0.75,
    )
    ax.plot(
        plot_frame["timestamp"],
        plot_frame["prediction"],
        label="residual LSTM",
        linewidth=1,
        alpha=0.85,
    )
    ax.set(title="Test Forecasts", xlabel="Time", ylabel="Temperature (C)")
    ax.legend()
    fig.autofmt_xdate()
    fig.tight_layout()
    fig.savefig(output_dir / "test_forecasts.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        frame["actual_change"],
        frame["model_error"],
        alpha=0.55,
        s=18,
    )
    ax.axhline(0, color="black", linewidth=1)
    ax.set(
        title="Model Error vs Actual Temperature Change",
        xlabel="Actual temperature change (C)",
        ylabel="Prediction error (C)",
    )
    fig.tight_layout()
    fig.savefig(output_dir / "error_vs_change.png", dpi=160)
    plt.close(fig)

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(frame["actual_change"], bins=30)
    ax.set(
        title="Test Temperature Change Distribution",
        xlabel="Actual temperature change (C)",
        ylabel="Samples",
    )
    fig.tight_layout()
    fig.savefig(output_dir / "change_distribution.png", dpi=160)
    plt.close(fig)

    labels = ["All", "Unchanged", "Changed"]
    model_mae = [
        metrics[name]["model"]["mae"]
        for name in ("all", "unchanged", "changed")
        if name in metrics
    ]
    persistence_mae = [
        metrics[name]["persistence"]["mae"]
        for name in ("all", "unchanged", "changed")
        if name in metrics
    ]
    x = np.arange(len(model_mae))
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.bar(x - 0.18, model_mae, width=0.36, label="residual LSTM")
    ax.bar(x + 0.18, persistence_mae, width=0.36, label="persistence")
    ax.set_xticks(x, labels[: len(x)])
    ax.set(title="MAE by Test Segment", ylabel="MAE (C)")
    ax.legend()
    fig.tight_layout()
    fig.savefig(output_dir / "segment_mae.png", dpi=160)
    plt.close(fig)


def write_report_summary(
    output_dir: Path, metrics: dict, config: dict, dataset: dict
) -> None:
    payload = {"config": config, "dataset": dataset, "metrics": metrics}
    (output_dir / "experiment_summary.json").write_text(
        json.dumps(payload, indent=2), encoding="utf-8"
    )
