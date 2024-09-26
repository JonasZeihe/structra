# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# test_structra.py

"""
Integration tests for the Structra application.

These tests cover the processing of Project Structure (PBS) files and the generation
of directory and file structures.

Author: Jonas Zeihe
"""

# test_structra.py

import unittest
import shutil
import tempfile
from pathlib import Path
from structra.structure_processor import StructureProcessor
from structra.logger_config import setup_logger


class TestStructra(unittest.TestCase):
    """
    Integration tests for the Structra project to ensure file and folder
    structures are correctly generated, logged, and handled.
    """

    def setUp(self):
        """
        Setup test environment with a temporary directory and test structure file.
        Initializes logger and prepares test data.
        """
        self.logger = setup_logger(log_to_file=False)

        self.test_dir = tempfile.mkdtemp()

        self.structure_file = Path(self.test_dir) / "test_structure.txt"
        with open(self.structure_file, "w", encoding="utf-8") as f:
            f.write(
                "structra/\n"
                "├── .gitignore\n"
                "├── .git/\n"
                "├── src/\n"
                "│   ├── build/\n"
                "│   ├── dist/\n"
                "│   ├── structra/\n"
                "│   │   ├── __pycache__/\n"
                "│   │   ├── __init__.py\n"
                "│   │   ├── logger_config.py\n"
                "│   │   ├── main.py\n"
                "│   │   └── structure_processor.py\n"
                "│   ├── tests/\n"
                "│   │   ├── __pycache__/\n"
                "│   │   ├── __init__.py\n"
                "│   │   └── test_structra.py\n"
                "│   ├── structra_run_build.bat\n"
                "│   └── structra_run_tests.bat\n"
                "├── LICENSE\n"
                "├── README.md\n"
                "└── src.zip\n"
            )

    def tearDown(self):
        """
        Clean up by removing the temporary test directory.
        """
        shutil.rmtree(self.test_dir)

    def test_structra_project_structure(self):
        """
        Test that the Structra project directory and file structure is correctly generated.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)

        processor.process_pbs_file(self.structure_file)

        expected_structure = [
            "structra/.gitignore",
            "structra/.git/",
            "structra/src/",
            "structra/src/build/",
            "structra/src/dist/",
            "structra/src/structra/",
            "structra/src/structra/__pycache__/",
            "structra/src/structra/__init__.py",
            "structra/src/structra/logger_config.py",
            "structra/src/structra/main.py",
            "structra/src/structra/structure_processor.py",
            "structra/src/tests/",
            "structra/src/tests/__pycache__/",
            "structra/src/tests/__init__.py",
            "structra/src/tests/test_structra.py",
            "structra/src/structra_run_build.bat",
            "structra/src/structra_run_tests.bat",
            "structra/LICENSE",
            "structra/README.md",
            "structra/src.zip",
        ]

        for expected_file in expected_structure:
            expected_path = Path(self.test_dir) / expected_file
            self.assertTrue(
                expected_path.exists(),
                f"Expected file {expected_path} was not created.",
            )

        empty_files = [
            "structra/.gitignore",
            "structra/src/structra/__init__.py",
            "structra/src/tests/__init__.py",
        ]
        for empty_file in empty_files:
            file_path = Path(self.test_dir) / empty_file
            self.assertEqual(file_path.stat().st_size, 0, f"{empty_file} is not empty")

    def test_invalid_file_type(self):
        """
        Test that an invalid file type triggers appropriate error logging.
        """
        invalid_file = Path(self.test_dir) / "invalid_file.json"
        invalid_file.touch()

        processor = StructureProcessor(Path(self.test_dir), self.logger)

        with self.assertLogs(self.logger, level="ERROR") as log:
            processor.process_pbs_file(invalid_file)
            self.assertIn("Failed to process PBS file", log.output[0])

    def test_logging_output(self):
        """
        Test that logging is correctly generated and saved to a log file.
        """
        log_file_path = Path(self.test_dir) / "structra_log.txt"

        self.logger = setup_logger(log_to_file=True, log_file=str(log_file_path))

        processor = StructureProcessor(Path(self.test_dir), self.logger)

        processor.process_pbs_file(self.structure_file)

        self.assertTrue(log_file_path.exists(), "Log file was not created.")

        with open(log_file_path, "r", encoding="utf-8") as log_file:
            logs = log_file.read()
            self.assertIn("Created directory", logs)
            self.assertIn("Created file", logs)

    def test_invalid_filenames(self):
        """
        Test that invalid filenames are properly logged and skipped.
        """
        invalid_file = Path(self.test_dir) / "invalid_structure.pdf"
        with open(invalid_file, "w") as f:
            f.write("This is not a valid structure file.")

        processor = StructureProcessor(Path(self.test_dir), self.logger)

        with self.assertLogs(self.logger, level="ERROR") as log:
            processor.process_pbs_file(invalid_file)
            self.assertIn("Failed to process PBS file", log.output[0])

    def test_invalid_output_directory(self):
        """
        Test that an error is raised if the output directory is invalid.
        """
        invalid_dir = "/invalid_directory/does_not_exist"
        processor = StructureProcessor(Path(invalid_dir), self.logger)

        with self.assertLogs(self.logger, level="ERROR") as log:
            processor.process_pbs_file(self.structure_file)
            self.assertIn("Error creating directory", log.output[0])


if __name__ == "__main__":
    unittest.main()
