"""
Enhanced Status Calculator with Real-Time Updates
Add-on module that extends existing status calculation with live data
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, List, Tuple
import time
from dataclasses import dataclass
from enum import Enum

class TrainStatus(Enum):
    """Enhanced train status enumeration."""
    UNKNOWN = "Unknown"
    ON_TIME = "On Time"
    RUNNING = "Running"
    ARRIVED = "Arrived"
    DEPARTED = "Departed"
    DELAYED = "Delayed"
    CANCELLED = "Cancelled"
    PLATFORM_CHANGED = "Platform Changed"
    EARLY = "Early"

@dataclass
class TrainStatusInfo:
    """Enhanced train status information."""
    train_no: str
    status: TrainStatus
    platform: Optional[str] = None
    scheduled_time: Optional[datetime] = None
    actual_time: Optional[datetime] = None
    delay_minutes: int = 0
    expected_arrival: Optional[datetime] = None
    expected_departure: Optional[datetime] = None
    last_updated: Optional[datetime] = None
    source: str = "schedule"
    alerts: List[str] = None

    def __post_init__(self):
        if self.alerts is None:
            self.alerts = []

class EnhancedStatusCalculator:
    """
    Enhanced status calculator with real-time capabilities.
    Extends existing StatusCalculator without breaking compatibility.
    """

    def __init__(self):
        self.detection_times: Dict[str, datetime] = {}
        self.realtime_status_cache: Dict[str, TrainStatusInfo] = {}
        self.platform_changes: Dict[str, List[Tuple[str, datetime]]] = {}
        self.alert_callbacks: List[callable] = []

    def add_change_callback(self, callback: callable):
        """
        Add a callback function to be called when status changes.
        """
        self.alert_callbacks.append(callback)

    def calculate_status(self, train_data: Dict) -> str:
        """
        Enhanced status calculation (maintains compatibility with existing code).
        """
        train_no = train_data.get('train_no', 'Unknown')

        # Check if we have real-time data
        if train_no in self.realtime_status_cache:
            realtime_info = self.realtime_status_cache[train_no]
            if (datetime.now() - realtime_info.last_updated).seconds < 300:  # 5 minutes
                return realtime_info.status.value

        # Fall back to existing logic
        return self._legacy_calculate_status(train_data)

    def _legacy_calculate_status(self, train_data: Dict) -> str:
        """Original status calculation logic."""
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

        scheduled_time = train_data.get('scheduled_time')
        if scheduled_time:
            return self._calculate_from_schedule(scheduled_time)

        return "Unknown"

    def get_enhanced_status(self, train_no: str, train_data: Dict) -> TrainStatusInfo:
        """
        Get enhanced status information with real-time data.
        """
        # Check cache first
        if train_no in self.realtime_status_cache:
            cached_info = self.realtime_status_cache[train_no]
            if (datetime.now() - cached_info.last_updated).seconds < 60:  # 1 minute cache
                return cached_info

        # Create enhanced status info
        status_info = self._create_status_info(train_no, train_data)
        self.realtime_status_cache[train_no] = status_info

        return status_info

    def _create_status_info(self, train_no: str, train_data: Dict) -> TrainStatusInfo:
        """Create TrainStatusInfo from train data."""
        status_str = self.calculate_status(train_data)
        status = self._string_to_status(status_str)

        # Parse scheduled time
        scheduled_time = None
        if 'scheduled_time' in train_data:
            try:
                time_str = train_data['scheduled_time']
                if isinstance(time_str, str):
                    scheduled_time = datetime.strptime(time_str, '%H:%M').time()
                    scheduled_datetime = datetime.combine(datetime.now().date(), scheduled_time)
                    scheduled_time = scheduled_datetime
            except ValueError:
                pass

        # Calculate delay
        delay_minutes = 0
        if 'delay' in train_data:
            delay_minutes = int(train_data['delay'])
        elif scheduled_time and status in [TrainStatus.DELAYED, TrainStatus.LATE]:
            # Extract delay from status string
            status_str_lower = status_str.lower()
            if 'late by' in status_str_lower:
                try:
                    delay_minutes = int(status_str_lower.split('late by')[1].split()[0])
                except (ValueError, IndexError):
                    pass

        # Calculate expected times
        expected_arrival = scheduled_time
        expected_departure = None

        if scheduled_time:
            # Assume departure is 5 minutes after arrival for passenger trains
            expected_departure = scheduled_time + timedelta(minutes=5)

        return TrainStatusInfo(
            train_no=train_no,
            status=status,
            platform=train_data.get('platform'),
            scheduled_time=scheduled_time,
            delay_minutes=delay_minutes,
            expected_arrival=expected_arrival,
            expected_departure=expected_departure,
            last_updated=datetime.now(),
            source="enhanced_calculator"
        )

    def _string_to_status(self, status_str: str) -> TrainStatus:
        """Convert status string to TrainStatus enum."""
        status_mapping = {
            "On Time": TrainStatus.ON_TIME,
            "Running": TrainStatus.RUNNING,
            "Arrived": TrainStatus.ARRIVED,
            "Departed": TrainStatus.DEPARTED,
            "Cancelled": TrainStatus.CANCELLED,
            "Early": TrainStatus.EARLY,
            "Platform Changed": TrainStatus.PLATFORM_CHANGED
        }

        # Check for delayed status
        if "Late by" in status_str or "Delayed" in status_str:
            return TrainStatus.DELAYED

        return status_mapping.get(status_str, TrainStatus.UNKNOWN)

    def update_realtime_status(self, train_no: str, status_data: Dict):
        """
        Update train status from real-time source.
        """
        current_info = self.realtime_status_cache.get(train_no)
        new_info = self._create_status_info_from_realtime(train_no, status_data)

        # Check for significant changes
        if current_info:
            changes = self._detect_status_changes(current_info, new_info)
            if changes:
                self._trigger_alerts(train_no, changes)

        # Update cache
        self.realtime_status_cache[train_no] = new_info

        # Update detection time for compatibility
        self.detection_times[train_no] = datetime.now()

    def _create_status_info_from_realtime(self, train_no: str, status_data: Dict) -> TrainStatusInfo:
        """Create TrainStatusInfo from real-time data."""
        status_str = status_data.get('status', 'Unknown')
        status = self._string_to_status(status_str)

        # Parse times
        expected_arrival = None
        expected_departure = None

        if 'expected_arrival' in status_data:
            try:
                expected_arrival = datetime.fromisoformat(status_data['expected_arrival'])
            except ValueError:
                pass

        if 'expected_departure' in status_data:
            try:
                expected_departure = datetime.fromisoformat(status_data['expected_departure'])
            except ValueError:
                pass

        # Handle platform changes
        platform = status_data.get('platform')
        if platform and train_no in self.platform_changes:
            # Check if platform changed
            last_platform = self.platform_changes[train_no][-1][0] if self.platform_changes[train_no] else None
            if last_platform and last_platform != platform:
                self.platform_changes[train_no].append((platform, datetime.now()))
                status = TrainStatus.PLATFORM_CHANGED

        return TrainStatusInfo(
            train_no=train_no,
            status=status,
            platform=platform,
            delay_minutes=status_data.get('delay', 0),
            expected_arrival=expected_arrival,
            expected_departure=expected_departure,
            last_updated=datetime.now(),
            source=status_data.get('source', 'realtime'),
            alerts=status_data.get('alerts', [])
        )

    def _detect_status_changes(self, old_info: TrainStatusInfo, new_info: TrainStatusInfo) -> List[str]:
        """Detect significant status changes."""
        changes = []

        if old_info.status != new_info.status:
            changes.append(f"Status changed from {old_info.status.value} to {new_info.status.value}")

        if old_info.platform != new_info.platform:
            changes.append(f"Platform changed from {old_info.platform} to {new_info.platform}")

        if abs(old_info.delay_minutes - new_info.delay_minutes) >= 5:
            changes.append(f"Delay changed by {new_info.delay_minutes - old_info.delay_minutes} minutes")

        return changes

    def _trigger_alerts(self, train_no: str, changes: List[str]):
        """Trigger alerts for significant changes."""
        for change in changes:
            alert_data = {
                'train_no': train_no,
                'change': change,
                'timestamp': datetime.now(),
                'type': 'status_change'
            }

            # Call alert callbacks
            for callback in self.alert_callbacks:
                try:
                    callback(alert_data)
                except Exception as e:
                    print(f"Alert callback error: {e}")

    def add_alert_callback(self, callback: callable):
        """Add callback for status change alerts."""
        self.alert_callbacks.append(callback)

    def get_platform_history(self, train_no: str) -> List[Tuple[str, datetime]]:
        """Get platform change history for a train."""
        return self.platform_changes.get(train_no, [])

    def get_upcoming_arrivals(self, minutes_ahead: int = 30) -> List[TrainStatusInfo]:
        """Get trains arriving in the next X minutes."""
        now = datetime.now()
        cutoff_time = now + timedelta(minutes=minutes_ahead)

        upcoming = []
        for train_info in self.realtime_status_cache.values():
            if (train_info.expected_arrival and
                train_info.expected_arrival > now and
                train_info.expected_arrival <= cutoff_time and
                train_info.status not in [TrainStatus.ARRIVED, TrainStatus.DEPARTED, TrainStatus.CANCELLED]):
                upcoming.append(train_info)

        return sorted(upcoming, key=lambda x: x.expected_arrival)

    def get_delayed_trains(self) -> List[TrainStatusInfo]:
        """Get all currently delayed trains."""
        return [info for info in self.realtime_status_cache.values()
                if info.status == TrainStatus.DELAYED or info.delay_minutes > 0]

    def _calculate_from_schedule(self, scheduled_time: str) -> str:
        """Calculate status based on scheduled time (legacy method)."""
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
            return f"Late by {int(minutes_diff)} mins"
        else:
            return "Early"


# Integration helper
def enhance_status_calculator(existing_calculator):
    """
    Enhance existing StatusCalculator with real-time capabilities.

    Args:
        existing_calculator: Existing StatusCalculator instance

    Returns:
        Enhanced calculator with backward compatibility
    """
    # Create enhanced calculator
    enhanced = EnhancedStatusCalculator()

    # Copy existing detection times for compatibility
    if hasattr(existing_calculator, 'detection_times'):
        enhanced.detection_times = existing_calculator.detection_times.copy()

    # Replace calculate_status method while maintaining interface
    original_calculate = existing_calculator.calculate_status
    existing_calculator.calculate_status = enhanced.calculate_status
    existing_calculator.get_enhanced_status = enhanced.get_enhanced_status
    existing_calculator.update_realtime_status = enhanced.update_realtime_status
    existing_calculator.add_alert_callback = enhanced.add_alert_callback
    existing_calculator.get_upcoming_arrivals = enhanced.get_upcoming_arrivals
    existing_calculator.get_delayed_trains = enhanced.get_delayed_trains
    existing_calculator.get_platform_history = enhanced.get_platform_history

    # Store original method for fallback
    existing_calculator._original_calculate_status = original_calculate

    return enhanced