# engine/core/CameraSystem/camera_system.py
from typing import Callable, Dict
from .camera import Camera, RenderMode

class CameraSystem:
    """
    Manages all cameras in the engine.
    
    Features:
    - Multiple cameras (though typically only one active)
    - Camera modes (2D vs 3D)
    - Entity tracking
    - Visibility culling
    - Hooks for renderer updates
    
    Completely headless - no rendering logic here.
    Renderer receives camera state and interprets it.
    """
    
    def __init__(self):
        self.cameras: Dict[str, Camera] = {}
        self.active_camera: str = None
        
        # Hooks that fire when camera state changes
        self.on_camera_created: Callable[[Camera], None] = None
        self.on_camera_updated: Callable[[Camera], None] = None
        self.on_camera_removed: Callable[[Camera], None] = None
        self.on_camera_mode_changed: Callable[[Camera, RenderMode], None] = None
    
    # -------------------
    # Camera Lifecycle
    # -------------------
    def create_camera(
        self,
        name: str,
        position: tuple = (0, 0, 0),
        viewport_size: tuple = (8, 8),
        zoom: float = 1.0,
        render_mode: RenderMode = RenderMode.MODE_2D,
    ) -> Camera:
        """Create and register a new camera."""
        if name in self.cameras:
            raise ValueError(f"Camera '{name}' already exists.")
        
        camera = Camera(
            name=name,
            position=position,
            viewport_size=viewport_size,
            zoom=zoom,
            render_mode=render_mode,
        )
        self.cameras[name] = camera
        
        # First camera becomes active by default
        if self.active_camera is None:
            self.active_camera = name
        
        if self.on_camera_created:
            self.on_camera_created(camera)
        
        return camera
    
    def get_camera(self, name: str) -> Camera:
        """Get camera by name."""
        return self.cameras.get(name)
    
    def get_active_camera(self) -> Camera:
        """Get currently active camera."""
        if self.active_camera is None:
            return None
        return self.cameras.get(self.active_camera)
    
    def set_active_camera(self, name: str):
        """Switch to a different camera."""
        if name not in self.cameras:
            raise ValueError(f"Camera '{name}' does not exist.")
        self.active_camera = name
        camera = self.cameras[name]
        if self.on_camera_updated:
            self.on_camera_updated(camera)
    
    def remove_camera(self, name: str):
        """Remove a camera."""
        camera = self.cameras.pop(name, None)
        if camera:
            if self.active_camera == name:
                self.active_camera = None
            if self.on_camera_removed:
                self.on_camera_removed(camera)
    
    # -------------------
    # Camera Movement
    # -------------------
    def pan_camera(self, name: str, dx: float, dy: float, dz: float = 0):
        """Move a camera by delta."""
        camera = self.get_camera(name)
        if camera:
            camera.pan(dx, dy, dz)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    def set_camera_position(self, name: str, x: float, y: float, z: float = 0):
        """Set camera position directly."""
        camera = self.get_camera(name)
        if camera:
            camera.set_position(x, y, z)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    # -------------------
    # Camera Viewport
    # -------------------
    def set_viewport_size(self, name: str, width: float, height: float):
        """Change what the camera can see."""
        camera = self.get_camera(name)
        if camera:
            camera.set_viewport_size(width, height)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    # -------------------
    # Zoom Control
    # -------------------
    def set_zoom(self, name: str, zoom: float):
        """Set zoom level."""
        camera = self.get_camera(name)
        if camera:
            camera.set_zoom(zoom)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    # -------------------
    # Render Mode (2D vs 3D)
    # -------------------
    def set_render_mode(self, name: str, mode: RenderMode):
        """Switch camera between 2D and 3D rendering."""
        camera = self.get_camera(name)
        if camera:
            old_mode = camera.get_render_mode()
            camera.set_render_mode(mode)
            if self.on_camera_mode_changed:
                self.on_camera_mode_changed(camera, old_mode)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    # -------------------
    # Entity Tracking
    # -------------------
    def set_camera_target(self, name: str, entity_name: str = None):
        """Make camera follow an entity."""
        camera = self.get_camera(name)
        if camera:
            camera.set_target_entity(entity_name)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    def update_camera_for_entity(self, name: str, entity_position: tuple):
        """
        Update camera position to track entity.
        Called externally when entity moves (e.g., from MovementSystem via hook).
        """
        camera = self.get_camera(name)
        if camera and camera.get_target_entity():
            # Center camera on entity
            ex, ey = entity_position[0], entity_position[1]
            camera.set_position(ex, ey, 0)
            if self.on_camera_updated:
                self.on_camera_updated(camera)
    
    # -------------------
    # Visibility Queries
    # -------------------
    def get_visible_area(self, name: str) -> dict:
        """Get visible area bounds for a camera."""
        camera = self.get_camera(name)
        if camera:
            return camera.get_visible_area()
        return None
    
    def is_point_visible(self, name: str, x: float, y: float, z: float = 0) -> bool:
        """Check if point is visible from a camera."""
        camera = self.get_camera(name)
        if camera:
            return camera.is_point_visible(x, y, z)
        return False
