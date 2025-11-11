# Backend/main.py
from fastapi import FastAPI
from backend.Database.database import create_db_and_tables
from backend.Routes.sensor_routes import router as sensor_router
from backend.Routes.predict_routes import router as predict_router
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

app = FastAPI(title="TempCastML Backend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(sensor_router, prefix="/sensor", tags=["Sensor"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    return {"message": "Welcome to TempCastML Backend!"}
