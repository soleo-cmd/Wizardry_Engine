from typing import Callable, List, Dict
from collections import deque
from .message import Message, MessageType

class MessageLogSystem:
    """
    Engine-level message logging system.
    Completely independent - stores and retrieves messages.
    """
    def __init__(self, max_messages: int = 1000):
        self.messages: deque = deque(maxlen=max_messages)
        self.max_messages = max_messages
        
        # Hooks
        self.on_message_added: Callable[[Message], None] = None
        self.on_message_cleared: Callable[[], None] = None

    def add_message(self, message: Message):
        """
        Add a message to the log.
        """
        self.messages.append(message)
        if self.on_message_added:
            self.on_message_added(message)

    def get_messages(self, message_type: MessageType = None, limit: int = None) -> List[Message]:
        """
        Get messages, optionally filtered by type and limited.
        """
        result = list(self.messages)
        
        if message_type:
            result = [m for m in result if m.type == message_type]
        
        if limit:
            result = result[-limit:]  # Get most recent N messages
        
        return result

    def get_latest_message(self) -> Message:
        """
        Get the most recent message.
        """
        return self.messages[-1] if self.messages else None

    def clear_messages(self):
        """
        Clear all messages from the log.
        """
        self.messages.clear()
        if self.on_message_cleared:
            self.on_message_cleared()

    def get_message_count(self) -> int:
        """
        Get the total number of messages in the log.
        """
        return len(self.messages)

    def get_message_count_by_type(self, message_type: MessageType) -> int:
        """
        Get the count of messages of a specific type.
        """
        return sum(1 for m in self.messages if m.type == message_type)
