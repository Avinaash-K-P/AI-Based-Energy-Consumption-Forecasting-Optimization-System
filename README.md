# AI-Based Energy Consumption Forecasting & Optimization System

## Overview

The **AI-Based Energy Consumption Forecasting & Optimization System** is a full-stack web application that leverages Artificial Intelligence and Machine Learning to analyze historical energy consumption data, predict future energy usage, detect anomalies, identify peak demand periods, and generate optimization recommendations to improve energy efficiency.

The application enables users to upload energy datasets, visualize analytics through interactive dashboards, and simulate different energy consumption scenarios for decision-making

# Tech Stack

## Backend

* FastAPI
* SQLAlchemy
* SQLite
* Pydantic
* JWT Authentication
* Uvicorn

## Frontend

* React
* Bootstrap
* Axios
* React Router DOM
* Jwt Decode
* React Toastify
* Recharts
* React Icons

## Machine Learning

* Pandas
* NumPy
* Random Forest Regressor
* Scikit-learn

## Database (SQLite)

* User - (id, username, email, password)
* Energy Consumption - (id, timestamp, building_id, device_id, energy_usage, temperatire, humidity)

### User Table

| Column   | Description            |
| -------- | ---------------------- |
| id       | Primary Key            |
| username | Unique username        |
| email    | Unique email address   |
| password | Bcrypt hashed password |

### Energy Consumption Table

| Column       | Description                     |
| ------------ | ------------------------------- |
| id           | Primary Key                     |
| timestamp    | Date and time of energy reading |
| building_id  | Building identifier             |
| device_id    | Device identifier               |
| energy_usage | Energy consumption (kWh)        |
| temperature  | Ambient temperature (°C)       |
| humidity     | Relative humidity (%)           |

# Dataset Explanation

The application uses a synthetic energy consumption dataset consist of 6053 rows generated to simulate real-world commercial building energy usage.

| Column       | Description                  |
| ------------ | ---------------------------- |
| timestamp    | Date and time of the reading |
| building_id  | Building identifier          |
| device_id    | Device identifier            |
| energy_usage | Energy consumption (kWh)     |
| temperature  | Ambient temperature (°C)    |
| humidity     | Relative humidity (%)        |

# Forecasting Methodology

The forecasting engine predicts future energy consumption using historical energy data.

### Steps

1. Dataset preprocessing
2. Missing value handling
3. Feature engineering
4. Time-series preparation
5. Model training
6. Forecast generation

### Forecast Windows

* Next 24 Hours
* Next 7 Days
* Next 30 Days

## Optimization Strategy

The system analyzes historical and predicted energy consumption patterns to generate intelligent recommendations for improving energy efficiency and reducing operational costs.

### Optimization Objectives

- Reduce unnecessary energy consumption
- Balance energy load during peak hours
- Improve device utilization
- Minimize operational costs
- Encourage energy-efficient scheduling

### Recommendation Strategy

The optimization engine evaluates forecasted energy usage and applies rule-based logic to generate actionable recommendations, including:

- Shift high-energy operations to off-peak hours.
- Reduce HVAC usage during periods of low occupancy.
- Schedule maintenance for devices with abnormal energy consumption.
- Turn off idle equipment to reduce energy waste.
- Optimize operational schedules based on forecasted demand.
- Recommend load balancing across buildings and devices.

These recommendations help users make informed decisions to improve overall energy efficiency while maintaining operational performance.


## Anomaly Detection Approach

The system identifies abnormal energy consumption patterns that may indicate equipment faults, inefficient operations, or unexpected energy usage.

### Detected Anomalies

- Sudden energy consumption spikes
- Unexpected night-time energy usage
- Device behavior outside normal operating ranges
- Abnormal HVAC energy consumption
- Irregular sensor readings

### Detection Methodology

The anomaly detection process consists of the following steps:

1. Data preprocessing and cleaning.
2. Feature selection using energy consumption and environmental data.
3. Statistical analysis of historical energy usage.
4. Machine Learning-based anomaly detection using Isolation Forest.
5. Identification and visualization of anomalous records.

### Output

The system highlights anomalous energy records within the analytics dashboard and enables users to:

- Identify abnormal devices.
- Detect unexpected consumption behavior.
- Investigate potential equipment failures.
- Improve operational efficiency through early detection.

This proactive approach helps organizations reduce energy waste, improve system reliability, and support preventive maintenance.

## System Architecture


```
                           User
                             │
                             ▼
                 React + Bootstrap Frontend
                             │
                    Axios HTTP Requests
                             │
                             ▼
                    FastAPI REST API
                             │
      ┌──────────────┬──────────────┬──────────────┐
      │              │              │              │
      ▼              ▼              ▼              ▼
 Authentication   Energy Module   ML Engine   Analytics Engine
      │              │              │              │
      └──────────────┴──────────────┴──────────────┘
                             │
                  SQLAlchemy ORM + Services
                             │
                ┌────────────┴────────────┐
                ▼                         ▼
          SQLite Database          Machine Learning
          • Users                  • Random Forest Regressor
          • Energy Data            • Scikit-learn
                                   • Recommendation Engine
```

## API Documentation (Total: 16 API's)

### 1. Auth

- POST: auth/register
- POST: auth/login

### 2. Energy Consumtion

- POST: energy-consumption/
- GET: energy-consumption/list
- GET: energy-consumption/filter
- GET: energy-consumption/forecast
- DELETE: energy-consumption/{energy_id}

### Peak Prediction

- GET: peak-prediction/future
- GET: peak-prediction/historical-spikes

### Optimization Recommondation

- GET: recommendation/optimization

### Anomalies Detection

- GET:  anomalies/detect

### Simulation Scenario

- POST: simulation/run

### ML Pipeline

- POST: ml/dataset/upload
- POST: ml/model/train
- GET: ml/model/train-summary
- GET: ml/pipeline/status

# Features

* User Authentication (JWT)
* Dataset Upload (CSV)
* Historical Energy Analytics
* AI-Based Energy Consumption Forecasting
* Peak Usage Prediction
* Energy Consumption Anomaly Detection
* AI Optimization Recommendations
* Scenario Simulation
* Interactive Dashboard
* Responsive React Dashboard

## Conclusion

This project demonstrates the development of a full-stack AI-powered Energy Consumption Forecasting & Optimization System using FastAPI, React, Machine Learning, and interactive data visualization. It provides intelligent forecasting, anomaly detection, peak usage prediction, optimization recommendations, and scenario simulation to support data-driven energy management.

## Developed By

**Avinaash K P**

Python Developer

