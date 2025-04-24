#!/usr/bin/python3
"""
    This Module contains the Utilities for sending Emails.
"""
from flask_mail import Message
import logging # Import logging

# Get a logger for this module
logger = logging.getLogger(__name__)

def send_email(subject, recipients, body):
    """
        Send an email using Flask-Mail
        Arguments:
            - subject: The subject of the Email
            - recipients: The list of recipients
            - body: The body of the Email
        Returns:
            - Boolean indicating success or failure
    """
    # Import mail instance here to avoid circular imports if mail is initialized in app.py
    from api.v1.app import mail 
    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)
        logger.info(f"Email sent successfully to {recipients} with subject '{subject}'")
        return True
    except Exception as e:
        # Use logger.exception to include stack trace for errors
        logger.exception(f"Error sending email to {recipients} with subject '{subject}'") 
        return False
