# engine/core/StateSystems/state.py
from enum import Enum, IntFlag

class StateType(Enum):
    MENU = 1
    GAMEPLAY = 2
    BATTLE = 3
    CUTSCENE = 4
    PAUSE = 5

class StateFlags(IntFlag):
    ACTIVE = 1
    BLOCKS_INPUT = 2
    VISIBLE = 4

class State:
    """
    Engine-level state data.
    Independent of scenes.
    """
    def __init__(self, name: str, state_type: StateType, flags: StateFlags = StateFlags(0)):
        self.name = name
        self.type = state_type
        self.flags = flags
        self.data = {}  # arbitrary data per state

    # -------------------
    # Serialization
    # -------------------
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.name,    # convert Enum -> string
            "flags": self.flags.value  # convert IntFlag -> int
        }

    @classmethod
    def from_dict(cls, data):
        state_type = StateType[data["type"]]   # string -> Enum
        flags = StateFlags(data["flags"])      # int -> IntFlag
        return cls(data["name"], state_type, flags)

    # -------------------
    # Helper Methods
    # -------------------
    def activate(self):
        self.flags |= StateFlags.ACTIVE

    def deactivate(self):
        self.flags &= ~StateFlags.ACTIVE

    def is_active(self):
        return bool(self.flags & StateFlags.ACTIVE)

    def __repr__(self):
        return f"<State {self.name}, Type: {self.type.name}, Flags: {self.flags}>"
