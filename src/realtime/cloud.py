"""
Cloud Integration Add-On
Provides cloud services integration for real-time train tracking
Supports Firebase, AWS, and Azure cloud platforms
"""

import json
import time
from datetime import datetime
from typing import Dict, List, Optional, Any, Callable
from abc import ABC, abstractmethod
import threading
import asyncio
from dataclasses import dataclass
from enum import Enum

# Optional imports with graceful degradation
try:
    import firebase_admin
    from firebase_admin import credentials, db
    FIREBASE_AVAILABLE = True
except ImportError:
    FIREBASE_AVAILABLE = False

try:
    import boto3
    from botocore.exceptions import ClientError
    AWS_AVAILABLE = True
except ImportError:
    AWS_AVAILABLE = False

try:
    from azure.iot.hub import IoTHubRegistryManager
    from azure.iot.hub.models import Twin, TwinProperties
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

class CloudProvider(Enum):
    """Supported cloud providers."""
    FIREBASE = "firebase"
    AWS = "aws"
    AZURE = "azure"
    NONE = "none"

@dataclass
class CloudConfig:
    """Cloud service configuration."""
    provider: CloudProvider
    credentials_path: Optional[str] = None
    project_id: Optional[str] = None
    region: Optional[str] = None
    endpoint: Optional[str] = None
    database_url: Optional[str] = None

class CloudService(ABC):
    """Abstract base class for cloud services."""

    @abstractmethod
    def connect(self) -> bool:
        """Connect to cloud service."""
        pass

    @abstractmethod
    def disconnect(self):
        """Disconnect from cloud service."""
        pass

    @abstractmethod
    def publish_train_status(self, train_no: str, status_data: Dict) -> bool:
        """Publish train status update."""
        pass

    @abstractmethod
    def subscribe_to_updates(self, callback: Callable) -> bool:
        """Subscribe to real-time updates."""
        pass

    @abstractmethod
    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get current train status."""
        pass

    @abstractmethod
    def publish_platform_status(self, platform_no: str, status_data: Dict) -> bool:
        """Publish platform status update."""
        pass

    @abstractmethod
    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get current platform status."""
        pass

class FirebaseService(CloudService):
    """Firebase Realtime Database integration."""

    def __init__(self, config: CloudConfig):
        self.config = config
        self.app = None
        self.database_ref = None
        self.connected = False
        self.listeners: List[Callable] = []

    def connect(self) -> bool:
        """Connect to Firebase."""
        if not FIREBASE_AVAILABLE:
            print("⚠️ Firebase not available. Install with: pip install firebase-admin")
            return False

        try:
            if self.config.credentials_path:
                cred = credentials.Certificate(self.config.credentials_path)
                self.app = firebase_admin.initialize_app(cred, {
                    'databaseURL': self.config.database_url
                })
            else:
                # Use default credentials (for deployed environments)
                self.app = firebase_admin.initialize_app(options={
                    'databaseURL': self.config.database_url
                })

            self.database_ref = db.reference()
            self.connected = True
            print("🔥 Connected to Firebase Realtime Database")
            return True

        except Exception as e:
            print(f"❌ Firebase connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from Firebase."""
        if self.app:
            try:
                firebase_admin.delete_app(self.app)
                self.app = None
                self.database_ref = None
                self.connected = False
                print("🔥 Disconnected from Firebase")
            except Exception as e:
                print(f"❌ Firebase disconnect error: {e}")

    def publish_train_status(self, train_no: str, status_data: Dict) -> bool:
        """Publish train status to Firebase."""
        if not self.connected or not self.database_ref:
            return False

        try:
            # Add timestamp
            status_data['timestamp'] = datetime.now().isoformat()
            status_data['source'] = 'firebase'

            # Publish to trains/{train_no}/status
            train_ref = self.database_ref.child(f'trains/{train_no}/status')
            train_ref.set(status_data)

            # Also add to history
            history_ref = self.database_ref.child(f'trains/{train_no}/history')
            history_ref.push(status_data)

            return True

        except Exception as e:
            print(f"❌ Firebase publish train status failed: {e}")
            return False

    def subscribe_to_updates(self, callback: Callable) -> bool:
        """Subscribe to Firebase real-time updates."""
        if not self.connected or not self.database_ref:
            return False

        try:
            def firebase_listener(event):
                try:
                    data = event.data
                    if data:
                        callback({
                            'type': 'firebase_update',
                            'path': event.path,
                            'data': data,
                            'timestamp': datetime.now()
                        })
                except Exception as e:
                    print(f"❌ Firebase listener error: {e}")

            # Listen to all train updates
            trains_ref = self.database_ref.child('trains')
            trains_ref.listen(firebase_listener)

            self.listeners.append(callback)
            return True

        except Exception as e:
            print(f"❌ Firebase subscribe failed: {e}")
            return False

    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get train status from Firebase."""
        if not self.connected or not self.database_ref:
            return None

        try:
            train_ref = self.database_ref.child(f'trains/{train_no}/status')
            snapshot = train_ref.get()

            if snapshot:
                return dict(snapshot)
            return None

        except Exception as e:
            print(f"❌ Firebase get train status failed: {e}")
            return None

    def publish_platform_status(self, platform_no: str, status_data: Dict) -> bool:
        """Publish platform status to Firebase."""
        if not self.connected or not self.database_ref:
            return False

        try:
            status_data['timestamp'] = datetime.now().isoformat()
            status_data['source'] = 'firebase'

            platform_ref = self.database_ref.child(f'platforms/{platform_no}/status')
            platform_ref.set(status_data)

            return True

        except Exception as e:
            print(f"❌ Firebase publish platform status failed: {e}")
            return False

    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get platform status from Firebase."""
        if not self.connected or not self.database_ref:
            return None

        try:
            platform_ref = self.database_ref.child(f'platforms/{platform_no}/status')
            snapshot = platform_ref.get()

            if snapshot:
                return dict(snapshot)
            return None

        except Exception as e:
            print(f"❌ Firebase get platform status failed: {e}")
            return None

class AWSService(CloudService):
    """AWS IoT integration."""

    def __init__(self, config: CloudConfig):
        self.config = config
        self.iot_client = None
        self.connected = False
        self.listeners: List[Callable] = []

    def connect(self) -> bool:
        """Connect to AWS IoT."""
        if not AWS_AVAILABLE:
            print("⚠️ AWS not available. Install with: pip install boto3")
            return False

        try:
            self.iot_client = boto3.client(
                'iot-data',
                region_name=self.config.region,
                aws_access_key_id=None,  # Use IAM roles or environment variables
                aws_secret_access_key=None
            )
            self.connected = True
            print("☁️ Connected to AWS IoT")
            return True

        except Exception as e:
            print(f"❌ AWS connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from AWS."""
        self.iot_client = None
        self.connected = False
        print("☁️ Disconnected from AWS IoT")

    def publish_train_status(self, train_no: str, status_data: Dict) -> bool:
        """Publish train status to AWS IoT."""
        if not self.connected or not self.iot_client:
            return False

        try:
            payload = json.dumps({
                'train_no': train_no,
                'status': status_data,
                'timestamp': datetime.now().isoformat(),
                'source': 'aws'
            })

            self.iot_client.publish(
                topic=f'trains/{train_no}/status',
                qos=1,
                payload=payload
            )

            return True

        except Exception as e:
            print(f"❌ AWS publish train status failed: {e}")
            return False

    def subscribe_to_updates(self, callback: Callable) -> bool:
        """Subscribe to AWS IoT updates."""
        # AWS IoT subscription requires MQTT client setup
        # This is a simplified version - full implementation would need MQTT
        print("⚠️ AWS IoT subscription requires MQTT client setup")
        return False

    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get train status from AWS (not directly supported)."""
        print("⚠️ AWS IoT doesn't support direct status retrieval")
        return None

    def publish_platform_status(self, platform_no: str, status_data: Dict) -> bool:
        """Publish platform status to AWS IoT."""
        if not self.connected or not self.iot_client:
            return False

        try:
            payload = json.dumps({
                'platform_no': platform_no,
                'status': status_data,
                'timestamp': datetime.now().isoformat(),
                'source': 'aws'
            })

            self.iot_client.publish(
                topic=f'platforms/{platform_no}/status',
                qos=1,
                payload=payload
            )

            return True

        except Exception as e:
            print(f"❌ AWS publish platform status failed: {e}")
            return False

    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get platform status from AWS (not directly supported)."""
        print("⚠️ AWS IoT doesn't support direct status retrieval")
        return None

class AzureService(CloudService):
    """Azure IoT Hub integration."""

    def __init__(self, config: CloudConfig):
        self.config = config
        self.registry_manager = None
        self.connected = False
        self.listeners: List[Callable] = []

    def connect(self) -> bool:
        """Connect to Azure IoT Hub."""
        if not AZURE_AVAILABLE:
            print("⚠️ Azure not available. Install with: pip install azure-iot-hub")
            return False

        try:
            connection_string = self.config.endpoint  # Should be IoT Hub connection string
            self.registry_manager = IoTHubRegistryManager(connection_string)
            self.connected = True
            print("☁️ Connected to Azure IoT Hub")
            return True

        except Exception as e:
            print(f"❌ Azure connection failed: {e}")
            return False

    def disconnect(self):
        """Disconnect from Azure."""
        self.registry_manager = None
        self.connected = False
        print("☁️ Disconnected from Azure IoT Hub")

    def publish_train_status(self, train_no: str, status_data: Dict) -> bool:
        """Publish train status to Azure IoT Hub."""
        if not self.connected or not self.registry_manager:
            return False

        try:
            # Update device twin with train status
            device_id = f"train-{train_no}"
            twin = Twin()
            twin.properties = TwinProperties(desired={
                'status': status_data,
                'timestamp': datetime.now().isoformat(),
                'source': 'azure'
            })

            self.registry_manager.update_twin(device_id, twin)
            return True

        except Exception as e:
            print(f"❌ Azure publish train status failed: {e}")
            return False

    def subscribe_to_updates(self, callback: Callable) -> bool:
        """Subscribe to Azure IoT Hub updates."""
        print("⚠️ Azure IoT Hub subscription requires event processing setup")
        return False

    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get train status from Azure IoT Hub."""
        if not self.connected or not self.registry_manager:
            return None

        try:
            device_id = f"train-{train_no}"
            twin = self.registry_manager.get_twin(device_id)

            if twin.properties.reported:
                return dict(twin.properties.reported)
            return None

        except Exception as e:
            print(f"❌ Azure get train status failed: {e}")
            return None

    def publish_platform_status(self, platform_no: str, status_data: Dict) -> bool:
        """Publish platform status to Azure IoT Hub."""
        if not self.connected or not self.registry_manager:
            return False

        try:
            device_id = f"platform-{platform_no}"
            twin = Twin()
            twin.properties = TwinProperties(desired={
                'status': status_data,
                'timestamp': datetime.now().isoformat(),
                'source': 'azure'
            })

            self.registry_manager.update_twin(device_id, twin)
            return True

        except Exception as e:
            print(f"❌ Azure publish platform status failed: {e}")
            return False

    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get platform status from Azure IoT Hub."""
        if not self.connected or not self.registry_manager:
            return None

        try:
            device_id = f"platform-{platform_no}"
            twin = self.registry_manager.get_twin(device_id)

            if twin.properties.reported:
                return dict(twin.properties.reported)
            return None

        except Exception as e:
            print(f"❌ Azure get platform status failed: {e}")
            return None

class CloudIntegrationManager:
    """
    Manages cloud service integration for real-time train tracking.
    Provides unified interface for multiple cloud providers.
    """

    def __init__(self):
        self.services: Dict[CloudProvider, CloudService] = {}
        self.active_provider: Optional[CloudProvider] = None
        self.update_callbacks: List[Callable] = []
        self.connected = False

    def add_service(self, provider: CloudProvider, config: CloudConfig):
        """Add a cloud service configuration."""
        if provider == CloudProvider.FIREBASE:
            service = FirebaseService(config)
        elif provider == CloudProvider.AWS:
            service = AWSService(config)
        elif provider == CloudProvider.AZURE:
            service = AzureService(config)
        else:
            print(f"❌ Unsupported cloud provider: {provider}")
            return

        self.services[provider] = service
        print(f"✅ Added {provider.value} cloud service")

    def connect(self, provider: CloudProvider) -> bool:
        """Connect to specified cloud provider."""
        if provider not in self.services:
            print(f"❌ Cloud service {provider.value} not configured")
            return False

        service = self.services[provider]

        if service.connect():
            self.active_provider = provider
            self.connected = True

            # Subscribe to updates if supported
            def update_callback(data):
                for callback in self.update_callbacks:
                    try:
                        callback(data)
                    except Exception as e:
                        print(f"❌ Cloud update callback error: {e}")

            if service.subscribe_to_updates(update_callback):
                print(f"📡 Subscribed to {provider.value} updates")

            return True

        return False

    def disconnect(self):
        """Disconnect from active cloud service."""
        if self.active_provider and self.active_provider in self.services:
            self.services[self.active_provider].disconnect()
            self.active_provider = None
            self.connected = False
            print("🔌 Disconnected from cloud service")

    def publish_train_status(self, train_no: str, status_data: Dict) -> bool:
        """Publish train status to cloud."""
        if not self.connected or not self.active_provider:
            return False

        service = self.services[self.active_provider]
        return service.publish_train_status(train_no, status_data)

    def get_train_status(self, train_no: str) -> Optional[Dict]:
        """Get train status from cloud."""
        if not self.connected or not self.active_provider:
            return None

        service = self.services[self.active_provider]
        return service.get_train_status(train_no)

    def publish_platform_status(self, platform_no: str, status_data: Dict) -> bool:
        """Publish platform status to cloud."""
        if not self.connected or not self.active_provider:
            return False

        service = self.services[self.active_provider]
        return service.publish_platform_status(platform_no, status_data)

    def get_platform_status(self, platform_no: str) -> Optional[Dict]:
        """Get platform status from cloud."""
        if not self.connected or not self.active_provider:
            return None

        service = self.services[self.active_provider]
        return service.get_platform_status(platform_no)

    def add_update_callback(self, callback: Callable):
        """Add callback for cloud updates."""
        self.update_callbacks.append(callback)

    def get_available_providers(self) -> List[CloudProvider]:
        """Get list of configured cloud providers."""
        return list(self.services.keys())

    def get_status(self) -> Dict:
        """Get cloud integration status."""
        return {
            'connected': self.connected,
            'active_provider': self.active_provider.value if self.active_provider else None,
            'available_providers': [p.value for p in self.get_available_providers()],
            'firebase_available': FIREBASE_AVAILABLE,
            'aws_available': AWS_AVAILABLE,
            'azure_available': AZURE_AVAILABLE
        }


# Integration helper functions
def create_firebase_config(credentials_path: str, database_url: str) -> CloudConfig:
    """Create Firebase configuration."""
    return CloudConfig(
        provider=CloudProvider.FIREBASE,
        credentials_path=credentials_path,
        database_url=database_url
    )

def create_aws_config(region: str) -> CloudConfig:
    """Create AWS configuration."""
    return CloudConfig(
        provider=CloudProvider.AWS,
        region=region
    )

def create_azure_config(connection_string: str) -> CloudConfig:
    """Create Azure configuration."""
    return CloudConfig(
        provider=CloudProvider.AZURE,
        endpoint=connection_string
    )

def integrate_cloud_services(app_instance, cloud_configs: List[CloudConfig] = None):
    """
    Integrate cloud services into existing app.

    Args:
        app_instance: Existing TrainDetectionApp instance
        cloud_configs: List of cloud service configurations
    """
    cloud_manager = CloudIntegrationManager()

    # Add default configurations if none provided
    if not cloud_configs:
        # Try to load from environment or config files
        cloud_configs = []

        # Add Firebase if credentials available
        try:
            import os
            firebase_creds = os.getenv('FIREBASE_CREDENTIALS_PATH')
            firebase_url = os.getenv('FIREBASE_DATABASE_URL')
            if firebase_creds and firebase_url:
                firebase_config = create_firebase_config(firebase_creds, firebase_url)
                cloud_configs.append(firebase_config)
        except:
            pass

    # Add configurations
    for config in cloud_configs:
        cloud_manager.add_service(config.provider, config)

    # Try to connect to first available service
    available_providers = cloud_manager.get_available_providers()
    if available_providers:
        for provider in available_providers:
            if cloud_manager.connect(provider):
                break

    # Add to app instance
    app_instance.cloud_manager = cloud_manager

    # Add callback for cloud updates
    def cloud_update_callback(data):
        print(f"☁️ Cloud update received: {data.get('type', 'unknown')}")

        # Forward to app's real-time service if available
        if hasattr(app_instance, 'realtime_service'):
            app_instance.realtime_service.handle_cloud_update(data)

    cloud_manager.add_update_callback(cloud_update_callback)

    return cloud_manager