from .turn_system import TurnSystem

class TurnParser:
    """
    Game-facing API for the TurnSystem.
    """

    def __init__(self):
        self.system = TurnSystem()
        
    def current_turn(self):
        """Return the Turn object instead of just entity ID"""
        return self.system.current_turn

    # -----------------------------
    # Entity Registration
    # -----------------------------
    def register_entity(self, entity_id: int, action_points: int = 1):
        self.system.add_entity(entity_id, action_points)

    def unregister_entity(self, entity_id: int):
        self.system.remove_entity(entity_id)

    # -----------------------------
    # Turn Flow
    # -----------------------------
    def next_turn(self):
        return self.system.start_next_turn()

    def end_turn(self):
        self.system.end_turn()

    # -----------------------------
    # Action Points
    # -----------------------------
    def spend_ap(self, amount: int = 1) -> bool:
        return self.system.consume_action_point(amount)

    # -----------------------------
    # Queries
    # -----------------------------
    def current_entity(self):
        return self.system.get_current_entity()

    def has_turn(self) -> bool:
        return self.system.has_active_turn()

    # -----------------------------
    # Hooks Exposure
    # -----------------------------
    def set_turn_started_hook(self, hook):
        self.system.on_turn_started = hook

    def set_turn_ended_hook(self, hook):
        self.system.on_turn_ended = hook

    def set_action_spent_hook(self, hook):
        self.system.on_action_spent = hook
