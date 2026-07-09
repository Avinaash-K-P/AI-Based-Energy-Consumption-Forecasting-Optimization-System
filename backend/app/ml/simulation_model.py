PEAK_START_HOUR = 18
PEAK_END_HOUR = 21

def get_adjustment_factor(scenario_type, adjustment_percent):
    adjustment = adjustment_percent / 100

    if scenario_type == "increased_occupancy":
        return 1 + adjustment

    if scenario_type in ["device_shutdown", "peak_hour_load_reduction"]:
        return 1 - adjustment

    if scenario_type == "temperature_change":
        return 1 + adjustment

    return 1


def is_peak_hour(timestamp):
    hour = timestamp.hour
    return PEAK_START_HOUR <= hour <= PEAK_END_HOUR

def apply_simulation_to_forecast(
    forecast,
    scenario_type,
    adjustment_percent,
):
    simulated_forecast = []
    adjustment_factor = get_adjustment_factor(
        scenario_type=scenario_type,
        adjustment_percent=adjustment_percent,
    )

    for item in forecast:
        baseline_usage = item["predicted_energy_usage"]
        simulated_usage = baseline_usage

        if scenario_type == "peak_hour_load_reduction":
            if is_peak_hour(item["timestamp"]):
                simulated_usage = baseline_usage * adjustment_factor

        else:
            simulated_usage = baseline_usage * adjustment_factor

        simulated_forecast.append(
            {
                "timestamp": item["timestamp"],
                "baseline_usage": round(float(baseline_usage), 2),
                "simulated_usage": round(float(simulated_usage), 2),
                "scenario_type": scenario_type,
            }
        )

    return simulated_forecast

def calculate_simulation_impact(
    simulated_forecast,
    energy_rate,
):
    baseline_total = sum(
        item["baseline_usage"] for item in simulated_forecast
    )

    simulated_total = sum(
        item["simulated_usage"] for item in simulated_forecast
    )

    energy_savings = baseline_total - simulated_total
    cost_savings = energy_savings * energy_rate

    if baseline_total == 0:
        reduction_percent = 0
    else:
        reduction_percent = (energy_savings / baseline_total) * 100

    return {
        "baseline_total_usage": round(float(baseline_total), 2),
        "simulated_total_usage": round(float(simulated_total), 2),
        "estimated_energy_savings": round(float(energy_savings), 2),
        "estimated_cost_savings": round(float(cost_savings), 2),
        "consumption_reduction_percent": round(float(reduction_percent), 2),
    }

def generate_simulation_summary(
    scenario_type,
    impact,
):
    if scenario_type == "increased_occupancy":
        return (
            "Increased occupancy is expected to raise energy consumption. "
            "Consider load balancing and HVAC schedule optimization."
        )

    if scenario_type == "temperature_change":
        return (
            "Temperature changes may affect HVAC-related consumption. "
            "Adjust cooling/heating schedules to control energy cost."
        )

    if scenario_type == "device_shutdown":
        return (
            "Device shutdown scenario shows estimated savings from turning off "
            "non-critical equipment."
        )

    if scenario_type == "peak_hour_load_reduction":
        return (
            "Peak-hour load reduction can lower demand during high-cost periods "
            "and improve operational efficiency."
        )

    return "Scenario simulation completed."

def run_scenario_simulation(
    forecast_result,
    scenario_type,
    adjustment_percent,
    energy_rate,
):
    forecast = forecast_result.get("forecast", [])

    if not forecast:
        return {
            "message": "No forecast data available for simulation.",
            "scenario_type": scenario_type,
            "simulated_forecast": [],
        }

    simulated_forecast = apply_simulation_to_forecast(
        forecast=forecast,
        scenario_type=scenario_type,
        adjustment_percent=adjustment_percent,
    )

    impact = calculate_simulation_impact(
        simulated_forecast=simulated_forecast,
        energy_rate=energy_rate,
    )

    summary = generate_simulation_summary(
        scenario_type=scenario_type,
        impact=impact,
    )

    return {
        "message": "Scenario simulation completed successfully.",
        "scenario_type": scenario_type,
        "adjustment_percent": adjustment_percent,
        "energy_rate": energy_rate,
        "impact": impact,
        "summary": summary,
        "simulated_forecast": simulated_forecast,
    }