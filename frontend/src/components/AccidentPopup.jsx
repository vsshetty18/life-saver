import React from "react";

/**
 * AccidentPopup
 * A fullscreen modal alert that appears the moment an accident is detected.
 * Designed to be impossible to miss — matches the spec's
 * "Display popup: Accident Detected" requirement.
 */
function AccidentPopup({ onClose }) {
  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 fade-in">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-sm w-full text-center">
        {/* Large warning icon */}
        <div className="text-6xl mb-4">🚨</div>

        <h2 className="text-xl font-bold text-danger mb-2">
          Accident Detected!
        </h2>

        <p className="text-gray-600 text-sm mb-6">
          An accident has been detected in the uploaded video. Emergency
          contacts and nearby services have been notified automatically.
        </p>

        <button
          onClick={onClose}
          className="bg-danger text-white px-6 py-2 rounded-lg font-medium
                     hover:bg-red-700 transition-colors w-full"
        >
          Acknowledge
        </button>
      </div>
    </div>
  );
}

export default AccidentPopup;
