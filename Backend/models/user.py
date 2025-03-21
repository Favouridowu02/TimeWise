#!/usr/bin/env python3
"""
    This Module contains the User Database model
"""
from sqlalchemy.dialects.postgresql import UUID
from .base_model import db, BaseModel
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__ = 'users'
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    timezone = db.Column(db.String(50), default='UTC')
    language = db.Column(db.String(10), default='en')
    profile_image = db.Column(db.String(255))
    bio = db.Column(db.Text)

    # Relationship
    tasks = db.relationship('Task', back_populates='user', lazy='select', cascade='all, delete-orphan')
    progress = db.relationship('Progress', back_populates='user', cascade='all, delete-orphan')

    def set_password(self, password):
        """Hash the password and store it securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"<User {self.username} {self.id}>"