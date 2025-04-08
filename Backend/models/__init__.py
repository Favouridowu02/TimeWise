#!/usr/bin/env python3
"""
    This module initializes the database and imports the models.
"""
from .base_model import db
from .user import User
from .task import Task
from .progress import Progress
from .analytics import Analytics