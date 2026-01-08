# engine/core/TileAndGridSystems/tile.py
from enum import Enum, IntFlag

class TileType(Enum):
    FLOOR = 1
    WALL = 2
    ENTRANCE = 3
    EXIT = 4

class TileFlags(IntFlag):
    WALKABLE = 1
    BLOCKS_SIGHT = 2
    IS_EXIT = 4

class Tile:
    def __init__(
        self,
        tile_type: TileType,
        flags: TileFlags = TileFlags(0),
        x: int | None = None,
        y: int | None = None,
    ):
        self.type = tile_type
        self.flags = flags
        self.x = x
        self.y = y
        self.contents = []

    def with_position(self, x: int, y: int):
        """Return a copy of this tile with coordinates set."""
        return Tile(self.type, self.flags, x, y)

    def is_walkable(self):
        return bool(self.flags & TileFlags.WALKABLE)

    def blocks_sight(self):
        return bool(self.flags & TileFlags.BLOCKS_SIGHT)

    def to_dict(self):
        return {
            "type": self.type.name,
            "flags": self.flags.value,
            "x": self.x,
            "y": self.y,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            TileType[data["type"]],
            TileFlags(data["flags"]),
            data.get("x"),
            data.get("y"),
        )

    def __repr__(self):
        return f"<Tile {self.type.name} ({self.x},{self.y}) Flags:{self.flags}>"
