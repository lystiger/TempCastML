# Backend/main.py
from fastapi import FastAPI
from backend.database.database import create_db_and_tables
from backend.routes.sensor_routes import router as sensor_router
from backend.routes.predict_routes import router as predict_router

app = FastAPI(title="TempCastML Backend")

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(sensor_router, prefix="/sensor", tags=["Sensor"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    return {"message": "Welcome to TempCastML Backend!"}
