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
    Main function to initiate the Structra application.
    Parses arguments, sets up logging, validates files, and processes them.

    Args:
        args (list, optional): Command-line arguments to parse. Defaults to None.
    """
    logger = None
    try:
        arguments = parse_arguments(args)

        logger = setup_logger(log_to_file=arguments.logging)
        logger.info("Structra started.")

        if not validate_files(arguments.files, logger):
            logger.error("File validation failed.")
            sys.exit(1)

        process_files(arguments.files, logger, arguments.root_folder)

        logger.info("Structra completed successfully.")
    except FileNotFoundError as file_error:
        handle_error(logger, f"File not found: {file_error}")
    except IsADirectoryError as dir_error:
        handle_error(logger, f"Expected a file but found a directory: {dir_error}")
    except Exception as error:  # Catching general exception as a fallback
        handle_error(logger, error)


def parse_arguments(args=None):
    """
    Parses command-line arguments for the Structra application.

    Args:
        args (list, optional): Arguments to parse. Defaults to None.

    Returns:
        Namespace: Parsed command-line arguments.
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
    parser.add_argument(
        "--root-folder",
        type=str,
        default="structra_output",
        help="Name of the root folder where the structure will be generated.",
    )
    return parser.parse_args(args)


def validate_files(files: list[str], logger) -> bool:
    """
    Validates the provided file paths to ensure they exist and have the correct format.

    Args:
        files (list[str]): List of file paths to validate.
        logger (Logger): Logger instance for logging errors.

    Returns:
        bool: True if all files are valid, False otherwise.
    """
    invalid_files = [
        file for file in files if not Path(file).exists() or not file.endswith(".txt")
    ]
    if invalid_files:
        for file in invalid_files:
            logger.error(f"File '{file}' does not exist or has an invalid format.")
        return False
    return True


def process_files(files: list[str], logger, root_folder_name: str):
    """
    Processes the list of files to generate the folder and file structure.

    Args:
        files (list[str]): List of file paths.
        logger (Logger): Logger instance for logging.
        root_folder_name (str): Name of the root folder where the structure will be generated.
    """
    output_directory = Path.cwd() / root_folder_name
    logger.info(f"Output directory set to: {output_directory}")

    for file_path_str in files:
        file_path = Path(file_path_str)

        processor = StructureProcessor(output_directory, logger)
        processor.process_pbs_file(file_path)


def handle_error(logger, error_message):
    """
    Handles errors by logging or printing them to the console.

    Args:
        logger (Logger): Logger instance for logging errors, if available.
        error_message (str): The error message to log or print.
    """
    if logger:
        logger.error(f"An unexpected error occurred: {error_message}")
    else:
        print(f"An unexpected error occurred: {error_message}", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    main()
