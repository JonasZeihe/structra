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

@echo off
cls

REM Set the working directory to the project root (one level above the test_runners folder)
cd /d %~dp0..\

REM Run all tests with coverage
echo Running all tests with coverage...

coverage run --source=structra -m unittest discover -s tests -p "test_*.py"
coverage report -m

REM Optional: Generate an HTML report
coverage html

echo.
echo Coverage report complete. Check the HTML report for detailed results in the 'htmlcov' directory.
echo Press any key to exit...
pause > nul
