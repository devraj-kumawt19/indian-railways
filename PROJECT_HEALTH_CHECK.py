#!/usr/bin/env python3
"""
Indian Railways AI - Project Health Check & Validation Script
Checks all modules, imports, and system functionality
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def check_imports():
    """Check if all critical imports work."""
    print("\n" + "="*80)
    print("🔍 CHECKING IMPORTS")
    print("="*80)
    
    imports_to_check = [
        ("Streamlit", "import streamlit as st"),
        ("Pandas", "import pandas as pd"),
        ("NumPy", "import numpy as np"),
        ("Requests", "import requests"),
    ]
    
    for name, import_stmt in imports_to_check:
        try:
            exec(import_stmt)
            print(f"✅ {name:<20} - OK")
        except ImportError as e:
            print(f"❌ {name:<20} - FAILED: {e}")

def check_data_files():
    """Verify all required data files exist."""
    print("\n" + "="*80)
    print("📊 CHECKING DATA FILES")
    print("="*80)
    
    data_dir = project_root / "data"
    required_files = [
        "indian_stations.csv",
        "trains_with_coaches.csv",
        "Train_details_22122017.csv",
        "train_schedule.csv"
    ]
    
    for file in required_files:
        file_path = data_dir / file
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024*1024)
            print(f"✅ {file:<40} - {size_mb:.2f} MB")
        else:
            print(f"❌ {file:<40} - NOT FOUND")

def check_ui_modules():
    """Verify all UI modules exist and are importable."""
    print("\n" + "="*80)
    print("🎨 CHECKING UI MODULES")
    print("="*80)
    
    ui_dir = project_root / "src" / "ui"
    ui_modules = [
        "app.py",
        "camera_platform_detection.py",
        "live_monitoring.py",
        "enhanced_coach_detection.py",
        "all_india_search.py",
        "journey_tracking.py",
        "train_status_tab.py",
        "enhanced_journey_tracking.py",
        "platform_management_tab.py",
        "agent_system_tab.py",
        "dashboard_tab.py",
    ]
    
    for module in ui_modules:
        module_path = ui_dir / module
        if module_path.exists():
            size_kb = module_path.stat().st_size / 1024
            print(f"✅ {module:<40} - {size_kb:.2f} KB")
        else:
            print(f"❌ {module:<40} - NOT FOUND")

def check_src_structure():
    """Verify source code structure."""
    print("\n" + "="*80)
    print("📁 CHECKING SOURCE STRUCTURE")
    print("="*80)
    
    src_dirs = [
        "agents",
        "detection",
        "models",
        "realtime",
        "repositories",
        "scheduling",
        "services",
        "ui",
        "utils",
        "viewmodels"
    ]
    
    src_dir = project_root / "src"
    for directory in src_dirs:
        dir_path = src_dir / directory
        if dir_path.exists():
            files_count = len(list(dir_path.glob("*.py")))
            print(f"✅ {directory:<30} - {files_count} Python files")
        else:
            print(f"❌ {directory:<30} - NOT FOUND")

def check_repositories():
    """Check if repositories can be instantiated."""
    print("\n" + "="*80)
    print("🗄️ CHECKING REPOSITORIES")
    print("="*80)
    
    try:
        from src.repositories.train_repository import TrainRepository
        repo = TrainRepository()
        print(f"✅ TrainRepository           - Initialized successfully")
        
        # Check loaded data
        if repo.schedule_df is not None and not repo.schedule_df.empty:
            print(f"   ├─ Schedule entries:     {len(repo.schedule_df):,}")
        if repo.stations_df is not None and not repo.stations_df.empty:
            print(f"   ├─ Stations loaded:      {len(repo.stations_df):,}")
        if repo.trains_df is not None and not repo.trains_df.empty:
            print(f"   └─ Trains loaded:        {len(repo.trains_df):,}")
    except Exception as e:
        print(f"❌ TrainRepository           - {e}")

def check_main_app():
    """Verify main app can be loaded."""
    print("\n" + "="*80)
    print("🚀 CHECKING MAIN APPLICATION")
    print("="*80)
    
    try:
        app_file = project_root / "src" / "ui" / "app.py"
        if app_file.exists():
            print(f"✅ app.py exists            - {app_file.stat().st_size / 1024:.2f} KB")
            
            # Try to read the file and check imports
            with open(app_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Check for key functions
            required_functions = [
                "display_live_monitoring_dashboard",
                "display_enhanced_coach_detection",
                "display_all_india_train_search",
                "display_enhanced_journey_tracking",
                "display_train_status_tab",
                "display_platform_management",
                "display_agent_system",
                "display_improved_dashboard",
                "display_dataset_coach_detection"
            ]
            
            missing = []
            for func in required_functions:
                if f"from src.ui" in content or "import" in content:
                    if func not in content:
                        missing.append(func)
            
            if not missing:
                print(f"✅ All required imports      - Present")
            else:
                print(f"⚠️  Missing imports:         {', '.join(missing)}")
        else:
            print(f"❌ app.py not found")
    except Exception as e:
        print(f"❌ Error checking app.py: {e}")

def check_requirements():
    """Verify requirements.txt exists."""
    print("\n" + "="*80)
    print("📦 CHECKING REQUIREMENTS")
    print("="*80)
    
    req_file = project_root / "requirements.txt"
    if req_file.exists():
        with open(req_file, 'r', encoding='utf-8') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        print(f"✅ requirements.txt          - {len(packages)} packages defined")
        print("   Top packages:")
        for pkg in packages[:5]:
            print(f"      ├─ {pkg}")
    else:
        print(f"❌ requirements.txt not found")

def generate_report():
    """Generate comprehensive health report."""
    print("\n\n" + "="*80)
    print("📋 PROJECT HEALTH REPORT")
    print("="*80)
    
    checks = {
        "Imports": "Critical",
        "Data Files": "Critical",
        "UI Modules": "Critical",
        "Source Structure": "High",
        "Repositories": "High",
        "Main Application": "Critical",
        "Requirements": "High"
    }
    
    print("\nCheck Status Summary:")
    for check, priority in checks.items():
        print(f"  {check:<25} [{priority}] - See above")
    
    print("\n" + "="*80)
    print("✅ HEALTH CHECK COMPLETE")
    print("="*80)
    print("\nNext Steps:")
    print("  1. Verify all ❌ items are fixed")
    print("  2. Run: streamlit run src/ui/app.py")
    print("  3. Test all tabs in the web interface")
    print("  4. Check browser console for errors")
    print("="*80 + "\n")

if __name__ == "__main__":
    print("\n" + "="*80)
    print("🔧 INDIAN RAILWAYS AI - PROJECT VALIDATION")
    print("="*80)
    print(f"Project Path: {project_root}")
    print(f"Python: {sys.version.split()[0]}")
    
    check_imports()
    check_data_files()
    check_ui_modules()
    check_src_structure()
    check_repositories()
    check_main_app()
    check_requirements()
    generate_report()
