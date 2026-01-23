"""Train schedule model - represents scheduled timings and status."""
from dataclasses import dataclass
from typing import Optional
from enum import Enum
from datetime import datetime


class TrainStatus(Enum):
    """Train operational status."""
    ON_TIME = "On Time"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"
    RUNNING = "Running"


@dataclass
class TrainSchedule:
    """Train schedule and current status information."""
    train_no: int
    scheduled_departure: str  # HH:MM:SS format
    scheduled_arrival: str    # HH:MM:SS format
    current_status: TrainStatus = TrainStatus.ON_TIME
    delay_minutes: int = 0
    current_location: Optional[str] = None
    last_updated: Optional[str] = None
    
    @property
    def is_delayed(self) -> bool:
        """Check if train is delayed."""
        return self.delay_minutes > 0 and self.current_status == TrainStatus.DELAYED
    
    @property
    def expected_arrival(self) -> str:
        """Get expected arrival time including delays."""
        # This would be calculated based on delay_minutes
        return self.scheduled_arrival
    
    def update_status(self, status: TrainStatus, delay: int = 0):
        """Update train status and delay information."""
        self.current_status = status
        self.delay_minutes = delay
        self.last_updated = datetime.now().isoformat()
