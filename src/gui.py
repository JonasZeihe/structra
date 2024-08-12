"""
gui.py

This module sets up the graphical user interface for the drag-and-drop project 
structure generator.
"""

import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
from file_handler import handle_files


def create_gui():
    """
    Sets up the GUI for the application.

    Returns:
        Tk: The root TkinterDnD window instance.
    """
    root = TkinterDnD.Tk()
    root.title("Drag and Drop Project Structure Generator")
    root.geometry("600x200")

    label = tk.Label(root, text="Drag and drop your .txt file(s) here", pady=20)
    label.pack(fill=tk.BOTH, expand=True)

    root.drop_target_register(DND_FILES)
    root.dnd_bind("<<Drop>>", lambda e: handle_files(e.data, root))

    return root
