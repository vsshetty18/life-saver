import React from "react";

/**
 * StatCard
 * A small reusable card that displays one summary statistic
 * (e.g. Total Vehicles, Total Alerts) with an icon and color accent.
 */
function StatCard({ label, value, color = "primary", icon }) {
  // Maps the "color" prop to actual Tailwind background classes.
  // Using a lookup object instead of string interpolation because
  // Tailwind needs full class names present in the code to generate them.
  const colorMap = {
    primary: "bg-primary/10 text-primary",
    danger: "bg-danger/10 text-danger",
    warning: "bg-warning/10 text-warning",
    success: "bg-success/10 text-success",
  };

  return (
    <div className="bg-white rounded-xl shadow p-4 flex items-center gap-4">
      {/* Icon badge */}
      <div className={`w-12 h-12 rounded-lg flex items-center justify-center text-2xl ${colorMap[color]}`}>
        {icon}
      </div>

      {/* Label + value */}
      <div>
        <p className="text-gray-500 text-sm">{label}</p>
        <p className="text-2xl font-bold text-gray-800">{value}</p>
      </div>
    </div>
  );
}

export default StatCard;
