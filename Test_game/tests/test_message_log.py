import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.MessageLog.message_log_parser import MessageLogParser
from engine.core.MessageLog.message import MessageType, MessageFlags

def test_message_log_system():
    clock = EngineClock()
    clock.start()

    parser = MessageLogParser(max_messages=100)

    # Test hooks
    messages_added = []
    cleared_count = [0]

    # -----------------------------
    # Hooks for debugging
    # -----------------------------
    parser.set_message_added_hook(lambda m: messages_added.append(m))
    parser.set_cleared_hook(lambda: cleared_count.__setitem__(0, cleared_count[0] + 1))

    # -----------------------------
    # Test 1: Log Info Messages
    # -----------------------------
    print("Test 1: Log Info Messages...")
    parser.log_info("Game started")
    parser.log_info("Player entered the arena")
    assert parser.get_message_count() == 2
    assert len(messages_added) == 2
    print("OKAY")

    # -----------------------------
    # Test 2: Log Different Message Types
    # -----------------------------
    print("Test 2: Log Different Message Types...")
    parser.log_warning("Low health warning")
    parser.log_error("Critical error occurred")
    parser.log_debug("Debug: Player position (5, 10)")
    assert parser.get_message_count() == 5
    assert parser.get_message_count_by_type(MessageType.WARNING) == 1
    assert parser.get_message_count_by_type(MessageType.ERROR) == 1
    assert parser.get_message_count_by_type(MessageType.DEBUG) == 1
    print("OKAY")

    # -----------------------------
    # Test 3: Log Game Events
    # -----------------------------
    print("Test 3: Log Game Events...")
    parser.log_game_event("Player attacked Goblin for 20 damage")
    parser.log_game_event("Goblin defeated", MessageFlags.IMPORTANT)
    assert parser.get_message_count_by_type(MessageType.GAME_EVENT) == 2
    print("OKAY")

    # -----------------------------
    # Test 4: Get Latest Message
    # -----------------------------
    print("Test 4: Get Latest Message...")
    latest = parser.get_latest_message()
    assert latest is not None
    assert "defeated" in latest.text
    print("OKAY")

    # -----------------------------
    # Test 5: Get Recent Messages
    # -----------------------------
    print("Test 5: Get Recent Messages...")
    recent = parser.get_recent_messages(limit=3)
    assert len(recent) == 3
    print("OKAY")

    # -----------------------------
    # Test 6: Filter Messages by Type
    # -----------------------------
    print("Test 6: Filter Messages by Type...")
    info_messages = parser.get_messages(MessageType.INFO)
    assert len(info_messages) == 2
    game_events = parser.get_messages(MessageType.GAME_EVENT)
    assert len(game_events) == 2
    print("OKAY")

    # -----------------------------
    # Test 7: Get Messages with Limit
    # -----------------------------
    print("Test 7: Get Messages with Limit...")
    limited = parser.get_messages(limit=2)
    assert len(limited) == 2
    print("OKAY")

    # -----------------------------
    # Test 8: Message Flags
    # -----------------------------
    print("Test 8: Message Flags...")
    important_msg = parser.log_game_event("Important announcement", MessageFlags.IMPORTANT | MessageFlags.SYSTEM)
    assert important_msg.flags & MessageFlags.IMPORTANT
    assert important_msg.flags & MessageFlags.SYSTEM
    print("OKAY")

    # -----------------------------
    # Test 9: Clear Messages
    # -----------------------------
    print("Test 9: Clear Messages...")
    count_before = parser.get_message_count()
    assert count_before > 0
    parser.clear_messages()
    assert parser.get_message_count() == 0
    assert cleared_count[0] == 1
    print("OKAY")

    # -----------------------------
    # Test 10: Max Messages Constraint
    # -----------------------------
    print("Test 10: Max Messages Constraint...")
    # Create parser with small max
    small_parser = MessageLogParser(max_messages=5)
    for i in range(10):
        small_parser.log_info(f"Message {i}")
    # Should only keep the last 5
    assert small_parser.get_message_count() == 5
    recent_msgs = small_parser.get_recent_messages(limit=5)
    assert "Message 9" in recent_msgs[-1].text
    print("OKAY")

    # -----------------------------
    # Test 11: Message Serialization
    # -----------------------------
    print("Test 11: Message Serialization...")
    parser.clear_messages()
    msg = parser.log_game_event("Serialization test", MessageFlags.IMPORTANT)
    msg_dict = msg.to_dict()
    assert msg_dict["text"] == "Serialization test"
    assert msg_dict["type"] == "GAME_EVENT"
    
    # Test deserialization
    from engine.core.MessageLog.message import Message
    restored = Message.from_dict(msg_dict)
    assert restored.text == msg.text
    assert restored.type == msg.type
    assert restored.flags == msg.flags
    print("OKAY")

    # -----------------------------
    # Test 12: Complex Logging Scenario
    # -----------------------------
    print("Test 12: Complex Logging Scenario...")
    parser.clear_messages()
    parser.log_info("Dungeon entered")
    parser.log_game_event("Combat started", MessageFlags.IMPORTANT)
    parser.log_debug("Player HP: 100, Enemy HP: 50")
    parser.log_game_event("Player used Fireball - 30 damage")
    parser.log_game_event("Enemy defeated", MessageFlags.IMPORTANT)
    parser.log_info("Dungeon cleared")
    
    assert parser.get_message_count() == 6
    assert parser.get_message_count_by_type(MessageType.INFO) == 2
    assert parser.get_message_count_by_type(MessageType.GAME_EVENT) == 3
    assert parser.get_message_count_by_type(MessageType.DEBUG) == 1
    print("OKAY")

    # -----------------------------
    # Timing Report
    # -----------------------------
    clock.tick()
    print(f"All message log tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_message_log_system()
