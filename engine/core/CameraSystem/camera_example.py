# engine/core/CameraSystem/camera_example.py
"""
Example usage of the Camera System.
Demonstrates integration with game and renderer.
"""

from .camera import Camera, RenderMode
from .camera_parser import CameraParser


def example_basic_camera_setup():
    """Example 1: Create cameras for different scenes"""
    parser = CameraParser()
    
    # Create 8x8 town camera (can see whole map)
    parser.create_camera('town_cam',
                        position=(4, 4, 0),
                        viewport_size=(8, 8),
                        render_mode=RenderMode.MODE_2D)
    
    # Create 30x30 dungeon camera (limited view)
    parser.create_camera('dungeon_cam',
                        position=(15, 15, 0),
                        viewport_size=(30, 30),
                        render_mode=RenderMode.MODE_2D)
    
    # Switch between cameras
    parser.set_active_camera('town_cam')
    print(f"Active camera: {parser.get_active_camera()}")
    
    parser.set_active_camera('dungeon_cam')
    print(f"Active camera: {parser.get_active_camera()}")


def example_player_tracking():
    """Example 2: Make camera follow the player"""
    parser = CameraParser()
    parser.create_camera('main', viewport_size=(8, 8))
    
    # Tell camera to track player
    parser.follow_entity_with_active_camera('player')
    
    # Simulate player movement
    player_position = (4, 4, 0)
    parser.update_camera_for_entity_position('main', player_position)
    
    print(f"Camera now tracking player at {player_position}")


def example_renderer_integration():
    """Example 3: Connect renderer via hooks"""
    parser = CameraParser()
    parser.create_camera('main', viewport_size=(8, 8))
    
    # Define callbacks that renderer would use
    def on_camera_updated(camera):
        visible_area = camera.get_visible_area()
        print(f"Renderer needs to redraw: visible area = {visible_area}")
    
    def on_mode_changed(camera, old_mode):
        print(f"Rendering mode changed: {old_mode.name} -> {camera.render_mode.name}")
    
    # Connect hooks
    parser.set_camera_updated_hook(on_camera_updated)
    parser.set_camera_mode_changed_hook(on_mode_changed)
    
    # Trigger updates
    parser.set_active_camera_position(10, 10, 0)  # Fires on_camera_updated
    parser.set_active_render_mode(RenderMode.MODE_3D)  # Fires on_mode_changed


def example_2d_to_3d_switch():
    """Example 4: Switch from 2D to 3D (the key feature!)"""
    parser = CameraParser()
    
    # Start in 2D
    parser.create_camera('main',
                        viewport_size=(8, 8),
                        render_mode=RenderMode.MODE_2D)
    
    camera = parser.get_active_camera()
    print(f"Current mode: {camera.get_render_mode()}")
    assert camera.is_2d()
    
    # Later, switch to 3D when ready
    parser.set_active_render_mode(RenderMode.MODE_3D)
    
    camera = parser.get_active_camera()
    print(f"Current mode: {camera.get_render_mode()}")
    assert camera.is_3d()
    
    print("Camera system handles both 2D and 3D!")


def example_visibility_culling():
    """Example 5: Use camera to determine what to render"""
    parser = CameraParser()
    parser.create_camera('main',
                        position=(8, 8, 0),
                        viewport_size=(8, 8),
                        zoom=1.0)
    
    # Check which tiles are visible
    tiles_to_check = [
        (8, 8),    # Center (should be visible)
        (12, 12),  # Edge (should be visible)
        (20, 20),  # Far away (not visible)
    ]
    
    for x, y in tiles_to_check:
        if parser.is_point_visible(x, y):
            print(f"Tile ({x}, {y}): VISIBLE - draw it")
        else:
            print(f"Tile ({x}, {y}): NOT VISIBLE - skip it")


def example_zoom_and_viewport():
    """Example 6: Dynamic viewport and zoom for different scenes"""
    parser = CameraParser()
    parser.create_camera('main', viewport_size=(8, 8))
    
    # Town: See whole map at normal zoom
    parser.set_active_viewport_size(8, 8)
    parser.set_active_zoom(1.0)
    print("Town mode: viewport 8x8, zoom 1.0x")
    
    # Dungeon: See more tiles but with same window
    parser.set_active_viewport_size(30, 30)
    parser.set_active_zoom(1.0)
    print("Dungeon mode: viewport 30x30, zoom 1.0x (camera farther back)")
    
    # Or same viewport but zoomed out
    parser.set_active_viewport_size(8, 8)
    parser.set_active_zoom(2.0)
    print("Zoomed out: viewport 8x8, zoom 2.0x (tiles appear bigger)")


def example_serialization():
    """Example 7: Save and load camera state"""
    parser = CameraParser()
    parser.create_camera('main',
                        position=(5, 5, 0),
                        viewport_size=(8, 8),
                        zoom=1.5,
                        render_mode=RenderMode.MODE_2D)
    
    camera = parser.get_active_camera()
    
    # Save to dict (could save to file)
    saved_state = camera.to_dict()
    print(f"Saved camera state: {saved_state}")
    
    # Load from dict
    loaded_camera = Camera.from_dict(saved_state)
    print(f"Loaded camera: {loaded_camera}")
    
    assert loaded_camera.get_position() == (5, 5, 0)
    assert loaded_camera.get_viewport_size() == (8, 8)
    assert loaded_camera.get_zoom() == 1.5


if __name__ == '__main__':
    print("=== Camera System Examples ===\n")
    
    print("--- Example 1: Basic Setup ---")
    example_basic_camera_setup()
    
    print("\n--- Example 2: Player Tracking ---")
    example_player_tracking()
    
    print("\n--- Example 3: Renderer Integration ---")
    example_renderer_integration()
    
    print("\n--- Example 4: 2D to 3D Switch ---")
    example_2d_to_3d_switch()
    
    print("\n--- Example 5: Visibility Culling ---")
    example_visibility_culling()
    
    print("\n--- Example 6: Zoom and Viewport ---")
    example_zoom_and_viewport()
    
    print("\n--- Example 7: Serialization ---")
    example_serialization()
    
    print("\n=== All examples completed! ===")
