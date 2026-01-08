from enum import Enum, IntFlag
from datetime import datetime

class MessageType(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3
    DEBUG = 4
    GAME_EVENT = 5

class MessageFlags(IntFlag):
    NONE = 0
    IMPORTANT = 1
    SYSTEM = 2

class Message:
    """
    Engine-level message data.
    Used for logging and message display.
    """
    def __init__(self, text: str, message_type: MessageType, flags: MessageFlags = MessageFlags.NONE, timestamp: datetime = None):
        self.text = text
        self.type = message_type
        self.flags = flags
        self.timestamp = timestamp or datetime.now()
        self.id = id(self)  # Unique message ID

    def to_dict(self):
        return {
            "text": self.text,
            "type": self.type.name,
            "flags": self.flags.value,
            "timestamp": self.timestamp.isoformat()
        }

    @classmethod
    def from_dict(cls, data):
        message_type = MessageType[data["type"]]
        flags = MessageFlags(data["flags"])
        timestamp = datetime.fromisoformat(data["timestamp"])
        return cls(data["text"], message_type, flags, timestamp)

    def __repr__(self):
        return f"<Message {self.type.name}: {self.text[:50]}>"
