# engine/core/InputSystem/input_system.py
from typing import Callable
from .input import Key

class InputSystem:
    """
    Engine-level input system.
    Tracks raw key states and provides query functions.
    """
    def __init__(self):
        self.key_states = {key: False for key in Key}         # Currently held
        self.prev_key_states = {key: False for key in Key}    # Last update

        # Hooks for engine to notify game logic
        self.on_key_pressed: Callable[[Key], None] = None
        self.on_key_released: Callable[[Key], None] = None

    # -----------------------------
    # Engine updates per frame
    # -----------------------------
    def update(self):
        """
        Call once per frame to update previous key states.
        """
        self.prev_key_states = self.key_states.copy()

    def press_key(self, key: Key):
        if not self.key_states[key]:
            self.key_states[key] = True
            if self.on_key_pressed:
                self.on_key_pressed(key)

    def release_key(self, key: Key):
        if self.key_states[key]:
            self.key_states[key] = False
            if self.on_key_released:
                self.on_key_released(key)

    # -----------------------------
    # Queries
    # -----------------------------
    def is_pressed(self, key: Key) -> bool:
        """Is the key currently held down?"""
        return self.key_states[key]

    def just_pressed(self, key: Key) -> bool:
        """True only on the frame the key was pressed."""
        return self.key_states[key] and not self.prev_key_states[key]

    def just_released(self, key: Key) -> bool:
        """True only on the frame the key was released."""
        return not self.key_states[key] and self.prev_key_states[key]

    def held(self, key: Key) -> bool:
        """Alias for is_pressed."""
        return self.key_states[key]
