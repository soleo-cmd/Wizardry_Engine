from enum import Enum, IntFlag

class EntityType(Enum):
    PLAYER = 1
    ENEMY = 2
    NPC = 3
    ITEM = 4

class EntityFlags(IntFlag):
    ALIVE = 1
    MOVABLE = 2
    INTERACTIVE = 4

class Entity:
    """
    Core entity data.
    """
    def __init__(self, name: str, entity_type: EntityType, flags: EntityFlags = EntityFlags(0), hp: int = 100, position=(0,0)):
        self.name = name
        self.type = entity_type
        self.flags = flags
        self.hp = hp
        self.position = position
        self.data = {}  # extra arbitrary data

    # -------------------
    # Serialization
    # -------------------
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.name,      # store enum as string
            "flags": self.flags.value,   # store IntFlag as int
            "hp": self.hp,
            "position": self.position
        }

    @classmethod
    def from_dict(cls, data):
        entity_type = EntityType[data["type"]]       # string → enum
        flags = EntityFlags(data["flags"])           # int → IntFlag
        position = tuple(data.get("position", (0,0)))
        return cls(data["name"], entity_type, flags, data["hp"], position)

    # -------------------
    # Helper Methods
    # -------------------
    def is_alive(self):
        return bool(self.flags & EntityFlags.ALIVE)

    def is_movable(self):
        return bool(self.flags & EntityFlags.MOVABLE)

    def move(self, x: int, y: int):
        if self.is_movable():
            self.position = (x, y)

    def take_damage(self, amount: int):
        self.hp = max(self.hp - amount, 0)
        if self.hp == 0:
            self.flags &= ~EntityFlags.ALIVE

    def heal(self, amount: int):
        if self.is_alive():
            self.hp += amount

    def __repr__(self):
        return f"<Entity {self.name}, Type: {self.type.name}, HP: {self.hp}, Pos: {self.position}>"
