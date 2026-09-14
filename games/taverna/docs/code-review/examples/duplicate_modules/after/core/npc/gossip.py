"""
NPC Gossip System - Consolidated version

This is the consolidated version after refactoring.
No more duplication!
"""

from typing import List, Dict, Optional, Set
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class GossipType(Enum):
    """Types of gossip that can spread."""
    RUMOR = "rumor"
    NEWS = "news"
    SECRET = "secret"
    OPINION = "opinion"
    FACT = "fact"


@dataclass
class GossipItem:
    """Represents a piece of gossip."""
    gossip_id: str
    gossip_type: GossipType
    content: str
    source_id: str
    subject_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    credibility: float = 1.0  # 0.0 to 1.0
    spread_count: int = 0
    known_by: Set[str] = field(default_factory=set)
    
    def spread_to(self, character_id: str) -> None:
        """Record that a character learned this gossip."""
        if character_id not in self.known_by:
            self.known_by.add(character_id)
            self.spread_count += 1


class GossipSystem:
    """Manages the spread of gossip between NPCs."""
    
    def __init__(self):
        self.gossip_items: Dict[str, GossipItem] = {}
        self.gossip_history: List[GossipItem] = []
    
    def create_gossip(
        self,
        gossip_type: GossipType,
        content: str,
        source_id: str,
        subject_id: Optional[str] = None
    ) -> GossipItem:
        """Create a new piece of gossip."""
        gossip_id = f"gossip_{len(self.gossip_items)}"
        gossip = GossipItem(
            gossip_id=gossip_id,
            gossip_type=gossip_type,
            content=content,
            source_id=source_id,
            subject_id=subject_id
        )
        gossip.known_by.add(source_id)
        self.gossip_items[gossip_id] = gossip
        return gossip
    
    def spread_gossip(
        self,
        gossip_id: str,
        from_char_id: str,
        to_char_id: str
    ) -> bool:
        """Spread gossip from one character to another."""
        gossip = self.gossip_items.get(gossip_id)
        if not gossip:
            return False
        
        # Character must know the gossip to spread it
        if from_char_id not in gossip.known_by:
            return False
        
        gossip.spread_to(to_char_id)
        return True
    
    def get_gossip_known_by(self, character_id: str) -> List[GossipItem]:
        """Get all gossip known by a character."""
        return [
            gossip for gossip in self.gossip_items.values()
            if character_id in gossip.known_by
        ]
    
    def get_gossip_about(self, subject_id: str) -> List[GossipItem]:
        """Get all gossip about a specific character."""
        return [
            gossip for gossip in self.gossip_items.values()
            if gossip.subject_id == subject_id
        ]
    
    def get_most_spread_gossip(self, count: int = 10) -> List[GossipItem]:
        """Get the most widely spread gossip."""
        sorted_gossip = sorted(
            self.gossip_items.values(),
            key=lambda g: g.spread_count,
            reverse=True
        )
        return sorted_gossip[:count]
    
    def modify_credibility(self, gossip_id: str, change: float) -> bool:
        """Modify the credibility of a gossip item."""
        gossip = self.gossip_items.get(gossip_id)
        if not gossip:
            return False
        
        gossip.credibility = max(0.0, min(1.0, gossip.credibility + change))
        return True
    
    def archive_old_gossip(self, max_age_days: int = 30) -> int:
        """Archive gossip older than specified days."""
        now = datetime.now()
        archived = 0
        
        for gossip_id, gossip in list(self.gossip_items.items()):
            age_days = (now - gossip.timestamp).days
            if age_days > max_age_days:
                self.gossip_history.append(gossip)
                del self.gossip_items[gossip_id]
                archived += 1
        
        return archived


# In the real codebase, this file continues for 638 lines
# with more complex gossip spreading algorithms, reputation effects, etc.
# ✅ SINGLE SOURCE OF TRUTH - No duplication!
