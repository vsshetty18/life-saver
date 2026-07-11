/**
 * Central API configuration.
 * All backend calls go through this single axios instance,
 * so the base URL only needs to be changed in ONE place
 * when moving from local development to production (Render).
 */

import axios from "axios";

// In development, Vite's proxy (vite.config.js) forwards "/api" to Flask.
// In production, we use the real deployed backend URL from an environment variable.
const BASE_URL = import.meta.env.VITE_API_URL || "/api";

const api = axios.create({
  baseURL: BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export default api;
