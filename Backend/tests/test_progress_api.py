import json
import pytest
from models.user import User
from models.task import Task
from models.progress import Progress # Assuming Progress model exists
from models.base_model import db


def test_create_progress_success(test_client, new_user, auth_headers, db_session):
    # Create a task first
    task = Task(title="Progress Task", user_id=new_user.id)
    db_session.add(task)
    db_session.commit()

    progress_data = {
        "task_id": task.id,
        "status": "in_progress", # Or whatever fields your API expects
        "notes": "Started working on it"
    }
    response = test_client.post('/api/v1/progress', json=progress_data, headers=auth_headers)
    assert response.status_code == 201
    # Add more assertions

def test_get_progress_for_task(test_client, new_user, auth_headers, db_session):
    # Create task and progress
    # ...
    response = test_client.get(f'/api/v1/tasks/{task.id}/progress', headers=auth_headers) # Example route
    assert response.status_code == 200
    # Add more assertions

def test_get_progress_unauthorized(test_client):
    response = test_client.get('/api/v1/progress') # Or specific task progress route
    assert response.status_code == 401