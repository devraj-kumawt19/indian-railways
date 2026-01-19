@echo off
REM ====================================================================================
REM INDIAN RAILWAYS AI SYSTEM - DEPLOYMENT & ACCESS HUB
REM Professional Menu System for Application Access & Documentation
REM ====================================================================================

setlocal enabledelayedexpansion
cd /d "%~dp0"

:menu
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║                                                                                ║
echo ║        🚂 INDIAN RAILWAYS AI DETECTION SYSTEM - CONTROL PANEL v1.0.0            ║
echo ║                  Enterprise Edition | Production Ready                          ║
echo ║                                                                                ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.
echo ┌─ QUICK ACCESS ─────────────────────────────────────────────────────────────────┐
echo │                                                                                │
echo │  1) 🚀  LAUNCH APPLICATION (Recommended)                                       │
echo │         Start the AI Detection System at http://localhost:8501                 │
echo │                                                                                │
echo │  2) 📊  OPEN DASHBOARD                                                         │
echo │         View the professional landing page with all links                      │
echo │                                                                                │
echo │  3) 📱  NETWORK ACCESS                                                         │
echo │         Access app from mobile/other devices (if on same network)              │
echo │                                                                                │
echo ├─ DOCUMENTATION ───────────────────────────────────────────────────────────────│
echo │                                                                                │
echo │  4) 📖  README (Project Overview)                                              │
echo │  5) 🏗️   SYSTEM OVERVIEW (Architecture & Features)                              │
echo │  6) ⚡  QUICK START GUIDE (Get Started in 60 Seconds)                           │
echo │  7) 🚀  DEPLOYMENT GUIDE (Production Setup)                                    │
echo │  8) 🔧  ERROR HANDLING (Troubleshooting)                                       │
echo │  9) 🔗  QUICK LINKS (Reference Guide)                                          │
echo │                                                                                │
echo ├─ UTILITIES ────────────────────────────────────────────────────────────────────│
echo │                                                                                │
echo │  10) 🔄 RESTART APPLICATION                                                    │
echo │  11) 🗑️   CLEAR CACHE & RESTART                                                │
echo │  12) 📝 OPEN CONFIGURATION (startup_config.json)                               │
echo │  13) ⚙️   SETUP GUIDE & LAUNCH                                                 │
echo │                                                                                │
echo ├─ SYSTEM ──────────────────────────────────────────────────────────────────────│
echo │                                                                                │
echo │  14) 🔍 CHECK SYSTEM STATUS                                                    │
echo │  15) 📁 OPEN PROJECT FOLDER                                                    │
echo │  16) 📋 VIEW REQUIREMENTS                                                      │
echo │                                                                                │
echo │  0)  ❌ EXIT                                                                    │
echo │                                                                                │
echo └────────────────────────────────────────────────────────────────────────────────┘
echo.
echo ┌─ SYSTEM STATUS ────────────────────────────────────────────────────────────────┐

REM Check if Python is available
python --version >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo │ ✅ Python: INSTALLED                                                        │
) else (
    echo │ ❌ Python: NOT FOUND                                                        │
)

REM Check if venv exists
if exist .venv (
    echo │ ✅ Virtual Environment: READY                                              │
) else (
    echo │ ⚠️  Virtual Environment: NOT INITIALIZED                                   │
)

REM Check if requirements are met
if exist requirements.txt (
    echo │ ✅ Requirements File: FOUND                                                │
) else (
    echo │ ⚠️  Requirements File: NOT FOUND                                           │
)

REM Check if app exists
if exist src\ui\app.py (
    echo │ ✅ Application: FOUND                                                      │
) else (
    echo │ ❌ Application: NOT FOUND                                                  │
)

echo │                                                                                │
echo └────────────────────────────────────────────────────────────────────────────────┘
echo.

set /p choice="Enter your choice (0-16): "

if "%choice%"=="1" goto launch
if "%choice%"=="2" goto dashboard
if "%choice%"=="3" goto network
if "%choice%"=="4" goto readme
if "%choice%"=="5" goto system
if "%choice%"=="6" goto quickstart
if "%choice%"=="7" goto deployment
if "%choice%"=="8" goto errors
if "%choice%"=="9" goto links
if "%choice%"=="10" goto restart
if "%choice%"=="11" goto clearcache
if "%choice%"=="12" goto config
if "%choice%"=="13" goto setup
if "%choice%"=="14" goto status
if "%choice%"=="15" goto explorer
if "%choice%"=="16" goto requirements
if "%choice%"=="0" goto exit
goto menu

:launch
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  🚀 LAUNCHING APPLICATION...                                                   ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

if not exist .venv (
    echo ⚠️  Virtual environment not found. Creating...
    python -m venv .venv
)

echo ✅ Activating virtual environment...
call .venv\Scripts\activate.bat

echo ✅ Installing/updating dependencies...
pip install -r requirements.txt --quiet

echo ✅ Clearing Streamlit cache...
streamlit cache clear

echo.
echo ✨ Starting application...
echo.
echo 🌐 The application will open at: http://localhost:8501
echo 📱 Network access: http://192.168.29.171:8501
echo.
echo Press Ctrl+C to stop the application
echo.

streamlit run src/ui/app.py
pause
goto menu

:dashboard
cls
echo Opening dashboard...
start index.html
timeout /t 2
goto menu

:network
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  📱 NETWORK ACCESS INFORMATION                                                 ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.
echo To access from another device on the same network:
echo.
ipconfig | findstr /R "IPv4 Address"
echo.
echo Use: http://[YOUR_IP]:8501
echo.
pause
goto menu

:readme
cls
if exist README.md (
    start README.md
    timeout /t 1
) else (
    echo README.md not found
    pause
)
goto menu

:system
cls
if exist SYSTEM_OVERVIEW.md (
    start SYSTEM_OVERVIEW.md
    timeout /t 1
) else (
    echo SYSTEM_OVERVIEW.md not found
    pause
)
goto menu

:quickstart
cls
if exist QUICK_START_GUIDE.md (
    start QUICK_START_GUIDE.md
    timeout /t 1
) else (
    echo QUICK_START_GUIDE.md not found
    pause
)
goto menu

:deployment
cls
if exist DEPLOYMENT_GUIDE.md (
    start DEPLOYMENT_GUIDE.md
    timeout /t 1
) else (
    echo DEPLOYMENT_GUIDE.md not found
    pause
)
goto menu

:errors
cls
if exist ERROR_HANDLING_GUIDE.md (
    start ERROR_HANDLING_GUIDE.md
    timeout /t 1
) else (
    echo ERROR_HANDLING_GUIDE.md not found
    pause
)
goto menu

:links
cls
if exist LINKS.md (
    start LINKS.md
    timeout /t 1
) else (
    echo LINKS.md not found
    pause
)
goto menu

:restart
cls
echo Restarting application...
taskkill /IM streamlit.exe /F 2>nul
timeout /t 2
goto launch

:clearcache
cls
echo.
echo Clearing Streamlit cache...
call .venv\Scripts\activate.bat
streamlit cache clear
echo ✅ Cache cleared
timeout /t 2
goto launch

:config
cls
if exist startup_config.json (
    start startup_config.json
    timeout /t 1
) else (
    echo Configuration file not found
    pause
)
goto menu

:setup
cls
if exist SETUP_AND_LAUNCH.md (
    start SETUP_AND_LAUNCH.md
    timeout /t 1
) else (
    echo Setup guide not found
    pause
)
goto menu

:status
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  🔍 SYSTEM STATUS                                                              ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

echo ✅ Checking system configuration...
python --version
pip --version
echo.

echo ✅ Checking project structure...
if exist src\ui\app.py echo [OK] Application found
if exist .venv echo [OK] Virtual environment found
if exist requirements.txt echo [OK] Requirements file found
if exist data echo [OK] Data folder found
if exist models echo [OK] Models folder found
echo.

echo ✅ Documentation status...
if exist README.md echo [OK] README.md
if exist SYSTEM_OVERVIEW.md echo [OK] SYSTEM_OVERVIEW.md
if exist QUICK_START_GUIDE.md echo [OK] QUICK_START_GUIDE.md
if exist DEPLOYMENT_GUIDE.md echo [OK] DEPLOYMENT_GUIDE.md
if exist ERROR_HANDLING_GUIDE.md echo [OK] ERROR_HANDLING_GUIDE.md
if exist LINKS.md echo [OK] LINKS.md
echo.

pause
goto menu

:explorer
start .
goto menu

:requirements
cls
if exist requirements.txt (
    type requirements.txt
) else (
    echo requirements.txt not found
)
echo.
pause
goto menu

:exit
cls
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  👋 Thank you for using Indian Railways AI Detection System                     ║
echo ║                                                                                ║
echo ║  For support: support@example.com                                              ║
echo ║  Website: https://example.com                                                  ║
echo ║                                                                                ║
echo ║  Version: 1.0.0 | Production Ready | © 2026                                    ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.
exit /b 0
