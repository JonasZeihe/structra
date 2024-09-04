"""
Integration test for the Structra project structure generation.
"""

import unittest
import os
import shutil
from pathlib import Path
from file_handler import process_structure


class TestStructra(unittest.TestCase):
    """Test suite for the Structra project structure generation."""

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.test_dir = Path("test_structra_environment")
        self.test_dir.mkdir(exist_ok=True)
        self.structure = [
            "skryper/",
            "skryper/.gitignore",
            "skryper/src/",
            "skryper/src/__init__.py",
            "skryper/src/main.py",
            "skryper/src/tests/",
            "skryper/src/tests/test_skryper.py",
        ]

    def tearDown(self):
        """Clean up the test environment."""
        shutil.rmtree(self.test_dir)

    def test_structure_creation(self):
        """Test the creation of the file structure."""
        process_structure(self.test_dir, self.structure)

        for item in self.structure:
            item_path = self.test_dir / item
            if item.endswith("/"):
                self.assertTrue(
                    item_path.is_dir(), f"Directory {item_path} was not created."
                )
            else:
                self.assertTrue(
                    item_path.is_file(), f"File {item_path} was not created."
                )


if __name__ == "__main__":
    unittest.main()
