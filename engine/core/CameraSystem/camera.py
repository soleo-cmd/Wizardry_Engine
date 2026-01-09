# engine/core/CameraSystem/camera.py
from enum import Enum

class RenderMode(Enum):
    """
    Specifies which rendering pipeline to use.
    Engine doesn't know about graphics - just tracks the mode.
    Renderer interprets this and applies appropriate transformations.
    """
    MODE_2D = 1
    MODE_3D = 2

class Camera:
    """
    Engine-level camera data.
    Pure data class - no rendering logic.
    
    Stores:
    - Position (can be 2D or 3D world coordinates)
    - Viewport size (tiles/units visible)
    - Zoom level (magnification)
    - Render mode (2D vs 3D)
    - Target entity (optional - for following)
    
    Renderer interprets this data and applies visual transformations.
    """
    
    def __init__(
        self,
        name: str = "main_camera",
        position: tuple = (0, 0, 0),  # x, y, z (z unused in 2D)
        viewport_size: tuple = (8, 8),  # width, height in tiles/units
        zoom: float = 1.0,
        render_mode: RenderMode = RenderMode.MODE_2D,
        target_entity: str = None
    ):
        self.name = name
        self.position = position  # (x, y, z)
        self.viewport_size = viewport_size  # (width, height)
        self.zoom = zoom
        self.render_mode = render_mode
        self.target_entity = target_entity  # entity name to follow, or None
        self.data = {}  # arbitrary extra data
    
    # -------------------
    # Position Management
    # -------------------
    def set_position(self, x: float, y: float, z: float = 0):
        """Set camera position in world space."""
        self.position = (x, y, z)
    
    def get_position(self) -> tuple:
        """Get camera position as (x, y, z)."""
        return self.position
    
    def pan(self, dx: float, dy: float, dz: float = 0):
        """Move camera by delta."""
        x, y, z = self.position
        self.position = (x + dx, y + dy, z + dz)
    
    # -------------------
    # Viewport Management
    # -------------------
    def set_viewport_size(self, width: float, height: float):
        """Set how many tiles/units are visible."""
        self.viewport_size = (width, height)
    
    def get_viewport_size(self) -> tuple:
        """Get viewport as (width, height)."""
        return self.viewport_size
    
    # -------------------
    # Zoom Management
    # -------------------
    def set_zoom(self, zoom: float):
        """Set zoom level (1.0 = normal, 2.0 = 2x magnified)."""
        if zoom <= 0:
            raise ValueError("Zoom must be positive")
        self.zoom = zoom
    
    def get_zoom(self) -> float:
        return self.zoom
    
    # -------------------
    # Render Mode
    # -------------------
    def set_render_mode(self, mode: RenderMode):
        """Switch between 2D and 3D rendering."""
        self.render_mode = mode
    
    def get_render_mode(self) -> RenderMode:
        return self.render_mode
    
    def is_3d(self) -> bool:
        return self.render_mode == RenderMode.MODE_3D
    
    def is_2d(self) -> bool:
        return self.render_mode == RenderMode.MODE_2D
    
    # -------------------
    # Target Tracking
    # -------------------
    def set_target_entity(self, entity_name: str = None):
        """Set entity to follow, or None to stop tracking."""
        self.target_entity = entity_name
    
    def get_target_entity(self) -> str:
        return self.target_entity
    
    # -------------------
    # Visibility Culling (Engine-level logic)
    # -------------------
    def get_visible_area(self) -> dict:
        """
        Returns visible area bounds as engine would see it.
        Renderer uses this to determine what to draw.
        
        Returns: {
            'min_x': float,
            'max_x': float,
            'min_y': float,
            'max_y': float,
            'min_z': float,
            'max_z': float,
        }
        """
        x, y, z = self.position
        width, height = self.viewport_size
        
        # Account for zoom (higher zoom = smaller visible area)
        view_width = width / self.zoom
        view_height = height / self.zoom
        
        return {
            'min_x': x - view_width / 2,
            'max_x': x + view_width / 2,
            'min_y': y - view_height / 2,
            'max_y': y + view_height / 2,
            'min_z': z - 10,  # Arbitrary depth for 3D
            'max_z': z + 10,
        }
    
    def is_point_visible(self, x: float, y: float, z: float = 0) -> bool:
        """Check if world point is within visible area."""
        visible = self.get_visible_area()
        return (
            visible['min_x'] <= x <= visible['max_x'] and
            visible['min_y'] <= y <= visible['max_y'] and
            visible['min_z'] <= z <= visible['max_z']
        )
    
    # -------------------
    # Serialization
    # -------------------
    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "position": self.position,
            "viewport_size": self.viewport_size,
            "zoom": self.zoom,
            "render_mode": self.render_mode.name,
            "target_entity": self.target_entity,
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        render_mode = RenderMode[data.get("render_mode", "MODE_2D")]
        return cls(
            name=data.get("name", "main_camera"),
            position=tuple(data.get("position", (0, 0, 0))),
            viewport_size=tuple(data.get("viewport_size", (8, 8))),
            zoom=data.get("zoom", 1.0),
            render_mode=render_mode,
            target_entity=data.get("target_entity"),
        )
    
    def __repr__(self):
        return (
            f"<Camera '{self.name}' pos={self.position} "
            f"viewport={self.viewport_size} zoom={self.zoom} "
            f"mode={self.render_mode.name}>"
        )
