#!/usr/bin/env python3
"""Quick import validation for all UI modules"""

import sys
import os
from pathlib import Path

project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

print("="*80)
print("🧪 TESTING ALL UI IMPORTS")
print("="*80)

modules_to_test = [
    ("live_monitoring", "display_live_monitoring_dashboard"),
    ("enhanced_coach_detection", "display_enhanced_coach_detection"),
    ("all_india_search", "display_all_india_train_search"),
    ("enhanced_journey_tracking", "display_enhanced_journey_tracking"),
    ("train_status_tab", "display_train_status_tab"),
    ("platform_management_tab", "display_platform_management"),
    ("agent_system_tab", "display_agent_system"),
    ("dashboard_tab", "display_improved_dashboard"),
    ("journey_tracking", "display_all_india_trains_and_stations"),
    ("camera_platform_detection", "display_dataset_coach_detection"),
]

failed = []
success_count = 0

for module_name, function_name in modules_to_test:
    try:
        module = __import__(f"src.ui.{module_name}", fromlist=[function_name])
        getattr(module, function_name)
        print(f"✅ {module_name:<40} [{function_name}]")
        success_count += 1
    except Exception as e:
        print(f"❌ {module_name:<40} - {str(e)[:40]}")
        failed.append((module_name, str(e)))

print("="*80)
print(f"\n✅ SUCCESS: {success_count}/{len(modules_to_test)} modules imported\n")

if failed:
    print("❌ FAILED MODULES:")
    for module, error in failed:
        print(f"   - {module}: {error[:60]}")
else:
    print("🎉 All modules imported successfully!")

print("="*80)
