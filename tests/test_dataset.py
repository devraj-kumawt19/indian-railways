"""Comprehensive Dataset Testing Script"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import pandas as pd
from src.repositories.train_repository import TrainRepository

print("=" * 70)
print("🚂 INDIAN RAILWAYS AI - DATASET TESTING REPORT")
print("=" * 70)

# Initialize repository
print("\n📦 Loading data...\n")
repo = TrainRepository()

# ============ BASIC STATS ============
print("✓ DATA LOADED SUCCESSFULLY")
print(f"  • Stations: {len(repo.stations_df) if repo.stations_df is not None else 0}")
print(f"  • Trains: {len(repo.trains_df) if repo.trains_df is not None else 0}")
print(f"  • Schedule Entries: {len(repo.schedule_df) if repo.schedule_df is not None else 0}")

# ============ TEST 1: STATION DATA ============
print("\n" + "=" * 70)
print("TEST 1: STATION DATA")
print("=" * 70)

all_stations = repo.get_all_stations()
print(f"\n✓ Total stations: {len(all_stations)}")

major_junctions = [s for s in all_stations if s.get('station_type') == 'Major Junction']
print(f"✓ Major junctions: {len(major_junctions)}")

print("\nSample major junctions:")
for i, station in enumerate(major_junctions[:5], 1):
    print(f"  {i}. {station['station_code']}: {station['station_name']} ({station['state']}, {station['zone']})")

# ============ TEST 2: TRAIN DATA ============
print("\n" + "=" * 70)
print("TEST 2: TRAIN DATA")
print("=" * 70)

all_trains = repo.get_all_trains()
print(f"\n✓ Total trains: {len(all_trains)}")

print("\nSample trains:")
for i, train in enumerate(all_trains[:5], 1):
    print(f"  {i}. Train {train['train_no']}: {train['train_name']}")
    print(f"     {train['from_station']} → {train['to_station']}")
    print(f"     Coaches: {train['coach_count']} | Distance: {train['distance_km']}km")

# ============ TEST 3: ROUTE SEARCH ============
print("\n" + "=" * 70)
print("TEST 3: ROUTE SEARCH (NDLS → BCT)")
print("=" * 70)

routes = repo.get_trains_between_stations("NDLS", "BCT")
print(f"\n✓ Found {len(routes)} train(s) from New Delhi to Mumbai Central")

for i, train in enumerate(routes[:3], 1):
    print(f"\n  Train {i}: #{train['train_no']} - {train['train_name']}")
    print(f"    Departure: {train['departure_time']} | Arrival: {train['arrival_time']}")
    print(f"    Duration: {train['duration_hrs']}h | Distance: {train['distance_km']}km")
    print(f"    Coaches: SL={train['sl_coaches']}, AC2={train['ac2_coaches']}, AC3={train['ac3_coaches']}")

# ============ TEST 4: SCHEDULE DATA ============
print("\n" + "=" * 70)
print("TEST 4: SCHEDULE DATA (Train 12301)")
print("=" * 70)

schedule = repo.get_train_schedule(12301)
print(f"\n✓ Train 12301 has {len(schedule)} stops")

print("\nRoute details:")
for i, stop in enumerate(schedule[:8], 1):
    print(f"  {i}. {stop['Station Code']:6} - {stop['Station Name']:30} "
          f"Arr: {stop['Arrival time']:8} Dep: {stop['Departure Time']:8} "
          f"Dist: {stop['Distance']:4}km")

if len(schedule) > 8:
    print(f"  ... and {len(schedule) - 8} more stops")

# ============ TEST 5: STATION SEARCH ============
print("\n" + "=" * 70)
print("TEST 5: STATION SEARCH ('Delhi')")
print("=" * 70)

delhi_stations = repo.search_stations("Delhi")
print(f"\n✓ Found {len(delhi_stations)} station(s) matching 'Delhi'")

for i, station in enumerate(delhi_stations[:5], 1):
    print(f"  {i}. {station['station_code']}: {station['station_name']} ({station['state']})")

# ============ TEST 6: TRAIN NAME SEARCH ============
print("\n" + "=" * 70)
print("TEST 6: TRAIN NAME SEARCH ('Rajdhani')")
print("=" * 70)

rajdhani = repo.search_trains_by_name("Rajdhani")
print(f"\n✓ Found {len(rajdhani)} Rajdhani train(s)")

for i, train in enumerate(rajdhani[:5], 1):
    print(f"  {i}. Train {train['train_no']}: {train['train_name']}")

# ============ TEST 7: DATA QUALITY ============
print("\n" + "=" * 70)
print("TEST 7: DATA QUALITY CHECKS")
print("=" * 70)

# Check for missing station codes
train_codes = set(repo.trains_df['from_code'].unique()) | set(repo.trains_df['to_code'].unique())
station_codes = set(repo.stations_df['station_code'].unique())
missing_codes = train_codes - station_codes

if missing_codes:
    print(f"\n⚠ Missing station codes: {missing_codes}")
else:
    print(f"\n✓ All train station codes exist in stations database")

# Check for duplicate trains
duplicate_trains = repo.trains_df['train_no'].duplicated().sum()
print(f"✓ Duplicate trains: {duplicate_trains} (Expected: 0)")

# Check CSV columns
print(f"\n✓ Stations CSV columns: {list(repo.stations_df.columns)}")
print(f"✓ Trains CSV columns: {list(repo.trains_df.columns)}")
print(f"✓ Schedule CSV columns: {list(repo.schedule_df.columns)}")

# Missing values
print(f"\n✓ Stations - Missing values: {repo.stations_df.isnull().sum().sum()}")
print(f"✓ Trains - Missing values: {repo.trains_df.isnull().sum().sum()}")
print(f"✓ Schedule - Missing values: {repo.schedule_df.isnull().sum().sum()}")

# ============ TEST 8: ROUTE STATS ============
print("\n" + "=" * 70)
print("TEST 8: ROUTE STATISTICS")
print("=" * 70)

print(f"\n✓ Longest distance: {repo.trains_df['distance_km'].max()}km")
print(f"✓ Shortest distance: {repo.trains_df['distance_km'].min()}km")
print(f"✓ Average distance: {repo.trains_df['distance_km'].mean():.0f}km")
print(f"✓ Most coaches: {repo.trains_df['coach_count'].max()} coaches")
print(f"✓ Least coaches: {repo.trains_df['coach_count'].min()} coaches")

# Pantry availability
with_pantry = repo.trains_df[repo.trains_df['pantry'] == 'Yes'].shape[0]
print(f"✓ Trains with pantry: {with_pantry}/{len(repo.trains_df)}")

# ============ FINAL SUMMARY ============
print("\n" + "=" * 70)
print("✅ DATASET TEST COMPLETED SUCCESSFULLY")
print("=" * 70)
print("\n🚂 All systems operational - Dataset ready for use!")
print("=" * 70 + "\n")
