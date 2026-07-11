import React from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";

// Fix a common Leaflet + Vite/Webpack bug where marker icon images
// don't load correctly because of how bundlers handle asset URLs.
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
});

// Default map center: Bengaluru (matches our seeded sample data)
const DEFAULT_CENTER = [12.9716, 77.5946];

/**
 * MapView
 * Renders an OpenStreetMap (via Leaflet) with a marker for every
 * alert that has valid latitude/longitude coordinates.
 */
function MapView({ alerts = [] }) {
  // Only show alerts that actually have location data
  const alertsWithLocation = alerts.filter(
    (a) => a.latitude != null && a.longitude != null
  );

  return (
    <div className="leaflet-map-container">
      <MapContainer
        center={DEFAULT_CENTER}
        zoom={11}
        scrollWheelZoom={false}
        style={{ height: "100%", width: "100%" }}
      >
        {/* Free OpenStreetMap tiles - no API key required */}
        <TileLayer
          attribution='&copy; OpenStreetMap contributors'
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        />

        {alertsWithLocation.map((alert) => (
          <Marker
            key={alert.id}
            position={[alert.latitude, alert.longitude]}
          >
            <Popup>
              <strong>{alert.vehicle_number}</strong>
              <br />
              {alert.alert_type}
              {alert.speed ? ` — ${alert.speed} km/h` : ""}
              <br />
              <span className="text-xs text-gray-500">
                {new Date(alert.timestamp).toLocaleString()}
              </span>
            </Popup>
          </Marker>
        ))}

        {alertsWithLocation.length === 0 && (
          // No markers to show, but the map itself still renders fine
          <></>
        )}
      </MapContainer>
    </div>
  );
}

export default MapView;
