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
import {
  getEnergyForecast,
  getEnergyRecords,
} from "../../services/energyService";
import "/src/styles/forecast.css";

const ForecastAnalytics = () => {
  const [buildingId, setBuildingId] = useState("B001");
  const [deviceId, setDeviceId] = useState("");
  const [forecastType, setForecastType] = useState("next_24_hours");
  const [chartData, setChartData] = useState([]);
  const [forecastSummary, setForecastSummary] = useState(null);
  const [loading, setLoading] = useState(false);

  const formatLabel = (timestamp) => {
    return new Date(timestamp).toLocaleString([], {
      month: "short",
      day: "2-digit",
      hour: "2-digit",
    });
  };

  const buildChartData = (historicalRecords, forecastRecords) => {
    const recentHistorical = historicalRecords.slice(-48).map((item) => ({
      timestamp: item.timestamp,
      label: formatLabel(item.timestamp),
      historical_usage: item.energy_usage,
      predicted_usage: null,
    }));

    const futureForecast = forecastRecords.map((item) => ({
      timestamp: item.timestamp,
      label: formatLabel(item.timestamp),
      historical_usage: null,
      predicted_usage: item.predicted_energy_usage,
    }));

    return [...recentHistorical, ...futureForecast];
  };

  const handleGenerateForecast = async () => {
    try {
      setLoading(true);

      const filters = {
        building_id: buildingId || undefined,
        device_id: deviceId || undefined,
      };

      const [historicalData, forecastData] = await Promise.all([
        getEnergyRecords(filters),
        getEnergyForecast({
          forecastType,
          buildingId,
          deviceId,
        }),
      ]);

      const combinedData = buildChartData(
        historicalData,
        forecastData.forecast || []
      );

      setChartData(combinedData);
      setForecastSummary(forecastData);
    } catch (error) {
      console.error("Forecast analytics error:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Forecast Analytics</h1>
        <p>Compare historical energy consumption with predicted usage</p>
      </div>

      <div className="filter-panel">
        <div className="form-control">
          <label>Building ID</label>
          <input
            value={buildingId}
            onChange={(event) => setBuildingId(event.target.value)}
            placeholder="B001"
          />
        </div>

        <div className="form-control">
          <label>Device ID</label>
          <input
            value={deviceId}
            onChange={(event) => setDeviceId(event.target.value)}
            placeholder="Optional"
          />
        </div>

        <div className="form-control">
          <label>Forecast Type</label>
          <select
            value={forecastType}
            onChange={(event) => setForecastType(event.target.value)}
          >
            <option value="next_24_hours">Next 24 Hours</option>
            <option value="next_7_days">Next 7 Days</option>
            <option value="next_30_days">Next 30 Days</option>
          </select>
        </div>

        <button onClick={handleGenerateForecast} disabled={loading}>
          {loading ? "Generating..." : "Generate Forecast"}
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Historical Records</span>
          <strong>{forecastSummary?.total_historical_records || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Forecast Points</span>
          <strong>{forecastSummary?.forecast?.length || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Forecast Type</span>
          <strong>{forecastType.replaceAll("_", " ")}</strong>
        </div>

        <div className="kpi-card">
          <span>Model</span>
          <strong>{forecastSummary?.forecast?.[0]?.model_used || "N/A"}</strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Historical vs Predicted Usage</h2>

        <div className="chart-panel">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={380}>
              <LineChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line
                  type="monotone"
                  dataKey="historical_usage"
                  name="Historical Usage"
                  stroke="#2563eb"
                  strokeWidth={2}
                  dot={false}
                  connectNulls={false}
                />
                <Line
                  type="monotone"
                  dataKey="predicted_usage"
                  name="Predicted Usage"
                  stroke="#f97316"
                  strokeWidth={2}
                  dot={false}
                  connectNulls={false}
                />
              </LineChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              Select filters and generate a forecast to view chart data.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default ForecastAnalytics;