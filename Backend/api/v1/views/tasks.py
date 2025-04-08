#!/usr/bin/env python3
"""
    This Module contains the api endpoints for the task
"""
from flask import Flask, abort, request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from models.task import Task
from datetime import datetime


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """Get all tasks for the current user."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    tasks = user.tasks
    return jsonify([task.to_json() for task in tasks]), 200


@task_bp.route('/tasks/<int:task_id>', methods=['GET'])
@jwt_required()
def get_task(task_id):
    """Get a specific task by ID."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    return jsonify(task.to_json()), 200


@task_bp.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """Create a new task."""
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate required fields
    required_fields = ['title', 'description']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    task = Task(
        title=data['title'],
        description=data['description'],
        user_id=user.id
    )

    # Save to database
    task.new(task)
    task.save()
    return jsonify({
        'message': 'Task created successfully',
        'task': task.to_json()
    }), 201


@task_bp.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """Update a specific task by ID."""
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Update task fields
    for key, value in data.items():
        if hasattr(task, key):
            setattr(task, key, value)

    # Save to database
    task.save()
    return jsonify({
        'message': 'Task updated successfully',
        'task': task.to_json()
    }), 200


@task_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """Delete a specific task by ID."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Delete task
    task.delete()
    return jsonify({'message': 'Task deleted successfully'}), 200


@task_bp.route('/tasks/<int:task_id>/complete', methods=['POST'])
@jwt_required()
def complete_task(task_id):
    """Mark a task as completed."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.completed = True
    task.save()
    return jsonify({
        'message': 'Task marked as completed',
        'task': task.to_json()
    }), 200


@task_bp.route('/tasks/<int:task_id>/uncomplete', methods=['POST'])
@jwt_required()
def uncomplete_task(task_id):
    """Mark a task as uncompleted."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    task.completed = False
    task.save()
    return jsonify({
        'message': 'Task marked as uncompleted',
        'task': task.to_json()
    }), 200


@task_bp.route('/tasks/<int:task_id>/progress', methods=['POST'])
@jwt_required()
def update_task_progress(task_id):
    """Update the progress of a task."""
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Validate required fields
    required_fields = ['progress']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    task.progress = data['progress']
    task.save()
    return jsonify({
        'message': 'Task progress updated successfully',
        'task': task.to_json()
    }), 200

@task_bp.route('/tasks/<int:task_id>/analytics', methods=['GET'])
@jwt_required()
def get_task_analytics(task_id):
    """Get analytics for a specific task."""
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Example analytics data
    analytics_data = {
        'total_time_spent': str(task.total_time_spent),
        'progress': task.progress,
        'completed': task.completed
    }

    return jsonify(analytics_data), 200


@task_bp.route('/tasks/<int:task_id>/analytics', methods=['POST'])
@jwt_required()
def update_task_analytics(task_id):
    """Update analytics for a specific task."""
    data = request.get_json()
    current_user = get_jwt_identity()
    user = User.get(id=current_user)
    if not user:
        return jsonify({"error": "User not found"}), 404

    task = user.tasks.filter_by(id=task_id).first()
    if not task:
        return jsonify({"error": "Task not found"}), 404

    # Update analytics data
    if 'total_time_spent' in data:
        task.total_time_spent = data['total_time_spent']
    
    task.save()
    return jsonify({
        'message': 'Task analytics updated successfully',
        'task': task.to_json()
    }), 200