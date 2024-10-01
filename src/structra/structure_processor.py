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
        self.current_path = None

    def process_pbs_file(self, pbs_file_path: Path) -> None:
        try:
            with open(pbs_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

                if not lines:
                    self.logger.error(f"The PBS file '{pbs_file_path}' is empty.")
                    return

                root_folder = self._get_base_folder_from_pbs(lines[0])
                self.current_path = self.output_directory / root_folder

                if not self.current_path.exists():
                    self.current_path.mkdir(parents=True, exist_ok=True)
                    self.logger.info(
                        f"Created root directory: {self.current_path.as_posix()}"
                    )

                previous_indent = 0
                path_stack = [self.current_path]

                for line in lines[1:]:
                    clean_line, current_indent = self._parse_line(line)
                    if not clean_line:
                        continue

                    if current_indent > previous_indent:
                        path_stack.append(path_stack[-1] / clean_line)
                    elif current_indent < previous_indent:
                        for _ in range(previous_indent - current_indent):
                            path_stack.pop()
                        path_stack[-1] = path_stack[-1].parent / clean_line
                    else:
                        path_stack[-1] = path_stack[-1].parent / clean_line

                    if clean_line.endswith("/"):
                        self._create_directory(path_stack[-1])
                    else:
                        self._create_file(path_stack[-1])

                    previous_indent = current_indent

                self.logger.info("Completed processing the PBS structure.")

        except Exception as e:
            self.logger.error(
                f"Failed to process PBS file: {pbs_file_path}. Error: {str(e)}"
            )
            raise

    def _get_base_folder_from_pbs(self, first_line: str) -> str:
        """
        Extracts the root folder name from the first line of the PBS file.
        """
        return first_line.strip().rstrip("/")

    def _parse_line(self, line: str) -> tuple:
        """
        Cleans a line by removing hierarchy symbols and extra spaces,
        and calculates the indentation level based on leading spaces.
        """
        clean_line = line.replace("├──", "").replace("└──", "").replace("│", "").strip()
        indent_level = (len(line) - len(line.lstrip())) // 4
        return clean_line, indent_level

    def _create_directory(self, folder_path: Path) -> None:
        """
        Creates a directory at the given path if it does not exist.
        """
        if not folder_path.exists():
            folder_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created directory: {folder_path.as_posix()}")

    def _create_file(self, file_path: Path) -> None:
        """
        Creates a file at the given path if it does not exist.
        """
        if not file_path.exists():
            file_path.touch(exist_ok=True)
            self.logger.info(f"Created file: {file_path.as_posix()}")
