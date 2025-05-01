#!/usr/bin/env python3
"""
    This module contains the test for the BaseModel model
"""
from models.base_model import BaseModel, db
from datetime import datetime


class _HelperTestModel(BaseModel):
    """A simple test model extending BaseModel for testing purposes."""
    __tablename__ = 'test_model' # Keep table name if needed for testing
    name = db.Column(db.String(50), nullable=False)

def test_base_model_creation(db_session): # Use db_session fixture for isolation
    """Test if a BaseModel record can be created, retrieved, and deleted."""
    # Use the renamed class
    test_record = _HelperTestModel(name="Test Record")
    # Use db_session from fixture
    db_session.add(test_record)
    db_session.commit()

    # Use the renamed class
    retrieved_record = _HelperTestModel.query.filter_by(name="Test Record").first()
    assert retrieved_record is not None
    assert retrieved_record.name == "Test Record"
    assert retrieved_record.id is not None # Check id is set
    assert isinstance(retrieved_record.created_at, datetime) # Check timestamp
    assert isinstance(retrieved_record.updated_at, datetime) # Check timestamp

    # Use db_session for delete operation
    db_session.delete(retrieved_record)
    db_session.commit()

    # Use the renamed class
    deleted_record = _HelperTestModel.query.filter_by(name="Test Record").first()
    assert deleted_record is None