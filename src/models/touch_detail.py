"""Touch interaction details model - for user interactions/bookings."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from datetime import datetime
from enum import Enum


class InteractionType(Enum):
    """Type of user interaction with the system."""
    SEARCH = "Search"
    VIEW_DETAILS = "View Details"
    BOOKING_INQUIRY = "Booking Inquiry"
    SCHEDULE_CHECK = "Schedule Check"
    AVAILABILITY_CHECK = "Availability Check"


@dataclass
class TouchDetail:
    """User interaction/touch point details."""
    interaction_id: str
    interaction_type: InteractionType
    train_no: Optional[int] = None
    from_station: Optional[str] = None
    to_station: Optional[str] = None
    journey_date: Optional[str] = None
    passenger_class: Optional[str] = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def is_booking_related(self) -> bool:
        """Check if this interaction is booking-related."""
        return self.interaction_type in [
            InteractionType.BOOKING_INQUIRY,
            InteractionType.AVAILABILITY_CHECK
        ]
    
    def add_metadata(self, key: str, value: Any):
        """Add additional metadata to interaction."""
        self.metadata[key] = value
