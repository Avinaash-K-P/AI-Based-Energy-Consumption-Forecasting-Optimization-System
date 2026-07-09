from sqlalchemy.orm import Session
from app.ml.forecast_model import generate_energy_forecast
from app.ml.simulation_model import run_scenario_simulation
from app.models.energy_consumption import EnergyConsumption

def get_simulation_records(
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

def run_energy_simulation(
    db: Session,
    forecast_type: str,
    scenario_type: str,
    adjustment_percent: float,
    energy_rate: float,
    building_id: str | None = None,
    device_id: str | None = None,
):
    records = get_simulation_records(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )

    forecast_result = generate_energy_forecast(
        records=records,
        forecast_type=forecast_type,
    )

    return run_scenario_simulation(
        forecast_result=forecast_result,
        scenario_type=scenario_type,
        adjustment_percent=adjustment_percent,
        energy_rate=energy_rate,
    )