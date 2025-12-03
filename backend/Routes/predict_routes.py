from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone, timedelta
from ..Database.database import engine
from ..Database.models import Reading
from ..AI.LTSM import predict_temperature

# Create a new router for the prediction
router = APIRouter()

@router.get("/")
def forecast(device_id: int, horizon: int = Query(24, description="Hours to predict")):
    """
    This endpoint generates a temperature forecast for a given device.
    It takes a device_id and an optional horizon in hours as input.
    It returns a list of predicted temperatures for the given horizon.
    """
    # Calculate the cutoff time for the data to be used for prediction
    cutoff = datetime.now(timezone.utc) - timedelta(hours=72)
    with Session(engine) as session:
        # Query the database for readings for the given device within the cutoff time
        readings = session.exec(
            select(Reading)
            .where(Reading.device_id == device_id, Reading.timestamp >= cutoff)
            .order_by(Reading.timestamp)
        ).all()

    # If there are no readings, raise an HTTPException
    if not readings:
        raise HTTPException(status_code=404, detail="No readings available for this device")

    # Extract the temperatures from the readings
    temps = [r.temperature_c for r in readings]
    try:
        # Generate the forecast using the LSTM model
        forecast_values = predict_temperature(temps, horizon)
    except Exception as e:
        # If there is an error during prediction, raise an HTTPException
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    # Return the forecast
    return {
        "device_id": device_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "horizon_hours": horizon,
        "forecast": forecast_values,
    }