"""
Main 2D Renderer - Coordinates all rendering systems

Integrates DrawingSystem, SpriteSystem, TextSystem with backends.
All systems communicate through hooks - complete decoupling.
"""

from typing import Optional, Literal
from .Core.renderer_config import RenderConfig
from .DrawingSystem.drawing_system import DrawingSystem
from .DrawingSystem.drawing_parser import DrawingParser
from .SpriteSystem.sprite_system import SpriteSystem
from .SpriteSystem.sprite_parser import SpriteParser
from .TextSystem.text_system import TextSystem
from .TextSystem.text_parser import TextParser
from .Backends.PygameRenderer.pygame_backend import PygameRenderer
from .Backends.HeadlessRenderer.headless_backend import HeadlessRenderer


class Renderer2D:
    """
    Main 2D renderer that coordinates all rendering systems.
    
    Features:
    - Independent DrawingSystem (shapes, rectangles, lines)
    - Independent SpriteSystem (sprites with animations)
    - Independent TextSystem (text rendering with fonts)
    - Dual backends: Pygame (visual) and Headless (testing)
    - Complete hook-based integration (no direct coupling)
    
    Usage:
        renderer = Renderer2D(backend="pygame")
        drawing_api = renderer.drawing()
        sprite_api = renderer.sprites()
        text_api = renderer.text()
        
        # Use APIs
        drawing_api.draw_rect(100, 100, 50, 50)
        sprite_api.load_sprite("player", "player.png", 32, 32)
        text_api.render_text("Hello", 10, 10)
        
        # Render frame
        renderer.clear()
        renderer.render()
        renderer.present()
    """
    
    def __init__(
        self,
        config: Optional[RenderConfig] = None,
        backend: Literal["pygame", "headless"] = "pygame",
    ):
        """
        Initialize Renderer2D.
        
        Args:
            config: RenderConfig with display settings
            backend: "pygame" for visual or "headless" for testing
        """
        self.config = config or RenderConfig()
        self.backend_type = backend
        
        # Initialize systems (completely independent)
        self.drawing_system = DrawingSystem()
        self.sprite_system = SpriteSystem()
        self.text_system = TextSystem()
        
        # Create parsers (game-facing APIs)
        self._drawing_parser = DrawingParser(self.drawing_system)
        self._sprite_parser = SpriteParser(self.sprite_system)
        self._text_parser = TextParser(self.text_system)
        
        # Create backend
        if backend == "headless":
            self.backend = HeadlessRenderer(self.config)
        else:
            self.backend = PygameRenderer(self.config)
        
        # Register hooks to connect systems to backend
        self._setup_hooks()
    
    def _setup_hooks(self):
        """Setup system-to-backend hooks."""
        # Drawing hooks
        self.drawing_system.register_draw_hook(
            self.backend.render_shapes
        )
        
        # Sprite hooks
        self.sprite_system.register_load_hook(
            lambda sprite: None  # Backend handles rendering via render frame
        )
        
        # Text hooks
        self.text_system.register_text_add_hook(
            lambda text: None  # Backend handles rendering via render frame
        )
    
    def drawing(self) -> DrawingParser:
        """Get drawing API for game code."""
        return self._drawing_parser
    
    def sprites(self) -> SpriteParser:
        """Get sprite API for game code."""
        return self._sprite_parser
    
    def text(self) -> TextParser:
        """Get text API for game code."""
        return self._text_parser
    
    def clear(self, color: tuple = (0, 0, 0)):
        """Clear screen with color."""
        self.backend.clear_screen(color)
    
    def render(self):
        """
        Render all systems.
        
        Calls backend hooks for all visible objects from each system.
        """
        # Render shapes
        self.drawing_system.draw()
        
        # Render sprites
        sprites = self.sprite_system.get_all_sprites()
        if sprites:
            self.backend.render_sprites(sprites)
        
        # Render text
        text_objects = self.text_system.get_all_text()
        if text_objects:
            self.backend.render_text(text_objects)
    
    def present(self):
        """Update display (platform-specific)."""
        self.backend.update_display()
    
    def update(self, delta_time: float):
        """
        Update all systems.
        
        Args:
            delta_time: Time since last update in seconds
        """
        self.sprite_system.update(delta_time)
    
    def tick(self):
        """Tick the clock."""
        self.backend.tick()
    
    def get_delta_time(self) -> float:
        """Get time since last tick."""
        return self.backend.get_delta_time()
    
    def process_events(self):
        """Process input events."""
        return self.backend.process_events()
    
    def get_backend_type(self) -> str:
        """Get current backend type."""
        return self.backend_type
    
    def shutdown(self):
        """Clean up resources."""
        self.backend.shutdown()
    
    def get_state(self) -> dict:
        """Get full renderer state for serialization."""
        return {
            'config': {
                'window_width': self.config.window_width,
                'window_height': self.config.window_height,
                'fps': self.config.fps,
            },
            'drawing': self.drawing_system.to_dict(),
            'sprites': self.sprite_system.to_dict(),
            'text': self.text_system.to_dict(),
        }
