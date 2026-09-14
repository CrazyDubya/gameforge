"""
NPC Relationships System - DUPLICATE in npc_modules directory

⚠️ WARNING: This is a DUPLICATE of core/npc_systems/relationships.py
This is a simplified example showing the duplication issue.
In the actual codebase, this file contains 626 lines.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class RelationshipType(Enum):
    """Types of relationships between NPCs."""
    FRIEND = "friend"
    ENEMY = "enemy"
    FAMILY = "family"
    ROMANTIC = "romantic"
    NEUTRAL = "neutral"
    ALLY = "ally"
    RIVAL = "rival"


@dataclass
class Relationship:
    """Represents a relationship between two characters."""
    character1_id: str
    character2_id: str
    relationship_type: RelationshipType
    strength: int = 0  # -100 to +100
    trust: int = 50  # 0 to 100
    history: List[str] = None
    
    def __post_init__(self):
        if self.history is None:
            self.history = []
    
    def modify_strength(self, amount: int) -> None:
        """Modify relationship strength."""
        self.strength = max(-100, min(100, self.strength + amount))
        self.history.append(f"Strength changed by {amount}")
    
    def modify_trust(self, amount: int) -> None:
        """Modify trust level."""
        self.trust = max(0, min(100, self.trust + amount))
        self.history.append(f"Trust changed by {amount}")


class RelationshipManager:
    """Manages relationships between NPCs."""
    
    def __init__(self):
        self.relationships: Dict[tuple, Relationship] = {}
    
    def _get_key(self, char1_id: str, char2_id: str) -> tuple:
        """Get consistent key for relationship lookup."""
        return tuple(sorted([char1_id, char2_id]))
    
    def create_relationship(
        self,
        char1_id: str,
        char2_id: str,
        rel_type: RelationshipType,
        strength: int = 0
    ) -> Relationship:
        """Create a new relationship."""
        key = self._get_key(char1_id, char2_id)
        relationship = Relationship(
            character1_id=char1_id,
            character2_id=char2_id,
            relationship_type=rel_type,
            strength=strength
        )
        self.relationships[key] = relationship
        return relationship
    
    def get_relationship(self, char1_id: str, char2_id: str) -> Optional[Relationship]:
        """Get relationship between two characters."""
        key = self._get_key(char1_id, char2_id)
        return self.relationships.get(key)
    
    def update_relationship(
        self,
        char1_id: str,
        char2_id: str,
        strength_change: int = 0,
        trust_change: int = 0
    ) -> bool:
        """Update an existing relationship."""
        relationship = self.get_relationship(char1_id, char2_id)
        if not relationship:
            return False
        
        if strength_change:
            relationship.modify_strength(strength_change)
        if trust_change:
            relationship.modify_trust(trust_change)
        
        return True
    
    def get_all_relationships(self, character_id: str) -> List[Relationship]:
        """Get all relationships for a character."""
        return [
            rel for key, rel in self.relationships.items()
            if character_id in key
        ]
    
    def get_friends(self, character_id: str) -> List[str]:
        """Get all friends of a character."""
        relationships = self.get_all_relationships(character_id)
        friends = []
        for rel in relationships:
            if rel.relationship_type == RelationshipType.FRIEND:
                other_id = (
                    rel.character2_id if rel.character1_id == character_id
                    else rel.character1_id
                )
                friends.append(other_id)
        return friends
    
    def get_enemies(self, character_id: str) -> List[str]:
        """Get all enemies of a character."""
        relationships = self.get_all_relationships(character_id)
        enemies = []
        for rel in relationships:
            if rel.relationship_type == RelationshipType.ENEMY:
                other_id = (
                    rel.character2_id if rel.character1_id == character_id
                    else rel.character1_id
                )
                enemies.append(other_id)
        return enemies


# In the real codebase, this file continues for 626 lines
# with more complex relationship dynamics, opinion systems, etc.
# ⚠️ THIS IS AN EXACT DUPLICATE - 100% CODE DUPLICATION!
