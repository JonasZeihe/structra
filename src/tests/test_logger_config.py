# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# test_logger_config.py

"""
Unit tests for the logger configuration module of the Structra application.

These tests cover the setup of the logger, including file logging and console logging.

Author: Jonas Zeihe
"""

import unittest
import logging
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from pathlib import Path
from structra.logger_config import setup_logger


class TestLoggerConfig(unittest.TestCase):
    """
    Unit tests for logger_config.py to ensure the logger is configured correctly.
    """

    def setUp(self):
        """
        Set up a temporary directory for logging tests involving file output.
        """
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Clean up the temporary directory.
        """
        for handler in logging.getLogger("structra_logger").handlers:
            handler.close()
        shutil.rmtree(self.test_dir)

    def test_setup_logger_console_logging(self):
        """
        Test if the logger is correctly set up with console logging.
        """
        logger = setup_logger(log_to_file=False)

        stream_handlers = [
            h for h in logger.handlers if isinstance(h, logging.StreamHandler)
        ]
        self.assertEqual(len(stream_handlers), 1)

        self.assertEqual(logger.level, logging.DEBUG)
        self.assertIsInstance(stream_handlers[0].formatter, logging.Formatter)

    def test_setup_logger_file_logging(self):
        """
        Test if the logger is correctly set up with file logging.
        """
        log_file_path = Path(self.test_dir) / "test_log.txt"

        logger = setup_logger(log_to_file=True, log_file_prefix=str(log_file_path))

        file_handlers = [
            h for h in logger.handlers if isinstance(h, logging.FileHandler)
        ]
        self.assertEqual(len(file_handlers), 1)

        self.assertTrue(file_handlers[0].baseFilename.startswith(str(log_file_path)))
        self.assertIsInstance(file_handlers[0].formatter, logging.Formatter)

    def test_logging_to_file(self):
        """
        Test that the logger writes messages to the specified log file.
        """
        log_file_prefix = Path(self.test_dir) / "test_logging.txt"
        logger = setup_logger(log_to_file=True, log_file_prefix=str(log_file_prefix))

        logger.info("Test log message")

        log_file_name = f"{log_file_prefix}_{logger.handlers[1].baseFilename.split('_')[-2]}_{logger.handlers[1].baseFilename.split('_')[-1]}"
        log_file_path = Path(log_file_name)

        with open(log_file_path, "r", encoding="utf-8") as log_file:
            log_content = log_file.read()
            self.assertIn("Test log message", log_content)

    @patch("structra.logger_config.logging.getLogger")
    def test_logger_reuse(self, mock_get_logger):
        """
        Test that the logger reuses existing handlers when re-initialized.
        """
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logger()
        setup_logger()

        self.assertEqual(mock_logger.handlers.clear.call_count, 2)
        mock_logger.setLevel.assert_called_with(logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
