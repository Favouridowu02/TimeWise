#!/usr/bin/python3
"""
    This Module contains the Progress API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from datetime import datetime
import uuid

progress_bp = Blueprint('progress', __name__)


@progress_bp.route('/progress', methods=['POST'])
@jwt_required()
def create_progress():
    """
        Create a new progress entry for the authenticated user.
    """
    user_id = get_jwt_identity()
    data = request.get_json()

    if not data or 'description' not in data or 'status' not in data:
        return jsonify({"error": "Invalid input"}), 400

    try:
        new_progress = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "description": data['description'],
            "status": data['status'],
            "created_at": datetime.utcnow()
        }
        db['progress'].append(new_progress)  # Assuming db['progress'] is a list for simplicity
        return jsonify(new_progress), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@progress_bp.route('/progress', methods=['GET'])
@jwt_required()
def get_progress():
    """
    Retrieve all progress entries for the authenticated user.
    """
    user_id = get_jwt_identity()
    try:
        user_progress = [p for p in db['progress'] if p['user_id'] == user_id]
        return jsonify(user_progress), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500