import numpy as np

from backend.AI.reporting import prediction_frame, segmented_metrics


def test_segmented_metrics_separate_changed_and_unchanged_samples():
    frame = prediction_frame(
        np.asarray(["2025-12-01", "2025-12-02"], dtype="datetime64[ns]"),
        np.asarray([20.0, 21.0]),
        np.asarray([20.0, 20.0]),
        np.asarray([20.1, 20.8]),
    )

    metrics = segmented_metrics(frame)

    assert metrics["unchanged"]["samples"] == 1
    assert metrics["changed"]["samples"] == 1
    assert metrics["all"]["samples"] == 2
