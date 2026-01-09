"""
Sprite System - Data layer for sprites and animations

Defines sprite data structures and animation frame management.
"""

from dataclasses import dataclass, field
from typing import Optional, List, Dict
from ..Core.renderer_config import Transform, Vector2, RenderableType, RenderableFlags


@dataclass
class AnimationFrame:
    """Single frame in a sprite animation."""
    frame_index: int
    duration: float  # Duration in seconds
    flip_x: bool = False
    flip_y: bool = False


@dataclass
class SpriteAnimation:
    """Animation sequence for a sprite."""
    name: str
    frames: List[AnimationFrame] = field(default_factory=list)
    looping: bool = True
    current_frame: int = 0
    elapsed: float = 0.0
    playing: bool = False
    
    def add_frame(self, frame: AnimationFrame):
        """Add a frame to the animation."""
        self.frames.append(frame)
    
    def get_current_frame(self) -> Optional[AnimationFrame]:
        """Get the current frame."""
        if 0 <= self.current_frame < len(self.frames):
            return self.frames[self.current_frame]
        return None
    
    def __repr__(self):
        return f"<Animation '{self.name}' frames={len(self.frames)}>"


@dataclass
class SpriteData:
    """Sprite data container."""
    name: str
    file_path: str
    width: int
    height: int
    transform: Transform = None
    frames_per_row: int = 1
    total_frames: int = 1
    animations: Dict[str, SpriteAnimation] = field(default_factory=dict)
    current_animation: Optional[str] = None
    is_visible: bool = True
    flags: RenderableFlags = RenderableFlags.VISIBLE
    
    def __post_init__(self):
        if self.transform is None:
            self.transform = Transform(Vector2(0, 0))
    
    def add_animation(self, animation: SpriteAnimation):
        """Add an animation to this sprite."""
        self.animations[animation.name] = animation
    
    def play_animation(self, name: str) -> bool:
        """Play an animation."""
        if name in self.animations:
            if self.current_animation:
                self.animations[self.current_animation].playing = False
            self.current_animation = name
            self.animations[name].playing = True
            self.animations[name].current_frame = 0
            self.animations[name].elapsed = 0.0
            return True
        return False
    
    def set_visible(self, visible: bool):
        """Set visibility."""
        if visible:
            self.flags |= RenderableFlags.VISIBLE
        else:
            self.flags &= ~RenderableFlags.VISIBLE
        self.is_visible = visible
    
    def __repr__(self):
        return f"<Sprite '{self.name}' {self.width}x{self.height}>"
