@echo off
echo ============================================
echo  Ushnik Technologies Interactive Chatbot
echo  Starting server...
echo ============================================
echo.

cd /d "%~dp0"

REM Check if venv exists
if not exist "venv" (
    echo [1/3] Creating virtual environment...
    python -m venv venv
    echo Virtual environment created.
) else (
    echo [1/3] Virtual environment found.
)

REM Activate venv
call venv\Scripts\activate.bat

REM Install dependencies
echo [2/3] Installing dependencies...
pip install -r requirements.txt --quiet

REM Run the server
echo [3/3] Starting server on http://localhost:8000
echo.
echo ========================================
echo   Open: http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

pause
