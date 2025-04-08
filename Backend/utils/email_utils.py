#!/usr/bin/python3
"""
    This Module contains the Utilities for sending Emails.
"""
from flask_mail import Message


def send_email(subject, recipients, body):
    """
        Send an email using Flask-Mail
        Arguments:
            - subject: The subject of the Email
            - recipients: The list of recipients
            - body: The body of the Email
        Returns:
            - None
    """
    from api.v1.app import mail
    try:
        msg = Message(subject=subject, recipients=recipients, body=body)
        mail.send(msg)
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
