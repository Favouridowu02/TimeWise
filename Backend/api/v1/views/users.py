#!/usr/bin/env python3
"""
    This Module is currently pending because most of the features are conatined in the auth.py module.
    This Module contains the api endpoints for the user
"""
from flask import Flask, abort, request, jsonify, Blueprint
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.base_model import db
from models.user import User
from datetime import datetime
import uuid

user_bp = Blueprint('user', __name__)