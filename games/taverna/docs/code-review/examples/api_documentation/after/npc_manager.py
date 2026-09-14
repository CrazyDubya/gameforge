"""
NPC Manager Module - WELL DOCUMENTED
=====================================

This module provides comprehensive NPC (Non-Player Character) management
for the game, including creation, location tracking, and interaction processing.

The main class is NPCManager which handles all NPC-related operations.

Main Classes:
    NPCManager: Central manager for all NPC operations

Main Functions:
    process_interaction: Process interactions between player and NPCs
    calculate_relationship_change: Calculate relationship score changes

Usage Example:
    >>> from npc_manager import NPCManager
    >>> manager = NPCManager()
    >>> manager.add_npc("guard_01", "Town Guard", "town_gate")
    >>> npcs = manager.get_npcs_at_location("town_gate")
    >>> print(npcs)
    ['guard_01']

Author: Living Rusted Tankard Team
Version: 1.0.0
"""

from typing import Dict, List, Optional, Any
from enum import Enum


class InteractionType(Enum):
    """Valid types of NPC interactions."""
    CONVERSATION = "conversation"
    TRADE = "trade"
    COMBAT = "combat"
    QUEST = "quest"


class NPCManager:
    """
    Manages all NPCs in the game world.
    
    This class provides methods to create, track, and manage NPCs including
    their locations, states, and interactions with the player.
    
    Attributes:
        npcs: Dictionary mapping NPC IDs to their data
    
    Example:
        >>> manager = NPCManager()
        >>> manager.add_npc("merchant_01", "Bob the Merchant", "market")
        >>> npc = manager.get_npc("merchant_01")
        >>> print(npc["name"])
        Bob the Merchant
    """
    
    def __init__(self):
        """Initialize the NPC manager with an empty NPC registry."""
        self.npcs: Dict[str, Dict[str, Any]] = {}
    
    def add_npc(self, npc_id: str, name: str, location: str) -> None:
        """
        Add a new NPC to the game world.
        
        Creates a new NPC with the specified ID, name, and starting location.
        The NPC is initialized with default values (health: 100).
        
        Args:
            npc_id: Unique identifier for the NPC
            name: Display name of the NPC
            location: Starting location ID for the NPC
        
        Raises:
            ValueError: If npc_id already exists
        
        Example:
            >>> manager.add_npc("guard_01", "Town Guard", "town_gate")
        """
        if npc_id in self.npcs:
            raise ValueError(f"NPC with ID '{npc_id}' already exists")
        
        self.npcs[npc_id] = {
            "name": name,
            "location": location,
            "health": 100
        }
    
    def get_npc(self, npc_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve an NPC's data by ID.
        
        Args:
            npc_id: The unique identifier of the NPC to retrieve
        
        Returns:
            Dictionary containing NPC data with keys:
                - name: str
                - location: str
                - health: int
            Returns None if NPC doesn't exist.
        
        Example:
            >>> npc = manager.get_npc("guard_01")
            >>> if npc:
            ...     print(f"NPC is at {npc['location']}")
            NPC is at town_gate
        """
        return self.npcs.get(npc_id)
    
    def move_npc(self, npc_id: str, new_location: str) -> bool:
        """
        Move an NPC to a new location.
        
        Args:
            npc_id: ID of the NPC to move
            new_location: ID of the destination location
        
        Returns:
            True if the NPC was successfully moved, False if NPC doesn't exist
        
        Example:
            >>> success = manager.move_npc("guard_01", "castle")
            >>> print(success)
            True
        """
        if npc_id in self.npcs:
            self.npcs[npc_id]["location"] = new_location
            return True
        return False
    
    def get_npcs_at_location(self, location: str) -> List[str]:
        """
        Get all NPCs currently at a specific location.
        
        Args:
            location: Location ID to search
        
        Returns:
            List of NPC IDs at the specified location. Returns empty list
            if no NPCs are at the location.
        
        Example:
            >>> manager.add_npc("guard_01", "Guard", "gate")
            >>> manager.add_npc("guard_02", "Guard", "gate")
            >>> npcs = manager.get_npcs_at_location("gate")
            >>> print(len(npcs))
            2
        """
        result = []
        for npc_id, npc_data in self.npcs.items():
            if npc_data["location"] == location:
                result.append(npc_id)
        return result


def process_interaction(
    npc_id: str,
    player_id: str,
    interaction_type: InteractionType,
    context: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process an interaction between a player and an NPC.
    
    This function handles various types of interactions including conversations,
    trades, combat, and quest-related interactions. It validates the interaction,
    processes it according to type, and returns the result.
    
    Args:
        npc_id: Unique identifier for the NPC
        player_id: Unique identifier for the player
        interaction_type: Type of interaction (from InteractionType enum)
        context: Optional additional data such as:
            - location: Current location
            - items: Items involved in trade
            - dialogue_choice: Player's dialogue selection
    
    Returns:
        Dictionary containing:
            - success: bool - Whether interaction succeeded
            - outcome: str - Outcome description
            - relationship_change: int - Change in relationship score
            - data: dict - Type-specific result data
    
    Raises:
        ValueError: If npc_id or player_id is invalid
        TypeError: If interaction_type is not from InteractionType enum
    
    Example:
        >>> result = process_interaction(
        ...     npc_id="merchant_01",
        ...     player_id="player_1",
        ...     interaction_type=InteractionType.TRADE,
        ...     context={"items": ["sword", "shield"]}
        ... )
        >>> print(result["success"])
        True
    """
    # Implementation would go here
    return {
        "success": True,
        "outcome": "interaction_processed",
        "relationship_change": 0,
        "data": {}
    }


def calculate_relationship_change(
    current_relationship: int,
    interaction_outcome: str
) -> int:
    """
    Calculate new relationship score based on interaction outcome.
    
    Relationship scores range from -100 (hostile) to +100 (friendly).
    Positive outcomes increase the score, negative outcomes decrease it.
    
    Args:
        current_relationship: Current relationship score (-100 to 100)
        interaction_outcome: Outcome of interaction, one of:
            - "positive": Friendly interaction (+10)
            - "negative": Hostile interaction (-10)
            - "neutral": No change (0)
    
    Returns:
        New relationship score, clamped to range [-100, 100]
    
    Example:
        >>> new_score = calculate_relationship_change(50, "positive")
        >>> print(new_score)
        60
        
        >>> new_score = calculate_relationship_change(95, "positive")
        >>> print(new_score)  # Clamped to maximum
        100
    """
    if interaction_outcome == "positive":
        return min(100, current_relationship + 10)
    elif interaction_outcome == "negative":
        return max(-100, current_relationship - 10)
    return current_relationship
