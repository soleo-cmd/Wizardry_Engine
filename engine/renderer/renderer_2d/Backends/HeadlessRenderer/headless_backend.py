"""
Headless Renderer Backend

Renders without display for testing and server environments.
Receives draw commands via hooks from DrawingSystem, SpriteSystem, TextSystem.
Records render data for verification in tests.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class RenderRecord:
    """Record of a render operation for testing."""
    command_type: str
    data: dict


class HeadlessRenderer:
    """
    Headless 2D renderer for testing and server environments.
    
    Records all render operations without displaying to screen.
    Useful for testing and headless game servers.
    """
    
    def __init__(self, config=None):
        """
        Initialize headless renderer.
        
        Args:
            config: RenderConfig object
        """
        self.config = config
        self.render_log: List[RenderRecord] = []
        self.fps = config.fps if config else 60
        self.delta_time = 0.0
        self.frame_count = 0
    
    def render_shapes(self, commands: List):
        """
        Record drawing commands.
        
        Args:
            commands: List of DrawCommand objects
        """
        for command in commands:
            if command.is_visible():
                self.render_log.append(RenderRecord(
                    command_type=command.command_type,
                    data={
                        'name': command.name,
                        'position': command.transform.position.to_tuple(),
                        'layer': command.layer.name,
                        **command.__dict__
                    }
                ))
    
    def render_sprites(self, sprites: List):
        """
        Record sprite rendering.
        
        Args:
            sprites: List of SpriteData objects
        """
        for sprite in sprites:
            if sprite.is_visible:
                self.render_log.append(RenderRecord(
                    command_type="sprite",
                    data={
                        'name': sprite.name,
                        'position': sprite.transform.position.to_tuple(),
                        'width': sprite.width,
                        'height': sprite.height,
                        'file_path': sprite.file_path,
                    }
                ))
    
    def render_text(self, text_objects: List):
        """
        Record text rendering.
        
        Args:
            text_objects: List of TextData objects
        """
        for text_obj in text_objects:
            if text_obj.is_visible:
                self.render_log.append(RenderRecord(
                    command_type="text",
                    data={
                        'name': text_obj.name,
                        'text': text_obj.text,
                        'position': text_obj.transform.position.to_tuple(),
                        'font': text_obj.font_name,
                        'color': text_obj.color,
                    }
                ))
    
    def clear_screen(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Record screen clear."""
        self.render_log.append(RenderRecord(
            command_type="clear",
            data={'color': color}
        ))
    
    def update_display(self):
        """Record display update."""
        self.frame_count += 1
        self.render_log.append(RenderRecord(
            command_type="frame_end",
            data={'frame': self.frame_count}
        ))
    
    def process_events(self) -> List:
        """
        Process events (no actual events in headless mode).
        
        Returns:
            Empty list
        """
        return []
    
    def tick(self):
        """Simulate tick."""
        self.delta_time = 1.0 / self.fps
    
    def get_delta_time(self) -> float:
        """Get elapsed time."""
        return self.delta_time
    
    def get_render_log(self) -> List[RenderRecord]:
        """Get all recorded render operations."""
        return list(self.render_log)
    
    def get_frame_count(self) -> int:
        """Get number of frames rendered."""
        return self.frame_count
    
    def clear_log(self):
        """Clear render log."""
        self.render_log.clear()
    
    def shutdown(self):
        """Clean up (no-op for headless)."""
        pass
