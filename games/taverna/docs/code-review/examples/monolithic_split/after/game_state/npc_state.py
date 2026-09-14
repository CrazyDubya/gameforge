"""
NPC State Module - Focused on NPC management only

This module handles all NPC-related state and operations.
Part of the game_state.py refactoring (P0 Issue #2).
"""

from typing import Dict, List, Optional
from dataclasses import dataclass


@dataclass
class NPCState:
    """State information for an NPC."""
    npc_id: str
    name: str
    health: int = 100
    location: str = "starting_area"
    current_activity: str = "idle"
    relationship_to_player: int = 0  # -100 to +100
    is_hostile: bool = False
    
    def move_to(self, location: str) -> None:
        """Move NPC to a new location."""
        self.location = location
    
    def change_relationship(self, amount: int) -> None:
        """Modify relationship with player."""
        self.relationship_to_player = max(-100, min(100, 
            self.relationship_to_player + amount))
    
    def take_damage(self, amount: int) -> bool:
        """Apply damage to NPC. Returns True if NPC is defeated."""
        self.health = max(0, self.health - amount)
        return self.health == 0


class NPCManager:
    """Manages all NPCs in the game."""
    
    def __init__(self):
        self.npcs: Dict[str, NPCState] = {}
    
    def add_npc(self, npc: NPCState) -> None:
        """Add an NPC to the game."""
        self.npcs[npc.npc_id] = npc
    
    def remove_npc(self, npc_id: str) -> bool:
        """Remove an NPC from the game."""
        if npc_id in self.npcs:
            del self.npcs[npc_id]
            return True
        return False
    
    def get_npc(self, npc_id: str) -> Optional[NPCState]:
        """Get an NPC by ID."""
        return self.npcs.get(npc_id)
    
    def get_npcs_at_location(self, location: str) -> List[NPCState]:
        """Get all NPCs at a specific location."""
        return [npc for npc in self.npcs.values() if npc.location == location]
    
    def get_hostile_npcs_at_location(self, location: str) -> List[NPCState]:
        """Get all hostile NPCs at a specific location."""
        return [
            npc for npc in self.npcs.values()
            if npc.location == location and npc.is_hostile
        ]
    
    def get_friendly_npcs(self) -> List[NPCState]:
        """Get all NPCs with positive relationship."""
        return [
            npc for npc in self.npcs.values()
            if npc.relationship_to_player > 0
        ]
    
    def move_npc(self, npc_id: str, new_location: str) -> bool:
        """Move an NPC to a new location."""
        npc = self.get_npc(npc_id)
        if npc:
            npc.move_to(new_location)
            return True
        return False


# ✅ FOCUSED MODULE - Only NPC-related functionality
# ✅ Easy to test, maintain, and understand
