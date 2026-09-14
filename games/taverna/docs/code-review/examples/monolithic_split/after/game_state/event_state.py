"""
Event State Module - Focused on event management only

This module handles all event-related state and operations.
Part of the game_state.py refactoring (P0 Issue #2).
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class GameEvent:
    """Represents a game event."""
    event_id: str
    event_type: str
    timestamp: datetime
    data: Dict[str, Any] = field(default_factory=dict)
    processed: bool = False


class EventManager:
    """Manages game events."""
    
    def __init__(self):
        self.events: List[GameEvent] = []
        self.event_queue: List[GameEvent] = []
        self.event_handlers: Dict[str, List] = {}
    
    def add_event(self, event: GameEvent) -> None:
        """Add an event to history."""
        self.events.append(event)
    
    def queue_event(self, event: GameEvent) -> None:
        """Queue an event for processing."""
        self.event_queue.append(event)
    
    def process_events(self) -> List[GameEvent]:
        """Process all queued events."""
        processed = []
        while self.event_queue:
            event = self.event_queue.pop(0)
            event.processed = True
            self.add_event(event)
            processed.append(event)
            
            # Call handlers for this event type
            if event.event_type in self.event_handlers:
                for handler in self.event_handlers[event.event_type]:
                    handler(event)
        
        return processed
    
    def register_handler(self, event_type: str, handler) -> None:
        """Register a handler for a specific event type."""
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)
    
    def get_events_by_type(self, event_type: str) -> List[GameEvent]:
        """Get all events of a specific type."""
        return [e for e in self.events if e.event_type == event_type]
    
    def get_recent_events(self, count: int = 10) -> List[GameEvent]:
        """Get the most recent events."""
        return self.events[-count:]
    
    def clear_old_events(self, keep_count: int = 1000) -> None:
        """Clear old events, keeping only the most recent."""
        if len(self.events) > keep_count:
            self.events = self.events[-keep_count:]


# ✅ FOCUSED MODULE - Only event-related functionality
# ✅ Easy to test, maintain, and understand
