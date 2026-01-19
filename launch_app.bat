@echo off
REM Indian Railways AI System - Application Launcher
REM This script launches the application with all necessary setup

title Indian Railways AI - System Launcher
color 0A

echo.
echo ============================================================================
echo.
echo   🚂 Indian Railways AI Detection System - Enterprise Edition
echo   Version 1.0.0 | Production Ready
echo.
echo ============================================================================
echo.

REM Check if virtual environment exists
if not exist ".venv" (
    echo ⚠️  Virtual environment not found!
    echo Creating virtual environment...
    python -m venv .venv
    echo ✅ Virtual environment created
)

REM Activate virtual environment
echo.
echo 🔄 Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install/update dependencies
echo.
echo 📦 Checking dependencies...
pip install -q -r requirements.txt

REM Clear any cached files
echo.
echo 🧹 Clearing cache...
if exist "__pycache__" rmdir /s /q __pycache__
if exist "src\__pycache__" rmdir /s /q src\__pycache__

REM Start the application
echo.
echo 🚀 Launching Indian Railways AI System...
echo.
echo ============================================================================
echo.
echo   📍 Access the application at:
echo   • Local:   http://localhost:8501
echo   • Network: http://192.168.x.x:8501
echo.
echo   ✅ System Status: OPERATIONAL
echo   ⚡ Version: 1.0.0
echo   📊 Mode: Production
echo.
echo ============================================================================
echo.
echo Press Ctrl+C to stop the application
echo.

REM Launch Streamlit app
streamlit run src/ui/app.py --server.port=8501 --logger.level=info

pause
