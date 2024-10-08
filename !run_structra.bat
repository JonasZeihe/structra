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

REM Running structra.exe without logging (For development purposes)
echo Running structra.exe without logging...
structra.exe

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul