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
from flasgger import swag_from


task_bp = Blueprint('task', __name__)


@task_bp.route('/tasks', methods=['GET'])
@jwt_required()
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get all tasks',
    'description': 'Get all tasks for the current user.',
    'responses': {
        200: {
            'description': 'List of tasks',
            'examples': {'application/json': [
                {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}
            ]}
        },
        404: {
            'description': 'User not found',
            'examples': {'application/json': {'error': 'User not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get task by ID',
    'description': 'Get a specific task by ID.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Task found',
            'examples': {'application/json': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Create task',
    'description': 'Create a new task for the current user.',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string', 'description': 'Task title'},
                    'description': {'type': 'string', 'description': 'Task description'}
                },
                'required': ['title', 'description']
            }
        }
    ],
    'responses': {
        201: {
            'description': 'Task created',
            'examples': {'application/json': {'message': 'Task created successfully', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        400: {
            'description': 'Missing required field',
            'examples': {'application/json': {'error': 'Missing required field: title'}}
        },
        404: {
            'description': 'User not found',
            'examples': {'application/json': {'error': 'User not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Update task',
    'description': 'Update a specific task by ID.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'title': {'type': 'string'},
                    'description': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Task updated',
            'examples': {'application/json': {'message': 'Task updated successfully', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Delete task',
    'description': 'Delete a specific task by ID.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Task deleted',
            'examples': {'application/json': {'message': 'Task deleted successfully'}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Complete task',
    'description': 'Mark a task as completed.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Task marked as completed',
            'examples': {'application/json': {'message': 'Task marked as completed', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Uncomplete task',
    'description': 'Mark a task as uncompleted.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Task marked as uncompleted',
            'examples': {'application/json': {'message': 'Task marked as uncompleted', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Update task progress',
    'description': 'Update the progress of a task.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Task progress updated',
            'examples': {'application/json': {'message': 'Task progress updated successfully', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        400: {
            'description': 'Missing required field',
            'examples': {'application/json': {'error': 'Missing required field: progress'}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Get task analytics',
    'description': 'Get analytics for a specific task.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'}
    ],
    'responses': {
        200: {
            'description': 'Analytics data',
            'examples': {'application/json': {'total_time_spent': '1 hour', 'progress': 50, 'completed': True}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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
@swag_from({
    'tags': ['Tasks'],
    'summary': 'Update task analytics',
    'description': 'Update analytics for a specific task.',
    'parameters': [
        {'name': 'task_id', 'in': 'path', 'type': 'integer', 'required': True, 'description': 'Task ID'},
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'total_time_spent': {'type': 'string', 'description': 'Total time spent on the task'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Analytics updated',
            'examples': {'application/json': {'message': 'Task analytics updated successfully', 'task': {'id': 1, 'title': 'Task 1', 'description': 'Desc', 'user_id': 'uuid'}}}
        },
        404: {
            'description': 'Task or user not found',
            'examples': {'application/json': {'error': 'Task not found'}}
        }
    }
})
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