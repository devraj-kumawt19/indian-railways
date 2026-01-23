"""Coordinator Agent - orchestrates all sub-agents."""
from typing import Dict, Any, Optional
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
from src.agents.train_info_agent import TrainInfoAgent
from src.agents.coach_formation_agent import CoachFormationAgent
from src.agents.coach_position_agent import CoachPositionAgent
from src.agents.status_agent import StatusAgent
import logging

logger = logging.getLogger(__name__)


class CoordinatorAgent(BaseAgent):
    """
    Master coordinator agent that orchestrates all sub-agents.
    
    Architecture:
    CoordinatorAgent
     ├─ TrainInfoAgent       (retrieves train information)
     ├─ CoachFormationAgent  (loads coach composition)
     ├─ CoachPositionAgent   (calculates coach positions)
     └─ StatusAgent          (aggregates all information)
    
    Usage:
    coordinator = CoordinatorAgent()
    response = coordinator.execute(train_no=12345, station_code='BPL', platform_no=5)
    """
    
    def __init__(self):
        super().__init__("coordinator_agent", "Coordinator Agent")
        # Initialize sub-agents
        self.train_info_agent = TrainInfoAgent()
        self.formation_agent = CoachFormationAgent()
        self.position_agent = CoachPositionAgent()
        self.status_agent = StatusAgent()
        
        self.sub_agents = [
            self.train_info_agent,
            self.formation_agent,
            self.position_agent,
            self.status_agent
        ]
    
    def execute(
        self,
        train_no: int,
        station_code: str,
        platform_no: int,
        platform_length_m: Optional[float] = None,
        engine_direction: Optional[str] = None,
        **kwargs
    ) -> AgentResponse:
        """
        Execute complete agent workflow.
        
        Args:
            train_no: Train number
            station_code: Station code
            platform_no: Platform number
            platform_length_m: Optional platform length
            engine_direction: Optional engine direction
            
        Returns:
            AgentResponse with complete train and platform information
        """
        self.set_status(AgentStatus.PROCESSING)
        
        try:
            logger.info(f"CoordinatorAgent processing train {train_no} at {station_code}")
            
            # Execute status agent which coordinates other agents
            status_response = self.status_agent.execute(
                train_no=train_no,
                station_code=station_code,
                platform_no=platform_no
            )
            
            if not status_response.success:
                return self._error_response(
                    error="Agent execution failed",
                    message=status_response.error
                )
            
            # Add metadata
            result_data = status_response.data
            result_data["metadata"] = {
                "coordinator_status": "success",
                "sub_agents_executed": len(self.sub_agents),
                "agents": [agent.name for agent in self.sub_agents],
                "request": {
                    "train_no": train_no,
                    "station_code": station_code,
                    "platform_no": platform_no
                }
            }
            
            self.set_status(AgentStatus.SUCCESS)
            return self._success_response(
                data=result_data,
                message=f"Successfully processed train {train_no} with all agents"
            )
            
        except Exception as e:
            logger.error(f"Error in CoordinatorAgent: {str(e)}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(
                error=str(e),
                message="Coordinator agent execution failed"
            )
    
    def get_agent_status(self) -> Dict[str, str]:
        """Get status of all sub-agents."""
        return {
            agent.name: agent.get_status().value
            for agent in self.sub_agents
        }
    
    def get_agent(self, agent_id: str) -> Optional[BaseAgent]:
        """Get specific agent by ID."""
        for agent in self.sub_agents:
            if agent.agent_id == agent_id:
                return agent
        return None
