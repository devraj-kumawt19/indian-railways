"""Coach Formation Agent - manages coach composition data."""
from typing import List, Dict, Any, Optional
from src.agents.base_agent import BaseAgent, AgentResponse, AgentStatus
import logging
import pandas as pd
import os

logger = logging.getLogger(__name__)


class CoachFormation:
    """Represents coach formation data for a train."""
    
    def __init__(
        self,
        train_no: int,
        coaches: List[Dict[str, Any]],
        engine_type: str = "WDG-4D"
    ):
        self.train_no = train_no
        self.coaches = coaches
        self.engine_type = engine_type
        self.total_length = self._calculate_total_length()
    
    def _calculate_total_length(self) -> float:
        """Calculate total length from coach composition."""
        total = 0.0
        # Engine is typically 20-25 meters
        total += 22.0
        # Add coach lengths (typically 21.5m each)
        total += len(self.coaches) * 21.5
        return total
    
    def get_coaches(self) -> List[Dict[str, Any]]:
        """Get list of all coaches."""
        return self.coaches
    
    def get_coach_by_number(self, coach_no: int) -> Optional[Dict[str, Any]]:
        """Get specific coach by number."""
        return next((c for c in self.coaches if c['coach_number'] == coach_no), None)


class CoachFormationAgent(BaseAgent):
    """Agent responsible for loading and managing coach formations."""
    
    def __init__(self, data_path: str = "data"):
        super().__init__("coach_formation_agent", "Coach Formation Agent")
        self.data_path = data_path
        self.formations_cache: Dict[int, CoachFormation] = {}
        self._load_formations()
    
    def _load_formations(self):
        """Load coach formations from data files."""
        try:
            csv_path = os.path.join(self.data_path, "trains_with_coaches.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                logger.info(f"Loaded coach data from {csv_path}")
            else:
                logger.warning(f"Coach data file not found: {csv_path}")
        except Exception as e:
            logger.error(f"Error loading coach formations: {str(e)}")
    
    def execute(
        self,
        train_no: int,
        **kwargs
    ) -> AgentResponse:
        """
        Execute coach formation retrieval.
        
        Args:
            train_no: Train number
            
        Returns:
            AgentResponse with coach composition
        """
        self.set_status(AgentStatus.PROCESSING)
        
        try:
            # Check cache
            if train_no in self.formations_cache:
                formation = self.formations_cache[train_no]
                return self._success_response(
                    data=self._formation_to_dict(formation),
                    message=f"Retrieved formation for train {train_no}"
                )
            
            # Load from data source
            formation = self._get_formation_from_source(train_no)
            if formation:
                self.formations_cache[train_no] = formation
                self.set_status(AgentStatus.SUCCESS)
                return self._success_response(
                    data=self._formation_to_dict(formation),
                    message=f"Retrieved formation for train {train_no}"
                )
            
            return self._error_response(
                error=f"Formation not found for train {train_no}",
                message="Could not retrieve coach composition"
            )
            
        except Exception as e:
            logger.error(f"Error in CoachFormationAgent: {str(e)}")
            self.set_status(AgentStatus.FAILED)
            return self._error_response(
                error=str(e),
                message="Failed to retrieve coach formation"
            )
    
    def _get_formation_from_source(self, train_no: int) -> Optional[CoachFormation]:
        """Get formation from data source."""
        try:
            csv_path = os.path.join(self.data_path, "trains_with_coaches.csv")
            if os.path.exists(csv_path):
                df = pd.read_csv(csv_path)
                train_data = df[df['train_no'] == train_no]
                
                if len(train_data) > 0:
                    coaches = []
                    for _, row in train_data.iterrows():
                        coach = {
                            'coach_number': row.get('coach_number', 0),
                            'coach_type': row.get('coach_type', 'S'),
                            'capacity': row.get('capacity', 72),
                            'length_m': 21.5  # Standard coach length
                        }
                        coaches.append(coach)
                    
                    formation = CoachFormation(
                        train_no=train_no,
                        coaches=coaches
                    )
                    return formation
        except Exception as e:
            logger.error(f"Error loading formation from source: {str(e)}")
        
        return None
    
    def _formation_to_dict(self, formation: CoachFormation) -> Dict[str, Any]:
        """Convert formation object to dictionary."""
        return {
            "train_no": formation.train_no,
            "total_coaches": len(formation.coaches),
            "total_length_m": formation.total_length,
            "engine_type": formation.engine_type,
            "coaches": formation.get_coaches()
        }
