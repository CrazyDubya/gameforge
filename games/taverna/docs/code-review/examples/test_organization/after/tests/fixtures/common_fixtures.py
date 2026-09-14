"""
Common test fixtures - PROPERLY ORGANIZED

Shared fixtures used across multiple test files.
"""

import pytest


@pytest.fixture
def sample_player():
    """Fixture providing a sample player for tests."""
    return {
        "id": "player_1",
        "name": "TestPlayer",
        "health": 100,
        "mana": 100
    }


@pytest.fixture
def sample_npc():
    """Fixture providing a sample NPC for tests."""
    return {
        "id": "npc_1",
        "name": "TestNPC",
        "health": 100,
        "location": "tavern"
    }
