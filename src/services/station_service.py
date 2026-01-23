"""Station Service - handles station operations."""
from typing import List, Optional, Dict
from src.models import Station
from src.repositories.train_repository import TrainRepository


class StationService:
    """Business logic for station queries and operations."""
    
    def __init__(self):
        self.repository = TrainRepository()
    
    def get_all_stations(self) -> List[Station]:
        """Get all available stations."""
        stations_data = self.repository.get_all_stations()
        return [self._dict_to_station(s) for s in stations_data]
    
    def search_stations(self, query: str) -> List[Station]:
        """Search stations by name or code (case-insensitive)."""
        results = self.repository.search_stations(query)
        return [self._dict_to_station(s) for s in results]
    
    def get_station_by_code(self, code: str) -> Optional[Station]:
        """Get station by its code."""
        station_data = self.repository.get_station_by_code(code)
        if station_data:
            return self._dict_to_station(station_data)
        return None
    
    def get_stations_by_state(self, state: str) -> List[Station]:
        """Get all stations in a specific state."""
        stations_data = self.repository.get_stations_by_state(state)
        return [self._dict_to_station(s) for s in stations_data]
    
    def get_stations_by_zone(self, zone: str) -> List[Station]:
        """Get all stations in a railway zone."""
        stations_data = self.repository.get_stations_by_zone(zone)
        return [self._dict_to_station(s) for s in stations_data]
    
    def get_major_junctions(self) -> List[Station]:
        """Get all major junction stations."""
        all_stations = self.get_all_stations()
        return [s for s in all_stations if s.is_major_junction]
    
    def get_stations_by_platform_capacity(
        self,
        min_platforms: int
    ) -> List[Station]:
        """Get stations with minimum platform capacity."""
        all_stations = self.get_all_stations()
        return [s for s in all_stations if s.platform_count >= min_platforms]
    
    def get_zone_distribution(self) -> Dict[str, int]:
        """Get distribution of stations across railway zones."""
        all_stations = self.get_all_stations()
        distribution = {}
        for station in all_stations:
            distribution[station.zone] = distribution.get(station.zone, 0) + 1
        return distribution
    
    def _dict_to_station(self, station_dict: Dict) -> Station:
        """Convert dictionary to Station model."""
        return Station(
            station_code=station_dict['station_code'],
            station_name=station_dict['station_name'],
            station_type=station_dict.get('station_type', 'Station'),
            state=station_dict.get('state', 'Unknown'),
            platform_count=int(station_dict.get('platform_count', 0)),
            zone=station_dict.get('zone', 'Unknown')
        )
