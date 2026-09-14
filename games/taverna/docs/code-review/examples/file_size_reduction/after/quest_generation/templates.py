"""
Quest Templates Module

Defines quest templates and related enums for quest generation.
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Any


class QuestDifficulty(Enum):
    """Quest difficulty levels"""
    TRIVIAL = "trivial"
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
    EPIC = "epic"


class QuestType(Enum):
    """Types of quests"""
    FETCH = "fetch"
    KILL = "kill"
    ESCORT = "escort"
    INVESTIGATE = "investigate"
    CRAFT = "craft"


@dataclass
class QuestTemplate:
    """Template for generating quests"""
    quest_type: QuestType
    difficulty: QuestDifficulty
    title_template: str
    description_template: str
    objectives: List[str]
    min_level: int
    max_level: int
    
    def generate_title(self, context: Dict[str, Any]) -> str:
        """Generate quest title from template"""
        return self.title_template.format(**context)
    
    def generate_description(self, context: Dict[str, Any]) -> str:
        """Generate quest description from template"""
        return self.description_template.format(**context)
    
    def is_valid_for_level(self, player_level: int) -> bool:
        """Check if quest is valid for player level"""
        return self.min_level <= player_level <= self.max_level


def create_sample_templates() -> List[QuestTemplate]:
    """Create sample quest templates for demonstration"""
    templates = [
        QuestTemplate(
            quest_type=QuestType.FETCH,
            difficulty=QuestDifficulty.EASY,
            title_template="Fetch {item_name} from {location}",
            description_template="{npc_name} needs you to retrieve {item_name} from {location}.",
            objectives=["Travel to {location}", "Find {item_name}", "Return to {npc_name}"],
            min_level=1,
            max_level=10
        ),
        QuestTemplate(
            quest_type=QuestType.KILL,
            difficulty=QuestDifficulty.MEDIUM,
            title_template="Defeat {monster_name} at {location}",
            description_template="A dangerous {monster_name} threatens {location}. Defeat it!",
            objectives=["Travel to {location}", "Defeat {monster_name}", "Report victory"],
            min_level=10,
            max_level=25
        )
    ]
    return templates
