import { Link, Outlet, useNavigate } from "react-router-dom";
import {  jwtDecode } from "jwt-decode";
import "/src/styles/layout.css"
import {
    FaTachometerAlt,
    FaDatabase,
    FaChartLine,
    FaBolt,
    FaExclamationTriangle,
    FaLightbulb,
    FaFlask,
    FaChartPie
} from "react-icons/fa";

const DashboardLayout = () => {
  const navigate = useNavigate();
  
  //Retrieving username from JWT Decode
  const token = localStorage.getItem("token");

  const user = token ? jwtDecode(token) : null;

  const username = user?.username;   //To get role
  
  //Logout
  const handleLogout = () => {
    localStorage.removeItem("token");  
    navigate("/");
  };
  return (
    
    <div className="dashboard-layout">
      <header className="dashboard-header">
        <div className="dashboard-title">
           <FaChartPie className="title-icon" />
           <span>AI Energy Consumption Forecast</span>
        </div>

        <div className="dashboard-user">
          <h5> Welcome, {username} </h5>
          <button type="button" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </header>

      <div className="dashboard-body">
        <aside className="dashboard-sidebar">
          <nav>

    <Link to="/dashboard">
        <FaTachometerAlt />
        <span>Dashboard</span>
    </Link>

    <Link to="/dashboard/dataset">
        <FaDatabase />
        <span>Dataset Upload</span>
    </Link>

    <Link to="/dashboard/forecast">
        <FaChartLine />
        <span>Forecast Analytics</span>
    </Link>

    <Link to="/dashboard/peaks">
        <FaBolt />
        <span>Peak Prediction</span>
    </Link>

    <Link to="/dashboard/anomalies">
        <FaExclamationTriangle />
        <span>Anomaly Detection</span>
    </Link>

    <Link to="/dashboard/recommendations">
        <FaLightbulb />
        <span>Recommendations</span>
    </Link>

    <Link to="/dashboard/simulation">
        <FaFlask />
        <span>Scenario Simulation</span>
    </Link>

</nav>
        </aside>

        <main className="dashboard-main">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;