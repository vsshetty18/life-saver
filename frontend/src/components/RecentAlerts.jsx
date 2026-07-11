import React from "react";

/**
 * RecentAlerts
 * Displays a short list of the most recent alerts (accident/overspeed)
 * with color-coded badges based on alert type.
 */
function RecentAlerts({ alerts }) {
  // No alerts yet — show a friendly empty state instead of a blank box
  if (!alerts || alerts.length === 0) {
    return (
      <p className="text-gray-400 text-sm text-center py-8">
        No alerts yet. Alerts will appear here once detection runs.
      </p>
    );
  }

  return (
    <ul className="divide-y divide-gray-100">
      {alerts.map((alert) => (
        <li
          key={alert.id}
          className="py-3 flex items-center justify-between fade-in"
        >
          <div>
            <p className="font-medium text-gray-800">
              {alert.vehicle_number}
            </p>
            <p className="text-xs text-gray-400">
              {new Date(alert.timestamp).toLocaleString()}
            </p>
          </div>

          {/* Color-coded badge: red for accidents, amber for overspeed */}
          <span
            className={`text-xs font-semibold px-3 py-1 rounded-full ${
              alert.alert_type === "Accident"
                ? "bg-danger/10 text-danger"
                : "bg-warning/10 text-warning"
            }`}
          >
            {alert.alert_type === "Accident" ? "🚨 Accident" : "⏱️ Overspeed"}
          </span>
        </li>
      ))}
    </ul>
  );
}

export default RecentAlerts;
