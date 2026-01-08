# engine/core/InputSystem/input_parser.py
from typing import Callable, Dict
from .input_system import InputSystem
from .input import Key

class InputParser:
    """
    Game-facing API for input.
    Handles contexts (scene/state-specific key mappings) and engine hooks.
    """
    def __init__(self):
        self.system = InputSystem()
        self.context_actions: Dict[str, Dict[Key, Callable]] = {}  # context -> key -> function
        self.current_context: str = "default"

    # -----------------------------
    # Context Management
    # -----------------------------
    def set_context(self, context_name: str):
        self.current_context = context_name

    def add_context_action(self, context: str, key: Key, action: Callable):
        """
        Bind a key to a function within a given context.
        """
        if context not in self.context_actions:
            self.context_actions[context] = {}
        self.context_actions[context][key] = action

    # -----------------------------
    # Hook Engine to Parser
    # -----------------------------
    def bind_engine_hooks(self):
        """
        Link engine-level key events to context-specific actions.
        """
        def on_key_pressed(key: Key):
            actions = self.context_actions.get(self.current_context, {})
            if key in actions:
                actions[key]()  # Call the game-defined function

        self.system.on_key_pressed = on_key_pressed
