"""Status Agent - aggregates train and platform status."""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
from src.agents.train_info_agent import TrainInfoAgent
from src.agents.coach_formation_agent import CoachFormationAgent
from src.agents.coach_position_agent import CoachPositionAgent
import logging

logger = logging.getLogger(__name__)


class StatusAgent(BaseAgent):
    """
    Agent responsible for aggregating status from other agents.
    Coordinates between TrainInfo, CoachFormation, and CoachPosition agents.
    """
    
    def __init__(self):
        super().__init__("status_agent", "Status Agent")
        self.train_info_agent = TrainInfoAgent()
        self.formation_agent = CoachFormationAgent()
        self.position_agent = CoachPositionAgent()
    
    def execute(
        self,
        train_no: int,
        station_code: str,
        platform_no: int,
        **kwargs
    ) -> AgentResponse:
        """
        Get comprehensive status by aggregating all agents.
        
        Args:
            train_no: Train number
            station_code: Station code
            platform_no: Platform number
            
        Returns:
            AgentResponse with complete status
        """
        self.set_status(AgentStatus.PROCESSING)
        
        try:
            # Get train info
            train_response = self.train_info_agent.execute(
                train_no=train_no,
                station_code=station_code
            )
            if not train_response.success:
                return self._error_response(
                    error="Failed to get train info",
                    message=train_response.error
                )
            
            # Get coach formation
            formation_response = self.formation_agent.execute(train_no=train_no)
            if not formation_response.success:
                return self._error_response(
                    error="Failed to get coach formation",
                    message=formation_response.error
                )
            
            # Get coach positions
            position_response = self.position_agent.execute(
                train_no=train_no,
                station_code=station_code,
                platform_no=platform_no
            )
            if not position_response.success:
                return self._error_response(
                    error="Failed to get coach positions",
                    message=position_response.error
                )
            
            # Aggregate all responses
            aggregated_status = {
                "train_info": train_response.data,
                "coach_formation": formation_response.data,
                "coach_positions": position_response.data,
                "summary": {
                    "total_coaches": position_response.data.get("total_coaches", 0),
                    "platform": platform_no,
                    "engine_direction": position_response.data.get("engine_direction", "unknown")
                }
            }
            
            self.set_status(AgentStatus.SUCCESS)
            return self._success_response(
                data=aggregated_status,
                message=f"Retrieved complete status for train {train_no}"
            )
            
        except Exception as e:
            logger.error(f"Error in StatusAgent: {str(e)}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(
                error=str(e),
                message="Failed to get status"
            )
