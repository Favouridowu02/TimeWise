#!/usr/bin/env python3
"""
    This module contains the test for the Progress model
"""
from models.progress import Progress
from models.task import Task
from models.base_model import db


def test_progress_tracking(test_client, new_user):
    """Test if progress can be tracked for a task."""
    db.session.add(new_user)
    db.session.commit()

    task = Task(title="Test Task", description="Track progress", user_id=new_user.id)
    db.session.add(task)
    db.session.commit()

    progress = Progress(user_id=new_user.id, task_id=task.id)
    db.session.add(progress)
    db.session.commit()

    retrieved_progress = Progress.query.filter_by(task_id=task.id).first()
    assert retrieved_progress is not None
    assert retrieved_progress.user_id == new_user.id
