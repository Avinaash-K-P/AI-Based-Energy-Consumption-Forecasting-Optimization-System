from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import (
    auth,
    energy_consumption,
    peak_prediction,
    recommendation,
    anamoly_detection,
    scenario_simulation,
    ml_pipeline
)

app = FastAPI(
    title="AI Energy Consumption Forecasting",
    
    description=
    """ 
    Features added:
    - Authentication using JWT
    - Energy Consumption tracking models
    - AI/ML model: Random Forest Regressor 
    - Predicted Peak Values
    - Historical vs predicted energy usage
    - Peak consumption visualization
    - Anomaly highlights
    - Device-wise analytics   
    - Optimization recommendations
    - Forecast accuracy metrics
    """,
    
    version="1.0.0"
    )

#CORS Confurigation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)    

#routes
app.include_router(auth.router)
app.include_router(energy_consumption.router)
app.include_router(peak_prediction.router)
app.include_router(recommendation.router)
app.include_router(anamoly_detection.router)
app.include_router(scenario_simulation.router)
app.include_router(ml_pipeline.router)

@app.get("/")
def get_root():
    return {"message":"API connected successfully!"}