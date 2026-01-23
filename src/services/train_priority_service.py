"""Train Priority Service - handles train priority and availability."""
from typing import List, Optional
from src.models import TrainPriority, PriorityLevel


class TrainPriorityService:
    """Business logic for train priorities and availability management."""
    
    def __init__(self):
        self.priorities = {}  # In-memory store (would be DB in production)
    
    def set_priority(
        self,
        train_no: int,
        priority_level: PriorityLevel,
        is_express: bool = False,
        has_pantry: bool = False
    ) -> TrainPriority:
        """Set/update train priority classification."""
        priority = TrainPriority(
            train_no=train_no,
            priority_level=priority_level,
            is_express=is_express,
            has_pantry=has_pantry
        )
        self.priorities[train_no] = priority
        return priority
    
    def get_priority(self, train_no: int) -> Optional[TrainPriority]:
        """Get priority info for a train."""
        return self.priorities.get(train_no)
    
    def update_availability(
        self,
        train_no: int,
        seats_available: int,
        occupancy_percentage: float
    ) -> bool:
        """Update seat availability for a train."""
        priority = self.get_priority(train_no)
        if priority:
            priority.seats_available = seats_available
            priority.occupancy_percentage = occupancy_percentage
            return True
        return False
    
    def get_high_priority_trains(self) -> List[TrainPriority]:
        """Get all high priority trains (Express/Rajdhani)."""
        return [
            p for p in self.priorities.values()
            if p.priority_level == PriorityLevel.HIGH
        ]
    
    def get_available_trains(self) -> List[TrainPriority]:
        """Get trains with available seats."""
        return [
            p for p in self.priorities.values()
            if p.seats_available > 0 and p.is_operational
        ]
    
    def get_fully_booked_trains(self) -> List[TrainPriority]:
        """Get fully booked trains."""
        return [
            p for p in self.priorities.values()
            if p.occupancy_percentage >= 90
        ]
    
    def get_operational_status(self) -> dict:
        """Get overall operational statistics."""
        total = len(self.priorities)
        operational = len([p for p in self.priorities.values() if p.is_operational])
        express_trains = len(self.get_high_priority_trains())
        available_trains = len(self.get_available_trains())
        
        return {
            'total_trains': total,
            'operational': operational,
            'express_trains': express_trains,
            'available_trains': available_trains,
            'operational_percentage': (operational / total * 100) if total > 0 else 0
        }
