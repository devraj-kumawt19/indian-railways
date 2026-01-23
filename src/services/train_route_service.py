"""Train Route Service - handles train route operations."""
from typing import List, Optional, Dict
from src.models import Train, Station, TrainRoute
from src.repositories.train_repository import TrainRepository


class TrainRouteService:
    """Business logic for train routes."""
    
    def __init__(self):
        self.repository = TrainRepository()
    
    def get_routes_between_stations(
        self,
        from_code: str,
        to_code: str
    ) -> List[TrainRoute]:
        """Get all available train routes between two stations."""
        trains = self.repository.get_trains_between_stations(from_code, to_code)
        routes = []
        
        for train_dict in trains:
            try:
                train = self._dict_to_train(train_dict)
                source = self.repository.get_station_by_code(from_code)
                dest = self.repository.get_station_by_code(to_code)
                
                if source and dest:
                    route = TrainRoute(
                        train=train,
                        source_station=self._dict_to_station(source),
                        destination_station=self._dict_to_station(dest),
                        stops=[]
                    )
                    routes.append(route)
            except Exception as e:
                print(f"Error processing train {train_dict.get('train_no')}: {e}")
                continue
        
        return sorted(routes, key=lambda r: r.train.departure_time)
    
    def get_direct_routes(
        self,
        from_code: str,
        to_code: str
    ) -> List[TrainRoute]:
        """Get only direct routes (express trains)."""
        all_routes = self.get_routes_between_stations(from_code, to_code)
        return [r for r in all_routes if r.train.is_express()]
    
    def search_routes_by_criteria(
        self,
        from_code: str,
        to_code: str,
        max_duration: Optional[float] = None,
        min_avg_speed: Optional[float] = None
    ) -> List[TrainRoute]:
        """Advanced route search with filtering criteria."""
        routes = self.get_routes_between_stations(from_code, to_code)
        
        if max_duration:
            routes = [r for r in routes if r.journey_duration_hours() <= max_duration]
        
        if min_avg_speed:
            routes = [r for r in routes if r.average_speed_kmh() >= min_avg_speed]
        
        return routes
    
    def _dict_to_train(self, train_dict: Dict) -> Train:
        """Convert dictionary to Train model."""
        from src.models import TrainCoachBreakdown
        
        coach_breakdown = TrainCoachBreakdown(
            SL=int(train_dict.get('sl_coaches', 0)),
            AC2=int(train_dict.get('ac2_coaches', 0)),
            AC3=int(train_dict.get('ac3_coaches', 0)),
            FC=int(train_dict.get('fc_coaches', 0))
        )
        
        return Train(
            train_no=train_dict['train_no'],
            train_name=train_dict['train_name'],
            from_station=train_dict['from_station'],
            to_station=train_dict['to_station'],
            from_code=train_dict['from_code'],
            to_code=train_dict['to_code'],
            departure_time=train_dict['departure_time'],
            arrival_time=train_dict['arrival_time'],
            duration_hrs=train_dict['duration_hrs'],
            distance_km=train_dict['distance_km'],
            coach_count=train_dict['coach_count'],
            pantry=train_dict.get('pantry', 'Unknown'),
            frequency=train_dict.get('frequency', 'Daily'),
            zone=train_dict.get('zone', 'Unknown'),
            coach_breakdown=coach_breakdown
        )
    
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
