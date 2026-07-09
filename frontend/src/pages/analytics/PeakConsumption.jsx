import { useState } from "react";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import {
  getFuturePeakPrediction,
  getHistoricalSpikes,
} from "../../services/peakService";
import "/src/styles/peak_consumption.css"


const PeakConsumption = () => {
  const [buildingId, setBuildingId] = useState("B001");
  const [deviceId, setDeviceId] = useState("");
  const [forecastType, setForecastType] = useState("next_24_hours");
  const [peakData, setPeakData] = useState(null);
  const [spikeData, setSpikeData] = useState(null);
  const [loading, setLoading] = useState(false);

  const formatLabel = (timestamp) => {
    return new Date(timestamp).toLocaleString([], {
      month: "short",
      day: "2-digit",
      hour: "2-digit",
    });
  };

  const buildPeakChartData = (periods = []) => {
    return periods.map((item) => ({
      label: formatLabel(item.timestamp),
      usage: item.predicted_energy_usage,
      level: item.level,
    }));
  };

  const getBarColor = (level) => {
    if (level === "unusual_spike") return "#dc2626";
    if (level === "peak") return "#f97316";
    if (level === "high_load") return "#eab308";
    return "#2563eb";
  };

  const handleAnalyze = async () => {
    try {
      setLoading(true);

      const [futurePeaks, historicalSpikes] = await Promise.all([
        getFuturePeakPrediction({
          forecastType,
          buildingId,
          deviceId,
        }),
        getHistoricalSpikes({
          buildingId,
          deviceId,
        }),
      ]);

      setPeakData(futurePeaks);
      setSpikeData(historicalSpikes);
    } catch (error) {
      console.error("Peak analysis error:", error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = buildPeakChartData(peakData?.peak_periods || []);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Peak Consumption</h1>
        <p>Visualize high-load periods and future peak usage alerts</p>
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

        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? "Analyzing..." : "Analyze Peaks"}
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Future Alerts</span>
          <strong>{peakData?.total_alerts || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Peak Periods</span>
          <strong>{peakData?.peak_periods?.length || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Historical Spikes</span>
          <strong>{spikeData?.total_spikes || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Peak Threshold</span>
          <strong>{peakData?.thresholds?.peak_threshold || "N/A"}</strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Peak Usage Visualization</h2>

        <div className="chart-panel">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={360}>
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="label" tick={{ fontSize: 12 }} />
                <YAxis />
                <Tooltip />
                <Bar dataKey="usage" name="Predicted Usage">
                  {chartData.map((entry, index) => (
                    <Cell key={index} fill={getBarColor(entry.level)} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              Run peak analysis to visualize future high-load periods.
            </div>
          )}
        </div>
      </section>

      <section className="dashboard-section">
        <h2>Peak Alerts</h2>

        <div className="alert-list">
          {peakData?.alerts?.length > 0 ? (
            peakData.alerts.map((alert, index) => (
              <div className={`alert-card ${alert.level}`} key={index}>
                <strong>{alert.level.replaceAll("_", " ")}</strong>
                <p>{alert.message}</p>
              </div>
            ))
          ) : (
            <div className="summary-panel">
              No future peak alerts found for the selected filters.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default PeakConsumption;