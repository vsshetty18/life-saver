"""
Alert Routes
Handles creation and retrieval of accident/overspeed alerts.
Also triggers SMS + Email notifications and finds nearest hospital/police station.
"""

from flask import Blueprint, request, jsonify
from models import db, Alert, Vehicle, Hospital, PoliceStation
from utils.notifications import send_sms, send_email
from utils.location_utils import find_nearest

alert_bp = Blueprint("alert_bp", __name__)


@alert_bp.route("/create", methods=["POST"])
def create_alert():
    """
    Creates a new alert (Accident or Overspeed).
    Expects JSON body:
    {
        "vehicle_number": "KA01AB1234",
        "alert_type": "Accident",   # or "Overspeed"
        "speed": 85.5,
        "latitude": 12.9716,
        "longitude": 77.5946
    }
    """
    data = request.get_json()

    required_fields = ["vehicle_number", "alert_type", "latitude", "longitude"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Find nearest hospital and police station using simulated DB tables
    nearest_hospital = find_nearest(Hospital, data["latitude"], data["longitude"])
    nearest_police = find_nearest(PoliceStation, data["latitude"], data["longitude"])

    # Create the alert record first (so it's saved even if notifications fail)
    alert = Alert(
        vehicle_number=data["vehicle_number"],
        alert_type=data["alert_type"],
        speed=data.get("speed"),
        latitude=data["latitude"],
        longitude=data["longitude"],
        nearest_hospital=nearest_hospital.name if nearest_hospital else None,
        nearest_police_station=nearest_police.name if nearest_police else None,
    )
    db.session.add(alert)
    db.session.commit()

    # Only send emergency notifications for actual accidents (not overspeed)
    if data["alert_type"] == "Accident":
        _send_accident_notifications(alert)

    return jsonify({
        "message": "Alert created successfully",
        "alert_id": alert.id,
        "nearest_hospital": alert.nearest_hospital,
        "nearest_police_station": alert.nearest_police_station
    }), 201


def _send_accident_notifications(alert):
    """
    Sends SMS to owner + 2 helpers, and an email notification.
    Updates the alert record with sms_sent / email_sent status.
    """
    vehicle = Vehicle.query.filter_by(vehicle_number=alert.vehicle_number).first()

    sms_success = False
    email_success = False

    message = (
        f"ACCIDENT ALERT: Vehicle {alert.vehicle_number} has been in an accident. "
        f"Location: {alert.latitude}, {alert.longitude}. "
        f"Nearest Hospital: {alert.nearest_hospital}. "
        f"Nearest Police Station: {alert.nearest_police_station}."
    )

    if vehicle:
        # Collect all phone numbers: owner + 2 helpers
        phone_numbers = []
        if vehicle.owner and vehicle.owner.phone_number:
            phone_numbers.append(vehicle.owner.phone_number)
        if vehicle.helper1_phone:
            phone_numbers.append(vehicle.helper1_phone)
        if vehicle.helper2_phone:
            phone_numbers.append(vehicle.helper2_phone)

        for number in phone_numbers:
            if send_sms(number, message):
                sms_success = True

        # Send email to owner if email is available
        if vehicle.owner and vehicle.owner.email:
            email_success = send_email(
                vehicle.owner.email,
                "Accident Alert - Immediate Attention Required",
                message
            )

    # Update alert with notification status
    alert.sms_sent = sms_success
    alert.email_sent = email_success
    db.session.commit()


@alert_bp.route("/list", methods=["GET"])
def list_alerts():
    """Returns all alerts, most recent first (used by dashboard)."""
    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    result = []
    for a in alerts:
        result.append({
            "id": a.id,
            "vehicle_number": a.vehicle_number,
            "alert_type": a.alert_type,
            "speed": a.speed,
            "latitude": a.latitude,
            "longitude": a.longitude,
            "nearest_hospital": a.nearest_hospital,
            "nearest_police_station": a.nearest_police_station,
            "sms_sent": a.sms_sent,
