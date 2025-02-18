@echo off
REM ----------------------------------------------------------------------
REM Enhanced Project Initializer
REM Ensures complete dependency tracking and synchronization.
REM ----------------------------------------------------------------------

REM Check if the virtual environment already exists
IF NOT EXIST venv (
    echo Creating virtual environment...
    python -m venv venv
) ELSE (
    echo Virtual environment already exists.
)

REM Activate the virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Upgrade pip to the latest version
echo Upgrading pip to the latest version...
pip install --upgrade pip

REM Check if pipreqsnb is installed
pip show pipreqsnb > nul 2>&1
IF ERRORLEVEL 1 (
    echo Installing pipreqsnb for dependency generation...
    pip install pipreqsnb
)

REM Generate or update requirements.txt
IF NOT EXIST requirements.txt (
    echo No requirements.txt found. Generating one from the codebase...
    pipreqsnb . --force
) ELSE (
    echo Using existing requirements.txt.
)

REM Install dependencies from requirements.txt
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

REM Add missing dependencies
echo Verifying installed dependencies...
pip install py-cpuinfo

REM Synchronize final environment with freeze
echo Freezing the full environment to update requirements.txt...
pip freeze > requirements.txt

REM Inform the user
echo Virtual environment setup complete! Press any key to deactivate and exit...
pause > nul

REM Deactivate the virtual environment
deactivate
