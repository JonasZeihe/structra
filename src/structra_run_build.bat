@echo off
REM ----------------------------------------------------------------------
REM Structra - Build Script
REM Creates a standalone executable for the project using PyInstaller.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Activate the virtual environment
call ..\venv\Scripts\activate

REM Start the build process
echo Building the Structra executable...
pyinstaller --onefile --name structra --specpath . --clean structra/main.py

REM Inform the user about the build location
echo.
echo Build complete! The executable can be found in the "dist" folder.
echo Press any key to deactivate the virtual environment and close this window...
pause > nul

REM Deactivate the virtual environment
deactivate
