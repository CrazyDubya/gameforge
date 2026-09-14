"""
World State Module - Focused on world management only

This module handles all world-related state and operations.
Part of the game_state.py refactoring (P0 Issue #2).
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta


@dataclass
class Location:
    """Represents a location in the game world."""
    location_id: str
    name: str
    description: str
    connected_locations: List[str] = field(default_factory=list)
    npcs_present: List[str] = field(default_factory=list)
    items_present: List[str] = field(default_factory=list)
    
    def add_npc(self, npc_id: str) -> None:
        """Add an NPC to this location."""
        if npc_id not in self.npcs_present:
            self.npcs_present.append(npc_id)
    
    def remove_npc(self, npc_id: str) -> None:
        """Remove an NPC from this location."""
        if npc_id in self.npcs_present:
            self.npcs_present.remove(npc_id)
    
    def is_connected_to(self, location_id: str) -> bool:
        """Check if this location is connected to another."""
        return location_id in self.connected_locations


class WorldState:
    """Manages the game world state."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_time: datetime = datetime.now()
        self.weather: str = "clear"
        self.day_count: int = 1
        self.season: str = "spring"
    
    def add_location(self, location: Location) -> None:
        """Add a location to the world."""
        self.locations[location.location_id] = location
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID."""
        return self.locations.get(location_id)
    
    def advance_time(self, hours: int) -> None:
        """Advance world time."""
        self.current_time += timedelta(hours=hours)
        # Update day count if we've passed midnight
        if self.current_time.hour < (self.current_time - timedelta(hours=hours)).hour:
            self.day_count += 1
    
    def set_weather(self, weather: str) -> None:
        """Set the current weather."""
        self.weather = weather
    
    def get_connected_locations(self, location_id: str) -> List[Location]:
        """Get all locations connected to the given location."""
        location = self.get_location(location_id)
        if not location:
            return []
        return [
            self.get_location(loc_id)
            for loc_id in location.connected_locations
            if self.get_location(loc_id) is not None
        ]


# ✅ FOCUSED MODULE - Only world-related functionality
# ✅ Easy to test, maintain, and understand
