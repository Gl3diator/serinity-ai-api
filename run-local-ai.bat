@echo off
setlocal enabledelayedexpansion

REM Get the directory where this script is located
set "PROJECT_DIR=%~dp0"
set "VENV_DIR=%PROJECT_DIR%.venv"
set "HOST=127.0.0.1"
set "PORT=8001"

cd /d "%PROJECT_DIR%"

REM Check if virtual environment exists
if not exist "%VENV_DIR%" (
    echo Virtual environment not found at: %VENV_DIR%
    echo Create it first with:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    exit /b 1
)

REM Activate the virtual environment
call "%VENV_DIR%\Scripts\activate.bat"
if errorlevel 1 (
    echo Failed to activate virtual environment
    exit /b 1
)

REM Check if main.py exists
if not exist "%PROJECT_DIR%app\main.py" (
    echo FastAPI entrypoint not found: %PROJECT_DIR%app\main.py
    exit /b 1
)

echo Starting Serinity AI API on http://%HOST%:%PORT%
uvicorn app.main:app --reload --host %HOST% --port %PORT%
