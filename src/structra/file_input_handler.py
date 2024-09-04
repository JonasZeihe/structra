# -----------------------------------------------------------------------------
# Structra - A tool to generate folder and file structures based on input text files
#
# Copyright (c) 2024 Jonas Zeihe
# Licensed under the MIT License. See LICENSE file in the project root for details.
#
# Project URL: https://github.com/jonaszeihe/structra
# Contact: JonasZeihe@gmail.com
# -----------------------------------------------------------------------------

# file_input_handler.py

"""
This module handles the file input for the project structure generator. 
It processes .txt files that are dragged and dropped into the application.
"""

import os
from tkinterdnd2 import TkinterDnD, DND_FILES
from structra.file_handler import process_structure


def handle_file_input():
    """
    Handles the file input for the application by processing .txt files.
    """
    root = TkinterDnD.Tk()
    root.withdraw()  # Hide the GUI as it is not needed

    def process_dropped_files(data):
        """
        Processes the files dropped into the application.

        Args:
            data (str): The file paths that were dropped.
        """
        file_paths = root.tk.splitlist(data)

        for file_path in file_paths:
            if file_path.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    base_dir = os.path.splitext(os.path.basename(file_path))[0]
                    os.makedirs(base_dir, exist_ok=True)
                    process_structure(base_dir, lines)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", lambda e: process_dropped_files(e.data))

    root.mainloop()
