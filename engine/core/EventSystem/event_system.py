from typing import Callable, List, Dict
from .event import Event, EventType

class EventSystem:
    """
    Engine-level event dispatch system.
    Completely independent - other systems register listeners.
    """
    def __init__(self):
        # Map event type -> list of listener callbacks
        self.listeners: Dict[EventType, List[Callable[[Event], None]]] = {}
        
        # Hooks for event lifecycle
        self.on_event_dispatched: Callable[[Event], None] = None
        self.on_event_received: Callable[[Event], None] = None

    def register_listener(self, event_type: EventType, callback: Callable[[Event], None]):
        """
        Register a listener for a specific event type.
        """
        if event_type not in self.listeners:
            self.listeners[event_type] = []
        self.listeners[event_type].append(callback)

    def unregister_listener(self, event_type: EventType, callback: Callable[[Event], None]):
        """
        Unregister a listener for a specific event type.
        """
        if event_type in self.listeners:
            self.listeners[event_type] = [
                listener for listener in self.listeners[event_type]
                if listener != callback
            ]

    def dispatch_event(self, event: Event):
        """
        Dispatch an event to all registered listeners for that event type.
        """
        if self.on_event_dispatched:
            self.on_event_dispatched(event)
        
        # Call listeners for this specific event type
        if event.type in self.listeners:
            for listener in self.listeners[event.type]:
                listener(event)
                if self.on_event_received:
                    self.on_event_received(event)

    def clear_listeners(self, event_type: EventType = None):
        """
        Clear all listeners for a specific event type, or all listeners if None.
        """
        if event_type is None:
            self.listeners.clear()
        elif event_type in self.listeners:
            self.listeners[event_type].clear()

    def get_listener_count(self, event_type: EventType) -> int:
        """
        Get the number of listeners for an event type.
        """
        return len(self.listeners.get(event_type, []))
