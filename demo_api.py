#!/usr/bin/env python3
"""
Demo script for Indian Railways API integration
"""

from src.scheduling.indian_railways_api import IndianRailwaysAPI

def demo_api():
    """Demonstrate API functionality."""
    api = IndianRailwaysAPI()

    print("🚂 Indian Railways API Demo")
    print("=" * 40)

    # Test train schedule
    print("\n📅 Train Schedule (12301 - Rajdhani Express):")
    schedule = api.get_train_schedule("12301")
    if schedule:
        print(f"Name: {schedule.get('train_name', 'N/A')}")
        print(f"From: {schedule.get('from_station', 'N/A')}")
        print(f"To: {schedule.get('to_station', 'N/A')}")
    else:
        print("Schedule not available")

    # Test live status
    print("\n📍 Live Status (12301):")
    status = api.get_live_train_status("12301")
    if status:
        print(f"Current Station: {status.get('current_station', 'N/A')}")
        print(f"Status: {status.get('status', 'N/A')}")
        print(f"Delay: {status.get('delay', 0)} mins")
    else:
        print("Live status not available")

    # Test station code
    print("\n🎯 Station Code Lookup:")
    stations = ["Delhi", "Mumbai", "Kolkata", "Chennai"]
    for station in stations:
        code = api.get_station_code(station)
        print(f"{station}: {code}")

    # Test trains between stations
    print("\n🔍 Trains between Delhi and Mumbai:")
    trains = api.get_all_trains_between_stations("NDLS", "BCT")
    if trains:
        for train in trains[:3]:  # Show first 3
            print(f"{train.get('number')} - {train.get('name')}")
    else:
        print("No trains found")

if __name__ == "__main__":
    demo_api()