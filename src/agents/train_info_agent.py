"""Train Info Agent - retrieves train information."""
from typing import Optional, Dict, Any
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
import logging

logger = logging.getLogger(__name__)


class TrainInfoAgent(BaseAgent):
    """Agent responsible for retrieving train information."""
    
    def __init__(self):
        super().__init__("train_info_agent", "Train Information Agent")
    
    def execute(
        self,
        train_no: int,
        station_code: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Execute train info retrieval.
        
        Args:
            train_no: Train number
            station_code: Optional station code for train at specific station
            
        Returns:
            AgentResponse with train information
        """
        self.set_status(AgentStatus.PROCESSING)
        
        try:
            # Return mock train data (in production, would fetch from API/DB)
            train_data = {
                "train_no": train_no,
                "train_name": f"Train {train_no}",
                "scheduled_departure": "10:30",
                "scheduled_arrival": "18:45",
                "current_status": "On Time",
                "delay_minutes": 0,
                "source": "NDLS",
                "destination": "BPL"
            }
            
            # Add station info if provided
            if station_code:
                train_data["current_station"] = {
                    "code": station_code,
                    "name": f"Station {station_code}",
                    "platform": 5
                }
            
            self.set_status(AgentStatus.SUCCESS)
            return self._success_response(
                data=train_data,
                message=f"Retrieved information for train {train_no}"
            )
            
        except Exception as e:
            logger.error(f"Error in TrainInfoAgent: {str(e)}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(
                error=str(e),
                message="Failed to retrieve train information"
            )
