# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

import unittest
import shutil
import tempfile
from pathlib import Path
from structra.structure_parser import handle_files
from structra.logger_config import setup_logger, save_logs_to_file
import logging


class TestStructra(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        self.test_dir = tempfile.mkdtemp()
        self.structure_file = Path(self.test_dir) / "complex_structure.txt"
        with open(self.structure_file, "w", encoding="utf-8") as f:
            f.write(
                "project/\n"
                "    ├── .gitignore\n"
                "    ├── src/\n"
                "    │   ├── module/\n"
                "    │   │   ├── __init__.py\n"
                "    │   │   ├── main.py\n"
                "    │   │   ├── utils/\n"
                "    │   │   │   ├── helper.py\n"
                "    │   │   │   └── deep_utils/\n"
                "    │   │   │       ├── helper_1.py\n"
                "    │   │   │       ├── helper_2.py\n"
                "    │   │   │       └── deeper_utils/\n"
                "    │   │   │           ├── deep_1.py\n"
                "    │   │   │           ├── deep_2.py\n"
                "    │   │   │           └── deep_3.py\n"
                "    ├── docs/\n"
                "    │   ├── .gitignore\n"
                "    │   └── readme.md\n"
                "    └── tests/\n"
                "        ├── .gitignore\n"
                "        ├── test_main.py\n"
                "        └── test_utils.py\n"
            )

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_complex_integration_structra(self):
        logging.debug("Starting test_complex_integration_structra")
        handle_files([str(self.structure_file)])

        expected_structure = [
            "project/.gitignore",
            "project/src/module/__init__.py",
            "project/src/module/main.py",
            "project/src/module/utils/helper.py",
            "project/src/module/utils/deep_utils/helper_1.py",
            "project/src/module/utils/deep_utils/helper_2.py",
            "project/src/module/utils/deep_utils/deeper_utils/deep_1.py",
            "project/src/module/utils/deep_utils/deeper_utils/deep_2.py",
            "project/src/module/utils/deep_utils/deeper_utils/deep_3.py",
            "project/docs/.gitignore",
            "project/docs/readme.md",
            "project/tests/.gitignore",
            "project/tests/test_main.py",
            "project/tests/test_utils.py",
        ]

        for expected_file in expected_structure:
            expected_path = Path(self.test_dir) / expected_file
            if not expected_path.exists():
                logging.error("File not created: %s", expected_path)
            self.assertTrue(
                expected_path.exists(),
                f"Expected file {expected_path} was not created.",
            )

    def test_empty_file(self):
        empty_file = Path(self.test_dir) / "empty.txt"
        empty_file.touch()

        handle_files([str(empty_file)])
        self.assertFalse((Path(self.test_dir) / "project").exists())

    def test_invalid_file_type(self):
        logging.debug("Starting test_invalid_file_type")
        invalid_file = Path(self.test_dir) / "invalid_file.json"
        invalid_file.touch()

        with self.assertLogs("structra", level="ERROR") as log:
            handle_files([str(invalid_file)])
            if log.output:
                logging.debug("Log output captured: %s", log.output)
                self.assertIn("Invalid file type", log.output[0])
            else:
                logging.error("No log output captured for invalid file type.")
                self.fail("No log output captured for invalid file type.")

    def test_logging_output(self):
        logging.debug("Starting test_logging_output")
        _, log_stream = setup_logger()
        handle_files([str(self.structure_file)])

        log_content = log_stream.getvalue()
        if not log_content:
            logging.error("No logs captured in the log stream")
            self.fail("No logs were captured in the log stream.")

        self.assertIn("Created directory:", log_content)
        self.assertIn("Created file:", log_content)

        log_file_path = Path(self.test_dir) / "logs"
        save_logs_to_file(log_stream, log_file_path)

        log_file = log_file_path / "structra_log.txt"
        self.assertTrue(log_file.exists(), "Log file was not created.")
        with open(log_file, "r", encoding="utf-8") as f:
            logs = f.read()
            self.assertIn("Created directory:", logs)
            self.assertIn("Created file:", logs)


if __name__ == "__main__":
    unittest.main()
