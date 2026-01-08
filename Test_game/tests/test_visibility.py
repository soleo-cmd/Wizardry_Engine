import sys
import os

# Add project root to sys.path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.VisibilitySystem.visibility_parser import VisibilityParser
from engine.core.VisibilitySystem.visibility import VisibilityType, VisibilityFlags

def test_visibility_system():
    clock = EngineClock()
    clock.start()

    parser = VisibilityParser(grid_width=50, grid_height=50)

    # Test counters
    visibility_changes = []
    observers_added = []
    observers_removed = []

    # -----------------------------
    # Hooks for debugging
    # -----------------------------
    parser.set_visibility_changed_hook(lambda v: visibility_changes.append(v))
    parser.set_observer_added_hook(lambda pos, eid: observers_added.append((pos, eid)))
    parser.set_observer_removed_hook(lambda pos, eid: observers_removed.append((pos, eid)))

    # -----------------------------
    # Test 1: Create Tiles
    # -----------------------------
    print("Test 1: Create Tiles...")
    tile1 = parser.create_tile((0, 0), VisibilityType.VISIBLE)
    tile2 = parser.create_tile((1, 1), VisibilityType.HIDDEN)
    tile3 = parser.create_tile((2, 2), VisibilityType.FOG_OF_WAR)
    assert tile1.type == VisibilityType.VISIBLE
    assert tile2.type == VisibilityType.HIDDEN
    assert tile3.type == VisibilityType.FOG_OF_WAR
    assert len(visibility_changes) == 3
    print("OKAY")

    # -----------------------------
    # Test 2: Get Tile
    # -----------------------------
    print("Test 2: Get Tile...")
    retrieved = parser.get_tile((0, 0))
    assert retrieved is not None
    assert retrieved.position == (0, 0)
    assert retrieved.type == VisibilityType.VISIBLE
    print("OKAY")

    # -----------------------------
    # Test 3: Set Tile Visibility
    # -----------------------------
    print("Test 3: Set Tile Visibility...")
    parser.set_tile_visibility((0, 0), VisibilityType.HIDDEN)
    assert parser.get_tile((0, 0)).type == VisibilityType.HIDDEN
    parser.set_tile_visibility((0, 0), VisibilityType.VISIBLE)
    assert parser.get_tile((0, 0)).type == VisibilityType.VISIBLE
    print("OKAY")

    # -----------------------------
    # Test 4: Add Observers
    # -----------------------------
    print("Test 4: Add Observers...")
    parser.add_observer((0, 0), entity_id=1)
    parser.add_observer((0, 0), entity_id=2)
    parser.add_observer((1, 1), entity_id=1)
    
    assert parser.can_see((0, 0), 1) == True
    assert parser.can_see((0, 0), 2) == True
    assert parser.can_see((1, 1), 1) == True
    assert parser.can_see((1, 1), 2) == False
    assert len(observers_added) == 3
    print("OKAY")

    # -----------------------------
    # Test 5: Get Observers
    # -----------------------------
    print("Test 5: Get Observers...")
    observers = parser.get_observers((0, 0))
    assert 1 in observers
    assert 2 in observers
    assert len(observers) == 2
    print("OKAY")

    # -----------------------------
    # Test 6: Get Visible Tiles for Entity
    # -----------------------------
    print("Test 6: Get Visible Tiles for Entity...")
    visible_tiles_1 = parser.get_visible_tiles(1)
    assert (0, 0) in visible_tiles_1
    assert (1, 1) in visible_tiles_1
    assert (2, 2) not in visible_tiles_1
    
    visible_tiles_2 = parser.get_visible_tiles(2)
    assert (0, 0) in visible_tiles_2
    assert (1, 1) not in visible_tiles_2
    print("OKAY")

    # -----------------------------
    # Test 7: Remove Observer
    # -----------------------------
    print("Test 7: Remove Observer...")
    parser.remove_observer((0, 0), 1)
    assert parser.can_see((0, 0), 1) == False
    assert parser.can_see((0, 0), 2) == True
    assert len(observers_removed) == 1
    print("OKAY")

    # -----------------------------
    # Test 8: Clear Observers from Tile
    # -----------------------------
    print("Test 8: Clear Observers from Tile...")
    parser.clear_observers((0, 0))
    observers = parser.get_observers((0, 0))
    assert len(observers) == 0
    print("OKAY")

    # -----------------------------
    # Test 9: Remove Entity from All Tiles
    # -----------------------------
    print("Test 9: Remove Entity from All Tiles...")
    # Reset and add entity 3 to multiple tiles
    parser.clear_observers((0, 0))
    parser.clear_observers((1, 1))
    parser.clear_observers((2, 2))
    
    parser.add_observer((0, 0), 3)
    parser.add_observer((1, 1), 3)
    parser.add_observer((2, 2), 3)
    
    assert parser.get_visible_tiles(3) == [(0, 0), (1, 1), (2, 2)]
    
    parser.remove_entity_from_all(3)
    assert len(parser.get_visible_tiles(3)) == 0
    print("OKAY")

    # -----------------------------
    # Test 10: Tile Flags
    # -----------------------------
    print("Test 10: Tile Flags...")
    blocking_tile = parser.create_tile((5, 5), VisibilityType.VISIBLE, VisibilityFlags.BLOCKING)
    light_tile = parser.create_tile((6, 6), VisibilityType.VISIBLE, VisibilityFlags.LIGHT_SOURCE | VisibilityFlags.TRANSPARENT)
    
    assert blocking_tile.is_blocked() == True
    assert light_tile.is_light_source() == True
    assert light_tile.is_transparent() == True
    assert blocking_tile.is_transparent() == False
    print("OKAY")

    # -----------------------------
    # Test 11: Tile Serialization
    # -----------------------------
    print("Test 11: Tile Serialization...")
    tile = parser.get_tile((5, 5))
    tile_dict = tile.to_dict()
    assert tile_dict["position"] == (5, 5)
    assert tile_dict["type"] == "VISIBLE"
    assert tile_dict["flags"] == VisibilityFlags.BLOCKING.value
    
    # Test deserialization
    from engine.core.VisibilitySystem.visibility import Visibility
    restored = Visibility.from_dict(tile_dict)
    assert restored.position == tile.position
    assert restored.type == tile.type
    assert restored.flags == tile.flags
    print("OKAY")

    # -----------------------------
    # Test 12: Complex Visibility Scenario
    # -----------------------------
    print("Test 12: Complex Visibility Scenario...")
    # Create a fresh parser for this scenario to avoid conflicts
    parser_scenario = VisibilityParser(grid_width=50, grid_height=50)
    
    # Simulate a game scenario
    # Create a small area
    for x in range(10):
        for y in range(10):
            if x == 5 and y == 5:
                # Center is a light source
                parser_scenario.create_tile((x, y), VisibilityType.VISIBLE, VisibilityFlags.LIGHT_SOURCE)
            elif (x - 5) ** 2 + (y - 5) ** 2 <= 9:
                # Adjacent to light
                parser_scenario.create_tile((x, y), VisibilityType.VISIBLE)
            else:
                # Far from light
                parser_scenario.create_tile((x, y), VisibilityType.FOG_OF_WAR)
    
    # Entity in center sees light area
    player_id = 100
    for x in range(10):
        for y in range(10):
            if (x - 5) ** 2 + (y - 5) ** 2 <= 9:
                parser_scenario.add_observer((x, y), player_id)
    
    visible = parser_scenario.get_visible_tiles(player_id)
    assert (5, 5) in visible
    assert (5, 4) in visible  # Adjacent
    assert (0, 0) not in visible  # Far away
    print("OKAY")

    # -----------------------------
    # Timing Report
    # -----------------------------
    clock.tick()
    print(f"All visibility system tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_visibility_system()
