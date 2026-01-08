import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.EventSystem.event_parser import EventParser
from engine.core.EventSystem.event import EventType, EventFlags

def test_event_system():
    clock = EngineClock()
    clock.start()

    parser = EventParser()

    # Test counter
    events_dispatched = []
    events_received = []

    # -----------------------------
    # Hooks for debugging
    # -----------------------------
    parser.set_dispatched_hook(lambda e: events_dispatched.append(e))
    parser.set_received_hook(lambda e: events_received.append(e))

    # Test handlers
    def on_entity_spawned(event):
        print(f"Handler: Entity spawned - {event.data}")

    def on_entity_moved(event):
        print(f"Handler: Entity moved to {event.data}")

    # -----------------------------
    # Test 1: Subscribe to Events
    # -----------------------------
    print("Test 1: Subscribe to Events...")
    parser.subscribe(EventType.ENTITY_SPAWNED, on_entity_spawned)
    parser.subscribe(EventType.ENTITY_MOVED, on_entity_moved)
    assert parser.get_listener_count(EventType.ENTITY_SPAWNED) == 1
    assert parser.get_listener_count(EventType.ENTITY_MOVED) == 1
    print("OKAY")

    # -----------------------------
    # Test 2: Emit Events
    # -----------------------------
    print("Test 2: Emit Events...")
    parser.emit("entity_spawned_1", EventType.ENTITY_SPAWNED, {"entity": "Hero", "position": (0, 0)})
    parser.emit("entity_moved_1", EventType.ENTITY_MOVED, {"entity": "Hero", "position": (1, 1)})
    assert len(events_dispatched) == 2
    assert len(events_received) == 2
    print("OKAY")

    # -----------------------------
    # Test 3: Emit with Flags
    # -----------------------------
    print("Test 3: Emit with Flags...")
    event = parser.emit(
        "critical_event",
        EventType.ACTION_EXECUTED,
        {"action": "critical_spell"},
        EventFlags.BLOCKING | EventFlags.CRITICAL
    )
    assert event.flags & EventFlags.BLOCKING
    assert event.flags & EventFlags.CRITICAL
    print("OKAY")

    # -----------------------------
    # Test 4: Multiple Subscribers
    # -----------------------------
    print("Test 4: Multiple Subscribers...")
    def handler_2(event):
        print(f"Handler 2: {event}")

    def handler_3(event):
        print(f"Handler 3: {event}")

    parser.subscribe(EventType.ENTITY_SPAWNED, handler_2)
    parser.subscribe(EventType.ENTITY_SPAWNED, handler_3)
    assert parser.get_listener_count(EventType.ENTITY_SPAWNED) == 3

    # Clear counters and emit
    events_dispatched.clear()
    events_received.clear()
    parser.emit("spawn", EventType.ENTITY_SPAWNED, {"entity": "Enemy"})
    assert len(events_dispatched) == 1
    assert len(events_received) == 3  # All three handlers receive it
    print("OKAY")

    # -----------------------------
    # Test 5: Unsubscribe
    # -----------------------------
    print("Test 5: Unsubscribe...")
    parser.unsubscribe(EventType.ENTITY_SPAWNED, on_entity_spawned)
    assert parser.get_listener_count(EventType.ENTITY_SPAWNED) == 2
    print("OKAY")

    # -----------------------------
    # Test 6: Clear Listeners
    # -----------------------------
    print("Test 6: Clear Listeners...")
    parser.clear_listeners(EventType.ENTITY_SPAWNED)
    assert parser.get_listener_count(EventType.ENTITY_SPAWNED) == 0
    parser.clear_listeners()  # Clear all
    assert parser.get_listener_count(EventType.ENTITY_MOVED) == 0
    print("OKAY")

    # -----------------------------
    # Test 7: Event Data
    # -----------------------------
    print("Test 7: Event Data...")
    event = parser.emit(
        "test_event",
        EventType.TURN_STARTED,
        {"turn_number": 5, "entity_id": 42}
    )
    assert event.data["turn_number"] == 5
    assert event.data["entity_id"] == 42
    print("OKAY")

    # -----------------------------
    # Test 8: Event Serialization
    # -----------------------------
    print("Test 8: Event Serialization...")
    event = parser.emit(
        "serialize_test",
        EventType.STATE_CHANGED,
        {"new_state": "BATTLE", "old_state": "MENU"},
        EventFlags.BLOCKING
    )
    event_dict = event.to_dict()
    assert event_dict["name"] == "serialize_test"
    assert event_dict["type"] == "STATE_CHANGED"
    assert event_dict["flags"] == EventFlags.BLOCKING.value
    
    # Test deserialization
    from engine.core.EventSystem.event import Event
    restored_event = Event.from_dict(event_dict)
    assert restored_event.name == event.name
    assert restored_event.type == event.type
    print("OKAY")

    # -----------------------------
    # Timing Report
    # -----------------------------
    clock.tick()
    print(f"All event system tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_event_system()
