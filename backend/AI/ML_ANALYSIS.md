# TempCastML AI/ML Analysis

## Current Status

The repository now has two reproducible modeling paths:

- `train_lstm.py`: one-step, temperature-only absolute-temperature LSTM used to
  validate the original forecasting approach.
- `train_residual_lstm.py`: direct multivariate residual LSTM experiments that
  predict temperature change over a fixed horizon.

The direct residual experiments use:

- Indoor temperature and humidity.
- Outside temperature, humidity, and pressure.
- Indoor-to-outside temperature difference.
- Cyclical hour-of-day and day-of-week features.
- A 24-reading history, representing roughly four hours.
- Chronological train, validation, and test splits.
- Gap rejection so examples do not cross missing collection periods.

Generated reports:

- [30-minute report](Reports/residual_30min/experiment_summary.json)
- [60-minute report](Reports/residual_60min/experiment_summary.json)
- [Horizon comparison chart](Reports/horizon_comparison.png)

## Problem

The dataset strongly favors a persistence forecast:

```text
future temperature = latest observed temperature
```

Most short-horizon readings do not change. A model that predicts small changes
can improve forecasts during actual movement but still lose overall because it
introduces error during the larger unchanged segment.

The chronological split also exposes distribution shift. The test period is
colder than the training and validation periods, and both residual experiments
retain a positive prediction bias.

## Experiment Results

### Direct 30-Minute Residual Forecast

| Segment | Samples | Residual LSTM MAE | Persistence MAE |
|---|---:|---:|---:|
| All test examples | 418 | 0.177 C | 0.104 C |
| Unchanged examples | 315 | 0.100 C | 0.001 C |
| Changed examples | 103 | 0.413 C | 0.419 C |

The model slightly improves changed-event MAE by approximately `0.006 C`, but
its `+0.101 C` overall bias makes it worse across all examples.

Charts:

- [Training loss](Reports/residual_30min/training_loss.png)
- [Test forecasts](Reports/residual_30min/test_forecasts.png)
- [Error versus change](Reports/residual_30min/error_vs_change.png)
- [Change distribution](Reports/residual_30min/change_distribution.png)
- [Segment MAE](Reports/residual_30min/segment_mae.png)

### Direct 60-Minute Residual Forecast

| Segment | Samples | Residual LSTM MAE | Persistence MAE |
|---|---:|---:|---:|
| All test examples | 412 | 0.354 C | 0.173 C |
| Unchanged examples | 272 | 0.281 C | 0.001 C |
| Changed examples | 140 | 0.497 C | 0.509 C |

The model improves changed-event MAE by approximately `0.012 C`, but its
`+0.288 C` overall bias causes a large regression on unchanged examples.

Charts:

- [Training loss](Reports/residual_60min/training_loss.png)
- [Test forecasts](Reports/residual_60min/test_forecasts.png)
- [Error versus change](Reports/residual_60min/error_vs_change.png)
- [Change distribution](Reports/residual_60min/change_distribution.png)
- [Segment MAE](Reports/residual_60min/segment_mae.png)

## Findings

1. **Persistence is an unusually strong baseline.**
   Most targets remain equal to the latest reading, especially at 30 minutes.

2. **Residual modeling helps on changed events.**
   Both residual experiments slightly beat persistence when temperature changes,
   confirming that the additional features contain some useful signal.

3. **Positive bias is the dominant model error.**
   The models systematically forecast warming during the colder test period.
   Bias increases with forecast horizon.

4. **Validation selection does not transfer reliably to the test period.**
   A one-epoch 60-minute smoke model reached `0.277 C` test MAE, while the
   validation-selected fully trained experiment reached `0.354 C`. Improving
   validation loss did not improve the colder test period, which confirms that
   the current single validation window is not representative enough.

5. **The dataset is too small and temporally concentrated.**
   The available data covers a limited date range and cannot represent seasonal
   or operational variation reliably.

6. **Sensor quantization affects evaluation.**
   Repeated discrete temperature values create many exact no-change targets and
   make persistence difficult to beat under aggregate MAE.

7. **Outside weather alone does not explain indoor changes.**
   Missing variables likely include occupancy, HVAC or fan state, windows,
   sunlight, room location, and device calibration.

8. **A single regression objective mixes two different problems.**
   Detecting whether temperature will change and estimating the magnitude of a
   change are distinct tasks.

## Decision

Do not deploy either residual model or export it to TinyML yet. Neither model
clearly beats persistence across the full test set.

Keep the residual experiments as the current research baseline because they
show measurable signal on changed events and produce reproducible diagnostics.

## Next Experiments

Run these in order:

1. Add a change-detection classifier:
   - Target: whether absolute future change is at least `0.1 C`.
   - Metrics: precision, recall, F1, and event-balanced accuracy.

2. Use a gated forecast:
   - Predict persistence when the classifier expects no change.
   - Use the residual regressor only when change is expected.

3. Add bias calibration:
   - Fit calibration only on validation predictions.
   - Re-check test bias without using test labels for calibration.

4. Add simple non-neural baselines:
   - Linear residual regression.
   - Gradient-boosted trees.
   - Compare model complexity against actual improvement.

5. Improve data collection:
   - Collect several months across warmer and colder conditions.
   - Record HVAC, fan, occupancy, windows, and sunlight state.
   - Validate and document sensor resolution and calibration.

6. Use rolling chronological evaluation:
   - Train and evaluate across multiple time windows.
   - Report mean performance and worst-window performance.
   - Select checkpoints using validation windows that cover different regimes.

7. Revisit deployment only when:
   - The model beats persistence on aggregate MAE and RMSE.
   - Changed-event performance improves materially.
   - Performance remains stable across multiple chronological test windows.

## Reproduction

```bash
# Direct 30-minute residual experiment
python3 -m backend.AI.train_residual_lstm \
  --forecast-horizon 3 \
  --model-output-dir backend/AI/Model/residual_30min \
  --report-output-dir backend/AI/Reports/residual_30min

# Direct 60-minute residual experiment
python3 -m backend.AI.train_residual_lstm \
  --forecast-horizon 6 \
  --model-output-dir backend/AI/Model/residual_60min \
  --report-output-dir backend/AI/Reports/residual_60min

# Cross-horizon comparison chart
python3 -m backend.AI.compare_reports \
  backend/AI/Reports/residual_30min \
  backend/AI/Reports/residual_60min \
  --output backend/AI/Reports/horizon_comparison.png
```
