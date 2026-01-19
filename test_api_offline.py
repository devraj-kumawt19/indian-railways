#!/usr/bin/env python3
"""
Test API with offline fallback - demonstrates graceful API error handling
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.scheduling.indian_railways_api import IndianRailwaysAPI

def test_station_codes():
    """Test station code resolution with local database fallback."""
    print("\n" + "="*60)
    print("🚉 Testing Station Code Resolution (Offline-First)")
    print("="*60)
    
    api = IndianRailwaysAPI()
    
    # Test cases - some with typos
    test_stations = [
        "Delhi",
        "jhodpur",  # Typo - should match 'jodhpur'
        "Mumbai",
        "Jaipur",
        "kolkata",
        "Bangalore"
    ]
    
    for station in test_stations:
        code = api.get_station_code(station)
        status = "✅" if code else "❌"
        print(f"{status} {station:15} → {code or 'NOT FOUND'}")

def test_trains_between_stations():
    """Test trains between stations with mock data fallback."""
    print("\n" + "="*60)
    print("🚂 Testing Trains Between Stations (Mock Data Fallback)")
    print("="*60)
    
    api = IndianRailwaysAPI()
    
    # Test route
    from_station = "NDLS"  # Delhi
    to_station = "BCT"      # Mumbai
    
    print(f"\n📍 Route: {from_station} → {to_station}")
    trains = api.get_all_trains_between_stations(from_station, to_station)
    
    if trains:
        print(f"Found {len(trains)} trains:\n")
        for i, train in enumerate(trains[:5], 1):  # Show first 5
            print(f"{i}. {train.get('number', 'N/A'):6} - {train.get('name', 'Unknown Train')}")
            print(f"   🕐 {train.get('depart', 'N/A'):6} → {train.get('arrive', 'N/A'):6}")
            print()
    else:
        print("No trains found")

def test_train_schedule():
    """Test train schedule with fallback."""
    print("\n" + "="*60)
    print("📅 Testing Train Schedule (Mock Data Fallback)")
    print("="*60)
    
    api = IndianRailwaysAPI()
    
    # Test common trains
    test_trains = ["12301", "12313", "12345"]
    
    for train_no in test_trains:
        print(f"\n🚂 Train {train_no}:")
        schedule = api.get_train_schedule(train_no)
        
        if schedule:
            print(f"   Name:      {schedule.get('train_name', 'N/A')}")
            print(f"   From:      {schedule.get('from_station', 'N/A')}")
            print(f"   To:        {schedule.get('to_station', 'N/A')}")
            print(f"   Type:      {schedule.get('train_type', 'N/A')}")
        else:
            print(f"   ❌ Schedule not available")

def test_live_status():
    """Test live train status with graceful fallback."""
    print("\n" + "="*60)
    print("📍 Testing Live Train Status (Mock Data Fallback)")
    print("="*60)
    
    api = IndianRailwaysAPI()
    
    # Test train
    train_no = "12301"
    
    print(f"\n🚂 Train {train_no}:")
    status = api.get_live_train_status(train_no)
    
    if status:
        print(f"   Current Station: {status.get('current_station', 'N/A')}")
        print(f"   Status:          {status.get('status', 'N/A')}")
        print(f"   Delay:           {status.get('delay', 0)} mins")
        print(f"   Updated:         {status.get('updated_time', 'N/A')}")
    else:
        print(f"   ❌ Status not available")

def main():
    """Run all tests."""
    print("\n")
    print("┌" + "─"*58 + "┐")
    print("│" + " "*58 + "│")
    print("│" + "  🚂 Indian Railways API - Offline-First Test Suite  ".center(58) + "│")
    print("│" + " "*58 + "│")
    print("└" + "─"*58 + "┘")
    
    try:
        test_station_codes()
        test_trains_between_stations()
        test_train_schedule()
        test_live_status()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        print("\n💡 NOTE: API failures are handled gracefully with local")
        print("         fallback data. External APIs are optional!")
        print()
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
