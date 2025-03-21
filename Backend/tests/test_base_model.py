#!/usr/bin/env python3
"""
    This module contains the test for the BaseModel model
"""
from models.base_model import BaseModel, db
from datetime import datetime

class TestModel(BaseModel):
    """A simple test model extending BaseModel for testing purposes."""
    __tablename__ = 'test_model'
    name = db.Column(db.String(50), nullable=False)

def test_base_model_creation(test_client):
    """Test if a BaseModel record can be created, retrieved, and deleted."""
    test_record = TestModel(name="Test Record")
    test_record.save()

    retrieved_record = TestModel.query.filter_by(name="Test Record").first()
    assert retrieved_record is not None
    assert retrieved_record.name == "Test Record"

    test_record.delete()
    deleted_record = TestModel.query.filter_by(name="Test Record").first()
    assert deleted_record is None