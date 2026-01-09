"""
Pygame Renderer Backend

Implements drawing using pygame for visual display.
Receives draw commands via hooks from DrawingSystem, SpriteSystem, TextSystem.
"""

import sys
from typing import Optional, List, Dict, Tuple
try:
    import pygame
except ImportError:
    pygame = None


class PygameRenderer:
    """
    Pygame-based 2D renderer.
    
    Handles actual rendering to screen using pygame.
    Completely decoupled from systems - communicates only via hooks.
    """
    
    def __init__(self, config=None):
        """
        Initialize Pygame renderer.
        
        Args:
            config: RenderConfig object with display settings
        """
        if pygame is None:
            raise ImportError("pygame not installed. Install with: pip install pygame")
        
        self.config = config
        self.screen: Optional[pygame.Surface] = None
        self.clock: Optional[pygame.time.Clock] = None
        self.font_cache: Dict[Tuple[str, int], pygame.font.Font] = {}
        self.sprite_cache: Dict[str, pygame.Surface] = {}
        self.running = False
        self.fps = config.fps if config else 60
        
        self._init_pygame()
    
    def _init_pygame(self):
        """Initialize pygame."""
        pygame.init()
        
        if not self.config.headless:
            flags = pygame.FULLSCREEN if self.config.fullscreen else 0
            self.screen = pygame.display.set_mode(
                (self.config.window_width, self.config.window_height),
                flags=flags,
                vsync=int(self.config.vsync)
            )
            pygame.display.set_caption(self.config.window_title)
        
        self.clock = pygame.time.Clock()
    
    def render_shapes(self, commands: List):
        """
        Render drawing commands.
        
        Args:
            commands: List of DrawCommand objects from DrawingSystem
        """
        if not self.screen:
            return
        
        for command in commands:
            if not command.is_visible():
                continue
            
            pos = command.transform.position.to_tuple()
            
            if command.command_type == "rect":
                pygame.draw.rect(
                    self.screen,
                    command.color[:3],  # RGB only for pygame
                    (*pos, command.width, command.height),
                    width=0 if command.fill else command.border_width,
                )
            
            elif command.command_type == "circle":
                pygame.draw.circle(
                    self.screen,
                    command.color[:3],
                    (int(pos[0]), int(pos[1])),
                    int(command.radius),
                    width=0 if command.fill else command.border_width,
                )
            
            elif command.command_type == "line":
                pygame.draw.line(
                    self.screen,
                    command.color[:3],
                    pos,
                    (command.end_x, command.end_y),
                    width=command.width,
                )
            
            elif command.command_type == "polygon":
                if len(command.points) > 2:
                    pygame.draw.polygon(
                        self.screen,
                        command.color[:3],
                        command.points,
                        width=0 if command.fill else command.border_width,
                    )
    
    def render_sprites(self, sprites: List):
        """
        Render sprites.
        
        Args:
            sprites: List of SpriteData objects from SpriteSystem
        """
        if not self.screen:
            return
        
        for sprite in sprites:
            if not sprite.is_visible:
                continue
            
            # In real implementation, would load actual sprite files
            # For now, render as placeholder rectangle
            pos = sprite.transform.position.to_tuple()
            pygame.draw.rect(
                self.screen,
                (100, 150, 255),
                (*pos, sprite.width, sprite.height),
            )
    
    def render_text(self, text_objects: List):
        """
        Render text.
        
        Args:
            text_objects: List of TextData objects from TextSystem
        """
        if not self.screen:
            return
        
        for text_obj in text_objects:
            if not text_obj.is_visible:
                continue
            # Determine font size: prefer per-text custom_data, fall back to 12
            size = 12
            try:
                if "font_size" in text_obj.custom_data:
                    size = int(text_obj.custom_data["font_size"])
            except Exception:
                size = 12

            # Get or create font
            font_key = (text_obj.font_name, size)
            if font_key not in self.font_cache:
                # If a file-based font is available, it should have been loaded
                # by TextSystem; here we use pygame default font if not present
                self.font_cache[font_key] = pygame.font.Font(None, size)

            font = self.font_cache[font_key]
            text_surface = font.render(text_obj.text, True, text_obj.color[:3])

            pos = text_obj.transform.position.to_tuple()
            self.screen.blit(text_surface, (int(pos[0]), int(pos[1])))
    
    def clear_screen(self, color: Tuple[int, int, int] = (0, 0, 0)):
        """Clear screen with color."""
        if self.screen:
            self.screen.fill(color)
    
    def update_display(self):
        """Update the display."""
        if self.screen:
            pygame.display.flip()
    
    def process_events(self) -> List:
        """
        Process pygame events.
        
        Returns:
            List of simplified event dicts with keys: 'type' and optional 'key'
        """
        out_events = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                out_events.append({'type': 'QUIT'})
                continue

            # Convert key events to a small backend-agnostic format
            if event.type == pygame.KEYDOWN and hasattr(event, 'key'):
                try:
                    name = pygame.key.name(event.key)
                    out_events.append({'type': 'KEYDOWN', 'key': name.upper()})
                except Exception:
                    out_events.append({'type': 'KEYDOWN', 'key': None})

            elif event.type == pygame.KEYUP and hasattr(event, 'key'):
                try:
                    name = pygame.key.name(event.key)
                    out_events.append({'type': 'KEYUP', 'key': name.upper()})
                except Exception:
                    out_events.append({'type': 'KEYUP', 'key': None})

            else:
                # For other events, include their type name if possible
                out_events.append({'type': str(event.type)})

        return out_events
    
    def tick(self):
        """Tick the clock."""
        if self.clock:
            self.clock.tick(self.fps)
    
    def get_delta_time(self) -> float:
        """Get time since last tick in seconds."""
        if self.clock:
            return self.clock.get_time() / 1000.0
        return 0.0
    
    def shutdown(self):
        """Clean up pygame."""
        pygame.quit()
