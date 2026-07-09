from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, BackgroundTasks, File, UploadFile
from app.db.database import get_db
from app.services.ml_pipeline_service import (
    import_energy_dataset,
    get_ml_pipeline_status,
    train_model_summary
)
from app.core.security import get_current_user

router = APIRouter(prefix="/ml", tags=["ML Pipeline"])

@router.post("/dataset/upload")
def upload_dataset(
    file: UploadFile = File(...),
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return import_energy_dataset(db=db, file=file)  


@router.post("/model/train")
def train_model(
    background_tasks: BackgroundTasks,
    building_id: str | None = None,
    device_id: str | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    background_tasks.add_task(
        train_model_summary,
        db,
        building_id,
        device_id,
    )

    return {
        "message": "Model training task started in background.",
        "building_id": building_id,
        "device_id": device_id,
        "status": "queued",
    }

@router.get("/model/train-summary")
def get_train_summary(
    building_id: str | None = None,
    device_id: str | None = None,
    db: Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return train_model_summary(
        db=db,
        building_id=building_id,
        device_id=device_id
    )


@router.get("/pipeline/status")
def pipeline_status(
    db:Session = Depends(get_db),
    user = Depends(get_current_user)
):
    return get_ml_pipeline_status(db)