"""
Comprehensive tests for the 2D Renderer

Tests all renderer systems: Drawing, Sprites, Text, and backends.
Uses headless backend for automated testing without display.
"""

import unittest
import sys
from pathlib import Path

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from engine.renderer import Renderer2D, RenderConfig, LayerType, Vector2, Color, Transform
from engine.renderer.renderer_2d.DrawingSystem.drawing import (
    DrawCommand, RectCommand, CircleCommand, LineCommand
)
from engine.renderer.renderer_2d.SpriteSystem.sprite import SpriteData, SpriteAnimation, AnimationFrame
from engine.renderer.renderer_2d.TextSystem.text import TextData


class TestRenderConfig(unittest.TestCase):
    """Test renderer configuration."""
    
    def test_render_config_defaults(self):
        """Test default config values."""
        config = RenderConfig()
        self.assertEqual(config.window_width, 1280)
        self.assertEqual(config.window_height, 720)
        self.assertEqual(config.fps, 60)
        self.assertFalse(config.headless)
        self.assertFalse(config.fullscreen)
    
    def test_render_config_custom(self):
        """Test custom config values."""
        config = RenderConfig(
            window_width=800,
            window_height=600,
            fps=30,
            headless=True
        )
        self.assertEqual(config.window_width, 800)
        self.assertEqual(config.window_height, 600)
        self.assertEqual(config.fps, 30)
        self.assertTrue(config.headless)
    
    def test_vector2(self):
        """Test Vector2 data."""
        v = Vector2(10, 20)
        self.assertEqual(v.x, 10)
        self.assertEqual(v.y, 20)
        self.assertEqual(v.to_tuple(), (10, 20))
    
    def test_color(self):
        """Test Color data."""
        c = Color(255, 128, 64, 200)
        self.assertEqual(c.r, 255)
        self.assertEqual(c.g, 128)
        self.assertEqual(c.b, 64)
        self.assertEqual(c.a, 200)
        self.assertEqual(c.to_tuple(), (255, 128, 64, 200))
    
    def test_transform(self):
        """Test Transform data."""
        transform = Transform(Vector2(100, 50), 45.0)
        self.assertEqual(transform.position.x, 100)
        self.assertEqual(transform.position.y, 50)
        self.assertEqual(transform.rotation, 45.0)
        self.assertEqual(transform.scale.x, 1.0)


class TestDrawingSystem(unittest.TestCase):
    """Test drawing system."""
    
    def setUp(self):
        """Set up test renderer."""
        config = RenderConfig(headless=True)
        self.renderer = Renderer2D(config=config, backend="headless")
        self.drawing = self.renderer.drawing()
    
    def test_draw_rect(self):
        """Test drawing rectangles."""
        name = self.drawing.draw_rect(10, 20, 50, 40, color=(255, 0, 0, 255))
        self.assertIsNotNone(name)
        
        command = self.renderer.drawing_system.get_command(name)
        self.assertIsNotNone(command)
        self.assertEqual(command.width, 50)
        self.assertEqual(command.height, 40)
    
    def test_draw_circle(self):
        """Test drawing circles."""
        name = self.drawing.draw_circle(100, 100, radius=25)
        self.assertIsNotNone(name)
        
        command = self.renderer.drawing_system.get_command(name)
        self.assertEqual(command.radius, 25)
    
    def test_draw_line(self):
        """Test drawing lines."""
        name = self.drawing.draw_line(0, 0, 100, 100)
        self.assertIsNotNone(name)
        
        command = self.renderer.drawing_system.get_command(name)
        self.assertEqual(command.end_x, 100)
        self.assertEqual(command.end_y, 100)
    
    def test_draw_polygon(self):
        """Test drawing polygons."""
        points = [(0, 0), (100, 0), (50, 100)]
        name = self.drawing.draw_polygon(points)
        self.assertIsNotNone(name)
    
    def test_update_position(self):
        """Test updating draw command position."""
        name = self.drawing.draw_rect(10, 10)
        self.drawing.update_position(name, 50, 50)
        
        command = self.renderer.drawing_system.get_command(name)
        self.assertEqual(command.transform.position.x, 50)
        self.assertEqual(command.transform.position.y, 50)
    
    def test_update_color(self):
        """Test updating draw command color."""
        name = self.drawing.draw_rect(10, 10, color=(100, 100, 100, 255))
        self.drawing.update_color(name, (255, 0, 0, 255))
        
        command = self.renderer.drawing_system.get_command(name)
        self.assertEqual(command.color, (255, 0, 0, 255))
    
    def test_show_hide(self):
        """Test showing/hiding draw commands."""
        name = self.drawing.draw_rect(10, 10)
        
        self.drawing.hide(name)
        command = self.renderer.drawing_system.get_command(name)
        self.assertFalse(command.is_visible())
        
        self.drawing.show(name)
        self.assertTrue(command.is_visible())
    
    def test_remove_command(self):
        """Test removing draw commands."""
        name = self.drawing.draw_rect(10, 10)
        self.assertIsNotNone(self.renderer.drawing_system.get_command(name))
        
        self.drawing.remove(name)
        self.assertIsNone(self.renderer.drawing_system.get_command(name))
    
    def test_layer_sorting(self):
        """Test drawing by layer."""
        self.drawing.draw_rect(10, 10, layer=LayerType.ENTITY)
        self.drawing.draw_rect(20, 20, layer=LayerType.BACKGROUND)
        self.drawing.draw_rect(30, 30, layer=LayerType.UI)
        
        all_commands = self.renderer.drawing_system.get_all_commands()
        self.assertEqual(len(all_commands), 3)


class TestSpriteSystem(unittest.TestCase):
    """Test sprite system."""
    
    def setUp(self):
        """Set up test renderer."""
        config = RenderConfig(headless=True)
        self.renderer = Renderer2D(config=config, backend="headless")
        self.sprites = self.renderer.sprites()
    
    def test_load_sprite(self):
        """Test loading sprites."""
        sprite_data = self.sprites.load_sprite(
            "player", "player.png", 32, 32, 4, 8
        )
        self.assertIsNotNone(sprite_data)
        self.assertEqual(sprite_data.name, "player")
        self.assertEqual(sprite_data.width, 32)
        self.assertEqual(sprite_data.height, 32)
    
    def test_create_sprite_instance(self):
        """Test creating sprite instances."""
        self.sprites.load_sprite("player", "player.png", 32, 32)
        instance = self.sprites.create_sprite("player_1", "player", 100, 150)
        
        self.assertIsNotNone(instance)
        self.assertEqual(instance.transform.position.x, 100)
        self.assertEqual(instance.transform.position.y, 150)
    
    def test_add_animation(self):
        """Test adding animations."""
        self.sprites.load_sprite("player", "player.png", 32, 32)
        
        result = self.sprites.add_animation(
            "player",
            "walk",
            [(0, 0.1), (1, 0.1), (2, 0.1), (3, 0.1)],
            looping=True
        )
        self.assertTrue(result)
        
        sprite = self.renderer.sprite_system.get_sprite("player")
        self.assertIn("walk", sprite.animations)
    
    def test_play_animation(self):
        """Test playing animations."""
        self.sprites.load_sprite("player", "player.png", 32, 32)
        self.sprites.add_animation("player", "walk", [(0, 0.1), (1, 0.1)])
        
        result = self.sprites.play_animation("player", "walk")
        self.assertTrue(result)
    
    def test_move_sprite(self):
        """Test moving sprites."""
        self.sprites.load_sprite("player", "player.png", 32, 32)
        self.sprites.create_sprite("player_1", "player", 10, 10)
        
        self.sprites.move_sprite("player_1", 50, 60)
        sprite = self.sprites.get_sprite("player_1")
        self.assertEqual(sprite.transform.position.x, 50)
        self.assertEqual(sprite.transform.position.y, 60)
    
    def test_sprite_visibility(self):
        """Test sprite visibility."""
        self.sprites.load_sprite("player", "player.png", 32, 32)
        self.sprites.create_sprite("player_1", "player")
        
        self.sprites.set_sprite_visible("player_1", False)
        sprite = self.sprites.get_sprite("player_1")
        self.assertFalse(sprite.is_visible)
        
        self.sprites.set_sprite_visible("player_1", True)
        self.assertTrue(sprite.is_visible)


class TestTextSystem(unittest.TestCase):
    """Test text system."""
    
    def setUp(self):
        """Set up test renderer."""
        config = RenderConfig(headless=True)
        self.renderer = Renderer2D(config=config, backend="headless")
        self.text = self.renderer.text()
    
    def test_load_font(self):
        """Test loading fonts."""
        font = self.text.load_font(
            "title", "arial.ttf", size=32, bold=True
        )
        self.assertIsNotNone(font)
        self.assertEqual(font.name, "title")
        self.assertEqual(font.size, 32)
        self.assertTrue(font.bold)
    
    def test_render_text(self):
        """Test rendering text."""
        name = self.text.render_text(
            "Hello World", 10, 20, font_name="default"
        )
        self.assertIsNotNone(name)
        
        text_obj = self.renderer.text_system.get_text(name)
        self.assertEqual(text_obj.text, "Hello World")
    
    def test_update_text(self):
        """Test updating text content."""
        name = self.text.render_text("Score: 0", 10, 10)
        self.text.update_text(name, "Score: 100")
        
        text_obj = self.text.get_text(name)
        self.assertEqual(text_obj.text, "Score: 100")
    
    def test_move_text(self):
        """Test moving text."""
        name = self.text.render_text("Hello", 10, 10)
        self.text.move_text(name, 50, 60)
        
        text_obj = self.text.get_text(name)
        self.assertEqual(text_obj.transform.position.x, 50)
        self.assertEqual(text_obj.transform.position.y, 60)
    
    def test_remove_text(self):
        """Test removing text."""
        name = self.text.render_text("Temporary", 10, 10)
        self.text.remove_text(name)
        
        text_obj = self.text.get_text(name)
        self.assertIsNone(text_obj)


class TestHeadlessBackend(unittest.TestCase):
    """Test headless renderer backend."""
    
    def setUp(self):
        """Set up test renderer."""
        config = RenderConfig(headless=True, fps=60)
        self.renderer = Renderer2D(config=config, backend="headless")
    
    def test_headless_backend_type(self):
        """Test backend type."""
        self.assertEqual(self.renderer.get_backend_type(), "headless")
    
    def test_render_recording(self):
        """Test render recording."""
        drawing = self.renderer.drawing()
        drawing.draw_rect(10, 10, 50, 50)
        
        self.renderer.clear()
        self.renderer.render()
        self.renderer.present()
        
        log = self.renderer.backend.get_render_log()
        self.assertGreater(len(log), 0)
    
    def test_frame_counting(self):
        """Test frame counting."""
        backend = self.renderer.backend
        self.assertEqual(backend.get_frame_count(), 0)
        
        backend.update_display()
        self.assertEqual(backend.get_frame_count(), 1)
        
        backend.update_display()
        self.assertEqual(backend.get_frame_count(), 2)
    
    def test_delta_time(self):
        """Test delta time calculation."""
        backend = self.renderer.backend
        backend.tick()
        delta = backend.get_delta_time()
        self.assertAlmostEqual(delta, 1.0 / 60.0, places=3)


class TestRenderer2DIntegration(unittest.TestCase):
    """Integration tests for complete renderer."""
    
    def test_full_render_flow(self):
        """Test complete rendering flow."""
        config = RenderConfig(headless=True)
        renderer = Renderer2D(config=config, backend="headless")
        
        # Use all APIs
        drawing = renderer.drawing()
        sprites = renderer.sprites()
        text = renderer.text()
        
        # Draw shapes
        rect = drawing.draw_rect(10, 10, 50, 50)
        circle = drawing.draw_circle(100, 100, 25)
        
        # Create sprite
        sprites.load_sprite("test", "test.png", 32, 32)
        sprite_inst = sprites.create_sprite("test_1", "test", 50, 50)
        
        # Render text
        text_obj = text.render_text("Test", 20, 20)
        
        # Render frame
        renderer.clear((255, 255, 255))
        renderer.render()
        renderer.present()
        
        # Verify
        self.assertIsNotNone(drawing.draw_rect(10, 10))
        
        renderer.shutdown()
    
    def test_multiple_draw_commands(self):
        """Test rendering multiple draw commands."""
        config = RenderConfig(headless=True)
        renderer = Renderer2D(config=config, backend="headless")
        drawing = renderer.drawing()
        
        # Create many commands
        for i in range(10):
            drawing.draw_rect(i * 10, i * 10, 20, 20)
        
        commands = renderer.drawing_system.get_all_commands()
        self.assertEqual(len(commands), 10)
        
        renderer.shutdown()
    
    def test_state_serialization(self):
        """Test getting renderer state."""
        config = RenderConfig(headless=True, window_width=1024, window_height=768)
        renderer = Renderer2D(config=config, backend="headless")
        
        drawing = renderer.drawing()
        drawing.draw_rect(10, 10)
        
        state = renderer.get_state()
        self.assertEqual(state['config']['window_width'], 1024)
        self.assertEqual(state['config']['window_height'], 768)
        self.assertIn('drawing', state)
        self.assertIn('sprites', state)
        self.assertIn('text', state)
        
        renderer.shutdown()


if __name__ == "__main__":
    unittest.main()
