from datetime import datetime, timedelta
from typing import Dict, Optional
import time

class StatusCalculator:
    """Calculates train status based on schedule and live data."""

    def __init__(self):
        self.detection_times = {}  # train_no: detection_time

    def calculate_status(self, train_data: Dict) -> str:
        """Calculate train status from live data."""
        # If we have live status from API
        if 'status' in train_data:
            status = train_data['status'].lower()
            delay = train_data.get('delay', 0)

            if 'running' in status:
                if delay == 0:
                    return "On Time"
                elif delay > 0:
                    return f"Late by {delay} mins"
                else:
                    return "Early"
            elif 'arrived' in status or 'reached' in status:
                return "Arrived"
            elif 'departed' in status:
                return "Departed"
            elif 'cancelled' in status:
                return "Cancelled"

        # Fallback to schedule-based calculation
        scheduled_time = train_data.get('scheduled_time')
        if scheduled_time:
            return self._calculate_from_schedule(scheduled_time)

        return "Unknown"

    def _calculate_from_schedule(self, scheduled_time: str) -> str:
        """Calculate status based on scheduled time."""
        current_time = datetime.now()

        try:
            scheduled_dt = datetime.strptime(scheduled_time, '%H:%M').time()
            scheduled_datetime = datetime.combine(current_time.date(), scheduled_dt)
        except ValueError:
            return "Unknown"

        time_diff = current_time - scheduled_datetime
        minutes_diff = time_diff.total_seconds() / 60

        if abs(minutes_diff) <= 5:
            return "On Time"
        elif minutes_diff > 5:
            return "Late"
        elif -30 <= minutes_diff < 0:
            return "Approaching"
        elif minutes_diff < -30:
            return "Scheduled"
        else:
            return "Departed"

    def record_detection(self, train_no: str):
        """Record when a train was detected."""
        self.detection_times[train_no] = datetime.now()

    def get_last_detection(self, train_no: str) -> Optional[datetime]:
        """Get last detection time for a train."""
        return self.detection_times.get(train_no)

    def get_platform_status(self, platform_no: str) -> Dict:
        """Get status for a specific platform."""
        # This would integrate with platform detection
        return {
            'platform': platform_no,
            'occupied': False,
            'train_no': None,
            'status': 'Available'
        }