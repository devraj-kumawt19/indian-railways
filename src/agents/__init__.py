"""Agent module initialization."""
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
from src.agents.train_info_agent import TrainInfoAgent
from src.agents.coach_formation_agent import CoachFormationAgent
from src.agents.coach_position_agent import CoachPositionAgent
from src.agents.status_agent import StatusAgent
from src.agents.coordinator_agent import CoordinatorAgent

__all__ = [
    'BaseAgent',
    'AgentResponse',
    'AgentStatus',
    'TrainInfoAgent',
    'CoachFormationAgent',
    'CoachPositionAgent',
    'StatusAgent',
    'CoordinatorAgent'
]
