from sqlalchemy.orm import Session
from app.models.energy_consumption import EnergyConsumption
from app.ml.forecast_model import generate_energy_forecast
from app.ml.peak_prediction_model import predict_peak_usage, detect_historical_spikes

def get_peak_prediction_records(
    db: Session,
    building_id: str | None = None,
    device_id: str | None = None,
):
    query = db.query(EnergyConsumption)

    if building_id:
        query = query.filter(EnergyConsumption.building_id == building_id)

    if device_id:
        query = query.filter(EnergyConsumption.device_id == device_id)

    return query.order_by(EnergyConsumption.timestamp.asc()).all()

def generate_peak_prediction(
    db: Session,
    forecast_type: str,
    building_id: str | None = None,
    device_id: str | None = None,
):
    records = get_peak_prediction_records(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )

    forecast = generate_energy_forecast(
        records=records,
        forecast_type=forecast_type,
    )

    return predict_peak_usage(
        records=records,
        forecast_result=forecast,
        building_id=building_id,
        device_id=device_id,
    )

def get_historical_spikes(
        db:Session, 
        building_id:str|None=None, 
        device_id:str|None=None):
    
    if building_id:
        records = db.query(EnergyConsumption).filter(
            EnergyConsumption.building_id==building_id
        ).all()

    elif device_id:
        records = db.query(EnergyConsumption).filter(
            EnergyConsumption.device_id==device_id
        ).all()    

    historical_spikes = detect_historical_spikes(records)

    return historical_spikes