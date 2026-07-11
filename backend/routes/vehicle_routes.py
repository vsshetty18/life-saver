"""
Vehicle Routes
Handles video/webcam upload and triggers vehicle detection + speed estimation.
"""

import os
from flask import Blueprint, request, jsonify, current_app
from werkzeug.utils import secure_filename
from models import db, Vehicle, Owner

vehicle_bp = Blueprint("vehicle_bp", __name__)


def allowed_file(filename):
    """Check if the uploaded file has a valid video extension."""
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in current_app.config["ALLOWED_EXTENSIONS"]
    )


@vehicle_bp.route("/upload", methods=["POST"])
def upload_video():
    """
    Accepts a video file uploaded from the frontend.
    Saves it to the uploads/ folder so the AI detection module can process it.
    """
    if "video" not in request.files:
        return jsonify({"error": "No video file provided"}), 400

    file = request.files["video"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Allowed: mp4, avi, mov"}), 400

    # Save file safely (prevents malicious filenames)
    filename = secure_filename(file.filename)
    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
    file.save(filepath)

    return jsonify({
        "message": "Video uploaded successfully",
        "filename": filename,
        "path": filepath
    }), 200


@vehicle_bp.route("/detect", methods=["POST"])
def detect_vehicle():
    """
    Runs YOLOv8 vehicle detection + speed estimation on an uploaded video.
    Expects JSON body: { "filename": "video.mp4" }
    """
    data = request.get_json()
    filename = data.get("filename") if data else None

    if not filename:
        return jsonify({"error": "filename is required"}), 400

    filepath = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)

    if not os.path.exists(filepath):
        return jsonify({"error": "Video file not found. Please upload first."}), 404

    # Import here (not at top) to avoid loading the heavy YOLO model
    # unless this route is actually called
    from model.detect_and_track import process_video

    results = process_video(filepath, current_app.config["SPEED_LIMIT"],
                             current_app.config["DISTANCE_BETWEEN_LINES"])

    return jsonify({
        "message": "Detection completed",
        "results": results
    }), 200


@vehicle_bp.route("/register", methods=["POST"])
def register_vehicle():
    """
    Registers a new vehicle with owner info (simulated RTO data).
    Expects JSON body with vehicle_number, owner name, phone, etc.
    """
    data = request.get_json()

    required_fields = ["vehicle_number", "owner_name", "owner_phone"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"{field} is required"}), 400

    # Create owner first
    owner = Owner(
        name=data["owner_name"],
        phone_number=data["owner_phone"],
        email=data.get("owner_email")
    )
    db.session.add(owner)
    db.session.flush()  # gets owner.id before committing

    # Create vehicle linked to that owner
    vehicle = Vehicle(
        vehicle_number=data["vehicle_number"],
        vehicle_type=data.get("vehicle_type", "car"),
        owner_id=owner.id,
        helper1_phone=data.get("helper1_phone"),
        helper2_phone=data.get("helper2_phone")
    )
    db.session.add(vehicle)
    db.session.commit()

    return jsonify({"message": "Vehicle registered successfully"}), 201


@vehicle_bp.route("/list", methods=["GET"])
def list_vehicles():
    """Returns all registered vehicles (used by admin dashboard)."""
    vehicles = Vehicle.query.all()
    result = []
    for v in vehicles:
        result.append({
            "id": v.id,
            "vehicle_number": v.vehicle_number,
            "vehicle_type": v.vehicle_type,
            "owner_name": v.owner.name if v.owner else None,
            "owner_phone": v.owner.phone_number if v.owner else None
        })
    return jsonify(result), 200
