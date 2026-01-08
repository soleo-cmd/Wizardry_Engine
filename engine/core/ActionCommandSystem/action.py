from enum import Enum, IntFlag

class ActionType(Enum):
    MOVE = 1
    ATTACK = 2
    ITEM = 3
    WAIT = 4

class ActionFlags(IntFlag):
    NONE = 0
    REQUIRES_TARGET = 1

class Action:
    """
    Engine-level action data.
    """
    def __init__(self, entity_id: int, action_type: ActionType, flags: ActionFlags = ActionFlags.NONE, target=None):
        self.entity_id = entity_id
        self.type = action_type
        self.flags = flags
        self.target = target

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "type": self.type.name,
            "flags": self.flags.name,
            "target": self.target
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["entity_id"],
            ActionType[data["type"]],
            ActionFlags[data["flags"]],
            data.get("target")
        )

    def __repr__(self):
        return f"<Action {self.type.name} by Entity={self.entity_id} Target={self.target}>"
