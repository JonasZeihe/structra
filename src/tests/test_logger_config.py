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
from unittest.mock import patch, MagicMock
from structra.logger_config import setup_logger


class TestLoggerConfig(unittest.TestCase):
    """
    Unit tests for logger_config.py to ensure the logger is configured correctly.
    """

    @patch("structra.logger_config.logging.StreamHandler")
    @patch("structra.logger_config._get_log_formatter")
    def test_setup_logger_console_logging(self, mock_formatter, mock_stream_handler):
        """
        Test if the logger is correctly set up with console logging.
        """
        mock_formatter.return_value = MagicMock()
        mock_handler = MagicMock()
        mock_stream_handler.return_value = mock_handler

        logger = setup_logger(log_to_file=False)

        mock_stream_handler.assert_called_once_with(logging.StreamHandler(sys.stdout))
        mock_handler.setFormatter.assert_called_once_with(mock_formatter())
        self.assertEqual(logger.level, logging.DEBUG)

    @patch("structra.logger_config.logging.FileHandler")
    @patch("structra.logger_config._setup_file_logging")
    def test_setup_logger_file_logging(self, mock_file_logging, mock_file_handler):
        """
        Test if the logger is correctly set up with file logging.
        """
        mock_file_handler.return_value = MagicMock()

        logger = setup_logger(log_to_file=True)

        mock_file_logging.assert_called_once_with(logger, "structra_log")

    @patch("structra.logger_config.Path")
    @patch("structra.logger_config.logging.FileHandler")
    @patch("structra.logger_config._get_log_formatter")
    def test_setup_file_logging(self, mock_formatter, mock_file_handler, mock_path):
        """
        Test the setup of file logging and the creation of log files.
        """
        mock_formatter.return_value = MagicMock()
        mock_handler = MagicMock()
        mock_file_handler.return_value = mock_handler
        mock_path.return_value = MagicMock()

        logger = logging.getLogger("structra_logger")
        logger.setLevel(logging.INFO)

        setup_logger(log_to_file=True)

        mock_file_handler.assert_called_once()
        mock_handler.setFormatter.assert_called_once_with(mock_formatter())

    @patch("structra.logger_config.logging.getLogger")
    def test_logger_reuse(self, mock_get_logger):
        """
        Test that the logger reuses existing handlers when re-initialized.
        """
        mock_logger = MagicMock()
        mock_get_logger.return_value = mock_logger

        setup_logger()
        setup_logger()

        mock_logger.handlers.clear.assert_called_once()
        mock_logger.setLevel.assert_called_with(logging.DEBUG)


if __name__ == "__main__":
    unittest.main()
