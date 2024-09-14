# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# logger_config.py

"""
This module is responsible for setting up the logging configuration.
It supports logging to both the console and to a file.
"""

import logging
import os
from io import StringIO


def setup_logger():
    """
    Sets up the logging configuration for the application.

    Returns:
        tuple: logger instance, log_stream (for saving to file later)
    """
    log_stream = StringIO()
    logger = logging.getLogger("structra")
    logger.setLevel(logging.INFO)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(console_format)

    stream_handler = logging.StreamHandler(log_stream)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(console_format)

    logger.addHandler(console_handler)
    logger.addHandler(stream_handler)

    return logger, log_stream


def save_logs_to_file(log_stream, output_dir):
    """
    Saves the logs from the log stream to a file in the specified directory.

    Args:
        log_stream (StringIO): Stream containing the logs to be saved.
        output_dir (Path or str): Directory where the log file will be saved.
    """
    try:
        log_file_path = os.path.join(output_dir, "structra_log.txt")
        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write(log_stream.getvalue())
    except OSError as e:
        logging.error(f"Error saving logs to file: {e}")
