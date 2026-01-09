"""
Drawing System - Data layer for drawing commands

Defines all types of shapes and drawing data.
"""

from dataclasses import dataclass
from typing import Tuple, Optional
from ..Core.renderer_config import Vector2, Color, Transform, LayerType, RenderableType, RenderableFlags


@dataclass
class DrawCommand:
    """Base class for draw commands."""
    name: str
    transform: Transform
    layer: LayerType = LayerType.OBJECT
    flags: RenderableFlags = RenderableFlags.VISIBLE
    custom_data: dict = None
    command_type: str = ""  # Set by subclasses
    
    def __post_init__(self):
        if self.custom_data is None:
            self.custom_data = {}
    
    def is_visible(self) -> bool:
        return bool(self.flags & RenderableFlags.VISIBLE)
    
    def set_visible(self, visible: bool):
        if visible:
            self.flags |= RenderableFlags.VISIBLE
        else:
            self.flags &= ~RenderableFlags.VISIBLE
    
    def __repr__(self):
        return f"<DrawCommand {self.name}, Type: {self.command_type}>"


@dataclass
class RectCommand(DrawCommand):
    """Rectangle drawing command."""
    width: float = 32
    height: float = 32
    color: Tuple[int, int, int, int] = (100, 100, 100, 255)
    fill: bool = True
    border_width: int = 0
    
    def __post_init__(self):
        self.command_type = "rect"
        if self.custom_data is None:
            self.custom_data = {}


@dataclass
class CircleCommand(DrawCommand):
    """Circle drawing command."""
    radius: float = 16
    color: Tuple[int, int, int, int] = (100, 100, 100, 255)
    fill: bool = True
    border_width: int = 0
    
    def __post_init__(self):
        self.command_type = "circle"
        if self.custom_data is None:
            self.custom_data = {}


@dataclass
class LineCommand(DrawCommand):
    """Line drawing command."""
    end_x: float = 100
    end_y: float = 100
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    width: int = 2
    
    def __post_init__(self):
        self.command_type = "line"
        if self.custom_data is None:
            self.custom_data = {}


@dataclass
class PolygonCommand(DrawCommand):
    """Polygon drawing command."""
    points: list = None  # List of (x, y) tuples
    color: Tuple[int, int, int, int] = (100, 100, 100, 255)
    fill: bool = True
    border_width: int = 0
    
    def __post_init__(self):
        self.command_type = "polygon"
        if self.points is None:
            self.points = []
        if self.custom_data is None:
            self.custom_data = {}
