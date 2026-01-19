# Real-Time Train Tracking Add-Ons

This package provides real-time train tracking capabilities for the Indian Train Detection System. These add-ons extend the existing application with live updates, cloud integration, and advanced monitoring features without breaking existing functionality.

## Features

### 🚀 Real-Time Services
- **WebSocket Integration**: Real-time communication for live updates
- **Background Monitoring**: Continuous train status monitoring
- **Platform Detection**: Live platform arrival/departure tracking
- **Status Updates**: Enhanced train status calculation with live data

### ☁️ Cloud Integration
- **Firebase Support**: Real-time database synchronization
- **AWS IoT**: Cloud-based pub/sub messaging
- **Azure IoT Hub**: Enterprise-grade IoT integration
- **Multi-Provider**: Automatic failover between cloud providers

### 🔔 Notification System
- **Real-Time Alerts**: Instant notifications for train events
- **Platform Changes**: Alerts for platform assignments
- **Delay Notifications**: Automatic delay alerts
- **Customizable**: User-configurable notification preferences

### 📊 Enhanced UI
- **Live Dashboard**: Real-time train and platform status
- **Interactive Controls**: Start/stop monitoring services
- **Status Indicators**: Visual status indicators for all services
- **Responsive Design**: Mobile-friendly real-time interface

## Installation

### Basic Installation
```bash
# Install core real-time dependencies
pip install websockets schedule pytz
```

### Cloud Integration (Optional)
```bash
# Install from realtime_requirements.txt
pip install -r realtime_requirements.txt
```

### Firebase Setup
1. Create a Firebase project at https://console.firebase.google.com/
2. Enable Realtime Database
3. Download service account credentials JSON
4. Set environment variables:
```bash
export FIREBASE_CREDENTIALS_PATH="/path/to/serviceAccountKey.json"
export FIREBASE_DATABASE_URL="https://your-project.firebaseio.com/"
```

### AWS Setup
1. Configure AWS credentials
2. Set region:
```bash
export AWS_REGION="us-east-1"
```

### Azure Setup
1. Create IoT Hub in Azure portal
2. Get connection string
3. Set environment variable:
```bash
export AZURE_IOT_CONNECTION_STRING="your-connection-string"
```

## Usage

### Basic Integration

```python
from enhanced_app import EnhancedTrainDetectionApp

# Create enhanced app with real-time features
app = EnhancedTrainDetectionApp()
app.run_enhanced_app()
```

### Manual Integration

```python
import streamlit as st
from ui.app import TrainDetectionApp
from realtime import (
    StreamlitRealTimeUI,
    UIConfig,
    integrate_realtime_ui,
    render_realtime_sidebar
)

# Create your existing app
app = TrainDetectionApp()

# Add real-time features
ui_config = UIConfig(
    update_mode=UIUpdateMode.HYBRID,
    poll_interval=30,
    enable_notifications=True
)

realtime_ui = integrate_realtime_ui(app, ui_config)

# In your Streamlit app
def main():
    st.set_page_config(page_title="Real-Time Train Tracking", layout="wide")

    # Your existing app content
    app.render_main_interface()

    # Add real-time sidebar
    render_realtime_sidebar(realtime_ui)

    # Add real-time dashboard
    realtime_ui.render_realtime_dashboard()

if __name__ == "__main__":
    main()
```

### Adding Trains to Monitoring

```python
# Add train to real-time monitoring
app.add_train_to_realtime_monitoring("12512")

# Or directly through UI
realtime_ui.add_train_to_monitoring("12512")
```

## Architecture

### Modular Design
The add-ons are designed as separate modules that extend existing functionality:

```
src/realtime/
├── __init__.py          # Package initialization
├── service.py           # Core real-time service (WebSocket)
├── enhanced_status.py   # Enhanced status calculation
├── notifications.py     # Notification management
├── worker.py           # Background monitoring worker
├── cloud.py            # Cloud integration (Firebase/AWS/Azure)
└── ui_integration.py   # Streamlit UI integration
```

### Service Integration
- **Non-Intrusive**: Add-ons don't modify existing code
- **Graceful Degradation**: Features work even if cloud services unavailable
- **Background Processing**: Monitoring runs in background threads
- **State Management**: Uses Streamlit session state for UI persistence

## API Reference

### RealTimeService
```python
from realtime.service import RealTimeService

service = RealTimeService()
service.start()
service.add_train_listener("12512", callback_function)
service.stop()
```

### EnhancedStatusCalculator
```python
from realtime.enhanced_status import EnhancedStatusCalculator

calculator = EnhancedStatusCalculator()
calculator.add_train_to_monitoring("12512")
status = calculator.get_train_status("12512")
```

### NotificationManager
```python
from realtime.notifications import NotificationManager

manager = NotificationManager()
manager.add_notification_callback(my_callback)
manager.create_notification("Train Delayed", "Train 12512 is 30 minutes late")
```

### BackgroundWorker
```python
from realtime.worker import BackgroundWorker, MonitoringTask

worker = BackgroundWorker("MyWorker")
task = MonitoringTask(
    task_id="check_status",
    name="Status Check",
    interval_seconds=30,
    callback=my_check_function
)
worker.add_task(task)
worker.start()
```

### CloudIntegrationManager
```python
from realtime.cloud import CloudIntegrationManager, CloudProvider, CloudConfig

manager = CloudIntegrationManager()
config = CloudConfig(
    provider=CloudProvider.FIREBASE,
    credentials_path="credentials.json",
    database_url="https://project.firebaseio.com/"
)
manager.add_service(CloudProvider.FIREBASE, config)
manager.connect(CloudProvider.FIREBASE)
```

## Configuration

### UI Configuration
```python
from realtime.ui_integration import UIConfig, UIUpdateMode

config = UIConfig(
    update_mode=UIUpdateMode.HYBRID,  # polling, websocket, or hybrid
    poll_interval=30,                 # seconds between updates
    enable_notifications=True,        # enable notification system
    enable_cloud_sync=True,          # sync with cloud services
    max_display_items=50,            # max items in UI
    auto_refresh=True                # automatic UI refresh
)
```

### Environment Variables
```bash
# Firebase
FIREBASE_CREDENTIALS_PATH=/path/to/credentials.json
FIREBASE_DATABASE_URL=https://project.firebaseio.com/

# AWS
AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your-key
AWS_SECRET_ACCESS_KEY=your-secret

# Azure
AZURE_IOT_CONNECTION_STRING=your-connection-string

# Railway API (existing)
RAILWAY_API_KEY=your-api-key
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check firewall settings
   - Ensure port 8765 is available
   - Verify network connectivity

2. **Cloud Service Not Available**
   - Check credentials and configuration
   - Verify API keys and permissions
   - Check service quotas and limits

3. **High CPU Usage**
   - Reduce polling interval
   - Decrease number of monitored trains
   - Check for infinite loops in callbacks

4. **Memory Issues**
   - Clear old notifications periodically
   - Limit number of cached status entries
   - Monitor background thread count

### Debugging

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check service status:
```python
status = realtime_ui.get_realtime_status()
print(status)
```

## Performance Considerations

- **Polling Interval**: Balance between real-time updates and API rate limits
- **Monitored Trains**: Limit concurrent monitoring to prevent API overload
- **Cache Management**: Implement TTL for cached data
- **Background Threads**: Monitor thread count and resource usage
- **Cloud Sync**: Use batch updates for multiple status changes

## Security

- Store credentials securely (environment variables, not code)
- Use HTTPS for cloud communications
- Implement rate limiting for API calls
- Validate input data from external sources
- Monitor for unusual activity patterns

## Contributing

1. Follow existing code patterns
2. Add comprehensive error handling
3. Include docstrings and type hints
4. Test with existing functionality
5. Update documentation

## License

This add-on package follows the same license as the main Indian Train Detection System.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review existing GitHub issues
3. Create a new issue with detailed information
4. Include logs and configuration (without sensitive data)</content>
<parameter name="filePath">e:\Indian Train\REALTIME_README.md