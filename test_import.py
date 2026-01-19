#!/usr/bin/env python3
"""Test script to check TrainDetectionApp import."""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

try:
    from src.ui.app import TrainDetectionApp
    print("✅ Import successful!")
    print(f"TrainDetectionApp class: {TrainDetectionApp}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
except Exception as e:
    print(f"❌ Unexpected error: {e}")