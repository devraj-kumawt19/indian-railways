import pandas as pd
import os
from typing import List, Dict, Optional
from pathlib import Path
from src.scheduling.indian_railways_api import IndianRailwaysAPI

class TrainRepository:
    """Repository for managing train and station data from CSV files + Live API."""
    
    def __init__(self):
        self.data_path = Path(__file__).parent.parent.parent / "data"
        self.stations_df = None
        self.trains_df = None
        self.schedule_df = None
        self.api = IndianRailwaysAPI()  # Initialize live API
        self._load_data()
    
    def _load_data(self):
        """Load data from CSV files."""
        try:
            stations_file = self.data_path / "indian_stations.csv"
            trains_file = self.data_path / "trains_with_coaches.csv"
            schedule_file = self.data_path / "Train_details_22122017.csv"
            
            if stations_file.exists():
                self.stations_df = pd.read_csv(stations_file)
            
            if trains_file.exists():
                self.trains_df = pd.read_csv(trains_file)
            
            # Load detailed schedule data
            if schedule_file.exists():
                self.schedule_df = pd.read_csv(schedule_file)
                print(f"✓ Loaded {len(self.schedule_df)} schedule entries from Train_details_22122017.csv")
            else:
                self.schedule_df = pd.DataFrame()
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.stations_df = pd.DataFrame()
            self.trains_df = pd.DataFrame()
            self.schedule_df = pd.DataFrame()
    
    def get_all_stations(self) -> List[Dict]:
        """Get all stations."""
        if self.stations_df is None or self.stations_df.empty:
            return []
        return self.stations_df.to_dict('records')
    
    def search_stations(self, query: str) -> List[Dict]:
        """Search stations by name or code."""
        if self.stations_df is None or self.stations_df.empty:
            return []
        
        query_lower = query.lower()
        results = self.stations_df[
            (self.stations_df['station_name'].str.lower().str.contains(query_lower, na=False)) |
            (self.stations_df['station_code'].str.lower().str.contains(query_lower, na=False))
        ]
        return results.to_dict('records')
    
    def get_station_by_code(self, code: str) -> Optional[Dict]:
        """Get station by code."""
        if self.stations_df is None or self.stations_df.empty:
            return None
        
        result = self.stations_df[self.stations_df['station_code'].str.upper() == code.upper()]
        if result.empty:
            return None
        return result.iloc[0].to_dict()
    
    def get_stations_by_state(self, state: str) -> List[Dict]:
        """Get all stations in a state."""
        if self.stations_df is None or self.stations_df.empty:
            return []
        
        results = self.stations_df[self.stations_df['state'].str.lower() == state.lower()]
        return results.to_dict('records')
    
    def get_trains_between_stations(self, from_code: str, to_code: str) -> List[Dict]:
        """Get trains between two stations."""
        if self.trains_df is None or self.trains_df.empty:
            return []
        
        from_code_upper = from_code.upper()
        to_code_upper = to_code.upper()
        
        results = self.trains_df[
            (self.trains_df['from_code'].str.upper() == from_code_upper) &
            (self.trains_df['to_code'].str.upper() == to_code_upper)
        ]
        return results.to_dict('records')
    
    def get_train_details(self, train_no: str) -> Optional[Dict]:
        """Get train details by train number."""
        if self.trains_df is None or self.trains_df.empty:
            return None
        
        result = self.trains_df[self.trains_df['train_no'] == int(train_no)]
        if result.empty:
            return None
        
        train = result.iloc[0].to_dict()
        # Add coach breakdown
        train['coach_breakdown'] = {
            'SL': int(train.get('sl_coaches', 0)),
            'AC2': int(train.get('ac2_coaches', 0)),
            'AC3': int(train.get('ac3_coaches', 0)),
            'FC': int(train.get('fc_coaches', 0))
        }
        return train
    
    def get_trains_from_station(self, station_code: str) -> List[Dict]:
        """Get all trains departing from a station."""
        if self.trains_df is None or self.trains_df.empty:
            return []
        
        station_code_upper = station_code.upper()
        results = self.trains_df[self.trains_df['from_code'].str.upper() == station_code_upper]
        return results.to_dict('records')
    
    def get_trains_to_station(self, station_code: str) -> List[Dict]:
        """Get all trains arriving at a station."""
        if self.trains_df is None or self.trains_df.empty:
            return []
        
        station_code_upper = station_code.upper()
        results = self.trains_df[self.trains_df['to_code'].str.upper() == station_code_upper]
        return results.to_dict('records')
    
    def get_all_trains(self) -> List[Dict]:
        """Get all trains."""
        if self.trains_df is None or self.trains_df.empty:
            return []
        return self.trains_df.to_dict('records')
    
    def get_stations_by_zone(self, zone: str) -> List[Dict]:
        """Get stations by railway zone."""
        if self.stations_df is None or self.stations_df.empty:
            return []
        
        results = self.stations_df[self.stations_df['zone'].str.upper() == zone.upper()]
        return results.to_dict('records')
    
    def get_coach_details(self, train_no: str) -> Optional[Dict]:
        """Get detailed coach information for a train."""
        train = self.get_train_details(train_no)
        if not train:
            return None
        
        return {
            'train_no': train['train_no'],
            'train_name': train['train_name'],
            'total_coaches': int(train['coach_count']),
            'coach_types': train.get('coach_breakdown', {
                'SL': int(train.get('sl_coaches', 0)),
                'AC2': int(train.get('ac2_coaches', 0)),
                'AC3': int(train.get('ac3_coaches', 0)),
                'FC': int(train.get('fc_coaches', 0))
            }),
            'pantry_car': train.get('pantry', 'Unknown'),
            'from_station': train['from_station'],
            'to_station': train['to_station'],
            'distance_km': train['distance_km']
        }    
    def get_train_schedule(self, train_no: int) -> List[Dict]:
        """Get complete schedule for a train with all stops."""
        if self.schedule_df is None or self.schedule_df.empty:
            return []
        
        schedule = self.schedule_df[self.schedule_df['Train No'] == train_no]
        if schedule.empty:
            return []
        
        return schedule.to_dict('records')
    
    def get_train_route_stops(self, train_no: int) -> List[str]:
        """Get all stops for a train in order."""
        schedule = self.get_train_schedule(train_no)
        if not schedule:
            return []
        
        stops = []
        for stop in schedule:
            code = stop['Station Code']
            name = stop['Station Name']
            if code not in [s.split('(')[1].strip(')') if '(' in s else s for s in stops]:
                stops.append(f"{name} ({code})")
        
        return stops
    
    def search_trains_by_name(self, train_name: str) -> List[Dict]:
        """Search trains by name pattern."""
        if self.trains_df is None or self.trains_df.empty:
            return []
        
        query_lower = train_name.lower()
        results = self.trains_df[
            self.trains_df['train_name'].str.lower().str.contains(query_lower, na=False)
        ]
        return results.to_dict('records')
    
    # ========== LIVE API METHODS ==========
    
    def get_live_train_status(self, train_no: str) -> Optional[Dict]:
        """Get real-time train status from live API."""
        try:
            return self.api.get_live_train_status(str(train_no))
        except Exception as e:
            print(f"Error fetching live status: {e}")
            return None
    
    def search_trains_api(self, from_station: str, to_station: str, date: str = None) -> List[Dict]:
        """Search trains between two stations using live API."""
        try:
            return self.api.get_all_trains_between_stations(from_station, to_station, date)
        except Exception as e:
            print(f"Error searching trains: {e}")
            return []
    
    def get_pnr_status(self, pnr_number: str) -> Optional[Dict]:
        """Get PNR status from live API."""
        try:
            return self.api.get_pnr_status(pnr_number)
        except Exception as e:
            print(f"Error fetching PNR status: {e}")
            return None
    
    def get_train_fare(self, train_no: str, from_station: str, to_station: str, train_class: str = "SL") -> Optional[Dict]:
        """Get train fare information from live API."""
        try:
            return self.api.get_train_fare(train_no, from_station, to_station, train_class)
        except Exception as e:
            print(f"Error fetching fare: {e}")
            return None
    
    def get_station_code(self, station_name: str) -> Optional[str]:
        """Get station code from station name using live API."""
        local_result = self.search_stations(station_name)
        if local_result:
            return local_result[0].get('station_code')
        
        try:
            return self.api.get_station_code(station_name)
        except Exception as e:
            print(f"Error getting station code: {e}")
            return None
    
    def get_train_journey_schedule(self, train_no: str, journey_date: str = None) -> Optional[Dict]:
        """Get detailed train journey schedule with station-by-station live tracking."""
        try:
            return self.api.get_train_journey_schedule(str(train_no), journey_date)
        except Exception as e:
            print(f"Error fetching journey schedule: {e}")
            return None