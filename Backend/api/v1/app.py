#!/usr/bin/python3
"""
    This module is the entry point for the TimeWise API. It initializes and configures
    the Flask application, sets up the database, and registers app_views.
"""
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_mail import Mail
from sqlalchemy import text
from api.v1.config import config_dict
from api.v1.views.auth import auth_bp
from api.v1.views.tasks import task_bp
from api.v1.views.progress import progress_bp
from api.v1.views.users import user_bp
from api.v1.views.analytics import analytics_bp
from models.base_model import db
from os import getenv
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager

load_dotenv()


def create_app(config_name="development"):
    """Initialize the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # Enable CORS
    CORS(app)

    # Initialize database
    db.init_app(app)
    with app.app_context():
        db.create_all()  # Create tables

    # Initialize JWTManager
    jwt = JWTManager(app)

    # Initialize Flask-Mail
    mail = Mail(app)

    # Register blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/v1/auth")
    app.register_blueprint(user_bp, url_prefix="/api/v1/user")
    app.register_blueprint(task_bp, url_prefix="/api/v1/task")
    app.register_blueprint(progress_bp, url_prefix="/api/v1/progress")
    app.register_blueprint(analytics_bp, url_prefix="/api/v1/analytics")
    
    @app.route('/api/v1/health', methods=["GET"])
    def health_check():
        """Check the health of the API."""
        try:
            db.session.execute(text('SELECT 1'))
            database_status = 'connected'
        except Exception as e:
            print(e)
            database_status = 'disconnected'
        
        return jsonify(
            status='healthy',
            version='1.0.0',
            database=database_status
        )

    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        """Return a custom 404 error."""
        return jsonify({'error': 'Not found'}), 404

    @app.errorhandler(500)
    def server_error(error):
        """Return a custom 500 error."""
        return jsonify({'error': 'Internal server error'}), 500

    @app.route("/")
    def home():
        return {"message": "Welcome to TimeWise API!"}, 200
    return app


if __name__ == "__main__":
    # Run the api
    app = create_app()
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=getenv("FLASK_ENV") == 'development')
