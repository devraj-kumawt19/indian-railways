"""
Background Worker Add-On
Provides background monitoring and status updates for real-time train tracking
"""

import threading
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
import json
import schedule
from dataclasses import dataclass
from enum import Enum

class WorkerStatus(Enum):
    """Background worker status."""
    STOPPED = "stopped"
    RUNNING = "running"
    PAUSED = "paused"
    ERROR = "error"

@dataclass
class MonitoringTask:
    """Monitoring task configuration."""
    task_id: str
    name: str
    interval_seconds: int
    callback: Callable
    enabled: bool = True
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None
    error_count: int = 0
    max_errors: int = 3

class BackgroundWorker:
    """
    Background worker for real-time train monitoring.
    Add-on component that runs monitoring tasks in the background.
    """

    def __init__(self, name: str = "TrainMonitor"):
        self.name = name
        self.status = WorkerStatus.STOPPED
        self.tasks: Dict[str, MonitoringTask] = {}
        self.thread: Optional[threading.Thread] = None
        self.running = False
        self.status_callbacks: List[Callable] = []
        self.error_log: List[Dict] = []

    def add_task(self, task: MonitoringTask):
        """Add a monitoring task."""
        self.tasks[task.task_id] = task
        print(f"✅ Added monitoring task: {task.name}")

    def remove_task(self, task_id: str):
        """Remove a monitoring task."""
        if task_id in self.tasks:
            del self.tasks[task_id]
            print(f"🗑️ Removed monitoring task: {task_id}")

    def enable_task(self, task_id: str):
        """Enable a monitoring task."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = True

    def disable_task(self, task_id: str):
        """Disable a monitoring task."""
        if task_id in self.tasks:
            self.tasks[task_id].enabled = False

    def start(self):
        """Start the background worker."""
        if self.running:
            return

        self.running = True
        self.status = WorkerStatus.RUNNING
        self.thread = threading.Thread(target=self._worker_loop, daemon=True)
        self.thread.start()

        self._notify_status_change()
        print(f"🚀 Started background worker: {self.name}")

    def stop(self):
        """Stop the background worker."""
        if not self.running:
            return

        self.running = False
        self.status = WorkerStatus.STOPPED

        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=5)

        self._notify_status_change()
        print(f"🛑 Stopped background worker: {self.name}")

    def pause(self):
        """Pause the background worker."""
        self.status = WorkerStatus.PAUSED
        self._notify_status_change()

    def resume(self):
        """Resume the background worker."""
        if self.status == WorkerStatus.PAUSED:
            self.status = WorkerStatus.RUNNING
            self._notify_status_change()

    def get_status(self) -> Dict:
        """Get worker status and statistics."""
        task_stats = {}
        for task_id, task in self.tasks.items():
            task_stats[task_id] = {
                'name': task.name,
                'enabled': task.enabled,
                'last_run': task.last_run.isoformat() if task.last_run else None,
                'next_run': task.next_run.isoformat() if task.next_run else None,
                'error_count': task.error_count,
                'interval_seconds': task.interval_seconds
            }

        return {
            'worker_name': self.name,
            'status': self.status.value,
            'running': self.running,
            'thread_alive': self.thread.is_alive() if self.thread else False,
            'task_count': len(self.tasks),
            'enabled_tasks': len([t for t in self.tasks.values() if t.enabled]),
            'tasks': task_stats,
            'error_count': len(self.error_log)
        }

    def add_status_callback(self, callback: Callable):
        """Add callback for status changes."""
        self.status_callbacks.append(callback)

    def _worker_loop(self):
        """Main worker loop."""
        while self.running:
            try:
                if self.status == WorkerStatus.RUNNING:
                    self._execute_tasks()
                time.sleep(1)  # Check every second
            except Exception as e:
                self._log_error("Worker loop error", str(e))
                self.status = WorkerStatus.ERROR
                time.sleep(5)  # Wait before retry

    def _execute_tasks(self):
        """Execute due monitoring tasks."""
        now = datetime.now()

        for task in self.tasks.values():
            if not task.enabled:
                continue

            # Check if task is due
            if task.next_run is None or now >= task.next_run:
                try:
                    # Execute task
                    task.callback()

                    # Update task info
                    task.last_run = now
                    task.next_run = now + timedelta(seconds=task.interval_seconds)
                    task.error_count = 0  # Reset error count on success

                except Exception as e:
                    task.error_count += 1
                    self._log_error(f"Task {task.task_id} error", str(e))

                    # Disable task if too many errors
                    if task.error_count >= task.max_errors:
                        task.enabled = False
                        self._log_error(f"Task {task.task_id} disabled", f"Too many errors ({task.error_count})")

    def _notify_status_change(self):
        """Notify status change callbacks."""
        for callback in self.status_callbacks:
            try:
                callback(self.status)
            except Exception as e:
                self._log_error("Status callback error", str(e))

    def _log_error(self, context: str, error: str):
        """Log an error."""
        error_entry = {
            'timestamp': datetime.now(),
            'context': context,
            'error': error
        }
        self.error_log.append(error_entry)

        # Keep only last 100 errors
        if len(self.error_log) > 100:
            self.error_log = self.error_log[-100:]

        print(f"❌ {context}: {error}")


class TrainStatusMonitor:
    """
    Specialized monitor for train status updates.
    Integrates with existing train management system.
    """

    def __init__(self, api_base_url: str = "https://api.railwayapi.com/v2",
                 api_key: Optional[str] = None):
        self.api_base_url = api_base_url
        self.api_key = api_key
        self.last_status_check: Dict[str, datetime] = {}
        self.status_cache: Dict[str, Dict] = {}
        self.monitoring_trains: List[str] = []

    def add_train_to_monitor(self, train_no: str):
        """Add a train to monitoring list."""
        if train_no not in self.monitoring_trains:
            self.monitoring_trains.append(train_no)
            print(f"👁️ Added train {train_no} to monitoring")

    def remove_train_from_monitor(self, train_no: str):
        """Remove a train from monitoring."""
        if train_no in self.monitoring_trains:
            self.monitoring_trains.remove(train_no)
            print(f"🚫 Removed train {train_no} from monitoring")

    def check_train_status(self, train_no: str) -> Optional[Dict]:
        """
        Check current status of a train.
        This method integrates with existing API calls.
        """
        try:
            # Use existing API integration
            # This would call your existing railway API
            url = f"{self.api_base_url}/live/train/{train_no}"

            params = {}
            if self.api_key:
                params['key'] = self.api_key

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()

            data = response.json()

            if data.get('response_code') == 200:
                train_data = data.get('train', {})
                current_station = data.get('current_station', {})

                status_info = {
                    'train_no': train_no,
                    'status': train_data.get('status', 'Unknown'),
                    'position': current_station.get('name', 'Unknown'),
                    'delay': train_data.get('delay', 0),
                    'expected_arrival': current_station.get('actarr', None),
                    'expected_departure': current_station.get('actdep', None),
                    'platform': current_station.get('platform', None),
                    'last_updated': datetime.now(),
                    'source': 'api'
                }

                # Update cache
                self.status_cache[train_no] = status_info
                self.last_status_check[train_no] = datetime.now()

                return status_info

        except requests.RequestException as e:
            print(f"API request failed for train {train_no}: {e}")
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed for train {train_no}: {e}")
        except Exception as e:
            print(f"Status check failed for train {train_no}: {e}")

        return None

    def get_status_updates(self) -> List[Dict]:
        """Get status updates for all monitored trains."""
        updates = []

        for train_no in self.monitoring_trains:
            current_status = self.check_train_status(train_no)
            if current_status:
                # Check if status changed
                previous_status = self.status_cache.get(train_no)
                if self._has_significant_change(previous_status, current_status):
                    updates.append({
                        'train_no': train_no,
                        'previous': previous_status,
                        'current': current_status,
                        'change_type': self._get_change_type(previous_status, current_status)
                    })

        return updates

    def _has_significant_change(self, previous: Optional[Dict], current: Dict) -> bool:
        """Check if status change is significant."""
        if not previous:
            return True

        significant_fields = ['status', 'platform', 'delay']

        for field in significant_fields:
            if previous.get(field) != current.get(field):
                return True

        return False

    def _get_change_type(self, previous: Optional[Dict], current: Dict) -> str:
        """Get the type of status change."""
        if not previous:
            return "new_status"

        if previous.get('status') != current.get('status'):
            return "status_change"

        if previous.get('platform') != current.get('platform'):
            return "platform_change"

        if previous.get('delay') != current.get('delay'):
            return "delay_change"

        return "minor_update"


class PlatformMonitor:
    """
    Monitor platform occupancy and train arrivals/departures.
    """

    def __init__(self):
        self.platform_status: Dict[str, Dict] = {}
        self.platform_history: Dict[str, List[Dict]] = {}

    def update_platform_status(self, platform_no: str, train_no: Optional[str] = None,
                             status: str = "available", occupancy_time: Optional[datetime] = None):
        """Update platform status."""
        if occupancy_time is None:
            occupancy_time = datetime.now()

        platform_data = {
            'platform_no': platform_no,
            'train_no': train_no,
            'status': status,  # 'available', 'occupied', 'arriving', 'departing'
            'last_updated': occupancy_time
        }

        self.platform_status[platform_no] = platform_data

        # Add to history
        if platform_no not in self.platform_history:
            self.platform_history[platform_no] = []

        self.platform_history[platform_no].append(platform_data)

        # Keep only last 50 entries per platform
        if len(self.platform_history[platform_no]) > 50:
            self.platform_history[platform_no] = self.platform_history[platform_no][-50:]

    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get current status of a platform."""
        return self.platform_status.get(platform_no)

    def get_available_platforms(self) -> List[str]:
        """Get list of available platforms."""
        return [p for p, data in self.platform_status.items()
                if data.get('status') == 'available']

    def detect_train_arrival(self, platform_no: str, train_no: str):
        """Detect and record train arrival."""
        self.update_platform_status(platform_no, train_no, "occupied")
        print(f"🚆 Train {train_no} arrived at Platform {platform_no}")

    def detect_train_departure(self, platform_no: str):
        """Detect and record train departure."""
        self.update_platform_status(platform_no, None, "available")
        print(f"🚆 Train departed from Platform {platform_no}")


# Integration helper functions
def create_monitoring_worker(train_monitor: TrainStatusMonitor,
                           platform_monitor: PlatformMonitor) -> BackgroundWorker:
    """
    Create a background worker with standard monitoring tasks.

    Args:
        train_monitor: Train status monitor instance
        platform_monitor: Platform monitor instance

    Returns:
        Configured background worker
    """
    worker = BackgroundWorker("TrainStatusMonitor")

    # Task: Check train statuses every 30 seconds
    def check_train_statuses():
        updates = train_monitor.get_status_updates()
        for update in updates:
            train_no = update['train_no']
            current = update['current']

            # Update platform status if train arrived
            if current.get('status', '').lower() in ['arrived', 'reached']:
                platform = current.get('platform')
                if platform:
                    platform_monitor.detect_train_arrival(platform, train_no)

    train_status_task = MonitoringTask(
        task_id="train_status_check",
        name="Train Status Monitoring",
        interval_seconds=30,
        callback=check_train_statuses
    )
    worker.add_task(train_status_task)

    # Task: Clean up old data every 5 minutes
    def cleanup_old_data():
        # Clean up old status cache entries (older than 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)

        # Clean train monitor cache
        expired_trains = []
        for train_no, last_check in train_monitor.last_status_check.items():
            if last_check < cutoff_time:
                expired_trains.append(train_no)

        for train_no in expired_trains:
            if train_no in train_monitor.status_cache:
                del train_monitor.status_cache[train_no]
            if train_no in train_monitor.last_status_check:
                del train_monitor.last_status_check[train_no]

        if expired_trains:
            print(f"🧹 Cleaned up {len(expired_trains)} expired train status entries")

    cleanup_task = MonitoringTask(
        task_id="cleanup_old_data",
        name="Data Cleanup",
        interval_seconds=300,  # 5 minutes
        callback=cleanup_old_data
    )
    worker.add_task(cleanup_task)

    # Task: Platform status monitoring every 60 seconds
    def monitor_platforms():
        # Check for trains that should have departed
        current_time = datetime.now()

        for platform_no, status in platform_monitor.platform_status.items():
            if status.get('status') == 'occupied':
                # Check if train has departed (this would need integration with schedule)
                # For now, just log platform status
                pass

    platform_task = MonitoringTask(
        task_id="platform_monitoring",
        name="Platform Status Monitoring",
        interval_seconds=60,
        callback=monitor_platforms
    )
    worker.add_task(platform_task)

    return worker


def integrate_background_worker(app_instance, api_key: Optional[str] = None):
    """
    Integrate background worker into existing app.

    Args:
        app_instance: Existing TrainDetectionApp instance
        api_key: API key for railway API
    """
    # Create monitoring components
    train_monitor = TrainStatusMonitor(api_key=api_key)
    platform_monitor = PlatformMonitor()
    worker = create_monitoring_worker(train_monitor, platform_monitor)

    # Add to app instance
    app_instance.train_monitor = train_monitor
    app_instance.platform_monitor = platform_monitor
    app_instance.background_worker = worker

    # Add callback for worker status changes
    def worker_status_callback(status):
        print(f"🔄 Background worker status: {status.value}")

    worker.add_status_callback(worker_status_callback)

    # Start worker
    worker.start()

    return worker, train_monitor, platform_monitor