# Indian Railways AI System - PowerShell Launcher
# This script launches the application with full setup

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  🚂 Indian Railways AI Detection System - Enterprise Edition" -ForegroundColor Green
Write-Host "  Version 1.0.0 | Production Ready" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check and create virtual environment if needed
if (-not (Test-Path ".venv")) {
    Write-Host "⚠️  Virtual environment not found!" -ForegroundColor Yellow
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host ""
Write-Host "🔄 Activating virtual environment..." -ForegroundColor Cyan
& .\.venv\Scripts\Activate.ps1

# Install/update dependencies
Write-Host ""
Write-Host "📦 Checking dependencies..." -ForegroundColor Cyan
pip install -q -r requirements.txt

# Clear cache
Write-Host ""
Write-Host "🧹 Clearing cache..." -ForegroundColor Cyan
if (Test-Path "__pycache__") { Remove-Item "__pycache__" -Recurse -Force -ErrorAction SilentlyContinue }
if (Test-Path "src/__pycache__") { Remove-Item "src/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue }

# Launch application
Write-Host ""
Write-Host "🚀 Launching Indian Railways AI System..." -ForegroundColor Green
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "  📍 Access the application at:" -ForegroundColor Yellow
Write-Host "  • Local:   http://localhost:8501" -ForegroundColor White
Write-Host "  • Network: http://192.168.x.x:8501" -ForegroundColor White
Write-Host ""
Write-Host "  ✅ System Status: OPERATIONAL" -ForegroundColor Green
Write-Host "  ⚡ Version: 1.0.0" -ForegroundColor Green
Write-Host "  📊 Mode: Production" -ForegroundColor Green
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the application" -ForegroundColor Yellow
Write-Host ""

# Run the app
streamlit run src/ui/app.py --server.port=8501 --logger.level=info

Read-Host "Press Enter to exit"
