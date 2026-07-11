"""
Dashboard Routes
Provides aggregated data for the main dashboard and admin dashboard views.
Combines info from multiple tables into single, easy-to-consume endpoints.
"""

from flask import Blueprint, jsonify
from models import Alert, Vehicle, FastagHistory
from sqlalchemy import func

dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.route("/summary", methods=["GET"])
def get_summary():
    """
    Returns high-level stats for the main dashboard:
    - Total vehicles registered
    - Total alerts
    - Total accidents
    - Total overspeed violations
    """
    total_vehicles = Vehicle.query.count()
    total_alerts = Alert.query.count()
    total_accidents = Alert.query.filter_by(alert_type="Accident").count()
    total_overspeed = Alert.query.filter_by(alert_type="Overspeed").count()

    return jsonify({
        "total_vehicles": total_vehicles,
        "total_alerts": total_alerts,
        "total_accidents": total_accidents,
        "total_overspeed": total_overspeed
    }), 200


@dashboard_bp.route("/admin", methods=["GET"])
def get_admin_dashboard():
    """
    Returns detailed data for the Admin Dashboard page:
    - Recent alerts (last 10)
    - Speed violations list
    - Accident count
    - Notification logs (sms/email sent status)
    """
    recent_alerts = Alert.query.order_by(Alert.timestamp.desc()).limit(10).all()

    speed_violations = Alert.query.filter_by(alert_type="Overspeed") \
        .order_by(Alert.timestamp.desc()).all()

    accident_count = Alert.query.filter_by(alert_type="Accident").count()

    notification_logs = [{
        "vehicle_number": a.vehicle_number,
        "alert_type": a.alert_type,
        "sms_sent": a.sms_sent,
        "email_sent": a.email_sent,
        "timestamp": a.timestamp.isoformat()
    } for a in recent_alerts]

    return jsonify({
        "recent_alerts": [{
            "id": a.id,
            "vehicle_number": a.vehicle_number,
            "alert_type": a.alert_type,
            "speed": a.speed,
            "timestamp": a.timestamp.isoformat()
        } for a in recent_alerts],

        "speed_violations": [{
            "vehicle_number": v.vehicle_number,
            "speed": v.speed,
            "timestamp": v.timestamp.isoformat()
        } for v in speed_violations],

        "accident_count": accident_count,
        "notification_logs": notification_logs
    }), 200


@dashboard_bp.route("/vehicle/<vehicle_number>", methods=["GET"])
def get_vehicle_dashboard(vehicle_number):
    """
    Returns everything needed to show a single vehicle's full status
    on the dashboard after detection:
    - Latest alert (if any)
    - Last 5 FASTag toll crossings
    """
    latest_alert = Alert.query.filter_by(vehicle_number=vehicle_number) \
        .order_by(Alert.timestamp.desc()).first()

    fastag_history = FastagHistory.query.filter_by(vehicle_number=vehicle_number) \
        .order_by(FastagHistory.timestamp.desc()).limit(5).all()

    return jsonify({
        "vehicle_number": vehicle_number,
        "latest_alert": {
            "alert_type": latest_alert.alert_type,
            "speed": latest_alert.speed,
            "latitude": latest_alert.latitude,
            "longitude": latest_alert.longitude,
            "nearest_hospital": latest_alert.nearest_hospital,
            "nearest_police_station": latest_alert.nearest_police_station,
            "sms_sent": latest_alert.sms_sent,
            "email_sent": latest_alert.email_sent,
            "timestamp": latest_alert.timestamp.isoformat()
        } if latest_alert else None,

        "fastag_history": [{
            "toll_name": f.toll_name,
            "city": f.city,
            "timestamp": f.timestamp.isoformat()
        } for f in fastag_history]
    }), 200
