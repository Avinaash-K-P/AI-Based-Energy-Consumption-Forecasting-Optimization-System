from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db 
from app.services.anomaly_detection_service import get_anomaly_records, detect_anomalies
from app.core.security import get_current_user

router = APIRouter(prefix="/anomalies", tags=["Anomalies Detection"])

@router.get("/detect")
def detect_consumption_anomalies(
    building_id: str | None = None,
    device_id: str | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return detect_anomalies(
        db=db,
        building_id=building_id,
        device_id=device_id,
    )