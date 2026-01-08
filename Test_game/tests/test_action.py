# Test_game/tests/test_action.py
import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from engine.core.ActionCommandSystem.action_parser import ActionParser
from engine.core.ActionCommandSystem.action import ActionType, ActionFlags

class DummyActor:
    def __init__(self, name):
        self.name = name

class DummyTarget:
    def __init__(self, name):
        self.name = name

def test_action_system():
    print("=== Action System Test ===")
    
    parser = ActionParser()

    # Hooks
    parser.set_added_hook(lambda a: print(f"[Hook] Action Added: {a}"))
    parser.set_executed_hook(lambda a: print(f"[Hook] Action Executed: {a}"))

    # Dummy actors and targets
    hero = DummyActor("Hero")
    enemy = DummyActor("Goblin")
    chest = DummyTarget("Chest")

    # -----------------------------
    # Create Actions
    # -----------------------------
    move_action = parser.create_action(hero, ActionType.MOVE, target=(1, 0))
    attack_action = parser.create_action(hero, ActionType.ATTACK, target=enemy)
    loot_action = parser.create_action(hero, ActionType.CUSTOM, target=chest, data={"item": "Gold"})

    assert parser.has_pending_actions()
    print("OKAY: Actions added to queue")

    # -----------------------------
    # Peek next action
    # -----------------------------
    next_action = parser.peek_next_action()
    assert next_action == move_action
    print(f"OKAY: Peeked next action: {next_action}")

    # -----------------------------
    # Execute Actions
    # -----------------------------
    executed = parser.execute_next_action()
    assert executed == move_action
    print(f"OKAY: Executed first action: {executed}")

    executed = parser.execute_next_action()
    assert executed == attack_action
    print(f"OKAY: Executed second action: {executed}")

    executed = parser.execute_next_action()
    assert executed == loot_action
    print(f"OKAY: Executed third action: {executed}")

    # -----------------------------
    # Queue should be empty now
    # -----------------------------
    assert not parser.has_pending_actions()
    print("OKAY: Action queue empty after execution")

    print("=== All Action System tests passed ===")

if __name__ == "__main__":
    test_action_system()
