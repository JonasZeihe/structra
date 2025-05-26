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
Comprehensive unit tests for the main entry point of the Structra application.

These tests cover the argument parsing, file validation, error handling,
and overall application flow when generating file structures based on project
structure files (PBS).

Author: Jonas Zeihe
"""

import unittest
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, MagicMock
from app.main import parse_arguments, validate_files, process_files, main


class TestMain(unittest.TestCase):
    """
    Unit tests for main.py functionalities, including argument parsing,
    file validation, error handling, and file processing.
    """

    def setUp(self):
        """
        Setup temporary directory for testing file-based operations.
        """
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        """
        Cleanup temporary directory after each test.
        """
        shutil.rmtree(self.test_dir)

    @patch(
        "sys.argv",
        ["script_name", "file1.txt", "--logging", "--root-folder", "output_dir"],
    )
    def test_parse_arguments(self):
        """
        Test the argument parsing function to ensure it correctly interprets command-line arguments.
        """
        parsed_args = parse_arguments()
        self.assertEqual(parsed_args.files, ["file1.txt"])
        self.assertTrue(parsed_args.logging)
        self.assertEqual(parsed_args.root_folder, "output_dir")

    def test_validate_files_valid(self):
        """
        Test the file validation function to ensure it correctly identifies valid files.
        """
        valid_file = Path(self.test_dir) / "valid_file.txt"
        valid_file.touch()
        logger = MagicMock()
        self.assertTrue(validate_files([str(valid_file)], logger))
        logger.error.assert_not_called()

    def test_validate_files_invalid(self):
        """
        Test the file validation function to ensure it correctly identifies invalid files.
        """
        invalid_file = Path(self.test_dir) / "invalid_file.doc"
        logger = MagicMock()
        self.assertFalse(validate_files([str(invalid_file)], logger))
        logger.error.assert_called_once_with(
            f"File '{invalid_file}' does not exist or has an invalid format."
        )

    @patch("app.main.StructureProcessor")
    def test_process_files(self, mock_processor):
        """
        Test the process_files function to ensure it correctly processes files and creates directories.
        """
        logger = MagicMock()
        root_folder = Path(self.test_dir) / "output"
        process_files(["file1.txt"], logger, str(root_folder))
        mock_processor.assert_called_once_with(root_folder, logger)
        mock_processor.return_value.process_pbs_file.assert_called_once_with(
            Path("file1.txt")
        )

    @patch("app.main.process_files")
    @patch("app.main.validate_files")
    @patch("app.main.setup_logger")
    @patch("sys.exit")
    def test_main_file_not_found_error(
        self, mock_exit, mock_setup_logger, mock_validate_files, mock_process_files
    ):
        """
        Test the main function to ensure that FileNotFoundError is properly handled.
        """
        mock_setup_logger.return_value = MagicMock()
        mock_validate_files.return_value = True
        mock_process_files.side_effect = FileNotFoundError("File not found")
        main(["file1.txt"])
        mock_exit.assert_called_once_with(1)

    @patch("app.main.process_files")
    @patch("app.main.validate_files")
    @patch("app.main.setup_logger")
    @patch("sys.exit")
    def test_main_is_a_directory_error(
        self, mock_exit, mock_setup_logger, mock_validate_files, mock_process_files
    ):
        """
        Test the main function to ensure that IsADirectoryError is properly handled.
        """
        mock_setup_logger.return_value = MagicMock()
        mock_validate_files.return_value = True
        mock_process_files.side_effect = IsADirectoryError("Expected a file")
        main(["file1.txt"])
        mock_exit.assert_called_once_with(1)

    @patch("app.main.process_files")
    @patch("app.main.validate_files")
    @patch("app.main.setup_logger")
    @patch("sys.exit")
    def test_main_generic_exception(
        self, mock_exit, mock_setup_logger, mock_validate_files, mock_process_files
    ):
        """
        Test the main function to ensure that a generic exception is properly handled.
        """
        mock_setup_logger.return_value = MagicMock()
        mock_validate_files.return_value = True
        mock_process_files.side_effect = Exception("Boom")
        main(["file1.txt"])
        mock_exit.assert_called_once_with(1)

    @patch("app.main.process_files")
    @patch("app.main.validate_files")
    @patch("app.main.setup_logger")
    def test_main_successful_execution(
        self, mock_setup_logger, mock_validate_files, mock_process_files
    ):
        """
        Test that main runs successfully when there are no errors.
        """
        mock_logger = MagicMock()
        mock_setup_logger.return_value = mock_logger
        mock_validate_files.return_value = True

        main(["file1.txt"])

        mock_setup_logger.assert_called_once()
        mock_process_files.assert_called_once_with(
            ["file1.txt"], mock_logger, "structra_output"
        )
        mock_logger.info.assert_any_call("Structra started.")
        mock_logger.info.assert_any_call("Structra completed successfully.")


if __name__ == "__main__":
    unittest.main()
