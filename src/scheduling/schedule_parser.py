import csv
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import os
from .indian_railways_api import IndianRailwaysAPI
from .train_tracker import AdvancedTrainTracker

class ScheduleParser:
    """Parses train schedule data from API and local cache."""

    def __init__(self, schedule_file: str = "data/train_schedule.csv"):
        self.schedule_file = schedule_file
        self.api = IndianRailwaysAPI()
        self.tracker = AdvancedTrainTracker()  # Advanced tracking
        self.schedule_data = self.load_schedule()

    def load_schedule(self) -> List[Dict]:
        """Load train schedule from file or API."""
        if os.path.exists(self.schedule_file):
            with open(self.schedule_file, 'r') as f:
                reader = csv.DictReader(f)
                return list(reader)
        else:
            # Create sample data from API
            sample_data = self._fetch_sample_trains()
            self.save_schedule(sample_data)
            return sample_data

    def save_schedule(self, data: List[Dict]):
        """Save schedule data to file."""
        if data:
            with open(self.schedule_file, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)

    def get_train_schedule(self, train_no: str) -> Optional[Dict]:
        """Get schedule for a specific train from API."""
        # Try API first
        api_data = self.api.get_train_schedule(train_no)
        if api_data:
            return api_data

        # Fallback to local data
        for train in self.schedule_data:
            if train['train_no'] == train_no:
                return train
        return None

    def get_live_train_status(self, train_no: str) -> Optional[Dict]:
        """Get live status for a train using advanced tracking."""
        try:
            train_number = int(train_no)
            current_position = self.tracker.get_train_current_position(train_number)

            if current_position:
                return {
                    'train_no': str(train_number),
                    'train_name': f'Train {train_number}',  # Could be enhanced
                    'current_station': current_position.get('current_station'),
                    'status': current_position.get('last_event', 'Running'),
                    'delay': current_position.get('delay', '0'),
                    'expected_time': None,
                    'actual_time': current_position.get('event_time').strftime('%H:%M') if current_position.get('event_time') else None,
                    'source': 'ntes_advanced'
                }
        except Exception as e:
            print(f"Advanced tracking failed: {e}")

        # Fallback to basic API
        return self.api.get_live_train_status(train_no)

    def get_train_route_events(self, train_no: str) -> List[Dict]:
        """Get detailed route events for a train."""
        try:
            # Validate input is a number
            if not train_no or not str(train_no).strip().isdigit():
                return []
            
            train_number = int(train_no)
            return self.tracker.get_train_route_events(train_number)
        except (ValueError, TypeError):
            # Silent failure - return empty list for invalid input
            return []
        except Exception as e:
            # Other errors - also silent to avoid spam
            return []

    def get_current_trains(self) -> List[Dict]:
        """Get trains scheduled for current time window."""
        current_time = datetime.now()
        window_start = current_time - timedelta(hours=1)
        window_end = current_time + timedelta(hours=2)

        current_trains = []
        for train in self.schedule_data:
            try:
                # For demo, assume trains run daily
                scheduled_time = datetime.strptime(train['scheduled_time'], '%H:%M').time()
                scheduled_datetime = datetime.combine(current_time.date(), scheduled_time)
                if window_start <= scheduled_datetime <= window_end:
                    # Get live status
                    live_status = self.get_live_train_status(train['train_no'])
                    if live_status:
                        train.update(live_status)
                    current_trains.append(train)
            except ValueError:
                continue

        return current_trains

    def search_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
        """Search trains between two stations."""
        # Try with station codes first
        from_code = self.api.get_station_code(from_station)
        to_code = self.api.get_station_code(to_station)

        if from_code and to_code:
            trains = self.api.get_all_trains_between_stations(from_code, to_code)
            if trains:
                return trains

        # Fallback: try with station names directly
        trains = self.api.get_all_trains_between_stations(from_station.upper(), to_station.upper())
        return trains or []

    def get_pnr_status(self, pnr_number: str) -> Optional[Dict]:
        """Get PNR status for a booking."""
        return self.api.get_pnr_status(pnr_number)

    def get_train_fare(self, train_no: str, from_station: str, to_station: str,
                      train_class: str = "SL", age: int = 25) -> Optional[Dict]:
        """Get fare information for a train journey."""
        from_code = self.api.get_station_code(from_station) or from_station.upper()
        to_code = self.api.get_station_code(to_station) or to_station.upper()

        return self.api.get_train_fare(train_no, from_code, to_code, train_class, age)

    def get_train_classes(self, train_no: str) -> List[str]:
        """Get available classes for a train."""
        return self.api.get_train_classes(train_no)

    def get_station_codes(self, station_name: str) -> Dict[str, str]:
        """Get all station codes matching a station name.
        Returns dict of {code: full_name}"""
        results = {}
        station_lower = station_name.lower()
        
        # Search in API's station codes
        for code, name in self.api.station_codes.items():
            if station_lower in code.lower() or station_lower in name.lower():
                results[code] = name
        
        return results

    def get_all_trains_between_stations(self, from_station: str, to_station: str) -> List[Dict]:
        """Get all trains between two stations."""
        # This is an alias for search_trains_between_stations for consistency
        return self.search_trains_between_stations(from_station, to_station)

    def _fetch_sample_trains(self) -> List[Dict]:
        """Fetch sample train data."""
        sample_trains = ['12301', '12302', '12303', '12401']
        trains_data = []

        for train_no in sample_trains:
            schedule = self.api.get_train_schedule(train_no)
            if schedule:
                # Convert to CSV format
                train_data = {
                    'train_no': schedule.get('train_no', train_no),
                    'train_name': schedule.get('train_name', f'Train {train_no}'),
                    'scheduled_time': '08:00',  # Default time
                    'platform': '1'  # Default platform
                }
                trains_data.append(train_data)

        if not trains_data:
            # Fallback mock data
            trains_data = [
                {'train_no': '12301', 'train_name': 'Rajdhani Express', 'scheduled_time': '08:00', 'platform': '1'},
                {'train_no': '12302', 'train_name': 'Shatabdi Express', 'scheduled_time': '10:30', 'platform': '2'},
                {'train_no': '12303', 'train_name': 'Duronto Express', 'scheduled_time': '14:00', 'platform': '3'}
            ]

        return trains_data