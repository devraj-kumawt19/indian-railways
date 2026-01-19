"""
UI Integration Add-On
Integrates real-time services with Streamlit UI for live updates
"""

import streamlit as st
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Callable
import threading
import json
from dataclasses import dataclass
from enum import Enum

# Import our add-on modules
try:
    from .service import RealtimeTrainService
    from src.scheduling.enhanced_status import EnhancedStatusCalculator
    from .notifications import NotificationManager
    from .worker import BackgroundWorker, TrainStatusMonitor, PlatformMonitor
    from .cloud import CloudIntegrationManager
except ImportError:
    # Fallback for direct execution
    from service import RealtimeTrainService
    from src.scheduling.enhanced_status import EnhancedStatusCalculator
    from notifications import NotificationManager
    from worker import BackgroundWorker, TrainStatusMonitor, PlatformMonitor
    from cloud import CloudIntegrationManager

class UIUpdateMode(Enum):
    """UI update modes."""
    POLLING = "polling"
    WEBSOCKET = "websocket"
    HYBRID = "hybrid"

@dataclass
class UIConfig:
    """UI integration configuration."""
    update_mode: UIUpdateMode = UIUpdateMode.POLLING
    poll_interval: int = 30  # seconds
    enable_notifications: bool = True
    enable_cloud_sync: bool = True
    max_display_items: int = 50
    auto_refresh: bool = True

class StreamlitRealTimeUI:
    """
    Integrates real-time services with Streamlit UI.
    Provides live updates, notifications, and cloud synchronization.
    """

    def __init__(self, config: UIConfig = None):
        self.config = config or UIConfig()
        self.realtime_service = None
        self.status_calculator = None
        self.notification_manager = None
        self.background_worker = None
        self.cloud_manager = None
        self.train_monitor = None
        self.platform_monitor = None

        # UI state
        self.last_update = datetime.now()
        self.update_counter = 0
        self.notification_queue: List[Dict] = []
        self.status_cache: Dict[str, Dict] = {}

        # Session state keys
        self.SESSION_KEYS = {
            'realtime_enabled': 'rt_enabled',
            'last_train_status': 'rt_last_status',
            'notifications': 'rt_notifications',
            'platform_status': 'rt_platform_status',
            'cloud_status': 'rt_cloud_status'
        }

    def initialize_services(self):
        """Initialize all real-time services."""
        try:
            # Initialize core services
            self.realtime_service = RealtimeTrainService()
            self.status_calculator = EnhancedStatusCalculator()
            self.notification_manager = NotificationManager()

            # Initialize monitoring services
            self.train_monitor = TrainStatusMonitor()
            self.platform_monitor = PlatformMonitor()

            # Create background worker
            from .worker import create_monitoring_worker
            self.background_worker = create_monitoring_worker(
                self.train_monitor, self.platform_monitor
            )

            # Initialize cloud integration
            self.cloud_manager = CloudIntegrationManager()

            # Connect services
            self._connect_services()

            print("✅ Real-time UI services initialized")
            return True

        except Exception as e:
            print(f"❌ Failed to initialize real-time services: {e}")
            return False

    def _connect_services(self):
        """Connect all services together."""
        # Connect notification manager to status calculator
        self.status_calculator.add_alert_callback(
            self.notification_manager.handle_status_change
        )

        # Connect notification manager to UI updates
        self.notification_manager.add_notification_callback(
            self._handle_notification
        )

        # Connect cloud manager to services
        if self.cloud_manager:
            self.status_calculator.add_alert_callback(
                self._handle_cloud_status_update
            )

    def start_services(self):
        """Start all background services."""
        if self.background_worker:
            self.background_worker.start()

        if self.realtime_service:
            self.realtime_service.start()

        print("🚀 Real-time services started")

    def stop_services(self):
        """Stop all background services."""
        if self.background_worker:
            self.background_worker.stop()

        if self.realtime_service:
            self.realtime_service.stop()

        if self.cloud_manager:
            self.cloud_manager.disconnect()

        print("🛑 Real-time services stopped")

    def _handle_notification(self, notification: Dict):
        """Handle incoming notifications."""
        self.notification_queue.append(notification)

        # Keep only recent notifications
        if len(self.notification_queue) > 20:
            self.notification_queue = self.notification_queue[-20:]

    def _handle_cloud_status_update(self, status_change: Dict):
        """Handle status changes for cloud sync."""
        if self.cloud_manager and self.cloud_manager.connected:
            train_no = status_change.get('train_no')
            if train_no:
                self.cloud_manager.publish_train_status(train_no, status_change)

    def update_ui_state(self):
        """Update Streamlit session state with real-time data."""
        if not st.session_state.get(self.SESSION_KEYS['realtime_enabled'], False):
            return

        current_time = datetime.now()

        # Update train statuses
        if self.status_calculator:
            active_trains = self.status_calculator.get_active_trains()
            for train_no in active_trains:
                status = self.status_calculator.get_train_status(train_no)
                if status:
                    self.status_cache[train_no] = status

        # Update platform statuses
        if self.platform_monitor:
            platforms = ['1', '2', '3', '4', '5']  # Common platforms
            platform_data = {}
            for platform in platforms:
                status = self.platform_monitor.get_platform_status(platform)
                if status:
                    platform_data[platform] = status

            st.session_state[self.SESSION_KEYS['platform_status']] = platform_data

        # Update cloud status
        if self.cloud_manager:
            cloud_status = self.cloud_manager.get_status()
            st.session_state[self.SESSION_KEYS['cloud_status']] = cloud_status

        # Update notifications
        if self.notification_queue:
            existing_notifications = st.session_state.get(self.SESSION_KEYS['notifications'], [])
            existing_notifications.extend(self.notification_queue)
            # Keep only recent notifications
            st.session_state[self.SESSION_KEYS['notifications']] = existing_notifications[-50:]
            self.notification_queue.clear()

        self.last_update = current_time
        self.update_counter += 1

    def render_realtime_dashboard(self):
        """Render the real-time dashboard in Streamlit."""
        st.header("🚀 Real-Time Train Tracking Dashboard")

        # Service status
        self._render_service_status()

        # Real-time controls
        self._render_realtime_controls()

        # Live train status
        self._render_live_train_status()

        # Platform status
        self._render_platform_status()

        # Notifications
        self._render_notifications()

        # Cloud status
        self._render_cloud_status()

    def _render_service_status(self):
        """Render service status indicators."""
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            realtime_status = "🟢 Active" if self.realtime_service and self.realtime_service.running else "🔴 Inactive"
            st.metric("Real-Time Service", realtime_status)

        with col2:
            worker_status = "🟢 Running" if self.background_worker and self.background_worker.status.value == "running" else "🔴 Stopped"
            st.metric("Background Worker", worker_status)

        with col3:
            cloud_status = "🟢 Connected" if self.cloud_manager and self.cloud_manager.connected else "🔴 Disconnected"
            st.metric("Cloud Service", cloud_status)

        with col4:
            last_update = self.last_update.strftime("%H:%M:%S") if self.last_update else "Never"
            st.metric("Last Update", last_update)

    def _render_realtime_controls(self):
        """Render real-time control panel."""
        with st.expander("⚙️ Real-Time Controls", expanded=False):
            col1, col2, col3 = st.columns(3)

            with col1:
                if st.button("🔄 Force Update", key="force_update"):
                    self.update_ui_state()
                    st.success("UI updated!")

            with col2:
                auto_refresh = st.checkbox(
                    "Auto Refresh",
                    value=self.config.auto_refresh,
                    key="auto_refresh_toggle"
                )
                self.config.auto_refresh = auto_refresh

            with col3:
                poll_interval = st.slider(
                    "Update Interval (seconds)",
                    min_value=5,
                    max_value=120,
                    value=self.config.poll_interval,
                    key="poll_interval_slider"
                )
                self.config.poll_interval = poll_interval

            # Service controls
            st.subheader("Service Controls")
            control_col1, control_col2, control_col3 = st.columns(3)

            with control_col1:
                if st.button("▶️ Start Services", key="start_services"):
                    self.start_services()
                    st.success("Services started!")

            with control_col2:
                if st.button("⏸️ Stop Services", key="stop_services"):
                    self.stop_services()
                    st.success("Services stopped!")

            with control_col3:
                if st.button("🔄 Restart Services", key="restart_services"):
                    self.stop_services()
                    time.sleep(1)
                    self.start_services()
                    st.success("Services restarted!")

    def _render_live_train_status(self):
        """Render live train status display."""
        st.subheader("🚆 Live Train Status")

        if not self.status_cache:
            st.info("No active trains being monitored. Add trains to monitoring to see live updates.")
            return

        # Display trains in a grid
        trains = list(self.status_cache.keys())
        cols = st.columns(min(len(trains), 3))

        for i, train_no in enumerate(trains):
            with cols[i % len(cols)]:
                status = self.status_cache[train_no]
                self._render_train_card(train_no, status)

    def _render_train_card(self, train_no: str, status: Dict):
        """Render individual train status card."""
        with st.container():
            # Status indicator
            status_color = self._get_status_color(status.get('status', 'Unknown'))
            st.markdown(f"### {status_color} Train {train_no}")

            # Key information
            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Status:** {status.get('status', 'Unknown')}")
                st.write(f"**Position:** {status.get('position', 'Unknown')}")

            with col2:
                delay = status.get('delay', 0)
                delay_text = f"{'🔴' if delay > 0 else '🟢'} {delay} min delay" if delay != 0 else "🟢 On time"
                st.write(f"**Delay:** {delay_text}")
                platform = status.get('platform')
                if platform:
                    st.write(f"**Platform:** {platform}")

            # Expected times
            if status.get('expected_arrival'):
                st.write(f"**Expected Arrival:** {status['expected_arrival']}")

            if status.get('expected_departure'):
                st.write(f"**Expected Departure:** {status['expected_departure']}")

            # Last updated
            if status.get('last_updated'):
                updated_time = status['last_updated']
                if isinstance(updated_time, str):
                    st.caption(f"Last updated: {updated_time}")
                else:
                    st.caption(f"Last updated: {updated_time.strftime('%H:%M:%S')}")

    def _render_platform_status(self):
        """Render platform status display."""
        st.subheader("🏗️ Platform Status")

        platform_data = st.session_state.get(self.SESSION_KEYS['platform_status'], {})

        if not platform_data:
            st.info("No platform data available.")
            return

        # Display platforms
        platforms = sorted(platform_data.keys())
        cols = st.columns(min(len(platforms), 5))

        for i, platform_no in enumerate(platforms):
            with cols[i % len(cols)]:
                status = platform_data[platform_no]
                self._render_platform_card(platform_no, status)

    def _render_platform_card(self, platform_no: str, status: Dict):
        """Render individual platform status card."""
        with st.container():
            status_indicator = self._get_platform_status_indicator(status.get('status', 'unknown'))
            st.markdown(f"### {status_indicator} Platform {platform_no}")

            train_no = status.get('train_no')
            if train_no:
                st.write(f"**Train:** {train_no}")
            else:
                st.write("**Status:** Available")

            if status.get('last_updated'):
                updated_time = status['last_updated']
                if isinstance(updated_time, str):
                    st.caption(f"Last updated: {updated_time}")
                else:
                    st.caption(f"Last updated: {updated_time.strftime('%H:%M:%S')}")

    def _render_notifications(self):
        """Render notifications panel."""
        st.subheader("🔔 Notifications")

        notifications = st.session_state.get(self.SESSION_KEYS['notifications'], [])

        if not notifications:
            st.info("No recent notifications.")
            return

        # Display recent notifications
        for notification in reversed(notifications[-10:]):  # Show last 10
            with st.container():
                notification_type = notification.get('type', 'info')
                icon = self._get_notification_icon(notification_type)

                col1, col2 = st.columns([1, 4])

                with col1:
                    st.write(icon)

                with col2:
                    st.write(f"**{notification.get('title', 'Notification')}**")
                    st.write(notification.get('message', ''))
                    if notification.get('timestamp'):
                        timestamp = notification['timestamp']
                        if isinstance(timestamp, str):
                            st.caption(f"{timestamp}")
                        else:
                            st.caption(f"{timestamp.strftime('%H:%M:%S')}")

                st.divider()

    def _render_cloud_status(self):
        """Render cloud integration status."""
        st.subheader("☁️ Cloud Integration")

        cloud_status = st.session_state.get(self.SESSION_KEYS['cloud_status'], {})

        if not cloud_status:
            st.info("Cloud integration not configured.")
            return

        col1, col2, col3 = st.columns(3)

        with col1:
            connected = "🟢 Connected" if cloud_status.get('connected', False) else "🔴 Disconnected"
            st.metric("Cloud Status", connected)

        with col2:
            provider = cloud_status.get('active_provider', 'None')
            st.metric("Provider", provider.title() if provider != 'None' else 'None')

        with col3:
            available = len(cloud_status.get('available_providers', []))
            st.metric("Available Providers", available)

        # Provider availability
        with st.expander("Provider Availability", expanded=False):
            providers = {
                'Firebase': cloud_status.get('firebase_available', False),
                'AWS': cloud_status.get('aws_available', False),
                'Azure': cloud_status.get('azure_available', False)
            }

            for provider, available in providers.items():
                status_icon = "✅" if available else "❌"
                st.write(f"{status_icon} {provider}: {'Available' if available else 'Not Available'}")

    def _get_status_color(self, status: str) -> str:
        """Get color indicator for train status."""
        status_lower = status.lower()
        if 'running' in status_lower or 'on time' in status_lower:
            return "🟢"
        elif 'delayed' in status_lower or 'late' in status_lower:
            return "🟡"
        elif 'cancelled' in status_lower:
            return "🔴"
        else:
            return "⚪"

    def _get_platform_status_indicator(self, status: str) -> str:
        """Get status indicator for platform."""
        status_lower = status.lower()
        if status_lower == 'occupied':
            return "🚆"
        elif status_lower == 'arriving':
            return "🚶"
        elif status_lower == 'departing':
            return "🚆"
        else:
            return "✅"

    def _get_notification_icon(self, notification_type: str) -> str:
        """Get icon for notification type."""
        type_lower = notification_type.lower()
        if 'arrival' in type_lower:
            return "🚆"
        elif 'departure' in type_lower:
            return "🚆"
        elif 'delay' in type_lower:
            return "⏰"
        elif 'platform' in type_lower:
            return "🏗️"
        elif 'error' in type_lower:
            return "❌"
        else:
            return "ℹ️"

    def enable_realtime_mode(self):
        """Enable real-time mode in session state."""
        st.session_state[self.SESSION_KEYS['realtime_enabled']] = True

    def disable_realtime_mode(self):
        """Disable real-time mode in session state."""
        st.session_state[self.SESSION_KEYS['realtime_enabled']] = False

    def is_realtime_enabled(self) -> bool:
        """Check if real-time mode is enabled."""
        return st.session_state.get(self.SESSION_KEYS['realtime_enabled'], False)

    def add_train_to_monitoring(self, train_no: str):
        """Add a train to real-time monitoring."""
        if self.train_monitor:
            self.train_monitor.add_train_to_monitor(train_no)

        if self.status_calculator:
            self.status_calculator.add_train_to_monitoring(train_no)

    def remove_train_from_monitoring(self, train_no: str):
        """Remove a train from real-time monitoring."""
        if self.train_monitor:
            self.train_monitor.remove_train_from_monitor(train_no)

        if self.status_calculator:
            self.status_calculator.remove_train_from_monitoring(train_no)


# Integration helper functions
def create_realtime_ui(config: UIConfig = None) -> StreamlitRealTimeUI:
    """
    Create and configure real-time UI integration.

    Args:
        config: UI configuration

    Returns:
        Configured StreamlitRealTimeUI instance
    """
    ui = StreamlitRealTimeUI(config)

    if ui.initialize_services():
        return ui
    else:
        st.error("Failed to initialize real-time services")
        return None

def integrate_realtime_ui(app_instance, ui_config: UIConfig = None):
    """
    Integrate real-time UI into existing Streamlit app.

    Args:
        app_instance: Existing Streamlit app instance
        ui_config: UI configuration
    """
    # Create real-time UI
    realtime_ui = create_realtime_ui(ui_config)

    if realtime_ui:
        # Add to app instance
        app_instance.realtime_ui = realtime_ui

        # Start services
        realtime_ui.start_services()

        # Enable real-time mode
        realtime_ui.enable_realtime_mode()

        return realtime_ui
    else:
        st.error("Failed to create real-time UI integration")
        return None

def render_realtime_sidebar(ui_instance: StreamlitRealTimeUI):
    """
    Render real-time controls in sidebar.

    Args:
        ui_instance: StreamlitRealTimeUI instance
    """
    with st.sidebar:
        st.header("🚀 Real-Time Controls")

        # Enable/disable real-time
        realtime_enabled = st.checkbox(
            "Enable Real-Time Updates",
            value=ui_instance.is_realtime_enabled(),
            key="sidebar_realtime_toggle"
        )

        if realtime_enabled:
            ui_instance.enable_realtime_mode()
        else:
            ui_instance.disable_realtime_mode()

        # Quick train monitoring
        st.subheader("Train Monitoring")

        train_no = st.text_input(
            "Add Train to Monitor",
            placeholder="Enter train number",
            key="sidebar_train_input"
        )

        if st.button("Add Train", key="sidebar_add_train"):
            if train_no:
                ui_instance.add_train_to_monitoring(train_no)
                st.success(f"Added train {train_no} to monitoring")
            else:
                st.error("Please enter a train number")

        # Service status
        st.subheader("Service Status")

        if ui_instance.realtime_service:
            service_status = "🟢 Running" if ui_instance.realtime_service.running else "🔴 Stopped"
            st.write(f"Real-Time Service: {service_status}")

        if ui_instance.background_worker:
            worker_status = ui_instance.background_worker.status.value.title()
            st.write(f"Background Worker: {worker_status}")

        if ui_instance.cloud_manager:
            cloud_status = "🟢 Connected" if ui_instance.cloud_manager.connected else "🔴 Disconnected"
            st.write(f"Cloud Service: {cloud_status}")

        # Last update info
        if ui_instance.last_update:
            time_since_update = datetime.now() - ui_instance.last_update
            st.caption(f"Last update: {time_since_update.seconds}s ago")