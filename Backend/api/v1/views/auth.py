#!/usr/bin/python3
"""
    This Module contains the authentication API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, decode_token
from models.base_model import db
from models.user import User
# from flask import current_app
from datetime import datetime
from datetime import timedelta
import uuid
from flask_jwt_extended import get_jwt, unset_jwt_cookies
from werkzeug.security import generate_password_hash
from datetime import datetime
from utils.email_utils import send_email
import logging

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    # Validate required fields
    required_fields = ['email', 'password', 'name', 'username']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    # Check if user already exists
    if User.get(email=data['email']):
        return jsonify({'error': 'User with this email already exists'}), 409

    # Check if user already exists
    if User.get(username=data['username']):
        return jsonify({'error': 'User with this username already exists'}), 409

    # Create new user
    user = User(
        email=data['email'],
        name=data['name'],
        username=data['username']
    )
    user.set_password(data['password'])

    try:
        # Save to database
        user.new(user)
        user.save()
        
        # Generate access token
        access_token = create_access_token(identity=user.id)

        logging.info(f"User registered successfully: {user.email}")
        return jsonify({
            'message': 'User registered successfully',
            'access_token': access_token,
            'user': user.to_json()
        }), 201
    except Exception as e:
        logging.error(f"Error during registration: {e}")
        return jsonify({'error': 'Registration failed'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate required fields
    if not data or 'password' not in data or ('email' not in data and 'username' not in data):
        return jsonify({'error': 'Username or email and password are required'}), 400

    # Find user by email or username
    user = None
    if 'email' in data:
        user = User.get(email=data['email'])
    elif 'username' in data:
        user = User.get(username=data['username'])

    # Check if user exists and password is correct
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid credentials'}), 401

    try:
        # Generate access token
        access_token = create_access_token(identity=user.id)
        
        logging.info(f"User logged in: {user.email}")
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user': user.to_json()
        }), 200
    except Exception as e:
        logging.error(f"Error during login: {e}")
        return jsonify({'error': 'Login failed'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Get the user's profile information."""
    user_id = get_jwt_identity()

    try:
        # convert user_id to UUID
        user_id = uuid.UUID(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID format'}), 400

    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify(user.to_json()), 200

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update the user's profile information."""
    user_id = get_jwt_identity()
    
    try:
        user_id = uuid.UUID(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID format'}), 400

    user = db.session.get(User, user_id)
    
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
    user.save()

    return jsonify(user.to_json()), 200


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Logout the user by invalidating the JWT token."""
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)  # Invalidate the current token by unsetting cookies
    return response, 200

@auth_bp.route('/logout', methods=['GET'])
def logout_status():
    """Check if the user is logged out."""
    return jsonify({"message": "Use POST to log out"}), 400


@auth_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_account():
    """Delete the user's account."""
    user_id = get_jwt_identity()

    try:
        user_id = uuid.UUID(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid user ID format'}), 400
    user = db.session.get(User, user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Delete user from database
    user.delete()
    
    return jsonify({'message': 'User account deleted successfully'}), 200

@auth_bp.route('/password-reset-request', methods=['POST'])
def password_reset_request():
    """Request a password reset token."""
    try:
        data = request.get_json()

        # Validate email
        if not data or 'email' not in data:
            logging.warning("Missing email in password reset request")
            return jsonify({'error': 'Email is required'}), 400

        # user = User.get(email=str(data['email']))
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            logging.info(f"No user found for email: {data['email']}")
            return jsonify({'error': 'User with this email does not exist'}), 404

        # Generate a password reset token (valid for 15 minutes)
        reset_token = create_access_token(
            identity=user.id,
            expires_delta=timedelta(minutes=15)
        )

        # In a real-world scenario, send this token to the user's email
        # For now, return it in the response for testing purposes
        logging.info(f"Password reset token generated for user: {data['email']}")
        return jsonify({
            'message': 'Password reset token generated successfully',
            'reset_token': reset_token
        }), 200
    except Exception as e:
        logging.error(f"Error processing password reset request: {str(e)}")
        return jsonify({"msg": "Internal server error"}), 500


@auth_bp.route('/password-reset', methods=['POST'])
def password_reset():
    """Reset the user's password using the reset token."""
    data = request.get_json()

    # Validate required fields
    required_fields = ['reset_token', 'new_password']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400

    try:
        # Decode the reset token
        decoded_token = decode_token(data['reset_token'])
        user_id = decoded_token.get('sub')
        if not user_id:
            return jsonify({'error': 'Invalid reset token'}), 400
        user_id = uuid.UUID(user_id)
    except Exception as e:
        return jsonify({'error': 'Invalid or expired reset token'}), 400

    # Find the user
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Update the user's password
    user.set_password(data['new_password'])
    user.save()

    return jsonify({'message': 'Password reset successfully'}), 200


@auth_bp.route('/email-verification-request', methods=['POST'])
@jwt_required()
def email_verification_request():
    """Request an email verification token."""
    user_id = get_jwt_identity()
    user = User.get(id=user_id)

    if not user:
        return jsonify({'error': 'User not found'}), 404

    if user.email_verified:
        return jsonify({'message': 'Email is already verified'}), 200

    # Generate an email verification token (valid for 1 hour)
    verification_token = create_access_token(
        identity=user.id,
        expires_delta=datetime.timedelta(hours=1)
    )

    # Send the verification token via email
    send_email(
        subject="Email Verification",
        recipients=[user.email],
        body=f"Use this token to verify your email: {verification_token}"
    )

    return jsonify({'message': 'Email verification token sent successfully'}), 200


@auth_bp.route('/email-verification', methods=['POST'])
def email_verification():
    """Verify the user's email using the verification token."""
    data = request.get_json()

    # Validate required fields
    if not data or 'verification_token' not in data:
        return jsonify({'error': 'Verification token is required'}), 400

    try:
        # Decode the verification token
        decoded_token = decode_token(data['verification_token'])
        user_id = decoded_token.get('sub')
        if not user_id:
            return jsonify({'error': 'Invalid verification token'}), 400
    except Exception as e:
        return jsonify({'error': 'Invalid or expired verification token'}), 400

    # Find the user
    user = User.get(id=user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    # Mark the user's email as verified
    user.email_verified = True
    user.save()

    return jsonify({'message': 'Email verified successfully'}), 200