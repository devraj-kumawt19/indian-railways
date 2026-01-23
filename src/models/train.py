"""Train model - represents a train entity."""
from dataclasses import dataclass, field
from typing import Optional, List, Dict


@dataclass
class TrainCoachBreakdown:
    """Coach composition of a train."""
    SL: int = 0  # Sleeper class
    AC2: int = 0  # AC 2-tier
    AC3: int = 0  # AC 3-tier
    FC: int = 0  # First class


@dataclass
class Train:
    """Core train entity."""
    train_no: int
    train_name: str
    from_station: str
    to_station: str
    from_code: str
    to_code: str
    departure_time: str
    arrival_time: str
    duration_hrs: float
    distance_km: int
    coach_count: int
    pantry: str
    frequency: str
    zone: str
    coach_breakdown: TrainCoachBreakdown = field(default_factory=TrainCoachBreakdown)
    
    def is_express(self) -> bool:
        """Determine if train is express class."""
        return self.coach_count >= 18
    
    def total_seats_estimate(self) -> int:
        """Estimate total seats based on coach breakdown."""
        return (
            self.coach_breakdown.SL * 80 +
            self.coach_breakdown.AC2 * 45 +
            self.coach_breakdown.AC3 * 72 +
            self.coach_breakdown.FC * 20
        )
