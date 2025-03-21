#!/usr/bin/env python3
"""
    This module contains fixtures and test setup
"""

import pytest
from api.v1.app import create_app
from models.base_model import db
from models.user import User
from models.task import Task
from models.progress import Progress
from sqlalchemy.orm import configure_mappers
configure_mappers()


@pytest.fixture
def test_client():
    """Set up a Flask test client with a test database."""
    app = create_app(config_name="testing")
    client = app.test_client()

    with app.app_context():
        db.create_all()  # Create tables before tests run
        yield client
        db.session.remove()
        db.drop_all()  # Drop tables after tests

@pytest.fixture
def new_user():
    """Create a test user."""
    user = User(name="Test User", username="testuser", email="test@example.com")
    user.set_password("password123")
    return user