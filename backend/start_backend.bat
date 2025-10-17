@echo off
echo ============================================================
echo Healthcare Symptom Checker - Backend Startup (Windows)
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo Python found!
python --version
echo.

REM Check if API key is set
if "%GEMINI_API_KEY%"=="" (
    echo ============================================================
    echo ERROR: GEMINI_API_KEY not set!
    echo ============================================================
    echo.
    echo Please set your API key first:
    echo   set GEMINI_API_KEY=your_api_key_here
    echo.
    echo Get your API key at:
    echo   https://makersuite.google.com/app/apikey
    echo.
    echo Then run this script again.
    echo ============================================================
    pause
    exit /b 1
)

echo API Key: Set (hidden for security)
echo.

REM Install dependencies if needed
echo Checking dependencies...
pip install -q fastapi uvicorn pydantic google-generativeai python-multipart aiofiles

echo.
echo ============================================================
echo Starting Backend Server...
echo ============================================================
echo.
echo Server URL: http://localhost:8000
echo API Docs: http://localhost:8000/docs
echo.
echo Press CTRL+C to stop the server
echo ============================================================
echo.

REM Start the server
cd backend
python app.py

pause