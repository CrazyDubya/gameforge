"""
Quest Rewards Module

Handles reward calculation and generation for quests.
"""

from dataclasses import dataclass
from typing import Dict, List
import random
from .templates import QuestDifficulty


@dataclass
class QuestReward:
    """Reward for completing a quest"""
    gold: int
    experience: int
    items: List[str]
    reputation: Dict[str, int]


class RewardCalculator:
    """Calculates appropriate rewards for quests"""
    
    def __init__(self):
        self.base_gold = {
            QuestDifficulty.TRIVIAL: 10,
            QuestDifficulty.EASY: 50,
            QuestDifficulty.MEDIUM: 200,
            QuestDifficulty.HARD: 500,
            QuestDifficulty.EPIC: 2000
        }
        
        self.base_xp = {
            QuestDifficulty.TRIVIAL: 25,
            QuestDifficulty.EASY: 100,
            QuestDifficulty.MEDIUM: 500,
            QuestDifficulty.HARD: 2000,
            QuestDifficulty.EPIC: 10000
        }
    
    def calculate_rewards(self, difficulty: QuestDifficulty, player_level: int) -> QuestReward:
        """
        Calculate rewards for quest based on difficulty and player level.
        
        Args:
            difficulty: Quest difficulty level
            player_level: Current player level
            
        Returns:
            QuestReward with calculated values
        """
        gold = int(self.base_gold[difficulty] * (1 + player_level * 0.1))
        xp = int(self.base_xp[difficulty] * (1 + player_level * 0.05))
        
        return QuestReward(
            gold=gold,
            experience=xp,
            items=self._generate_item_rewards(difficulty),
            reputation={"guild": 10 * (list(QuestDifficulty).index(difficulty) + 1)}
        )
    
    def _generate_item_rewards(self, difficulty: QuestDifficulty) -> List[str]:
        """Generate item rewards based on difficulty"""
        item_counts = {
            QuestDifficulty.TRIVIAL: 0,
            QuestDifficulty.EASY: 1,
            QuestDifficulty.MEDIUM: 2,
            QuestDifficulty.HARD: 3,
            QuestDifficulty.EPIC: 5
        }
        
        count = item_counts[difficulty]
        items = ["Health Potion", "Mana Potion", "Strength Elixir", "Magic Scroll", "Rare Gem"]
        return random.sample(items, min(count, len(items)))
