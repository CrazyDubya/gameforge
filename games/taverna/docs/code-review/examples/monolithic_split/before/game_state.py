"""
Game State Module - MONOLITHIC VERSION (Simplified)

This is a simplified demonstration of a monolithic file.
In the actual codebase, this file contains 3,017 lines with:
- 3 classes
- 88 functions
- Multiple responsibilities (player, world, NPCs, events)

This simplified version demonstrates the problem structure.
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


# ============================================================================
# PLAYER STATE (Should be in player_state.py)
# ============================================================================

class PlayerStatus(Enum):
    """Player status enumeration."""
    ALIVE = "alive"
    DEAD = "dead"
    UNCONSCIOUS = "unconscious"


@dataclass
class PlayerInventory:
    """Player inventory management."""
    items: Dict[str, int] = field(default_factory=dict)
    max_capacity: int = 100
    current_weight: float = 0.0
    
    def add_item(self, item_name: str, quantity: int = 1) -> bool:
        """Add item to inventory."""
        if self.current_weight >= self.max_capacity:
            return False
        self.items[item_name] = self.items.get(item_name, 0) + quantity
        return True


@dataclass
class PlayerState:
    """Player state information."""
    player_id: str
    name: str
    status: PlayerStatus = PlayerStatus.ALIVE
    health: int = 100
    mana: int = 100
    level: int = 1
    experience: int = 0
    location: str = "starting_area"
    inventory: PlayerInventory = field(default_factory=PlayerInventory)
    
    def take_damage(self, amount: int) -> None:
        """Apply damage to player."""
        self.health = max(0, self.health - amount)
        if self.health == 0:
            self.status = PlayerStatus.DEAD
    
    def heal(self, amount: int) -> None:
        """Heal the player."""
        self.health = min(100, self.health + amount)


# ============================================================================
# WORLD STATE (Should be in world_state.py)
# ============================================================================

@dataclass
class Location:
    """Represents a location in the game world."""
    location_id: str
    name: str
    description: str
    connected_locations: List[str] = field(default_factory=list)
    npcs_present: List[str] = field(default_factory=list)


class WorldState:
    """Manages the game world state."""
    
    def __init__(self):
        self.locations: Dict[str, Location] = {}
        self.current_time: datetime = datetime.now()
        self.weather: str = "clear"
        self.day_count: int = 1
    
    def add_location(self, location: Location) -> None:
        """Add a location to the world."""
        self.locations[location.location_id] = location
    
    def get_location(self, location_id: str) -> Optional[Location]:
        """Get a location by ID."""
        return self.locations.get(location_id)
    
    def advance_time(self, hours: int) -> None:
        """Advance world time."""
        from datetime import timedelta
        self.current_time += timedelta(hours=hours)


# ============================================================================
# NPC STATE (Should be in npc_state.py)
# ============================================================================

@dataclass
class NPCState:
    """State information for an NPC."""
    npc_id: str
    name: str
    health: int = 100
    location: str = "starting_area"
    current_activity: str = "idle"
    relationship_to_player: int = 0  # -100 to +100


class NPCManager:
    """Manages all NPCs in the game."""
    
    def __init__(self):
        self.npcs: Dict[str, NPCState] = {}
    
    def add_npc(self, npc: NPCState) -> None:
        """Add an NPC to the game."""
        self.npcs[npc.npc_id] = npc
    
    def get_npc(self, npc_id: str) -> Optional[NPCState]:
        """Get an NPC by ID."""
        return self.npcs.get(npc_id)
    
    def get_npcs_at_location(self, location: str) -> List[NPCState]:
        """Get all NPCs at a specific location."""
        return [npc for npc in self.npcs.values() if npc.location == location]


# ============================================================================
# EVENT STATE (Should be in event_state.py)
# ============================================================================

@dataclass
class GameEvent:
    """Represents a game event."""
    event_id: str
    event_type: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)


class EventManager:
    """Manages game events."""
    
    def __init__(self):
        self.events: List[GameEvent] = []
        self.event_queue: List[GameEvent] = []
    
    def add_event(self, event: GameEvent) -> None:
        """Add an event to history."""
        self.events.append(event)
    
    def queue_event(self, event: GameEvent) -> None:
        """Queue an event for processing."""
        self.event_queue.append(event)
    
    def process_events(self) -> None:
        """Process all queued events."""
        while self.event_queue:
            event = self.event_queue.pop(0)
            self.add_event(event)


# ============================================================================
# MAIN GAME STATE (Should coordinate the above modules)
# ============================================================================

class GameState:
    """
    MONOLITHIC CLASS - Contains everything!
    
    This demonstrates the problem: One class managing:
    - Player state
    - World state  
    - NPC management
    - Event handling
    - Game persistence
    
    Result: 3,017 lines, 88 functions, impossible to maintain!
    """
    
    def __init__(self):
        self.player: Optional[PlayerState] = None
        self.world: WorldState = WorldState()
        self.npc_manager: NPCManager = NPCManager()
        self.event_manager: EventManager = EventManager()
        self.save_data: Dict[str, Any] = {}
    
    def initialize_game(self, player_name: str) -> None:
        """Initialize a new game."""
        self.player = PlayerState(
            player_id="player_1",
            name=player_name
        )
        self.world = WorldState()
        self.npc_manager = NPCManager()
        self.event_manager = EventManager()
    
    def save_game(self) -> Dict[str, Any]:
        """Save game state."""
        return {
            "player": self.player,
            "world": self.world,
            "npcs": self.npc_manager.npcs,
            "events": self.event_manager.events
        }
    
    def load_game(self, save_data: Dict[str, Any]) -> None:
        """Load game state."""
        self.save_data = save_data
        # ... complex loading logic ...
    
    # ... 88 more functions handling all game systems ...
    # ... 2,900 more lines of code ...


# ⚠️ PROBLEM: Everything in one file!
# ⚠️ 3,017 lines, multiple responsibilities
# ⚠️ Difficult to maintain, test, and understand
