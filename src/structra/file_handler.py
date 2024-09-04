# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# file_handler.py

"""
This module contains functions to process file structures based on input text files.
It reads the structure definitions from .txt files and generates the corresponding
directory and file structures.
"""

import os
import logging


def process_structure(base_path, lines):
    """
    Processes the lines defining the directory and file structure and creates them
    under the specified base path.

    Args:
        base_path (str): The base directory where the structure will be created.
        lines (list of str): The lines from the .txt file defining the structure.
    """
    path_stack = [base_path]
    logging.info(f"Processing structure under base path: {base_path}")

    for line in lines:
        stripped_line = line.rstrip()
        if not stripped_line:
            continue

        depth = (len(line) - len(line.lstrip())) // 4
        name = (
            stripped_line.replace("├── ", "")
            .replace("└── ", "")
            .replace("│", "")
            .strip()
        )

        logging.info(f"Processing: {name} at depth {depth}")

        while len(path_stack) > depth + 1:
            path_stack.pop()

        current_path = os.path.join(path_stack[-1], name)

        try:
            if "." not in os.path.basename(current_path) and not current_path.endswith(
                "/"
            ):
                if not os.path.exists(current_path):
                    os.makedirs(current_path)
                    logging.info(f"Created directory: {current_path}")
                path_stack.append(current_path)
            else:
                dir_path = os.path.dirname(current_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    logging.info(f"Created directory for file: {dir_path}")
                if not os.path.exists(current_path):
                    with open(current_path, "w", encoding="utf-8"):
                        pass  # Create an empty file
                    logging.info(f"Created file: {current_path}")

        except PermissionError as e:
            logging.error(f"Permission error with path {current_path}: {e}")
        except OSError as e:
            logging.error(f"OS error with path {current_path}: {e}")


def handle_files(file_paths):
    """
    Processes the provided .txt file paths and generates the corresponding directory
    structures.

    Args:
        file_paths (list of str): List of paths to .txt files to process.
    """
    for file_path in file_paths:
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.readlines()
                    if not content:
                        logging.warning(f"File {file_path} is empty")
                        continue

                    project_name = content[0].strip().rstrip("/")
                    base_path = os.path.join(os.path.dirname(file_path), project_name)
                    os.makedirs(base_path, exist_ok=True)

                    logging.info(f"Processing project: {project_name}")
                    process_structure(base_path, content[1:])
                    logging.info(
                        f'Project structure for "{project_name}" created successfully at {base_path}'
                    )

            except FileNotFoundError as e:
                logging.error(f"File not found: {file_path}. Error: {e}")
            except PermissionError as e:
                logging.error(f"Permission error with file {file_path}: {e}")
            except OSError as e:
                logging.error(f"OS error with file {file_path}: {e}")
