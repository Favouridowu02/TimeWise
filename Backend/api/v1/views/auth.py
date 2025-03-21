#!/usr/bin/python3
"""
    This Module contains the authentication API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models import db, User, UserSettings
from datetime import datetime
import uuid

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['email', 'password', 'name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'User with this email already exists'}), 409

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=data['email'],
        name=data['name']
    )
    user.set_password(data['password'])

    # Create default user settings
    settings = UserSettings(
        id=str(uuid.uuid4()),
        user_id=user.id
    )

    # Save to database
    db.session.add(user)
    db.session.add(settings)
    db.session.commit()

    # Generate access token
    access_token = create_access_token(identity=user.id)

    return jsonify({
        'message': 'User registered successfully',
        'access_token': access_token,
        'user': user.to_dict()
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate required fields
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({'error': 'Email and password are required'}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()

    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    # Generate access token
    access_token = create_access_token(identity=user.id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'user': user.to_dict()
    }), 200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_dict()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    
    # Update user fields
    updatable_fields = ['name', 'timezone', 'language', 'profile_image', 'bio']
    for field in updatable_fields:
        if field in data:
            setattr(user, field, data[field])
    
    # Update password if provided
    if 'current_password' in data and 'new_password' in data:
        if not user.check_password(data['current_password']):
            return jsonify({'error': 'Current password is incorrect'}), 400
        user.set_password(data['new_password'])
    
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Profile updated successfully',
        'user': user.to_dict()
    }), 200

@auth_bp.route('/settings', methods=['GET'])
@jwt_required()
def get_settings():
    user_id = get_jwt_identity()
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        # Create default settings if not found
        settings = UserSettings(
            id=str(uuid.uuid4()),
            user_id=user_id
        )
        db.session.add(settings)
        db.session.commit()
    
    return jsonify(settings.to_dict()), 200

@auth_bp.route('/settings', methods=['PUT'])
@jwt_required()
def update_settings():
    user_id = get_jwt_identity()
    settings = UserSettings.query.filter_by(user_id=user_id).first()
    
    if not settings:
        return jsonify({'error': 'Settings not found'}), 404
    
    data = request.get_json()
    
    # Update settings fields
    updatable_fields = [
        'theme', 'font_size', 'enable_animations', 'reduce_motion',
        'compact_sidebar', 'sticky_header', 'email_notifications',
        'push_notifications', 'task_reminder_frequency', 'weekly_summary_day',
        'do_not_disturb', 'dnd_start_time', 'dnd_end_time'
    ]
    
    for field in updatable_fields:
        if field in data:
            setattr(settings, field, data[field])
    
    settings.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({
        'message': 'Settings updated successfully',
        'settings': settings.to_dict()
    }), 200
