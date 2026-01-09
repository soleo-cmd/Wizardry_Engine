## Wizardry Engine - 2D Renderer Documentation

### Overview

The Wizardry 2D Renderer is a **completely modular, hook-based rendering system** that operates independently from game logic. It features three independent subsystems (Drawing, Sprites, Text) that can be used together or separately, with dual backends for both visual rendering (Pygame) and headless testing.

**Key Architecture Principle:** All systems communicate through hooks, maintaining complete decoupling. The renderer doesn't know about or depend on any game systems.

### Features

✅ **Three Independent Rendering Systems**
- **DrawingSystem**: Shapes, rectangles, circles, lines, polygons
- **SpriteSystem**: Sprite loading, animation, sprite instances
- **TextSystem**: Text rendering, font management

✅ **Dual Backend Support**
- **PygameRenderer**: Visual rendering with Pygame
- **HeadlessRenderer**: Headless rendering for testing and servers

✅ **Hook-Based Integration**
- Systems register hooks with backends
- Completely decoupled from game code
- Zero dependencies on engine systems

✅ **Comprehensive Test Suite**
- 32 tests covering all systems
- 100% pass rate
- Headless testing without display

### Architecture

```
Renderer2D (Main Coordinator)
├── DrawingSystem
│   ├── drawing.py (Data: DrawCommand, RectCommand, etc.)
│   ├── drawing_system.py (Engine: Management & hooks)
│   └── drawing_parser.py (API: draw_rect, draw_circle, etc.)
├── SpriteSystem
│   ├── sprite.py (Data: SpriteData, Animation)
│   ├── sprite_system.py (Engine: Loading & updates)
│   └── sprite_parser.py (API: load_sprite, create_sprite, etc.)
├── TextSystem
│   ├── text.py (Data: TextData, FontConfig)
│   ├── text_system.py (Engine: Font & text management)
│   └── text_parser.py (API: render_text, load_font, etc.)
└── Backends
    ├── PygameRenderer/ (Visual rendering)
    └── HeadlessRenderer/ (Testing/server rendering)
```

### Three-Layer Pattern

Like all Wizardry engine systems, the renderer follows a **Data → System → Parser** architecture:

1. **Data Layer** (`drawing.py`, `sprite.py`, `text.py`)
   - Pure dataclasses with no logic
   - Define structure and state
   - Example: `RectCommand`, `SpriteData`, `TextData`

2. **System Layer** (`drawing_system.py`, `sprite_system.py`, `text_system.py`)
   - Business logic and management
   - Hook-based communication with backends
   - Independent from rendering backend
   - Example: Command registration, animation updates

3. **Parser Layer** (`drawing_parser.py`, `sprite_parser.py`, `text_parser.py`)
   - Game-facing convenient API
   - Translates game code into system operations
   - Example: `draw_rect()`, `load_sprite()`, `render_text()`

### Quick Start

#### Basic Setup

```python
from engine.renderer import Renderer2D, RenderConfig

# Create renderer
config = RenderConfig(
    window_title="My Game",
    window_width=1280,
    window_height=720,
    headless=False  # True for testing
)
renderer = Renderer2D(config=config, backend="pygame")

# Get API parsers
drawing = renderer.drawing()
sprites = renderer.sprites()
text = renderer.text()
```

#### Drawing Shapes

```python
# Draw rectangle
rect_id = drawing.draw_rect(10, 20, width=50, height=40, color=(255, 0, 0, 255))

# Draw circle
circle_id = drawing.draw_circle(100, 100, radius=25, color=(0, 255, 0, 255))

# Draw line
line_id = drawing.draw_line(0, 0, 100, 100, color=(0, 0, 255, 255))

# Manipulate commands
drawing.update_position(rect_id, 50, 50)
drawing.update_color(rect_id, (255, 255, 0, 255))
drawing.hide(rect_id)
drawing.show(rect_id)
drawing.remove(rect_id)
```

#### Working with Sprites

```python
# Load a sprite
sprites.load_sprite("player", "player.png", width=32, height=32, 4, 8)

# Create an instance at a position
player = sprites.create_sprite("player_1", "player", x=100, y=100)

# Add animation
sprites.add_animation(
    "player",
    "walk",
    frames=[(0, 0.1), (1, 0.1), (2, 0.1), (3, 0.1)],
    looping=True
)

# Play animation
sprites.play_animation("player", "walk")

# Move sprite
sprites.move_sprite("player_1", x=150, y=100)

# Control visibility
sprites.set_sprite_visible("player_1", False)
sprites.set_sprite_visible("player_1", True)
```

#### Rendering Text

```python
# Load font
fonts = text.load_font("title", "arial.ttf", size=32, bold=True)

# Render text
score_text = text.render_text(
    "Score: 0",
    x=10, y=10,
    font_name="default",
    color=(255, 255, 255, 255)
)

# Update text
text.update_text(score_text, "Score: 100")

# Move text
text.move_text(score_text, 50, 50)

# Remove text
text.remove_text(score_text)
```

#### Game Loop

```python
running = True
while running:
    # Update
    delta = renderer.get_delta_time()
    renderer.update(delta)
    
    # Render
    renderer.clear((0, 0, 0))  # Clear with black
    renderer.render()
    renderer.present()
    
    # Input
    events = renderer.process_events()
    
    # Frame timing
    renderer.tick()

renderer.shutdown()
```

### Layers (Z-Ordering)

Draw commands support layer-based z-ordering:

```python
from engine.renderer import LayerType

# Available layers (in order):
# LayerType.BACKGROUND
# LayerType.GROUND
# LayerType.OBJECT
# LayerType.ENTITY
# LayerType.UI
# LayerType.OVERLAY

drawing.draw_rect(10, 10, layer=LayerType.BACKGROUND)
drawing.draw_rect(20, 20, layer=LayerType.ENTITY)
drawing.draw_rect(30, 30, layer=LayerType.UI)
# Rendered in order: BACKGROUND, ENTITY, UI
```

### Headless Rendering

For testing and server environments, use the headless backend:

```python
config = RenderConfig(headless=True)
renderer = Renderer2D(config=config, backend="headless")

# Use normally, but no display output
drawing = renderer.drawing()
drawing.draw_rect(10, 10, 50, 50)

# Check render records
renderer.clear()
renderer.render()
renderer.present()

log = renderer.backend.get_render_log()
frame_count = renderer.backend.get_frame_count()

print(f"Rendered {frame_count} frames")
print(f"Render log size: {len(log)} entries")
```

### Integration with Game Systems

The renderer is **completely independent** from all game systems. To integrate it with engine systems like InputSystem or EventSystem:

```python
from engine.core.InputSystem.input_parser import InputParser
from engine.renderer import Renderer2D

input_system = InputParser()  # From engine
renderer = Renderer2D()

# Hook systems together
def on_player_move(event):
    # Update player sprite based on event
    renderer.sprites().move_sprite("player", event.x, event.y)

input_system.on_input(on_player_move)
```

### API Reference

#### Drawing Parser

```python
drawing = renderer.drawing()

# Core drawing operations
drawing.draw_rect(x, y, width=32, height=32, color=(100,100,100,255), 
                  fill=True, border_width=0, layer=LayerType.OBJECT)
drawing.draw_circle(x, y, radius=16, color=(100,100,100,255), 
                    fill=True, border_width=0, layer=LayerType.OBJECT)
drawing.draw_line(start_x, start_y, end_x, end_y, color=(255,255,255,255), 
                  width=2, layer=LayerType.OBJECT)
drawing.draw_polygon(points, color=(100,100,100,255), 
                     fill=True, border_width=0, layer=LayerType.OBJECT)

# Manipulation
drawing.update_position(name, x, y)
drawing.update_color(name, color)
drawing.show(name)
drawing.hide(name)
drawing.remove(name)
drawing.clear_all()
```

#### Sprite Parser

```python
sprites = renderer.sprites()

# Loading and instantiation
sprites.load_sprite(name, file_path, width, height, frames_per_row=1, total_frames=1)
sprites.create_sprite(name, sprite_name, x=0, y=0)

# Animation
sprites.add_animation(sprite_name, animation_name, frames, looping=True)
sprites.play_animation(sprite_name, animation_name)

# Manipulation
sprites.move_sprite(sprite_name, x, y)
sprites.set_sprite_visible(sprite_name, visible)
sprites.remove_sprite(sprite_name)
sprites.get_sprite(sprite_name)
```

#### Text Parser

```python
text = renderer.text()

# Font management
text.load_font(name, file_path, size=12, bold=False, italic=False)

# Text rendering
text.render_text(text_content, x, y, font_name="default", 
                 color=(255,255,255,255), layer=LayerType.UI)

# Manipulation
text.update_text(name, new_content)
text.move_text(name, x, y)
text.remove_text(name)
text.get_text(name)
```

### Configuration Options

```python
from engine.renderer import RenderConfig

config = RenderConfig(
    window_title="Game Title",        # Window title
    window_width=1280,               # Window width in pixels
    window_height=720,               # Window height in pixels
    fps=60,                          # Target FPS
    fullscreen=False,                # Enable fullscreen
    vsync=True,                      # Enable vertical sync
    headless=False,                  # Headless mode (no display)
)

renderer = Renderer2D(config=config, backend="pygame")
```

### Testing

All systems are thoroughly tested with 32 automated tests:

```bash
python3 -m unittest Test_game.tests.test_renderer_2d -v
```

Test coverage includes:
- Configuration and data structures
- Drawing commands (rect, circle, line, polygon)
- Sprite loading and instancing
- Animation playback
- Text rendering
- Headless backend recording
- Full integration flows

### Performance Notes

- **Independent systems**: Each system updates independently
- **Hook-based rendering**: Only registered backends receive updates
- **Headless mode**: No GPU/display overhead for servers/tests
- **Layer sorting**: Commands sorted by layer once per frame
- **Animation updates**: Only play if animation is active

### Limitations & Future Work

- Sprite animation currently updates in update(), not automatic
- Text rendering basic (no styling, shadows, gradients)
- No particle system
- No 3D rendering (use 3dRenderer when available)
- Pygame backend only (no DirectX, OpenGL backends)

### Directory Structure

```
engine/renderer/
├── renderer_2d/
│   ├── renderer_2d.py           # Main coordinator
│   ├── Core/
│   │   └── renderer_config.py  # Configuration & base classes
│   ├── DrawingSystem/
│   │   ├── drawing.py           # Data layer
│   │   ├── drawing_system.py    # Engine layer
│   │   └── drawing_parser.py    # API layer
│   ├── SpriteSystem/
│   │   ├── sprite.py            # Data layer
│   │   ├── sprite_system.py     # Engine layer
│   │   └── sprite_parser.py     # API layer
│   ├── TextSystem/
│   │   ├── text.py              # Data layer
│   │   ├── text_system.py       # Engine layer
│   │   └── text_parser.py       # API layer
│   └── Backends/
│       ├── PygameRenderer/
│       │   └── pygame_backend.py
│       └── HeadlessRenderer/
│           └── headless_backend.py
└── 3dRenderer/                  # Future 3D renderer
```

### Getting Help

- Check the test suite in `Test_game/tests/test_renderer_2d.py` for examples
- Review the parser API documentation above
- Each module includes detailed docstrings

---

**Last Updated:** January 8, 2025  
**Status:** Production Ready (32/32 tests passing)  
**Version:** 1.0
