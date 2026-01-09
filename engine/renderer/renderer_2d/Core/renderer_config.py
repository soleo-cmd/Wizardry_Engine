"""
Core Renderer Configuration and Data Structures

Shared by all renderer systems - completely independent from game logic.
"""

from enum import Enum, IntFlag
from dataclasses import dataclass
from typing import Tuple, Optional, Dict, Any


@dataclass
class Vector2:
    """2D Vector for positions and sizes."""
    x: float
    y: float
    
    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)


@dataclass
class Color:
    """RGBA Color."""
    r: int
    g: int
    b: int
    a: int = 255
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)


@dataclass
class Transform:
    """Position, rotation, and scale."""
    position: Vector2
    rotation: float = 0.0  # Degrees
    scale: Vector2 = None
    
    def __post_init__(self):
        if self.scale is None:
            self.scale = Vector2(1.0, 1.0)


class LayerType(Enum):
    """Rendering layer order (z-depth)."""
    BACKGROUND = 0
    GROUND = 1
    OBJECT = 2
    ENTITY = 3
    UI = 4
    OVERLAY = 5


class RenderableType(Enum):
    """Types of renderables."""
    SHAPE = 1
    SPRITE = 2
    TEXT = 3


class RenderableFlags(IntFlag):
    """Flags for renderable properties."""
    NONE = 0
    VISIBLE = 1
    ANIMATED = 2


class RenderConfig:
    """Renderer configuration."""
    
    def __init__(
        self,
        window_title: str = "Wizardry Game",
        window_width: int = 1280,
        window_height: int = 720,
        fps: int = 60,
        fullscreen: bool = False,
        vsync: bool = True,
        headless: bool = False,  # Run without display
    ):
        self.window_title = window_title
        self.window_width = window_width
        self.window_height = window_height
        self.fps = fps
        self.fullscreen = fullscreen
        self.vsync = vsync
        self.headless = headless
    
    def __repr__(self):
        mode = "Headless" if self.headless else f"{self.window_width}x{self.window_height}"
        return f"<RenderConfig {mode} @ {self.fps}fps>"
