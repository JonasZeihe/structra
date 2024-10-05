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


import unittest
import shutil
import tempfile
from pathlib import Path
from structra.structure_processor import StructureProcessor
from structra.logger_config import setup_logger


class TestStructra(unittest.TestCase):
    """
    Integration test to ensure the Structra PBS file is correctly processed,
    and the directory and file structure is accurately generated.
    """

    def setUp(self):
        """
        Setup test environment with a temporary directory and the Structra PBS structure file.
        """
        self.logger = setup_logger(log_to_file=False)

        # Create a temporary directory for the test
        self.test_dir = tempfile.mkdtemp()

        # Create the Structra PBS file for testing
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
        Test that the Structra PBS file generates the correct project structure.
        """
        # Instantiate the Structure_Processor and process the PBS file
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        processor.process_pbs_file(self.structure_file)

        # Define the expected structure that should be generated
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

        # Check if all expected files and directories exist
        for expected_file in expected_structure:
            expected_path = Path(self.test_dir) / expected_file
            self.assertTrue(
                expected_path.exists(),
                f"Expected file or directory {expected_path} was not created.",
            )

        # Check that the key files that should be empty are indeed empty
        empty_files = [
            "structra/.gitignore",
            "structra/src/structra/__init__.py",
            "structra/src/tests/__init__.py",
        ]
        for empty_file in empty_files:
            file_path = Path(self.test_dir) / empty_file
            self.assertEqual(file_path.stat().st_size, 0, f"{empty_file} is not empty")


if __name__ == "__main__":
    unittest.main()
