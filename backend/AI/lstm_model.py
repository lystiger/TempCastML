from typing import Any

from backend.AI.training_config import TrainingConfig


def configure_tensorflow(seed: int) -> Any:
    import tensorflow as tf

    tf.keras.utils.set_random_seed(seed)
    try:
        tf.config.experimental.enable_op_determinism()
    except Exception:
        pass
    return tf


def build_lstm_model(config: TrainingConfig):
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
        name="tempcast_lstm",
    )
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=config.learning_rate),
        loss="mse",
        metrics=["mae"],
    )
    return model
