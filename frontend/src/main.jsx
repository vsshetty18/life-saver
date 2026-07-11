import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App.jsx";
import "./index.css";

// This is the entry point of the React app.
// It mounts the <App /> component into the #root div from index.html.
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    {/* BrowserRouter enables page navigation (Dashboard, Upload, Admin) */}
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </React.StrictMode>
);
