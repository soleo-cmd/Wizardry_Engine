"""
Sprite System - Engine layer for sprite management

Manages sprite loading, caching, and animation updates.
Completely independent from rendering backend.
"""

import os
from typing import Dict, Optional, Callable, List
from .sprite import SpriteData, SpriteAnimation, AnimationFrame
from ..Core.renderer_config import Transform, Vector2


class SpriteSystem:
    """
    Manages sprites and sprite animations.
    
    Handles sprite loading, caching, and animation frame updates.
    Backends register hooks to receive sprite update events.
    """
    
    def __init__(self, assets_path: str = "./assets/sprites"):
        """
        Initialize sprite system.
        
        Args:
            assets_path: Base path for sprite assets
        """
        self.assets_path = assets_path
        self.sprites: Dict[str, SpriteData] = {}
        self.sprite_cache: Dict[str, bytes] = {}  # For caching file data
        
        # Hooks
        self.on_sprite_loaded: List[Callable] = []
        self.on_animation_changed: List[Callable] = []
        self.on_frame_updated: List[Callable] = []
    
    def register_load_hook(self, hook: Callable):
        """Register hook for sprite loading."""
        if hook not in self.on_sprite_loaded:
            self.on_sprite_loaded.append(hook)
    
    def register_animation_hook(self, hook: Callable):
        """Register hook for animation changes."""
        if hook not in self.on_animation_changed:
            self.on_animation_changed.append(hook)
    
    def register_frame_hook(self, hook: Callable):
        """Register hook for frame updates."""
        if hook not in self.on_frame_updated:
            self.on_frame_updated.append(hook)
    
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
        Load a sprite from file.
        
        Args:
            name: Unique sprite name
            file_path: Path to sprite image (relative to assets_path)
            width: Sprite frame width
            height: Sprite frame height
            frames_per_row: Frames per row in sprite sheet
            total_frames: Total frames in sprite sheet
        
        Returns:
            SpriteData if successful, None if file not found
        """
        if name in self.sprites:
            raise ValueError(f"Sprite '{name}' already loaded")
        
        full_path = os.path.join(self.assets_path, file_path)
        
        # Check if file exists (in real scenario)
        # For now, we'll allow virtual sprites
        
        sprite = SpriteData(
            name=name,
            file_path=file_path,
            width=width,
            height=height,
            frames_per_row=frames_per_row,
            total_frames=total_frames,
        )
        
        self.sprites[name] = sprite
        
        # Trigger hooks
        for hook in self.on_sprite_loaded:
            hook(sprite)
        
        return sprite
    
    def get_sprite(self, name: str) -> Optional[SpriteData]:
        """Get a loaded sprite."""
        return self.sprites.get(name)
    
    def create_sprite_instance(
        self,
        name: str,
        sprite_name: str,
        x: float = 0,
        y: float = 0,
    ) -> Optional[SpriteData]:
        """
        Create an instance of a sprite (copy with independent transforms).
        
        Args:
            name: Name for this instance
            sprite_name: Name of sprite to instance
            x: Initial X position
            y: Initial Y position
        
        Returns:
            New SpriteData instance or None if sprite not found
        """
        if sprite_name not in self.sprites:
            return None
        
        if name in self.sprites:
            raise ValueError(f"Sprite instance '{name}' already exists")
        
        original = self.sprites[sprite_name]
        
        # Create a copy with new transform
        from dataclasses import replace
        
        instance = replace(
            original,
            name=name,
            transform=Transform(Vector2(x, y))
        )
        
        # Create new animation instances for this copy
        instance.animations = {
            anim_name: replace(anim)
            for anim_name, anim in original.animations.items()
        }
        
        self.sprites[name] = instance
        
        for hook in self.on_sprite_loaded:
            hook(instance)
        
        return instance
    
    def play_animation(self, sprite_name: str, animation_name: str) -> bool:
        """Play an animation on a sprite."""
        if sprite_name not in self.sprites:
            return False
        
        sprite = self.sprites[sprite_name]
        result = sprite.play_animation(animation_name)
        
        if result:
            for hook in self.on_animation_changed:
                hook(sprite, animation_name)
        
        return result
    
    def update(self, delta_time: float):
        """
        Update all sprite animations.
        
        Args:
            delta_time: Time elapsed since last update in seconds
        """
        for sprite in self.sprites.values():
            if sprite.current_animation:
                animation = sprite.animations[sprite.current_animation]
                
                if animation.playing and animation.frames:
                    animation.elapsed += delta_time
                    current_frame = animation.get_current_frame()
                    
                    if current_frame and animation.elapsed >= current_frame.duration:
                        animation.elapsed -= current_frame.duration
                        animation.current_frame += 1
                        
                        if animation.current_frame >= len(animation.frames):
                            if animation.looping:
                                animation.current_frame = 0
                            else:
                                animation.playing = False
                        
                        for hook in self.on_frame_updated:
                            hook(sprite, animation)
    
    def remove_sprite(self, name: str) -> bool:
        """Remove a sprite."""
        if name in self.sprites:
            del self.sprites[name]
            return True
        return False
    
    def get_all_sprites(self) -> List[SpriteData]:
        """Get all loaded sprites."""
        return list(self.sprites.values())
    
    def to_dict(self) -> dict:
        """Serialize sprite system state."""
        return {
            'sprites': {
                name: {
                    'file_path': sprite.file_path,
                    'width': sprite.width,
                    'height': sprite.height,
                }
                for name, sprite in self.sprites.items()
            }
        }
