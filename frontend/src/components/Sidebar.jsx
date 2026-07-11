import React from "react";
import { NavLink } from "react-router-dom";

/**
 * Sidebar Navigation
 * Fixed on the left side of the screen, links to all main pages.
 * Uses NavLink so the active page's link is automatically highlighted.
 */
function Sidebar() {
  // Reusable Tailwind classes for nav links (active vs inactive states)
  const linkClasses = ({ isActive }) =>
    `flex items-center gap-3 px-4 py-3 rounded-lg mb-2 transition-colors ${
      isActive
        ? "bg-primary text-white"
        : "text-gray-300 hover:bg-gray-800"
    }`;

  return (
    <aside className="fixed left-0 top-0 h-screen w-64 bg-dark p-4 flex flex-col">
      {/* App title / branding */}
      <div className="mb-8 px-2">
        <h1 className="text-white text-lg font-bold leading-tight">
          SpeedGuard AI
        </h1>
        <p className="text-gray-400 text-xs mt-1">
          Vehicle Speed & Accident Detection
        </p>
      </div>

      {/* Navigation links */}
      <nav className="flex-1">
        <NavLink to="/" end className={linkClasses}>
          📊 Dashboard
        </NavLink>
        <NavLink to="/upload" className={linkClasses}>
          🎥 Upload & Detect
        </NavLink>
        <NavLink to="/admin" className={linkClasses}>
          🛠️ Admin Panel
        </NavLink>
      </nav>

      {/* Footer note */}
      <div className="text-gray-500 text-xs px-2">
        Final Year Major Project
      </div>
    </aside>
  );
}

export default Sidebar;
