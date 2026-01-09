# engine/core/DungeonGenerationSystem/generation_config.py
"""
Configuration for dungeon generation.
Pure data classes - no generation logic here.
"""

from enum import Enum
from typing import Dict, Any, List, Tuple

class GenerationAlgorithm(Enum):
    """Available generation algorithms"""
    BINARY_SPACE_PARTITION = 1  # BSP - good for castle-like dungeons
    CELLULAR_AUTOMATA = 2       # CA - good for cave-like dungeons
    RANDOM_ROOMS = 3            # RR - simple random room placement
    CUSTOM = 4                  # Custom algorithm via callback


class DungeonConfig:
    """
    Headless configuration for dungeon generation.
    No rendering, no game logic - pure parameters.
    """
    
    def __init__(
        self,
        name: str = "dungeon",
        width: int = 30,
        height: int = 30,
        algorithm: GenerationAlgorithm = GenerationAlgorithm.RANDOM_ROOMS,
        seed: int = None,
        # For RANDOM_ROOMS algorithm
        min_room_size: int = 4,
        max_room_size: int = 12,
        target_room_count: int = 15,
        # For CELLULAR_AUTOMATA
        wall_fill_probability: float = 0.45,
        iterations: int = 5,
    ):
        self.name = name
        self.width = width
        self.height = height
        self.algorithm = algorithm
        self.seed = seed
        
        # Random rooms
        self.min_room_size = min_room_size
        self.max_room_size = max_room_size
        self.target_room_count = target_room_count
        
        # Cellular automata
        self.wall_fill_probability = wall_fill_probability
        self.iterations = iterations
        
        # Extra data for custom algorithms
        self.extra_data = {}
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "width": self.width,
            "height": self.height,
            "algorithm": self.algorithm.name,
            "seed": self.seed,
            "min_room_size": self.min_room_size,
            "max_room_size": self.max_room_size,
            "target_room_count": self.target_room_count,
            "wall_fill_probability": self.wall_fill_probability,
            "iterations": self.iterations,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DungeonConfig':
        config = cls(
            name=data.get("name", "dungeon"),
            width=data.get("width", 30),
            height=data.get("height", 30),
            algorithm=GenerationAlgorithm[data.get("algorithm", "RANDOM_ROOMS")],
            seed=data.get("seed"),
            min_room_size=data.get("min_room_size", 4),
            max_room_size=data.get("max_room_size", 12),
            target_room_count=data.get("target_room_count", 15),
            wall_fill_probability=data.get("wall_fill_probability", 0.45),
            iterations=data.get("iterations", 5),
        )
        return config
    
    def __repr__(self):
        return (
            f"<DungeonConfig '{self.name}' {self.width}x{self.height} "
            f"algo={self.algorithm.name}>"
        )


class Room:
    """
    Represents a room in a generated dungeon.
    Pure data - no rendering logic.
    """
    
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        room_type: str = "normal",
        room_id: str = None,
    ):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.room_type = room_type  # "normal", "treasure", "boss", "quest", etc.
        self.room_id = room_id or f"room_{x}_{y}"
        self.data = {}  # Arbitrary extra data
    
    def get_center(self) -> Tuple[int, int]:
        """Get the center coordinates of the room."""
        center_x = self.x + self.width // 2
        center_y = self.y + self.height // 2
        return (center_x, center_y)
    
    def contains(self, x: int, y: int) -> bool:
        """Check if point is inside this room."""
        return (
            self.x <= x < self.x + self.width and
            self.y <= y < self.y + self.height
        )
    
    def overlaps(self, other: 'Room') -> bool:
        """Check if this room overlaps with another."""
        return not (
            self.x + self.width < other.x or
            other.x + other.width < self.x or
            self.y + self.height < other.y or
            other.y + other.height < self.y
        )
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
            "room_type": self.room_type,
            "room_id": self.room_id,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Room':
        return cls(
            x=data["x"],
            y=data["y"],
            width=data["width"],
            height=data["height"],
            room_type=data.get("room_type", "normal"),
            room_id=data.get("room_id"),
        )
    
    def __repr__(self):
        return (
            f"<Room '{self.room_id}' ({self.x},{self.y}) "
            f"{self.width}x{self.height} type={self.room_type}>"
        )
