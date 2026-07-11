# SpeedGuard AI 🚗🚨
### Real-Time Vehicle Speed Detection and Accident Alert System

A final-year BE (AI & ML) major project that detects vehicle speed from video,
identifies possible accidents, and automatically alerts emergency contacts —
all backed by a simulated FASTag/RTO/hospital/police database.

---

## 🧩 Tech Stack

| Layer        | Technology                          |
|--------------|--------------------------------------|
| Frontend     | React + Vite + Tailwind CSS          |
| Backend      | Python + Flask                       |
| AI / CV      | YOLOv8 (Ultralytics) + OpenCV        |
| Database     | SQLite (via SQLAlchemy ORM)          |
| Maps         | Leaflet.js (OpenStreetMap)           |
| Notifications| Twilio (SMS) + SMTP (Email)          |
| Deployment   | Frontend → Vercel, Backend → Render  |

---

## ✨ Features

- 🎥 Upload a video (or webcam) and detect vehicles using YOLOv8
- ⏱️ Estimate real-world speed using a two-line crossing method
- 🚨 Simple rule-based accident detection (sudden stop after fast movement)
- 📩 Automatic SMS (Twilio) + Email alerts to owner & 2 emergency contacts
- 🏥 Nearest hospital & police station lookup (Haversine distance, simulated DB)
- 🛣️ Simulated FASTag toll journey history (last 5 tolls before incident)
- 🗺️ Live map of all alert locations (Leaflet + OpenStreetMap, no API key)
- 📊 Dashboard with stats, recent alerts, and map
- 🛠️ Admin panel with speed violations, accident count, notification logs

---

## 📁 Project Structure
