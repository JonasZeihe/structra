"""
file_handler.py

This module contains functions to process file structures and handle file drops
in the drag-and-drop GUI.
"""

import os
import logging


def process_structure(base_path, lines):
    path_stack = [base_path]

    for line in lines:
        stripped_line = line.rstrip()
        if not stripped_line:
            continue

        # Berechne die Tiefe anhand der führenden Leerzeichen oder der Baumstruktur
        depth = (len(line) - len(line.lstrip())) // 4

        # Entferne unerwünschte Baumstrukturzeichen und führende Leerzeichen
        name = (
            stripped_line.replace("├── ", "")
            .replace("└── ", "")
            .replace("│", "")
            .strip()
        )

        # Passe den Pfad-Stack auf die korrekte Ebene an
        while len(path_stack) > depth + 1:
            path_stack.pop()

        current_path = os.path.join(path_stack[-1], name)

        try:
            # Erkennen, ob der aktuelle Name ein Verzeichnis ist (endet auf "/")
            if not os.path.splitext(current_path)[1] and not current_path.endswith(
                ("/")
            ):
                if not os.path.exists(current_path):
                    os.makedirs(current_path)
                    logging.info("Created directory: %s", current_path)
                path_stack.append(current_path)
            else:
                # Es handelt sich um eine Datei
                if not os.path.exists(current_path):
                    os.makedirs(os.path.dirname(current_path), exist_ok=True)
                    with open(current_path, "w", encoding="utf-8"):
                        pass
                    logging.info("Created file: %s", current_path)

        except PermissionError as e:
            logging.error("Permission error with file %s: %s", current_path, e)
        except OSError as e:
            logging.error("OS error with file %s: %s", current_path, e)
        except Exception as e:
            logging.error("Error processing file %s: %s", current_path, e)


def handle_files(files, root):
    """
    Processes the dropped file(s) and creates the directory structure.

    Args:
        files (str): Dropped file paths in a format recognized by TkinterDnD.
        root (Tk): The root TkinterDnD window instance.
    """
    files = root.tk.splitlist(files)
    for file_path in files:
        if file_path.endswith(".txt"):
            try:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.readlines()
                    if not content:
                        logging.warning("File %s is empty", file_path)
                        continue

                    project_name = content[0].strip().rstrip("/")
                    base_path = os.path.join(os.path.dirname(file_path), project_name)
                    os.makedirs(base_path, exist_ok=True)

                    logging.info(
                        "Starting processing for project: %s, base path: %s",
                        project_name,
                        base_path,
                    )
                    process_structure(base_path, content[1:])
                    logging.info(
                        'Project structure for "%s" created successfully at %s',
                        project_name,
                        base_path,
                    )

            except FileNotFoundError as e:
                logging.error("File not found: %s", file_path)
            except PermissionError as e:
                logging.error("Permission error with file %s: %s", file_path, e)
            except OSError as e:
                logging.error("OS error with file %s: %s", file_path, e)
            except Exception as e:
                logging.error("Error processing file %s: %s", file_path, e)

    root.quit()
