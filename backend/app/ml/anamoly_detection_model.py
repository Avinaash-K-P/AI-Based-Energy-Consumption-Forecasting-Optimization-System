import pandas as pd
from sklearn.ensemble import IsolationForest

MIN_RECORDS_FOR_ISOLATION_FOREST = 20
NIGHT_START_HOUR = 22
NIGHT_END_HOUR = 6


def records_to_dataframe(records):
    data = []

    for record in records:
        data.append(
            {
                "timestamp": record.timestamp,
                "building_id": record.building_id,
                "device_id": record.device_id,
                "energy_usage": record.energy_usage,
                "temperature": record.temperature,
                "humidity": record.humidity,
            }
        )

    df = pd.DataFrame(data)

    if df.empty:
        return df

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    return df


def add_anomaly_features(df):
    df = df.copy()

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["is_night"] = (
        (df["hour"] >= NIGHT_START_HOUR) | (df["hour"] < NIGHT_END_HOUR)
    ).astype(int)

    df["temperature"] = df["temperature"].fillna(df["temperature"].mean())
    df["humidity"] = df["humidity"].fillna(df["humidity"].mean())

    df["temperature"] = df["temperature"].fillna(0)
    df["humidity"] = df["humidity"].fillna(0)

    return df

def calculate_anomaly_thresholds(df):
    if df.empty:
        return {
            "average_usage": 0,
            "std_usage": 0,
            "spike_threshold": 0,
            "night_usage_threshold": 0,
        }

    average_usage = df["energy_usage"].mean()
    std_usage = df["energy_usage"].std()

    if pd.isna(std_usage):
        std_usage = 0

    spike_threshold = average_usage + (2 * std_usage)
    night_usage_threshold = df["energy_usage"].quantile(0.75)

    return {
        "average_usage": round(float(average_usage), 2),
        "std_usage": round(float(std_usage), 2),
        "spike_threshold": round(float(spike_threshold), 2),
        "night_usage_threshold": round(float(night_usage_threshold), 2),
    }

def get_anomaly_severity(energy_usage, thresholds):
    if energy_usage >= thresholds["spike_threshold"]:
        return "high"

    if energy_usage >= thresholds["night_usage_threshold"]:
        return "medium"

    return "low"

def detect_rule_based_anomalies(df, thresholds):
    anomalies = []

    for _, row in df.iterrows():
        anomaly_types = []

        if row["energy_usage"] < 0:
            anomaly_types.append("sensor_negative_usage")

        if row["energy_usage"] >= thresholds["spike_threshold"]:
            anomaly_types.append("sudden_energy_spike")

        if (
            row["is_night"] == 1
            and row["energy_usage"] >= thresholds["night_usage_threshold"]
        ):
            anomaly_types.append("unexpected_night_usage")

        for anomaly_type in anomaly_types:
            anomalies.append(
                {
                    "timestamp": row["timestamp"],
                    "building_id": row["building_id"],
                    "device_id": row["device_id"],
                    "energy_usage": round(float(row["energy_usage"]), 2),
                    "anomaly_type": anomaly_type,
                    "severity": get_anomaly_severity(
                        row["energy_usage"],
                        thresholds,
                    ),
                    "source": "rule_based",
                    "message": create_anomaly_message(anomaly_type), # type: ignore
                }
            )

    return anomalies

def detect_isolation_forest_anomalies(df):
    if len(df) < MIN_RECORDS_FOR_ISOLATION_FOREST:
        return []

    feature_columns = [
        "energy_usage",
        "temperature",
        "humidity",
        "hour",
        "day_of_week",
        "is_night",
    ]

    model = IsolationForest(
        contamination=0.1,
        random_state=42,
    )

    predictions = model.fit_predict(df[feature_columns])

    anomalies = []

    for index, prediction in enumerate(predictions):
        if prediction == -1:
            row = df.iloc[index]

            anomalies.append(
                {
                    "timestamp": row["timestamp"],
                    "building_id": row["building_id"],
                    "device_id": row["device_id"],
                    "energy_usage": round(float(row["energy_usage"]), 2),
                    "anomaly_type": "ml_detected_anomaly",
                    "severity": "medium",
                    "source": "isolation_forest",
                    "message": "Machine learning model detected an unusual consumption pattern.",
                }
            )

    return anomalies

def create_anomaly_message(anomaly_type):
    messages = {
        "sensor_negative_usage": "Sensor reported negative energy usage, which may indicate faulty sensor behavior.",
        "sudden_energy_spike": "Sudden energy spike detected compared with normal historical usage.",
        "unexpected_night_usage": "High energy usage detected during night-time hours.",
        "ml_detected_anomaly": "Machine learning model detected an unusual consumption pattern.",
    }

    return messages.get(
        anomaly_type,
        "Abnormal energy consumption pattern detected.",
    )


def merge_anomalies(rule_anomalies, ml_anomalies):
    merged = {}
    combined = rule_anomalies + ml_anomalies

    for anomaly in combined:
        key = (
            str(anomaly["timestamp"]),
            anomaly["building_id"],
            anomaly["device_id"],
            anomaly["anomaly_type"],
        )

        merged[key] = anomaly

    return list(merged.values())

def detect_consumption_anomalies(records):
    df = records_to_dataframe(records)

    if df.empty:
        return {
            "message": "No historical data available for anomaly detection.",
            "thresholds": {},
            "total_anomalies": 0,
            "anomalies": [],
        }

    df = add_anomaly_features(df)
    thresholds = calculate_anomaly_thresholds(df)

    rule_anomalies = detect_rule_based_anomalies(
        df=df,
        thresholds=thresholds,
    )

    ml_anomalies = detect_isolation_forest_anomalies(df)

    anomalies = merge_anomalies(
        rule_anomalies=rule_anomalies,
        ml_anomalies=ml_anomalies,
    )

    return {
        "message": "Consumption anomaly detection completed.",
        "method": "IsolationForest + rule_based_detection",
        "thresholds": thresholds,
        "total_anomalies": len(anomalies),
        "anomalies": anomalies,
    }