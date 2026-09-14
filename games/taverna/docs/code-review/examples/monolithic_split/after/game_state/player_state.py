"""
Player State Module - Focused on player management only

This module handles all player-related state and operations.
Part of the game_state.py refactoring (P0 Issue #2).
"""

from typing import Dict
from dataclasses import dataclass, field
from enum import Enum


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
    
    def remove_item(self, item_name: str, quantity: int = 1) -> bool:
        """Remove item from inventory."""
        if item_name not in self.items:
            return False
        current = self.items[item_name]
        if current < quantity:
            return False
        self.items[item_name] = current - quantity
        if self.items[item_name] == 0:
            del self.items[item_name]
        return True
    
    def has_item(self, item_name: str, quantity: int = 1) -> bool:
        """Check if player has specified quantity of item."""
        return self.items.get(item_name, 0) >= quantity


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
        if self.status == PlayerStatus.DEAD:
            self.status = PlayerStatus.ALIVE
    
    def gain_experience(self, amount: int) -> bool:
        """Add experience and check for level up."""
        self.experience += amount
        xp_for_next_level = self.level * 100
        if self.experience >= xp_for_next_level:
            self.level_up()
            return True
        return False
    
    def level_up(self) -> None:
        """Level up the player."""
        self.level += 1
        self.health = 100
        self.mana = 100
    
    def move_to(self, location: str) -> None:
        """Move player to a new location."""
        self.location = location


# ✅ FOCUSED MODULE - Only player-related functionality
# ✅ Easy to test, maintain, and understand
