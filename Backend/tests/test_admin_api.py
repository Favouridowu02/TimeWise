#!/usr/bin/python3
"""
    THIS WILL BE UPDATED LATER
    Test cases for admin API endpoints in the Flask application.
    These tests cover the following functionalities:
"""
import json
import pytest
from models.user import User, UserRole
from models.base_model import db
# Fixtures new_user, admin_user, another_user, test_client, auth_headers, admin_auth_headers auto-imported

def test_admin_get_all_users_forbidden(test_client, auth_headers):
     """Test GET /admin/users forbidden for regular user."""
     response = test_client.get('/api/v1/admin/users', headers=auth_headers)
     assert response.status_code == 403

def test_admin_get_all_users_success(test_client, new_user, admin_user, another_user, admin_auth_headers):
     """Test GET /admin/users success for admin."""
     # Users are added by fixtures
     response = test_client.get('/api/v1/admin/users', headers=admin_auth_headers)
     assert response.status_code == 200
     json_data = response.get_json()
     assert isinstance(json_data, list)
     # Expecting admin, new_user, another_user
     assert len(json_data) >= 3
     usernames = {u['username'] for u in json_data}
     assert admin_user.username in usernames
     assert new_user.username in usernames
     assert another_user.username in usernames
     # Check structure of one user
     test_user_data = next(u for u in json_data if u['username'] == new_user.username)
     assert test_user_data['email'] == new_user.email
     assert test_user_data['role'] == new_user.role.value
     assert 'password_hash' not in test_user_data

def test_admin_get_specific_user_success(test_client, new_user, admin_auth_headers):
    """Test GET /admin/users/<id> success for admin."""
    response = test_client.get(f'/api/v1/admin/users/{new_user.id}', headers=admin_auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == str(new_user.id)
    assert json_data['username'] == new_user.username
    assert json_data['role'] == new_user.role.value
    assert json_data['email'] == new_user.email
    # Check if the password hash is not included - This is important for security
    assert 'password_hash' not in json_data
    # Check if the response contains all expected fields
    expected_fields = ['id', 'username', 'email', 'role', 'profile_image', 'bio', 'email_verified']
    for field in expected_fields:
        assert field in json_data, f"Field {field} is missing in the response"

def test_admin_get_specific_user_forbidden(test_client, new_user, auth_headers):
    """Test GET /admin/users/<id> forbidden for regular user."""
    response = test_client.get(f'/api/v1/admin/users/{new_user.id}', headers=auth_headers)
    assert response.status_code == 403

def test_admin_get_specific_user_not_found(test_client, admin_auth_headers):
    """Test GET /admin/users/<id> returns 404 for non-existent user."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = test_client.get(f'/api/v1/admin/users/{non_existent_id}', headers=admin_auth_headers)
    assert response.status_code == 404

def test_admin_update_user_role_success(test_client, new_user, admin_auth_headers, db_session):
    """Test PUT /admin/users/<id>/role success for admin."""
    assert new_user.role == UserRole.USER # Verify initial role

    update_data = {'role': 'ADMIN'} # Case-insensitive check might be needed in route
    response = test_client.put(f'/api/v1/admin/users/{new_user.id}/role', json=update_data, headers=admin_auth_headers)
    assert response.status_code == 200
    assert f"role updated to {UserRole.ADMIN.value}" in response.get_json()['message']

    # Verify change in DB
    db_session.refresh(new_user) # Refresh object state from DB
    assert new_user.role == UserRole.ADMIN

def test_admin_update_user_role_forbidden(test_client, new_user, auth_headers):
    """Test PUT /admin/users/<id>/role forbidden for regular user."""
    update_data = {'role': 'ADMIN'}
    response = test_client.put(f'/api/v1/admin/users/{new_user.id}/role', json=update_data, headers=auth_headers)
    assert response.status_code == 403

def test_admin_update_user_role_invalid_role(test_client, new_user, admin_auth_headers):
    """Test PUT /admin/users/<id>/role with invalid role value."""
    update_data = {'role': 'INVALID_ROLE'}
    response = test_client.put(f'/api/v1/admin/users/{new_user.id}/role', json=update_data, headers=admin_auth_headers)
    assert response.status_code == 400
    assert "Invalid role" in response.get_json()['error']

def test_admin_update_user_role_missing_role(test_client, new_user, admin_auth_headers):
    """Test PUT /admin/users/<id>/role with missing role field."""
    update_data = {'not_role': 'some_value'}
    response = test_client.put(f'/api/v1/admin/users/{new_user.id}/role', json=update_data, headers=admin_auth_headers)
    assert response.status_code == 400
    assert "Missing 'role'" in response.get_json()['error']

def test_admin_update_user_role_user_not_found(test_client, admin_auth_headers):
    """Test PUT /admin/users/<id>/role for non-existent user."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    update_data = {'role': 'ADMIN'}
    response = test_client.put(f'/api/v1/admin/users/{non_existent_id}/role', json=update_data, headers=admin_auth_headers)
    assert response.status_code == 404

def test_admin_delete_user_success(test_client, another_user, admin_auth_headers, db_session):
    """Test DELETE /admin/users/<id> success for admin."""
    user_to_delete_id = another_user.id
    response = test_client.delete(f'/api/v1/admin/users/{user_to_delete_id}', headers=admin_auth_headers)
    assert response.status_code == 200
    assert "deleted successfully" in response.get_json()['message']

    # Verify deleted from DB
    deleted_user = db_session.get(User, user_to_delete_id) # Use session.get for primary key lookup
    assert deleted_user is None

def test_admin_delete_user_forbidden(test_client, another_user, auth_headers):
    """Test DELETE /admin/users/<id> forbidden for regular user."""
    response = test_client.delete(f'/api/v1/admin/users/{another_user.id}', headers=auth_headers)
    assert response.status_code == 403

def test_admin_delete_user_not_found(test_client, admin_auth_headers):
    """Test DELETE /admin/users/<id> for non-existent user."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = test_client.delete(f'/api/v1/admin/users/{non_existent_id}', headers=admin_auth_headers)
    assert response.status_code == 404

# Optional: Test deleting self (if prevented in the route)
# def test_admin_delete_self(test_client, admin_user, admin_auth_headers):
#     """Test DELETE /admin/users/<id> prevents admin from deleting self."""
#     response = test_client.delete(f'/api/v1/admin/users/{admin_user.id}', headers=admin_auth_headers)
#     assert response.status_code == 403 # Or 400 depending on implementation
#     assert "cannot delete themselves" in response.get_json()['error']