"""
NPC Interactions System - DUPLICATE in npc_systems directory

This is a simplified example showing the duplication issue.
In the actual codebase, this file contains 669 lines.
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from enum import Enum


class InteractionType(Enum):
    """Types of interactions between NPCs and player."""
    CONVERSATION = "conversation"
    TRADE = "trade"
    COMBAT = "combat"
    QUEST = "quest"
    GIFT = "gift"
    HELP = "help"
    THREATEN = "threaten"


class InteractionOutcome(Enum):
    """Possible outcomes of an interaction."""
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"
    REJECTED = "rejected"


@dataclass
class Interaction:
    """Represents an interaction between NPCs or player and NPC."""
    interaction_id: str
    interaction_type: InteractionType
    initiator_id: str
    target_id: str
    outcome: InteractionOutcome = InteractionOutcome.SUCCESS
    dialogue: List[str] = field(default_factory=list)
    items_exchanged: Dict[str, int] = field(default_factory=dict)
    relationship_change: int = 0
    
    def add_dialogue(self, speaker: str, text: str) -> None:
        """Add dialogue to the interaction."""
        self.dialogue.append(f"{speaker}: {text}")
    
    def exchange_item(self, item_name: str, quantity: int) -> None:
        """Record an item exchange."""
        self.items_exchanged[item_name] = quantity


class InteractionManager:
    """Manages interactions between characters."""
    
    def __init__(self):
        self.interactions: Dict[str, Interaction] = {}
        self.interaction_history: List[Interaction] = []
        self.blocked_interactions: Set[tuple] = set()
    
    def create_interaction(
        self, 
        interaction_type: InteractionType,
        initiator_id: str,
        target_id: str
    ) -> Optional[Interaction]:
        """Create a new interaction."""
        # Check if interaction is blocked
        if (initiator_id, target_id) in self.blocked_interactions:
            return None
        
        interaction_id = f"{initiator_id}_{target_id}_{len(self.interaction_history)}"
        interaction = Interaction(
            interaction_id=interaction_id,
            interaction_type=interaction_type,
            initiator_id=initiator_id,
            target_id=target_id
        )
        
        self.interactions[interaction_id] = interaction
        return interaction
    
    def complete_interaction(self, interaction_id: str) -> bool:
        """Complete an interaction and add to history."""
        interaction = self.interactions.get(interaction_id)
        if not interaction:
            return False
        
        self.interaction_history.append(interaction)
        del self.interactions[interaction_id]
        return True
    
    def block_interaction(self, initiator_id: str, target_id: str) -> None:
        """Block interactions between two characters."""
        self.blocked_interactions.add((initiator_id, target_id))
    
    def unblock_interaction(self, initiator_id: str, target_id: str) -> None:
        """Unblock interactions between two characters."""
        self.blocked_interactions.discard((initiator_id, target_id))
    
    def get_interaction_history(
        self, 
        character_id: str,
        interaction_type: Optional[InteractionType] = None
    ) -> List[Interaction]:
        """Get interaction history for a character."""
        history = [
            i for i in self.interaction_history
            if i.initiator_id == character_id or i.target_id == character_id
        ]
        
        if interaction_type:
            history = [i for i in history if i.interaction_type == interaction_type]
        
        return history
    
    def get_recent_interactions(self, count: int = 10) -> List[Interaction]:
        """Get the most recent interactions."""
        return self.interaction_history[-count:]


# In the real codebase, this file continues for 669 lines
# with more complex interaction logic, dialogue systems, etc.
