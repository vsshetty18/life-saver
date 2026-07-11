import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// Vite configuration for the React frontend
export default defineConfig({
  plugins: [react()],

  server: {
    port: 5173, // default dev server port
    proxy: {
      // Forward any request starting with /api to the Flask backend
      // This avoids CORS issues during local development
      "/api": {
        target: "http://localhost:5000",
        changeOrigin: true,
      },
    },
  },
});
