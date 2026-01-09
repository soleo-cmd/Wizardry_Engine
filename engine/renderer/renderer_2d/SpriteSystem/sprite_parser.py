"""
Sprite System - Parser layer for game code API

Provides convenient sprite loading and management functions.
"""

from typing import Optional
from .sprite import SpriteData, SpriteAnimation, AnimationFrame
from .sprite_system import SpriteSystem
from ..Core.renderer_config import Transform, Vector2, LayerType


class SpriteParser:
    """
    Game-facing API for sprite operations.
    
    Handles sprite loading, instance creation, and animation control.
    """
    
    def __init__(self, sprite_system: SpriteSystem):
        self.sprite_system = sprite_system
    
    def load_sprite(
        self,
        name: str,
        file_path: str,
        width: int,
        height: int,
        frames_per_row: int = 1,
        total_frames: int = 1,
    ) -> Optional[SpriteData]:
        """
        Load a sprite from an image file.
        
        Args:
            name: Unique name for this sprite
            file_path: Path to image (relative to assets/sprites)
            width: Width of each frame
            height: Height of each frame
            frames_per_row: Frames per row in sprite sheet
            total_frames: Total frames in sprite sheet
        
        Returns:
            SpriteData if successful
        
        Example:
            parser.load_sprite("player", "player.png", 32, 32, 4, 8)
        """
        return self.sprite_system.load_sprite(
            name=name,
            file_path=file_path,
            width=width,
            height=height,
            frames_per_row=frames_per_row,
            total_frames=total_frames,
        )
    
    def create_sprite(
        self,
        name: str,
        sprite_name: str,
        x: float = 0,
        y: float = 0,
    ) -> Optional[SpriteData]:
        """
        Create an instance of a loaded sprite at a position.
        
        Args:
            name: Name for this instance
            sprite_name: Name of loaded sprite to instantiate
            x: X position
            y: Y position
        
        Returns:
            SpriteData instance
        
        Example:
            parser.create_sprite("player_1", "player", 100, 100)
        """
        return self.sprite_system.create_sprite_instance(
            name=name,
            sprite_name=sprite_name,
            x=x,
            y=y,
        )
    
    def add_animation(
        self,
        sprite_name: str,
        animation_name: str,
        frames: list,  # List of (frame_index, duration) tuples
        looping: bool = True,
    ) -> bool:
        """
        Add an animation to a sprite.
        
        Args:
            sprite_name: Name of sprite
            animation_name: Name for this animation
            frames: List of (frame_index, duration) tuples
            looping: Whether animation loops
        
        Returns:
            True if successful
        
        Example:
            parser.add_animation("player", "walk", [(0, 0.1), (1, 0.1), (2, 0.1)], True)
        """
        sprite = self.sprite_system.get_sprite(sprite_name)
        if not sprite:
            return False
        
        animation = SpriteAnimation(
            name=animation_name,
            looping=looping
        )
        
        for frame_idx, duration in frames:
            animation.add_frame(AnimationFrame(frame_idx, duration))
        
        sprite.add_animation(animation)
        return True
    
    def play_animation(self, sprite_name: str, animation_name: str) -> bool:
        """
        Play an animation.
        
        Args:
            sprite_name: Name of sprite instance
            animation_name: Name of animation to play
        
        Returns:
            True if successful
        
        Example:
            parser.play_animation("player_1", "walk")
        """
        return self.sprite_system.play_animation(sprite_name, animation_name)
    
    def move_sprite(self, sprite_name: str, x: float, y: float) -> bool:
        """Move a sprite instance."""
        sprite = self.sprite_system.get_sprite(sprite_name)
        if sprite:
            sprite.transform.position = Vector2(x, y)
            return True
        return False
    
    def set_sprite_visible(self, sprite_name: str, visible: bool) -> bool:
        """Show or hide a sprite."""
        sprite = self.sprite_system.get_sprite(sprite_name)
        if sprite:
            sprite.set_visible(visible)
            return True
        return False
    
    def remove_sprite(self, sprite_name: str) -> bool:
        """Remove a sprite instance."""
        return self.sprite_system.remove_sprite(sprite_name)
    
    def get_sprite(self, sprite_name: str) -> Optional[SpriteData]:
        """Get a sprite by name."""
        return self.sprite_system.get_sprite(sprite_name)
