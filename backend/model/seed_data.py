"""
Seed Data Script
=================
Populates the database with sample data so the app has something
to demo immediately — no need to manually create records via API calls.

Run this ONCE after the database is created:
    python model/seed_data.py

Adds:
- Sample hospitals
- Sample police stations
- Sample vehicles + owners
- Sample FASTag toll history
"""

import sys
import os

# Allow this script to import from the parent backend/ folder
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from models import db, Hospital, PoliceStation, Owner, Vehicle, FastagHistory


def seed_hospitals():
    """Adds sample hospitals around Bengaluru (simulated data)."""
    hospitals = [
        Hospital(name="Victoria Hospital", latitude=12.9634, longitude=77.5771, phone_number="08026700447"),
        Hospital(name="Manipal Hospital", latitude=12.9581, longitude=77.6484, phone_number="08025023456"),
        Hospital(name="Fortis Hospital Bannerghatta", latitude=12.8916, longitude=77.5963, phone_number="08066214444"),
        Hospital(name="St. John's Medical College Hospital", latitude=12.9279, longitude=77.6271, phone_number="08022065000"),
        Hospital(name="Apollo Hospital Bannerghatta", latitude=12.9089, longitude=77.5973, phone_number="08026304050"),
    ]
    db.session.bulk_save_objects(hospitals)
    print(f"Added {len(hospitals)} hospitals.")


def seed_police_stations():
    """Adds sample police stations around Bengaluru (simulated data)."""
    stations = [
        PoliceStation(name="Koramangala Police Station", latitude=12.9352, longitude=77.6245, phone_number="08025531164"),
        PoliceStation(name="Indiranagar Police Station", latitude=12.9719, longitude=77.6412, phone_number="08025203020"),
        PoliceStation(name="Jayanagar Police Station", latitude=12.9250, longitude=77.5938, phone_number="08026630480"),
        PoliceStation(name="Whitefield Police Station", latitude=12.9698, longitude=77.7500, phone_number="08028452500"),
        PoliceStation(name="Rajarajeshwari Nagar Police Station", latitude=12.9260, longitude=77.5180, phone_number="08028602100"),
    ]
    db.session.bulk_save_objects(stations)
    print(f"Added {len(stations)} police stations.")


def seed_vehicles():
    """Adds a couple of sample owners + vehicles for demo purposes."""
    owner1 = Owner(name="Ramesh Kumar", phone_number="+919900000001", email="ramesh@example.com")
    owner2 = Owner(name="Suresh Rao", phone_number="+919900000002", email="suresh@example.com")

    db.session.add(owner1)
    db.session.add(owner2)
    db.session.flush()  # get their IDs before creating vehicles

    vehicle1 = Vehicle(
        vehicle_number="KA01AB1234",
        vehicle_type="car",
        owner_id=owner1.id,
        helper1_phone="+919900000003",
        helper2_phone="+919900000004"
    )
    vehicle2 = Vehicle(
        vehicle_number="KA05CD5678",
        vehicle_type="bike",
        owner_id=owner2.id,
        helper1_phone="+919900000005",
        helper2_phone="+919900000006"
    )

    db.session.add(vehicle1)
    db.session.add(vehicle2)
    print("Added 2 sample vehicles with owners.")


def seed_fastag_history():
    """Adds sample toll crossing history for the demo vehicle."""
    history = [
        FastagHistory(vehicle_number="KA01AB1234", toll_name="Nelamangala Toll Plaza", city="Bengaluru"),
        FastagHistory(vehicle_number="KA01AB1234", toll_name="Bidadi Toll Plaza", city="Ramanagara"),
        FastagHistory(vehicle_number="KA01AB1234", toll_name="Maddur Toll Plaza", city="Mandya"),
        FastagHistory(vehicle_number="KA01AB1234", toll_name="Kunigal Toll Plaza", city="Tumkur"),
        FastagHistory(vehicle_number="KA01AB1234", toll_name="Hoskote Toll Plaza", city="Bengaluru"),
    ]
    db.session.bulk_save_objects(history)
    print(f"Added {len(history)} FASTag history records.")


def run_seed():
    """Main entry point — creates app context and runs all seed functions."""
    app = create_app()

    with app.app_context():
        # Avoid duplicate seeding if script is run more than once
        if Hospital.query.count() > 0:
            print("Database already seeded. Skipping.")
            return

        seed_hospitals()
        seed_police_stations()
        seed_vehicles()
        seed_fastag_history()

        db.session.commit()
        print("✅
