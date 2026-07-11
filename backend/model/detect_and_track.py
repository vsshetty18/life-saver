"""
Vehicle Detection, Speed Estimation & Accident Detection
==========================================================
This is the core AI module of the project.

Pipeline for each video:
1. Run YOLOv8 to detect vehicles in every frame.
2. Track each vehicle across frames using simple centroid tracking.
3. Estimate speed using how far the vehicle moved between two reference lines.
4. Detect accidents using simple rules (sudden stop / heavy overlap).

Kept intentionally simple (no deep tracking algorithms like DeepSORT)
since this is a college-level demo project.
"""

import cv2
from ultralytics import YOLO

# Load YOLOv8 pretrained model once when this module is imported.
# "yolov8n.pt" = the small/fast "nano" version — good enough for a demo project.
model = YOLO("yolov8n.pt")

# COCO class IDs for vehicles (YOLOv8 is pretrained on the COCO dataset)
VEHICLE_CLASSES = {2: "car", 3: "motorcycle", 5: "bus", 7: "truck"}

# Two virtual horizontal lines used to measure speed.
# When a vehicle crosses LINE_1 then LINE_2, we know how long it took
# to cover DISTANCE_BETWEEN_LINES (from config), so we can calculate speed.
LINE_1_Y = 300
LINE_2_Y = 500

# Safety cap: stop processing very long videos after this many frames (demo purposes)
MAX_FRAMES = 2000


def get_centroid(box):
    """Returns the center point (x, y) of a bounding box [x1, y1, x2, y2]."""
    x1, y1, x2, y2 = box
    return int((x1 + x2) / 2), int((y1 + y2) / 2)


def process_video(video_path, speed_limit, distance_between_lines):
    """
    Processes the uploaded video and returns detection results.

    Returns a list of dicts, one per tracked vehicle, containing:
    - vehicle_id, vehicle_type, speed, is_overspeed, accident_detected
    """
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30  # fallback to 30 fps if unknown

    # Tracks each vehicle's data across frames.
    # Key = a simple tracking ID we assign, Value = tracking info.
    tracked_vehicles = {}
    next_id = 0

    frame_count = 0

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break  # end of video

        frame_count += 1

        # Run YOLOv8 detection on this frame
        results = model(frame, verbose=False)[0]

        current_boxes = []
        for box in results.boxes:
            class_id = int(box.cls[0])
            if class_id in VEHICLE_CLASSES:
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                current_boxes.append({
                    "box": [x1, y1, x2, y2],
                    "type": VEHICLE_CLASSES[class_id]
                })

        # Match current detections to existing tracked vehicles (simple centroid distance matching)
        for detection in current_boxes:
            centroid = get_centroid(detection["box"])
            matched_id = _match_to_existing(centroid, tracked_vehicles)

            if matched_id is None:
                # New vehicle detected — assign a new ID
                matched_id = next_id
                next_id += 1
                tracked_vehicles[matched_id] = {
                    "type": detection["type"],
                    "positions": [],       # list of (frame_number, centroid_y)
                    "line1_time": None,
                    "line2_time": None,
                    "speed": 0,
                    "accident_detected": False,
                    "last_centroid": centroid
                }

            vehicle = tracked_vehicles[matched_id]
            vehicle["positions"].append((frame_count, centroid[1]))
            vehicle["last_centroid"] = centroid

            # --- Speed calculation: check if vehicle crossed the two reference lines ---
            if vehicle["line1_time"] is None and centroid[1] >= LINE_1_Y:
                vehicle["line1_time"] = frame_count / fps

            if vehicle["line2_time"] is None and centroid[1] >= LINE_2_Y:
                vehicle["line2_time"] = frame_count / fps

                # Both lines crossed -> calculate speed
                if vehicle["line1_time"] is not None:
                    time_taken = vehicle["line2_time"] - vehicle["line1_time"]
                    if time_taken > 0:
                        # speed = distance / time, converted to km/h
                        speed_mps = distance_between_lines / time_taken
                        vehicle["speed"] = round(speed_mps * 3.6, 2)  # m/s -> km/h

            # --- Simple accident detection ---
            vehicle["accident_detected"] = _check_accident(vehicle)

        # Safety cap: stop processing very long videos (demo purposes)
        if frame_count > MAX_FRAMES:
            break

    cap.release()

    # Build final result list
    final_results = []
    for vehicle_id, data in tracked_vehicles.items():
        final_results.append({
            "vehicle_id": vehicle_id,
            "vehicle_type": data["type"],
            "speed": data["speed"],
            "is_overspeed": data["speed"] > speed_limit,
            "accident_detected": data["accident_detected"]
        })

    return final_results


def _match_to_existing(centroid, tracked_vehicles, max_distance=80):
    """
    Matches a new detection's centroid to an existing tracked vehicle
    if it's within max_distance pixels of that vehicle's last known position.
    This is a very simple tracking method (good enough for a demo project).
    """
    for vehicle_id, data in tracked_vehicles.items():
        last_x, last_y = data["last_centroid"]
        distance = ((centroid[0] - last_x) ** 2 + (centroid[1] - last_y) ** 2) ** 0.5
        if distance < max_distance:
            return vehicle_id
    return None


def _check_accident(vehicle):
    """
    Simple rule-based accident detection:
    - Looks at the vehicle's recent Y-position movement.
    - If it was moving fast and then suddenly stops (very little movement
      over several recent frames), we flag it as a possible accident.
    """
    positions = vehicle["positions"]

    # Need at least 10 frames of history to judge "sudden stop"
    if len(positions) < 10:
        return vehicle["accident_detected"]

    recent = positions[-10:]

    # Movement in the first half vs the second half of this recent window
    early_movement = abs(recent[4][1] - recent[0][1])
    late_movement = abs(recent[9][1] - recent[5][1])

    # Was moving significantly, then suddenly almost stopped -> possible accident
    if early_movement > 15 and late_movement < 3:
        return True

    return vehicle["accident_detected"]
