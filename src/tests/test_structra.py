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
Unit and integration tests for the Structra application.

These tests cover the processing of Project Structure (PBS) files, the generation
of directory and file structures, and specific unit tests for the StructureProcessor class.

Author: Jonas Zeihe
"""

import unittest
import shutil
import tempfile
from pathlib import Path
import os
import stat
from structra.structure_processor import StructureProcessor
from structra.logger_config import setup_logger


class TestStructra(unittest.TestCase):
    """
    Tests to ensure the Structra PBS file is correctly processed,
    and the directory and file structure is accurately generated.
    """

    def setUp(self):
        """
        Setup test environment with a temporary directory and the Structra PBS structure file.
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
        Reset permissions for the read-only directories before cleanup.
        """
        read_only_dir = Path(self.test_dir) / "readonly"
        if read_only_dir.exists():
            os.chmod(read_only_dir, stat.S_IWRITE)

        shutil.rmtree(self.test_dir)

    def test_structra_project_structure(self):
        """
        Test that the Structra PBS file generates the correct project structure.
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
                f"Expected file or directory {expected_path} was not created.",
            )

        empty_files = [
            "structra/.gitignore",
            "structra/src/structra/__init__.py",
            "structra/src/tests/__init__.py",
        ]
        for empty_file in empty_files:
            file_path = Path(self.test_dir) / empty_file
            self.assertEqual(file_path.stat().st_size, 0, f"{empty_file} is not empty")

    def test_clean_line(self):
        """
        Unit test for the _clean_line method in StructureProcessor.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        result = processor._clean_line("│   ├── main.py")
        self.assertEqual(result, "main.py")

    def test_count_hierarchy_level(self):
        """
        Unit test for the _count_hierarchy_level method in StructureProcessor.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        result = processor._count_hierarchy_level("│       ├── main.py")
        self.assertEqual(result, 2)

    def test_create_directory(self):
        """
        Unit test for the _create_directory method in StructureProcessor.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        new_directory = Path(self.test_dir) / "test_directory/"
        processor._create_directory(new_directory)
        self.assertTrue(new_directory.exists())

    def test_create_file(self):
        """
        Unit test for the _create_file method in StructureProcessor.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        new_file = Path(self.test_dir) / "test_file.txt"
        processor._create_file(new_file)
        self.assertTrue(new_file.exists())

    def test_file_not_found_error(self):
        """
        Test that a FileNotFoundError is logged if a PBS file does not exist.
        """
        processor = StructureProcessor(Path(self.test_dir), self.logger)
        non_existent_file = Path(self.test_dir) / "non_existent.txt"
        with self.assertLogs(self.logger, level="ERROR") as log:
            processor.process_pbs_file(non_existent_file)
            self.assertIn(f"PBS file '{non_existent_file}' not found.", log.output[0])


if __name__ == "__main__":
    unittest.main()
