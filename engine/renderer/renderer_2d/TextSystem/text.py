"""
Text System - Data layer for text rendering

Defines text data structures and font management.
"""

from dataclasses import dataclass, field
from typing import Dict, Optional, Tuple
from ..Core.renderer_config import Transform, Vector2, RenderableFlags, LayerType


@dataclass
class FontConfig:
    """Font configuration."""
    name: str
    file_path: str
    size: int = 12
    bold: bool = False
    italic: bool = False
    
    def __repr__(self):
        return f"<Font '{self.name}' {self.size}px>"


@dataclass
class TextData:
    """Text rendering data."""
    name: str
    text: str
    font_name: str
    x: float
    y: float
    color: Tuple[int, int, int, int] = (255, 255, 255, 255)
    transform: Transform = None
    layer: LayerType = LayerType.UI
    is_visible: bool = True
    flags: RenderableFlags = RenderableFlags.VISIBLE
    alignment: str = "left"  # "left", "center", "right"
    custom_data: dict = field(default_factory=dict)
    
    def __post_init__(self):
        if self.transform is None:
            self.transform = Transform(Vector2(self.x, self.y))
    
    def set_visible(self, visible: bool):
        """Set text visibility."""
        if visible:
            self.flags |= RenderableFlags.VISIBLE
        else:
            self.flags &= ~RenderableFlags.VISIBLE
        self.is_visible = visible
    
    def __repr__(self):
        text_preview = self.text[:20] + "..." if len(self.text) > 20 else self.text
        return f"<Text '{text_preview}'>"
