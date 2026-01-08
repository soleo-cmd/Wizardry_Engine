from enum import Enum, IntFlag

class EventType(Enum):
    ENTITY_SPAWNED = 1
    ENTITY_REMOVED = 2
    ENTITY_MOVED = 3
    ENTITY_DAMAGED = 4
    ENTITY_HEALED = 5
    ACTION_EXECUTED = 6
    STATE_CHANGED = 7
    TURN_STARTED = 8
    TURN_ENDED = 9
    CUSTOM = 10

class EventFlags(IntFlag):
    NONE = 0
    BLOCKING = 1
    CRITICAL = 2

class Event:
    """
    Engine-level event data.
    Used for game-wide event dispatch.
    """
    def __init__(self, name: str, event_type: EventType, flags: EventFlags = EventFlags.NONE, data: dict = None):
        self.name = name
        self.type = event_type
        self.flags = flags
        self.data = data or {}

    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.name,
            "flags": self.flags.value,
            "data": self.data
        }

    @classmethod
    def from_dict(cls, data):
        event_type = EventType[data["type"]]
        flags = EventFlags(data["flags"])
        return cls(data["name"], event_type, flags, data.get("data", {}))

    def __repr__(self):
        return f"<Event {self.name}, Type: {self.type.name}, Flags: {self.flags}>"
