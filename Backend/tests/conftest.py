#!/usr/bin/env python3
"""
    This module contains fixtures and test setup
"""

import pytest
import uuid
from api.v1.app import create_app
from models.base_model import db
from models.user import User, UserRole
from models.task import Task
from models.progress import Progress
from sqlalchemy.orm import configure_mappers
configure_mappers()


@pytest.fixture(scope='module')
def test_app():
    """Create and configure a new app instance for each test module."""
    app = create_app(config_name="testing")
    # Establish an application context
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def test_client(test_app):
    """A test client for the app."""
    return test_app.test_client()

@pytest.fixture(scope='function')
def db_session(test_app):
    """Provides a database session for tests with automatic cleanup."""
    with test_app.app_context():
        yield db.session
        db.session.rollback()

@pytest.fixture(scope='function')
def new_user(db_session):
    """Create a test user and add to session with unique email/username."""
    unique_id = uuid.uuid4().hex
    user = User(
        name="Test User",
        username=f"testuser_{unique_id}",
        email=f"test_{unique_id}@example.com"
    )
    user.set_password("password123")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(scope='function')
def another_user(db_session):
    """Create another test user with unique email/username."""
    unique_id = uuid.uuid4().hex
    user = User(
        name="Another User",
        username=f"anotheruser_{unique_id}",
        email=f"another_{unique_id}@example.com"
    )
    user.set_password("password456")
    db_session.add(user)
    db_session.commit()
    return user

@pytest.fixture(scope='function')
def admin_user(db_session):
    """Creates an admin user and adds to session with unique email/username."""
    unique_id = uuid.uuid4().hex
    admin = User(
        name="Admin User",
        username=f"adminuser_{unique_id}",
        email=f"admin_{unique_id}@example.com",
        role=UserRole.ADMIN
    )
    admin.set_password("adminpass")
    db_session.add(admin)
    db_session.commit()
    return admin

# Helper Function
def get_auth_token(test_client, email, password):
    """Logs in a user and returns the access token."""
    login_data = {'email': email, 'password': password}
    response = test_client.post('/api/v1/auth/login', json=login_data)
    if response.status_code != 200:
        print(f"Login failed during token fetch: {response.get_data(as_text=True)}")
        return None # Return None on failure
    data = response.get_json()
    return data.get('access_token')

@pytest.fixture(scope='function')
def auth_headers(test_client, new_user):
    """Provides authorization headers for the default test user."""
    token = get_auth_token(test_client, new_user.email, "password123")
    if not token:
         pytest.fail("Failed to get auth token for default user")
    return {'Authorization': f'Bearer {token}'}

@pytest.fixture(scope='function')
def admin_auth_headers(test_client, admin_user):
    """Provides authorization headers for the admin user."""
    token = get_auth_token(test_client, admin_user.email, "adminpass")
    if not token:
         pytest.fail("Failed to get auth token for admin user")
    return {'Authorization': f'Bearer {token}'}