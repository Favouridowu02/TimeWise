#!/usr/bin/python3
"""
    This Module contains the Progress API Route
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from datetime import datetime
import uuid

progress_bp = Blueprint('progress', __name__)