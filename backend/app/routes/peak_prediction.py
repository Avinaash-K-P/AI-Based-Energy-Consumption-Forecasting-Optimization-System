from fastapi import APIRouter, Depends
from app.db.database import get_db
from sqlalchemy.orm import Session
from app.services.peak_prediction_service import (
    generate_peak_prediction,
    get_historical_spikes
)

router = APIRouter(prefix="/peak-prediction", tags=["Peak Predictions"])
from app.core.security import get_current_user

@router.get("/future")
def future_data(
        forecast_type:str,
        building_id:str|None=None,
        device_id:str|None=None,
        db:Session = Depends(get_db),
        user = Depends(get_current_user)
    ):
    
    result = generate_peak_prediction(db, forecast_type, building_id, device_id)

    return result

@router.get("/historical-spikes")
def historical_spikes(
        building_id:str|None=None, 
        device_id:str|None=None,
        db:Session = Depends(get_db),
        user = Depends(get_current_user) 
    ):

    result = get_historical_spikes(db, building_id, device_id)

    return result