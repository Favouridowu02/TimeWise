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
import logging

db = SQLAlchemy()


class BaseModel(db.Model):
    """Abstract base model with UUID primary key and common fields."""
    __abstract__ = True # This Prevents the table creation

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """Save the instance to the database."""
        try:
            db.session.commit()
            logging.info(f"Saved {self} to the database.")
        except Exception as e:
            logging.error(f"Error saving {self}: {e}")
            db.session.rollback()

    def delete(self, obj=None):
        """Delete the instance from the database."""
        try:
            if obj is None:
                db.session.delete(self)
            else:
                db.session.delete(obj)
            db.session.commit()
            logging.info(f"Deleted {self} from the database.")
        except Exception as e:
            logging.error(f"Error deleting {self}: {e}")
            db.session.rollback()
    
    def new(self, obj=None):
        """Create a New instance of the Model"""
        try:
            if obj is None:
                db.session.add(self)
            else:
                db.session.add(obj)
            logging.info(f"Added new instance: {obj or self}")
        except Exception as e:
            logging.error(f"Error adding object: {e}")

    @classmethod
    def get(cls, **kwargs):
        """Retrieve an instance from the Database"""
        instance = None
        try:
            instance = cls.query.filter_by(**kwargs).first()
            if instance:
                logging.debug(f"Retrieved instance {instance} using filter {kwargs}")
            else:
                logging.debug(f"No instance found for {cls.__name__} with filter {kwargs}")
        except Exception as e:
            logging.exception(f"Error retrieving {cls.__name__} object from the database with filter {kwargs}") 
        return instance

    @classmethod
    def all(cls):
        """Return all records of the model."""
        return cls.query.all()

    def to_json(self):
        """Convert the model instance to a JSON-friendly dictionary."""
        from models.user import UserRole
        result = {}
        for column in self.__table__.columns:
            if column.name == 'password_hash':
                continue
            value = getattr(self, column.name)
            if isinstance(value, UserRole):
                value = value.value
            elif isinstance(value, datetime):
                value = value.isoformat()
            else:
                value = str(value)
            result[column.name] = value
        return result

    def __str__(self):
        """Return a string representation of the model instance."""
        return f"<{self.__class__.__name__} {self.id}>"

    def __repr__(self):
        """Return a developer-friendly string representation."""
        return self.__str__()
