# Backend/routes/predict.py
from fastapi import APIRouter, HTTPException, Query
from sqlmodel import Session, select
from datetime import datetime, timezone, timedelta
from backend.Database.database import engine
from backend.Database.models import Reading
from backend.AI.LTSM import predict_temperature

router = APIRouter()

@router.get("/")
def forecast(device_id: int, horizon: int = Query(24, description="Hours to predict")):
    cutoff = datetime.now(timezone.utc) - timedelta(hours=72)
    with Session(engine) as session:
        readings = session.exec(
            select(Reading)
            .where(Reading.device_id == device_id, Reading.timestamp >= cutoff)
            .order_by(Reading.timestamp)
        ).all()

    if not readings:
        raise HTTPException(status_code=404, detail="No readings available for this device")

    temps = [r.temperature_c for r in readings]
    try:
        forecast_values = predict_temperature(temps, horizon)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {e}")

    return {
        "device_id": device_id,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "horizon_hours": horizon,
        "forecast": forecast_values,
    }
