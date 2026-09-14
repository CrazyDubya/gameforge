"""
Quest Difficulty Analyzer Module

Analyzes and adjusts quest difficulty based on various factors.
"""

from typing import Dict, Any
from .templates import QuestDifficulty


class QuestDifficultyAnalyzer:
    """Analyzes and adjusts quest difficulty"""
    
    def __init__(self):
        self.difficulty_factors = {
            "player_level": 0.4,
            "quest_complexity": 0.3,
            "reward_value": 0.2,
            "time_estimate": 0.1
        }
    
    def analyze_difficulty(self, quest: Dict[str, Any], player_level: int) -> float:
        """
        Analyze actual difficulty of a quest.
        
        Args:
            quest: Quest dictionary to analyze
            player_level: Current player level
            
        Returns:
            Difficulty score from 0-100
        """
        score = 0.0
        
        # Factor 1: Level appropriateness
        quest_difficulty = quest.get("difficulty", QuestDifficulty.MEDIUM)
        difficulty_values = {
            QuestDifficulty.TRIVIAL: 10,
            QuestDifficulty.EASY: 25,
            QuestDifficulty.MEDIUM: 50,
            QuestDifficulty.HARD: 75,
            QuestDifficulty.EPIC: 100
        }
        score += difficulty_values[quest_difficulty] * self.difficulty_factors["player_level"]
        
        # Factor 2: Quest complexity (number of objectives)
        objectives = quest.get("objectives", [])
        complexity_score = min(len(objectives) * 10, 100)
        score += complexity_score * self.difficulty_factors["quest_complexity"]
        
        # Factor 3: Reward value
        rewards = quest.get("rewards")
        if rewards:
            reward_score = min((rewards.gold / 100) + (rewards.experience / 500), 100)
            score += reward_score * self.difficulty_factors["reward_value"]
        
        # Factor 4: Estimated time
        time_score = len(objectives) * 15  # 15 points per objective
        score += min(time_score, 100) * self.difficulty_factors["time_estimate"]
        
        return min(score, 100.0)
    
    def suggest_difficulty_adjustment(
        self,
        quest: Dict[str, Any],
        player_level: int,
        target_difficulty: QuestDifficulty
    ) -> Dict[str, Any]:
        """
        Suggest adjustments to reach target difficulty.
        
        Args:
            quest: Quest to analyze
            player_level: Current player level
            target_difficulty: Desired difficulty level
            
        Returns:
            Dictionary with suggestions for adjustments
        """
        current_score = self.analyze_difficulty(quest, player_level)
        target_scores = {
            QuestDifficulty.TRIVIAL: 10,
            QuestDifficulty.EASY: 25,
            QuestDifficulty.MEDIUM: 50,
            QuestDifficulty.HARD: 75,
            QuestDifficulty.EPIC: 95
        }
        target_score = target_scores[target_difficulty]
        
        suggestions = {
            "current_score": current_score,
            "target_score": target_score,
            "adjustments": []
        }
        
        if current_score < target_score:
            suggestions["adjustments"].append("Increase number of objectives")
            suggestions["adjustments"].append("Add more challenging monsters")
            suggestions["adjustments"].append("Increase reward values")
        elif current_score > target_score:
            suggestions["adjustments"].append("Reduce number of objectives")
            suggestions["adjustments"].append("Simplify quest requirements")
            suggestions["adjustments"].append("Decrease reward values")
        else:
            suggestions["adjustments"].append("No adjustment needed")
        
        return suggestions
