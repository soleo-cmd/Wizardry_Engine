"""
Drawing System - Parser layer for game code API

Provides game-facing drawing functions with convenient defaults.
"""

from typing import Tuple, Optional, Dict
from .drawing import (
    DrawCommand, RectCommand, CircleCommand, 
    LineCommand, PolygonCommand
)
from .drawing_system import DrawingSystem
from ..Core.renderer_config import Transform, Vector2, LayerType, RenderableFlags


class DrawingParser:
    """
    Game-facing API for drawing operations.
    
    Transforms game code requests into DrawCommand objects
    and manages them through the DrawingSystem.
    """
    
    def __init__(self, drawing_system: DrawingSystem):
        self.drawing_system = drawing_system
        self._counter = 0
    
    def _generate_name(self, prefix: str) -> str:
        """Generate unique command names."""
        self._counter += 1
        return f"{prefix}_{self._counter}"
    
    def draw_rect(
        self,
        x: float,
        y: float,
        width: float = 32,
        height: float = 32,
        color: Tuple[int, int, int, int] = (100, 100, 100, 255),
        fill: bool = True,
        border_width: int = 0,
        layer: LayerType = LayerType.OBJECT,
        name: Optional[str] = None,
        rotation: float = 0.0,
    ) -> str:
        """
        Draw a rectangle.
        
        Args:
            x: X position
            y: Y position
            width: Rectangle width
            height: Rectangle height
            color: RGBA tuple
            fill: Whether to fill the rectangle
            border_width: Border width (0 for no border)
            layer: Rendering layer
            name: Optional command name (auto-generated if not provided)
            rotation: Rotation in degrees
        
        Returns:
            Command name for later reference/manipulation
        """
        name = name or self._generate_name("rect")
        
        command = RectCommand(
            name=name,
            transform=Transform(Vector2(x, y), rotation),
            width=width,
            height=height,
            color=color,
            fill=fill,
            border_width=border_width,
            layer=layer,
        )
        
        return self.drawing_system.add_command(command)
    
    def draw_circle(
        self,
        x: float,
        y: float,
        radius: float = 16,
        color: Tuple[int, int, int, int] = (100, 100, 100, 255),
        fill: bool = True,
        border_width: int = 0,
        layer: LayerType = LayerType.OBJECT,
        name: Optional[str] = None,
    ) -> str:
        """
        Draw a circle.
        
        Args:
            x: Center X position
            y: Center Y position
            radius: Circle radius
            color: RGBA tuple
            fill: Whether to fill the circle
            border_width: Border width (0 for no border)
            layer: Rendering layer
            name: Optional command name (auto-generated if not provided)
        
        Returns:
            Command name
        """
        name = name or self._generate_name("circle")
        
        command = CircleCommand(
            name=name,
            transform=Transform(Vector2(x, y)),
            radius=radius,
            color=color,
            fill=fill,
            border_width=border_width,
            layer=layer,
        )
        
        return self.drawing_system.add_command(command)
    
    def draw_line(
        self,
        start_x: float,
        start_y: float,
        end_x: float,
        end_y: float,
        color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        width: int = 2,
        layer: LayerType = LayerType.OBJECT,
        name: Optional[str] = None,
    ) -> str:
        """
        Draw a line.
        
        Args:
            start_x: Starting X position
            start_y: Starting Y position
            end_x: Ending X position
            end_y: Ending Y position
            color: RGBA tuple
            width: Line width
            layer: Rendering layer
            name: Optional command name
        
        Returns:
            Command name
        """
        name = name or self._generate_name("line")
        
        command = LineCommand(
            name=name,
            transform=Transform(Vector2(start_x, start_y)),
            end_x=end_x,
            end_y=end_y,
            color=color,
            width=width,
            layer=layer,
        )
        
        return self.drawing_system.add_command(command)
    
    def draw_polygon(
        self,
        points: list,
        color: Tuple[int, int, int, int] = (100, 100, 100, 255),
        fill: bool = True,
        border_width: int = 0,
        layer: LayerType = LayerType.OBJECT,
        name: Optional[str] = None,
    ) -> str:
        """
        Draw a polygon from points.
        
        Args:
            points: List of (x, y) tuples
            color: RGBA tuple
            fill: Whether to fill the polygon
            border_width: Border width
            layer: Rendering layer
            name: Optional command name
        
        Returns:
            Command name
        """
        name = name or self._generate_name("polygon")
        
        command = PolygonCommand(
            name=name,
            transform=Transform(Vector2(0, 0)),
            points=points,
            color=color,
            fill=fill,
            border_width=border_width,
            layer=layer,
        )
        
        return self.drawing_system.add_command(command)
    
    def update_position(self, name: str, x: float, y: float) -> bool:
        """Update a command's position."""
        if command := self.drawing_system.get_command(name):
            command.transform.position = Vector2(x, y)
            return True
        return False
    
    def update_color(self, name: str, color: Tuple[int, int, int, int]) -> bool:
        """Update a command's color."""
        if command := self.drawing_system.get_command(name):
            command.color = color
            return True
        return False
    
    def show(self, name: str) -> bool:
        """Show a command."""
        if command := self.drawing_system.get_command(name):
            command.set_visible(True)
            return True
        return False
    
    def hide(self, name: str) -> bool:
        """Hide a command."""
        if command := self.drawing_system.get_command(name):
            command.set_visible(False)
            return True
        return False
    
    def remove(self, name: str) -> bool:
        """Remove a command."""
        return self.drawing_system.remove_command(name) is not None
    
    def clear_all(self):
        """Clear all drawing commands."""
        self.drawing_system.clear_all()
