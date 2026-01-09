# engine/core/CameraSystem/camera_parser.py
from typing import Callable
from .camera import Camera, RenderMode
from .camera_system import CameraSystem

class CameraParser:
    """
    Game-facing API for camera management.
    
    The game calls methods here to control the camera.
    Hooks notify the renderer when camera changes.
    
    Example:
        camera_parser = CameraParser()
        
        # Create camera for 8x8 town view
        camera_parser.create_camera('town_cam', viewport_size=(8, 8))
        
        # Later, switch to dungeon with different viewport
        camera_parser.create_camera('dungeon_cam', viewport_size=(30, 30))
        camera_parser.set_active_camera('dungeon_cam')
        
        # Track player
        camera_parser.follow_entity('player')
        
        # Eventually switch to 3D
        camera_parser.set_render_mode(RenderMode.MODE_3D)
    """
    
    def __init__(self):
        self.system = CameraSystem()
    
    # -------------------
    # Camera Creation
    # -------------------
    def create_camera(
        self,
        name: str,
        position: tuple = (0, 0, 0),
        viewport_size: tuple = (8, 8),
        zoom: float = 1.0,
        render_mode: RenderMode = RenderMode.MODE_2D,
    ) -> Camera:
        """
        Create a new camera.
        
        Args:
            name: Unique camera identifier
            position: (x, y, z) in world coordinates
            viewport_size: (width, height) tiles/units visible
            zoom: Magnification level (1.0 = normal)
            render_mode: MODE_2D or MODE_3D
        """
        return self.system.create_camera(name, position, viewport_size, zoom, render_mode)
    
    def get_camera(self, name: str) -> Camera:
        """Get a camera by name."""
        return self.system.get_camera(name)
    
    def get_active_camera(self) -> Camera:
        """Get the currently active camera."""
        return self.system.get_active_camera()
    
    def set_active_camera(self, name: str):
        """Switch to a different camera."""
        self.system.set_active_camera(name)
    
    def remove_camera(self, name: str):
        """Remove a camera."""
        self.system.remove_camera(name)
    
    # -------------------
    # Camera Movement
    # -------------------
    def pan_camera(self, name: str, dx: float, dy: float, dz: float = 0):
        """Move camera by delta."""
        self.system.pan_camera(name, dx, dy, dz)
    
    def pan_active_camera(self, dx: float, dy: float, dz: float = 0):
        """Move the active camera by delta."""
        if self.system.active_camera:
            self.system.pan_camera(self.system.active_camera, dx, dy, dz)
    
    def set_camera_position(self, name: str, x: float, y: float, z: float = 0):
        """Set camera position directly."""
        self.system.set_camera_position(name, x, y, z)
    
    def set_active_camera_position(self, x: float, y: float, z: float = 0):
        """Set active camera position directly."""
        if self.system.active_camera:
            self.system.set_camera_position(self.system.active_camera, x, y, z)
    
    # -------------------
    # Viewport Control (for different scene sizes)
    # -------------------
    def set_viewport_size(self, name: str, width: float, height: float):
        """
        Change camera viewport (e.g., 8x8 for town, 30x30 for dungeon).
        This controls how many tiles are visible.
        """
        self.system.set_viewport_size(name, width, height)
    
    def set_active_viewport_size(self, width: float, height: float):
        """Set viewport for active camera."""
        if self.system.active_camera:
            self.system.set_viewport_size(self.system.active_camera, width, height)
    
    # -------------------
    # Zoom
    # -------------------
    def set_zoom(self, name: str, zoom: float):
        """Set camera zoom level."""
        self.system.set_zoom(name, zoom)
    
    def set_active_zoom(self, zoom: float):
        """Set zoom for active camera."""
        if self.system.active_camera:
            self.system.set_zoom(self.system.active_camera, zoom)
    
    # -------------------
    # Render Mode (2D vs 3D switching)
    # -------------------
    def set_render_mode(self, name: str, mode: RenderMode):
        """
        Switch camera to 2D or 3D mode.
        
        This is the key for Wizardry engine - when you're ready to go 3D,
        call this and the renderer will adapt automatically.
        """
        self.system.set_render_mode(name, mode)
    
    def set_active_render_mode(self, mode: RenderMode):
        """Switch render mode for active camera."""
        if self.system.active_camera:
            self.system.set_render_mode(self.system.active_camera, mode)
    
    # -------------------
    # Entity Tracking
    # -------------------
    def follow_entity(self, name: str, entity_name: str = None):
        """Make camera follow an entity."""
        self.system.set_camera_target(name, entity_name)
    
    def follow_entity_with_active_camera(self, entity_name: str = None):
        """Make active camera follow an entity."""
        if self.system.active_camera:
            self.system.set_camera_target(self.system.active_camera, entity_name)
    
    def update_camera_for_entity_position(self, name: str, entity_position: tuple):
        """
        Called when tracked entity moves.
        Typically connected via hook from MovementSystem.
        """
        self.system.update_camera_for_entity(name, entity_position)
    
    # -------------------
    # Visibility Queries
    # -------------------
    def get_visible_area(self, name: str = None) -> dict:
        """
        Get visible area for camera.
        If name is None, use active camera.
        """
        if name is None:
            name = self.system.active_camera
        return self.system.get_visible_area(name)
    
    def is_point_visible(self, x: float, y: float, z: float = 0, name: str = None) -> bool:
        """
        Check if point is visible from camera.
        If name is None, use active camera.
        """
        if name is None:
            name = self.system.active_camera
        return self.system.is_point_visible(name, x, y, z)
    
    # -------------------
    # Hooks for Renderer/Game
    # -------------------
    def set_camera_created_hook(self, hook: Callable[[Camera], None]):
        """Called when a camera is created."""
        self.system.on_camera_created = hook
    
    def set_camera_updated_hook(self, hook: Callable[[Camera], None]):
        """Called when camera state changes (move, zoom, etc)."""
        self.system.on_camera_updated = hook
    
    def set_camera_removed_hook(self, hook: Callable[[Camera], None]):
        """Called when a camera is removed."""
        self.system.on_camera_removed = hook
    
    def set_camera_mode_changed_hook(self, hook: Callable[[Camera, RenderMode], None]):
        """Called when render mode changes (2D vs 3D)."""
        self.system.on_camera_mode_changed = hook
