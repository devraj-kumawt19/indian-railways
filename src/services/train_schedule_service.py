"""Train Schedule Service - handles schedule and status operations."""
from typing import Optional, List
from src.models import TrainSchedule, TrainStatus


class TrainScheduleService:
    """Business logic for train schedules and status management."""
    
    def __init__(self):
        self.schedules = {}  # In-memory store (would be DB in production)
    
    def create_schedule(
        self,
        train_no: int,
        departure: str,
        arrival: str,
        status: TrainStatus = TrainStatus.ON_TIME
    ) -> TrainSchedule:
        """Create a new train schedule."""
        schedule = TrainSchedule(
            train_no=train_no,
            scheduled_departure=departure,
            scheduled_arrival=arrival,
            current_status=status
        )
        self.schedules[train_no] = schedule
        return schedule
    
    def get_schedule(self, train_no: int) -> Optional[TrainSchedule]:
        """Get schedule for a specific train."""
        return self.schedules.get(train_no)
    
    def update_status(
        self,
        train_no: int,
        status: TrainStatus,
        delay_minutes: int = 0
    ) -> bool:
        """Update train status and delay information."""
        schedule = self.get_schedule(train_no)
        if schedule:
            schedule.update_status(status, delay_minutes)
            return True
        return False
    
    def get_delayed_trains(self) -> List[TrainSchedule]:
        """Get all currently delayed trains."""
        return [s for s in self.schedules.values() if s.is_delayed]
    
    def get_on_time_trains(self) -> List[TrainSchedule]:
        """Get all trains running on time."""
        return [
            s for s in self.schedules.values()
            if s.current_status == TrainStatus.ON_TIME
        ]
    
    def get_cancelled_trains(self) -> List[TrainSchedule]:
        """Get all cancelled trains."""
        return [
            s for s in self.schedules.values()
            if s.current_status == TrainStatus.CANCELLED
        ]
    
    def get_running_trains(self) -> List[TrainSchedule]:
        """Get all trains currently running."""
        return [
            s for s in self.schedules.values()
            if s.current_status == TrainStatus.RUNNING
        ]
    
    def get_statistics(self) -> dict:
        """Get schedule statistics."""
        total = len(self.schedules)
        on_time = len(self.get_on_time_trains())
        delayed = len(self.get_delayed_trains())
        cancelled = len(self.get_cancelled_trains())
        running = len(self.get_running_trains())
        
        return {
            'total_trains': total,
            'on_time': on_time,
            'delayed': delayed,
            'cancelled': cancelled,
            'running': running,
            'on_time_percentage': (on_time / total * 100) if total > 0 else 0
        }
