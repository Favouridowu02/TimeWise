#!/usr/bin/env python3
"""
    This Module contains the api endpoints for managing users, primarily for administrative purposes.
"""
from flask import Flask, abort, request, jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User, UserRole
from datetime import datetime
import uuid
import logging
from utils.decorators import admin_required # Import the decorator

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@jwt_required()
@admin_required
def get_all_users():
    """Retrieve a List of all users (Admin only)."""
    # RBAC check is now handled by the decorator
    current_user_id = get_jwt_identity()

    logging.info(f"User {current_user_id} attempting to list all users.")
    
    try:
        users = User.all()
        return jsonify([user.to_json() for user in users]), 200
    except Exception as e:
        logging.error(f"Error listing users: {e}")
        return jsonify({'error': 'Failed to retrieve users'}), 500

@admin_bp.route('/users/<uuid:user_id>', methods=['GET'])
@jwt_required()
@admin_required # Apply the decorator
def get_user_by_id(user_id):
    """Get a specific user by ID (Admin only)."""
    # RBAC check is now handled by the decorator
    current_user_id = get_jwt_identity()
    logging.info(f"User {current_user_id} attempting to get user {user_id}.")

    user = User.get(id=user_id)
    if not user:
        logging.warning(f"User {user_id} not found.")
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_json()), 200

@admin_bp.route('/users/<uuid:user_id>', methods=['PUT'])
@jwt_required()
@admin_required # Apply the decorator
def update_user_by_id(user_id):
    """Update a specific user by ID (Admin only)."""
    # RBAC check is now handled by the decorator
    current_user_id = get_jwt_identity()
    logging.info(f"User {current_user_id} attempting to update user {user_id}.")

    user = User.get(id=user_id)
    if not user:
        logging.warning(f"User {user_id} not found for update.")
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    # Fields that an admin might update (excluding password for now)
    updatable_fields = ['name', 'username', 'email', 'timezone', 'language', 'profile_image', 'bio', 'email_verified']
    
    try:
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.updated_at = datetime.utcnow()
        user.save()
        logging.info(f"User {user_id} updated successfully by {current_user_id}.")
        return jsonify(user.to_json()), 200
    except Exception as e:
        logging.error(f"Error updating user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to update user'}), 500

@admin_bp.route('/users/<uuid:user_id>', methods=['DELETE'])
@jwt_required()
@admin_required # Apply the decorator
def delete_user_by_id(user_id):
    """Delete a specific user by ID (Admin only)."""
    # RBAC check is now handled by the decorator
    current_user_id = get_jwt_identity()
    logging.info(f"User {current_user_id} attempting to delete user {user_id}.")

    user = User.get(id=user_id)
    if not user:
        logging.warning(f"User {user_id} not found for deletion.")
        return jsonify({'error': 'User not found'}), 404

    # Prevent self-deletion? (Optional check)
    # if str(user_id) == str(current_user_id):
    #     return jsonify({'error': 'Cannot delete your own account via this endpoint'}), 403

    try:
        user.delete()
        logging.info(f"User {user_id} deleted successfully by {current_user_id}.")
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        logging.error(f"Error deleting user {user_id}: {e}")
        db.session.rollback()
        return jsonify({'error': 'Failed to delete user'}), 500


@admin_bp.route('/users/<uuid:user_id>/role', methods=['PUT'])
@jwt_required()
@admin_required
def update_user_role(user_id):
    """
    [Admin] Update the role of a specific user.
    """
    data = request.get_json()
    if not data or 'role' not in data:
        return jsonify({"error": "Missing 'role' in request body"}), 400

    new_role_str = data['role'].upper()
    try:
        # Validate the role string against the UserRole enum
        new_role = UserRole[new_role_str]
    except KeyError:
        valid_roles = [role.name for role in UserRole]
        return jsonify({"error": f"Invalid role. Valid roles are: {valid_roles}"}), 400

    try:
        user = User.query.get(str(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.role = new_role
        db.session.commit()

        return jsonify({"message": f"User {user.username}'s role updated to {new_role.value}"}), 200
    except Exception as e:
        db.session.rollback()
        # Log the error e
        return jsonify({"error": "Failed to update user role", "details": str(e)}), 500