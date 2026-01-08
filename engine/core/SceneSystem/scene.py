# engine/core/SceneSystem/scene.py
from enum import Enum, IntFlag

class SceneType(Enum):
    MENU = 1
    OVERWORLD = 2
    BATTLE = 3

class SceneFlags(IntFlag):
    ACTIVE = 1
    PAUSES_STATE = 2
    VISIBLE = 4

class Scene:
    """
    Engine-level scene data.
    Holds data independent of states.
    """
    def __init__(self, name: str, scene_type: SceneType, flags: SceneFlags = SceneFlags(0), nodes: list = None):
        self.name = name
        self.type = scene_type
        self.flags = flags
        self.data = {}  # arbitrary scene-level data

    # -------------------
    # Serialization
    # -------------------
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.name,     # Enum -> string
            "flags": self.flags.value,  # IntFlag -> int
            "nodes": self.nodes
        }

    @classmethod
    def from_dict(cls, data):
        scene_type = SceneType[data["type"]]   # string -> Enum
        flags = SceneFlags(data["flags"])      # int -> IntFlag
        nodes = data.get("nodes", [])
        return cls(data["name"], scene_type, flags)

    # -------------------
    # Helper Methods
    # -------------------
    def activate(self):
        self.flags |= SceneFlags.ACTIVE

    def deactivate(self):
        self.flags &= ~SceneFlags.ACTIVE

    def is_active(self):
        return bool(self.flags & SceneFlags.ACTIVE)

    def __repr__(self):
        return f"<Scene {self.name}, Type: {self.type.name}, Flags: {self.flags}>"
