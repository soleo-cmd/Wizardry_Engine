from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.TileAndGridSystems.tile import Tile, TileType, TileFlags
from engine.core.TileAndGridSystems.grid_parser import GridParser

def test_grid_system():
    clock = EngineClock()
    clock.start()

    parser = GridParser()

    print("Test 1: Spawn Grid...")
    grid = parser.spawn_grid("test_grid", 8, 8)
    print("OKAY")

    print("Test 2: Fill Borders with Walls...")
    wall_tile = Tile(TileType.WALL, TileFlags.BLOCKS_SIGHT)
    parser.fill_borders("test_grid", wall_tile)
    print("OKAY")

    print("Test 3: Set Entrance and Exit...")
    entrance_tile = Tile(TileType.ENTRANCE, TileFlags.WALKABLE)
    exit_tile = Tile(TileType.EXIT, TileFlags.WALKABLE | TileFlags.IS_EXIT)
    parser.set_tile("test_grid", 1, 0, entrance_tile)
    parser.set_tile("test_grid", 6, 7, exit_tile)
    print("OKAY")

    print("Test 4: Access Tiles...")
    tile1 = parser.get_tile("test_grid", 1, 0)
    tile2 = parser.get_tile("test_grid", 6, 7)
    assert tile1.type == TileType.ENTRANCE
    assert tile2.type == TileType.EXIT
    print("OKAY")

    print("Test 5: Print Grid Layout...")
    parser.print_grid("test_grid")
    print("OKAY")

    clock.tick()  # update clock after all tests
    print(f"All tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_grid_system()
