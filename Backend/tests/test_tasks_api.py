import json
import pytest # Import pytest
from models.user import User, UserRole
from models.task import Task
from models.base_model import db
# Fixtures like new_user, admin_user, test_client, auth_headers, admin_auth_headers are now auto-imported from conftest.py

def test_get_tasks_unauthorized(test_client):
    """Test GET /tasks without authentication."""
    response = test_client.get('/api/v1/tasks')
    assert response.status_code == 401 # Unauthorized

def test_create_task_success(test_client, new_user, auth_headers):
    """Test POST /tasks successfully creates a task."""
    task_data = {
        'title': 'API Test Task',
        'description': 'Testing task creation via API',
        'due_date': '2025-12-31T10:00:00Z'
    }
    response = test_client.post('/api/v1/tasks', json=task_data, headers=auth_headers)

    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data['title'] == 'API Test Task'
    assert 'id' in json_data
    assert json_data['user_id'] == new_user.id

    task_in_db = Task.query.get(json_data['id'])
    assert task_in_db is not None
    assert task_in_db.title == 'API Test Task'

def test_create_task_missing_data(test_client, auth_headers):
    """Test POST /tasks with missing required fields."""
    task_data = {'description': 'Missing title'}
    response = test_client.post('/api/v1/tasks', json=task_data, headers=auth_headers)
    assert response.status_code == 400
    assert 'error' in response.get_json()

def test_get_tasks_list(test_client, new_user, auth_headers, db_session):
    """Test GET /tasks returns tasks for the authenticated user."""
    task1 = Task(title="User Task 1", user_id=new_user.id)
    task2 = Task(title="User Task 2", user_id=new_user.id)
    db_session.add_all([task1, task2])
    db_session.commit()

    response = test_client.get('/api/v1/tasks', headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2
    titles = {t['title'] for t in json_data}
    assert "User Task 1" in titles
    assert "User Task 2" in titles
    assert json_data[0]['user_id'] == new_user.id

def test_get_tasks_list_empty(test_client, auth_headers):
    """Test GET /tasks returns empty list when no tasks exist."""
    response = test_client.get('/api/v1/tasks', headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 0

def test_get_specific_task_success(test_client, new_user, auth_headers, db_session):
    """Test GET /tasks/<id> successfully retrieves a specific task."""
    task = Task(title="Specific Task", user_id=new_user.id)
    db_session.add(task)
    db_session.commit()

    response = test_client.get(f'/api/v1/tasks/{task.id}', headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['id'] == task.id
    assert json_data['title'] == "Specific Task"
    assert json_data['user_id'] == new_user.id

def test_get_specific_task_not_found(test_client, auth_headers):
    """Test GET /tasks/<id> returns 404 for non-existent task."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = test_client.get(f'/api/v1/tasks/{non_existent_id}', headers=auth_headers)
    assert response.status_code == 404

def test_get_specific_task_forbidden(test_client, new_user, another_user, auth_headers, db_session):
    """Test GET /tasks/<id> returns 403 when accessing another user's task."""
    other_task = Task(title="Other User Task", user_id=another_user.id)
    db_session.add(other_task)
    db_session.commit()

    # Use auth_headers for 'new_user' to try accessing 'another_user's task
    response = test_client.get(f'/api/v1/tasks/{other_task.id}', headers=auth_headers)
    assert response.status_code == 403 # Forbidden

def test_update_task_success(test_client, new_user, auth_headers, db_session):
    """Test PUT /tasks/<id> successfully updates a task."""
    task = Task(title="Original Title", description="Original Desc", user_id=new_user.id)
    db_session.add(task)
    db_session.commit()

    update_data = {'title': 'Updated Title', 'status': 'completed'}
    response = test_client.put(f'/api/v1/tasks/{task.id}', json=update_data, headers=auth_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['title'] == 'Updated Title'
    assert json_data['status'] == 'completed'
    assert json_data['description'] == 'Original Desc' # Check unchanged field

    # Verify in DB
    updated_task = Task.query.get(task.id)
    assert updated_task.title == 'Updated Title'
    assert updated_task.status == 'completed'

def test_update_task_not_found(test_client, auth_headers):
    """Test PUT /tasks/<id> returns 404 for non-existent task."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    update_data = {'title': 'Wont Update'}
    response = test_client.put(f'/api/v1/tasks/{non_existent_id}', json=update_data, headers=auth_headers)
    assert response.status_code == 404

def test_update_task_forbidden(test_client, new_user, another_user, auth_headers, db_session):
    """Test PUT /tasks/<id> returns 403 when updating another user's task."""
    other_task = Task(title="Other User Task", user_id=another_user.id)
    db_session.add(other_task)
    db_session.commit()

    update_data = {'title': 'Attempted Update'}
    response = test_client.put(f'/api/v1/tasks/{other_task.id}', json=update_data, headers=auth_headers)
    assert response.status_code == 403

def test_delete_task_success(test_client, new_user, auth_headers, db_session):
    """Test DELETE /tasks/<id> successfully deletes a task."""
    task = Task(title="To Be Deleted", user_id=new_user.id)
    db_session.add(task)
    db_session.commit()
    task_id = task.id

    response = test_client.delete(f'/api/v1/tasks/{task_id}', headers=auth_headers)
    assert response.status_code == 200
    assert response.get_json()['message'] == "Task deleted successfully"

    # Verify deleted from DB
    deleted_task = Task.query.get(task_id)
    assert deleted_task is None

def test_delete_task_not_found(test_client, auth_headers):
    """Test DELETE /tasks/<id> returns 404 for non-existent task."""
    non_existent_id = "00000000-0000-0000-0000-000000000000"
    response = test_client.delete(f'/api/v1/tasks/{non_existent_id}', headers=auth_headers)
    assert response.status_code == 404

def test_delete_task_forbidden(test_client, new_user, another_user, auth_headers, db_session):
    """Test DELETE /tasks/<id> returns 403 when deleting another user's task."""
    other_task = Task(title="Other User Task", user_id=another_user.id)
    db_session.add(other_task)
    db_session.commit()

    response = test_client.delete(f'/api/v1/tasks/{other_task.id}', headers=auth_headers)
    assert response.status_code == 403