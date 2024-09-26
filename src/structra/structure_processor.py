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
        try:
            with open(pbs_file_path, "r", encoding="utf-8") as file:
                lines = file.readlines()

                if not lines:
                    self.logger.error(f"The PBS file '{pbs_file_path}' is empty.")
                    return

                root_folder = self._get_base_folder_from_pbs(lines[0])
                root_path = self.output_directory / root_folder
                root_path.mkdir(parents=True, exist_ok=True)

                for line in lines[1:]:
                    clean_line = self._clean_line(line)
                    if not clean_line:
                        continue

                    if clean_line.endswith("/"):
                        folder_name = clean_line.rstrip("/")
                        self._handle_folder_creation(folder_name, root_path)
                    else:
                        self._handle_file_creation(clean_line, root_path)

        except Exception as e:
            self.logger.error(
                f"Failed to process PBS file: {pbs_file_path}. Error: {str(e)}"
            )
            raise

    def _get_base_folder_from_pbs(self, first_line: str) -> str:
        return first_line.strip().rstrip("/")

    def _get_indent_level(self, line: str) -> int:
        leading_spaces = len(line) - len(line.lstrip())
        return leading_spaces // 4

    def _clean_line(self, line: str) -> str:
        return line.replace("├──", "").replace("└──", "").replace("│", "").strip()

    def _handle_folder_creation(self, folder_name: str, root_path: Path) -> None:
        folder_path = root_path / folder_name
        folder_path.mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {folder_path.as_posix()}")

    def _handle_file_creation(self, file_name: str, root_path: Path) -> None:
        file_path = root_path / file_name
        file_path.touch(exist_ok=True)
        self.logger.info(f"Created file: {file_path.as_posix()}")
