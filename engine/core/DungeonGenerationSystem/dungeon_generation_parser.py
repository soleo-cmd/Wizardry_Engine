# engine/core/DungeonGenerationSystem/dungeon_generation_parser.py
"""
Game-facing API for dungeon generation.
High-level, simple interface for game code to generate dungeons.
"""

from typing import List, Callable, Optional, Tuple
from .dungeon_generator import DungeonGenerator
from .generation_config import DungeonConfig, Room, GenerationAlgorithm
from ..TileAndGridSystems.grid import Grid


class DungeonGenerationParser:
    """
    Simple game-facing API for dungeon generation.
    Game code calls methods here, generation happens headlessly.
    
    Example:
        parser = DungeonGenerationParser()
        
        # Generate basic dungeon
        config = DungeonConfig(width=30, height=30, target_room_count=15)
        grid, rooms = parser.generate_dungeon(config)
        
        # With quest rooms
        quest_room = Room(0, 0, 5, 5, room_type="quest")
        grid, rooms = parser.generate_dungeon(config, quest_rooms=[quest_room])
    """
    
    def __init__(self):
        self.generator = DungeonGenerator()
    
    # -------------------
    # Generation - Main API
    # -------------------
    
    def generate_dungeon(
        self,
        config: DungeonConfig,
        quest_rooms: Optional[List[Room]] = None,
    ) -> Tuple[Grid, List[Room]]:
        """
        Generate a dungeon.
        
        Args:
            config: DungeonConfig with generation parameters
            quest_rooms: Optional list of quest rooms to place
            
        Returns:
            Tuple of (grid, rooms)
        """
        return self.generator.generate(config, quest_rooms)
    
    # -------------------
    # Quick Generation Presets
    # -------------------
    
    def generate_small_dungeon(
        self,
        quest_rooms: Optional[List[Room]] = None,
        seed: int = None,
    ) -> Tuple[Grid, List[Room]]:
        """Quick generation: small (20x20) dungeon."""
        config = DungeonConfig(
            width=20,
            height=20,
            target_room_count=8,
            seed=seed,
        )
        return self.generate_dungeon(config, quest_rooms)
    
    def generate_medium_dungeon(
        self,
        quest_rooms: Optional[List[Room]] = None,
        seed: int = None,
    ) -> Tuple[Grid, List[Room]]:
        """Quick generation: medium (30x30) dungeon."""
        config = DungeonConfig(
            width=30,
            height=30,
            target_room_count=15,
            seed=seed,
        )
        return self.generate_dungeon(config, quest_rooms)
    
    def generate_large_dungeon(
        self,
        quest_rooms: Optional[List[Room]] = None,
        seed: int = None,
    ) -> Tuple[Grid, List[Room]]:
        """Quick generation: large (50x50) dungeon."""
        config = DungeonConfig(
            width=50,
            height=50,
            target_room_count=30,
            seed=seed,
        )
        return self.generate_dungeon(config, quest_rooms)
    
    def generate_cave_dungeon(
        self,
        quest_rooms: Optional[List[Room]] = None,
        seed: int = None,
    ) -> Tuple[Grid, List[Room]]:
        """Quick generation: cave-like dungeon."""
        config = DungeonConfig(
            width=40,
            height=40,
            algorithm=GenerationAlgorithm.CELLULAR_AUTOMATA,
            seed=seed,
        )
        return self.generate_dungeon(config, quest_rooms)
    
    def generate_castle_dungeon(
        self,
        quest_rooms: Optional[List[Room]] = None,
        seed: int = None,
    ) -> Tuple[Grid, List[Room]]:
        """Quick generation: castle-like dungeon with clear rooms."""
        config = DungeonConfig(
            width=40,
            height=40,
            algorithm=GenerationAlgorithm.BINARY_SPACE_PARTITION,
            seed=seed,
        )
        return self.generate_dungeon(config, quest_rooms)
    
    # -------------------
    # Room Utilities
    # -------------------
    
    def create_quest_room(
        self,
        width: int = 5,
        height: int = 5,
        room_type: str = "quest",
        room_id: str = None,
    ) -> Room:
        """
        Create a quest room template (doesn't place it, just creates data).
        
        Args:
            width, height: Room dimensions
            room_type: Type identifier (e.g., "quest", "boss")
            room_id: Unique identifier
            
        Returns:
            Room object (not placed yet)
        """
        return Room(0, 0, width, height, room_type=room_type, room_id=room_id)
    
    def get_accessible_rooms(self, grid: Grid, rooms: List[Room]) -> List[Room]:
        """Filter rooms to only those that are walkable."""
        return self.generator.get_accessible_rooms(grid, rooms)
    
    def find_room_by_id(self, rooms: List[Room], room_id: str) -> Optional[Room]:
        """Find a specific room by ID."""
        for room in rooms:
            if room.room_id == room_id:
                return room
        return None
    
    def get_rooms_by_type(self, rooms: List[Room], room_type: str) -> List[Room]:
        """Get all rooms of a specific type."""
        return [r for r in rooms if r.room_type == room_type]
    
    # -------------------
    # Configuration Presets
    # -------------------
    
    def create_config(
        self,
        name: str = "dungeon",
        width: int = 30,
        height: int = 30,
        algorithm: str = "RANDOM_ROOMS",
        target_room_count: int = 15,
        seed: int = None,
    ) -> DungeonConfig:
        """Create a DungeonConfig with parameters."""
        algo = GenerationAlgorithm[algorithm]
        return DungeonConfig(
            name=name,
            width=width,
            height=height,
            algorithm=algo,
            target_room_count=target_room_count,
            seed=seed,
        )
    
    # -------------------
    # Hooks for Integration
    # -------------------
    
    def set_generation_started_hook(self, hook: Callable[[DungeonConfig], None]):
        """Called when generation starts."""
        self.generator.on_generation_started = hook
    
    def set_generation_complete_hook(self, hook: Callable[[Grid, List[Room]], None]):
        """Called when generation completes."""
        self.generator.on_generation_complete = hook
    
    def set_room_placed_hook(self, hook: Callable[[Room], None]):
        """Called when a room is placed."""
        self.generator.on_room_placed = hook
    
    def set_quest_room_placed_hook(self, hook: Callable[[Room], None]):
        """Called when a quest room is placed."""
        self.generator.on_quest_room_placed = hook
