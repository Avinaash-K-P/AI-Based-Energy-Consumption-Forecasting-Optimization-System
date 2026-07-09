from sqlalchemy.orm import Session
from app.ml.anamoly_detection_model import detect_consumption_anomalies
from app.models.energy_consumption import EnergyConsumption

def get_anomaly_records(
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

def detect_anomalies(
    db: Session,
    building_id: str | None = None,
    device_id: str | None = None,
):
    records = get_anomaly_records(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )

    return detect_consumption_anomalies(records)