"""
Main Flask Application
This is the entry point of the backend server.
It creates the Flask app, connects the database, and registers all API routes.
"""

import os
from flask import Flask
from flask_cors import CORS
from config import Config
from models import db


def create_app():
    """
    Factory function to create and configure the Flask app.
    Using a factory pattern keeps things clean and testable.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Allow the React frontend (running on a different port/domain) to call this API
    CORS(app)

    # Connect SQLAlchemy to this Flask app
    db.init_app(app)

    # Create the uploads folder if it doesn't exist
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Create the database folder if it doesn't exist.
    # SQLite needs this directory to already be present before it can
    # create the .db file inside it — this is what was missing on Render.
    db_uri = app.config["SQLALCHEMY_DATABASE_URI"]
    if db_uri.startswith("sqlite:///"):
        db_path = db_uri.replace("sqlite:///", "", 1)
        db_dir = os.path.dirname(db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)

    # Create all database tables (if they don't already exist)
    with app.app_context():
        db.create_all()

    # ---- Register Blueprints (API routes) ----
    from routes.vehicle_routes import vehicle_bp
    from routes.alert_routes import alert_bp
    from routes.fastag_routes import fastag_bp
    from routes.dashboard_routes import dashboard_bp

    app.register_blueprint(vehicle_bp, url_prefix="/api/vehicle")
    app.register_blueprint(alert_bp, url_prefix="/api/alert")
    app.register_blueprint(fastag_bp, url_prefix="/api/fastag")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    @app.route("/")
    def health_check():
        """Simple route to check if the server is running. Render also
        uses this for its default health check ping."""
        return {"status": "OK", "message": "Vehicle Speed Detection API is running"}

    return app


# Create the app instance — this is what gunicorn imports as "app:app"
app = create_app()

if __name__ == "__main__":
    # Local dev only. In production, gunicorn (see Dockerfile CMD) runs this instead,
    # binding to Render's dynamic $PORT.
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
