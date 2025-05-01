import json
from models.user import User
from tests.conftest import get_auth_token # Import helper if needed directly
from flask_jwt_extended import create_access_token
import datetime

# Register User Tests
def test_register_user_success(test_client):
    """Test user registration success."""
    register_data = {
        "name": "New User",
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123"
    }
    response = test_client.post('/api/v1/auth/register', json=register_data)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['message'] == "User registered successfully"
    # Verify user exists in DB
    user = User.query.filter_by(username="newuser").first()
    assert user is not None
    assert user.email == "new@example.com"

def test_register_user_duplicate_username(test_client, new_user):
    """Test user registration with duplicate username."""
    register_data = {
        "name": "Duplicate User",
        "username": new_user.username, # Use existing username
        "email": "duplicate@example.com",
        "password": "password123"
    }
    response = test_client.post('/api/v1/auth/register', json=register_data)
    assert response.status_code == 409 # Conflict
    assert 'error' in response.get_json()
    assert 'User with this username already exists' in response.get_json()['error']

def test_register_user_duplicate_email(test_client, new_user):
    """Test user registration with duplicate email."""
    register_data = {
        "name": "Duplicate Email User",
        "username": "unique_username",
        "email": new_user.email, # Use existing email
        "password": "password123"
    }
    response = test_client.post('/api/v1/auth/register', json=register_data)
    assert response.status_code == 409 # Conflict
    assert 'error' in response.get_json()
    assert 'User with this email already exists' in response.get_json()['error']

def test_register_user_missing_fields(test_client):
    """Test user registration with missing fields."""
    response = test_client.post('/api/v1/auth/register', json={"username": "missing"})
    assert response.status_code == 400 # Bad Request
    assert 'error' in response.get_json()

# Login Tests

def test_login_user_success(test_client, new_user):
    """Test user login success."""
    login_data = {'username': new_user.username, 'password': 'password123'}
    response = test_client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 200
    json_data = response.get_json()
    assert 'access_token' in json_data

def test_login_user_wrong_password(test_client, new_user):
    """Test user login with incorrect password."""
    login_data = {'username': new_user.username, 'password': 'wrongpassword'}
    response = test_client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 401 # Unauthorized
    assert 'error' in response.get_json()
    assert "Invalid credentials" in response.get_json()['error']

def test_login_user_not_found(test_client):
    """Test user login for a non-existent user."""
    login_data = {'username': 'nosuchuser', 'password': 'password123'}
    response = test_client.post('/api/v1/auth/login', json=login_data)
    assert response.status_code == 401 # Unauthorized (or 404 depending on implementation)
    assert 'error' in response.get_json()
    assert "Invalid credentials" in response.get_json()['error'] # Common practice

# User Profile Tests

def test_get_profile_success(test_client, new_user, auth_headers):
    """Test retrieving the user's profile successfully."""
    response = test_client.get('/api/v1/auth/profile', headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == str(new_user.id)
    assert json_data['email'] == new_user.email
    assert json_data['username'] == new_user.username

def test_get_profile_unauthorized(test_client):
    """Test retrieving the user's profile without authentication."""
    response = test_client.get('/api/v1/auth/profile')
    assert response.status_code == 401  # Unauthorized

def test_update_profile_success(test_client, new_user, auth_headers):
    """Test updating the user's profile successfully."""
    update_data = {
        "name": "Updated Name",
        "bio": "Updated bio"
    }
    response = test_client.put('/api/v1/auth/profile', json=update_data, headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['name'] == "Updated Name"
    assert json_data['bio'] == "Updated bio"

def test_update_profile_invalid_password(test_client, new_user, auth_headers):
    """Test updating the user's profile with an incorrect current password."""
    update_data = {
        "current_password": "wrongpassword",
        "new_password": "newpassword123"
    }
    response = test_client.put('/api/v1/auth/profile', json=update_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'error' in response.get_json()
    assert response.get_json()['error'] == "Current password is incorrect"

# Logout Tests

def test_logout_success(test_client, auth_headers):
    """Test logging out successfully."""
    response = test_client.post('/api/v1/auth/logout', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Logout successful"

def test_logout_status(test_client):
    """Test checking logout status with GET method."""
    response = test_client.get('/api/v1/auth/logout')
    assert response.status_code == 400
    assert response.get_json()['message'] == "Use POST to log out"

# Delete User account Tests

def test_delete_account_success(test_client, new_user, auth_headers):
    """Test deleting the user's account successfully."""
    response = test_client.delete('/api/v1/auth/delete', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == "User account deleted successfully"

def test_delete_account_unauthorized(test_client):
    """Test deleting the user's account without authentication."""
    response = test_client.delete('/api/v1/auth/delete')
    assert response.status_code == 401  # Unauthorized

# Password Reset Tests

def test_password_reset_request_success(test_client, new_user):
    """Test requesting a password reset token successfully."""
    response = test_client.post('/api/v1/auth/password-reset-request', json={"email": new_user.email})
    assert response.status_code == 200
    assert 'reset_token' in response.get_json()

def test_password_reset_request_user_not_found(test_client):
    """Test requesting a password reset token for a non-existent user."""
    response = test_client.post('/api/v1/auth/password-reset-request', json={"email": "nonexistent@example.com"})
    assert response.status_code == 404
    assert response.get_json()['error'] == "User with this email does not exist"

def test_password_reset_success(test_client, new_user, auth_headers):
    """Test resetting the user's password successfully."""
    # Simulate generating a reset token
    reset_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(minutes=15))
    reset_data = {
        "reset_token": reset_token,
        "new_password": "newpassword123"
    }
    response = test_client.post('/api/v1/auth/password-reset', json=reset_data)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Password reset successfully"

def test_password_reset_invalid_token(test_client):
    """Test resetting the user's password with an invalid token."""
    reset_data = {
        "reset_token": "invalidtoken",
        "new_password": "newpassword123"
    }
    response = test_client.post('/api/v1/auth/password-reset', json=reset_data)
    assert response.status_code == 400
    assert response.get_json()['error'] == "Invalid or expired reset token"

# Email Veriufication Tests

# def test_email_verification_request_success(test_client, new_user, auth_headers):
#     """Test requesting an email verification token successfully."""
#     response = test_client.post('/api/v1/auth/email-verification-request', headers=auth_headers)
#     assert response.status_code == 200
#     assert response.get_json()['message'] == "Email verification token sent successfully"

# def test_email_verification_request_already_verified(test_client, verified_user, auth_headers):
#     """Test requesting an email verification token for an already verified user."""
#     response = test_client.post('/api/v1/auth/email-verification-request', headers=auth_headers)
#     assert response.status_code == 200
#     assert response.get_json()['message'] == "Email is already verified"

# def test_email_verification_success(test_client, new_user):
#     """Test verifying the user's email successfully."""
#     # Simulate generating a verification token
#     verification_token = create_access_token(identity=new_user.id, expires_delta=datetime.timedelta(hours=1))
#     verification_data = {"verification_token": verification_token}
#     response = test_client.post('/api/v1/auth/email-verification', json=verification_data)
#     assert response.status_code == 200
#     assert response.get_json()['message'] == "Email verified successfully"

# def test_email_verification_invalid_token(test_client):
#     """Test verifying the user's email with an invalid token."""
#     verification_data = {"verification_token": "invalidtoken"}
#     response = test_client.post('/api/v1/auth/email-verification', json=verification_data)
#     assert response.status_code == 400
#     assert response.get_json()['error'] == "Invalid or expired verification token"