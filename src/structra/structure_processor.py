# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# structure_processor.py

"""
Handles the processing of Project Structure (PBS) files and generates corresponding
folders and files based on the hierarchy defined in the input file.

Author: Jonas Zeihe
"""

from pathlib import Path
import logging


class StructureProcessor:
    def __init__(self, output_directory: Path, logger: logging.Logger):
        self.output_directory = output_directory
        self.logger = logger

    def process_pbs_file(self, pbs_file_path: Path) -> None:
        with open(pbs_file_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        root_folder = lines[0].strip().rstrip("/")
        root_path = self.output_directory / root_folder
        root_path.mkdir(parents=True, exist_ok=True)
        path_stack = [root_path]

        for line in lines[1:]:
            clean_line = self._clean_line(line)

            if clean_line == root_folder:
                continue

            level = self._count_hierarchy_level(line)

            # Keep track of the path stack based on the hierarchy level
            while len(path_stack) > level + 1:
                path_stack.pop()

            full_path = path_stack[-1] / clean_line.rstrip("/")

            # If it's a directory, create it and add it to the path stack
            if clean_line.endswith("/"):
                full_path.mkdir(parents=True, exist_ok=True)
                path_stack.append(full_path)
            else:
                # Handle both empty and non-empty files
                full_path.touch(exist_ok=True)

    def _clean_line(self, line: str) -> str:
        # Clean up the line by removing structure symbols and leading spaces
        return line.lstrip("├──│└── ").strip()

    def _count_hierarchy_level(self, line: str) -> int:
        # Calculate the hierarchy level based on the leading symbols or spaces
        indent_level = len(line) - len(line.lstrip(" │"))
        return indent_level // 4  # Assuming indentation is in multiples of 4 spaces
