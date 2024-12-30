@echo off
REM ----------------------------------------------------------------------
REM Universal Test Runner - Run All Tests
REM Executes all tests in the project and generates a coverage report.
REM 
REM Copyright (c) 2024 Jonas Zeihe
REM Licensed under the MIT License. See LICENSE file in the project root for details.
REM 
REM Project URL: https://github.com/jonaszeihe/structra
REM Contact: JonasZeihe@gmail.com
REM ----------------------------------------------------------------------

cls

REM Activate the virtual environment
call ..\..\venv\Scripts\activate

REM Set the working directory to the project root (one level above the test_runners folder)
cd /d %~dp0..\

REM Run all tests with coverage
echo Running all tests with coverage...
coverage run --source=structra -m unittest discover -s tests -p "test_*.py"
coverage report -m

REM Inform the user
echo.
echo All tests completed successfully. Check the results above.
echo Press any key to deactivate the virtual environment and close this window...
pause > nul

REM Deactivate the virtual environment
deactivate
