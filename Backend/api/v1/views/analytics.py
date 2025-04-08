#!/usr/bin/python3
"""
    This Module contains the Analytics API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from datetime import datetime
import uuid
from models.analytics import Analytics
from models.task import Task

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_user_analytics():
    """Retrieve analytics for the current user."""
    user_id = get_jwt_identity()
    user = User.get(id=user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Calculate analytics
    total_tasks = len(user.tasks)
    completed_tasks = len([task for task in user.tasks if task.completed])
    total_time_spent = sum(
        (task.total_time_spent for task in user.tasks if task.total_time_spent), 
        datetime.timedelta()
    )

    analytics_data = {
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'total_time_spent': str(total_time_spent)
    }

    return jsonify(analytics_data), 200
