# Backend/main.py
from fastapi import FastAPI
from backend.Database.database import create_db_and_tables
from backend.Routes.sensor_routes import router as sensor_router
from backend.Routes.predict_routes import router as predict_router
import sys, os

# Add the project root to the Python path to allow for absolute imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Create a FastAPI application instance
app = FastAPI(title="TempCastML Backend")

@app.on_event("startup")
def on_startup():
    """
    This function is called when the application starts.
    It creates the database and tables if they don't already exist.
    """
    create_db_and_tables()

# Include the sensor and predict routers
# The sensor router handles all routes related to sensor data
app.include_router(sensor_router, prefix="/sensor", tags=["Sensor"])
# The predict router handles all routes related to temperature prediction
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    """
    This is the root endpoint of the application.
    It returns a welcome message.
    """
    return {"message": "Welcome to TempCastML Backend!"}
