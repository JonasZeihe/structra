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

REM Running test_logger_config.py
echo Running test_logger_config.py...
python -m unittest tests.test_logger_config

REM Pause to keep the window open until the user presses a key 
echo.
echo Press any key to exit...
pause > nul
