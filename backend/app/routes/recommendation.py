from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.recommendation_service import (
    generate_optimization_recommendations,
)
from app.core.security import get_current_user

router = APIRouter(
    prefix="/recommendations",
    tags=["Optimization Recommendations"],
)


@router.get("/optimization")
def get_optimization_recommendations(
    forecast_type: str,
    building_id: str | None = None,
    device_id: str | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return generate_optimization_recommendations(
        db=db,
        forecast_type=forecast_type,
        building_id=building_id,
        device_id=device_id,
    )