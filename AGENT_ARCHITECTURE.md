# Agent Architecture Documentation

## Overview

The Indian Railways AI System uses an agent-based architecture to handle train information retrieval and coach positioning on platforms. This document describes the architecture, agent roles, and implementation details.

## Architecture Design

### Problem Statement
Design a scalable, modular system that can:
1. Retrieve train information from multiple sources
2. Load coach formation data for trains
3. Calculate precise coach positions on platforms
4. Aggregate information from multiple sources
5. Provide reliable fallbacks for missing data

### Solution: Agent-Based Architecture

```
┌─────────────────────────────────────────┐
│         CoordinatorAgent                │
│  (Master Orchestrator)                  │
│                                         │
│  ├─ TrainInfoAgent                     │
│  ├─ CoachFormationAgent                │
│  ├─ CoachPositionAgent                 │
│  └─ StatusAgent                        │
└─────────────────────────────────────────┘
```

## Agent Roles

### 1. BaseAgent
**Purpose**: Abstract base class for all agents

**Responsibilities**:
- Define common interface for all agents
- Manage agent state (IDLE, PROCESSING, SUCCESS, ERROR, FAILED)
- Provide standardized response format
- Handle error logging

**Key Methods**:
```python
execute(**kwargs) -> AgentResponse  # Abstract method
_success_response(data, message) -> AgentResponse
_error_response(error, message) -> AgentResponse
```

### 2. TrainInfoAgent
**Purpose**: Retrieve train information

**Responsibilities**:
- Fetch train schedule and status
- Retrieve current train location
- Get delay information
- Fetch station details

**Input**:
```python
train_no: int          # Train number
station_code: str      # Optional station code
```

**Output**:
```python
{
    "train_no": 12345,
    "train_name": "Train Name",
    "scheduled_departure": "10:30",
    "scheduled_arrival": "18:45",
    "current_status": "On Time",
    "delay_minutes": 0,
    "source": "NDLS",
    "destination": "BPL"
}
```

### 3. CoachFormationAgent
**Purpose**: Load and manage coach composition data

**Responsibilities**:
- Load coach formation from database
- Cache formation data for performance
- Provide coach composition by train number
- Track coach types and capacities

**Input**:
```python
train_no: int  # Train number
```

**Output**:
```python
{
    "train_no": 12345,
    "total_coaches": 12,
    "total_length_m": 280.0,
    "engine_type": "WDG-4D",
    "coaches": [
        {
            "coach_number": 1,
            "coach_type": "A",
            "capacity": 72,
            "length_m": 21.5
        }
    ]
}
```

**Coach Types**:
- A: AC First Class
- B: AC 2-Tier
- C: AC 3-Tier
- D: AC Chair Car
- S: Sleeper Class
- etc.

### 4. CoachPositionAgent ⭐ (Most Important)
**Purpose**: Calculate coach positions on platform

**Workflow**:
1. **Load coach formation** - Get coach composition from CoachFormationAgent
2. **Decide engine direction** - Determine which way engine faces
3. **Calculate coach distances** - Compute position of each coach
4. **Map to platform zones** - Assign zones (A, B, C, D, etc.)
5. **Return position mapping** - Provide complete position data

**Input**:
```python
train_no: int                  # Train number
station_code: str              # Station code
platform_no: int               # Platform number
platform_length_m: float       # Platform length (optional)
engine_direction: str          # "towards_back" or "towards_front"
```

**Process**:
```
Engine Direction: TOWARDS_BACK
├─ Engine at platform start (0-22m)
├─ Coach 1: 22-43.5m (Zone A, B)
├─ Coach 2: 43.5-65m (Zone B)
├─ Coach 3: 65-86.5m (Zone B, C)
├─ ... (continues)
└─ Coach 12: 237-258.5m (Zone G)

Platform Zones:
A: 0-35m
B: 35-70m
C: 70-105m
D: 105-140m
E: 140-175m
F: 175-210m
G: 210-250m
```

**Output**:
```python
{
    "train_no": 12345,
    "station_code": "NDLS",
    "platform_no": 5,
    "engine_direction": "towards_back",
    "total_coaches": 12,
    "coach_positions": [
        {
            "coach_number": 1,
            "coach_type": "A",
            "start_distance_m": 22.0,
            "end_distance_m": 43.5,
            "zones": ["A", "B"],
            "position_on_platform": "center"
        }
    ]
}
```

**Constants**:
- Engine length: 22 meters
- Standard coach length: 21.5 meters
- Platform zone width: 35 meters (approximately)

### 5. StatusAgent
**Purpose**: Aggregate information from all agents

**Responsibilities**:
- Coordinate other agents
- Combine results into unified response
- Handle agent failures gracefully
- Provide fallback values

**Input**:
```python
train_no: int
station_code: str
platform_no: int
```

**Output**: Aggregated data from all agents

### 6. CoordinatorAgent
**Purpose**: Master orchestrator

**Responsibilities**:
- Initialize all sub-agents
- Manage agent lifecycle
- Coordinate execution flow
- Provide unified API

**Usage**:
```python
coordinator = CoordinatorAgent()
response = coordinator.execute(
    train_no=12345,
    station_code="NDLS",
    platform_no=5
)
```

## Agent Response Format

All agents return a standardized `AgentResponse`:

```python
class AgentResponse:
    success: bool              # Operation succeeded
    status: AgentStatus        # IDLE, PROCESSING, SUCCESS, ERROR, FAILED
    data: Dict[str, Any]      # Response data
    message: str              # Human-readable message
    error: Optional[str]      # Error message if failed
    timestamp: str            # ISO format timestamp
```

## Data Flow

```
┌─────────────────────────────────────────────────────┐
│ User Request (train_no, station_code, platform_no) │
└─────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────┐
│         CoordinatorAgent.execute()                  │
└─────────────────────────────────────────────────────┘
         │              │              │
         ▼              ▼              ▼
    ┌────────┐   ┌──────────┐   ┌──────────────┐
    │TrainInfo│  │CoachFormation│ │CoachPosition│
    │ Agent  │   │Agent     │   │Agent        │
    └────────┘   └──────────┘   └──────────────┘
         │              │              │
         ▼              ▼              ▼
    Response       Response        Response
    (train info)  (coaches)      (positions)
         │              │              │
         └──────────────┼──────────────┘
                        ▼
            ┌──────────────────────┐
            │  StatusAgent         │
            │  (Aggregates all)    │
            └──────────────────────┘
                        │
                        ▼
            ┌──────────────────────┐
            │  Final Response      │
            │  (Complete data)     │
            └──────────────────────┘
```

## Implementation Details

### Coach Position Algorithm

```python
def calculate_coach_positions(coaches, engine_direction):
    """
    Algorithm:
    1. Start with engine at position 0
    2. For each coach in sequence:
        a. Calculate start distance = current_distance
        b. Calculate end distance = current_distance + coach_length
        c. Find zones that overlap with [start, end]
        d. Create CoachPosition object
        e. Update current_distance = end_distance
    3. Return list of all positions
    """
```

### Zone Mapping

Platform zones are calculated based on start and end positions:

```python
platform_zones = {
    'A': (0, 35),
    'B': (35, 70),
    'C': (70, 105),
    'D': (105, 140),
    'E': (140, 175),
    'F': (175, 210),
    'G': (210, 250)
}

def get_zones_for_distance(start_m, end_m):
    """Return list of zones that overlap with [start_m, end_m]"""
    zones = []
    for zone_name, (zone_start, zone_end) in zones.items():
        if start_m < zone_end and end_m > zone_start:
            zones.append(zone_name)
    return zones
```

## Testing Strategy

### Unit Tests
- Test each agent independently
- Verify response format
- Test edge cases (empty coaches, invalid input)

### Integration Tests
- Test agent coordination
- Verify data flow between agents
- Test error handling

### Test Cases Covered
✓ BaseAgent initialization and response creation
✓ CoachPositionAgent zone calculation
✓ CoachPositionAgent position calculation
✓ Coach formation loading
✓ Train info retrieval
✓ Coordinator orchestration
✓ 12-coach train positioning (integration test)

## Usage Examples

### Example 1: Get Coach Positions
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
        print(f"Coach {coach['coach_number']}: {coach['zones']}")
```

### Example 2: Use Coordinator
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
    coach_positions = response.data["coach_positions"]
    print(f"Train {train_info['train_no']}: {coach_positions['total_coaches']} coaches")
```

### Example 3: Get Agent Status
```python
coordinator = CoordinatorAgent()
status = coordinator.get_agent_status()
# Output: {
#     'Train Information Agent': 'idle',
#     'Coach Formation Agent': 'idle',
#     'Coach Position Agent': 'idle',
#     'Status Agent': 'idle'
# }
```

## Error Handling

Agents use a consistent error handling pattern:

1. **Try-Catch**: Wrap execute() in try-except
2. **Status Update**: Set status to FAILED on error
3. **Error Response**: Return error response with message
4. **Logging**: Log errors for debugging

```python
try:
    # Execute agent logic
    result = process_data()
    return self._success_response(data=result)
except Exception as e:
    logger.error(f"Error in Agent: {str(e)}")
    return self._error_response(error=str(e))
```

## Extension Points

### Adding New Agents
1. Inherit from `BaseAgent`
2. Implement `execute()` method
3. Use `_success_response()` and `_error_response()`
4. Add to CoordinatorAgent
5. Write tests

### Custom Coach Positioning Logic
Override `_calculate_coach_positions()` in subclass

### Custom Zone Mapping
Override `_create_zone_mapping()` in subclass

## Performance Considerations

- **Caching**: CoachFormationAgent caches loaded formations
- **Async**: Agents can be executed in parallel (future enhancement)
- **Lazy Loading**: Services loaded only when needed
- **Data Structure**: Efficient zone lookup using dictionary

## Future Enhancements

1. **Async Execution**: Execute agents in parallel
2. **Real-time Updates**: Live coach position updates
3. **Multiple Platforms**: Handle multiple platforms simultaneously
4. **ML-based Direction**: ML model to predict engine direction
5. **API Integration**: Connect to real Indian Railways APIs
6. **Visualization**: Interactive platform map
7. **Notifications**: Alert users of coach locations

## Conclusion

The agent-based architecture provides:
- ✓ Modularity: Each agent has single responsibility
- ✓ Extensibility: Easy to add new agents
- ✓ Reliability: Consistent error handling
- ✓ Testability: Each agent can be tested independently
- ✓ Scalability: Can handle multiple requests
- ✓ Maintainability: Clear separation of concerns
