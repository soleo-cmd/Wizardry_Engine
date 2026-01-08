from enum import Enum, IntFlag

class VisibilityType(Enum):
    VISIBLE = 1
    HIDDEN = 2
    FOG_OF_WAR = 3

class VisibilityFlags(IntFlag):
    NONE = 0
    BLOCKING = 1
    TRANSPARENT = 2
    LIGHT_SOURCE = 4

class Visibility:
    """
    Engine-level visibility data.
    Represents a tile or entity's visibility state.
    """
    def __init__(self, position: tuple, visibility_type: VisibilityType, flags: VisibilityFlags = VisibilityFlags.NONE):
        self.position = position
        self.type = visibility_type
        self.flags = flags
        self.observed_by: set = set()  # Set of entity IDs that can see this

    def to_dict(self):
        return {
            "position": self.position,
            "type": self.type.name,
            "flags": self.flags.value,
            "observed_by": list(self.observed_by)
        }

    @classmethod
    def from_dict(cls, data):
        visibility_type = VisibilityType[data["type"]]
        flags = VisibilityFlags(data["flags"])
        visibility = cls(tuple(data["position"]), visibility_type, flags)
        visibility.observed_by = set(data.get("observed_by", []))
        return visibility

    def is_visible(self) -> bool:
        return self.type == VisibilityType.VISIBLE

    def is_blocked(self) -> bool:
        return bool(self.flags & VisibilityFlags.BLOCKING)

    def is_transparent(self) -> bool:
        return bool(self.flags & VisibilityFlags.TRANSPARENT)

    def is_light_source(self) -> bool:
        return bool(self.flags & VisibilityFlags.LIGHT_SOURCE)

    def add_observer(self, entity_id: int):
        self.observed_by.add(entity_id)

    def remove_observer(self, entity_id: int):
        self.observed_by.discard(entity_id)

    def __repr__(self):
        return f"<Visibility {self.type.name} at {self.position}, Observers: {len(self.observed_by)}>"
