@echo off
REM ----------------------------------------------------------------------
REM Universal Application Runner
REM Runs the application within the virtual environment, allowing drag-and-drop for input files.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Check if at least one argument (file) is provided
if "%~1"=="" (
    echo No file provided. Please drag and drop a .txt file onto this batch script.
    pause
    exit /b 1
)

REM Activate the virtual environment
call venv\Scripts\activate

REM Set PYTHONPATH to include the src directory
set PYTHONPATH=%~dp0src

REM Run the application with the provided file(s)
echo Running the application with input files...
python src/structra/main.py %*

REM Inform the user
echo Application execution complete. Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate
