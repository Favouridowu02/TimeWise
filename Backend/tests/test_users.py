#!/usr/bin/env python3
"""
    This module contains the test for the User model
"""
from models.user import User
from models.base_model import db


def test_user_creation(test_client, new_user):
    """Test if a new user can be added to the database."""
    db.session.add(new_user)
    db.session.commit()

    retrieved_user = User.query.filter_by(username="testuser").first()
    assert retrieved_user is not None
    assert retrieved_user.check_password("password123") is True
