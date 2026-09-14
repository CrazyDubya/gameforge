"""
NPC Manager Module - UNDOCUMENTED

This module lacks proper documentation making it hard to use and maintain.
"""

from typing import Dict, Optional


class NPCManager:
    def __init__(self):
        self.npcs = {}
    
    def add_npc(self, npc_id, name, location):
        # No docstring
        # Parameters unclear
        # No type hints
        self.npcs[npc_id] = {
            "name": name,
            "location": location,
            "health": 100
        }
    
    def get_npc(self, npc_id):
        # What does this return?
        # What if NPC doesn't exist?
        return self.npcs.get(npc_id)
    
    def move_npc(self, npc_id, new_location):
        # Can this fail?
        # What's the return value?
        if npc_id in self.npcs:
            self.npcs[npc_id]["location"] = new_location
            return True
        return False
    
    def get_npcs_at_location(self, location):
        # Return type?
        # Empty list or None?
        result = []
        for npc_id, npc_data in self.npcs.items():
            if npc_data["location"] == location:
                result.append(npc_id)
        return result


def process_interaction(npc_id, player_id, interaction_type, context=None):
    # What does this do?
    # What are valid interaction types?
    # What's in context?
    pass


def calculate_relationship_change(current_relationship, interaction_outcome):
    # Algorithm unclear
    # Range of values?
    if interaction_outcome == "positive":
        return min(100, current_relationship + 10)
    elif interaction_outcome == "negative":
        return max(-100, current_relationship - 10)
    return current_relationship
