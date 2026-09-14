"""
Quest Validator Module

Validates quest configurations and requirements.
"""

from typing import Dict, List, Any
from .templates import QuestDifficulty
from .rewards import QuestReward


class QuestValidator:
    """Validates quest configurations and requirements"""
    
    def __init__(self):
        self.validation_rules = []
    
    def validate_quest_structure(self, quest: Dict[str, Any]) -> bool:
        """
        Validate quest has required fields.
        
        Args:
            quest: Quest dictionary to validate
            
        Returns:
            True if quest structure is valid
        """
        required_fields = ["title", "description", "objectives", "rewards"]
        return all(field in quest for field in required_fields)
    
    def validate_objectives(self, objectives: List[str]) -> bool:
        """
        Validate quest objectives are achievable.
        
        Args:
            objectives: List of quest objectives
            
        Returns:
            True if objectives are valid
        """
        if not objectives:
            return False
        if len(objectives) > 10:
            return False
        return True
    
    def validate_rewards(self, rewards: QuestReward, difficulty: QuestDifficulty) -> bool:
        """
        Validate rewards are appropriate for difficulty.
        
        Args:
            rewards: Quest reward structure
            difficulty: Quest difficulty level
            
        Returns:
            True if rewards match difficulty
        """
        min_gold = {
            "trivial": 10,
            "easy": 50,
            "medium": 200,
            "hard": 500,
            "epic": 2000
        }
        return rewards.gold >= min_gold.get(difficulty.value, 0)
    
    def validate_level_requirements(self, min_level: int, max_level: int) -> bool:
        """
        Validate level requirements make sense.
        
        Args:
            min_level: Minimum player level
            max_level: Maximum player level
            
        Returns:
            True if level requirements are valid
        """
        return 1 <= min_level <= max_level <= 100
