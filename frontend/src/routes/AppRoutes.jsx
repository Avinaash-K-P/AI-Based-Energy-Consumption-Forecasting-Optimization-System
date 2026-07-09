import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "../pages/auth/Login";
import Register from "../pages/auth/Register";
import Dashboard from "../pages/analytics/Dashboard";
import DashboardLayout from "../layouts/DashboardLayout";
import DatasetUpload from "../pages/analytics/DatasetUpload";
import ForecastAnalytics from "../pages/analytics/ForecastAnalytics";
import PeakConsumption from "../pages/analytics/PeakConsumption";
import AnomalyHighlights from "../pages/analytics/AnomalyHighlights";
import Recommendations from "../pages/analytics/Recommendations";
import ScenarioSimulation from "../pages/analytics/ScenarioSimulation";

function AppRoutes()
{
    return(
        <BrowserRouter>
            <Routes>
                <Route path = "/"                   element = {<Login/>}/>
                <Route path = "/register"           element = {<Register/>} />

                <Route path="/dashboard"            element={<DashboardLayout />}>
                    <Route index element={<Dashboard />} />
                    <Route path="dataset"           element={<DatasetUpload />} />
                    <Route path="forecast"          element={<ForecastAnalytics />} />
                    <Route path="peaks"             element={<PeakConsumption />} />
                    <Route path="anomalies"         element={<AnomalyHighlights />} />
                    <Route path="recommendations"   element={<Recommendations />} />
                    <Route path="simulation"        element={<ScenarioSimulation />} />
                </Route>
            
            </Routes>
        </BrowserRouter>
    )
}

export default AppRoutes;