"""Base Agent class for all agents in the system."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from enum import Enum
from datetime import datetime


class AgentStatus(Enum):
    """Agent execution status."""
    IDLE = "idle"
    PROCESSING = "processing"
    SUCCESS = "success"
    ERROR = "error"
    FAILED = "failed"


class AgentResponse:
    """Standardized response from agent execution."""
    
    def __init__(
        self,
        success: bool,
        status: AgentStatus,
        data: Optional[Dict[str, Any]] = None,
        message: str = "",
        error: Optional[str] = None
    ):
        self.success = success
        self.status = status
        self.data = data or {}
        self.message = message
        self.error = error
        self.timestamp = datetime.now().isoformat()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert response to dictionary."""
        return {
            "success": self.success,
            "status": self.status.value,
            "data": self.data,
            "message": self.message,
            "error": self.error,
            "timestamp": self.timestamp
        }


class BaseAgent(ABC):
    """Base class for all agents."""
    
    def __init__(self, agent_id: str, name: str):
        self.agent_id = agent_id
        self.name = name
        self.status = AgentStatus.IDLE
        self.last_response: Optional[AgentResponse] = None
    
    @abstractmethod
    def execute(self, **kwargs) -> AgentResponse:
        """Execute agent logic. Must be implemented by subclasses."""
        pass
    
    def set_status(self, status: AgentStatus):
        """Set agent status."""
        self.status = status
    
    def get_status(self) -> AgentStatus:
        """Get current agent status."""
        return self.status
    
    def log_response(self, response: AgentResponse):
        """Log agent response."""
        self.last_response = response
    
    def _success_response(
        self,
        data: Dict[str, Any],
        message: str = ""
    ) -> AgentResponse:
        """Create a success response."""
        response = AgentResponse(
            success=True,
            status=AgentStatus.SUCCESS,
            data=data,
            message=message
        )
        self.log_response(response)
        return response
    
    def _error_response(
        self,
        error: str,
        message: str = ""
    ) -> AgentResponse:
        """Create an error response."""
        response = AgentResponse(
            success=False,
            status=AgentStatus.ERROR,
            message=message,
            error=error
        )
        self.log_response(response)
        return response
