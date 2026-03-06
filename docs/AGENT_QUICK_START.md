# Agent Architecture - Quick Start Guide

## 🚀 Quick Start

### Run the Agent Demo
```bash
python demo_agents.py
```

This demonstrates:
- Coach position calculation
- Platform zone mapping
- Agent initialization
- Coordinator orchestration

### Run Tests
```bash
python run_tests.py
```

Results: **13/13 tests passing**

### Launch Streamlit App
```bash
streamlit run src/ui/agents_app.py
```

## 📁 Project Structure

```
src/agents/
├── __init__.py                 # Package initialization
├── base_agent.py              # Base class for all agents
├── train_info_agent.py         # Train information retrieval
├── coach_formation_agent.py    # Coach composition loading
├── coach_position_agent.py     # Coach position calculation ⭐
├── status_agent.py             # Information aggregation
└── coordinator_agent.py        # Master orchestrator

src/ui/
└── agents_app.py              # Streamlit interface

tests/
└── test_agents.py             # Unit tests

Root:
├── demo_agents.py             # Agent demonstration
├── run_tests.py               # Test runner
└── AGENT_ARCHITECTURE.md      # Detailed documentation
```

## 🎯 Agent Roles at a Glance

| Agent | Role | Input | Output |
|-------|------|-------|--------|
| **TrainInfoAgent** | Retrieve train data | `train_no` | Train schedule, status, delays |
| **CoachFormationAgent** | Load coach composition | `train_no` | Coach list, types, capacities |
| **CoachPositionAgent** | Calculate positions | `train_no, station, platform` | Coach positions & zones |
| **StatusAgent** | Aggregate all data | `train_no, station, platform` | Complete information |
| **CoordinatorAgent** | Orchestrate all agents | `train_no, station, platform` | Unified response |

## 🔧 Key Implementation: CoachPositionAgent

### Input
```python
train_no=12345              # Train number
station_code="NDLS"         # Station code
platform_no=5               # Platform number
platform_length_m=300       # Platform length (optional)
engine_direction="towards_back"  # Engine facing direction
```

### Process
```
1. Load coach formation (12 coaches, each 21.5m)
2. Engine positioned at 0m (length 22m)
3. Calculate each coach:
   Coach 1: 22.0m - 43.5m
   Coach 2: 43.5m - 65.0m
   ...
4. Map to zones:
   Zone A: 0-35m
   Zone B: 35-70m
   Zone C: 70-105m
   ... etc
5. Assign zones to each coach
```

### Output
```python
{
    "train_no": 12345,
    "station_code": "NDLS",
    "platform_no": 5,
    "total_coaches": 12,
    "coach_positions": [
        {
            "coach_number": 1,
            "coach_type": "A",
            "start_distance_m": 22.0,
            "end_distance_m": 43.5,
            "zones": ["A", "B"]
        },
        ...
    ]
}
```

## 💡 Usage Examples

### Example 1: Find Coach Position
```python
from src.agents import CoachPositionAgent

agent = CoachPositionAgent()
response = agent.execute(
    train_no=12345,
    station_code="NDLS",
    platform_no=5,
    engine_direction="towards_back"
)

if response.success:
    for coach in response.data["coach_positions"]:
        print(f"Coach {coach['coach_number']}: Zones {coach['zones']}")
    # Output:
    # Coach 1: Zones ['A', 'B']
    # Coach 2: Zones ['B']
    # ... etc
```

### Example 2: Use Coordinator Agent
```python
from src.agents import CoordinatorAgent

coordinator = CoordinatorAgent()
response = coordinator.execute(
    train_no=12345,
    station_code="NDLS",
    platform_no=5
)

if response.success:
    train_info = response.data["train_info"]
    positions = response.data["coach_positions"]["coach_positions"]
    
    print(f"Train: {train_info['train_name']}")
    print(f"Status: {train_info['current_status']}")
    print(f"Coaches: {len(positions)}")
```

### Example 3: Platform Zone Mapping
```python
from src.agents import CoachPositionAgent

agent = CoachPositionAgent()

# Get zones for a coach at specific position
zones = agent._get_zones_for_distance(start_m=50, end_m=90)
print(zones)  # Output: ['B', 'C']

# Check platform zone definitions
print(agent.platform_zone_mapping)
# Output: {'A': (0, 35), 'B': (35, 70), 'C': (70, 105), ...}
```

## 📊 Platform Layout Reference

```
Standard Indian Railway Platform Layout:

0m          35m         70m        105m       140m       175m       210m        250m
|-----------|-----------|-----------|-----------|-----------|-----------|-----------|
A           B           C           D           E           F           G

Engine: WDG-4D (~22m)
Coach: ~21.5m each

Example: 12-coach train
|Engine|Coach1|Coach2|Coach3|Coach4|Coach5|Coach6|Coach7|Coach8|Coach9|C10|C11|C12|
0     22     44     65     87    108   130   151   173   194   215   237  258  280m

Zones:
A: 0-35m
B: 35-70m
C: 70-105m
D: 105-140m
E: 140-175m
F: 175-210m
G: 210-250m
```

## 🧪 Test Results

```
✓ BaseAgent initialization
✓ Success response creation
✓ CoachPositionAgent initialization
✓ Platform zone mapping
✓ Zone calculation for coach position
✓ Coach position calculation (towards_back)
✓ CoachFormationAgent initialization
✓ TrainInfoAgent initialization
✓ TrainInfoAgent execution
✓ CoordinatorAgent initialization
✓ Get sub-agent by ID
✓ Get agent status
✓ Integration test (12-coach train)

Test Results: 13/13 passed ✅
```

## 🚀 Features

- ✅ Modular agent architecture
- ✅ Standardized response format
- ✅ Comprehensive error handling
- ✅ Zone-based coach positioning
- ✅ Coach caching for performance
- ✅ Extensible design
- ✅ Full test coverage
- ✅ Streamlit UI integration
- ✅ Detailed documentation

## 📚 Related Documents

- [AGENT_ARCHITECTURE.md](AGENT_ARCHITECTURE.md) - Detailed architecture documentation
- [src/agents/](src/agents/) - Agent source code
- [tests/test_agents.py](tests/test_agents.py) - Unit tests
- [demo_agents.py](demo_agents.py) - Live demonstration
- [run_tests.py](run_tests.py) - Test runner

## 🔗 API Reference

### BaseAgent
```python
class BaseAgent:
    execute(**kwargs) -> AgentResponse
    set_status(status: AgentStatus)
    get_status() -> AgentStatus
    _success_response(data, message) -> AgentResponse
    _error_response(error, message) -> AgentResponse
```

### CoachPositionAgent
```python
class CoachPositionAgent(BaseAgent):
    execute(train_no, station_code, platform_no, 
            platform_length_m=None, engine_direction=None) -> AgentResponse
    _get_zones_for_distance(start_m, end_m) -> List[str]
    _calculate_coach_positions(coaches, engine_direction) -> List[CoachPosition]
    _decide_engine_direction(station_code, train_no) -> str
```

### AgentResponse
```python
class AgentResponse:
    success: bool
    status: AgentStatus
    data: Dict[str, Any]
    message: str
    error: Optional[str]
    timestamp: str
    
    to_dict() -> Dict
```

## 🎓 Architecture Principles

1. **Single Responsibility**: Each agent has one job
2. **Separation of Concerns**: Agents don't depend on each other
3. **Error Handling**: Consistent try-catch-respond pattern
4. **Testability**: Each agent can be tested independently
5. **Extensibility**: Easy to add new agents
6. **Logging**: All operations logged for debugging
7. **Documentation**: Code is self-documenting

## ❓ FAQ

**Q: How do I add a new agent?**
A: Inherit from BaseAgent, implement execute(), and add to CoordinatorAgent.

**Q: How do zones map to coach positions?**
A: Zones are 35m wide. A coach spanning 50-90m will be in zones B and C.

**Q: What if the train has fewer than 12 coaches?**
A: The algorithm handles any number of coaches dynamically.

**Q: Can I customize the engine direction?**
A: Yes, pass `engine_direction="towards_front"` or override `_decide_engine_direction()`.

**Q: How is caching handled?**
A: CoachFormationAgent caches by train number after first load.

## 🤝 Contributing

To extend the agent system:

1. Create new agent inheriting from BaseAgent
2. Implement execute() method
3. Add comprehensive docstrings
4. Write unit tests
5. Add to CoordinatorAgent
6. Update documentation

---

**Version**: 1.0  
**Last Updated**: January 23, 2026  
**Status**: Production Ready ✅
