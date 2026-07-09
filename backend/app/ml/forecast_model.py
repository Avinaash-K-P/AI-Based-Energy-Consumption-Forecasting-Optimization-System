from datetime import timedelta
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

MIN_RECORDS_FOR_ML = 20

def records_to_dataframe(records):

    data = []

    for record in records:
        data.append(
            {
            "timestamp": record.timestamp,
            "energy_usage": record.energy_usage,
            "temperature": record.temperature,
            "humidity": record.humidity
        }
    )
        
    df = pd.DataFrame(data)

    if df.empty:
        return df
    
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values("timestamp")

    return df

def add_time_features(df):
    df = df.copy()

    df["hour"] = df["timestamp"].dt.hour
    df["day_of_week"] = df["timestamp"].dt.dayofweek
    df["day_of_month"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    df["temperature"] = df["temperature"].fillna(df["temperature"].mean())
    df["humidity"] = df["humidity"].fillna(df["humidity"].mean())

    df["temperature"] = df["temperature"].fillna(0)
    df["humidity"] = df["humidity"].fillna(0)

    return df

def baseline_forecast(df, periods, frequency):
    predictions = []

    last_timestamp = df["timestamp"].max()
    average_usage = df["energy_usage"].mean()

    for step in range(1, periods + 1):
        future_timestamp = last_timestamp + step * frequency

        predictions.append(
            {
                "timestamp": future_timestamp,
                "predicted_energy_usage": round(float(average_usage), 2),
                "model_used": "baseline_average",
            }
        )

    return predictions

def train_random_forest_forecast(df, periods, frequency):
    
    df = add_time_features(df)

    feature_columns = [
        "hour",
        "day_of_week",
        "day_of_month",
        "month",
        "is_weekend",
        "temperature",
        "humidity",
    ]

    x = df[feature_columns]
    y = df["energy_usage"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42,
    )

    model.fit(x, y)

    last_timestamp = df["timestamp"].max()
    future_rows = []

    last_temperature = df["temperature"].iloc[-1]
    last_humidity = df["humidity"].iloc[-1]

    for step in range(1, periods + 1):
        future_timestamp = last_timestamp + step * frequency

        future_rows.append(
            {
                "timestamp": future_timestamp,
                "temperature": last_temperature,
                "humidity": last_humidity,
            }
        )

    future_df = pd.DataFrame(future_rows)
    future_df = add_time_features(future_df)

    predictions = model.predict(future_df[feature_columns])

    forecast = []

    for timestamp, prediction in zip(future_df["timestamp"], predictions):
        forecast.append(
            {
                "timestamp": timestamp,
                "predicted_energy_usage": round(float(prediction), 2),
                "model_used": "random_forest",
            }
        )

    return forecast

def generate_energy_forecast(records, forecast_type):
    df = records_to_dataframe(records)

    if df.empty:
        return {
            "message": "No historical data available for forecasting.",
            "forecast": [],
        }

    forecast_settings = {
        "next_24_hours": {
            "periods": 24,
            "frequency": timedelta(hours=1),
        },
        "next_7_days": {
            "periods": 7,
            "frequency": timedelta(days=1),
        },
        "next_30_days": {
            "periods": 30,
            "frequency": timedelta(days=1),
        },
    }

    if forecast_type not in forecast_settings:
        return {
            "message": "Invalid forecast type.",
            "forecast": [],
        }

    periods = forecast_settings[forecast_type]["periods"]
    frequency = forecast_settings[forecast_type]["frequency"]

    if len(df) < MIN_RECORDS_FOR_ML:
        forecast = baseline_forecast(df, periods, frequency)
    else:
        forecast = train_random_forest_forecast(df, periods, frequency)

    return {
        "message": "Forecast generated successfully.",
        "forecast_type": forecast_type,
        "total_historical_records": len(df),
        "forecast": forecast,
    }