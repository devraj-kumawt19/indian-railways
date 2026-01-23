"""Train priority and availability model."""
from dataclasses import dataclass
from enum import Enum
from typing import Optional


class PriorityLevel(Enum):
    """Train priority classification."""
    HIGH = "High"      # Express/Rajdhani trains
    MEDIUM = "Medium"  # Regular express trains
    LOW = "Low"        # Local/passenger trains


@dataclass
class TrainPriority:
    """Train priority and operational details."""
    train_no: int
    priority_level: PriorityLevel = PriorityLevel.MEDIUM
    is_express: bool = False
    has_pantry: bool = False
    is_operational: bool = True
    seats_available: int = 0
    occupancy_percentage: float = 0.0
    
    @property
    def seat_availability_status(self) -> str:
        """Get human-readable seat availability."""
        if self.occupancy_percentage >= 90:
            return "Fully Booked"
        elif self.occupancy_percentage >= 70:
            return "Heavily Booked"
        elif self.occupancy_percentage >= 40:
            return "Moderately Booked"
        else:
            return "Seats Available"
    
    @property
    def travel_class(self) -> str:
        """Get travel class description."""
        if self.priority_level == PriorityLevel.HIGH:
            return "Premium Express"
        elif self.priority_level == PriorityLevel.MEDIUM:
            return "Express"
        else:
            return "Regular"
