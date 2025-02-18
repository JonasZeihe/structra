@echo off
REM ----------------------------------------------------------------------
REM Universal Run Script
REM Runs the application within its virtual environment.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/noctua
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

REM Activate the virtual environment
call venv\Scripts\activate

REM Set PYTHONPATH to include the src directory
set PYTHONPATH=%~dp0src

REM Run the application explicitly from the main module
echo Running the application...
python -m structra.main %*

REM Inform the user
echo Application execution complete. Press any key to deactivate the virtual environment and exit...
pause > nul

REM Deactivate the virtual environment
deactivate

