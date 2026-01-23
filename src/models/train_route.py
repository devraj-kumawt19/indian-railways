"""Train route model - represents a train journey between stations."""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from src.models.train import Train
from src.models.station import Station


@dataclass
class TrainRoute:
    """Represents a train's complete route."""
    train: Train
    source_station: Station
    destination_station: Station
    stops: List[Station] = field(default_factory=list)
    
    def total_route_distance(self) -> int:
        """Get total distance of the route."""
        return self.train.distance_km
    
    def journey_duration_hours(self) -> float:
        """Get journey duration in hours."""
        return self.train.duration_hrs
    
    def is_direct_route(self) -> bool:
        """Check if this is a direct route (few/no stops)."""
        return len(self.stops) <= 3
    
    def average_speed_kmh(self) -> float:
        """Calculate average speed of the train."""
        if self.journey_duration_hours() == 0:
            return 0
        return self.total_route_distance() / self.journey_duration_hours()
