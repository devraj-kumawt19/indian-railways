"""
Notification System Add-On
Provides real-time notifications and alerts for train updates
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import json
import streamlit as st

class NotificationType(Enum):
    """Types of notifications."""
    TRAIN_ARRIVAL = "train_arrival"
    TRAIN_DEPARTURE = "train_departure"
    PLATFORM_CHANGE = "platform_change"
    DELAY_UPDATE = "delay_update"
    STATUS_CHANGE = "status_change"
    GENERAL_ALERT = "general_alert"

class NotificationPriority(Enum):
    """Notification priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class Notification:
    """Notification data structure."""
    id: str
    type: NotificationType
    title: str
    message: str
    priority: NotificationPriority
    train_no: Optional[str] = None
    platform: Optional[str] = None
    timestamp: Optional[datetime] = None
    expires_at: Optional[datetime] = None
    is_read: bool = False
    metadata: Optional[Dict] = None

    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()
        if self.metadata is None:
            self.metadata = {}
        if self.expires_at is None:
            # Default expiration: 1 hour for regular, 24 hours for critical
            if self.priority == NotificationPriority.CRITICAL:
                self.expires_at = self.timestamp + timedelta(hours=24)
            else:
                self.expires_at = self.timestamp + timedelta(hours=1)

    def to_dict(self) -> Dict:
        """Convert to dictionary for serialization."""
        return {
            'id': self.id,
            'type': self.type.value,
            'title': self.title,
            'message': self.message,
            'priority': self.priority.value,
            'train_no': self.train_no,
            'platform': self.platform,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'is_read': self.is_read,
            'metadata': self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'Notification':
        """Create from dictionary."""
        data_copy = data.copy()
        data_copy['type'] = NotificationType(data_copy['type'])
        data_copy['priority'] = NotificationPriority(data_copy['priority'])
        if 'timestamp' in data_copy and data_copy['timestamp']:
            data_copy['timestamp'] = datetime.fromisoformat(data_copy['timestamp'])
        if 'expires_at' in data_copy and data_copy['expires_at']:
            data_copy['expires_at'] = datetime.fromisoformat(data_copy['expires_at'])
        return cls(**data_copy)

    def is_expired(self) -> bool:
        """Check if notification has expired."""
        return datetime.now() > self.expires_at

    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True

class NotificationManager:
    """
    Manages notifications and alerts for the train system.
    Add-on component that integrates with existing UI.
    """

    def __init__(self, max_notifications: int = 100):
        self.notifications: List[Notification] = []
        self.max_notifications = max_notifications
        self.subscribers: List[Callable] = []
        self.notification_filters: Dict[str, Callable] = {}

    def add_notification(self, notification: Notification):
        """Add a new notification."""
        # Check if notification already exists (avoid duplicates)
        existing = next((n for n in self.notifications
                        if n.id == notification.id), None)
        if existing:
            return

        # Add to list
        self.notifications.insert(0, notification)  # Add to beginning

        # Maintain max limit
        if len(self.notifications) > self.max_notifications:
            self.notifications = self.notifications[:self.max_notifications]

        # Notify subscribers
        self._notify_subscribers(notification)

        print(f"🔔 New notification: {notification.title}")

    def create_notification(self, type: NotificationType, title: str, message: str,
                          priority: NotificationPriority = NotificationPriority.MEDIUM,
                          **kwargs) -> Notification:
        """Create and add a notification."""
        notification_id = f"{type.value}_{int(datetime.now().timestamp() * 1000)}"

        notification = Notification(
            id=notification_id,
            type=type,
            title=title,
            message=message,
            priority=priority,
            **kwargs
        )

        self.add_notification(notification)
        return notification

    def get_notifications(self, unread_only: bool = False,
                         priority_filter: Optional[NotificationPriority] = None,
                         type_filter: Optional[NotificationType] = None,
                         limit: Optional[int] = None) -> List[Notification]:
        """Get notifications with optional filtering."""
        notifications = self.notifications.copy()

        # Apply filters
        if unread_only:
            notifications = [n for n in notifications if not n.is_read]

        if priority_filter:
            notifications = [n for n in notifications if n.priority == priority_filter]

        if type_filter:
            notifications = [n for n in notifications if n.type == type_filter]

        # Remove expired notifications
        notifications = [n for n in notifications if not n.is_expired()]

        # Apply limit
        if limit:
            notifications = notifications[:limit]

        return notifications

    def mark_as_read(self, notification_id: str):
        """Mark a notification as read."""
        for notification in self.notifications:
            if notification.id == notification_id:
                notification.mark_as_read()
                break

    def mark_all_as_read(self):
        """Mark all notifications as read."""
        for notification in self.notifications:
            notification.mark_as_read()

    def delete_notification(self, notification_id: str):
        """Delete a notification."""
        self.notifications = [n for n in self.notifications if n.id != notification_id]

    def clear_expired(self):
        """Clear expired notifications."""
        self.notifications = [n for n in self.notifications if not n.is_expired()]

    def add_subscriber(self, callback: Callable):
        """Add a subscriber for new notifications."""
        self.subscribers.append(callback)

    def add_notification_callback(self, callback: Callable):
        """Add a callback for notification events (alias for add_subscriber)."""
        self.add_subscriber(callback)

    def remove_subscriber(self, callback: Callable):
        """Remove a subscriber."""
        if callback in self.subscribers:
            self.subscribers.remove(callback)

    def _notify_subscribers(self, notification: Notification):
        """Notify all subscribers of new notification."""
        for subscriber in self.subscribers:
            try:
                subscriber(notification)
            except Exception as e:
                print(f"Subscriber notification error: {e}")

    def get_stats(self) -> Dict:
        """Get notification statistics."""
        total = len(self.notifications)
        unread = len([n for n in self.notifications if not n.is_read])
        expired = len([n for n in self.notifications if n.is_expired()])

        by_priority = {}
        for priority in NotificationPriority:
            by_priority[priority.value] = len([n for n in self.notifications if n.priority == priority])

        by_type = {}
        for ntype in NotificationType:
            by_type[ntype.value] = len([n for n in self.notifications if n.type == ntype])

        return {
            'total': total,
            'unread': unread,
            'expired': expired,
            'by_priority': by_priority,
            'by_type': by_type
        }

    def handle_status_change(self, alert_data: Dict):
        """
        Handle status change alerts from the status calculator.
        Creates appropriate notifications based on the change type.
        """
        train_no = alert_data.get('train_no', 'Unknown')
        change = alert_data.get('change', 'Status changed')

        # Create appropriate notification
        if 'arrived' in change.lower():
            notification_type = NotificationType.TRAIN_ARRIVAL
            title = f"🚆 Train {train_no} Arrived"
        elif 'departed' in change.lower():
            notification_type = NotificationType.TRAIN_DEPARTURE
            title = f"🚆 Train {train_no} Departed"
        elif 'platform' in change.lower():
            notification_type = NotificationType.PLATFORM_CHANGE
            title = f"🔄 Platform Change - Train {train_no}"
        elif 'delay' in change.lower():
            notification_type = NotificationType.DELAY_UPDATE
            title = f"⏰ Delay Update - Train {train_no}"
        else:
            notification_type = NotificationType.STATUS_CHANGE
            title = f"📢 Status Update - Train {train_no}"

        self.create_notification(
            type=notification_type,
            title=title,
            message=change,
            priority=NotificationPriority.MEDIUM,
            train_no=train_no
        )


class NotificationUI:
    """
    UI components for notifications.
    Add-on components for Streamlit integration.
    """

    def __init__(self, notification_manager: NotificationManager):
        self.manager = notification_manager

    def render_notification_bell(self) -> str:
        """Render notification bell with unread count."""
        unread_count = len(self.manager.get_notifications(unread_only=True))

        bell_color = "#dc3545" if unread_count > 0 else "#6c757d"
        bell_icon = "🔔" if unread_count == 0 else "🔔"

        badge_html = ""
        if unread_count > 0:
            badge_html = f"""
            <span style="position: absolute; top: -8px; right: -8px;
                         background: #dc3545; color: white; border-radius: 50%;
                         width: 18px; height: 18px; font-size: 11px;
                         display: flex; align-items: center; justify-content: center;
                         font-weight: bold;">
                {unread_count if unread_count < 10 else '9+'}
            </span>
            """

        return f"""
        <div style="position: relative; display: inline-block;">
            <span style="font-size: 1.5rem; color: {bell_color}; cursor: pointer;">
                {bell_icon}
            </span>
            {badge_html}
        </div>
        """

    def render_notification_panel(self, max_display: int = 10) -> str:
        """Render notification panel."""
        notifications = self.manager.get_notifications(limit=max_display)

        if not notifications:
            return """
            <div style="background: white; border-radius: 12px; padding: 2rem; text-align: center;
                        box-shadow: 0 2px 8px rgba(0,0,0,0.1);">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🔔</div>
                <div style="color: #6c757d;">No notifications yet</div>
            </div>
            """

        notification_html = ""
        for notification in notifications:
            # Priority styling
            priority_styles = {
                NotificationPriority.LOW: {"bg": "#f8f9fa", "border": "#dee2e6", "icon": "ℹ️"},
                NotificationPriority.MEDIUM: {"bg": "#fff3cd", "border": "#ffc107", "icon": "⚠️"},
                NotificationPriority.HIGH: {"bg": "#f8d7da", "border": "#dc3545", "icon": "🚨"},
                NotificationPriority.CRITICAL: {"bg": "#f5c6cb", "border": "#b02a37", "icon": "🚨"}
            }

            style = priority_styles.get(notification.priority, priority_styles[NotificationPriority.MEDIUM])

            read_style = "opacity: 0.6;" if notification.is_read else ""

            time_str = notification.timestamp.strftime("%H:%M") if notification.timestamp else "N/A"

            notification_html += f"""
            <div style="background: {style['bg']}; border: 1px solid {style['border']};
                        border-radius: 8px; padding: 1rem; margin: 0.5rem 0; {read_style}
                        cursor: pointer; transition: all 0.2s;">
                <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                    <span style="font-size: 1.2rem;">{style['icon']}</span>
                    <div style="flex: 1;">
                        <div style="font-weight: bold; color: #2c3e50; margin-bottom: 0.25rem;">
                            {notification.title}
                        </div>
                        <div style="color: #6c757d; font-size: 0.9rem; margin-bottom: 0.5rem;">
                            {notification.message}
                        </div>
                        <div style="display: flex; justify-content: space-between; align-items: center;">
                            <span style="font-size: 0.8rem; color: #6c757d;">
                                {notification.train_no or 'System'}
                            </span>
                            <span style="font-size: 0.8rem; color: #6c757d;">
                                {time_str}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
            """

        stats = self.manager.get_stats()

        return f"""
        <div style="background: white; border-radius: 12px; padding: 1rem;
                    box-shadow: 0 2px 8px rgba(0,0,0,0.1); max-height: 600px; overflow-y: auto;">
            <div style="display: flex; justify-content: space-between; align-items: center;
                        margin-bottom: 1rem; padding-bottom: 0.5rem; border-bottom: 1px solid #dee2e6;">
                <h4 style="margin: 0; color: #2c3e50;">🔔 Notifications</h4>
                <div style="font-size: 0.8rem; color: #6c757d;">
                    {stats['unread']} unread of {stats['total']}
                </div>
            </div>
            {notification_html}
            {f'<div style="text-align: center; margin-top: 1rem; padding-top: 0.5rem; border-top: 1px solid #dee2e6;">' +
             f'<button style="background: #007bff; color: white; border: none; padding: 0.5rem 1rem; ' +
             f'border-radius: 6px; cursor: pointer;">Load More</button></div>' if len(notifications) >= max_display else ''}
        </div>
        """

    def render_notification_toast(self, notification: Notification) -> str:
        """Render a toast notification."""
        priority_styles = {
            NotificationPriority.LOW: {"bg": "#d1ecf1", "border": "#bee5eb", "text": "#0c5460"},
            NotificationPriority.MEDIUM: {"bg": "#fff3cd", "border": "#ffeaa7", "text": "#856404"},
            NotificationPriority.HIGH: {"bg": "#f8d7da", "border": "#f5c6cb", "text": "#721c24"},
            NotificationPriority.CRITICAL: {"bg": "#f5c6cb", "border": "#f1aeb5", "text": "#721c24"}
        }

        style = priority_styles.get(notification.priority, priority_styles[NotificationPriority.MEDIUM])

        return f"""
        <div id="toast-{notification.id}" style="position: fixed; top: 20px; right: 20px;
                    background: {style['bg']}; border: 1px solid {style['border']};
                    border-radius: 8px; padding: 1rem; min-width: 300px; max-width: 400px;
                    box-shadow: 0 4px 12px rgba(0,0,0,0.15); z-index: 1000;
                    animation: slideIn 0.3s ease-out;">
            <div style="display: flex; align-items: flex-start; gap: 0.75rem;">
                <div style="flex: 1;">
                    <div style="font-weight: bold; color: {style['text']}; margin-bottom: 0.25rem;">
                        {notification.title}
                    </div>
                    <div style="color: {style['text']}; font-size: 0.9rem;">
                        {notification.message}
                    </div>
                </div>
                <button onclick="this.parentElement.parentElement.remove()"
                        style="background: none; border: none; font-size: 1.2rem;
                               cursor: pointer; color: {style['text']}; opacity: 0.7;">
                    ×
                </button>
            </div>
        </div>
        <style>
        @keyframes slideIn {{
            from {{ transform: translateX(100%); opacity: 0; }}
            to {{ transform: translateX(0); opacity: 1; }}
        }}
        </style>
        """


# Integration helper functions
def integrate_notifications(app_instance):
    """
    Integrate notification system into existing app.

    Args:
        app_instance: Existing TrainDetectionApp instance
    """
    # Create notification manager
    notification_manager = NotificationManager()
    notification_ui = NotificationUI(notification_manager)

    # Add to app instance
    app_instance.notifications = notification_manager
    app_instance.notification_ui = notification_ui

    # Add notification callback for status changes
    def status_change_callback(alert_data):
        train_no = alert_data.get('train_no', 'Unknown')
        change = alert_data.get('change', 'Status changed')

        # Create appropriate notification
        if 'arrived' in change.lower():
            notification_type = NotificationType.TRAIN_ARRIVAL
            title = f"🚆 Train {train_no} Arrived"
        elif 'departed' in change.lower():
            notification_type = NotificationType.TRAIN_DEPARTURE
            title = f"🚆 Train {train_no} Departed"
        elif 'platform' in change.lower():
            notification_type = NotificationType.PLATFORM_CHANGE
            title = f"🔄 Platform Change - Train {train_no}"
        elif 'delay' in change.lower():
            notification_type = NotificationType.DELAY_UPDATE
            title = f"⏰ Delay Update - Train {train_no}"
        else:
            notification_type = NotificationType.STATUS_CHANGE
            title = f"📢 Status Update - Train {train_no}"

        notification_manager.create_notification(
            type=notification_type,
            title=title,
            message=change,
            priority=NotificationPriority.MEDIUM,
            train_no=train_no
        )

    # Connect to status calculator if available
    if hasattr(app_instance, 'status_calculator') and hasattr(app_instance.status_calculator, 'add_alert_callback'):
        app_instance.status_calculator.add_alert_callback(status_change_callback)

    return notification_manager, notification_ui


# Example usage and integration
def create_sample_notifications(notification_manager: NotificationManager):
    """Create sample notifications for testing."""
    notification_manager.create_notification(
        type=NotificationType.TRAIN_ARRIVAL,
        title="🚆 Train 12301 Arrived",
        message="Train 12301 has arrived at Platform 2",
        priority=NotificationPriority.HIGH,
        train_no="12301",
        platform="2"
    )

    notification_manager.create_notification(
        type=NotificationType.PLATFORM_CHANGE,
        title="🔄 Platform Change Alert",
        message="Train 12302 platform changed from 3 to 4",
        priority=NotificationPriority.CRITICAL,
        train_no="12302",
        platform="4"
    )

    notification_manager.create_notification(
        type=NotificationType.DELAY_UPDATE,
        title="⏰ Delay Update",
        message="Train 12303 delayed by 15 minutes",
        priority=NotificationPriority.MEDIUM,
        train_no="12303"
    )