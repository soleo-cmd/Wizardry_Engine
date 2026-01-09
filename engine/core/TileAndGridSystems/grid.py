from typing import Optional, Callable, List, Tuple, Set
from .tile import Tile, TileType, TileFlags
import random
from collections import deque

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

    # -------------------
    # Grid Utilities (for generation and manipulation)
    # -------------------
    
    def clone(self) -> 'Grid':
        """Create a deep copy of this grid."""
        new_grid = Grid(self.width, self.height)
        for y in range(self.height):
            for x in range(self.width):
                original_tile = self.tiles[y][x]
                # Create new tile with same properties
                new_tile = Tile(original_tile.type, original_tile.flags, x, y)
                new_grid.tiles[y][x] = new_tile
        return new_grid
    
    def subgrid(self, x: int, y: int, width: int, height: int) -> 'Grid':
        """
        Extract a rectangular portion of this grid as a new grid.
        
        Args:
            x, y: Top-left corner of subgrid
            width, height: Dimensions of subgrid
            
        Returns:
            New Grid containing the extracted tiles
        """
        subgrid = Grid(width, height)
        for dy in range(height):
            for dx in range(width):
                src_x = x + dx
                src_y = y + dy
                if self.in_bounds(src_x, src_y):
                    src_tile = self.tiles[src_y][src_x]
                    new_tile = Tile(src_tile.type, src_tile.flags, dx, dy)
                    subgrid.tiles[dy][dx] = new_tile
        return subgrid
    
    def stamp(self, other_grid: 'Grid', x: int, y: int) -> bool:
        """
        Paste another grid onto this grid at the given position.
        
        Args:
            other_grid: Grid to stamp
            x, y: Position to stamp at (top-left corner)
            
        Returns:
            True if stamp succeeded, False if out of bounds
        """
        # Check bounds
        if x + other_grid.width > self.width or y + other_grid.height > self.height:
            return False
        
        # Stamp tiles
        for dy in range(other_grid.height):
            for dx in range(other_grid.width):
                dest_x = x + dx
                dest_y = y + dy
                src_tile = other_grid.tiles[dy][dx]
                new_tile = Tile(src_tile.type, src_tile.flags, dest_x, dest_y)
                self.set_tile(dest_x, dest_y, new_tile)
        
        return True
    
    def find_tiles(self, tile_type: Optional[TileType] = None, flag: Optional[TileFlags] = None) -> List[Tuple[int, int]]:
        """
        Find all tiles matching criteria.
        
        Args:
            tile_type: Filter by TileType (None = any)
            flag: Filter by flag requirement (None = any)
            
        Returns:
            List of (x, y) positions matching criteria
        """
        results = []
        for y in range(self.height):
            for x in range(self.width):
                tile = self.tiles[y][x]
                
                # Check type filter
                if tile_type is not None and tile.type != tile_type:
                    continue
                
                # Check flag filter
                if flag is not None and not (tile.flags & flag):
                    continue
                
                results.append((x, y))
        
        return results
    
    def is_region_walkable(self, x: int, y: int, width: int, height: int) -> bool:
        """
        Check if a rectangular region is entirely walkable.
        
        Args:
            x, y: Top-left corner
            width, height: Dimensions
            
        Returns:
            True if all tiles in region are walkable
        """
        for dy in range(height):
            for dx in range(width):
                check_x = x + dx
                check_y = y + dy
                if not self.in_bounds(check_x, check_y):
                    return False
                if not self.get_tile(check_x, check_y).is_walkable():
                    return False
        return True
    
    def find_path(self, start: Tuple[int, int], end: Tuple[int, int]) -> Optional[List[Tuple[int, int]]]:
        """
        Find a path between two points using BFS (breadth-first search).
        
        Args:
            start: (x, y) starting position
            end: (x, y) ending position
            
        Returns:
            List of (x, y) positions from start to end, or None if no path exists
        """
        if not self.in_bounds(*start) or not self.in_bounds(*end):
            return None
        
        if not self.get_tile(*start).is_walkable() or not self.get_tile(*end).is_walkable():
            return None
        
        queue = deque([start])
        visited = {start}
        parent = {start: None}
        
        while queue:
            current = queue.popleft()
            
            if current == end:
                # Reconstruct path
                path = []
                node = end
                while node is not None:
                    path.append(node)
                    node = parent[node]
                return list(reversed(path))
            
            # Check 4 adjacent tiles (up, down, left, right)
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_x, next_y = current[0] + dx, current[1] + dy
                next_pos = (next_x, next_y)
                
                if next_pos not in visited and self.in_bounds(next_x, next_y):
                    if self.get_tile(next_x, next_y).is_walkable():
                        visited.add(next_pos)
                        parent[next_pos] = current
                        queue.append(next_pos)
        
        return None
    
    def flood_fill(self, start: Tuple[int, int], target_flag: Optional[TileFlags] = None) -> Set[Tuple[int, int]]:
        """
        Flood fill from a starting position.
        Finds all connected tiles matching criteria (or walkable by default).
        
        Args:
            start: (x, y) starting position
            target_flag: Fill tiles with this flag (None = any walkable)
            
        Returns:
            Set of (x, y) positions that were filled
        """
        if not self.in_bounds(*start):
            return set()
        
        start_tile = self.get_tile(*start)
        if target_flag is None:
            # Default: fill walkable tiles
            if not start_tile.is_walkable():
                return set()
        else:
            # Fill tiles with target flag
            if not (start_tile.flags & target_flag):
                return set()
        
        visited = set()
        queue = deque([start])
        visited.add(start)
        
        while queue:
            current = queue.popleft()
            x, y = current
            
            # Check 4 adjacent tiles
            for dx, dy in [(0, -1), (0, 1), (-1, 0), (1, 0)]:
                next_x, next_y = x + dx, y + dy
                next_pos = (next_x, next_y)
                
                if next_pos not in visited and self.in_bounds(next_x, next_y):
                    next_tile = self.get_tile(next_x, next_y)
                    
                    # Check criteria
                    if target_flag is None:
                        should_fill = next_tile.is_walkable()
                    else:
                        should_fill = bool(next_tile.flags & target_flag)
                    
                    if should_fill:
                        visited.add(next_pos)
                        queue.append(next_pos)
        
        return visited
    
    def random_floor_tile(self) -> Optional[Tuple[int, int]]:
        """
        Get a random walkable floor tile.
        
        Returns:
            (x, y) of random floor tile, or None if no walkable tiles exist
        """
        walkable_tiles = self.find_tiles(flag=TileFlags.WALKABLE)
        if not walkable_tiles:
            return None
        return random.choice(walkable_tiles)
    
    def get_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """
        Calculate Manhattan distance between two positions.
        
        Args:
            pos1: (x, y) first position
            pos2: (x, y) second position
            
        Returns:
            Manhattan distance
        """
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def __repr__(self):
        return f"<Grid {self.width}x{self.height}>"
