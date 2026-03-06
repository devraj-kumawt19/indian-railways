#!/usr/bin/env python3
"""Test script to check TrainDetectionApp import."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

try:
    from src.ui.app import main
    print("✅ Import successful!")
    print(f"Main function: {main}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")