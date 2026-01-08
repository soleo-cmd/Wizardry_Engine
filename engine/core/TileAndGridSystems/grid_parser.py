from typing import Optional, Callable
from engine.core.TileAndGridSystems.tile import Tile, TileType, TileFlags
from engine.core.TileAndGridSystems.grid import Grid

class GridParser:
    """
    Game-facing API for grids.
    Handles creation, access, and tile manipulation in a way
    that the game engine can easily call.
    """

    def __init__(self):
        self.grids = {}  # Store multiple grids by name

    # ----------------------
    # Grid Creation
    # ----------------------
    def spawn_grid(self, name: str, width: int, height: int, default_tile: Optional[Tile] = None) -> Grid:
        """Create a new grid and store it under a name."""
        if name in self.grids:
            raise ValueError(f"Grid '{name}' already exists.")
        grid = Grid(width, height, default_tile)
        self.grids[name] = grid
        return grid

    def get_grid(self, name: str) -> Grid:
        """Return a grid by name."""
        if name not in self.grids:
            raise ValueError(f"Grid '{name}' does not exist.")
        return self.grids[name]

    # ----------------------
    # Tile Access
    # ----------------------
    def get_tile(self, grid_name: str, x: int, y: int) -> Tile:
        grid = self.get_grid(grid_name)
        return grid.get_tile(x, y)

    def set_tile(self, grid_name: str, x: int, y: int, tile: Tile):
        grid = self.get_grid(grid_name)
        grid.set_tile(x, y, tile)

    # ----------------------
    # Map Utilities
    # ----------------------
    def fill_borders(self, grid_name: str, border_tile: Tile):
        grid = self.get_grid(grid_name)
        grid.fill_borders(border_tile)

    # ----------------------
    # Hooks for Renderer/Game
    # ----------------------
    def set_tile_changed_hook(self, grid_name: str, hook: Callable[[int, int, Tile], None]):
        """Hook called whenever a tile is changed."""
        grid = self.get_grid(grid_name)
        grid.on_tile_changed = hook

    def set_tile_accessed_hook(self, grid_name: str, hook: Callable[[int, int, Tile], None]):
        """Hook called whenever a tile is accessed."""
        grid = self.get_grid(grid_name)
        grid.on_tile_accessed = hook

    # ----------------------
    # Convenience Functions
    # ----------------------
    def print_grid(self, grid_name: str):
        """Print the grid to console using tile type names."""
        grid = self.get_grid(grid_name)
        for y in range(grid.height):
            row = [grid.get_tile(x, y).type.name[0] for x in range(grid.width)]
            print(" ".join(row))
