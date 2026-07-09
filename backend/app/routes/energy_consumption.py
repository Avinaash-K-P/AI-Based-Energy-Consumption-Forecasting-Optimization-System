from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.energy_consumption import (
    CreateEnergyConsumption,
    EnergyConsumptionResponse
)
from app.services.energy_consumption_service import (
    create_energy_consumption,
    get_all_energy_consumption,
    get_energy_consumption_by_filter,
    generate_forecast,
    delete_energy_consumption
)
from typing import List, Optional
from app.core.security import get_current_user

router = APIRouter(prefix="/energy-consumption", tags=["Energy Consumption"])

@router.post("/")
def add_energy_consumption(
    payload: CreateEnergyConsumption,
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):

    data = create_energy_consumption(db,payload)

    return data

@router.get("/list")
def list_energy_consumption(
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):
    data = get_all_energy_consumption(db)

    return data


@router.get("/filter", response_model=list[EnergyConsumptionResponse])
def filter_energy_consumption(
    building_id: Optional[str] = None,
    device_id: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_energy_consumption_by_filter(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )

@router.get("/forecast")
def forecast_energy_consumption(
    forecast_type: str,
    building_id: Optional[str] = None,
    device_id: Optional[str] = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return generate_forecast(
        db=db,
        forecast_type=forecast_type,
        building_id=building_id,
        device_id=device_id,
    )

@router.delete("/{energy_id}")
def remove_energy_consumption(
    energy_id: int,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    deleted_record = delete_energy_consumption(db, energy_id)

    if not deleted_record:
        raise HTTPException(
            status_code=404,
            detail="Energy consumption record not found",
        )

    return {
        "message": "Energy consumption record deleted successfully",
        "deleted_id": energy_id,
    }