@echo off
REM ----------------------------------------------------------------------
REM Structra - A tool to generate folder and file structures based on input text files
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

REM Running structra.exe with the provided file(s)
echo Running structra.exe with logging...
structra.exe --logging %*

REM Pause to keep the window open until the user presses a key
echo.
echo Press any key to exit...
pause > nul
