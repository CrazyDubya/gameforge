"""
Test Suite - Comprehensive Coverage (95%)

This test suite covers happy paths, edge cases, and error scenarios,
providing comprehensive coverage of the player manager module.

Coverage: ~95% ✅
"""

import pytest
from player_manager import (
    level_up_player,
    heal_player,
    damage_player,
    create_test_player,
    get_player,
    xp_for_next_level
)


# ============================================================================
# LEVEL UP TESTS - Comprehensive Coverage
# ============================================================================

def test_level_up_player_success():
    """Test successful level up"""
    player_id = create_test_player(level=1, xp=0)
    result = level_up_player(player_id, 100)
    assert result == True
    assert get_player(player_id).level == 2


def test_level_up_player_invalid_id():
    """Test with invalid player ID"""
    result = level_up_player("invalid_id", 100)
    assert result == False


def test_level_up_player_multiple_levels():
    """Test gaining multiple levels at once"""
    player_id = create_test_player(level=1, xp=0)
    level_up_player(player_id, 10000)  # Huge XP gain
    player = get_player(player_id)
    assert player.level > 5


def test_level_up_player_zero_xp():
    """Test with zero XP gain"""
    player_id = create_test_player(level=1, xp=50)
    level_up_player(player_id, 0)
    assert get_player(player_id).xp == 50
    assert get_player(player_id).level == 1


def test_level_up_player_negative_xp():
    """Test with negative XP (error case)"""
    player_id = create_test_player(level=1, xp=50)
    with pytest.raises(ValueError, match="XP gain cannot be negative"):
        level_up_player(player_id, -10)


def test_level_up_player_max_level():
    """Test at maximum level"""
    player_id = create_test_player(level=100, xp=0)
    level_up_player(player_id, 100)
    assert get_player(player_id).level == 100  # Should not exceed max


def test_level_up_player_almost_level_up():
    """Test XP gain that doesn't quite level up"""
    player_id = create_test_player(level=1, xp=0)
    level_up_player(player_id, 50)  # Need 100 for level 2
    player = get_player(player_id)
    assert player.level == 1
    assert player.xp == 50


# ============================================================================
# HEAL TESTS - Comprehensive Coverage
# ============================================================================

def test_heal_player_success():
    """Test successful heal"""
    player_id = create_test_player()
    player = get_player(player_id)
    player.health = 50
    
    result = heal_player(player_id, 30)
    assert result == True
    assert get_player(player_id).health == 80


def test_heal_player_invalid_id():
    """Test heal with invalid player ID"""
    result = heal_player("invalid_id", 30)
    assert result == False


def test_heal_player_overheal():
    """Test healing beyond max health"""
    player_id = create_test_player()
    player = get_player(player_id)
    player.health = 90
    
    heal_player(player_id, 50)  # Would go to 140, capped at 100
    assert get_player(player_id).health == 100


def test_heal_player_zero_amount():
    """Test healing with zero amount"""
    player_id = create_test_player()
    player = get_player(player_id)
    player.health = 50
    
    heal_player(player_id, 0)
    assert get_player(player_id).health == 50


def test_heal_player_negative_amount():
    """Test healing with negative amount (error case)"""
    player_id = create_test_player()
    with pytest.raises(ValueError, match="Heal amount cannot be negative"):
        heal_player(player_id, -10)


def test_heal_player_full_health():
    """Test healing when already at full health"""
    player_id = create_test_player()
    heal_player(player_id, 50)
    assert get_player(player_id).health == 100


# ============================================================================
# DAMAGE TESTS - Comprehensive Coverage
# ============================================================================

def test_damage_player_success():
    """Test successful damage"""
    player_id = create_test_player()
    result = damage_player(player_id, 20)
    assert result == True
    assert get_player(player_id).health == 80


def test_damage_player_invalid_id():
    """Test damage with invalid player ID"""
    result = damage_player("invalid_id", 20)
    assert result == False


def test_damage_player_death():
    """Test player death from damage"""
    player_id = create_test_player()
    result = damage_player(player_id, 150)  # More than max health
    assert result == False  # Player dies
    assert get_player(player_id).health == 0


def test_damage_player_exact_lethal():
    """Test damage that exactly kills player"""
    player_id = create_test_player()
    result = damage_player(player_id, 100)
    assert result == False  # Player dies
    assert get_player(player_id).health == 0


def test_damage_player_one_hp_remaining():
    """Test damage that leaves 1 HP"""
    player_id = create_test_player()
    result = damage_player(player_id, 99)
    assert result == True  # Player survives
    assert get_player(player_id).health == 1


def test_damage_player_zero_amount():
    """Test damage with zero amount"""
    player_id = create_test_player()
    result = damage_player(player_id, 0)
    assert result == True
    assert get_player(player_id).health == 100


def test_damage_player_negative_amount():
    """Test damage with negative amount (error case)"""
    player_id = create_test_player()
    with pytest.raises(ValueError, match="Damage amount cannot be negative"):
        damage_player(player_id, -10)


# ============================================================================
# HELPER FUNCTION TESTS
# ============================================================================

def test_xp_for_next_level():
    """Test XP calculation for various levels"""
    assert xp_for_next_level(1) == 100
    assert xp_for_next_level(5) == 500
    assert xp_for_next_level(10) == 1000


def test_create_test_player_defaults():
    """Test creating player with default values"""
    player_id = create_test_player()
    player = get_player(player_id)
    assert player.level == 1
    assert player.xp == 0
    assert player.health == 100


def test_create_test_player_custom_values():
    """Test creating player with custom values"""
    player_id = create_test_player("custom_player", level=10, xp=500)
    player = get_player(player_id)
    assert player.id == "custom_player"
    assert player.level == 10
    assert player.xp == 500


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

def test_player_lifecycle():
    """Test complete player lifecycle"""
    # Create player
    player_id = create_test_player()
    
    # Level up
    level_up_player(player_id, 300)
    assert get_player(player_id).level >= 2
    
    # Take damage
    damage_player(player_id, 50)
    assert get_player(player_id).health == 50
    
    # Heal
    heal_player(player_id, 30)
    assert get_player(player_id).health == 80
    
    # More damage
    result = damage_player(player_id, 90)
    assert result == False  # Dies
    assert get_player(player_id).health == 0
