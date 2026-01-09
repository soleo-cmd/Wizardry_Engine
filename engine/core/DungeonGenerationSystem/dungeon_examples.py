# engine/core/DungeonGenerationSystem/dungeon_examples.py
"""
Examples showing dungeon generation usage.
Run with: python3 -m engine.core.DungeonGenerationSystem.dungeon_examples
"""

from dungeon_generation_parser import DungeonGenerationParser
from generation_config import DungeonConfig, GenerationAlgorithm, Room


def example_1_basic_generation():
    """Example 1: Generate a simple dungeon"""
    print("=== Example 1: Basic Generation ===\n")
    
    parser = DungeonGenerationParser()
    
    # Generate medium dungeon
    grid, rooms = parser.generate_medium_dungeon()
    
    print(f"Generated dungeon: {grid}")
    print(f"Number of rooms: {len(rooms)}\n")
    
    for room in rooms[:5]:  # Show first 5
        print(f"  {room}")
    
    if len(rooms) > 5:
        print(f"  ... and {len(rooms) - 5} more\n")


def example_2_different_algorithms():
    """Example 2: Generate with different algorithms"""
    print("=== Example 2: Different Algorithms ===\n")
    
    parser = DungeonGenerationParser()
    
    algorithms = [
        ("Random Rooms", parser.generate_medium_dungeon),
        ("Cave-like", parser.generate_cave_dungeon),
        ("Castle-like", parser.generate_castle_dungeon),
    ]
    
    for name, gen_func in algorithms:
        grid, rooms = gen_func()
        print(f"{name}: {len(rooms)} rooms generated")
    
    print()


def example_3_custom_config():
    """Example 3: Custom configuration"""
    print("=== Example 3: Custom Configuration ===\n")
    
    parser = DungeonGenerationParser()
    
    # Create custom config
    config = DungeonConfig(
        name="my_dungeon",
        width=25,
        height=25,
        algorithm=GenerationAlgorithm.RANDOM_ROOMS,
        target_room_count=10,
        min_room_size=4,
        max_room_size=8,
    )
    
    print(f"Config: {config}")
    grid, rooms = parser.generate_dungeon(config)
    print(f"Generated: {len(rooms)} rooms\n")


def example_4_quest_rooms():
    """Example 4: Generate with quest rooms"""
    print("=== Example 4: Quest Room Placement ===\n")
    
    parser = DungeonGenerationParser()
    
    # Create quest room template
    quest_room_template = parser.create_quest_room(
        width=5,
        height=5,
        room_type="quest",
        room_id="lost_person_chamber",
    )
    
    config = DungeonConfig(width=30, height=30)
    
    # Generate with quest room
    grid, rooms = parser.generate_dungeon(
        config,
        quest_rooms=[quest_room_template],
    )
    
    print(f"Generated {len(rooms)} rooms (including quest room)\n")
    
    # Find the quest room
    quest_room = parser.find_room_by_id(rooms, "lost_person_chamber")
    if quest_room:
        center = quest_room.get_center()
        print(f"Quest room placed at: {center}")
        print(f"Quest room bounds: ({quest_room.x}, {quest_room.y}) to "
              f"({quest_room.x + quest_room.width}, {quest_room.y + quest_room.height})\n")


def example_5_multiple_quest_rooms():
    """Example 5: Multiple quest rooms"""
    print("=== Example 5: Multiple Quest Rooms ===\n")
    
    parser = DungeonGenerationParser()
    
    # Create multiple quest rooms
    quest_rooms = [
        parser.create_quest_room(
            width=5, height=5,
            room_type="quest",
            room_id="treasure_vault",
        ),
        parser.create_quest_room(
            width=6, height=6,
            room_type="boss",
            room_id="boss_chamber",
        ),
    ]
    
    config = DungeonConfig(width=40, height=40, target_room_count=12)
    grid, rooms = parser.generate_dungeon(config, quest_rooms=quest_rooms)
    
    print(f"Generated {len(rooms)} rooms\n")
    
    # Find quest rooms
    for room_id in ["treasure_vault", "boss_chamber"]:
        room = parser.find_room_by_id(rooms, room_id)
        if room:
            print(f"{room_id}: {room}")
            print(f"  Center: {room.get_center()}\n")


def example_6_seeded_generation():
    """Example 6: Reproducible generation with seeds"""
    print("=== Example 6: Seeded Generation ===\n")
    
    parser = DungeonGenerationParser()
    
    # Generate with seed
    config1 = DungeonConfig(width=20, height=20, seed=42)
    grid1, rooms1 = parser.generate_dungeon(config1)
    print(f"First generation (seed=42): {len(rooms1)} rooms")
    print(f"First room: {rooms1[0]}")
    
    # Generate again with same seed
    config2 = DungeonConfig(width=20, height=20, seed=42)
    grid2, rooms2 = parser.generate_dungeon(config2)
    print(f"\nSecond generation (seed=42): {len(rooms2)} rooms")
    print(f"First room: {rooms2[0]}")
    
    print(f"\nSame layout: {len(rooms1) == len(rooms2)}\n")


def example_7_grid_utilities():
    """Example 7: Using grid utilities"""
    print("=== Example 7: Grid Utilities ===\n")
    
    parser = DungeonGenerationParser()
    grid, rooms = parser.generate_medium_dungeon()
    
    # Find all walkable tiles
    walkable = grid.find_tiles()
    print(f"Total walkable tiles: {len(walkable)}\n")
    
    # Check if region is clear
    test_x, test_y = 5, 5
    is_clear = grid.is_region_walkable(test_x, test_y, 3, 3)
    print(f"Region ({test_x},{test_y}) to ({test_x+3},{test_y+3}) is clear: {is_clear}\n")
    
    # Find random floor
    if walkable:
        pos = grid.random_floor_tile()
        print(f"Random floor tile: {pos}\n")
    
    # Pathfinding
    if len(walkable) >= 2:
        start = walkable[0]
        end = walkable[-1]
        path = grid.find_path(start, end)
        if path:
            print(f"Path from {start} to {end}: {len(path)} steps\n")
    
    # Distance
    if len(walkable) >= 2:
        dist = grid.get_distance(walkable[0], walkable[1])
        print(f"Distance between two random points: {dist}\n")


def example_8_hooks():
    """Example 8: Using hooks for integration"""
    print("=== Example 8: Hooks & Integration ===\n")
    
    parser = DungeonGenerationParser()
    
    # Define hooks
    def on_generation_started(config):
        print(f"[Generation Started] {config.name}")
    
    def on_generation_complete(grid, rooms):
        print(f"[Generation Complete] {len(rooms)} rooms created")
    
    def on_room_placed(room):
        print(f"[Room Placed] {room.room_id} at {room.get_center()}")
    
    # Connect hooks
    parser.set_generation_started_hook(on_generation_started)
    parser.set_generation_complete_hook(on_generation_complete)
    parser.set_room_placed_hook(on_room_placed)
    
    # Generate (hooks will fire)
    config = DungeonConfig(width=20, height=20, target_room_count=5)
    grid, rooms = parser.generate_dungeon(config)
    print()


def example_9_game_scenario():
    """Example 9: Game scenario - player enters dungeon with quest"""
    print("=== Example 9: Game Scenario ===\n")
    
    # Simulate game state
    class Player:
        def __init__(self):
            self.x = 0
            self.y = 0
            self.active_quests = ["find_lost_person", "slay_boss"]
    
    class GameWorld:
        def __init__(self):
            self.player = Player()
            self.parser = DungeonGenerationParser()
        
        def enter_dungeon(self):
            # Create quest rooms for active quests
            quest_rooms = []
            for quest_id in self.player.active_quests:
                qr = self.parser.create_quest_room(
                    width=5, height=5,
                    room_type="quest",
                    room_id=f"room_{quest_id}",
                )
                quest_rooms.append(qr)
            
            # Generate dungeon
            config = DungeonConfig(width=30, height=30, target_room_count=15)
            self.grid, self.rooms = self.parser.generate_dungeon(
                config,
                quest_rooms=quest_rooms,
            )
            
            # Place player in first room
            first_room = self.rooms[0]
            self.player.x, self.player.y = first_room.get_center()
            
            print(f"Entered dungeon!")
            print(f"Player spawned at: ({self.player.x}, {self.player.y})\n")
        
        def show_quest_locations(self):
            print("Quest rooms:")
            for quest_id in self.player.active_quests:
                room = self.parser.find_room_by_id(
                    self.rooms,
                    f"room_{quest_id}",
                )
                if room:
                    print(f"  {quest_id}: {room.get_center()}")
            print()
    
    # Run scenario
    world = GameWorld()
    world.enter_dungeon()
    world.show_quest_locations()


if __name__ == '__main__':
    print("╔════════════════════════════════════════════╗")
    print("║  Dungeon Generation System - Examples      ║")
    print("╚════════════════════════════════════════════╝\n")
    
    examples = [
        example_1_basic_generation,
        example_2_different_algorithms,
        example_3_custom_config,
        example_4_quest_rooms,
        example_5_multiple_quest_rooms,
        example_6_seeded_generation,
        example_7_grid_utilities,
        example_8_hooks,
        example_9_game_scenario,
    ]
    
    for example_func in examples:
        example_func()
    
    print("╔════════════════════════════════════════════╗")
    print("║  All examples completed!                   ║")
    print("╚════════════════════════════════════════════╝")
