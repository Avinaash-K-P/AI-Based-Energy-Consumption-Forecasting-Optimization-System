from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends
from app.db.database import get_db
from app.services.simulation_service import run_energy_simulation
from app.schemas.simulation import SimulationRequest
from app.core.security import get_current_user

router = APIRouter(prefix="/simulation", tags=["Simulations Scenario"])

@router.post("/run")
def create_scenario(
    payload: SimulationRequest,
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return run_energy_simulation(
        db=db,
        forecast_type=payload.forecast_type,
        scenario_type=payload.scenario_type,
        adjustment_percent=payload.adjustment_percent,
        energy_rate=payload.energy_rate,
        building_id=payload.building_id,
        device_id=payload.device_id
        )