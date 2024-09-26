# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# main.py

"""
Main entry point for the Structra application.

This module handles argument parsing, logging setup, and initiates the process
of generating file structures based on input project structure files (PBS).

Author: Jonas Zeihe
"""


import argparse
import sys
from pathlib import Path
from structra.logger_config import setup_logger
from structra.structure_processor import StructureProcessor


def main(args=None):
    """
    Main function that sets up logging, processes input files, and handles errors.

    Args:
        args (list, optional): Command-line arguments for testing purposes. Defaults to None.
    """
    try:
        arguments = parse_arguments(args)

        logger = setup_logger(log_to_file=arguments.logging)

        logger.info("Structra started.")

        if not validate_files(arguments.files, logger):
            logger.error("File validation failed.")
            sys.exit(1)

        process_files(arguments.files, logger)

        logger.info("Structra completed successfully.")

    except Exception as error:
        handle_error(logger, error)


def parse_arguments(args=None):
    """
    Parses command-line arguments.

    Args:
        args (list, optional): Arguments passed for testing. Defaults to None.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Structra - File Structure Generator")
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs="+",
        help="Path(s) to the .txt file(s) defining the structure(s).",
    )
    parser.add_argument(
        "--logging", action="store_true", help="Enable logging to file and console"
    )
    return parser.parse_args(args)


def validate_files(files: list[str], logger) -> bool:
    """
    Validates if the provided files exist and have the correct .txt format.

    Args:
        files (list[str]): List of file paths as strings.
        logger (logging.Logger): Logger instance for logging.

    Returns:
        bool: True if all files are valid, else False.
    """
    invalid_files = [
        file for file in files if not Path(file).exists() or not file.endswith(".txt")
    ]
    if invalid_files:
        for file in invalid_files:
            logger.error(f"File '{file}' does not exist or has an invalid format.")
        return False
    return True


def process_files(files: list[str], logger):
    """
    Processes the given list of structure files and generates the folder structures.

    Args:
        files (list[str]): List of structure file paths.
        logger (logging.Logger): Logger instance for logging.
    """
    for file_path in files:
        file_path = Path(file_path)
        root_folder_name = get_root_folder_name(file_path)
        output_directory = Path.cwd() / root_folder_name

        logger.info(f"Output directory set to: {output_directory}")

        processor = StructureProcessor(output_directory, logger)
        processor.process_pbs_file(file_path)


def get_root_folder_name(file_path: Path) -> str:
    """
    Extracts the name of the root folder from the first line of the structure file.

    Args:
        file_path (Path): The path to the structure definition file.

    Returns:
        str: The name of the root folder.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        first_line = file.readline().strip()
        root_folder = first_line.split("/")[0]
    return root_folder


def handle_error(logger, error):
    """
    Handles errors by logging them or printing if the logger is unavailable.

    Args:
        logger (logging.Logger): Logger instance.
        error (Exception): Exception raised during execution.
    """
    if logger:
        logger.error(f"An unexpected error occurred: {str(error)}")
    else:
        print(f"An unexpected error occurred: {str(error)}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
