#!/usr/bin/env python3
"""
Indian Railways API Setup and Testing Script
This script helps set up and test all Indian railway APIs
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.scheduling.indian_railways_api import IndianRailwaysAPI

def setup_environment():
    """Setup environment variables for API keys."""
    print("🚂 Indian Railways API Setup")
    print("=" * 50)

    # Check if .env file exists
    env_file = Path('.env')
    if not env_file.exists():
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("""# Indian Railways API Configuration
# Get API keys from the respective services

# RailwayAPI.com (Primary API)
RAILWAY_API_KEY=demo_key

# IndianRailAPI.com (Secondary API)
INDIAN_RAIL_API_KEY=demo_key

# IRCTC API (if available)
IRCTC_API_KEY=

# Application Settings
DEBUG=True
LOG_LEVEL=INFO
""")
        print("✅ .env file created. Please add your API keys.")

    # Load environment variables
    if env_file.exists():
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment variables loaded.")

def test_api_functionality():
    """Test all API functionalities."""
    print("\n🧪 Testing API Functionality")
    print("=" * 50)

    api = IndianRailwaysAPI()

    # Test station code lookup
    print("\n📍 Testing Station Code Lookup:")
    test_stations = ['Delhi', 'Mumbai', 'Kolkata', 'Chennai', 'Bangalore']
    for station in test_stations:
        code = api.get_station_code(station)
        status = "✅" if code else "❌"
        print(f"  {status} {station}: {code}")

    # Test train schedule
    print("\n📅 Testing Train Schedule:")
    test_trains = ['12301', '12302', '12401']
    for train in test_trains:
        schedule = api.get_train_schedule(train)
        status = "✅" if schedule else "❌"
        train_name = schedule.get('train_name', 'N/A') if schedule else 'N/A'
        print(f"  {status} {train}: {train_name}")

    # Test live status
    print("\n📊 Testing Live Status:")
    for train in test_trains:
        status = api.get_live_train_status(train)
        status_icon = "✅" if status else "❌"
        current_station = status.get('current_station', 'N/A') if status else 'N/A'
        print(f"  {status_icon} {train}: {current_station}")

    # Test trains between stations
    print("\n🔍 Testing Route Search:")
    routes = [('NDLS', 'BCT'), ('NDLS', 'KOAA'), ('MAS', 'SBC')]
    for from_station, to_station in routes:
        trains = api.get_all_trains_between_stations(from_station, to_station)
        status = "✅" if trains else "❌"
        count = len(trains) if trains else 0
        print(f"  {status} {from_station} → {to_station}: {count} trains found")

    # Test PNR status
    print("\n🎫 Testing PNR Status:")
    test_pnr = "1234567890"
    pnr_status = api.get_pnr_status(test_pnr)
    status = "✅" if pnr_status else "❌"
    print(f"  {status} PNR {test_pnr}: {pnr_status.get('train_name', 'N/A') if pnr_status else 'N/A'}")

    # Test fare inquiry
    print("\n💰 Testing Fare Inquiry:")
    fare = api.get_train_fare('12301', 'NDLS', 'BCT', 'SL')
    status = "✅" if fare else "❌"
    fare_amount = fare.get('total_fare', 'N/A') if fare else 'N/A'
    print(f"  {status} Rajdhani NDLS→BCT (SL): ₹{fare_amount}")

def show_api_instructions():
    """Show instructions for getting API keys."""
    print("\n📚 API Setup Instructions")
    print("=" * 50)

    print("""
🔑 Getting API Keys:

1. RailwayAPI.com (Primary):
   - Visit: https://railwayapi.com/
   - Sign up for a free account
   - Get your API key from dashboard
   - Add to .env: RAILWAY_API_KEY=your_key_here

2. IndianRailAPI.com (Secondary):
   - Visit: https://indianrailapi.com/
   - Register and get API key
   - Add to .env: INDIAN_RAIL_API_KEY=your_key_here

3. IRCTC Official API (Advanced):
   - Visit IRCTC developer portal
   - Requires business verification
   - Add to .env: IRCTC_API_KEY=your_key_here

📋 Available API Methods:
• Train Schedule & Route Information
• Live Train Status & Position
• Trains Between Stations
• Station Code Lookup
• PNR Status Check
• Fare Inquiry
• Train Classes & Availability

⚠️  Note: Free API keys have rate limits.
    Consider upgrading to paid plans for production use.
""")

def main():
    """Main setup function."""
    try:
        setup_environment()
        test_api_functionality()
        show_api_instructions()

        print("\n🎉 Setup Complete!")
        print("Your Indian Railways API is ready to use.")
        print("Run the Streamlit app with: python -m streamlit run src/ui/app.py")

    except Exception as e:
        print(f"❌ Setup failed: {e}")
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())