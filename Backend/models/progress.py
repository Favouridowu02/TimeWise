#!/usr/bin/env python3
"""
    This Module contains the Progress Database Model 
"""
from sqlalchemy.dialects.postgresql import UUID
from .base_model import db, BaseModel
from datetime import datetime

class Progress(BaseModel):
    """
        This Model is used for keeping track of each user with their tasks
    """
    __tablename__ = 'progress'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tasks.id'), nullable=False)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, nullable=True)
    duration = db.Column(db.Interval, nullable=True)

    # Relationship
    user = db.relationship('User', back_populates="progress")
    task = db.relationship('Task', back_populates="progress")

    def __str__(self):
        return f"<Progress for Task {self.task_id} - Duration: {self.duration}>"