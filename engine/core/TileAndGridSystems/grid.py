from typing import Optional, Callable, List
from .tile import Tile, TileType, TileFlags

class Grid:
    def __init__(self, width: int, height: int, default_tile: Optional[Tile] = None):
        self.width = width
        self.height = height
        self.tiles = [
            [
                (default_tile or Tile(TileType.FLOOR, TileFlags.WALKABLE)).with_position(x, y)
                for x in range(width)
            ]
            for y in range(height)
        ]

        # Hooks
        self.on_tile_changed: Optional[Callable[[int, int, Tile], None]] = None
        self.on_tile_accessed: Optional[Callable[[int, int, Tile], None]] = None

    def to_dict(self):
        return {
            "width": self.width,
            "height": self.height,
            "tiles": [[tile.to_dict() for tile in row] for row in self.tiles]
        }

    @classmethod
    def from_dict(cls, data):
        grid = cls(data["width"], data["height"])
        for y in range(grid.height):
            for x in range(grid.width):
                grid.tiles[y][x] = Tile.from_dict(data["tiles"][y][x])
        return grid

    def set_tile(self, x: int, y: int, tile: Tile):
        if self.in_bounds(x, y):
            self.tiles[y][x] = tile
            if self.on_tile_changed:
                self.on_tile_changed(x, y, tile)
        else:
            raise IndexError(f"Position ({x},{y}) out of bounds")

    def get_tile(self, x: int, y: int) -> Tile:
        if self.in_bounds(x, y):
            tile = self.tiles[y][x]
            if self.on_tile_accessed:
                self.on_tile_accessed(x, y, tile)
            return tile
        else:
            raise IndexError(f"Position ({x},{y}) out of bounds")

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def fill_borders(self, border_tile: Tile):
        for x in range(self.width):
            self.set_tile(x, 0, border_tile)
            self.set_tile(x, self.height - 1, border_tile)
        for y in range(self.height):
            self.set_tile(0, y, border_tile)
            self.set_tile(self.width - 1, y, border_tile)

    def iterate_tiles(self):
        for y in range(self.height):
            for x in range(self.width):
                yield x, y, self.tiles[y][x]

    def __repr__(self):
        return f"<Grid {self.width}x{self.height}>"
