"""
Real-Time Integration Script
Demonstrates how to integrate real-time add-ons into the existing Indian Train Detection System
"""

import streamlit as st
import sys
import os
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import existing app components
try:
    from src.ui.app import TrainDetectionApp
except ImportError:
    st.error("Could not import existing TrainDetectionApp. Make sure the app structure is correct.")
    st.stop()

# Import real-time add-ons
try:
    from src.realtime import (
        RealtimeTrainService,
        EnhancedStatusCalculator,
        NotificationManager,
        BackgroundWorker,
        TrainStatusMonitor,
        PlatformMonitor,
        CloudIntegrationManager,
        CloudProvider,
        CloudConfig,
        StreamlitRealTimeUI,
        UIConfig,
        UIUpdateMode,
        integrate_realtime_ui,
        render_realtime_sidebar,
        integrate_background_worker,
        integrate_cloud_services
    )
except ImportError as e:
    st.error(f"Could not import real-time add-ons: {e}")
    st.error("Make sure all real-time modules are properly installed.")
    st.stop()

class EnhancedTrainDetectionApp(TrainDetectionApp):
    """
    Enhanced version of TrainDetectionApp with real-time capabilities.
    Extends the existing app without breaking existing functionality.
    """

    def __init__(self):
        super().__init__()

        # Add real-time components
        self.realtime_ui = None
        self.realtime_service = None
        self.enhanced_status_calculator = None
        self.notification_manager = None
        self.background_worker = None
        self.cloud_manager = None

        # Initialize real-time features
        self._initialize_realtime_features()

    def _initialize_realtime_features(self):
        """Initialize real-time features as add-ons."""
        try:
            # Create UI configuration
            ui_config = UIConfig(
                update_mode=UIUpdateMode.HYBRID,
                poll_interval=30,
                enable_notifications=True,
                enable_cloud_sync=True,
                auto_refresh=True
            )

            # Initialize real-time UI
            self.realtime_ui = StreamlitRealTimeUI(ui_config)

            # Initialize core services
            self.realtime_service = RealtimeTrainService()
            self.enhanced_status_calculator = EnhancedStatusCalculator()
            self.notification_manager = NotificationManager()

            # Initialize monitoring services
            train_monitor = TrainStatusMonitor()
            platform_monitor = PlatformMonitor()

            # Create background worker
            self.background_worker = BackgroundWorker("EnhancedTrainMonitor")

            # Add monitoring tasks
            from src.realtime.worker import create_monitoring_worker
            self.background_worker = create_monitoring_worker(
                train_monitor, platform_monitor
            )

            # Initialize cloud integration
            self.cloud_manager = CloudIntegrationManager()

            # Configure cloud services (optional)
            self._configure_cloud_services()

            # Connect all services
            self._connect_realtime_services()

            print("✅ Real-time features initialized successfully")

        except Exception as e:
            print(f"❌ Failed to initialize real-time features: {e}")
            # Continue without real-time features - graceful degradation

    def _configure_cloud_services(self):
        """Configure cloud services if credentials are available."""
        try:
            # Try to load Firebase configuration
            firebase_creds = os.getenv('FIREBASE_CREDENTIALS_PATH')
            firebase_url = os.getenv('FIREBASE_DATABASE_URL')

            if firebase_creds and firebase_url:
                firebase_config = CloudConfig(
                    provider=CloudProvider.FIREBASE,
                    credentials_path=firebase_creds,
                    database_url=firebase_url
                )
                self.cloud_manager.add_service(CloudProvider.FIREBASE, firebase_config)

            # Try to load AWS configuration
            aws_region = os.getenv('AWS_REGION')
            if aws_region:
                aws_config = CloudConfig(
                    provider=CloudProvider.AWS,
                    region=aws_region
                )
                self.cloud_manager.add_service(CloudProvider.AWS, aws_config)

            # Try to load Azure configuration
            azure_connection = os.getenv('AZURE_IOT_CONNECTION_STRING')
            if azure_connection:
                azure_config = CloudConfig(
                    provider=CloudProvider.AZURE,
                    endpoint=azure_connection
                )
                self.cloud_manager.add_service(CloudProvider.AZURE, azure_config)

        except Exception as e:
            print(f"⚠️ Cloud configuration failed: {e}")

    def _connect_realtime_services(self):
        """Connect all real-time services together."""
        # Connect status calculator to notification manager
        self.enhanced_status_calculator.add_alert_callback(
            self.notification_manager.handle_status_change
        )

        # Connect notification manager to UI updates
        self.notification_manager.add_notification_callback(
            self.realtime_ui._handle_notification
        )

        # Connect cloud manager to status updates
        if self.cloud_manager:
            self.enhanced_status_calculator.add_change_callback(
                self._handle_cloud_status_update
            )

    def _handle_cloud_status_update(self, status_change: Dict):
        """Handle status changes for cloud sync."""
        if self.cloud_manager and self.cloud_manager.connected:
            train_no = status_change.get('train_no')
            if train_no:
                self.cloud_manager.publish_train_status(train_no, status_change)

    def run_enhanced_app(self):
        """Run the enhanced app with real-time features."""
        # Start real-time services
        if self.realtime_ui:
            self.realtime_ui.start_services()

        # Run the main app
        self.run()

        # Add real-time dashboard
        self._render_realtime_section()

    def _render_realtime_section(self):
        """Render the real-time features section."""
        st.header("🚀 Real-Time Features")

        # Check if real-time features are available
        if not self.realtime_ui:
            st.warning("Real-time features are not available. Some add-ons may not be properly installed.")
            return

        # Render real-time sidebar controls
        render_realtime_sidebar(self.realtime_ui)

        # Render real-time dashboard
        self.realtime_ui.render_realtime_dashboard()

        # Update UI state periodically
        if self.realtime_ui.config.auto_refresh:
            self.realtime_ui.update_ui_state()

    def add_train_to_realtime_monitoring(self, train_no: str):
        """Add a train to real-time monitoring."""
        if self.realtime_ui:
            self.realtime_ui.add_train_to_monitoring(train_no)

        # Also add to enhanced status calculator
        if self.enhanced_status_calculator:
            self.enhanced_status_calculator.add_train_to_monitoring(train_no)

    def get_realtime_status(self) -> Dict:
        """Get real-time system status."""
        status = {
            'realtime_available': self.realtime_ui is not None,
            'services_running': False,
            'cloud_connected': False,
            'monitored_trains': 0,
            'active_notifications': 0
        }

        if self.realtime_ui:
            status['services_running'] = (
                self.realtime_service and self.realtime_service.running
            ) if self.realtime_service else False

            status['cloud_connected'] = (
                self.cloud_manager and self.cloud_manager.connected
            ) if self.cloud_manager else False

            if self.enhanced_status_calculator:
                status['monitored_trains'] = len(
                    self.enhanced_status_calculator.get_active_trains()
                )

            notifications = st.session_state.get('rt_notifications', [])
            status['active_notifications'] = len(notifications)

        return status


def main():
    """Main function to run the enhanced app."""
    st.set_page_config(
        page_title="Indian Train Detection System - Real-Time",
        page_icon="🚆",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Create enhanced app
    app = EnhancedTrainDetectionApp()

    # Add custom CSS for real-time features
    st.markdown("""
    <style>
    .realtime-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background-color: #00ff00;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }

    .notification-card {
        border-left: 4px solid #ff6b6b;
        padding: 10px;
        margin: 5px 0;
        background-color: #f8f9fa;
        border-radius: 5px;
    }

    .status-card {
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 15px;
        margin: 10px 0;
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

    # Run enhanced app
    app.run_enhanced_app()


if __name__ == "__main__":
    main()