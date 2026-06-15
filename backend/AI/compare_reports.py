import argparse
import json
from pathlib import Path

import matplotlib
import numpy as np

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def load_metrics(report_dir: Path) -> dict:
    summary_path = report_dir / "experiment_summary.json"
    return json.loads(summary_path.read_text(encoding="utf-8"))


def export_comparison(report_dirs: list[Path], output_path: Path) -> None:
    reports = [load_metrics(path) for path in report_dirs]
    labels = [f'{report["config"]["horizon_minutes"]} min' for report in reports]
    model_all = [report["metrics"]["all"]["model"]["mae"] for report in reports]
    persistence_all = [
        report["metrics"]["all"]["persistence"]["mae"] for report in reports
    ]
    model_changed = [
        report["metrics"]["changed"]["model"]["mae"] for report in reports
    ]
    persistence_changed = [
        report["metrics"]["changed"]["persistence"]["mae"] for report in reports
    ]

    x = np.arange(len(labels))
    width = 0.18
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - 1.5 * width, model_all, width, label="model: all")
    ax.bar(x - 0.5 * width, persistence_all, width, label="persistence: all")
    ax.bar(x + 0.5 * width, model_changed, width, label="model: changed")
    ax.bar(
        x + 1.5 * width,
        persistence_changed,
        width,
        label="persistence: changed",
    )
    ax.set_xticks(x, labels)
    ax.set(
        title="Direct Residual Forecast MAE by Horizon",
        xlabel="Forecast horizon",
        ylabel="MAE (C)",
    )
    ax.legend()
    fig.tight_layout()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare residual experiment reports.")
    parser.add_argument("report_dirs", nargs="+", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    export_comparison(args.report_dirs, args.output)


if __name__ == "__main__":
    main()
