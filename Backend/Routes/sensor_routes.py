from fastapi import APIRouter, HTTPException
from sqlmodel import Session
from backend.Database.database import engine
from backend.Database.models import Reading
from pydantic import BaseModel

# Create a new router for the sensor data
router = APIRouter()

class SensorData(BaseModel):
    """
    This is the Pydantic model for the sensor data.
    It defines the expected data types for the device_id and temperature_c fields.
    """
    device_id: int
    temperature_c: float

@router.post("/")
def receive_data(data: SensorData):
    """
    This endpoint receives sensor data via a POST request.
    The data is validated against the SensorData model.
    If the data is valid, it is saved to the database.
    """
    with Session(engine) as session:
        # Create a new Reading object from the received data
        db_reading = Reading.from_orm(data)
        # Add the new reading to the session
        session.add(db_reading)
        # Commit the session to save the reading to the database
        session.commit()
        # Refresh the session to get the updated reading from the database
        session.refresh(db_reading)
    # Return the newly created reading
    return db_reading