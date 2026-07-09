import { useState } from "react";
import {
  CartesianGrid,
  Legend,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { runSimulation } from "../../services/simulationService";
import "/src/styles/simulation.css";

const ScenarioSimulation = () => {
  const [formData, setFormData] = useState({
    forecast_type: "next_24_hours",
    scenario_type: "device_shutdown",
    adjustment_percent: 15,
    energy_rate: 8.5,
    building_id: "B001",
    device_id: "",
  });

  const [simulationData, setSimulationData] = useState(null);
  const [loading, setLoading] = useState(false);

  const formatLabel = (timestamp) => {
    return new Date(timestamp).toLocaleString([], {
      month: "short",
      day: "2-digit",
      hour: "2-digit",
    });
  };

  const handleChange = (event) => {
    const { name, value } = event.target;

    setFormData((current) => ({
      ...current,
      [name]:
        name === "adjustment_percent" || name === "energy_rate"
          ? Number(value)
          : value,
    }));
  };

  const buildChartData = (items = []) => {
    return items.map((item) => ({
      label: formatLabel(item.timestamp),
      baseline_usage: item.baseline_usage,
      simulated_usage: item.simulated_usage,
    }));
  };

  const handleRunSimulation = async () => {
    try {
      setLoading(true);

      const payload = {
        ...formData,
        device_id: formData.device_id || null,
      };

      const result = await runSimulation(payload);
      setSimulationData(result);
    } catch (error) {
      console.error("Simulation error:", error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = buildChartData(simulationData?.simulated_forecast || []);
  const impact = simulationData?.impact;

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Scenario Simulation</h1>
        <p>Estimate savings and cost impact for operational changes</p>
      </div>

      <div className="filter-panel simulation-filter-panel">
        <div className="form-control">
          <label>Building ID</label>
          <input
            name="building_id"
            value={formData.building_id}
            onChange={handleChange}
            placeholder="B001"
          />
        </div>

        <div className="form-control">
          <label>Device ID</label>
          <input
            name="device_id"
            value={formData.device_id}
            onChange={handleChange}
            placeholder="Optional"
          />
        </div>

        <div className="form-control">
          <label>Forecast Type</label>
          <select
            name="forecast_type"
            value={formData.forecast_type}
            onChange={handleChange}
          >
            <option value="next_24_hours">Next 24 Hours</option>
            <option value="next_7_days">Next 7 Days</option>
            <option value="next_30_days">Next 30 Days</option>
          </select>
        </div>

        <div className="form-control">
          <label>Scenario</label>
          <select
            name="scenario_type"
            value={formData.scenario_type}
            onChange={handleChange}
          >
            <option value="increased_occupancy">Increased Occupancy</option>
            <option value="temperature_change">Temperature Change</option>
            <option value="device_shutdown">Device Shutdown</option>
            <option value="peak_hour_load_reduction">
              Peak-Hour Load Reduction
            </option>
          </select>
        </div>

        <div className="form-control">
          <label>Adjustment %</label>
          <input
            type="number"
            name="adjustment_percent"
            value={formData.adjustment_percent}
            onChange={handleChange}
          />
        </div>

        <div className="form-control">
          <label>Energy Rate</label>
          <input
            type="number"
            name="energy_rate"
            value={formData.energy_rate}
            onChange={handleChange}
          />
        </div>

        <button onClick={handleRunSimulation} disabled={loading}>
          {loading ? "Running..." : "Run Simulation"}
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Baseline Usage</span>
          <strong>{impact?.baseline_total_usage ?? "N/A"}</strong>
        </div>

        <div className="kpi-card">
          <span>Simulated Usage</span>
          <strong>{impact?.simulated_total_usage ?? "N/A"}</strong>
        </div>

        <div className="kpi-card">
          <span>Energy Savings</span>
          <strong>{impact?.estimated_energy_savings ?? "N/A"}</strong>
        </div>

        <div className="kpi-card">
          <span>Cost Savings</span>
          <strong>{impact?.estimated_cost_savings ?? "N/A"}</strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Baseline vs Simulated Usage</h2>

        <div className="chart-panel">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={360}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="baseline_usage"
                  name="Baseline Usage"
                  stroke="#2563eb"
                  strokeWidth={2}
                  dot={false}
                />
                <Line
                  type="monotone"
                  dataKey="simulated_usage"
                  name="Simulated Usage"
                  stroke="#16a34a"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              Run a scenario simulation to compare usage impact.
            </div>
          )}
        </div>
      </section>

      {simulationData && (
        <section className="dashboard-section">
          <h2>Simulation Summary</h2>

          <div className="summary-panel">
            <p>{simulationData.summary}</p>
            <p>
              <strong>Scenario:</strong>{" "}
              {simulationData.scenario_type.replaceAll("_", " ")}
            </p>
            <p>
              <strong>Consumption Reduction:</strong>{" "}
              {impact?.consumption_reduction_percent}%
            </p>
          </div>
        </section>
      )}
    </div>
  );
};

export default ScenarioSimulation;