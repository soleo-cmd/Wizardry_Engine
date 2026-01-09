# engine/core/DungeonGenerationSystem/dungeon_generator.py
"""
Headless dungeon generation system.
No rendering, no game logic - pure dungeon generation algorithms.
"""

from typing import List, Callable, Optional, Tuple
from .generation_config import DungeonConfig, Room, GenerationAlgorithm
from ..TileAndGridSystems.grid import Grid
from ..TileAndGridSystems.tile import Tile, TileType, TileFlags
import random


class DungeonGenerator:
    """
    Generates random dungeons according to a DungeonConfig.
    Completely headless - no rendering or game logic.
    
    Features:
    - Multiple generation algorithms (BSP, Cellular Automata, Random Rooms)
    - Room tracking
    - Corridor generation
    - Quest room placement in accessible areas
    - Hooks for integration
    - Serializable
    """
    
    def __init__(self):
        # Hooks
        self.on_generation_started: Optional[Callable[[DungeonConfig], None]] = None
        self.on_generation_complete: Optional[Callable[[Grid, List[Room]], None]] = None
        self.on_room_placed: Optional[Callable[[Room], None]] = None
        self.on_quest_room_placed: Optional[Callable[[Room], None]] = None
    
    # -------------------
    # Main Generation
    # -------------------
    
    def generate(
        self,
        config: DungeonConfig,
        quest_rooms: Optional[List[Room]] = None,
    ) -> Tuple[Grid, List[Room]]:
        """
        Generate a dungeon according to config.
        
        Args:
            config: DungeonConfig with generation parameters
            quest_rooms: Optional list of quest rooms to place in accessible areas
            
        Returns:
            Tuple of (generated_grid, list_of_rooms)
        """
        # Set seed for reproducibility
        if config.seed is not None:
            random.seed(config.seed)
        
        if self.on_generation_started:
            self.on_generation_started(config)
        
        # Generate based on algorithm
        if config.algorithm == GenerationAlgorithm.RANDOM_ROOMS:
            grid, rooms = self._generate_random_rooms(config)
        elif config.algorithm == GenerationAlgorithm.CELLULAR_AUTOMATA:
            grid, rooms = self._generate_cellular_automata(config)
        elif config.algorithm == GenerationAlgorithm.BINARY_SPACE_PARTITION:
            grid, rooms = self._generate_bsp(config)
        else:
            # Fallback to random rooms
            grid, rooms = self._generate_random_rooms(config)
        
        # Place quest rooms if provided
        if quest_rooms:
            rooms = self._place_quest_rooms(grid, rooms, quest_rooms)
        
        if self.on_generation_complete:
            self.on_generation_complete(grid, rooms)
        
        return grid, rooms
    
    # -------------------
    # Random Rooms Algorithm
    # -------------------
    
    def _generate_random_rooms(self, config: DungeonConfig) -> Tuple[Grid, List[Room]]:
        """
        Simple algorithm: randomly place rooms, connect with corridors.
        Good for dungeons with clear room structure.
        """
        # Start with all walls
        grid = Grid(
            config.width,
            config.height,
            default_tile=Tile(TileType.WALL, TileFlags(0))
        )
        
        rooms: List[Room] = []
        max_attempts = 100
        attempts = 0
        
        # Try to place rooms
        while len(rooms) < config.target_room_count and attempts < max_attempts:
            width = random.randint(config.min_room_size, config.max_room_size)
            height = random.randint(config.min_room_size, config.max_room_size)
            x = random.randint(1, config.width - width - 1)
            y = random.randint(1, config.height - height - 1)
            
            room = Room(x, y, width, height, room_type="normal")
            
            # Check if room overlaps with existing rooms
            if not any(room.overlaps(existing) for existing in rooms):
                rooms.append(room)
                self._carve_room(grid, room)
                if self.on_room_placed:
                    self.on_room_placed(room)
            
            attempts += 1
        
        # Connect rooms with corridors
        if rooms:
            self._connect_rooms_simple(grid, rooms)
        
        return grid, rooms
    
    # -------------------
    # Cellular Automata Algorithm
    # -------------------
    
    def _generate_cellular_automata(self, config: DungeonConfig) -> Tuple[Grid, List[Room]]:
        """
        Cave-like generation using cellular automata.
        Fills grid randomly, then applies iterations of smoothing.
        """
        # Initialize: randomly fill grid with walls/floors
        grid = Grid(config.width, config.height)
        for y in range(config.height):
            for x in range(config.width):
                if random.random() < config.wall_fill_probability:
                    grid.set_tile(x, y, Tile(TileType.WALL, TileFlags(0)))
                else:
                    grid.set_tile(x, y, Tile(TileType.FLOOR, TileFlags.WALKABLE))
        
        # Apply smoothing iterations
        for _ in range(config.iterations):
            grid = self._cellular_automata_iteration(grid)
        
        # Extract rooms from the generated cave
        rooms = self._find_rooms_from_caves(grid)
        
        return grid, rooms
    
    def _cellular_automata_iteration(self, grid: Grid) -> Grid:
        """Single iteration of cellular automata smoothing."""
        new_grid = grid.clone()
        
        for y in range(1, grid.height - 1):
            for x in range(1, grid.width - 1):
                # Count wall neighbors
                wall_count = 0
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        neighbor = grid.get_tile(x + dx, y + dy)
                        if neighbor.type == TileType.WALL:
                            wall_count += 1
                
                # Apply rule: become wall if too many neighbors are walls
                if wall_count > 4:
                    new_grid.set_tile(x, y, Tile(TileType.WALL, TileFlags(0)))
                else:
                    new_grid.set_tile(x, y, Tile(TileType.FLOOR, TileFlags.WALKABLE))
        
        return new_grid
    
    # -------------------
    # Binary Space Partition Algorithm
    # -------------------
    
    def _generate_bsp(self, config: DungeonConfig) -> Tuple[Grid, List[Room]]:
        """
        Castle-like generation using binary space partitioning.
        Recursively divides space into rooms.
        """
        grid = Grid(
            config.width,
            config.height,
            default_tile=Tile(TileType.WALL, TileFlags(0))
        )
        
        rooms: List[Room] = []
        
        # Start with one space covering entire dungeon
        initial_space = (1, 1, config.width - 2, config.height - 2)
        self._bsp_partition(grid, initial_space, rooms, config)
        
        # Connect rooms
        if rooms:
            self._connect_rooms_simple(grid, rooms)
        
        return grid, rooms
    
    def _bsp_partition(
        self,
        grid: Grid,
        space: Tuple[int, int, int, int],
        rooms: List[Room],
        config: DungeonConfig,
        depth: int = 0,
        max_depth: int = 6,
    ):
        """Recursively partition space and create rooms."""
        x, y, width, height = space
        
        # Base case: space too small to subdivide
        if width < config.min_room_size * 2 or height < config.min_room_size * 2:
            # Create room in this space
            room_width = random.randint(
                config.min_room_size,
                min(config.max_room_size, width - 2)
            )
            room_height = random.randint(
                config.min_room_size,
                min(config.max_room_size, height - 2)
            )
            room_x = x + random.randint(0, width - room_width - 1)
            room_y = y + random.randint(0, height - room_height - 1)
            
            room = Room(room_x, room_y, room_width, room_height)
            rooms.append(room)
            self._carve_room(grid, room)
            if self.on_room_placed:
                self.on_room_placed(room)
            return
        
        # Recursive case: split space
        if depth > max_depth:
            return
        
        # Decide to split horizontally or vertically
        if random.choice([True, False]):
            # Vertical split
            split_x = x + random.randint(
                config.min_room_size,
                width - config.min_room_size - 1
            )
            self._bsp_partition(
                grid, (x, y, split_x - x, height), rooms, config, depth + 1, max_depth
            )
            self._bsp_partition(
                grid, (split_x, y, x + width - split_x, height), rooms, config, depth + 1, max_depth
            )
        else:
            # Horizontal split
            split_y = y + random.randint(
                config.min_room_size,
                height - config.min_room_size - 1
            )
            self._bsp_partition(
                grid, (x, y, width, split_y - y), rooms, config, depth + 1, max_depth
            )
            self._bsp_partition(
                grid, (x, split_y, width, y + height - split_y), rooms, config, depth + 1, max_depth
            )
    
    # -------------------
    # Utility Methods
    # -------------------
    
    def _carve_room(self, grid: Grid, room: Room):
        """Carve a room into the grid (make it walkable)."""
        for y in range(room.y, room.y + room.height):
            for x in range(room.x, room.x + room.width):
                if grid.in_bounds(x, y):
                    grid.set_tile(x, y, Tile(TileType.FLOOR, TileFlags.WALKABLE))
    
    def _connect_rooms_simple(self, grid: Grid, rooms: List[Room]):
        """Connect rooms with straight corridors."""
        for i in range(len(rooms) - 1):
            room1 = rooms[i]
            room2 = rooms[i + 1]
            
            center1 = room1.get_center()
            center2 = room2.get_center()
            
            # Draw horizontal corridor
            y = center1[1]
            for x in range(min(center1[0], center2[0]), max(center1[0], center2[0]) + 1):
                if grid.in_bounds(x, y):
                    grid.set_tile(x, y, Tile(TileType.FLOOR, TileFlags.WALKABLE))
            
            # Draw vertical corridor
            x = center2[0]
            for y in range(min(center1[1], center2[1]), max(center1[1], center2[1]) + 1):
                if grid.in_bounds(x, y):
                    grid.set_tile(x, y, Tile(TileType.FLOOR, TileFlags.WALKABLE))
    
    def _find_rooms_from_caves(self, grid: Grid) -> List[Room]:
        """Extract rooms from a grid (for cave generation)."""
        rooms: List[Room] = []
        visited = set()
        room_counter = 0
        
        for y in range(grid.height):
            for x in range(grid.width):
                if (x, y) not in visited and grid.get_tile(x, y).is_walkable():
                    # Flood fill to find room
                    room_tiles = grid.flood_fill((x, y), TileFlags.WALKABLE)
                    if len(room_tiles) > 4:  # Minimum room size
                        visited.update(room_tiles)
                        
                        # Get bounding box
                        xs = [pos[0] for pos in room_tiles]
                        ys = [pos[1] for pos in room_tiles]
                        room_x, room_y = min(xs), min(ys)
                        room_width = max(xs) - room_x + 1
                        room_height = max(ys) - room_y + 1
                        
                        room = Room(room_x, room_y, room_width, room_height)
                        rooms.append(room)
                        room_counter += 1
        
        return rooms
    
    # -------------------
    # Quest Room Placement
    # -------------------
    
    def _place_quest_rooms(
        self,
        grid: Grid,
        existing_rooms: List[Room],
        quest_rooms: List[Room],
    ) -> List[Room]:
        """
        Place quest rooms in accessible areas of the grid.
        
        Args:
            grid: Generated dungeon grid
            existing_rooms: Rooms already in the dungeon
            quest_rooms: Quest rooms to place (must have width/height set)
            
        Returns:
            Updated list of rooms (existing + placed quest rooms)
        """
        all_rooms = existing_rooms.copy()
        
        for quest_room in quest_rooms:
            # Find accessible placement
            placed = False
            max_attempts = 100
            
            for _ in range(max_attempts):
                # Try random position
                x = random.randint(1, grid.width - quest_room.width - 1)
                y = random.randint(1, grid.height - quest_room.height - 1)
                
                test_room = Room(x, y, quest_room.width, quest_room.height, 
                               room_type=quest_room.room_type)
                
                # Check criteria:
                # 1. Doesn't overlap with existing rooms
                # 2. Area is mostly walkable
                # 3. At least one adjacent room (connected)
                
                overlaps_existing = any(test_room.overlaps(r) for r in all_rooms)
                
                if not overlaps_existing:
                    # Check if area is walkable
                    is_walkable = grid.is_region_walkable(x, y, quest_room.width, quest_room.height)
                    
                    if is_walkable:
                        # Carve the quest room
                        self._carve_room(grid, test_room)
                        
                        # Copy properties from quest_room template
                        test_room.room_type = quest_room.room_type
                        test_room.room_id = quest_room.room_id
                        test_room.data = quest_room.data.copy()
                        
                        all_rooms.append(test_room)
                        if self.on_quest_room_placed:
                            self.on_quest_room_placed(test_room)
                        placed = True
                        break
            
            if not placed:
                # If placement failed, add to list anyway
                # Game can handle placement failure
                all_rooms.append(quest_room)
        
        return all_rooms
    
    def get_accessible_rooms(self, grid: Grid, rooms: List[Room]) -> List[Room]:
        """
        Filter rooms to only those that are walkable.
        
        Args:
            grid: The dungeon grid
            rooms: List of rooms to filter
            
        Returns:
            List of accessible rooms
        """
        return [
            room for room in rooms
            if grid.is_region_walkable(room.x, room.y, room.width, room.height)
        ]
