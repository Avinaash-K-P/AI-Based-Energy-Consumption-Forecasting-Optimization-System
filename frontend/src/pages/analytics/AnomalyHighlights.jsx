import { useState } from "react";
import {
  CartesianGrid,
  Cell,
  ResponsiveContainer,
  Scatter,
  ScatterChart,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";
import { detectAnomalies } from "../../services/anomalyService";
import "/src/styles/anomaly.css"

const AnomalyHighlights = () => {
  const [buildingId, setBuildingId] = useState("B001");
  const [deviceId, setDeviceId] = useState("");
  const [anomalyData, setAnomalyData] = useState(null);
  const [loading, setLoading] = useState(false);

  const formatLabel = (timestamp) => {
    return new Date(timestamp).toLocaleString([], {
      month: "short",
      day: "2-digit",
      hour: "2-digit",
    });
  };

  const getSeverityColor = (severity) => {
    if (severity === "high") return "#dc2626";
    if (severity === "medium") return "#f97316";
    return "#2563eb";
  };

  const buildChartData = (anomalies = []) => {
    return anomalies.map((item, index) => ({
      x: index + 1,
      label: formatLabel(item.timestamp),
      usage: item.energy_usage,
      severity: item.severity,
      type: item.anomaly_type,
      source: item.source,
    }));
  };

  const handleDetectAnomalies = async () => {
    try {
      setLoading(true);

      const result = await detectAnomalies({
        buildingId,
        deviceId,
      });

      setAnomalyData(result);
    } catch (error) {
      console.error("Anomaly detection error:", error);
    } finally {
      setLoading(false);
    }
  };

  const chartData = buildChartData(anomalyData?.anomalies || []);

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Anomaly Highlights</h1>
        <p>Detect spikes, night-time usage, and abnormal sensor behavior</p>
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

        <button onClick={handleDetectAnomalies} disabled={loading}>
          {loading ? "Detecting..." : "Detect Anomalies"}
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Total Anomalies</span>
          <strong>{anomalyData?.total_anomalies || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Detection Method</span>
          <strong>{anomalyData?.method || "N/A"}</strong>
        </div>

        <div className="kpi-card">
          <span>Spike Threshold</span>
          <strong>{anomalyData?.thresholds?.spike_threshold || "N/A"}</strong>
        </div>

        <div className="kpi-card">
          <span>Night Threshold</span>
          <strong>
            {anomalyData?.thresholds?.night_usage_threshold || "N/A"}
          </strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Anomaly Chart</h2>

        <div className="chart-panel">
          {chartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={360}>
              <ScatterChart>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis
                  dataKey="x"
                  name="Reading"
                  tick={{ fontSize: 12 }}
                />
                <YAxis dataKey="usage" name="Energy Usage" />
                <Tooltip
                  cursor={{ strokeDasharray: "3 3" }}
                  formatter={(value, name) => [value, name]}
                  labelFormatter={(_, payload) =>
                    payload?.[0]?.payload?.label || ""
                  }
                />
                <Scatter name="Anomalies" data={chartData}>
                  {chartData.map((entry, index) => (
                    <Cell
                      key={index}
                      fill={getSeverityColor(entry.severity)}
                    />
                  ))}
                </Scatter>
              </ScatterChart>
            </ResponsiveContainer>
          ) : (
            <div className="empty-state">
              Run anomaly detection to highlight abnormal consumption points.
            </div>
          )}
        </div>
      </section>

      <section className="dashboard-section">
        <h2>Detected Anomalies</h2>

        <div className="table-panel">
          {anomalyData?.anomalies?.length > 0 ? (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Time</th>
                  <th>Device</th>
                  <th>Usage</th>
                  <th>Type</th>
                  <th>Severity</th>
                  <th>Source</th>
                </tr>
              </thead>
              <tbody>
                {anomalyData.anomalies.slice(0, 50).map((item, index) => (
                  <tr key={index}>
                    <td>{formatLabel(item.timestamp)}</td>
                    <td>{item.device_id || "N/A"}</td>
                    <td>{item.energy_usage}</td>
                    <td>{item.anomaly_type.replaceAll("_", " ")}</td>
                    <td>
                      <span className={`severity-pill ${item.severity}`}>
                        {item.severity}
                      </span>
                    </td>
                    <td>{item.source}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <div className="summary-panel">
              No anomalies detected for the selected filters.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default AnomalyHighlights;