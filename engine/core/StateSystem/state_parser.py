# engine/core/StateSystems/state_parser.py
from typing import Callable
from .state import State, StateType, StateFlags
from .state_system import StateSystem

class StateParser:
    """
    Game-facing API for states.
    Fully independent from scenes.
    """
    def __init__(self):
        self.system = StateSystem()

    # -----------------------------
    # Commands
    # -----------------------------
    def create_state(self, name: str, state_type: StateType, flags: StateFlags = StateFlags(0)) -> State:
        state = State(name, state_type, flags)
        self.system.add_state(state)
        return state

    def get_state(self, name: str) -> State:
        return self.system.get_state(name)

    def remove_state(self, name: str):
        self.system.remove_state(name)

    def set_current_state(self, name: str):
        self.system.set_current_state(name)

    def get_current_state(self) -> State | None:
        return self.system.current_state

    # -----------------------------
    # Hooks
    # -----------------------------
    def set_created_hook(self, hook: Callable[[State], None]):
        self.system.on_state_created = hook

    def set_changed_hook(self, hook: Callable[[State], None]):
        self.system.on_state_changed = hook

    def set_removed_hook(self, hook: Callable[[State], None]):
        self.system.on_state_removed = hook
