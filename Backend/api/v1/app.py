#!/usr/bin/python3
"""
    This module is the entry point for the TimeWise API. It initializes and configures
    the Flask application, sets up the database, and registers app_views.
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from api.v1.config import config_dict
from api.v1.views import app_views
from models.base_model import db
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def create_app(config_name="development"):
    """Initialize the Flask app."""
    app = Flask(__name__)
    app.config.from_object(config_dict[config_name])

    # Enable CORS
    # CORS(app, resources={r'/api/v1/*': {'origins': '*'}})
    CORS(app)

    # Initialize database
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    app.register_blueprint(app_views)

    @app.route("/")
    def home():
        return {"message": "Welcome to TimeWise API!"}, 200

    return app


if __name__ == "__main__":
    app = create_app()
    # Run the api
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port, debug=True)
