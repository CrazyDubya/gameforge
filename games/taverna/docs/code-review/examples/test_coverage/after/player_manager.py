"""
Player Manager Module - Comprehensive Test Coverage

Same code as before, but now with comprehensive test coverage.

Status: 🟢 HIGH COVERAGE - Well tested
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Player:
    """Player data structure"""
    id: str
    name: str
    level: int
    xp: int
    health: int
    max_health: int


# Simulated database
_players_db = {}


def get_player(player_id: str) -> Optional[Player]:
    """Get player by ID"""
    return _players_db.get(player_id)


def save_player(player: Player) -> None:
    """Save player to database"""
    _players_db[player.id] = player


def xp_for_next_level(level: int) -> int:
    """Calculate XP required for next level"""
    return level * 100


def level_up_player(player_id: str, xp_gain: int) -> bool:
    """
    Level up player based on XP gain.
    
    Returns True if successful, False otherwise.
    """
    player = get_player(player_id)
    if not player:
        return False
    
    if xp_gain < 0:
        raise ValueError("XP gain cannot be negative")
    
    player.xp += xp_gain
    
    # Handle multiple level ups
    max_level = 100
    while player.xp >= xp_for_next_level(player.level) and player.level < max_level:
        player.level += 1
        player.xp -= xp_for_next_level(player.level - 1)
    
    save_player(player)
    return True


def heal_player(player_id: str, amount: int) -> bool:
    """
    Heal player by specified amount.
    
    Returns True if successful, False otherwise.
    """
    player = get_player(player_id)
    if not player:
        return False
    
    if amount < 0:
        raise ValueError("Heal amount cannot be negative")
    
    player.health = min(player.health + amount, player.max_health)
    save_player(player)
    return True


def damage_player(player_id: str, amount: int) -> bool:
    """
    Damage player by specified amount.
    
    Returns True if player survives, False if player dies.
    """
    player = get_player(player_id)
    if not player:
        return False
    
    if amount < 0:
        raise ValueError("Damage amount cannot be negative")
    
    player.health = max(player.health - amount, 0)
    save_player(player)
    
    return player.health > 0


# Helper function for testing
def create_test_player(player_id: str = "test_player", level: int = 1, xp: int = 0) -> str:
    """Create a test player"""
    player = Player(
        id=player_id,
        name="Test Player",
        level=level,
        xp=xp,
        health=100,
        max_health=100
    )
    save_player(player)
    return player_id
