import { useEffect, useState } from "react";
import "/src/styles/dashboard.css";
import { getDashboardOverview } from "../../services/dashboardService";

const Dashboard = () => {
  const [status, setStatus] = useState(null);
  const [trainingSummary, setTrainingSummary] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchDashboardData = async () => {
    try {
      const data = await getDashboardOverview();

      setStatus(data.status);
      setTrainingSummary(data.trainingSummary);
    } catch (error) {
      console.error("Dashboard fetch error:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  if (loading) {
    return <div className="page-loading">Loading dashboard...</div>;
  }

  return (

    <div className="dashboard-page">
      <div className="page-header">
        <h1>Dashboard Overview</h1>
        <p>ML pipeline health and energy dataset summary</p>
      </div>

      <div className="kpi-grid">
        <div className="kpi-card">
          <span>Total Records</span>
          <strong>{status?.total_energy_records || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Buildings</span>
          <strong>{status?.total_buildings || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Devices</span>
          <strong>{status?.total_devices || 0}</strong>
        </div>

        <div className="kpi-card">
          <span>Model Status</span>
          <strong>{trainingSummary?.model_status || "unknown"}</strong>
        </div>
      </div>

      <section className="dashboard-section">
        <h2>Available ML Modules</h2>

        <div className="module-grid">
          {status?.modules &&
            Object.entries(status.modules).map(([moduleName, moduleStatus]) => (
              <div className="module-card" key={moduleName}>
                <span>{moduleName.replaceAll("_", " ")}</span>
                <strong>{moduleStatus}</strong>
              </div>
            ))}
        </div>
      </section>

      <section className="dashboard-section">
        <h2>Training Summary</h2>

        <div className="summary-panel">
          <p>{trainingSummary?.message}</p>
          <p>
            <strong>Model:</strong>{" "}
            {trainingSummary?.model_type || "Baseline / pending"}
          </p>
          <p>
            <strong>Total Records:</strong>{" "}
            {trainingSummary?.total_records || 0}
          </p>
        </div>
      </section>
    </div>

  )
}

export default Dashboard;