import React, { useEffect, useState } from "react";
import api from "../api/api.js";
import StatCard from "../components/StatCard.jsx";
import RecentAlerts from "../components/RecentAlerts.jsx";
import MapView from "../components/MapView.jsx";

/**
 * Main Dashboard Page
 * Shows high-level stats, recent alerts, and a map with the latest
 * accident/overspeed locations. This is the "home page" of the app.
 */
function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [alerts, setAlerts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      // Fetch summary stats and recent alerts in parallel for speed
      const [summaryRes, alertsRes] = await Promise.all([
        api.get("/dashboard/summary"),
        api.get("/alert/list"),
      ]);

      setSummary(summaryRes.data);
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p className="text-gray-500">Loading dashboard...</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Dashboard</h1>

      {/* Stat cards row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
        <StatCard
          label="Total Vehicles"
          value={summary?.total_vehicles ?? 0}
          color="primary"
          icon="🚗"
        />
        <StatCard
          label="Total Alerts"
          value={summary?.total_alerts ?? 0}
          color="warning"
          icon="⚠️"
        />
        <StatCard
          label="Accidents"
          value={summary?.total_accidents ?? 0}
          color="danger"
          icon="🚨"
        />
        <StatCard
          label="Overspeed Violations"
          value={summary?.total_overspeed ?? 0}
          color="warning"
          icon="⏱️"
        />
      </div>

      {/* Map + Recent Alerts side by side */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Alert Locations
          </h2>
          <MapView alerts={alerts} />
        </div>

        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Recent Alerts
          </h2>
          <RecentAlerts alerts={alerts.slice(0, 5)} />
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
