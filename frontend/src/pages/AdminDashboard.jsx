import React, { useEffect, useState } from "react";
import api from "../api/api.js";
import StatCard from "../components/StatCard.jsx";

/**
 * Admin Dashboard Page
 * Shows detailed operational data: recent alerts, speed violations,
 * accident count, and notification (SMS/Email) logs.
 * Matches the spec's "Admin Dashboard" feature exactly.
 */
function AdminDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const res = await api.get("/dashboard/admin");
      setData(res.data);
    } catch (error) {
      console.error("Failed to load admin dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p className="text-gray-500">Loading admin panel...</p>;
  }

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">Admin Panel</h1>

      {/* Accident count highlight */}
      <div className="mb-6 max-w-xs">
        <StatCard
          label="Total Accidents"
          value={data?.accident_count ?? 0}
          color="danger"
          icon="🚨"
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Speed Violations table */}
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Speed Violations
          </h2>
          {data?.speed_violations?.length ? (
            <table className="w-full text-sm text-left">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="py-2">Vehicle</th>
                  <th className="py-2">Speed</th>
                  <th className="py-2">Time</th>
                </tr>
              </thead>
              <tbody>
                {data.speed_violations.map((v, idx) => (
                  <tr key={idx} className="border-b border-gray-50">
                    <td className="py-2">{v.vehicle_number}</td>
                    <td className="py-2 text-warning font-semibold">
                      {v.speed} km/h
                    </td>
                    <td className="py-2 text-gray-400 text-xs">
                      {new Date(v.timestamp).toLocaleString()}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-gray-400 text-sm py-4 text-center">
              No speed violations recorded.
            </p>
          )}
        </div>

        {/* Notification Logs table */}
        <div className="bg-white rounded-xl shadow p-4">
          <h2 className="text-lg font-semibold text-gray-800 mb-3">
            Notification Logs
          </h2>
          {data?.notification_logs?.length ? (
            <table className="w-full text-sm text-left">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="py-2">Vehicle</th>
                  <th className="py-2">Type</th>
                  <th className="py-2">SMS</th>
                  <th className="py-2">Email</th>
                </tr>
              </thead>
              <tbody>
                {data.notification_logs.map((log, idx) => (
                  <tr key={idx} className="border-b border-gray-50">
                    <td className="py-2">{log.vehicle_number}</td>
                    <td className="py-2">{log.alert_type}</td>
                    <td className="py-2">
                      {log.sms_sent ? "✅" : "❌"}
                    </td>
                    <td className="py-2">
                      {log.email_sent ? "✅" : "❌"}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <p className="text-gray-400 text-sm py-4 text-center">
              No notifications sent yet.
            </p>
          )}
        </div>
      </div>

      {/* Recent Alerts full list */}
      <div className="bg-white rounded-xl shadow p-4 mt-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-3">
          Recent Alerts
        </h2>
        {data?.recent_alerts?.length ? (
          <table className="w-full text-sm text-left">
            <thead>
              <tr className="border-b text-gray-500">
                <th className="py-2">Vehicle</th>
                <th className="py-2">Type</th>
                <th className="py-2">Speed</th>
                <th className="py-2">Time</th>
              </tr>
            </thead>
            <tbody>
              {data.recent_alerts.map((a) => (
                <tr key={a.id} className="border-b border-gray-50">
                  <td className="py-2">{a.vehicle_number}</td>
                  <td className="py-2">
                    <span
                      className={
                        a.alert_type === "Accident"
                          ? "text-danger font-semibold"
                          : "text-warning font-semibold"
                      }
                    >
                      {a.alert_type}
                    </span>
                  </td>
                  <td className="py-2">{a.speed ?? "-"}</td>
                  <td className="py-2 text-gray-400 text-xs">
                    {new Date(a.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          <p className="text-gray-400 text-sm py-4 text-center">
            No alerts recorded yet.
          </p>
        )}
      </div>
    </div>
  );
}

export default AdminDashboard;
