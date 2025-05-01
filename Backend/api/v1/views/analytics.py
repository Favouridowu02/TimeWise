#!/usr/bin/python3
"""
    This Module contains the Analytics API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from datetime import datetime, timedelta
import uuid
from models.analytics import Analytics
from models.task import Task
import logging 


analytics_bp = Blueprint('analytics', __name__)
logger = logging.getLogger(__name__)

@analytics_bp.route('/analytics', methods=['GET'])
@jwt_required()
def get_user_analytics():
    """Retrieve analytics for the current user."""
    user_id = get_jwt_identity()
    logger.info(f"Attempting to retrieve analytics for user {user_id}")
    user = User.get(id=user_id)

    if not user:
        logger.warning(f"User {user_id} not found for analytics retrieval.")
        return jsonify({'error': 'User not found'}), 404

    try:
        # Calculate analytics
        total_tasks = len(user.tasks)
        completed_tasks = len([task for task in user.tasks if task.completed])
        
        total_time_spent_sum = timedelta()
        for task in user.tasks:
            if task.total_time_spent:
                total_time_spent_sum += task.total_time_spent

        analytics_data = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'total_time_spent': str(total_time_spent_sum) # Use the calculated sum
        }
        logger.info(f"Successfully retrieved analytics for user {user_id}")
        return jsonify(analytics_data), 200
    except Exception as e:
        logger.exception(f"Error calculating analytics for user {user_id}")
        return jsonify({'error': 'Failed to calculate analytics'}), 500

@analytics_bp.route('/analytics', methods=['POST'])
@jwt_required()
def create_user_analytics():
    """Create a new analytics entry for the current user."""
    user_id = get_jwt_identity()
    logger.info(f"Attempting to create analytics entry for user {user_id}")
    user = User.get(id=user_id)

    if not user:
        logger.warning(f"User {user_id} not found for creating analytics.")
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        logger.warning(f"Invalid input received for creating analytics for user {user_id}")
        return jsonify({'error': 'Invalid input'}), 400

    try:
        task_id = data.get('task_id')
        task = Task.get(id=task_id, user_id=user_id) 

        if not task:
            logger.warning(f"Task {task_id} not found or does not belong to user {user_id}")
            return jsonify({'error': 'Task not found'}), 404

        # Validate time_spent
        time_spent_data = data.get('time_spent') 
        # Convert time_spent_data to timedelta if it's not already
        time_spent_interval = timedelta(seconds=int(time_spent_data)) if time_spent_data else timedelta()


        analytics_entry = Analytics(
            user_id=user_id,
            task_id=task_id,
            total_time_spent=time_spent_interval
        )

        analytics_entry.new(analytics_entry)
        analytics_entry.save()

        logger.info(f"Analytics entry created successfully for user {user_id}, task {task_id}")
        return jsonify({'message': 'Analytics entry created successfully', 'analytics': analytics_entry.to_json()}), 201

    except Exception as e:
        logger.exception(f"Error creating analytics entry for user {user_id}")
        db.session.rollback() 
        return jsonify({'error': 'Failed to create analytics entry'}), 500