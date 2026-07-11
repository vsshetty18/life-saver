"""
Configuration file for the Flask backend.
Loads settings from the .env file so we never hardcode secrets in code.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()


class Config:
    """
    Central place for all app settings.
    Flask will read these values when the app starts.
    """

    # Secret key used by Flask for sessions/security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    # SQLite database file location
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "sqlite:///database/app.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # turn off unnecessary overhead

    # Twilio credentials (for SMS alerts)
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Email (SMTP) credentials
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = int(os.getenv("SMTP_PORT", 587))
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    # Speed detection settings
    SPEED_LIMIT = int(os.getenv("SPEED_LIMIT", 60))  # km/h
    DISTANCE_BETWEEN_LINES = float(os.getenv("DISTANCE_BETWEEN_LINES", 10))  # meters

    # Folder where uploaded videos are stored
    UPLOAD_FOLDER = os.path.join(os.getcwd(), "uploads")
    ALLOWED_EXTENSIONS = {"mp4", "avi", "mov"}
