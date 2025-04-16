#!/usr/bin/env python3
"""
    This Module contains the Utilities for setting up logging.
    It configures a logger to log messages to both the console and a rotating file.
    The file handler rotates the log files when they reach a certain size.
"""
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging(log_file="app.log"):
    """
    Configure logging for the application.
    Logs will be written to both the console and a rotating file.

    Arguments:
        log_file: This is the File to store all the Logs
    """
    # Validates the Log file exists else Create it
    log_dir = os.path.dirname(log_file) or "."
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    logger = logging.getLogger()

    # Avoid adding handlers multiple times if called again (e.g., in tests)
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.setLevel(logging.DEBUG)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(log_file, maxBytes=5 * 1024 * 1024, backupCount=3)
    except (PermissionError, OSError) as e:
        logging.error(f"Failed to create log file {log_file}: {str(e)}")
        raise
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s [in %(pathname)s:%(lineno)d]')
    file_handler.setFormatter(file_formatter)

    # Add handlers to the logger
    try:
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to configure logging: {str(e)}", file=sys.stderr)
        raise

    logging.info("Logging configured.")
