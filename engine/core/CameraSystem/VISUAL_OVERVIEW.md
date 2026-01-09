# Camera System - Visual Overview

## The Problem Statement (Before)

```
TOWN (8x8)                      DUNGEON (30x30)
┌─────────────────────┐         ┌─────────────────────────────────────────────┐
│                     │         │ ┌─────────────────────┐                   │ │
│  Can see whole map  │         │ │ What player sees    │                   │ │
│  (good!)            │         │ │ (can't see edges)   │                   │ │
│                     │         │ └─────────────────────┘                   │ │
└─────────────────────┘         └─────────────────────────────────────────────┘

Problem 1: Different viewport sizes needed per scene
Problem 2: Need to switch to 3D eventually
Problem 3: Renderer and Engine are tightly coupled?
Problem 4: Where does camera logic live?
```

## The Solution (After)

```
┌──────────────────────────────────────────────────────────┐
│  GAME CODE (test_game.py)                               │
│                                                          │
│  camera_parser.create_camera('town', viewport=(8, 8))  │
│  camera_parser.set_render_mode(RenderMode.MODE_2D)     │
│  ...                                                     │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│  CAMERA PARSER (Game-facing API)                        │
│  - create_camera(), set_active_camera()                 │
│  - follow_entity(), set_viewport_size()                 │
│  - set_render_mode() ← THE KEY FOR 2D↔3D               │
│  - register hooks()                                      │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│  CAMERA SYSTEM (Core Logic - HEADLESS)                 │
│  ❌ No pygame imports                                    │
│  ❌ No renderer imports                                  │
│  ✅ Pure position math                                  │
│  ✅ Viewport calculations                               │
│  ✅ Visibility culling (is_point_visible)              │
│  ✅ Fires hooks when state changes                      │
└──────────────────────────────────────────────────────────┘
                           ↓
┌──────────────────────────────────────────────────────────┐
│  CAMERA DATA (Pure Data)                                │
│  - position: (x, y, z)                                  │
│  - viewport_size: (width, height)                       │
│  - zoom: float                                          │
│  - render_mode: RenderMode enum ← FLEXIBLE!            │
│  - target_entity: str or None                           │
│  ✅ Serializable (to_dict/from_dict)                    │
└──────────────────────────────────────────────────────────┘
            ↓ HOOKS ↓       ↓ HOOKS ↓
    ┌───────────┴───────────────┴────────┐
    ↓                                     ↓
RENDERER 2D                         SERIALIZATION
- Receives hook                     - Save game state
- Sees position: (x, y, z)         - Load camera position
- Sees mode: MODE_2D               - Reload viewport settings
- Sees viewport: (8, 8)
- Applies 2D transforms
  (tile grid, sprite scaling)

[Later: Renderer 3D]
- Receives same hook
- Sees mode: MODE_3D
- Applies 3D transforms
  (perspective, rotation matrices)
- CAMERA CODE UNCHANGED!
```

## Data Flow: Town → Dungeon → 3D Future

```
STEP 1: Setup Town Camera
┌─────────────────────────────────┐
│ Game: Create town camera        │
│ camera_parser.create_camera(    │
│   'town',                       │
│   viewport=(8, 8),              │ ← Can see whole 8x8 map
│   render_mode=MODE_2D)          │
└─────────────────────────────────┘
         ↓
┌─────────────────────────────────┐
│ CameraSystem creates Camera     │
│ Camera(                         │
│   position=(0,0,0),             │
│   viewport_size=(8,8),          │
│   render_mode=MODE_2D)          │
└─────────────────────────────────┘
         ↓ [Hook]
┌─────────────────────────────────┐
│ Renderer 2D                     │
│ See: viewport=(8,8)             │
│ Render full town on screen      │
└─────────────────────────────────┘


STEP 2: Switch to Dungeon
┌──────────────────────────────────┐
│ Game: Switch camera + viewport   │
│ camera_parser.                   │
│   set_active_camera('dungeon')   │
│ camera_parser.                   │
│   set_viewport_size(30, 30)      │ ← Much larger area
└──────────────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ CameraSystem updates Camera      │
│ Camera.viewport_size = (30, 30)  │
└──────────────────────────────────┘
         ↓ [Hook]
┌──────────────────────────────────┐
│ Renderer 2D                      │
│ See: viewport=(30,30)            │
│ Render portion of 30x30 dungeon  │
│ (visible area only!)             │
└──────────────────────────────────┘


STEP 3: The Future - 3D Wizardry Engine
┌──────────────────────────────────┐
│ Game: Switch to 3D mode!         │
│ camera_parser.                   │
│   set_render_mode(MODE_3D)       │
└──────────────────────────────────┘
         ↓
┌──────────────────────────────────┐
│ CameraSystem updates Camera      │
│ Camera.render_mode = MODE_3D     │
│ [on_camera_mode_changed hook]    │
└──────────────────────────────────┘
         ↓ [Hook]
┌──────────────────────────────────┐
│ Renderer 3D (future)             │
│ See: mode=MODE_3D                │
│ Load 3D pipeline!                │
│ Apply perspective matrix         │
│ Apply camera rotation            │
│ Apply frustum culling            │
│ (Camera.get_position still works)│
└──────────────────────────────────┘

❌ Game code: UNCHANGED!
❌ CameraSystem: UNCHANGED!
✅ Only Renderer changes!
```

## Visibility Culling Example

```
TOWN CAMERA: pos=(4,4), viewport=(8,8)
Visible area:
  min_x = 4 - 8/2 = 0
  max_x = 4 + 8/2 = 8
  min_y = 4 - 8/2 = 0
  max_y = 4 + 8/2 = 8

┌─────────────────────────────────────┐
│ (0,0) ═══════════════════ (8,0)    │
│   ║  ┌─────────────────┐  ║        │
│   ║  │   VISIBLE       │  ║        │
│   ║  │  (see whole)    │  ║        │
│   ║  │                 │  ║        │
│ (0,8) ║  ┌─────────────┘  (8,8)   │
│       │  │                         │
│       └──┘ Outside visible area    │
│                                     │
└─────────────────────────────────────┘
          ↑ Renderer
          │ Only draws what's visible


DUNGEON CAMERA: pos=(15,15), viewport=(30,30)
Visible area:
  min_x = 15 - 30/2 = 0
  max_x = 15 + 30/2 = 30
  min_y = 15 - 30/2 = 0
  max_y = 15 + 30/2 = 30

┌──────────────────────────────────────────────────────────┐
│ (0,0)                                              (30,0)│
│   ┌──────────────────────────────────────┐              │
│   │  VISIBLE (30x30)                     │              │
│   │  Can only see this portion of        │              │
│   │  the 30x30 dungeon on screen         │              │
│   │  (viewport defines screen size)      │              │
│   │                                      │              │
│   │  Player moves → camera follows       │              │
│   │  Camera pans to keep player visible  │              │
│   └──────────────────────────────────────┘              │
│                                              (30,30)     │
└──────────────────────────────────────────────────────────┘
          ↑ Renderer
          │ Only draws what's visible
```

## Directory Structure

```
engine/core/CameraSystem/
│
├── camera.py
│   └── Camera class (data)
│       ├── position (x, y, z)
│       ├── viewport_size (w, h)
│       ├── zoom (float)
│       ├── render_mode (MODE_2D or MODE_3D)
│       └── Methods: set_position, get_visible_area, is_point_visible, etc.
│
├── camera_system.py
│   └── CameraSystem class (logic)
│       ├── Manages multiple cameras
│       ├── Lifecycle: create, get, set_active, remove
│       └── Hooks: on_camera_updated, on_camera_mode_changed, etc.
│
├── camera_parser.py
│   └── CameraParser class (API)
│       ├── Game calls these methods
│       ├── create_camera(), set_active_camera()
│       ├── follow_entity(), set_viewport_size()
│       ├── set_render_mode() ← KEY!
│       └── Hook registration methods
│
├── __init__.py
│   └── Module exports
│
├── camera_example.py
│   └── 7 complete usage examples
│
├── README.md
│   └── Quick reference
│
├── CAMERA_DESIGN.md
│   └── Full design documentation
│
└── IMPLEMENTATION_SUMMARY.md
    └── This summary + integration checklist
```

## Integration Points

```
┌──────────────────────────────────────┐
│  Test Game (test_game.py)            │
├──────────────────────────────────────┤
│ Must add:                            │
│ • camera_parser = CameraParser()     │
│ • Create cameras for each scene      │
│ • Connect movement hook               │
│ • Connect renderer hook               │
└──────────────────────────────────────┘
             ↓↑
    ┌─────────────────┐
    │  CameraParser   │ ← You are here
    └─────────────────┘
             ↓↑
    ┌─────────────────┐
    │ CameraSystem    │
    └─────────────────┘
             ↓↑
    ┌─────────────────┐
    │  Camera Data    │
    └─────────────────┘
             ↓
    ┌─────────────────┐
    │ Renderer 2D     │ ← Update to listen to hooks
    │ (interprets     │
    │  MODE_2D)       │
    └─────────────────┘
             ↓
    ┌─────────────────┐
    │ Renderer 3D     │ ← Future: will listen to hooks
    │ (interprets     │   for MODE_3D
    │  MODE_3D)       │
    └─────────────────┘
```

## Key Features at a Glance

| Feature | Implementation |
|---------|-----------------|
| Multiple cameras | ✅ Named cameras, active camera |
| 2D rendering | ✅ MODE_2D support |
| 3D ready | ✅ MODE_3D support (future) |
| Headless | ✅ Zero pygame/renderer imports |
| Entity tracking | ✅ Hook from MovementSystem |
| Viewport control | ✅ Set different sizes per scene |
| Zoom support | ✅ Magnification level |
| Visibility culling | ✅ is_point_visible(), get_visible_area() |
| Serialization | ✅ to_dict() / from_dict() |
| Hooks/callbacks | ✅ on_camera_updated, on_mode_changed, etc. |
| Extendable | ✅ Easy to add more cameras/features |

## Summary

✅ **Engine-agnostic**: No rendering code  
✅ **Renderer-flexible**: Works with any renderer via hooks  
✅ **Game-simple**: Clean API for game logic  
✅ **Future-proof**: Ready for 3D when needed  
✅ **Consistent**: Matches your architecture patterns  
✅ **Complete**: Fully documented with examples  
