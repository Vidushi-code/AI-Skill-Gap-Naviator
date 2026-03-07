@echo off
echo ================================
echo AI Skill Gap Navigator - Startup
echo ================================
echo.

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo Virtual environment not found. Creating...
    python -m venv venv
    echo Virtual environment created.
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if needed
echo.
echo Checking dependencies...
pip install -q -r requirements.txt

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please create .env file with your CEREBRAS_API_KEY
    echo.
    pause
    exit /b
)

REM Start the backend server
echo.
echo Starting FastAPI server...
echo Server will be available at: http://localhost:8000
echo API docs will be available at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run_backend.py
