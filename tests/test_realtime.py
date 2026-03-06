"""
Test Script for Real-Time Add-Ons
Tests the real-time functionality without running the full Streamlit UI
"""

import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def test_imports():
    """Test that all real-time modules can be imported."""
    print("Testing real-time add-on imports...")

    try:
        from src.realtime import (
            RealtimeTrainService,
            EnhancedStatusCalculator,
            NotificationManager,
            BackgroundWorker,
            TrainStatusMonitor,
            PlatformMonitor,
            CloudIntegrationManager,
            CloudProvider,
            CloudConfig,
            StreamlitRealTimeUI,
            UIConfig,
            UIUpdateMode
        )
        print("✅ All real-time modules imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_service_initialization():
    """Test basic service initialization."""
    print("\nTesting service initialization...")

    try:
        from src.realtime.service import RealtimeTrainService
        from src.scheduling.enhanced_status import EnhancedStatusCalculator
        from src.realtime.notifications import NotificationManager

        # Test RealtimeTrainService
        service = RealtimeTrainService()
        print("✅ RealtimeTrainService initialized")

        # Test EnhancedStatusCalculator
        calculator = EnhancedStatusCalculator()
        print("✅ EnhancedStatusCalculator initialized")

        # Test NotificationManager
        manager = NotificationManager()
        print("✅ NotificationManager initialized")

        return True
    except Exception as e:
        print(f"❌ Service initialization failed: {e}")
        return False

def test_background_worker():
    """Test background worker functionality."""
    print("\nTesting background worker...")

    try:
        from src.realtime.worker import BackgroundWorker, MonitoringTask

        worker = BackgroundWorker("TestWorker")

        # Add a simple test task
        def test_task():
            print("Test task executed")

        task = MonitoringTask(
            task_id="test_task",
            name="Test Task",
            interval_seconds=5,
            callback=test_task
        )

        worker.add_task(task)
        print("✅ Background worker and task created")

        # Start briefly then stop
        worker.start()
        import time
        time.sleep(1)  # Let it run for 1 second
        worker.stop()

        print("✅ Background worker started and stopped successfully")
        return True
    except Exception as e:
        print(f"❌ Background worker test failed: {e}")
        return False

def test_cloud_integration():
    """Test cloud integration setup."""
    print("\nTesting cloud integration...")

    try:
        from src.realtime.cloud import CloudIntegrationManager, CloudProvider

        manager = CloudIntegrationManager()
        print("✅ CloudIntegrationManager initialized")

        # Test provider availability
        providers = manager.get_available_providers()
        print(f"✅ Available providers: {[p.value for p in providers]}")

        status = manager.get_status()
        print(f"✅ Cloud status: Connected={status['connected']}")

        return True
    except Exception as e:
        print(f"❌ Cloud integration test failed: {e}")
        return False

def test_enhanced_status():
    """Test enhanced status calculator."""
    print("\nTesting enhanced status calculator...")

    try:
        from src.scheduling.enhanced_status import EnhancedStatusCalculator

        calculator = EnhancedStatusCalculator()

        # Test basic functionality
        train_data = {
            'train_no': '12512',
            'status': 'running',
            'delay': 0
        }

        status = calculator.calculate_status(train_data)
        print(f"✅ Status calculated: {status}")

        # Test enhanced status
        enhanced_info = calculator.get_enhanced_status('12512', train_data)
        print(f"✅ Enhanced status retrieved: {enhanced_info.status}")

        # Test upcoming arrivals
        arrivals = calculator.get_upcoming_arrivals(60)
        print(f"✅ Upcoming arrivals retrieved: {len(arrivals)} trains")

        return True
    except Exception as e:
        print(f"❌ Enhanced status test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing Real-Time Train Tracking Add-Ons")
    print("=" * 50)

    tests = [
        test_imports,
        test_service_initialization,
        test_background_worker,
        test_cloud_integration,
        test_enhanced_status
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        if test():
            passed += 1
        print()

    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! Real-time add-ons are working correctly.")
        return True
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)