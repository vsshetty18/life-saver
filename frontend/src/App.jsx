import React from "react";
import { Routes, Route } from "react-router-dom";
import Sidebar from "./components/Sidebar.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import UploadDetect from "./pages/UploadDetect.jsx";
import AdminDashboard from "./pages/AdminDashboard.jsx";

/**
 * Root App component.
 * Lays out a fixed Sidebar for navigation + a main content area
 * that swaps pages based on the current route.
 */
function App() {
  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Sidebar stays visible on every page */}
      <Sidebar />

      {/* Main content area changes based on the route */}
      <main className="flex-1 p-6 ml-64">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<UploadDetect />} />
          <Route path="/admin" element={<AdminDashboard />} />
        </Routes>
      </main>
    </div>
  );
}

export default App;
