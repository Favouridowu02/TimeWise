#!/usr/bin/env python3
"""
    This module contains the base model for the TimeWise application.

    It sets up the SQLAlchemy database instance and imports necessary
    modules for handling datetime operations. This base model would be
    extended by other models to interact with the database.
"""

import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()


class BaseModel(db.Model):
    """Abstract base model with UUID primary key and common fields."""
    __abstract__ = True # This Prevents the table creation

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the instance to the database."""
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """Delete the instance from the database."""
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def all(cls):
        """Return all records of the model."""
        return cls.query.all()

    def to_json(self):
        """Convert the model instance to a JSON-friendly dictionary."""
        return {column.name: str(getattr(self, column.name)) for column in self.__table__.columns}

    def __str__(self):
        """Return a string representation of the model instance."""
        return f"<{self.__class__.__name__} {self.id}>"

    def __repr__(self):
        """Return a developer-friendly string representation."""
        return self.__str__()
