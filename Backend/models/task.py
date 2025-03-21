#!/usr/bin/env python3
"""
    This Module contains the Task Database Model for TimeWise
"""
from sqlalchemy.dialects.postgresql import UUID
from .base_model import db, BaseModel
from datetime import datetime, timedelta


class Task(BaseModel):
    __tablename__ = 'tasks'

    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    priority = db.Column(db.Enum('low', 'medium', 'high', name='priority_enum'), default='medium')
    deadline = db.Column(db.DateTime, nullable=True)
    completed = db.Column(db.Boolean, default=False)
    # I would update this soon
    total_time_spent = db.Column(db.Interval, default=timedelta(seconds=0))

    # Foreign Key
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)

    # Relationship
    user = db.relationship('User', back_populates='tasks')
    progress = db.relationship('Progress', back_populates='task', uselist=False) # one task -> one progress

    def __str__(self):
        return f"<Task {self.title} - {self.priority} {self.id}>"