"""
Real-Time Train Tracking Add-On Module
Provides WebSocket and Firebase integration for live train updates
"""

import asyncio
import json
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable, Any
import websockets
import requests
from queue import Queue
import streamlit as st

try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

class RealtimeTrainService:
    """
    Real-time train tracking service with multiple backend support.
    Add-on module that integrates with existing train management system.
    """

    def __init__(self, firebase_config: Optional[Dict] = None, websocket_url: Optional[str] = None):
        """
        Initialize real-time service with optional Firebase and WebSocket support.

        Args:
            firebase_config: Firebase configuration dictionary
            websocket_url: WebSocket server URL for real-time updates
        """
        self.firebase_config = firebase_config
        self.websocket_url = websocket_url
        self.firebase_app = None
        self.websocket_client = None
        self.is_connected = False
        self.update_callbacks: List[Callable] = []
        self.train_status_cache: Dict[str, Dict] = {}
        self.notification_queue = Queue()
        self.monitoring_thread = None
        self.websocket_thread = None
        self.running = False

        # Initialize Firebase if config provided
        if FIREBASE_AVAILABLE and firebase_config:
            self._init_firebase()

        # Initialize WebSocket if URL provided
        if websocket_url:
            self._init_websocket()

    def _init_firebase(self):
        """Initialize Firebase Realtime Database."""
        try:
            if not firebase_admin._apps:
                cred = credentials.Certificate(self.firebase_config)
                self.firebase_app = firebase_admin.initialize_app(cred, {
                    'databaseURL': self.firebase_config.get('databaseURL')
                })
            self.is_connected = True
            print("✅ Firebase Realtime Database initialized")
        except Exception as e:
            print(f"❌ Firebase initialization failed: {e}")

    def _init_websocket(self):
        """Initialize WebSocket connection."""
        try:
            self.websocket_client = websocket.WebSocketApp(
                self.websocket_url,
                on_message=self._on_websocket_message,
                on_error=self._on_websocket_error,
                on_close=self._on_websocket_close,
                on_open=self._on_websocket_open
            )
            print("✅ WebSocket client initialized")
        except Exception as e:
            print(f"❌ WebSocket initialization failed: {e}")

    def _on_websocket_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        try:
            data = json.loads(message)
            self._process_realtime_update(data)
        except json.JSONDecodeError:
            print(f"Invalid JSON received: {message}")

    def _on_websocket_error(self, ws, error):
        """Handle WebSocket errors."""
        print(f"WebSocket error: {error}")

    def _on_websocket_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket connection close."""
        print("WebSocket connection closed")
        self.is_connected = False

    def _on_websocket_open(self, ws):
        """Handle WebSocket connection open."""
        print("WebSocket connection established")
        self.is_connected = True

    def _process_realtime_update(self, data: Dict):
        """Process real-time train updates."""
        train_no = data.get('train_no')
        if not train_no:
            return

        # Update cache
        self.train_status_cache[train_no] = {
            **data,
            'last_updated': datetime.now(),
            'source': 'realtime'
        }

        # Trigger callbacks
        for callback in self.update_callbacks:
            try:
                callback(train_no, data)
            except Exception as e:
                print(f"Callback error: {e}")

        # Add to notification queue if significant change
        if self._is_significant_update(data):
            self.notification_queue.put({
                'type': 'train_update',
                'train_no': train_no,
                'data': data,
                'timestamp': datetime.now()
            })

    def _is_significant_update(self, data: Dict) -> bool:
        """Check if update is significant enough for notification."""
        significant_events = ['arrived', 'departed', 'platform_changed', 'delayed', 'cancelled']
        status = data.get('status', '').lower()
        return any(event in status for event in significant_events)

    def add_update_callback(self, callback: Callable):
        """Add callback function for real-time updates."""
        self.update_callbacks.append(callback)

    def remove_update_callback(self, callback: Callable):
        """Remove callback function."""
        if callback in self.update_callbacks:
            self.update_callbacks.remove(callback)

    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get current status of a train."""
        return self.train_status_cache.get(train_no)

    def update_train_status(self, train_no: str, status_data: Dict):
        """Update train status (for admin/backoffice use)."""
        if FIREBASE_AVAILABLE and self.firebase_app:
            try:
                ref = db.reference(f'trains/{train_no}')
                ref.update({
                    **status_data,
                    'last_updated': datetime.now().isoformat(),
                    'updated_by': 'system'
                })
            except Exception as e:
                print(f"Firebase update failed: {e}")

        # Also update local cache
        self.train_status_cache[train_no] = {
            **status_data,
            'last_updated': datetime.now(),
            'source': 'manual'
        }

    def start_realtime_monitoring(self):
        """Start real-time monitoring in background thread."""
        if self.running:
            return

        self.running = True

        # Start WebSocket thread
        if self.websocket_client:
            self.websocket_thread = threading.Thread(
                target=self.websocket_client.run_forever,
                daemon=True
            )
            self.websocket_thread.start()

        # Start monitoring thread
        self.monitoring_thread = threading.Thread(
            target=self._monitoring_loop,
            daemon=True
        )
        self.monitoring_thread.start()

        print("✅ Real-time monitoring started")

    def stop_realtime_monitoring(self):
        """Stop real-time monitoring."""
        self.running = False

        if self.websocket_client:
            self.websocket_client.close()

        print("🛑 Real-time monitoring stopped")

    def _monitoring_loop(self):
        """Background monitoring loop."""
        while self.running:
            try:
                # Process notification queue
                while not self.notification_queue.empty():
                    notification = self.notification_queue.get_nowait()
                    self._handle_notification(notification)

                # Periodic health check
                if self.is_connected:
                    # Could add periodic status checks here
                    pass

                time.sleep(1)  # Check every second

            except Exception as e:
                print(f"Monitoring loop error: {e}")
                time.sleep(5)  # Wait before retry

    def _handle_notification(self, notification: Dict):
        """Handle notifications (could integrate with UI)."""
        print(f"🔔 Notification: {notification}")

    def get_connection_status(self) -> Dict:
        """Get connection status of all services."""
        return {
            'firebase_connected': FIREBASE_AVAILABLE and self.firebase_app is not None,
            'websocket_connected': self.websocket_client is not None and self.is_connected,
            'monitoring_active': self.running
        }


class RealtimeUIComponents:
    """
    UI components for real-time train tracking.
    Add-on components that integrate with existing Streamlit app.
    """

    def __init__(self, realtime_service: RealtimeTrainService):
        self.realtime_service = realtime_service
        self.status_indicators = {}
        self.last_updates = {}

    def render_realtime_status_card(self, train_no: str, train_data: Dict) -> str:
        """
        Render a real-time status card for a train.
        Returns HTML string for integration with existing UI.
        """
        status = train_data.get('status', 'Unknown')
        platform = train_data.get('platform', 'TBD')
        delay = train_data.get('delay', 0)
        last_updated = train_data.get('last_updated', datetime.now())

        # Determine status styling
        status_colors = {
            'On Time': '#28a745',
            'Arrived': '#007bff',
            'Departed': '#6c757d',
            'Delayed': '#ffc107',
            'Cancelled': '#dc3545'
        }

        color = status_colors.get(status, '#6c757d')

        # Real-time indicator
        is_live = (datetime.now() - last_updated).seconds < 30
        live_indicator = "🟢 LIVE" if is_live else "⚪"

        html = f"""
        <div style="background: white; border-radius: 12px; padding: 1rem; margin: 0.5rem 0;
                    border-left: 4px solid {color}; box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                <h4 style="margin: 0; color: #2c3e50;">Train {train_no}</h4>
                <span style="background: {color}; color: white; padding: 0.25rem 0.5rem;
                      border-radius: 12px; font-size: 0.8rem; font-weight: bold;">
                    {status}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-size: 0.9rem; color: #6c757d;">
                        Platform: <strong>{platform}</strong>
                    </div>
                    {f'<div style="font-size: 0.9rem; color: #dc3545;">Delay: {delay} mins</div>' if delay > 0 else ''}
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.8rem; color: #28a745; font-weight: bold;">
                        {live_indicator}
                    </div>
                    <div style="font-size: 0.7rem; color: #6c757d;">
                        {last_updated.strftime('%H:%M:%S')}
                    </div>
                </div>
            </div>
        </div>
        """

        return html

    def render_connection_status(self) -> str:
        """Render connection status indicator."""
        status = self.realtime_service.get_connection_status()

        indicators = []
        if status['firebase_connected']:
            indicators.append('<span style="color: #28a745;">🔥 Firebase: Connected</span>')
        else:
            indicators.append('<span style="color: #dc3545;">🔥 Firebase: Disconnected</span>')

        if status['websocket_connected']:
            indicators.append('<span style="color: #28a745;">🔌 WebSocket: Connected</span>')
        else:
            indicators.append('<span style="color: #dc3545;">🔌 WebSocket: Disconnected</span>')

        if status['monitoring_active']:
            indicators.append('<span style="color: #28a745;">📡 Monitoring: Active</span>')
        else:
            indicators.append('<span style="color: #dc3545;">📡 Monitoring: Inactive</span>')

        return f"""
        <div style="background: #f8f9fa; padding: 0.75rem; border-radius: 8px; margin: 1rem 0;
                    border: 1px solid #dee2e6;">
            <div style="font-size: 0.9rem; font-weight: bold; margin-bottom: 0.5rem; color: #2c3e50;">
                🔄 Real-Time Status
            </div>
            <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                {" | ".join(indicators)}
            </div>
        </div>
        """

    def render_notification_panel(self, max_notifications: int = 5) -> str:
        """Render recent notifications panel."""
        # This would integrate with the notification queue
        notifications = [
            {"type": "arrival", "message": "Train 12301 arrived at Platform 2", "time": "14:30:15"},
            {"type": "delay", "message": "Train 12302 delayed by 15 mins", "time": "14:25:30"},
            {"type": "platform_change", "message": "Train 12303 platform changed to 4", "time": "14:20:45"}
        ]

        notification_html = ""
        for notification in notifications[:max_notifications]:
            icon = {"arrival": "🚆", "delay": "⏰", "platform_change": "🔄"}.get(notification["type"], "📢")
            notification_html += f"""
            <div style="display: flex; align-items: center; padding: 0.5rem; margin: 0.25rem 0;
                        background: #fff3cd; border-radius: 6px; border-left: 3px solid #ffc107;">
                <span style="margin-right: 0.5rem;">{icon}</span>
                <span style="flex: 1; font-size: 0.9rem;">{notification["message"]}</span>
                <span style="font-size: 0.8rem; color: #6c757d;">{notification["time"]}</span>
            </div>
            """

        return f"""
        <div style="background: white; border-radius: 12px; padding: 1rem; margin: 1rem 0;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
            <h5 style="margin: 0 0 1rem 0; color: #2c3e50;">🔔 Recent Notifications</h5>
            {notification_html}
        </div>
        """


# Integration helper functions
def integrate_realtime_service(app_instance, firebase_config: Optional[Dict] = None,
                              websocket_url: Optional[str] = None):
    """
    Integration function to add real-time capabilities to existing app.

    Args:
        app_instance: Existing TrainDetectionApp instance
        firebase_config: Firebase configuration
        websocket_url: WebSocket URL
    """
    # Create real-time service
    realtime_service = RealtimeTrainService(firebase_config, websocket_url)
    ui_components = RealtimeUIComponents(realtime_service)

    # Add to app instance
    app_instance.realtime_service = realtime_service
    app_instance.realtime_ui = ui_components

    # Add callback for status updates
    def status_update_callback(train_no, data):
        # Update app's internal status
        if hasattr(app_instance, 'status_calculator'):
            app_instance.status_calculator.detection_times[train_no] = datetime.now()

    realtime_service.add_update_callback(status_update_callback)

    # Start monitoring
    realtime_service.start_realtime_monitoring()

    return realtime_service, ui_components


# Example Firebase configuration
DEFAULT_FIREBASE_CONFIG = {
    "type": "service_account",
    "project_id": "your-project-id",
    "private_key_id": "your-private-key-id",
    "private_key": "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY\n-----END PRIVATE KEY-----\n",
    "client_email": "firebase-adminsdk@your-project.iam.gserviceaccount.com",
    "client_id": "your-client-id",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk%40your-project.iam.gserviceaccount.com"
}