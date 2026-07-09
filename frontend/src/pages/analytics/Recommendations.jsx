import { useState } from "react";
import { getOptimizationRecommendations } from "../../services/recommendationService";
import "/src/styles/recommendation.css"

const Recommendations = () => {
  const [buildingId, setBuildingId] = useState("B001");
  const [deviceId, setDeviceId] = useState("");
  const [forecastType, setForecastType] = useState("next_24_hours");
  const [recommendationData, setRecommendationData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleGenerateRecommendations = async () => {
    try {
      setLoading(true);

      const result = await getOptimizationRecommendations({
        forecastType,
        buildingId,
        deviceId,
      });

      setRecommendationData(result);
    } catch (error) {
      console.error("Recommendation fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  const getPriorityClass = (priority) => {
    return priority || "low";
  };

  return (
    <div className="dashboard-page">
      <div className="page-header">
        <h1>Optimization Recommendations</h1>
        <p>AI-driven operational suggestions based on forecast and peak risk</p>
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

        <button onClick={handleGenerateRecommendations} disabled={loading}>
          {loading ? "Generating..." : "Generate"}
        </button>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Recommendations</span>
          <strong>{recommendationData?.recommendations_count || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Peak Alerts</span>
          <strong>{recommendationData?.context?.total_peak_alerts || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Forecast Points</span>
          <strong>{recommendationData?.context?.total_forecast_points || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Records Used</span>
          <strong>{recommendationData?.context?.total_historical_records || 0}</strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Recommended Actions</h2>

        <div className="recommendation-grid">
          {recommendationData?.recommendations?.length > 0 ? (
            recommendationData.recommendations.map((item, index) => (
              <div className="recommendation-card" key={index}>
                <div className="recommendation-card-header">
                  <span>{item.type?.replaceAll("_", " ")}</span>
                  <strong className={`priority-pill ${getPriorityClass(item.priority)}`}>
                    {item.priority}
                  </strong>
                </div>

                <p>{item.recommendation}</p>

                {item.reason && (
                  <div className="recommendation-reason">
                    {item.reason}
                  </div>
                )}

                {item.predicted_energy_usage && (
                  <small>
                    Predicted usage: {item.predicted_energy_usage} kWh
                  </small>
                )}
              </div>
            ))
          ) : (
            <div className="summary-panel">
              Generate recommendations to view optimization actions.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

export default Recommendations;