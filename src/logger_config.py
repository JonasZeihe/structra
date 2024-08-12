"""
logger_config.py

This module sets up the logging configuration for the application.
"""

import logging
from datetime import datetime


def setup_logger():
    """
    Sets up the logging configuration.

    Creates a log file with a timestamp and configures the logging module to
    write logs to this file.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = f"timestamp_log_{timestamp}.txt"
    logging.basicConfig(
        filename=log_filename,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
