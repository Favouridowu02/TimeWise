#!/usr/bin/env python3
"""
    This Module contains the Decorators that are used for the API
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended.exceptions import JWTDecodeError, NoAuthorizationError
from models.user import User, UserRole
import logging
import uuid

def admin_required(fn):
    """
    Decorator to ensure the user has the 'admin' role.
    Handles JWT and database errors gracefully.
    """
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verify JWT is present and valid
            verify_jwt_in_request()
            user_id = get_jwt_identity()
        except NoAuthorizationError:
            logging.warning("Admin access denied: No JWT provided.")
            return jsonify(msg="Authorization token required."), 401
        except JWTDecodeError:
            logging.warning("Admin access denied: Invalid JWT.")
            return jsonify(msg="Invalid or malformed token."), 401
        except Exception as e:
            logging.error(f"Unexpected JWT verification error: {str(e)}")
            return jsonify(msg="Authentication error."), 500

        try:
            # Retrieve user from database
            user_id = uuid.UUID(user_id)
            user = User.get(id=user_id)
            if not user:
                logging.warning(f"Admin access denied: User {user_id} not found.")
                return jsonify(msg="Admin access required."), 403
        except Exception as e:
            logging.error(f"Database error while fetching user {user_id}: {str(e)}")
            return jsonify(msg="Error accessing user data."), 500

        # Check if user has admin role
        if user.role != UserRole.ADMIN:
            logging.warning(f"Admin access denied for user {user_id} (Role: {user.role}).")
            return jsonify(msg="Admin access required."), 403

        return fn(*args, **kwargs)
    return wrapper