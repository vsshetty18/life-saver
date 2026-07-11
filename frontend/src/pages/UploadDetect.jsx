import React, { useState } from "react";
import api from "../api/api.js";
import AccidentPopup from "../components/AccidentPopup.jsx";

/**
 * Upload & Detect Page
 * Lets the user upload a video, run detection on it, and see results
 * (speed, overspeed flags, accident detection) immediately.
 */
function UploadDetect() {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [detecting, setDetecting] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState("");
  const [showAccidentPopup, setShowAccidentPopup] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setResults(null);
    setError("");
  };

  const handleUploadAndDetect = async () => {
    if (!file) {
      setError("Please select a video file first.");
      return;
    }

    setError("");
    setResults(null);

    try {
      // Step 1: Upload the video
      setUploading(true);
      const formData = new FormData();
      formData.append("video", file);

      const uploadRes = await api.post("/vehicle/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploading(false);

      // Step 2: Run detection on the uploaded video
      setDetecting(true);
      const detectRes = await api.post("/vehicle/detect", {
        filename: uploadRes.data.filename,
      });
      setDetecting(false);

      const detectedVehicles = detectRes.data.results || [];
      setResults(detectedVehicles);

      // If any vehicle triggered accident detection, show the popup alert
      const hasAccident = detectedVehicles.some((v) => v.accident_detected);
      if (hasAccident) {
        setShowAccidentPopup(true);
      }
    } catch (err) {
      console.error(err);
      setError(
        err.response?.data?.error || "Something went wrong. Please try again."
      );
      setUploading(false);
      setDetecting(false);
    }
  };

  return (
    <div>
      <h1 className="text-2xl font-bold text-gray-800 mb-6">
        Upload & Detect
      </h1>

      {/* Upload card */}
      <div className="bg-white rounded-xl shadow p-6 mb-6 max-w-xl">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select a video file (mp4, avi, mov)
        </label>
        <input
          type="file"
          accept=".mp4,.avi,.mov"
          onChange={handleFileChange}
          className="block w-full text-sm text-gray-600 mb-4
                     file:mr-4 file:py-2 file:px-4 file:rounded-lg
                     file:border-0 file:bg-primary file:text-white
                     hover:file:bg-blue-800 file:cursor-pointer"
        />

        <button
          onClick={handleUploadAndDetect}
          disabled={uploading || detecting}
          className="bg-primary text-white px-5 py-2 rounded-lg font-medium
                     hover:bg-blue-800 transition-colors disabled:opacity-50
                     disabled:cursor-not-allowed"
        >
          {uploading
            ? "Uploading..."
            : detecting
            ? "Detecting..."
            : "Upload & Run Detection"}
        </button>

        {error && (
          <p className="text-danger text-sm mt-3">{error}</p>
        )}
      </div>

      {/* Results table */}
      {results && (
        <div className="bg-white rounded-xl shadow p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">
            Detection Results
          </h2>

          {results.length === 0 ? (
            <p className="text-gray-400 text-sm">
              No vehicles were detected in this video.
            </p>
          ) : (
            <table className="w-full text-sm text-left">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="py-2">Vehicle ID</th>
                  <th className="py-2">Type</th>
                  <th className="py-2">Speed (km/h)</th>
                  <th className="py-2">Status</th>
                </tr>
              </thead>
              <tbody>
                {results.map((v) => (
                  <tr key={v.vehicle_id} className="border-b border-gray-50">
                    <td className="py-2">#{v.vehicle_id}</td>
                    <td className="py-2 capitalize">{v.vehicle_type}</td>
                    <td className="py-2">{v.speed}</td>
                    <td className="py-2">
                      {v.accident_detected ? (
                        <span className="text-danger font-semibold">
                          🚨 Accident
                        </span>
                      ) : v.is_overspeed ? (
                        <span className="text-warning font-semibold">
                          ⏱️ Overspeed
                        </span>
                      ) : (
                        <span className="text-success font-semibold">
                          ✅ Normal
                        </span>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>
      )}

      {/* Accident popup shown when detection finds an accident */}
      {showAccidentPopup && (
        <AccidentPopup onClose={() => setShowAccidentPopup(false)} />
      )}
    </div>
  );
}

export default UploadDetect;
