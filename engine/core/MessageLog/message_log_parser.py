from typing import Callable, List
from .message import Message, MessageType, MessageFlags
from .message_log_system import MessageLogSystem

class MessageLogParser:
    """
    Game-facing API for MessageLogSystem.
    Completely independent - game code logs messages.
    """
    def __init__(self, max_messages: int = 1000):
        self.system = MessageLogSystem(max_messages)

    # -------------------
    # Message Commands
    # -------------------
    def log(self, text: str, message_type: MessageType = MessageType.INFO, flags: MessageFlags = MessageFlags.NONE):
        """
        Log a message to the message log.
        """
        message = Message(text, message_type, flags)
        self.system.add_message(message)
        return message

    def log_info(self, text: str):
        """Log an info message."""
        return self.log(text, MessageType.INFO)

    def log_warning(self, text: str):
        """Log a warning message."""
        return self.log(text, MessageType.WARNING)

    def log_error(self, text: str):
        """Log an error message."""
        return self.log(text, MessageType.ERROR)

    def log_debug(self, text: str):
        """Log a debug message."""
        return self.log(text, MessageType.DEBUG)

    def log_game_event(self, text: str, flags: MessageFlags = MessageFlags.NONE):
        """Log a game event message."""
        return self.log(text, MessageType.GAME_EVENT, flags)

    # -------------------
    # Message Queries
    # -------------------
    def get_messages(self, message_type: MessageType = None, limit: int = None) -> List[Message]:
        """
        Get messages, optionally filtered by type and limited.
        """
        return self.system.get_messages(message_type, limit)

    def get_latest_message(self) -> Message:
        """
        Get the most recent message.
        """
        return self.system.get_latest_message()

    def get_recent_messages(self, limit: int = 10) -> List[Message]:
        """
        Get the most recent N messages.
        """
        return self.system.get_messages(limit=limit)

    def get_message_count(self) -> int:
        """
        Get the total number of messages in the log.
        """
        return self.system.get_message_count()

    def get_message_count_by_type(self, message_type: MessageType) -> int:
        """
        Get the count of messages of a specific type.
        """
        return self.system.get_message_count_by_type(message_type)

    # -------------------
    # Message Management
    # -------------------
    def clear_messages(self):
        """
        Clear all messages from the log.
        """
        self.system.clear_messages()

    # -------------------
    # Hooks
    # -------------------
    def set_message_added_hook(self, hook: Callable[[Message], None]):
        """
        Hook called when a message is added to the log.
        """
        self.system.on_message_added = hook

    def set_cleared_hook(self, hook: Callable[[], None]):
        """
        Hook called when the message log is cleared.
        """
        self.system.on_message_cleared = hook
