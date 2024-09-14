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
This module sets up the logging configuration and processes input .txt files
to generate the corresponding directory and file structures.
It is the entry point of the application.
"""

import argparse
from pathlib import Path
from structra.logger_config import setup_logger, save_logs_to_file
from structra.structure_parser import handle_files


def parse_arguments():
    """
    Parses command-line arguments.

    Returns:
        Namespace: Parsed arguments.
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
        "-l", "--logging", action="store_true", help="Enable logging to file"
    )
    parser.add_argument(
        "--output", type=str, default=None, help="Specify output directory"
    )
    return parser.parse_args()


def main(args=None):
    """
    Main function to set up logging and process input .txt files.
    """
    if args is None:
        args = parse_arguments()

    logger, log_stream = setup_logger()
    logger.info("Logger initialized successfully.")

    handle_files(args.files)

    if args.logging:
        output_dir = Path(args.output) if args.output else Path(".")
        save_logs_to_file(log_stream, output_dir)
        logger.info("Logs saved to %s", output_dir)


if __name__ == "__main__":
    main()
