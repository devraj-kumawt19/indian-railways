"""
Advanced Train Tracking Service
Merged from TrainTrack project for enhanced train status monitoring
"""

from typing import Dict, List, Optional
from datetime import datetime, time, timedelta
import re
from .indian_railways_api import IndianRailwaysAPI

class TrainEvent:
    """Train event data model."""

    def __init__(self, raw: str, event_type: Optional[str] = None, station: Optional[str] = None,
                 code: Optional[str] = None, datetime_obj: Optional[datetime] = None,
                 delay: Optional[str] = None):
        self.raw = raw
        self.type = event_type
        self.station = station
        self.code = code
        self.datetime = datetime_obj
        self.delay = delay

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'raw': self.raw,
            'type': self.type,
            'station': self.station,
            'code': self.code,
            'datetime': self.datetime.isoformat() if self.datetime else None,
            'delay': self.delay
        }

class TrainStatusResponse:
    """Train status response data model."""

    def __init__(self, train_number: int, start_date: Optional[str] = None,
                 last_update: Optional[datetime] = None, events: Optional[List[TrainEvent]] = None):
        self.train_number = train_number
        self.start_date = start_date
        self.last_update = last_update
        self.events = events or []

    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'train_number': self.train_number,
            'start_date': self.start_date,
            'last_update': self.last_update.isoformat() if self.last_update else None,
            'events': [event.to_dict() for event in self.events]
        }

class AdvancedTrainTracker:
    """Advanced train tracking service with NTES integration."""

    def __init__(self):
        self.api = IndianRailwaysAPI()

    def get_train_status(self, train_number: int, start_time: Optional[str] = None,
                        end_time: Optional[str] = None) -> TrainStatusResponse:
        """Get comprehensive train running status."""
        # Validate train number
        if train_number < 10000 or train_number > 99999:
            raise ValueError("Train number must be a 5-digit number (10000-99999)")

        try:
            # Get real-time data from NTES
            ntes_data = self.api.get_realtime_train_status(train_number)

            if ntes_data:
                # Convert to our response format
                events = []
                for event_data in ntes_data.get('events', []):
                    event = TrainEvent(
                        raw=event_data.get('raw', ''),
                        event_type=event_data.get('type'),
                        station=event_data.get('station'),
                        code=event_data.get('code'),
                        datetime_obj=event_data.get('datetime'),
                        delay=event_data.get('delay')
                    )
                    events.append(event)

                # Filter events by time window if specified
                if start_time or end_time:
                    window_start, window_end = self._compute_time_window(start_time, end_time)
                    events = [
                        e for e in events
                        if e.datetime and window_start <= e.datetime < window_end
                    ]

                return TrainStatusResponse(
                    train_number=train_number,
                    start_date=ntes_data.get('start_date'),
                    last_update=ntes_data.get('last_update'),
                    events=events
                )

        except Exception as e:
            print(f"Advanced tracking failed: {e}")

        # Fallback to basic API
        basic_status = self.api.get_live_train_status(str(train_number))
        if basic_status:
            # Convert basic status to our format
            event = TrainEvent(
                raw=f"{basic_status.get('status', 'Unknown')} at {basic_status.get('current_station', 'Unknown')}",
                event_type="Status",
                station=basic_status.get('current_station'),
                datetime_obj=datetime.now(),
                delay=str(basic_status.get('delay', 0))
            )

            return TrainStatusResponse(
                train_number=train_number,
                last_update=datetime.now(),
                events=[event]
            )

        # Final fallback
        return TrainStatusResponse(train_number=train_number, events=[])

    def _compute_time_window(self, start_time_raw: Optional[str], end_time_raw: Optional[str]) -> tuple[datetime, datetime]:
        """Compute time window for filtering events."""
        now = datetime.now()
        today = now.date()
        local_tz = datetime.now().astimezone().tzinfo

        def normalize_dt(dt: datetime) -> datetime:
            if dt.tzinfo is None:
                return dt
            if local_tz is None:
                return dt.replace(tzinfo=None)
            return dt.astimezone(local_tz).replace(tzinfo=None)

        def parse_time_bound(raw: str) -> tuple[Optional[datetime], Optional[time]]:
            s = raw.strip()
            # Support ISO datetime
            if s.endswith("Z"):
                s = s[:-1] + "+00:00"

            try:
                dt = datetime.fromisoformat(s)
                return normalize_dt(dt), None
            except ValueError:
                pass

            try:
                return None, time.fromisoformat(s)
            except ValueError as e:
                raise ValueError(f"Invalid time format: '{raw}'. Use HH:MM[:SS] or ISO datetime") from e

        start_dt_raw = None
        start_t_raw = None
        end_dt_raw = None
        end_t_raw = None

        if start_time_raw:
            start_dt_raw, start_t_raw = parse_time_bound(start_time_raw)
        if end_time_raw:
            end_dt_raw, end_t_raw = parse_time_bound(end_time_raw)

        if start_time_raw is None and end_time_raw is None:
            start_dt = datetime.combine(today, time(0, 0, 0))
            end_dt = datetime.combine(today + timedelta(days=1), time(0, 0, 0))
            return start_dt, end_dt

        base_date = (
            start_dt_raw.date()
            if start_dt_raw is not None
            else (end_dt_raw.date() if end_dt_raw is not None else today)
        )

        def to_datetime(dt_part: Optional[datetime], t_part: Optional[time]) -> datetime:
            if dt_part is not None:
                return dt_part
            if t_part is not None:
                return datetime.combine(base_date, t_part)
            return now

        if start_time_raw is None and end_time_raw is not None:
            start_dt = now
            end_dt = to_datetime(end_dt_raw, end_t_raw)
            if end_dt < start_dt:
                start_dt, end_dt = end_dt, start_dt
            return start_dt, end_dt

        if start_time_raw is not None and end_time_raw is None:
            start_dt = to_datetime(start_dt_raw, start_t_raw)
            end_dt = now
            if end_dt < start_dt:
                start_dt, end_dt = end_dt, start_dt
            return start_dt, end_dt

        # Both provided
        start_dt = to_datetime(start_dt_raw, start_t_raw)
        end_dt = to_datetime(end_dt_raw, end_t_raw)

        if end_dt < start_dt:
            if start_dt_raw is None and end_dt_raw is None and start_t_raw and end_t_raw:
                end_dt = end_dt + timedelta(days=1)
            else:
                start_dt, end_dt = end_dt, start_dt

        return start_dt, end_dt

    def get_train_current_position(self, train_number: int) -> Optional[Dict]:
        """Get current position and status of a train."""
        status_response = self.get_train_status(train_number)

        if not status_response.events:
            return None

        # Get latest event
        latest_event = max(status_response.events, key=lambda e: e.datetime or datetime.min)

        return {
            'train_number': train_number,
            'current_station': latest_event.station,
            'last_event': latest_event.type,
            'event_time': latest_event.datetime,
            'delay': latest_event.delay,
            'last_update': status_response.last_update,
            'raw_status': latest_event.raw
        }

    def get_train_route_events(self, train_number: int) -> List[Dict]:
        """Get all route events for a train."""
        status_response = self.get_train_status(train_number)
        return [event.to_dict() for event in status_response.events]