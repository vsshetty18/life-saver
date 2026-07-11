"""
Main Flask Application
This is the entry point of the backend server.
It creates the Flask app, connects the database, and registers all API routes.
"""

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
    import os
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    # Create all database tables (if they don't already exist)
    with app.app_context():
        db.create_all()

    # ---- Register Blueprints (API routes) ----
    # These will be created in upcoming files
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
        """Simple route to check if the server is running."""
        return {"status": "OK", "message": "Vehicle Speed Detection API is running"}

    return app


# Create the app instance
app = create_app()

if __name__ == "__main__":
    # debug=True gives auto-reload + detailed errors during development
    app.run(debug=True, port=5000)
