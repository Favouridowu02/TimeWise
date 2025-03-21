#!/usr/bin/env python3
"""
    This module contains the test for the Analytics model
"""
from models.analytics import Analytics
from models.task import Task
from models.base_model import db
from datetime import timedelta

def test_analytics_creation(test_client, new_user):
    """Test if an analytics record can be created and linked to a user and task."""
    db.session.add(new_user)
    db.session.commit()

    task = Task(title="Test Task", description="Track time spent", user_id=new_user.id)
    db.session.add(task)
    db.session.commit()

    analytics = Analytics(user_id=new_user.id, task_id=task.id, total_time_spent=timedelta(hours=1))
    db.session.add(analytics)
    db.session.commit()

    retrieved_analytics = Analytics.query.filter_by(task_id=task.id).first()
    assert retrieved_analytics is not None
    assert retrieved_analytics.user_id == new_user.id
    assert str(retrieved_analytics.total_time_spent) == '1:00:00'
