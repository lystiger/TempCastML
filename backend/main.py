# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Use relative imports within the 'backend' package
from .Database.database import create_db_and_tables
from .Routes.sensor_routes import router as sensor_router
from .Routes.predict_routes import router as predict_router

# Create a FastAPI application instance
app = FastAPI(title="TempCastML Backend")

# Add CORS middleware
origins = [
    "http://localhost",
    "http://localhost:5173",  # Allow requests from the frontend development server
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    """
    This function is called when the application starts.
    It creates the database and tables if they don't already exist.
    """
    create_db_and_tables()

# Include the sensor and predict routers
app.include_router(sensor_router, prefix="/sensor", tags=["Sensor"])
app.include_router(predict_router, prefix="/predict", tags=["Prediction"])

@app.get("/")
def root():
    """
    This is the root endpoint of the application.
    It returns a welcome message.
    """
    return {"message": "Welcome to TempCastML Backend!"}
