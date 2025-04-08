#!/usr/bin/python3
""" Testing Email"""
import secrets
from flask import Flask
from flask.ext.mail import Mail


app = Flask(__name__)

secret_key = secrets.token_urlsafe()

app.config["JWT_SECRET_KEY"] = secret_key
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["MAIL_SERVER"] = 'smtp.googlemail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "favouridowu02@gmail.com"
app.config["MAIL_PASSWORD"] = "password"


mail = Mail(app)