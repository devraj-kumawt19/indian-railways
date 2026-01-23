"""Coach Position Agent - calculates coach positions on platform."""
from typing import List, Dict, Any, Optional
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
from src.agents.coach_formation_agent import CoachFormationAgent, CoachFormation
import logging

logger = logging.getLogger(__name__)


class EngineDirection:
    """Engine direction for coach positioning."""
    TOWARDS_BACK = "towards_back"  # Engine at front, coaches extend backwards
    TOWARDS_FRONT = "towards_front"  # Engine at back, coaches extend forwards


class CoachPosition:
    """Position of a coach on the platform."""
    
    def __init__(
        self,
        coach_number: int,
        coach_type: str,
        start_distance_m: float,
        end_distance_m: float,
        zones: List[str],
        position_on_platform: str = "center"
    ):
        self.coach_number = coach_number
        self.coach_type = coach_type
        self.start_distance_m = start_distance_m
        self.end_distance_m = end_distance_m
        self.zones = zones
        self.position_on_platform = position_on_platform
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "coach_number": self.coach_number,
            "coach_type": self.coach_type,
            "start_distance_m": round(self.start_distance_m, 2),
            "end_distance_m": round(self.end_distance_m, 2),
            "zones": self.zones,
            "position_on_platform": self.position_on_platform
        }


class CoachPositionAgent(BaseAgent):
    """
    Agent responsible for calculating coach positions on platform.
    
    Workflow:
    1. Load coach formation from database/cache
    2. Decide engine direction based on station and route
    3. Calculate coach distances from engine
    4. Map distances to platform zones (A, B, C, D, etc.)
    5. Return coach position mapping
    """
    
    def __init__(self):
        super().__init__("coach_position_agent", "Coach Position Agent")
        self.formation_agent = CoachFormationAgent()
        self.platform_zone_mapping = self._create_zone_mapping()
    
    def _create_zone_mapping(self) -> Dict[str, tuple]:
        """
        Create platform zone mapping.
        Standard Indian platforms are divided into zones A, B, C, D, E, F, G
        Each zone is typically 30-40 meters.
        """
        return {
            'A': (0, 35),
            'B': (35, 70),
            'C': (70, 105),
            'D': (105, 140),
            'E': (140, 175),
            'F': (175, 210),
            'G': (210, 250)
        }
    
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
        Calculate coach positions on platform.
        
        Args:
            train_no: Train number
            station_code: Station code
            platform_no: Platform number
            platform_length_m: Optional platform length in meters
            engine_direction: Optional engine direction override
            
        Returns:
            AgentResponse with coach positions
        """
        self.set_status(AgentStatus.PROCESSING)
        
        try:
            # Step 1: Load coach formation
            formation_response = self.formation_agent.execute(train_no=train_no)
            if not formation_response.success:
                return self._error_response(
                    error="Could not load coach formation",
                    message=formation_response.error
                )
            
            formation_data = formation_response.data
            coaches = formation_data.get('coaches', [])
            
            if not coaches:
                return self._error_response(
                    error="No coaches found in formation",
                    message=f"Train {train_no} has no coach data"
                )
            
            # Step 2: Decide engine direction
            if engine_direction is None:
                engine_direction = self._decide_engine_direction(
                    station_code, train_no
                )
            
            # Step 3 & 4: Calculate positions and map to zones
            coach_positions = self._calculate_coach_positions(
                coaches=coaches,
                engine_direction=engine_direction,
                platform_length_m=platform_length_m
            )
            
            # Step 5: Return coach position mapping
            self.set_status(AgentStatus.SUCCESS)
            return self._success_response(
                data={
                    "train_no": train_no,
                    "station_code": station_code,
                    "platform_no": platform_no,
                    "engine_direction": engine_direction,
                    "coach_positions": [cp.to_dict() for cp in coach_positions],
                    "total_coaches": len(coach_positions)
                },
                message=f"Calculated positions for {len(coach_positions)} coaches"
            )
            
        except Exception as e:
            logger.error(f"Error in CoachPositionAgent: {str(e)}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(
                error=str(e),
                message="Failed to calculate coach positions"
            )
    
    def _decide_engine_direction(
        self,
        station_code: str,
        train_no: int
    ) -> str:
        """
        Decide engine direction based on station and train information.
        
        Logic:
        - Check if station is origin/destination
        - Check if train is terminating
        - Check platform orientation
        
        For now, use simple heuristic.
        """
        # Default direction - engine at front (coaches extend backward)
        # In production, would check:
        # 1. Train route information
        # 2. Station orientation
        # 3. Platform layout
        return EngineDirection.TOWARDS_BACK
    
    def _calculate_coach_positions(
        self,
        coaches: List[Dict[str, Any]],
        engine_direction: str,
        platform_length_m: Optional[float] = None
    ) -> List[CoachPosition]:
        """
        Calculate positions for all coaches.
        
        Args:
            coaches: List of coach information
            engine_direction: Direction engine faces
            platform_length_m: Optional platform length
            
        Returns:
            List of CoachPosition objects
        """
        coach_positions: List[CoachPosition] = []
        
        # Engine length (typically 22 meters)
        engine_length = 22.0
        # Standard coach length
        coach_length = 21.5
        
        if engine_direction == EngineDirection.TOWARDS_BACK:
            # Engine at position 0-22, coaches extend backward (0 to n*21.5)
            current_distance = engine_length
            
            for coach in coaches:
                coach_number = coach.get('coach_number', 0)
                coach_type = coach.get('coach_type', 'S')
                
                start_dist = current_distance
                end_dist = current_distance + coach_length
                
                # Map to zones
                zones = self._get_zones_for_distance(start_dist, end_dist)
                
                position = CoachPosition(
                    coach_number=coach_number,
                    coach_type=coach_type,
                    start_distance_m=start_dist,
                    end_distance_m=end_dist,
                    zones=zones
                )
                coach_positions.append(position)
                
                current_distance = end_dist
        
        else:  # EngineDirection.TOWARDS_FRONT
            # Engine at end, coaches extend forward (reverse order)
            if platform_length_m is None:
                platform_length_m = 300  # Default platform length
            
            coaches_reversed = list(reversed(coaches))
            current_distance = platform_length_m - engine_length
            
            for coach in coaches_reversed:
                coach_number = coach.get('coach_number', 0)
                coach_type = coach.get('coach_type', 'S')
                
                start_dist = current_distance - coach_length
                end_dist = current_distance
                
                # Map to zones
                zones = self._get_zones_for_distance(start_dist, end_dist)
                
                position = CoachPosition(
                    coach_number=coach_number,
                    coach_type=coach_type,
                    start_distance_m=start_dist,
                    end_distance_m=end_dist,
                    zones=zones
                )
                coach_positions.insert(0, position)
                
                current_distance = start_dist
        
        return coach_positions
    
    def _get_zones_for_distance(
        self,
        start_m: float,
        end_m: float
    ) -> List[str]:
        """
        Get platform zones that coach occupies.
        
        Args:
            start_m: Start distance from origin
            end_m: End distance from origin
            
        Returns:
            List of zone names
        """
        zones = []
        
        for zone_name, (zone_start, zone_end) in self.platform_zone_mapping.items():
            # Check if coach overlaps with this zone
            if start_m < zone_end and end_m > zone_start:
                zones.append(zone_name)
        
        return zones
