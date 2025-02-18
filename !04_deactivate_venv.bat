@echo off
REM ----------------------------------------------------------------------
REM Virtual Environment Deactivator
REM Deactivates the virtual environment if it is currently active.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/project-template
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Check if the virtual environment exists
IF NOT EXIST venv (
    echo Virtual environment not found. Nothing to deactivate.
    pause
    exit /b 0
)

REM Deactivating the virtual environment
echo Attempting to deactivate the virtual environment...
call venv\Scripts\deactivate 2>nul || (
    echo No active virtual environment found to deactivate.
    pause
    exit /b 0
)

echo Virtual environment deactivated successfully!
pause
