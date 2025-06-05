import pytest
from models.task import Task
from models.analytics import Analytics
from models.user import User
from datetime import timedelta


def test_get_user_analytics_success(test_client, new_user, auth_headers, db_session):
    # Create tasks for the user
    task1 = Task(title="Task 1", user_id=new_user.id, completed=True, total_time_spent=timedelta(hours=2))
    task2 = Task(title="Task 2", user_id=new_user.id, completed=False, total_time_spent=timedelta(hours=1, minutes=30))
    db_session.add_all([task1, task2])
    db_session.commit()

    response = test_client.get('/api/v1/analytics', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_tasks'] == 2
    assert data['completed_tasks'] == 1
    assert 'total_time_spent' in data


def test_get_user_analytics_unauthorized(test_client):
    response = test_client.get('/api/v1/analytics')
    assert response.status_code == 401


def test_create_user_analytics_success(test_client, new_user, auth_headers, db_session):
    # Create a task for the user
    task = Task(title="Analytics Task", user_id=new_user.id)
    db_session.add(task)
    db_session.commit()

    analytics_data = {
        "task_id": task.id,
        "time_spent": 3600  # 1 hour in seconds
    }
    response = test_client.post('/api/v1/analytics', json=analytics_data, headers=auth_headers)
    assert response.status_code == 201
    data = response.get_json()
    assert data['message'] == 'Analytics entry created successfully'
    assert data['analytics']['task_id'] == str(task.id)
    assert data['analytics']['user_id'] == str(new_user.id)


def test_create_user_analytics_invalid_task(test_client, new_user, auth_headers):
    analytics_data = {
        "task_id": "00000000-0000-0000-0000-000000000000",
        "time_spent": 1800
    }
    response = test_client.post('/api/v1/analytics', json=analytics_data, headers=auth_headers)
    assert response.status_code == 404
    assert 'Task not found' in response.get_json()['error']


def test_create_user_analytics_unauthorized(test_client):
    analytics_data = {
        "task_id": "00000000-0000-0000-0000-000000000000",
        "time_spent": 1800
    }
    response = test_client.post('/api/v1/analytics', json=analytics_data)
    assert response.status_code == 401


def test_get_user_analytics_no_tasks(test_client, new_user, auth_headers):
    response = test_client.get('/api/v1/analytics', headers=auth_headers)
    assert response.status_code == 200
    data = response.get_json()
    assert data['total_tasks'] == 0
    assert data['completed_tasks'] == 0
    assert data['total_time_spent'] == '0:00:00'
