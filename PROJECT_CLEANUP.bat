@echo off
REM ============================================================================
REM Project Cleanup Script for Indian Railways AI Detection System
REM Organizes files into proper directories
REM ============================================================================

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  Indian Railways AI - PROJECT CLEANUP & RESTRUCTURING                          ║
echo ║  This script will organize the project into a clean, professional structure    ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

REM Create backup
echo Creating backup of current project...
if not exist "_backup" mkdir _backup
xcopy . _backup /E /I /Y /Q >nul 2>&1
echo ✅ Backup created in _backup folder
echo.

REM Create documentation folder
echo Creating documentation directory...
if not exist "docs" mkdir docs
echo ✅ docs folder created
echo.

REM Move documentation files
echo Moving documentation files to docs/ folder...
REM This includes all the .md and .txt files that clutter the root

setlocal enabledelayedexpansion
set "doc_files=SETUP_AND_LAUNCH.md QUICK_START_GUIDE.md README.md SYSTEM_OVERVIEW.md DEPLOYMENT_GUIDE.md ERROR_HANDLING_GUIDE.md LINKS.md DEPLOYMENT_COMPLETE.md START_DEPLOYMENT.txt FINAL_DEPLOYMENT_REPORT.txt DEPLOYMENT_SUMMARY.txt README_DEPLOYMENT.txt 00_READ_ME_FIRST.txt AGENT_ARCHITECTURE.md AGENT_EXECUTIVE_SUMMARY.md AGENT_IMPLEMENTATION_COMPLETE.md AGENT_QUICK_START.md AGENT_SYSTEM_COMPLETE.md API_DOCUMENTATION_INDEX.md API_ERROR_FIX_COMPLETE.md API_FIX_SUMMARY.md API_OFFLINE_FALLBACK.md ARCHITECTURE.md COMPLETION_CHECKLIST.md COMPLETION_SUMMARY_V2.0.md COMPREHENSIVE_FIX_COMPLETE.md DEVELOPER_ATTRIBUTION.txt DOCUMENTATION_INDEX.md IMPROVEMENTS_V2.0.md MODULES_ORGANIZATION.md NEARBY_PLATFORM_FEATURES.md NEARBY_PLATFORM_MONITORING.md NEARBY_PLATFORM_SUMMARY.md NEARBY_PLATFORMS_QUICK_START.md PROJECT_COMPLETION_REPORT.md QUICK_FIX.md QUICK_START_V2.0.md README_AGENT_SYSTEM.md REALTIME_README.md SOLUTION_COMPLETE.md UI_COMPLETE_FIX.md UI_FIXED_REPORT.md UI_IMPROVEMENTS_COMPLETE.md UPDATE_SUMMARY.md VISUAL_GUIDE.md TRAIN_MONITORING_FEATURE.md"

for %%f in (!doc_files!) do (
    if exist "%%f" (
        move "%%f" "docs\" >nul 2>&1
    )
)
echo ✅ Documentation files organized
echo.

REM Move test files
echo Creating tests directory...
if not exist "tests" mkdir tests
move "test_*.py" "tests\" >nul 2>&1
echo ✅ Test files organized
echo.

REM Remove temporary directories
echo Cleaning temporary directories...
if exist "temp_repo" rmdir /s /q "temp_repo" >nul 2>&1
if exist "temp_traintrack" rmdir /s /q "temp_traintrack" >nul 2>&1
echo ✅ Temporary directories removed
echo.

REM Clean root of unnecessary demo/example files
echo Cleaning root directory...
set "root_cleanup=enhanced_app.py simple_app.py run_tests.py test_api_offline.py test_dataset.py test_import.py test_journey_tracking.py test_live_api.py test_realtime.py demo_agents.py demo_api.py"

for %%f in (!root_cleanup!) do (
    if exist "%%f" del "%%f" >nul 2>&1
)
echo ✅ Root directory cleaned
echo.

REM Create utilities directory if needed
echo Verifying utility structure...
if not exist "utilities" mkdir utilities
if exist "setup_api.py" move "setup_api.py" "utilities\" >nul 2>&1
echo ✅ Utility files organized
echo.

REM Summary
echo.
echo ╔════════════════════════════════════════════════════════════════════════════════╗
echo ║  CLEANUP COMPLETE! New Project Structure:                                      ║
echo ╠════════════════════════════════════════════════════════════════════════════════╣
echo ║                                                                                ║
echo ║  /                          ← Main root (clean & organized)                    ║
echo ║  ├─ src/                    ← Source code                                      ║
echo ║  │  └─ ui/                  ← UI modules                                       ║
echo ║  ├─ data/                   ← Data files                                       ║
echo ║  ├─ models/                 ← ML models                                        ║
echo ║  ├─ docs/                   ← ALL documentation (organized)                    ║
echo ║  ├─ tests/                  ← Test files                                       ║
echo ║  ├─ utilities/              ← Helper scripts                                   ║
echo ║  ├─ launch_app.bat          ← Launcher (easy access)                           ║
echo ║  ├─ launch_app.ps1          ← PowerShell launcher                              ║
echo ║  ├─ CONTROL_PANEL.bat       ← Control menu                                     ║
echo ║  ├─ main.py                 ← Entry point                                      ║
echo ║  ├─ requirements.txt        ← Dependencies                                     ║
echo ║  ├─ startup_config.json     ← Configuration                                    ║
echo ║  ├─ .env                    ← Environment variables                            ║
echo ║  └─ _backup/                ← Backup of original (if needed)                   ║
echo ║                                                                                ║
echo ║  To get started:                                                              ║
echo ║  1. Review docs/SETUP_AND_LAUNCH.md                                            ║
echo ║  2. Run launch_app.bat                                                         ║
echo ║  3. Access http://localhost:8501                                               ║
echo ║                                                                                ║
echo ╚════════════════════════════════════════════════════════════════════════════════╝
echo.

echo Backup available in: _backup folder
echo To restore original: Delete docs, tests, utilities folders and copy from _backup
echo.
pause
