"""Test Live API Integration"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from src.repositories.train_repository import TrainRepository

print("\n" + "="*70)
print("🚂 TESTING LIVE API INTEGRATION")
print("="*70)

repo = TrainRepository()

# Test 1: Live train status
print("\n📍 TEST 1: LIVE TRAIN STATUS (Train 12301)")
print("-" * 70)
try:
    status = repo.get_live_train_status("12301")
    if status:
        print(f"✓ Train: {status.get('train_no')}")
        print(f"  Current Station: {status.get('current_station')}")
        print(f"  Status: {status.get('status')}")
        print(f"  Delay: {status.get('delay')} mins")
        print(f"  Source: {status.get('source', 'API')}")
    else:
        print("⚠ No data received")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 2: Search trains between stations
print("\n📍 TEST 2: LIVE TRAIN SEARCH (NDLS → BCT)")
print("-" * 70)
try:
    trains = repo.search_trains_api("NDLS", "BCT")
    if trains:
        print(f"✓ Found {len(trains)} train(s)")
        for train in trains[:2]:
            print(f"  - Train {train.get('number')}: {train.get('name')}")
    else:
        print("⚠ No trains found")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 3: Station code lookup
print("\n📍 TEST 3: STATION CODE LOOKUP")
print("-" * 70)
try:
    code = repo.get_station_code("Delhi")
    print(f"✓ Delhi → {code}" if code else "⚠ Station not found")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Fare information
print("\n📍 TEST 4: TRAIN FARE (Train 12301)")
print("-" * 70)
try:
    fare = repo.get_train_fare("12301", "NDLS", "BCT", "2A")
    if fare:
        print(f"✓ Fare Information Received")
        print(f"  Class: {fare.get('class')}")
        print(f"  Total Fare: ₹{fare.get('total_fare')}")
    else:
        print("⚠ No fare data")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 5: PNR Status
print("\n📍 TEST 5: PNR STATUS")
print("-" * 70)
try:
    pnr = repo.get_pnr_status("1234567890")
    if pnr:
        print(f"✓ PNR Status Received")
        print(f"  Train: {pnr.get('train_name')}")
        print(f"  Passengers: {len(pnr.get('passengers', []))}")
    else:
        print("⚠ No PNR data")
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "="*70)
print("✅ LIVE API INTEGRATION COMPLETE")
print("="*70 + "\n")
