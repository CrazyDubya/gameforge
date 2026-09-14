"""
NPC Schedules System - DUPLICATE in npc_modules directory

⚠️ WARNING: This is a DUPLICATE of core/npc_systems/schedules.py
This is a simplified example showing the duplication issue.
In the actual codebase, this file contains 867 lines.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import time


class SchedulePriority(Enum):
    """Priority levels for scheduled activities."""
    CRITICAL = 1
    HIGH = 2
    MEDIUM = 3
    LOW = 4


class ActivityType(Enum):
    """Types of activities NPCs can perform."""
    WORK = "work"
    SLEEP = "sleep"
    EAT = "eat"
    SOCIALIZE = "socialize"
    PATROL = "patrol"
    GUARD = "guard"
    TRAVEL = "travel"
    LEISURE = "leisure"


@dataclass
class ScheduledActivity:
    """Represents a scheduled activity for an NPC."""
    name: str
    activity_type: ActivityType
    start_time: time
    end_time: time
    location: str
    priority: SchedulePriority = SchedulePriority.MEDIUM
    is_flexible: bool = False
    conditions: List[str] = None
    
    def __post_init__(self):
        if self.conditions is None:
            self.conditions = []


class Schedule:
    """Represents an NPC's daily schedule."""
    
    def __init__(self, npc_id: str):
        self.npc_id = npc_id
        self.activities: List[ScheduledActivity] = []
        self.current_activity: Optional[ScheduledActivity] = None
    
    def add_activity(self, activity: ScheduledActivity) -> None:
        """Add an activity to the schedule."""
        self.activities.append(activity)
        self.activities.sort(key=lambda a: a.start_time)
    
    def remove_activity(self, activity_name: str) -> bool:
        """Remove an activity from the schedule."""
        for i, activity in enumerate(self.activities):
            if activity.name == activity_name:
                self.activities.pop(i)
                return True
        return False
    
    def get_activity_at_time(self, current_time: time) -> Optional[ScheduledActivity]:
        """Get the activity that should be happening at the given time."""
        for activity in self.activities:
            if activity.start_time <= current_time < activity.end_time:
                return activity
        return None
    
    def get_next_activity(self, current_time: time) -> Optional[ScheduledActivity]:
        """Get the next activity after the current time."""
        for activity in self.activities:
            if activity.start_time > current_time:
                return activity
        return None


class ScheduleManager:
    """Manages schedules for all NPCs."""
    
    def __init__(self):
        self.schedules: Dict[str, Schedule] = {}
    
    def create_schedule(self, npc_id: str) -> Schedule:
        """Create a new schedule for an NPC."""
        schedule = Schedule(npc_id)
        self.schedules[npc_id] = schedule
        return schedule
    
    def get_schedule(self, npc_id: str) -> Optional[Schedule]:
        """Get the schedule for an NPC."""
        return self.schedules.get(npc_id)
    
    def update_current_activities(self, current_time: time) -> None:
        """Update current activities for all NPCs based on time."""
        for schedule in self.schedules.values():
            schedule.current_activity = schedule.get_activity_at_time(current_time)
    
    def get_npcs_at_location(self, location: str, current_time: time) -> List[str]:
        """Get all NPCs that should be at a given location at the current time."""
        npcs = []
        for npc_id, schedule in self.schedules.items():
            activity = schedule.get_activity_at_time(current_time)
            if activity and activity.location == location:
                npcs.append(npc_id)
        return npcs


# In the real codebase, this file continues for 867 lines
# with more complex scheduling algorithms, conflict resolution, etc.
# ⚠️ THIS IS AN EXACT DUPLICATE - 100% CODE DUPLICATION!
