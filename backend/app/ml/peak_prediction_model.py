import pandas as pd

from app.ml.forecast_model import generate_energy_forecast, records_to_dataframe # type: ignore


def records_to_dataframe(records):
    data = []

    for record in records:
        data.append(
            {
                "timestamp": record.timestamp,
                "building_id": record.building_id,
                "device_id": record.device_id,
                "energy_usage": record.energy_usage,
            }
        )

    df = pd.DataFrame(data)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    return df


def calculate_peak_thresholds(df):
    if df.empty:
        return {
            "average_usage": 0,
            "std_usage": 0,
            "high_load_threshold": 0,
            "peak_threshold": 0,
            "spike_threshold": 0,
        }

    average_usage = df["energy_usage"].mean()
    std_usage = df["energy_usage"].std()
    high_load_threshold = df["energy_usage"].quantile(0.75)
    peak_threshold = df["energy_usage"].quantile(0.90)

    if pd.isna(std_usage):
        std_usage = 0

    spike_threshold = average_usage + (2 * std_usage)

    return {
        "average_usage": round(float(average_usage), 2),
        "std_usage": round(float(std_usage), 2),
        "high_load_threshold": round(float(high_load_threshold), 2),
        "peak_threshold": round(float(peak_threshold), 2),
        "spike_threshold": round(float(spike_threshold), 2),
    }


def classify_peak_level(predicted_usage, thresholds):
    if predicted_usage >= thresholds["spike_threshold"]:
        return "unusual_spike"

    if predicted_usage >= thresholds["peak_threshold"]:
        return "peak"

    if predicted_usage >= thresholds["high_load_threshold"]:
        return "high_load"

    return "normal"


def generate_peak_alert_message(
    forecast_item,
    level,
    building_id=None,
    device_id=None,
):
    timestamp = forecast_item["timestamp"]
    predicted_usage = forecast_item["predicted_energy_usage"]

    target = "Energy usage"

    if device_id:
        target = f"Device {device_id}"

    elif building_id:
        target = f"Building {building_id}"

    if level == "unusual_spike":
        return (
            f"{target} may exceed normal energy threshold at {timestamp}. "
            f"Predicted usage: {predicted_usage} kWh."
        )

    if level == "peak":
        return (
            f"Expected peak consumption for {target} at {timestamp}. "
            f"Predicted usage: {predicted_usage} kWh."
        )

    if level == "high_load":
        return (
            f"High-load period expected for {target} at {timestamp}. "
            f"Predicted usage: {predicted_usage} kWh."
        )

    return None

def detect_historical_spikes(records):
    df = records_to_dataframe(records)

    if df.empty:
        return {
            "message": "No historical data available for spike detection.",
            "spikes": [],
        }

    thresholds = calculate_peak_thresholds(df)
    spikes = []

    for _, row in df.iterrows():
        level = classify_peak_level(
            predicted_usage=row["energy_usage"],
            thresholds=thresholds,
        )

        if level in ["peak", "unusual_spike"]:
            spikes.append(
                {
                    "timestamp": row["timestamp"],
                    "building_id": row["building_id"],
                    "device_id": row["device_id"],
                    "energy_usage": round(float(row["energy_usage"]), 2),
                    "level": level,
                }
            )

    return {
        "message": "Historical spike detection completed.",
        "thresholds": thresholds,
        "total_spikes": len(spikes),
        "spikes": spikes,
    }


def predict_peak_usage(records, forecast_result, building_id=None, device_id=None):
    df = records_to_dataframe(records)

    if df.empty:
        return {
            "message": "No historical data available for peak prediction.",
            "alerts": [],
            "peak_periods": [],
        }

    forecast = forecast_result.get("forecast", [])

    if not forecast:
        return {
            "message": "No forecast data available for peak prediction.",
            "alerts": [],
            "peak_periods": [],
        }

    thresholds = calculate_peak_thresholds(df)
    alerts = []
    peak_periods = []

    for item in forecast:
        predicted_usage = item["predicted_energy_usage"]

        level = classify_peak_level(
            predicted_usage=predicted_usage,
            thresholds=thresholds,
        )

        if level != "normal":
            alert_message = generate_peak_alert_message(
                forecast_item=item,
                level=level,
                building_id=building_id,
                device_id=device_id,
            )

            alerts.append(
                {
                    "timestamp": item["timestamp"],
                    "level": level,
                    "predicted_energy_usage": predicted_usage,
                    "message": alert_message,
                }
            )

            peak_periods.append(
                {
                    "timestamp": item["timestamp"],
                    "predicted_energy_usage": predicted_usage,
                    "level": level,
                }
            )

    return {
        "message": "Peak usage prediction completed.",
        "thresholds": thresholds,
        "total_alerts": len(alerts),
        "alerts": alerts,
        "peak_periods": peak_periods,
    }