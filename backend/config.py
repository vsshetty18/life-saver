"""
Configuration file for the Flask backend.
Loads settings from the .env file so we never hardcode secrets in code.
"""

import os
from dotenv import load_dotenv

# Load variables from .env file into the environment
load_dotenv()

# Absolute path to the backend/ folder (where this file lives).
# Using an absolute path (instead of a relative "database/app.db") avoids
# "unable to open database file" errors caused by the container's working
# directory not matching where we expect it to be.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_DIR = os.path.join(BASE_DIR, "database")
DEFAULT_DB_PATH = os.path.join(DATABASE_DIR, "app.db")


def _int_env(key, default):
    """
    Safely reads an integer environment variable.
    Falls back to `default` if the variable is missing OR blank/empty —
    plain os.getenv(key, default) only falls back when the variable is
    completely unset, not when it exists but is an empty string.
    """
    value = os.getenv(key)
    if value is None or value.strip() == "":
        return default
    return int(value)


def _float_env(key, default):
    """Same idea as _int_env, but for float values."""
    value = os.getenv(key)
    if value is None or value.strip() == "":
        return default
    return float(value)


class Config:
    """
    Central place for all app settings.
    Flask will read these values when the app starts.
    """

    # Secret key used by Flask for sessions/security
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_key")

    # SQLite database file location.
    # Falls back to an absolute path under backend/database/app.db so it
    # works the same whether run locally, in Docker, or on Render.
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # turn off unnecessary overhead

    # Twilio credentials (for SMS alerts)
    TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
    TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
    TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

    # Email (SMTP) credentials
    SMTP_SERVER = os.getenv("SMTP_SERVER")
    SMTP_PORT = _int_env("SMTP_PORT", 587)
    SMTP_EMAIL = os.getenv("SMTP_EMAIL")
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

    # Speed detection settings
    SPEED_LIMIT = _int_env("SPEED_LIMIT", 60)  # km/h
    DISTANCE_BETWEEN_LINES = _float_env("DISTANCE_BETWEEN_LINES", 10)  # meters

    # Folder where uploaded videos are stored
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
    ALLOWED_EXTENSIONS = {"mp4", "avi", "mov"}
