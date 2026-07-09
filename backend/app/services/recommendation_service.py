from sqlalchemy.orm import Session
from app.models.energy_consumption import EnergyConsumption
from app.ml.forecast_model import generate_energy_forecast
from app.ml.peak_prediction_model import predict_peak_usage

def get_recommendation_records(
        db:Session,
        building_id:str|None=None,
        device_id:str|None=None,
    ):  
    
    query = db.query(EnergyConsumption)

    if building_id:
        query = query.filter(EnergyConsumption.building_id == building_id)

    if device_id:
        query = query.filter(EnergyConsumption.device_id == device_id)

    return query.order_by(EnergyConsumption.timestamp.asc()).all()


def calculate_recommendation_priority(level: str):
    priority_map = {
        "unusual_spike": "critical",
        "peak": "high",
        "high_load": "medium",
        "normal": "low",
    }

    return priority_map.get(level, "low")


def create_recommendation_from_alert(alert):
    level = alert.get("level")
    timestamp = alert.get("timestamp")
    predicted_usage = alert.get("predicted_energy_usage")

    priority = calculate_recommendation_priority(level)

    if level == "unusual_spike":
        action = "Investigate abnormal consumption and reduce non-critical loads during this period."
        recommendation_type = "spike_control"

    elif level == "peak":
        action = "Shift heavy processing tasks to off-peak hours and balance load across available devices."
        recommendation_type = "load_balancing"

    elif level == "high_load":
        action = "Delay flexible operations and monitor equipment usage during this high-load window."
        recommendation_type = "schedule_optimization"

    else:
        action = "Continue normal operation and monitor usage patterns."
        recommendation_type = "general_monitoring"

    return {
        "type": recommendation_type,
        "priority": priority,
        "timestamp": timestamp,
        "predicted_energy_usage": predicted_usage,
        "recommendation": action,
        "reason": alert.get("message"),
    }


def create_general_efficiency_recommendations(
    building_id: str | None = None,
    device_id: str | None = None,
):
    target = "the facility"

    if device_id:
        target = f"device {device_id}"

    elif building_id:
        target = f"building {building_id}"

    return [
        {
            "type": "off_peak_scheduling",
            "priority": "medium",
            "recommendation": (
                f"Schedule flexible workloads for {target} during off-peak hours "
                "to reduce demand during high-cost periods."
            ),
        },
        {
            "type": "device_shutdown",
            "priority": "medium",
            "recommendation": (
                f"Review idle equipment for {target} and shut down non-critical "
                "devices outside operating hours."
            ),
        },
        {
            "type": "hvac_optimization",
            "priority": "low",
            "recommendation": (
                f"Optimize HVAC schedules for {target} based on expected occupancy "
                "and predicted low-demand periods."
            ),
        },
    ]

def build_recommendation_context(
    records,
    forecast_result,
    peak_prediction,
    forecast_type: str,
    building_id: str | None = None,
    device_id: str | None = None,
):
    alerts = peak_prediction.get("alerts", [])
    recommendations = []

    for alert in alerts:
        recommendations.append(
            create_recommendation_from_alert(alert)
        )

    general_recommendations = create_general_efficiency_recommendations(
        building_id=building_id,
        device_id=device_id,
    )

    recommendations.extend(general_recommendations)

    return {
        "message": "Optimization recommendations generated successfully.",
        "context": {
            "forecast_type": forecast_type,
            "building_id": building_id,
            "device_id": device_id,
            "total_historical_records": len(records),
            "forecast_message": forecast_result.get("message"),
            "total_forecast_points": len(forecast_result.get("forecast", [])),
            "total_peak_alerts": peak_prediction.get("total_alerts", 0),
        },
        "thresholds": peak_prediction.get("thresholds", {}),
        "recommendations_count": len(recommendations),
        "recommendations": recommendations,
    }


def generate_optimization_recommendations(        
        db:Session,
        forecast_type: str,
        building_id: str | None = None,
        device_id: str | None = None,
):
    records = get_recommendation_records(db, building_id, device_id)

    forecast_results = generate_energy_forecast(records, forecast_type)

    peak_prediction = predict_peak_usage(records, forecast_results, building_id, device_id)

    recommendation = build_recommendation_context(records,forecast_results, peak_prediction,forecast_type,building_id,device_id)

    return recommendation