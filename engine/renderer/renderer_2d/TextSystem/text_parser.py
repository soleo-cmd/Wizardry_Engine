"""
Text System - Parser layer for game code API

Provides convenient text rendering and font management functions.
"""

from typing import Optional, Tuple
from .text import TextData, FontConfig
from .text_system import TextSystem
from ..Core.renderer_config import LayerType


class TextParser:
    """
    Game-facing API for text operations.
    
    Handles font loading, text rendering, and text updates.
    """
    
    def __init__(self, text_system: TextSystem):
        self.text_system = text_system
        self._counter = 0
    
    def _generate_name(self, prefix: str = "text") -> str:
        """Generate unique text names."""
        self._counter += 1
        return f"{prefix}_{self._counter}"
    
    def load_font(
        self,
        name: str,
        file_path: str,
        size: int = 12,
        bold: bool = False,
        italic: bool = False,
    ) -> FontConfig:
        """
        Load a font from file.
        
        Args:
            name: Unique font name
            file_path: Path to font file (relative to assets/fonts)
            size: Font size in pixels
            bold: Whether to render bold
            italic: Whether to render italic
        
        Returns:
            FontConfig object
        
        Example:
            parser.load_font("title", "arial.ttf", 32, bold=True)
        """
        return self.text_system.load_font(
            name=name,
            file_path=file_path,
            size=size,
            bold=bold,
            italic=italic,
        )
    
    def render_text(
        self,
        text: str,
        x: float,
        y: float,
        font_name: str = "default",
        color: Tuple[int, int, int, int] = (255, 255, 255, 255),
        layer: LayerType = LayerType.UI,
        name: Optional[str] = None,
        font_size: Optional[int] = None,
    ) -> Optional[str]:
        """
        Render text at a position.
        
        Args:
            text: Text content to render
            x: X position
            y: Y position
            font_name: Name of font to use
            color: RGBA color tuple
            layer: Rendering layer
            name: Optional name (auto-generated if not provided)
        
        Returns:
            Text object name if successful
        
        Example:
            parser.render_text("Score: 100", 10, 10, "title", (255, 0, 0, 255))
        """
        name = name or self._generate_name("text")
        
        text_obj = self.text_system.render_text(
            name=name,
            text=text,
            x=x,
            y=y,
            font_name=font_name,
            color=color,
            layer=layer,
            font_size=font_size,
        )
        
        return text_obj.name if text_obj else None
    
    def update_text(self, name: str, text: str) -> bool:
        """
        Update text content.
        
        Args:
            name: Text object name
            text: New text content
        
        Returns:
            True if successful
        
        Example:
            parser.update_text("score_text", "Score: 150")
        """
        return self.text_system.update_text(name, text)
    
    def move_text(self, name: str, x: float, y: float) -> bool:
        """
        Move text to a new position.
        
        Args:
            name: Text object name
            x: New X position
            y: New Y position
        
        Returns:
            True if successful
        """
        return self.text_system.update_text_position(name, x, y)
    
    def remove_text(self, name: str) -> bool:
        """Remove a text object."""
        return self.text_system.remove_text(name) is not None
    
    def get_text(self, name: str) -> Optional[TextData]:
        """Get a text object by name."""
        return self.text_system.get_text(name)
