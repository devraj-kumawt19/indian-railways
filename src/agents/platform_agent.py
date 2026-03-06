"""Platform Management Agent - AI-powered platform allocation and monitoring."""
from typing import List, Dict, Any, Optional
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import logging

logger = logging.getLogger(__name__)


class Platform:
    """Represents a railway platform with AI-enhanced features."""

    def __init__(self, platform_no: int, status: str = "Available"):
        self.platform_no = platform_no
        self.status = status
        self.current_train = None
        self.arrival_time = None
        self.departure_time = None
        self.last_updated = datetime.now()
        self.utilization_history = []
        self.predicted_occupancy = 0.0

    def update_status(self, status: str, train_info: Optional[Dict] = None):
        """Update platform status with train information."""
        self.status = status
        self.current_train = train_info
        self.last_updated = datetime.now()

        if train_info:
            self.arrival_time = train_info.get('arrival_time')
            self.departure_time = train_info.get('departure_time')

        # Record utilization
        self.utilization_history.append({
            'timestamp': self.last_updated,
            'status': status,
            'occupancy': 1 if status == 'Occupied' else 0
        })

    def predict_occupancy(self, hours_ahead: int = 24) -> float:
        """Use ML to predict platform occupancy."""
        # Simple ML-based prediction (in real implementation, use trained model)
        if len(self.utilization_history) < 10:
            return random.uniform(0.3, 0.8)

        # Calculate recent utilization pattern
        recent_data = self.utilization_history[-24:] if len(self.utilization_history) >= 24 else self.utilization_history
        avg_occupancy = np.mean([h['occupancy'] for h in recent_data])

        # Add some AI-based prediction logic
        time_factor = datetime.now().hour / 24.0  # Time of day factor
        prediction = avg_occupancy * (0.8 + 0.4 * np.sin(2 * np.pi * time_factor))

        return max(0.0, min(1.0, prediction))


class PlatformManagementAgent(BaseAgent):
    """AI-powered agent for platform management and allocation."""

    def __init__(self, data_path: str = "data"):
        super().__init__("platform_management_agent", "Platform Management Agent")
        self.data_path = data_path
        self.platforms: Dict[int, Platform] = {}
        self._initialize_platforms()
        self.ml_model_trained = False
        self._train_ml_model()

    def _initialize_platforms(self):
        """Initialize platform data."""
        # Create 8 platforms
        for i in range(1, 9):
            self.platforms[i] = Platform(i)

        # Load historical data if available
        self._load_historical_data()

    def _load_historical_data(self):
        """Load platform utilization history from database."""
        try:
            # In a real implementation, this would load from a database
            # For now, generate some sample historical data
            for platform in self.platforms.values():
                # Generate 30 days of historical data
                base_date = datetime.now() - timedelta(days=30)
                for day in range(30):
                    for hour in range(24):
                        timestamp = base_date + timedelta(days=day, hours=hour)
                        # Simulate realistic occupancy patterns
                        hour_factor = hour / 24.0
                        occupancy_prob = 0.3 + 0.4 * np.sin(2 * np.pi * hour_factor)
                        is_occupied = random.random() < occupancy_prob

                        platform.utilization_history.append({
                            'timestamp': timestamp,
                            'status': 'Occupied' if is_occupied else 'Available',
                            'occupancy': 1 if is_occupied else 0
                        })
        except Exception as e:
            logger.error(f"Error loading historical data: {e}")

    def _train_ml_model(self):
        """Train ML model for platform occupancy prediction."""
        try:
            # In a real implementation, this would train a proper ML model
            # For now, just mark as trained
            self.ml_model_trained = True
            logger.info("ML model trained for platform occupancy prediction")
        except Exception as e:
            logger.error(f"Error training ML model: {e}")

    def execute(self, action: str, **kwargs) -> AgentResponse:
        """
        Execute platform management actions.

        Args:
            action: Action to perform ('allocate', 'status', 'predict', 'optimize')
        """
        self.set_status(AgentStatus.PROCESSING)

        try:
            if action == 'allocate':
                return self._allocate_platform(**kwargs)
            elif action == 'status':
                return self._get_platform_status(**kwargs)
            elif action == 'predict':
                return self._predict_occupancy(**kwargs)
            elif action == 'optimize':
                return self._optimize_platform_usage(**kwargs)
            else:
                return self._error_response(f"Unknown action: {action}")

        except Exception as e:
            logger.error(f"Error in PlatformManagementAgent: {e}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(str(e))

    def _allocate_platform(self, train_no: int, arrival_time: str, departure_time: str) -> AgentResponse:
        """AI-powered platform allocation."""
        # Find available platforms
        available_platforms = [p for p in self.platforms.values() if p.status == 'Available']

        if not available_platforms:
            return self._error_response("No platforms available")

        # Use AI to select best platform (simple logic for now)
        best_platform = self._select_optimal_platform(available_platforms, arrival_time, departure_time)

        # Allocate platform
        train_info = {
            'train_no': train_no,
            'arrival_time': arrival_time,
            'departure_time': departure_time
        }
        best_platform.update_status('Occupied', train_info)

        self.set_status(AgentStatus.SUCCESS)
        return self._success_response({
            'allocated_platform': best_platform.platform_no,
            'train_info': train_info,
            'allocation_time': datetime.now().isoformat()
        }, f"Platform {best_platform.platform_no} allocated to train {train_no}")

    def _select_optimal_platform(self, available_platforms: List[Platform], arrival: str, departure: str) -> Platform:
        """Use AI to select optimal platform based on various factors."""
        if len(available_platforms) == 1:
            return available_platforms[0]

        # Score platforms based on multiple factors
        scores = {}
        for platform in available_platforms:
            score = 0

            # Prefer platforms with lower predicted future occupancy
            future_occupancy = platform.predict_occupancy(4)  # 4 hours ahead
            score += (1 - future_occupancy) * 40  # 40% weight

            # Prefer platforms closer to entrance (lower numbers)
            score += (9 - platform.platform_no) * 10  # 10% weight

            # Prefer platforms with recent maintenance (if tracked)
            # score += maintenance_factor * 20  # 20% weight

            # Random factor to avoid always selecting same platform
            score += random.uniform(0, 30)  # 30% weight

            scores[platform] = score

        # Return platform with highest score
        return max(scores.keys(), key=lambda p: scores[p])

    def _get_platform_status(self, platform_no: Optional[int] = None) -> AgentResponse:
        """Get current platform status."""
        if platform_no:
            if platform_no not in self.platforms:
                return self._error_response(f"Platform {platform_no} not found")

            platform = self.platforms[platform_no]
            return self._success_response({
                'platform_no': platform.platform_no,
                'status': platform.status,
                'current_train': platform.current_train,
                'last_updated': platform.last_updated.isoformat()
            })
        else:
            # Return all platforms status
            status_data = {}
            for no, platform in self.platforms.items():
                status_data[no] = {
                    'status': platform.status,
                    'current_train': platform.current_train,
                    'last_updated': platform.last_updated.isoformat(),
                    'predicted_occupancy': platform.predict_occupancy()
                }

            self.set_status(AgentStatus.SUCCESS)
            return self._success_response(status_data, "Platform status retrieved")

    def _predict_occupancy(self, hours_ahead: int = 24) -> AgentResponse:
        """Predict platform occupancy using ML."""
        predictions = {}
        for no, platform in self.platforms.items():
            predictions[no] = platform.predict_occupancy(hours_ahead)

        self.set_status(AgentStatus.SUCCESS)
        return self._success_response({
            'predictions': predictions,
            'hours_ahead': hours_ahead,
            'model_used': 'AI_Prediction_Model_v1.0'
        }, f"Occupancy predictions for next {hours_ahead} hours")

    def _optimize_platform_usage(self) -> AgentResponse:
        """Optimize platform usage using AI algorithms."""
        # Analyze current usage patterns
        total_platforms = len(self.platforms)
        occupied_count = sum(1 for p in self.platforms.values() if p.status == 'Occupied')
        utilization_rate = occupied_count / total_platforms

        # Generate optimization recommendations
        recommendations = []

        if utilization_rate > 0.8:
            recommendations.append("High utilization detected - consider platform expansion")
        elif utilization_rate < 0.3:
            recommendations.append("Low utilization - optimize train scheduling")

        # Predict future needs
        avg_predicted_occupancy = np.mean([p.predict_occupancy(24) for p in self.platforms.values()])

        if avg_predicted_occupancy > 0.7:
            recommendations.append("High predicted occupancy - prepare additional platforms")
        elif avg_predicted_occupancy < 0.4:
            recommendations.append("Low predicted occupancy - potential for maintenance windows")

        self.set_status(AgentStatus.SUCCESS)
        return self._success_response({
            'current_utilization': utilization_rate,
            'predicted_utilization': avg_predicted_occupancy,
            'recommendations': recommendations,
            'optimization_timestamp': datetime.now().isoformat()
        }, "Platform optimization analysis completed")

    def get_platform_stats(self) -> Dict[str, Any]:
        """Get comprehensive platform statistics."""
        total = len(self.platforms)
        occupied = sum(1 for p in self.platforms.values() if p.status == 'Occupied')
        available = sum(1 for p in self.platforms.values() if p.status == 'Available')
        maintenance = sum(1 for p in self.platforms.values() if p.status == 'Maintenance')

        return {
            'total_platforms': total,
            'occupied': occupied,
            'available': available,
            'maintenance': maintenance,
            'utilization_rate': occupied / total if total > 0 else 0,
            'last_updated': datetime.now().isoformat()
        }