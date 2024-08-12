"""
main.py

This module sets up the logging configuration and starts the GUI event loop.
It is the entry point of the application.
"""

from gui import create_gui
from logger_config import setup_logger


def main():
    """
    Main function to set up logging and start the GUI.
    """
    setup_logger()  # Set up logging
    root = create_gui()  # Create the GUI
    root.mainloop()  # Start the GUI event loop


if __name__ == "__main__":
    main()
