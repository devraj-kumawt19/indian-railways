"""Unit tests for all agents."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest
from src.agents import (
    BaseAgent,
    AgentResponse,
    AgentStatus,
    TrainInfoAgent,
    CoachFormationAgent,
    CoachPositionAgent,
    StatusAgent,
    CoordinatorAgent
)


class TestBaseAgent:
    """Test base agent functionality."""
    
    def test_agent_initialization(self):
        """Test agent can be created."""
        class TestAgent(BaseAgent):
            def execute(self, **kwargs):
                return self._success_response({"test": True})
        
        agent = TestAgent("test_id", "Test Agent")
        assert agent.agent_id == "test_id"
        assert agent.name == "Test Agent"
        assert agent.status == AgentStatus.IDLE
    
    def test_success_response(self):
        """Test success response creation."""
        class TestAgent(BaseAgent):
            def execute(self, **kwargs):
                pass
        
        agent = TestAgent("test", "Test")
        response = agent._success_response(
            data={"key": "value"},
            message="Success"
        )
        
        assert response.success is True
        assert response.status == AgentStatus.SUCCESS
        assert response.data == {"key": "value"}
        assert response.message == "Success"
    
    def test_error_response(self):
        """Test error response creation."""
        class TestAgent(BaseAgent):
            def execute(self, **kwargs):
                pass
        
        agent = TestAgent("test", "Test")
        response = agent._error_response(
            error="Test error",
            message="Failed"
        )
        
        assert response.success is False
        assert response.status == AgentStatus.ERROR
        assert response.error == "Test error"


class TestCoachPositionAgent:
    """Test coach position agent."""
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = CoachPositionAgent()
        assert agent.agent_id == "coach_position_agent"
        assert agent.status == AgentStatus.IDLE
    
    def test_zone_mapping(self):
        """Test platform zone mapping."""
        agent = CoachPositionAgent()
        zones = agent.platform_zone_mapping
        
        assert 'A' in zones
        assert 'B' in zones
        assert zones['A'] == (0, 35)
        assert zones['B'] == (35, 70)
    
    def test_get_zones_for_distance(self):
        """Test zone calculation for coach position."""
        agent = CoachPositionAgent()
        
        # Coach spanning zones A and B
        zones = agent._get_zones_for_distance(20, 50)
        assert 'A' in zones
        assert 'B' in zones
        
        # Coach in single zone
        zones = agent._get_zones_for_distance(10, 30)
        assert 'A' in zones
        assert 'B' not in zones
    
    def test_calculate_coach_positions_towards_back(self):
        """Test coach position calculation - towards back."""
        agent = CoachPositionAgent()
        
        coaches = [
            {'coach_number': 1, 'coach_type': 'A'},
            {'coach_number': 2, 'coach_type': 'B'},
            {'coach_number': 3, 'coach_type': 'S'}
        ]
        
        positions = agent._calculate_coach_positions(
            coaches=coaches,
            engine_direction="towards_back"
        )
        
        assert len(positions) == 3
        # First coach starts after engine (22m)
        assert positions[0].start_distance_m == 22.0
        # Each coach is 21.5m long
        assert positions[0].end_distance_m == 22.0 + 21.5
        assert positions[1].start_distance_m == 22.0 + 21.5


class TestCoachFormationAgent:
    """Test coach formation agent."""
    
    def test_agent_initialization(self):
        """Test agent initialization."""
        agent = CoachFormationAgent()
        assert agent.agent_id == "coach_formation_agent"
        assert agent.status == AgentStatus.IDLE
    
    def test_formation_to_dict(self):
        """Test formation conversion to dict."""
        from src.agents.coach_formation_agent import CoachFormation
        
        agent = CoachFormationAgent()
        coaches = [
            {'coach_number': 1, 'coach_type': 'A'},
            {'coach_number': 2, 'coach_type': 'B'}
        ]
        
        formation = CoachFormation(train_no=12345, coaches=coaches)
        formation_dict = agent._formation_to_dict(formation)
        
        assert formation_dict['train_no'] == 12345
        assert formation_dict['total_coaches'] == 2
        assert len(formation_dict['coaches']) == 2


class TestCoordinatorAgent:
    """Test coordinator agent."""
    
    def test_agent_initialization(self):
        """Test coordinator initialization."""
        coordinator = CoordinatorAgent()
        assert coordinator.agent_id == "coordinator_agent"
        assert len(coordinator.sub_agents) == 4
    
    def test_get_agent(self):
        """Test getting sub-agents."""
        coordinator = CoordinatorAgent()
        
        agent = coordinator.get_agent("train_info_agent")
        assert agent is not None
        assert agent.name == "Train Information Agent"
    
    def test_get_agent_status(self):
        """Test getting agent status."""
        coordinator = CoordinatorAgent()
        status = coordinator.get_agent_status()
        
        assert 'Train Information Agent' in status
        assert 'Coach Formation Agent' in status
        assert 'Coach Position Agent' in status
        assert 'Status Agent' in status


# Integration test
def test_coach_position_agent_with_real_coaches():
    """Integration test with realistic coach data."""
    agent = CoachPositionAgent()
    
    # Simulate real coach composition
    coaches = [
        {'coach_number': i+1, 'coach_type': 'S', 'capacity': 72, 'length_m': 21.5}
        for i in range(12)  # 12-coach train
    ]
    
    positions = agent._calculate_coach_positions(
        coaches=coaches,
        engine_direction="towards_back"
    )
    
    # Verify positions
    assert len(positions) == 12
    assert positions[0].start_distance_m == 22.0
    assert positions[-1].end_distance_m == 22.0 + (12 * 21.5)
    
    # Verify coaches don't overlap
    for i in range(len(positions) - 1):
        assert positions[i].end_distance_m == positions[i+1].start_distance_m


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
