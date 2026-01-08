# engine/core/StateSystems/state_system.py
from typing import Callable, Dict
from .state import State, StateType, StateFlags

class StateSystem:
    """
    Engine-level state system.
    Completely independent from SceneSystem.
    """
    def __init__(self):
        self.states: Dict[str, State] = {}
        self.current_state: State | None = None

        # Hooks
        self.on_state_created: Callable[[State], None] = None
        self.on_state_changed: Callable[[State], None] = None
        self.on_state_removed: Callable[[State], None] = None

    # -----------------------------
    # State Management
    # -----------------------------
    def add_state(self, state: State):
        if state.name in self.states:
            raise ValueError(f"State '{state.name}' already exists.")
        self.states[state.name] = state
        if self.on_state_created:
            self.on_state_created(state)

    def get_state(self, name: str) -> State:
        return self.states.get(name)

    def remove_state(self, name: str):
        state = self.states.pop(name, None)
        if state and self.on_state_removed:
            self.on_state_removed(state)
        if self.current_state == state:
            self.current_state = None

    # -----------------------------
    # State Switching
    # -----------------------------
    def set_current_state(self, name: str):
        state = self.get_state(name)
        if not state:
            raise ValueError(f"State '{name}' does not exist.")
        if self.current_state:
            self.current_state.deactivate()
        state.activate()
        self.current_state = state
        if self.on_state_changed:
            self.on_state_changed(state)
