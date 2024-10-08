# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# test_main.py

"""
Unit tests for the main entry point of the Structra application.

These tests cover the argument parsing, file validation, and overall application
flow when generating file structures based on project structure files (PBS).

Author: Jonas Zeihe
"""

import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
import sys
from structra.main import parse_arguments, validate_files, process_files, main


class TestMain(unittest.TestCase):
    """
    Unit tests for main.py functionalities, including argument parsing, file validation, and file processing.
    """

    @patch("structra.main.setup_logger")
    def test_parse_arguments(self, mock_logger):
        """
        Test the argument parsing function to ensure it correctly interprets command-line arguments.
        """
        test_args = [
            "script_name",
            "file1.txt",
            "--logging",
            "--root-folder",
            "output_dir",
        ]
        with patch.object(sys, "argv", test_args):
            parsed_args = parse_arguments()

            self.assertEqual(parsed_args.files, ["file1.txt"])
            self.assertTrue(parsed_args.logging)
            self.assertEqual(parsed_args.root_folder, "output_dir")

    @patch("structra.main.Path")
    @patch("structra.main.setup_logger")
    def test_validate_files(self, mock_logger, mock_path):
        """
        Test the file validation function to ensure it correctly identifies invalid files.
        """
        mock_path.return_value.exists.side_effect = [
            True,
            False,
        ]
        mock_logger_instance = MagicMock()

        valid_files = validate_files(
            ["valid_file.txt", "invalid_file.txt"], mock_logger_instance
        )

        mock_logger_instance.error.assert_called_once_with(
            "File 'invalid_file.txt' does not exist or has an invalid format."
        )
        self.assertFalse(valid_files)

    @patch("structra.main.StructureProcessor")
    @patch("structra.main.setup_logger")
    @patch("structra.main.Path")
    def test_process_files(self, mock_path, mock_logger, mock_processor):
        """
        Test the process_files function to ensure it correctly processes files and creates directories.
        """
        mock_path().cwd.return_value = Path("/fake/directory")
        mock_logger_instance = MagicMock()

        process_files(["file1.txt"], mock_logger_instance, "root_folder")

        mock_processor.assert_called_once_with(
            Path("/fake/directory/root_folder"), mock_logger_instance
        )
        mock_processor_instance = mock_processor.return_value
        mock_processor_instance.process_pbs_file.assert_called_once_with(
            Path("/fake/directory/file1.txt")
        )

    @patch("structra.main.handle_error")
    @patch("structra.main.setup_logger")
    @patch("structra.main.validate_files")
    @patch("structra.main.process_files")
    @patch("structra.main.parse_arguments")
    @patch("sys.exit")
    def test_main_generic_exception(
        self,
        mock_exit,
        mock_parse_arguments,
        mock_process_files,
        mock_validate_files,
        mock_setup_logger,
        mock_handle_error,
    ):
        """
        Test the main function to ensure that a generic exception is properly handled.
        """
        mock_parse_arguments.return_value.files = ["file1.txt"]
        mock_validate_files.return_value = True
        mock_logger_instance = MagicMock()
        mock_setup_logger.return_value = mock_logger_instance

        mock_process_files.side_effect = Exception("Unexpected error")

        main()

        mock_handle_error.assert_called_once_with(
            mock_logger_instance, "Unexpected error"
        )
        mock_exit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
