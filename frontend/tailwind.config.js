/** @type {import('tailwindcss').Config} */
export default {
  // Tell Tailwind which files to scan for class names (so unused styles are removed in production build)
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Custom color palette for a clean, professional dashboard look
        primary: "#1e40af",     // deep blue - main brand color
        danger: "#dc2626",      // red - accident alerts
        warning: "#f59e0b",     // amber - overspeed warnings
        success: "#16a34a",     // green - normal/safe status
        dark: "#0f172a",        // dark background for cards/sidebar
      },
    },
  },
  plugins: [],
};
