from datetime import datetime
from typing import Dict, Optional, Union
import requests


class LiveTrainAPIClient:
    """Client for fetching live train data from an external API.

    This is intentionally minimal and provider-agnostic. Inject a
    different implementation for IRCTC/NTES/RapidAPI as needed.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None, timeout: float = 5.0):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout

    def get_live_status(self, train_no: str) -> Optional[Dict]:
        try:
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"

            resp = requests.get(f"{self.base_url}/train/status/{train_no}", headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            return resp.json()

        except requests.RequestException:
            return None


class StatusCalculator:
    """Calculates train status using live API data with schedule fallback.

    This implementation supports both the new live-first API (call with
    a train number and fallback data) and the legacy usage where a
    `train_data` dict containing a `status` field is passed.
    """

    def __init__(self, api_client: Optional[LiveTrainAPIClient] = None):
        self.api_client = api_client
        self.detection_times: Dict[str, datetime] = {}

    def calculate_status(self, identifier: Union[str, Dict], fallback_data: Optional[Dict] = None) -> str:
        """Calculate status using live API if possible; fall back to schedule.

        identifier may be either:
        - a `str` train number (preferred), or
        - a `dict` of train data (legacy callers).
        """

        # Legacy path: caller passed a train_data dict
        if isinstance(identifier, dict):
            train_data = identifier

            if 'status' in train_data:
                status = str(train_data['status']).lower()
                delay = train_data.get('delay', 0)

                if 'running' in status:
                    if delay == 0:
                        return "On Time"
                    elif delay > 0:
                        return f"Late by {delay} mins"
                    else:
                        return "Early"
                if 'arrived' in status or 'reached' in status:
                    return "Arrived"
                if 'departed' in status:
                    return "Departed"
                if 'cancelled' in status:
                    return "Cancelled"

            scheduled_time = train_data.get('scheduled_time')
            if scheduled_time:
                return self._calculate_from_schedule(scheduled_time)

            return "Unknown"

        # New path: identifier is a train number string
        train_no = str(identifier)

        live_data = None
        if self.api_client:
            try:
                live_data = self.api_client.get_live_status(train_no)
            except Exception:
                live_data = None

        if live_data:
            status = self._calculate_from_live_data(live_data)
            if status:
                return status

        # schedule fallback
        scheduled_time = None
        if fallback_data:
            scheduled_time = fallback_data.get('scheduled_time')

        if scheduled_time:
            return self._calculate_from_schedule(scheduled_time)

        return "Unknown"

    def _calculate_from_live_data(self, data: Dict) -> str:
        status = str(data.get('status', '')).lower()
        # support multiple naming conventions across providers
        delay = data.get('delay_minutes', data.get('delay', 0)) or 0

        if 'running' in status:
            if delay == 0:
                return "On Time"
            elif delay > 0:
                return f"Late by {delay} mins"
            else:
                return "Early"

        if 'arrived' in status or 'reached' in status:
            return "Arrived"

        if 'departed' in status:
            return "Departed"

        if 'cancelled' in status:
            return "Cancelled"

        return "Unknown"

    def _calculate_from_schedule(self, scheduled_time: str) -> str:
        current_time = datetime.now()

        try:
            scheduled_dt = datetime.strptime(scheduled_time, '%H:%M').time()
            scheduled_datetime = datetime.combine(current_time.date(), scheduled_dt)
        except ValueError:
            return "Unknown"

        minutes_diff = (current_time - scheduled_datetime).total_seconds() / 60

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
        self.detection_times[train_no] = datetime.now()

    def get_last_detection(self, train_no: str) -> Optional[datetime]:
        return self.detection_times.get(train_no)

    def get_platform_status(self, platform_no: str) -> Dict:
        return {
            'platform': platform_no,
            'occupied': False,
            'train_no': None,
            'status': 'Available'
        }