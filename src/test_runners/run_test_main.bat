@echo off
REM ----------------------------------------------------------------------
REM Structra - Test Runner for test_main.py
REM Runs the test with coverage in a virtual environment.
REM 
REM Copyright (c) 2024 Jonas Zeihe 
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra 
REM Contact: JonasZeihe@gmail.com 
REM ----------------------------------------------------------------------

@echo off
cls

REM Activate the virtual environment
call ..\..\venv\Scripts\activate

REM Set the working directory to the project root (one level above the test_runners folder)
cd /d %~dp0..\

REM Running test_main.py with coverage
echo Running test_main.py with coverage...
coverage run --source=structra -m unittest tests.test_main
coverage report -m


REM Pause to keep the window open until the user presses a key 
echo.
echo Press any key to deactivate the virtual environment and close this window...
pause > nul

REM Deactivate the virtual environment
deactivate
