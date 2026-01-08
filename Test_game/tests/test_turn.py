def test_turn_with_actions():
    from engine.core.TurnSystem.turn_parser import TurnParser
    from engine.core.ActionCommandSystem.action_parser import ActionParser, ActionType

    print("=== TEST: TurnSystem with Actions ===")

    # -----------------------------
    # Initialize Parsers
    # -----------------------------
    turn_parser = TurnParser()
    action_parser = ActionParser()

    # -----------------------------
    # Register Entities
    # -----------------------------
    turn_parser.register_entity(1, action_points=2)
    turn_parser.register_entity(2, action_points=1)
    print("Registered entities 1 (AP=2) and 2 (AP=1)")

    # -----------------------------
    # Hook: Spend 1 AP per action
    # -----------------------------
    def spend_ap_hook(action):
        print(f"Executing Action: {action.type.name} for Entity {action.entity_id}, Target: {action.target}")
        result = turn_parser.spend_ap(1)
        turn_obj = turn_parser.current_turn()
        print(f"   -> Action Points Remaining: {turn_obj.action_points if turn_obj else 0}")
        return result

    action_parser.on_execute_action = spend_ap_hook

    # -----------------------------
    # Queue Actions for Entity 1
    # -----------------------------
    action_parser.create_action(1, ActionType.MOVE, target=(1, 0))
    action_parser.create_action(1, ActionType.ATTACK, target="Goblin")
    print("Added MOVE and ATTACK actions for Entity 1")

    # -----------------------------
    # Start First Turn
    # -----------------------------
    turn = turn_parser.next_turn()
    print(f"Turn started: {turn}")

    # Execute all actions for Entity 1
    while action_parser.has_actions_for_entity(turn.entity_id):
        action_parser.execute_next_action(turn.entity_id)

    # Confirm AP exhausted
    print(f"End of Entity {turn.entity_id} turn: {turn}")

    # -----------------------------
    # Start Next Turn
    # -----------------------------
    turn2 = turn_parser.next_turn()
    print(f"Turn started: {turn2}")

    # Queue an action for Entity 2
    action_parser.create_action(2, ActionType.MOVE, target=(0, -1))
    print("Added MOVE action for Entity 2")

    # Execute all actions for Entity 2
    while action_parser.has_actions_for_entity(turn2.entity_id):
        action_parser.execute_next_action(turn2.entity_id)

    print(f"End of Entity {turn2.entity_id} turn: {turn2}")

    # -----------------------------
    # Cycle back to Entity 1
    # -----------------------------
    turn3 = turn_parser.next_turn()
    print(f"Next turn: {turn3}")

    # -----------------------------
    # Test completed
    # -----------------------------
    print("\n=== TEST COMPLETE ===")

# -----------------------------
# Run test if called directly
# -----------------------------
if __name__ == "__main__":
    test_turn_with_actions()
