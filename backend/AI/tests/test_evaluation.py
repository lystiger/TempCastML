import numpy as np

from backend.AI.evaluation import moving_average, naive_last_value, regression_metrics


def test_regression_metrics_for_exact_predictions():
    actual = np.asarray([20.0, 21.0, 22.0])

    metrics = regression_metrics(actual, actual)

    assert metrics == {"mae": 0.0, "rmse": 0.0, "r2": 1.0}


def test_baselines_use_only_sequence_history():
    sequences = np.asarray(
        [
            [[1.0], [2.0], [3.0]],
            [[4.0], [5.0], [6.0]],
        ]
    )

    assert naive_last_value(sequences, 0).tolist() == [3.0, 6.0]
    assert moving_average(sequences, 0, window=2).tolist() == [2.5, 5.5]
