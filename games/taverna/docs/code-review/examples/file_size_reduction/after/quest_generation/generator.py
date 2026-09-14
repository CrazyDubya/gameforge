"""
Quest Generator Module

Main quest generation engine that coordinates all components.
"""

from typing import Dict, List, Optional, Any
import random
from .templates import QuestTemplate, QuestType, QuestDifficulty
from .validator import QuestValidator
from .rewards import RewardCalculator


class QuestGenerator:
    """Main quest generation engine"""
    
    def __init__(self):
        self.templates: List[QuestTemplate] = []
        self.validator = QuestValidator()
        self.reward_calculator = RewardCalculator()
        self.generated_quests: List[Dict] = []
    
    def add_template(self, template: QuestTemplate):
        """Add a quest template to the generator"""
        self.templates.append(template)
    
    def generate_quest(
        self,
        player_level: int,
        quest_type: Optional[QuestType] = None,
        difficulty: Optional[QuestDifficulty] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Generate a quest for the player.
        
        Args:
            player_level: Current player level
            quest_type: Optional specific quest type
            difficulty: Optional specific difficulty
            
        Returns:
            Generated quest dictionary or None if no valid template
        """
        # Filter templates by player level
        valid_templates = [
            t for t in self.templates
            if t.is_valid_for_level(player_level)
        ]
        
        # Filter by quest type if specified
        if quest_type:
            valid_templates = [t for t in valid_templates if t.quest_type == quest_type]
        
        # Filter by difficulty if specified
        if difficulty:
            valid_templates = [t for t in valid_templates if t.difficulty == difficulty]
        
        if not valid_templates:
            return None
        
        # Select random template
        template = random.choice(valid_templates)
        
        # Generate quest from template
        context = self._create_context(player_level, template)
        quest = {
            "title": template.generate_title(context),
            "description": template.generate_description(context),
            "objectives": template.objectives,
            "difficulty": template.difficulty,
            "rewards": self.reward_calculator.calculate_rewards(template.difficulty, player_level)
        }
        
        # Validate quest
        if not self.validator.validate_quest_structure(quest):
            return None
        
        self.generated_quests.append(quest)
        return quest
    
    def _create_context(self, player_level: int, template: QuestTemplate) -> Dict[str, Any]:
        """Create context for quest generation"""
        return {
            "player_level": player_level,
            "difficulty": template.difficulty.value,
            "location": self._get_random_location(),
            "npc_name": self._get_random_npc_name(),
            "item_name": self._get_random_item(),
            "monster_name": self._get_random_monster()
        }
    
    def _get_random_location(self) -> str:
        """Get random location name"""
        locations = ["Dark Forest", "Mountain Peak", "Ancient Ruins", "Misty Swamp"]
        return random.choice(locations)
    
    def _get_random_npc_name(self) -> str:
        """Get random NPC name"""
        names = ["Eldric", "Morgana", "Theron", "Lyra"]
        return random.choice(names)
    
    def _get_random_item(self) -> str:
        """Get random item name"""
        items = ["Ancient Scroll", "Magic Crystal", "Golden Chalice", "Enchanted Sword"]
        return random.choice(items)
    
    def _get_random_monster(self) -> str:
        """Get random monster name"""
        monsters = ["Goblin", "Dragon", "Skeleton", "Demon"]
        return random.choice(monsters)
