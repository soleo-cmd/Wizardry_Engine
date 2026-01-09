# Camera System - Quick Reference

## Import
```python
from engine.core.CameraSystem import CameraParser, RenderMode, Camera
```

## Initialize
```python
camera_parser = CameraParser()
```

## Create Cameras
```python
# Town camera (can see whole 8x8 map)
camera_parser.create_camera('town_cam', 
                           position=(4, 4, 0),
                           viewport_size=(8, 8),
                           render_mode=RenderMode.MODE_2D)

# Dungeon camera (can only see 30x30 slice of map)
camera_parser.create_camera('dungeon_cam',
                           position=(15, 15, 0), 
                           viewport_size=(30, 30),
                           render_mode=RenderMode.MODE_2D)
```

## Switch Cameras
```python
camera_parser.set_active_camera('town_cam')
camera_parser.set_active_camera('dungeon_cam')
```

## Move Cameras
```python
# Direct position
camera_parser.set_active_camera_position(10, 10, 0)

# Pan (relative)
camera_parser.pan_active_camera(1, 0, 0)

# Follow entity
camera_parser.follow_entity_with_active_camera('player')
camera_parser.update_camera_for_entity_position('main_cam', player.position)
```

## Viewport & Zoom
```python
# Change viewport (8x8 town, 30x30 dungeon)
camera_parser.set_active_viewport_size(8, 8)
camera_parser.set_active_viewport_size(30, 30)

# Zoom (1.0 = normal, 2.0 = 2x magnified)
camera_parser.set_active_zoom(1.0)
camera_parser.set_active_zoom(2.0)
```

## 2D ↔ 3D Switching (The Key!)
```python
# Currently 2D
camera_parser.set_active_render_mode(RenderMode.MODE_2D)

# Switch to 3D when ready
camera_parser.set_active_render_mode(RenderMode.MODE_3D)

# Renderer will adapt automatically via hook!
```

## Visibility Queries
```python
# Get visible area bounds
visible = camera_parser.get_visible_area()
# {'min_x': ..., 'max_x': ..., 'min_y': ..., 'max_y': ..., 'min_z': ..., 'max_z': ...}

# Check if point is visible
if camera_parser.is_point_visible(x, y, z):
    print("Draw this tile")
```

## Renderer Integration (Listen to Hooks)
```python
def on_camera_updated(camera):
    print(f"Camera moved: {camera.get_position()}")
    # Redraw with new camera data
    
def on_mode_changed(camera, old_mode):
    if camera.is_3d():
        print("Switch to 3D rendering")
    else:
        print("Switch to 2D rendering")

camera_parser.set_camera_updated_hook(on_camera_updated)
camera_parser.set_camera_mode_changed_hook(on_mode_changed)
```

## Get Current State
```python
camera = camera_parser.get_active_camera()
print(camera.get_position())           # (x, y, z)
print(camera.get_viewport_size())      # (width, height)
print(camera.get_zoom())               # float
print(camera.get_render_mode())        # RenderMode enum
print(camera.get_target_entity())      # "player" or None
```

## Serialization
```python
camera = camera_parser.get_active_camera()
data = camera.to_dict()
# Save to file...

# Load from file...
camera = Camera.from_dict(data)
```

## Key Concept: Headless Design

```
GAME                      ENGINE                  RENDERER
  |                         |                        |
  |-- pan_camera --------> CAMERA PARSER --hook--> Update display
  |-- set_mode ---------> CAMERA SYSTEM          (2D transform?)
  |                       (no rendering code)    (3D transform?)
  |                       (pure position math)
  |                       (doesn't import pygame)
```

The camera is **data + logic**, renderer **interprets** it.
