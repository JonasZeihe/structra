# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# structure_generator.py

import os
import logging


def generate_structure(base_path, structure_lines):
    """
    Generates the directory and file structure based on the provided lines.

    Args:
        base_path (str): The base directory where the structure will be created.
        structure_lines (list of str): The lines from the .txt file defining the structure.
    """
    path_stack = [base_path]
    logging.info("Generating structure under base path: %s", base_path)

    for line in structure_lines:
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

        logging.info("Processing: %s at depth %d", name, depth)

        while len(path_stack) > depth + 1:
            path_stack.pop()

        current_path = os.path.join(path_stack[-1], name)

        try:
            if "." not in os.path.basename(current_path):
                if not os.path.exists(current_path):
                    os.makedirs(current_path)
                    logging.info("Created directory: %s", current_path)
                path_stack.append(current_path)
            else:
                dir_path = os.path.dirname(current_path)
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path, exist_ok=True)
                    logging.info("Created directory for file: %s", dir_path)
                if not os.path.exists(current_path):
                    with open(current_path, "w", encoding="utf-8"):
                        pass
                    logging.info("Created file: %s", current_path)

        except PermissionError as e:
            logging.error("Permission error with path %s: %s", current_path, e)
        except OSError as e:
            logging.error("OS error with path %s: %s", current_path, e)
