from datetime import datetime

import pandas as pd
from sqlalchemy.orm import Session

from app.models.energy_consumption import EnergyConsumption

REQUIRED_DATASET_COLUMNS = {
    "timestamp",
    "building_id",
    "device_id",
    "energy_usage",
}

def validate_dataset_columns(df):
    missing_columns = REQUIRED_DATASET_COLUMNS - set(df.columns)

    if missing_columns:
        return {
            "is_valid": False,
            "missing_columns": list(missing_columns),
        }

    return {
        "is_valid": True,
        "missing_columns": [],
    }

def parse_optional_float(value):
    if pd.isna(value) or value == "":
        return None

    return float(value)

def import_energy_dataset(db: Session, file):
    df = pd.read_csv(file.file)

    validation = validate_dataset_columns(df)

    if not validation["is_valid"]:
        return {
            "message": "Dataset upload failed. Missing required columns.",
            "missing_columns": validation["missing_columns"],
            "inserted_rows": 0,
            "skipped_rows": len(df),
        }
    

    inserted_rows = 0
    skipped_rows = 0
    batch_size = 500

    try:

        for _, row in df.iterrows():
            try:
                energy_record = EnergyConsumption(
                    timestamp=pd.to_datetime(row["timestamp"], dayfirst=True),
                    building_id=str(row["building_id"]),
                    device_id=str(row["device_id"]),
                    energy_usage=float(row["energy_usage"]),
                    temperature=parse_optional_float(row.get("temperature")),
                    humidity=parse_optional_float(row.get("humidity")),
                    created_at=datetime.utcnow(),
                )

                db.add(energy_record)
                inserted_rows += 1

            except Exception:
                skipped_rows += 1

        db.commit()

    except Exception as error:
        
        db.rollback()
        return {
            "message": "Dataset upload failed during database insert.",
            "error": str(error),
            "total_rows": len(df),
            "inserted_rows": inserted_rows,
            "skipped_rows": skipped_rows,
        }

    return {
        "message": "Dataset imported successfully.",
        "total_rows": len(df),
        "inserted_rows": inserted_rows,
        "skipped_rows": skipped_rows,
    }

def get_ml_pipeline_status(db: Session):
    total_records = db.query(EnergyConsumption).count()

    buildings = db.query(EnergyConsumption.building_id).distinct().count()
    devices = db.query(EnergyConsumption.device_id).distinct().count()

    return {
        "message": "ML pipeline status fetched successfully.",
        "total_energy_records": total_records,
        "total_buildings": buildings,
        "total_devices": devices,
        "modules": {
            "forecasting": "available",
            "peak_prediction": "available",
            "optimization_recommendations": "available",
            "anomaly_detection": "available",
            "scenario_simulation": "available",
            "dataset_upload": "available",
        },
    }

def train_model_summary(
    db: Session,
    building_id: str | None = None,
    device_id: str | None = None,
):
    query = db.query(EnergyConsumption)

    if building_id:
        query = query.filter(EnergyConsumption.building_id == building_id)

    if device_id:
        query = query.filter(EnergyConsumption.device_id == device_id)

    records = query.all()
    total_records = len(records)

    if total_records < 20:
        return {
            "message": "Not enough data for ML training. Baseline forecasting will be used.",
            "total_records": total_records,
            "model_status": "fallback_baseline",
            "minimum_required_records": 20,
        }

    return {
        "message": "Dataset is ready for ML forecasting.",
        "total_records": total_records,
        "model_status": "ready_for_random_forest_training",
        "model_type": "RandomForestRegressor",
        "training_mode": "on_demand_during_forecast_generation",
    }    