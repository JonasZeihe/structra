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
This module sets up the logging configuration for Structra.
It provides functions to set up a logger and save logs to a file.
"""

import logging
from datetime import datetime
from pathlib import Path
from io import StringIO


def setup_logger() -> (logging.Logger, StringIO):
    """
    Sets up the logger for Structra. Logs are stored in memory and can be written to a file later.

    Returns:
        logging.Logger: Configured logger instance.
        StringIO: Log stream to store logs in memory.
    """
    logger = logging.getLogger("StructraLogger")
    logger.setLevel(logging.INFO)

    log_stream = StringIO()
    stream_handler = logging.StreamHandler(log_stream)
    stream_handler.setLevel(logging.INFO)

    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)

    logger.addHandler(stream_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger, log_stream


def save_logs_to_file(log_stream: StringIO, log_dir: Path = Path(".")) -> None:
    """
    Saves the in-memory logs to a log file.

    Args:
        log_stream (StringIO): The in-memory log stream.
        log_dir (Path): The directory where the log file will be saved.
    """
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_filename = log_dir / f"structra_log_{timestamp}.txt"

    with log_filename.open("w", encoding="utf-8") as log_file:
        log_file.write(log_stream.getvalue())
