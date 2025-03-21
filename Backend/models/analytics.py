"""
    This Module contains the Analytics Database Model for TimeWise
"""
from sqlalchemy.dialects.postgresql import UUID
from .base_model import db, BaseModel


class Analytics(BaseModel):
    """
        This Model is used for keeping the analytics of a user of the total time spent on a task
    """
    __tablename__ = 'analytics'

    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('users.id'), nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('tasks.id'), nullable=True)
    total_time_spent = db.Column(db.Interval, default='0')

    # Relationship
    user = db.relationship('User')

    def __str__(self):
        return f"<Analytics for User {self.user_id} - Total Time: {self.total_time_spent}>"