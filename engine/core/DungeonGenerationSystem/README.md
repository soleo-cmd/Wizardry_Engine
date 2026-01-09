# Dungeon Generation - Quick Reference

## Import
```python
from engine.core.DungeonGenerationSystem import (
    DungeonGenerationParser,
    DungeonConfig,
    Room,
    GenerationAlgorithm,
)
```

## Initialize
```python
parser = DungeonGenerationParser()
```

## Quick Generate

```python
# Small dungeon (20x20, 8 rooms)
grid, rooms = parser.generate_small_dungeon()

# Medium dungeon (30x30, 15 rooms)
grid, rooms = parser.generate_medium_dungeon()

# Large dungeon (50x50, 30 rooms)
grid, rooms = parser.generate_large_dungeon()

# Cave-like dungeon
grid, rooms = parser.generate_cave_dungeon()

# Castle-like dungeon (clear rooms)
grid, rooms = parser.generate_castle_dungeon()
```

## Custom Config
```python
config = DungeonConfig(
    name="undead_crypt",
    width=30,
    height=30,
    algorithm=GenerationAlgorithm.RANDOM_ROOMS,
    target_room_count=12,
    seed=42,  # Reproducible
)
grid, rooms = parser.generate_dungeon(config)
```

## Quest Rooms
```python
# Create quest room template
quest_room = parser.create_quest_room(
    width=6,
    height=6,
    room_type="quest",
    room_id="lost_person_room",
)

# Generate with quest room
grid, rooms = parser.generate_dungeon(
    config,
    quest_rooms=[quest_room],
)

# Find placed quest room
room = parser.find_room_by_id(rooms, "lost_person_room")
center_x, center_y = room.get_center()
```

## Room Utilities
```python
# Get all rooms of a type
quest_rooms = parser.get_rooms_by_type(rooms, "quest")
boss_rooms = parser.get_rooms_by_type(rooms, "boss")

# Get accessible rooms only
accessible = parser.get_accessible_rooms(grid, rooms)

# Find specific room
room = parser.find_room_by_id(rooms, "quest_room_01")

# Room info
print(room.x, room.y)                # Position
print(room.width, room.height)       # Dimensions
center = room.get_center()           # (x, y) center
is_inside = room.contains(player_x, player_y)
```

## Grid Utilities

```python
# Copy grid
grid_copy = grid.clone()

# Extract portion
sub = grid.subgrid(x, y, width, height)

# Paste grid
success = grid.stamp(other_grid, x, y)

# Find tiles
walkable = grid.find_tiles(flag=TileFlags.WALKABLE)
floors = grid.find_tiles(TileType.FLOOR)

# Check region
is_clear = grid.is_region_walkable(x, y, width, height)

# Pathfinding
path = grid.find_path((x1, y1), (x2, y2))
if path:
    for next_x, next_y in path:
        print(f"Move to {next_x}, {next_y}")

# Flood fill
connected = grid.flood_fill((x, y))  # All connected walkable
connected_type = grid.flood_fill((x, y), TileFlags.WALKABLE)

# Random tile
random_pos = grid.random_floor_tile()

# Distance
dist = grid.get_distance((x1, y1), (x2, y2))
```

## Hooks (Integration)

```python
def on_started(config):
    print(f"Generating {config.name}...")

def on_complete(grid, rooms):
    print(f"Generated {len(rooms)} rooms")

def on_room_placed(room):
    print(f"Room: {room.room_id} at {room.get_center()}")

def on_quest_placed(room):
    print(f"Quest room {room.room_id} placed!")

parser.set_generation_started_hook(on_started)
parser.set_generation_complete_hook(on_complete)
parser.set_room_placed_hook(on_room_placed)
parser.set_quest_room_placed_hook(on_quest_placed)

# Now generate - hooks will fire
grid, rooms = parser.generate_medium_dungeon()
```

## Game Integration Example

```python
class Game:
    def enter_dungeon(self):
        gen = DungeonGenerationParser()
        
        # Determine config based on game state
        if self.difficulty == "hard":
            config = DungeonConfig(
                width=40,
                height=40,
                target_room_count=20,
            )
        else:
            config = DungeonConfig(
                width=30,
                height=30,
                target_room_count=12,
            )
        
        # Create quest rooms for active quests
        quest_rooms = []
        for quest in self.player.active_quests:
            qr = gen.create_quest_room(
                width=5,
                height=5,
                room_type="quest",
                room_id=f"quest_{quest.id}",
            )
            qr.data['quest'] = quest
            quest_rooms.append(qr)
        
        # Generate
        grid, rooms = gen.generate_dungeon(config, quest_rooms)
        
        # Store
        self.current_dungeon_grid = grid
        self.current_dungeon_rooms = rooms
        
        # Place player
        start_room = rooms[0]
        self.player.x, self.player.y = start_room.get_center()

    def check_quest_completion(self):
        gen = DungeonGenerationParser()
        
        for quest in self.player.active_quests:
            room = gen.find_room_by_id(
                self.current_dungeon_rooms,
                f"quest_{quest.id}",
            )
            
            if self.is_player_in_room(room):
                quest.complete()
```

## Algorithms

**Random Rooms**: Default, good for variety
```python
config = DungeonConfig(algorithm=GenerationAlgorithm.RANDOM_ROOMS)
```

**Cellular Automata**: Cave-like, organic
```python
config = DungeonConfig(
    algorithm=GenerationAlgorithm.CELLULAR_AUTOMATA,
    wall_fill_probability=0.45,
    iterations=5,
)
```

**Binary Space Partition**: Structured, castle-like
```python
config = DungeonConfig(algorithm=GenerationAlgorithm.BINARY_SPACE_PARTITION)
```

## Serialization

```python
# Save config
config_data = config.to_dict()
# Save to file...

# Load config
config = DungeonConfig.from_dict(config_data)

# Save room
room_data = room.to_dict()

# Load room
room = Room.from_dict(room_data)
```

## Key Concepts

**Deterministic**: Use seed for same layout
```python
config = DungeonConfig(seed=42)
# Same dungeon every time with seed=42
```

**Quest Room Placement**: Guaranteed accessible
```python
# System checks that quest room area is walkable
# before placing it
```

**Connected Rooms**: Corridors automatically created
```python
# All rooms connected via corridors
# Use pathfinding to navigate
```

**Multiple Algorithms**: Choose based on preference
```python
# Try different algorithms, pick what looks best
```
