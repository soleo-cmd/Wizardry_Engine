from typing import Callable
from .event import Event, EventType, EventFlags
from .event_system import EventSystem

class EventParser:
    """
    Game-facing API for EventSystem.
    Completely independent - game code registers listeners and dispatches events.
    """
    def __init__(self):
        self.system = EventSystem()

    # -------------------
    # Event Registration
    # -------------------
    def subscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """
        Subscribe to an event type.
        """
        self.system.register_listener(event_type, callback)

    def unsubscribe(self, event_type: EventType, callback: Callable[[Event], None]):
        """
        Unsubscribe from an event type.
        """
        self.system.unregister_listener(event_type, callback)

    # -------------------
    # Event Dispatch
    # -------------------
    def emit(self, name: str, event_type: EventType, data: dict = None, flags: EventFlags = EventFlags.NONE):
        """
        Create and dispatch an event.
        """
        event = Event(name, event_type, flags, data)
        self.system.dispatch_event(event)
        return event

    def emit_event(self, event: Event):
        """
        Dispatch an already-created event.
        """
        self.system.dispatch_event(event)

    # -------------------
    # Listener Management
    # -------------------
    def clear_listeners(self, event_type: EventType = None):
        """
        Clear listeners for a specific event type or all listeners.
        """
        self.system.clear_listeners(event_type)

    def get_listener_count(self, event_type: EventType) -> int:
        """
        Get the count of listeners for an event type.
        """
        return self.system.get_listener_count(event_type)

    # -------------------
    # Hooks
    # -------------------
    def set_dispatched_hook(self, hook: Callable[[Event], None]):
        """
        Hook called when an event is dispatched.
        """
        self.system.on_event_dispatched = hook

    def set_received_hook(self, hook: Callable[[Event], None]):
        """
        Hook called when a listener receives an event.
        """
        self.system.on_event_received = hook
