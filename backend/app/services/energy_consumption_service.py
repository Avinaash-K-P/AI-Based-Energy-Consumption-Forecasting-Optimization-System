from sqlalchemy.orm import Session
from app.models.energy_consumption import EnergyConsumption
from app.ml.forecast_model import generate_energy_forecast
from app.schemas.energy_consumption import CreateEnergyConsumption

def create_energy_consumption(db:Session, payload: CreateEnergyConsumption):

    new_energy_consumption = EnergyConsumption(
        timestamp = payload.timestamp,
        building_id = payload.building_id,
        device_id = payload.device_id,
        energy_usage = payload.energy_usage,
        temperature = payload.temperature,
        humidity = payload.humidity
    )

    db.add(new_energy_consumption)
    db.commit()
    db.refresh(new_energy_consumption)

    return new_energy_consumption

def get_all_energy_consumption(db:Session):

    result = db.query(EnergyConsumption).all()

    return result

def get_energy_consumption_by_filter(
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
    
def generate_forecast(
    db: Session,
    forecast_type: str,
    building_id: str | None = None,
    device_id: str | None = None,
):
    records = get_energy_consumption_by_filter(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )

    return generate_energy_forecast(
        records=records,
        forecast_type=forecast_type,
    )

def delete_energy_consumption(
    db: Session,
    energy_id: int,
):
    energy_record = db.query(EnergyConsumption).filter(
        EnergyConsumption.id == energy_id
    ).first()

    if not energy_record:
        return None

    db.delete(energy_record)
    db.commit()

    return energy_record