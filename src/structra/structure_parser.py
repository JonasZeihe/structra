# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# structure_parser.py

"""
This module is responsible for parsing the input text files and
processing the directory and file structure using the structure generator.
"""

import os
import logging
from structra.structure_generator import generate_structure


def parse_structure_file(file_path):
    """
    Parses a .txt file containing the structure definition and passes
    the content to the structure generator.

    Args:
        file_path (str): Path to the .txt file containing the structure.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()
            if not lines:
                logging.warning("File %s is empty", file_path)
                return

            project_name = lines[0].strip().rstrip("/")
            base_path = os.path.join(os.path.dirname(file_path), project_name)
            os.makedirs(base_path, exist_ok=True)

            logging.info("Processing project: %s", project_name)
            generate_structure(base_path, lines[1:])
            logging.info(
                'Project structure for "%s" created successfully at %s',
                project_name,
                base_path,
            )

    except FileNotFoundError as e:
        logging.error("File not found: %s. Error: %s", file_path, e)
    except PermissionError as e:
        logging.error("Permission error with file %s: %s", file_path, e)
    except OSError as e:
        logging.error("OS error with file %s: %s", file_path, e)


def handle_files(file_paths):
    """
    Processes a list of .txt files and generates the corresponding
    directory structures.

    Args:
        file_paths (list of str): List of file paths to .txt files.
    """
    for file_path in file_paths:
        if file_path.endswith(".txt"):
            parse_structure_file(file_path)
        else:
            logging.error("Invalid file type: %s. Expected a .txt file.", file_path)
