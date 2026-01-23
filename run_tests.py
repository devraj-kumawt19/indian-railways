"""Simple test runner for agents (without pytest dependency)."""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

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


class TestResults:
    """Track test results."""
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def record_pass(self, test_name):
        self.passed += 1
        print(f"  ✓ {test_name}")
    
    def record_fail(self, test_name, error):
        self.failed += 1
        self.errors.append((test_name, error))
        print(f"  ✗ {test_name}")
        print(f"    Error: {error}")
    
    def summary(self):
        total = self.passed + self.failed
        print(f"\n{'='*60}")
        print(f"Test Results: {self.passed}/{total} passed")
        print(f"{'='*60}")
        if self.errors:
            for test_name, error in self.errors:
                print(f"FAILED: {test_name}")
                print(f"  {error}")


results = TestResults()


def test_base_agent():
    """Test base agent functionality."""
    print("\nTesting BaseAgent...")
    
    try:
        class TestAgent(BaseAgent):
            def execute(self, **kwargs):
                return self._success_response({"test": True})
        
        agent = TestAgent("test_id", "Test Agent")
        assert agent.agent_id == "test_id", "Agent ID mismatch"
        assert agent.name == "Test Agent", "Agent name mismatch"
        assert agent.status == AgentStatus.IDLE, "Initial status should be IDLE"
        results.record_pass("BaseAgent initialization")
    except Exception as e:
        results.record_fail("BaseAgent initialization", str(e))
    
    try:
        class TestAgent(BaseAgent):
            def execute(self, **kwargs):
                pass
        
        agent = TestAgent("test", "Test")
        response = agent._success_response(
            data={"key": "value"},
            message="Success"
        )
        
        assert response.success is True, "Response should be successful"
        assert response.status == AgentStatus.SUCCESS, "Status should be SUCCESS"
        assert response.data == {"key": "value"}, "Data mismatch"
        results.record_pass("Success response creation")
    except Exception as e:
        results.record_fail("Success response creation", str(e))


def test_coach_position_agent():
    """Test CoachPositionAgent."""
    print("\nTesting CoachPositionAgent...")
    
    try:
        agent = CoachPositionAgent()
        assert agent.agent_id == "coach_position_agent", "Agent ID mismatch"
        assert agent.status == AgentStatus.IDLE, "Initial status should be IDLE"
        results.record_pass("CoachPositionAgent initialization")
    except Exception as e:
        results.record_fail("CoachPositionAgent initialization", str(e))
    
    try:
        agent = CoachPositionAgent()
        zones = agent.platform_zone_mapping
        assert 'A' in zones, "Zone A not found"
        assert 'B' in zones, "Zone B not found"
        assert zones['A'] == (0, 35), "Zone A mapping incorrect"
        results.record_pass("Platform zone mapping")
    except Exception as e:
        results.record_fail("Platform zone mapping", str(e))
    
    try:
        agent = CoachPositionAgent()
        zones = agent._get_zones_for_distance(20, 50)
        assert 'A' in zones, "Coach should be in Zone A"
        assert 'B' in zones, "Coach should be in Zone B"
        results.record_pass("Zone calculation for coach position")
    except Exception as e:
        results.record_fail("Zone calculation for coach position", str(e))
    
    try:
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
        
        assert len(positions) == 3, f"Expected 3 coaches, got {len(positions)}"
        assert positions[0].start_distance_m == 22.0, "First coach should start at 22m"
        assert abs(positions[0].end_distance_m - (22.0 + 21.5)) < 0.01, "Coach length incorrect"
        results.record_pass("Coach position calculation (towards_back)")
    except Exception as e:
        results.record_fail("Coach position calculation (towards_back)", str(e))


def test_coach_formation_agent():
    """Test CoachFormationAgent."""
    print("\nTesting CoachFormationAgent...")
    
    try:
        agent = CoachFormationAgent()
        assert agent.agent_id == "coach_formation_agent", "Agent ID mismatch"
        assert agent.status == AgentStatus.IDLE, "Initial status should be IDLE"
        results.record_pass("CoachFormationAgent initialization")
    except Exception as e:
        results.record_fail("CoachFormationAgent initialization", str(e))


def test_train_info_agent():
    """Test TrainInfoAgent."""
    print("\nTesting TrainInfoAgent...")
    
    try:
        agent = TrainInfoAgent()
        assert agent.agent_id == "train_info_agent", "Agent ID mismatch"
        assert agent.status == AgentStatus.IDLE, "Initial status should be IDLE"
        results.record_pass("TrainInfoAgent initialization")
    except Exception as e:
        results.record_fail("TrainInfoAgent initialization", str(e))
    
    try:
        agent = TrainInfoAgent()
        response = agent.execute(train_no=12345, station_code="NDLS")
        assert response.success is True, "Execution should succeed"
        assert response.data.get("train_no") == 12345, "Train number mismatch"
        results.record_pass("TrainInfoAgent execution")
    except Exception as e:
        results.record_fail("TrainInfoAgent execution", str(e))


def test_coordinator_agent():
    """Test CoordinatorAgent."""
    print("\nTesting CoordinatorAgent...")
    
    try:
        coordinator = CoordinatorAgent()
        assert coordinator.agent_id == "coordinator_agent", "Agent ID mismatch"
        assert len(coordinator.sub_agents) == 4, f"Expected 4 sub-agents, got {len(coordinator.sub_agents)}"
        results.record_pass("CoordinatorAgent initialization")
    except Exception as e:
        results.record_fail("CoordinatorAgent initialization", str(e))
    
    try:
        coordinator = CoordinatorAgent()
        agent = coordinator.get_agent("train_info_agent")
        assert agent is not None, "Should find train_info_agent"
        assert agent.name == "Train Information Agent", "Agent name mismatch"
        results.record_pass("Get sub-agent by ID")
    except Exception as e:
        results.record_fail("Get sub-agent by ID", str(e))
    
    try:
        coordinator = CoordinatorAgent()
        status = coordinator.get_agent_status()
        assert 'Train Information Agent' in status, "Missing Train Information Agent"
        assert 'Coach Formation Agent' in status, "Missing Coach Formation Agent"
        assert 'Coach Position Agent' in status, "Missing Coach Position Agent"
        assert 'Status Agent' in status, "Missing Status Agent"
        results.record_pass("Get agent status")
    except Exception as e:
        results.record_fail("Get agent status", str(e))


def integration_test_coach_position():
    """Integration test with realistic coach data."""
    print("\nTesting Integration (Coach Positioning)...")
    
    try:
        agent = CoachPositionAgent()
        
        coaches = [
            {'coach_number': i+1, 'coach_type': 'S', 'capacity': 72, 'length_m': 21.5}
            for i in range(12)
        ]
        
        positions = agent._calculate_coach_positions(
            coaches=coaches,
            engine_direction="towards_back"
        )
        
        assert len(positions) == 12, f"Expected 12 coaches, got {len(positions)}"
        assert positions[0].start_distance_m == 22.0, "First coach incorrect start"
        
        # Verify coaches don't overlap
        for i in range(len(positions) - 1):
            assert positions[i].end_distance_m == positions[i+1].start_distance_m, \
                f"Gap between coach {i} and {i+1}"
        
        results.record_pass("Integration test (12-coach train)")
    except Exception as e:
        results.record_fail("Integration test (12-coach train)", str(e))


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("Indian Railways Agent Architecture - Unit Tests")
    print("="*60)
    
    test_base_agent()
    test_coach_position_agent()
    test_coach_formation_agent()
    test_train_info_agent()
    test_coordinator_agent()
    integration_test_coach_position()
    
    results.summary()
    
    return 0 if results.failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
