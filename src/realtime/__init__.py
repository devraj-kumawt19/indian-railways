"""
Real-Time Services Add-On Package
Provides real-time train tracking capabilities for the Indian Train Detection System
"""

from .service import RealtimeTrainService
from src.scheduling.enhanced_status import EnhancedStatusCalculator
from .notifications import NotificationManager
from .worker import BackgroundWorker, TrainStatusMonitor, PlatformMonitor, integrate_background_worker
from .cloud import CloudIntegrationManager, CloudProvider, CloudConfig, integrate_cloud_services
from .ui_integration import StreamlitRealTimeUI, UIConfig, UIUpdateMode, integrate_realtime_ui, render_realtime_sidebar

__version__ = "1.0.0"
__author__ = "GitHub Copilot"
__description__ = "Real-time train tracking add-on for Indian Train Detection System"

__all__ = [
    # Core services
    'RealtimeTrainService',
    'EnhancedStatusCalculator',
    'NotificationManager',

    # Background monitoring
    'BackgroundWorker',
    'TrainStatusMonitor',
    'PlatformMonitor',
    'integrate_background_worker',

    # Cloud integration
    'CloudIntegrationManager',
    'CloudProvider',
    'CloudConfig',
    'integrate_cloud_services',

    # UI integration
    'StreamlitRealTimeUI',
    'UIConfig',
    'UIUpdateMode',
    'integrate_realtime_ui',
    'render_realtime_sidebar'
]