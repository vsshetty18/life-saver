"""
Location Utilities
Provides distance calculation to find the nearest hospital/police station
from a given latitude/longitude using the Haversine formula.
"""

from math import radians, sin, cos, sqrt, atan2


def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculates the distance (in km) between two GPS coordinates
    using the Haversine formula — accounts for Earth's curvature.
    """
    R = 6371  # Earth's radius in kilometers

    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c  # distance in km


def find_nearest(model_class, latitude, longitude):
    """
    Finds the nearest record (Hospital or PoliceStation) to a given location.

    model_class: the SQLAlchemy model to search (Hospital or PoliceStation)
    latitude, longitude: the accident location

    Returns the closest matching record, or None if the table is empty.
    """
    all_records = model_class.query.all()

    if not all_records:
        return None

    nearest_record = None
    shortest_distance = float("inf")

    for record in all_records:
        distance = haversine_distance(
            latitude, longitude,
            record.latitude, record.longitude
        )
        if distance < shortest_distance:
            shortest_distance = distance
            nearest_record = record

    return nearest_record
