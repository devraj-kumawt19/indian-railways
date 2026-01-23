"""Station model - represents a railway station."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Station:
    """Railway station entity."""
    station_code: str
    station_name: str
    station_type: str  # Major Junction, Major Station, etc.
    state: str
    platform_count: int
    zone: str  # Railway zone (NR, CR, ER, etc.)
    
    @property
    def is_major_junction(self) -> bool:
        """Check if station is a major junction."""
        return self.station_type == "Major Junction"
    
    @property
    def full_name(self) -> str:
        """Return formatted station name with code."""
        return f"{self.station_name} ({self.station_code})"
