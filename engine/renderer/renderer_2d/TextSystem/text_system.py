"""
Text System - Engine layer for text management

Manages fonts and text rendering data.
Completely independent from rendering backend.
"""

from typing import Dict, Optional, Callable, List
from .text import TextData, FontConfig
from ..Core.renderer_config import LayerType, Vector2


class TextSystem:
    """
    Manages text rendering.
    
    Handles font loading and text data management.
    Backends register hooks to receive text rendering updates.
    """
    
    def __init__(self, assets_path: str = "./assets/fonts"):
        """
        Initialize text system.
        
        Args:
            assets_path: Base path for font assets
        """
        self.assets_path = assets_path
        self.fonts: Dict[str, FontConfig] = {}
        self.text_objects: Dict[str, TextData] = {}
        
        # Hooks
        self.on_font_loaded: List[Callable] = []
        self.on_text_added: List[Callable] = []
        self.on_text_updated: List[Callable] = []
        self.on_text_removed: List[Callable] = []
        
        # Register a default font
        self._register_default_font()
    
    def _register_default_font(self):
        """Register a basic default font."""
        default_font = FontConfig(
            name="default",
            file_path="",  # System default
            size=12,
        )
        self.fonts["default"] = default_font
    
    def register_font_hook(self, hook: Callable):
        """Register hook for font loading."""
        if hook not in self.on_font_loaded:
            self.on_font_loaded.append(hook)
    
    def register_text_add_hook(self, hook: Callable):
        """Register hook for text addition."""
        if hook not in self.on_text_added:
            self.on_text_added.append(hook)
    
    def register_text_update_hook(self, hook: Callable):
        """Register hook for text updates."""
        if hook not in self.on_text_updated:
            self.on_text_updated.append(hook)
    
    def register_text_remove_hook(self, hook: Callable):
        """Register hook for text removal."""
        if hook not in self.on_text_removed:
            self.on_text_removed.append(hook)
    
    def load_font(
        self,
        name: str,
        file_path: str,
        size: int = 12,
        bold: bool = False,
        italic: bool = False,
    ) -> FontConfig:
        """
        Load a font.
        
        Args:
            name: Unique font name
            file_path: Path to font file (relative to assets_path)
            size: Font size
            bold: Whether to bold
            italic: Whether to italicize
        
        Returns:
            FontConfig object
        """
        if name in self.fonts:
            raise ValueError(f"Font '{name}' already loaded")
        
        font = FontConfig(
            name=name,
            file_path=file_path,
            size=size,
            bold=bold,
            italic=italic,
        )
        
        self.fonts[name] = font
        
        # Trigger hooks
        for hook in self.on_font_loaded:
            hook(font)
        
        return font
    
    def get_font(self, name: str) -> Optional[FontConfig]:
        """Get a loaded font."""
        return self.fonts.get(name)
    
    def render_text(
        self,
        name: str,
        text: str,
        x: float,
        y: float,
        font_name: str = "default",
        color: tuple = (255, 255, 255, 255),
        layer = None,
    ) -> Optional[TextData]:
        """
        Create a text object for rendering.
        
        Args:
            name: Unique text object name
            text: Text content
            x: X position
            y: Y position
            font_name: Name of font to use
            color: RGBA color tuple
            layer: Rendering layer
        
        Returns:
            TextData object if successful
        """
        if name in self.text_objects:
            raise ValueError(f"Text object '{name}' already exists")
        
        if font_name not in self.fonts:
            font_name = "default"
        
        if layer is None:
            layer = LayerType.UI
        
        text_obj = TextData(
            name=name,
            text=text,
            font_name=font_name,
            x=x,
            y=y,
            color=color,
            layer=layer,
        )
        
        self.text_objects[name] = text_obj
        
        # Trigger hooks
        for hook in self.on_text_added:
            hook(text_obj)
        
        return text_obj
    
    def get_text(self, name: str) -> Optional[TextData]:
        """Get a text object."""
        return self.text_objects.get(name)
    
    def update_text(self, name: str, text: str) -> bool:
        """Update text content."""
        if name not in self.text_objects:
            return False
        
        self.text_objects[name].text = text
        
        for hook in self.on_text_updated:
            hook(self.text_objects[name])
        
        return True
    
    def update_text_position(self, name: str, x: float, y: float) -> bool:
        """Update text position."""
        if name not in self.text_objects:
            return False
        
        self.text_objects[name].transform.position = Vector2(x, y)
        
        for hook in self.on_text_updated:
            hook(self.text_objects[name])
        
        return True
    
    def remove_text(self, name: str) -> Optional[TextData]:
        """Remove a text object."""
        if name not in self.text_objects:
            return None
        
        text_obj = self.text_objects.pop(name)
        
        for hook in self.on_text_removed:
            hook(text_obj)
        
        return text_obj
    
    def get_all_text(self) -> List[TextData]:
        """Get all text objects."""
        return list(self.text_objects.values())
    
    def to_dict(self) -> dict:
        """Serialize text system state."""
        return {
            'fonts': {
                name: {'size': font.size}
                for name, font in self.fonts.items()
            },
            'text_objects': {
                name: {'text': obj.text, 'font': obj.font_name}
                for name, obj in self.text_objects.items()
            }
        }
