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
This module handles the configuration of logging for the Structra application.
It supports logging to both the console and a log file, depending on user preferences.
"""

import logging
import sys
from pathlib import Path
from datetime import datetime


def setup_logger(
    log_to_file: bool = False,
    log_file_prefix: str = "structra_log",
    log_level: int = logging.DEBUG,
) -> logging.Logger:
    """
    Sets up the logger for the Structra application.

    Args:
        log_to_file (bool): If True, logs will also be saved to a file. Default is False.
        log_file_prefix (str): The prefix for the log file name.
        log_level (int): The minimum logging level. Default is logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("structra_logger")
    logger.setLevel(log_level)

    if logger.hasHandlers():
        logger.handlers.clear()

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(_get_log_formatter())
    logger.addHandler(console_handler)

    if log_to_file:
        _setup_file_logging(logger, log_file_prefix)

    return logger


def _setup_file_logging(logger: logging.Logger, log_file_prefix: str) -> None:
    """
    Helper function to set up logging to a file.

    Args:
        logger (logging.Logger): Logger instance.
        log_file_prefix (str): The prefix for the log file name.
    """
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file = f"{log_file_prefix}_{timestamp}.txt"
        log_file_path = Path(log_file)

        log_file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8")
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(_get_log_formatter())

        logger.addHandler(file_handler)
        logger.info(f"Logging to file: {log_file_path}")

    except Exception as error:
        logger.error(f"Failed to initialize file logging: {error}")


def _get_log_formatter() -> logging.Formatter:
    """
    Returns a consistent log formatter for both console and file handlers.

    Returns:
        logging.Formatter: A formatter instance.
    """
    return logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
