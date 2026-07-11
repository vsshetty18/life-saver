"""
FASTag Routes
Handles FASTag toll history — simulated journey tracking for each vehicle.
"""

from flask import Blueprint, request, jsonify
from models import db, FastagHistory

fastag_bp = Blueprint("fastag_bp", __name__)


@fastag_bp.route("/add", methods=["POST"])
def add_fastag_entry():
    """
    Adds a new toll crossing record for a vehicle.
    Expects JSON body:
    {
        "vehicle_number": "KA01AB1234",
        "toll_name": "Nelamangala Toll Plaza",
        "city": "Bengaluru"
    }
    Used to seed sample journey data for demo purposes.
    """
    data = request.get_json()

    required_fields = ["vehicle_number", "toll_name", "city"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    entry = FastagHistory(
        vehicle_number=data["vehicle_number"],
        toll_name=data["toll_name"],
        city=data["city"]
    )
    db.session.add(entry)
    db.session.commit()

    return jsonify({"message": "FASTag entry added successfully"}), 201


@fastag_bp.route("/history/<vehicle_number>", methods=["GET"])
def get_history(vehicle_number):
    """
    Returns the full toll crossing history for a specific vehicle,
    most recent first.
    """
    entries = FastagHistory.query.filter_by(
        vehicle_number=vehicle_number
    ).order_by(FastagHistory.timestamp.desc()).all()

    result = [{
        "id": e.id,
        "toll_name": e.toll_name,
        "city": e.city,
        "timestamp": e.timestamp.isoformat()
    } for e in entries]

    return jsonify(result), 200


@fastag_bp.route("/recent/<vehicle_number>", methods=["GET"])
def get_recent_history(vehicle_number):
    """
    Returns only the last 5 toll plazas crossed by a vehicle.
    Used to show "journey history before accident" on the dashboard.
    """
    entries = FastagHistory.query.filter_by(
        vehicle_number=vehicle_number
    ).order_by(FastagHistory.timestamp.desc()).limit(5).all()

    result = [{
        "toll_name": e.toll_name,
        "city": e.city,
        "timestamp": e.timestamp.isoformat()
    } for e in entries]

    return jsonify(result), 200
