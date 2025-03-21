import os
from dotenv import load_dotenv

# Loads environment variables from .env file
load_dotenv()


class Config:
    """ This Class contains the base configuration settings for the API."""

    # Security key
    SECRET_KEY = os.getenv("SECRET_KEY", "super_secret_key")

    # Database Configuration - When cloned Update this Database to your intended database
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", "postgresql://user:password@localhost/timewise"
    )

    # Track modifications
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Debug Mode
    DEBUG = os.getenv("FLASK_DEBUG", "False").lower() == "true"


class TestConfig(Config):
    """This Class is used for the configuration for testing mode."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"  # Use SQLite in-memory database for tests


class DevelopmentConfig(Config):
    """Configuration for development mode."""
    DEBUG = True


class ProductionConfig(Config):
    """Configuration for production mode."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")



# Dictionary to select configurations dynamically when imported
config_dict = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestConfig,
}