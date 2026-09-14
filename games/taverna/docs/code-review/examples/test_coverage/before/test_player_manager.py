"""
Test Suite - Inadequate Coverage (50%)

This test suite only covers the happy path, leaving many edge cases
and error scenarios untested.

Coverage: ~50% ❌
"""

import pytest
from player_manager import (
    level_up_player,
    heal_player,
    damage_player,
    create_test_player,
    get_player
)


def test_level_up_player_success():
    """Test successful level up - HAPPY PATH ONLY"""
    player_id = create_test_player(level=1, xp=0)
    result = level_up_player(player_id, 100)
    assert result == True
    assert get_player(player_id).level == 2


def test_heal_player_success():
    """Test successful heal - HAPPY PATH ONLY"""
    player_id = create_test_player()
    player = get_player(player_id)
    player.health = 50
    
    result = heal_player(player_id, 30)
    assert result == True
    assert get_player(player_id).health == 80


def test_damage_player_success():
    """Test successful damage - HAPPY PATH ONLY"""
    player_id = create_test_player()
    result = damage_player(player_id, 20)
    assert result == True
    assert get_player(player_id).health == 80


# Missing tests for:
# - Invalid player IDs
# - Multiple level ups
# - Zero/negative values
# - Maximum level
# - Player death
# - Overheal
# - Edge cases
# - Error paths
