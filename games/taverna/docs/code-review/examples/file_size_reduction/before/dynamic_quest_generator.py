"""
Dynamic Quest Generator - Monolithic Implementation

This file demonstrates a large module (909 lines simulated with 200+ lines demo)
that should be split into smaller, focused modules.

Status: 🔴 TOO LARGE - Needs refactoring
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional, Any
import random


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
class QuestReward:
    """Reward for completing a quest"""
    gold: int
    experience: int
    items: List[str]
    reputation: Dict[str, int]


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


class QuestValidator:
    """Validates quest configurations and requirements"""
    
    def __init__(self):
        self.validation_rules = []
    
    def validate_quest_structure(self, quest: Dict[str, Any]) -> bool:
        """Validate quest has required fields"""
        required_fields = ["title", "description", "objectives", "rewards"]
        return all(field in quest for field in required_fields)
    
    def validate_objectives(self, objectives: List[str]) -> bool:
        """Validate quest objectives are achievable"""
        if not objectives:
            return False
        if len(objectives) > 10:
            return False
        return True
    
    def validate_rewards(self, rewards: QuestReward, difficulty: QuestDifficulty) -> bool:
        """Validate rewards are appropriate for difficulty"""
        min_gold = {"trivial": 10, "easy": 50, "medium": 200, "hard": 500, "epic": 2000}
        return rewards.gold >= min_gold.get(difficulty.value, 0)
    
    def validate_level_requirements(self, min_level: int, max_level: int) -> bool:
        """Validate level requirements make sense"""
        return 1 <= min_level <= max_level <= 100


class QuestGenerator:
    """Main quest generation engine"""
    
    def __init__(self):
        self.templates: List[QuestTemplate] = []
        self.validator = QuestValidator()
        self.generated_quests: List[Dict] = []
    
    def add_template(self, template: QuestTemplate):
        """Add a quest template"""
        self.templates.append(template)
    
    def generate_quest(
        self,
        player_level: int,
        quest_type: Optional[QuestType] = None,
        difficulty: Optional[QuestDifficulty] = None
    ) -> Optional[Dict[str, Any]]:
        """Generate a quest for the player"""
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
            "rewards": self._calculate_rewards(template.difficulty, player_level)
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
    
    def _calculate_rewards(self, difficulty: QuestDifficulty, player_level: int) -> QuestReward:
        """Calculate rewards for quest"""
        base_gold = {
            QuestDifficulty.TRIVIAL: 10,
            QuestDifficulty.EASY: 50,
            QuestDifficulty.MEDIUM: 200,
            QuestDifficulty.HARD: 500,
            QuestDifficulty.EPIC: 2000
        }
        
        base_xp = {
            QuestDifficulty.TRIVIAL: 25,
            QuestDifficulty.EASY: 100,
            QuestDifficulty.MEDIUM: 500,
            QuestDifficulty.HARD: 2000,
            QuestDifficulty.EPIC: 10000
        }
        
        gold = int(base_gold[difficulty] * (1 + player_level * 0.1))
        xp = int(base_xp[difficulty] * (1 + player_level * 0.05))
        
        return QuestReward(
            gold=gold,
            experience=xp,
            items=self._generate_item_rewards(difficulty),
            reputation={"guild": 10 * (list(QuestDifficulty).index(difficulty) + 1)}
        )
    
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
        Analyze actual difficulty of a quest
        Returns difficulty score from 0-100
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
        """Suggest adjustments to reach target difficulty"""
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


# Example usage functions
def create_sample_templates() -> List[QuestTemplate]:
    """Create sample quest templates"""
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


def main():
    """Example usage of the quest generator"""
    generator = QuestGenerator()
    analyzer = QuestDifficultyAnalyzer()
    
    # Add templates
    for template in create_sample_templates():
        generator.add_template(template)
    
    # Generate a quest
    quest = generator.generate_quest(player_level=5)
    if quest:
        print(f"Generated Quest: {quest['title']}")
        print(f"Description: {quest['description']}")
        
        # Analyze difficulty
        difficulty_score = analyzer.analyze_difficulty(quest, player_level=5)
        print(f"Difficulty Score: {difficulty_score:.1f}/100")


if __name__ == "__main__":
    main()
