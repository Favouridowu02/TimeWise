#!/usr/bin/env python3
"""
    This module contains the test for the Task model
"""
from models.task import Task
from models.base_model import db


def test_task_creation(test_client, new_user):
    """Test if a task can be created and linked to a user."""
    db.session.add(new_user)
    db.session.commit()

    task = Task(title="Test Task", description="This is a test task", user_id=new_user.id)
    db.session.add(task)
    db.session.commit()

    retrieved_task = Task.query.filter_by(title="Test Task").first()
    assert retrieved_task is not None
    assert retrieved_task.user_id == new_user.id
