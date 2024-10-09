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
    """
    Processes Project Structure (PBS) files to generate folders and files according
    to the hierarchy defined in the input file.
    """

    def __init__(self, output_directory: Path, logger: logging.Logger):
        """
        Initializes the StructureProcessor with the output directory and logger.

        Args:
            output_directory (Path): The root directory where the structure will be generated.
            logger (logging.Logger): Logger for logging messages and errors.
        """
        self.output_directory = output_directory
        self.logger = logger

    def process_pbs_file(self, pbs_file_path: Path) -> None:
        """
        Processes a PBS (Project Structure) file and generates the corresponding folders and files.

        Args:
            pbs_file_path (Path): The path to the PBS file.
        """
        try:
            lines = self._read_pbs_file(pbs_file_path)

            root_folder = self._get_root_folder(lines[0])
            root_path = self.output_directory / root_folder
            self._create_directory(root_path)

            path_stack = [root_path]

            for line in lines[1:]:
                clean_line = self._clean_line(line)

                if clean_line == root_folder:
                    continue

                level = self._count_hierarchy_level(line)
                self._adjust_path_stack(path_stack, level)

                full_path = path_stack[-1] / clean_line.rstrip("/")

                if clean_line.endswith("/"):
                    self._create_directory(full_path)
                    path_stack.append(full_path)
                else:
                    self._create_file(full_path)

        except FileNotFoundError:
            self.logger.error(f"PBS file '{pbs_file_path}' not found.")
        except OSError as e:
            self.logger.error(f"Error processing PBS file '{pbs_file_path}': {e}")

    def _read_pbs_file(self, pbs_file_path: Path) -> list[str]:
        """
        Reads the contents of a PBS file.

        Args:
            pbs_file_path (Path): The path to the PBS file.

        Returns:
            list[str]: A list of lines from the file.
        """
        self.logger.info(f"Reading PBS file: {pbs_file_path}")
        with open(pbs_file_path, "r", encoding="utf-8") as file:
            return file.readlines()

    def _get_root_folder(self, first_line: str) -> str:
        """
        Extracts the root folder name from the first line of the PBS file.

        Args:
            first_line (str): The first line of the PBS file.

        Returns:
            str: The root folder name.
        """
        return first_line.strip().rstrip("/")

    def _create_directory(self, directory_path: Path) -> None:
        """
        Creates a directory if it doesn't exist.

        Args:
            directory_path (Path): The path to the directory.
        """
        try:
            directory_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Directory created: {directory_path}")
        except OSError as e:
            self.logger.error(f"Failed to create directory '{directory_path}': {e}")

    def _create_file(self, file_path: Path) -> None:
        """
        Creates an empty file if it doesn't exist.

        Args:
            file_path (Path): The path to the file.
        """
        try:
            file_path.touch(exist_ok=True)
            self.logger.info(f"File created: {file_path}")
        except OSError as e:
            self.logger.error(f"Failed to create file '{file_path}': {e}")

    def _adjust_path_stack(self, path_stack: list[Path], level: int) -> None:
        """
        Adjusts the path stack based on the hierarchy level.

        Args:
            path_stack (list[Path]): The stack of paths representing the current directory structure.
            level (int): The current hierarchy level.
        """
        while len(path_stack) > level + 1:
            path_stack.pop()

    def _clean_line(self, line: str) -> str:
        """
        Cleans up a line by removing structure symbols and leading spaces.

        Args:
            line (str): The line to clean.

        Returns:
            str: The cleaned line.
        """
        return line.lstrip("├──│└── ").strip()

    def _count_hierarchy_level(self, line: str) -> int:
        """
        Calculates the hierarchy level based on leading symbols or spaces.

        Args:
            line (str): The line to calculate the hierarchy level for.

        Returns:
            int: The calculated hierarchy level.
        """
        indent_level = len(line) - len(line.lstrip(" │"))
        return indent_level // 4
