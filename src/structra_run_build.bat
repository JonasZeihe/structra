@echo off
REM -----------------------------------------------------------------------------
REM Structra - A tool to generate folder and file structures based on input text files
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM -----------------------------------------------------------------------------

pyinstaller --onefile --name structra --specpath . --clean structra/main.py
