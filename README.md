<<<<<<< HEAD
# Wizardry_Engine
its pretty cool :)
=======
# Wizardry Engine API Documentation

## Overview

Wizardry is a modular, hook-based game engine written in Python. It provides independent systems for managing game state, entities, events, and more. Each system is completely decoupled from others and communicates through hooks/callbacks.

## Architecture Pattern

The engine follows a consistent three-layer pattern:

```
Data Class (entity.py)
    ↓
System Class (entity_system.py) 
    ↓
Parser Class (entity_parser.py) - Game-facing API
```

### Layer Breakdown

1. **Data Class** (`*_data.py` or `class.py`)
   - Contains pure data structures
   - Enums for types and flags
   - Serialization methods (to_dict/from_dict)
   - Helper methods specific to the data

2. **System Class** (`*_system.py`)
   - Engine-level business logic
   - Manages internal state and collections
   - Defines hooks for integration
   - No direct game code dependencies

3. **Parser Class** (`*_parser.py`)
   - Game-facing API
   - Wrapper around the system
   - Exposes clean methods for game code
   - Manages hook registration
   - Only class directly used by game code

## Available Systems

### 1. Entity System

**Purpose**: Manage game entities (players, enemies, NPCs, items)

**Files**:
- `engine/core/EntitySystem/entity.py`
- `engine/core/EntitySystem/entity_system.py`
- `engine/core/EntitySystem/entity_parser.py`

**Basic Usage**:
```python
from engine.core.EntitySystem.entity_parser import EntityParser
from engine.core.EntitySystem.entity import EntityType, EntityFlags

parser = EntityParser()

# Set up hooks
parser.set_created_hook(lambda e: print(f"Entity created: {e}"))
parser.set_updated_hook(lambda e: print(f"Entity updated: {e}"))
parser.set_removed_hook(lambda e: print(f"Entity removed: {e}"))

# Create entities
player = parser.spawn_entity(
    "Hero", 
    EntityType.PLAYER, 
    EntityFlags.ALIVE | EntityFlags.MOVABLE, 
    hp=100
)

# Manipulate entities
parser.move_entity("Hero", 5, 10)
parser.damage_entity("Hero", 25)
parser.heal_entity("Hero", 10)

# Query entities
hero = parser.get_entity("Hero")
print(f"Hero HP: {hero.hp}, Position: {hero.position}")

# Remove entities
parser.remove_entity("Hero")
```

**Data Structure** - Entity:
```python
class Entity:
    name: str                    # Unique identifier
    type: EntityType             # PLAYER, ENEMY, NPC, ITEM
    flags: EntityFlags           # ALIVE, MOVABLE, INTERACTIVE
    hp: int                       # Health points
    position: tuple              # (x, y) coordinate
    data: dict                    # Custom data storage
```

---

### 2. State System

**Purpose**: Manage global game states (menu, gameplay, battle, pause, etc.)

**Files**:
- `engine/core/StateSystem/state.py`
- `engine/core/StateSystem/state_system.py`
- `engine/core/StateSystem/state_parser.py`

**Basic Usage**:
```python
from engine.core.StateSystem.state_parser import StateParser
from engine.core.StateSystem.state import StateType, StateFlags

parser = StateParser()

# Set up hooks
parser.set_created_hook(lambda s: print(f"State created: {s}"))
parser.set_changed_hook(lambda s: print(f"State changed: {s}"))

# Create states
parser.create_state("MainMenu", StateType.MENU, StateFlags.VISIBLE | StateFlags.BLOCKS_INPUT)
parser.create_state("Gameplay", StateType.GAMEPLAY, StateFlags.VISIBLE)
parser.create_state("Pause", StateType.PAUSE, StateFlags.BLOCKS_INPUT)

# Switch states
parser.set_current_state("Gameplay")
current = parser.get_current_state()

# Remove state
parser.remove_state("MainMenu")
```

**Completely independent from SceneSystem** - Use for global game state, not scene-specific state.

---

### 3. Turn System

**Purpose**: Manage turn-based gameplay and action points

**Files**:
- `engine/core/TurnSystem/turn.py`
- `engine/core/TurnSystem/turn_system.py`
- `engine/core/TurnSystem/turn_parser.py`

**Basic Usage**:
```python
from engine.core.TurnSystem.turn_parser import TurnParser

parser = TurnParser()

# Set up hooks
parser.set_turn_started_hook(lambda t: print(f"Turn started: Entity {t.entity_id}"))
parser.set_turn_ended_hook(lambda t: print(f"Turn ended"))
parser.set_action_spent_hook(lambda t, ap: print(f"AP spent: {ap}"))

# Register entities
parser.register_entity(entity_id=1, action_points=5)
parser.register_entity(entity_id=2, action_points=3)

# Manage turn flow
current_turn = parser.next_turn()  # Start next turn
entity_id = parser.current_entity()

# Spend action points
if parser.spend_ap(amount=1):
    print("Action point spent")
else:
    print("Not enough action points")

# End turn
parser.end_turn()
```

---

### 4. Action System

**Purpose**: Queue and execute player actions

**Files**:
- `engine/core/ActionCommandSystem/action.py`
- `engine/core/ActionCommandSystem/action_system.py`
- `engine/core/ActionCommandSystem/action_parser.py`

**Basic Usage**:
```python
from engine.core.ActionCommandSystem.action_parser import ActionParser
from engine.core.ActionCommandSystem.action import ActionType

parser = ActionParser()

# Set hook
parser.on_execute_action = lambda a: print(f"Executing: {a}")

# Create actions
parser.create_action(entity_id=1, action_type=ActionType.MOVE, target=(5, 10))
parser.create_action(entity_id=1, action_type=ActionType.ATTACK, target=2)

# Execute actions
if parser.has_actions_for_entity(1):
    action = parser.execute_next_action(entity_id=1)
```

---

### 5. Event System

**Purpose**: Game-wide event dispatch and listener registration

**Files**:
- `engine/core/EventSystem/event.py`
- `engine/core/EventSystem/event_system.py`
- `engine/core/EventSystem/event_parser.py`

**Basic Usage**:
```python
from engine.core.EventSystem.event_parser import EventParser
from engine.core.EventSystem.event import EventType, EventFlags

parser = EventParser()

# Set up hooks
parser.set_dispatched_hook(lambda e: print(f"Event dispatched: {e}"))

# Define handlers
def on_entity_spawned(event):
    print(f"Entity spawned: {event.data}")

def on_entity_moved(event):
    print(f"Entity moved to {event.data['position']}")

# Subscribe to events
parser.subscribe(EventType.ENTITY_SPAWNED, on_entity_spawned)
parser.subscribe(EventType.ENTITY_MOVED, on_entity_moved)

# Emit events
parser.emit(
    "player_spawned",
    EventType.ENTITY_SPAWNED,
    data={"entity": "Hero", "position": (0, 0)},
    flags=EventFlags.CRITICAL
)

parser.emit(
    "player_moved",
    EventType.ENTITY_MOVED,
    data={"entity": "Hero", "position": (5, 10)}
)

# Query listeners
count = parser.get_listener_count(EventType.ENTITY_SPAWNED)
print(f"Listeners for ENTITY_SPAWNED: {count}")

# Clear listeners
parser.clear_listeners(EventType.ENTITY_SPAWNED)  # Clear specific type
parser.clear_listeners()  # Clear all
```

**Available Event Types**:
- `ENTITY_SPAWNED`, `ENTITY_REMOVED`, `ENTITY_MOVED`, `ENTITY_DAMAGED`, `ENTITY_HEALED`
- `ACTION_EXECUTED`
- `STATE_CHANGED`
- `TURN_STARTED`, `TURN_ENDED`
- `CUSTOM`

---

### 6. Message Log System

**Purpose**: Log game messages for UI display and debugging

**Files**:
- `engine/core/MessageLog/message.py`
- `engine/core/MessageLog/message_log_system.py`
- `engine/core/MessageLog/message_log_parser.py`

**Basic Usage**:
```python
from engine.core.MessageLog.message_log_parser import MessageLogParser
from engine.core.MessageLog.message import MessageType, MessageFlags

parser = MessageLogParser(max_messages=100)

# Set up hooks
parser.set_message_added_hook(lambda m: print(f"Message added: {m}"))

# Log messages with convenience methods
parser.log_info("Game started")
parser.log_warning("Low health!")
parser.log_error("Critical failure")
parser.log_debug("Debug info")
parser.log_game_event("Player defeated Goblin", MessageFlags.IMPORTANT)

# Custom logging
parser.log("Custom message", MessageType.GAME_EVENT, MessageFlags.SYSTEM)

# Query messages
recent = parser.get_recent_messages(limit=10)
info_msgs = parser.get_messages(MessageType.INFO)
count = parser.get_message_count_by_type(MessageType.GAME_EVENT)

# Get latest
latest = parser.get_latest_message()

# Clear log
parser.clear_messages()
```

**Message Types**:
- `INFO`, `WARNING`, `ERROR`, `DEBUG`, `GAME_EVENT`

**Message Flags**:
- `IMPORTANT`, `SYSTEM`

---

### 7. Visibility System

**Purpose**: Manage tile visibility and line-of-sight for fog of war

**Files**:
- `engine/core/VisibilitySystem/visibility.py`
- `engine/core/VisibilitySystem/visibility_system.py`
- `engine/core/VisibilitySystem/visibility_parser.py`

**Basic Usage**:
```python
from engine.core.VisibilitySystem.visibility_parser import VisibilityParser
from engine.core.VisibilitySystem.visibility import VisibilityType, VisibilityFlags

parser = VisibilityParser(grid_width=100, grid_height=100)

# Set up hooks
parser.set_visibility_changed_hook(lambda v: print(f"Visibility changed"))
parser.set_observer_added_hook(lambda pos, eid: print(f"Observer added"))

# Create tiles
tile = parser.create_tile(
    (5, 5), 
    VisibilityType.VISIBLE,
    VisibilityFlags.LIGHT_SOURCE | VisibilityFlags.TRANSPARENT
)

# Set visibility
parser.set_tile_visibility((5, 5), VisibilityType.FOG_OF_WAR)

# Manage observers (entities that can see)
parser.add_observer((5, 5), entity_id=1)
parser.add_observer((5, 5), entity_id=2)

# Query visibility
can_see = parser.can_see((5, 5), entity_id=1)  # True
visible_tiles = parser.get_visible_tiles(entity_id=1)
observers = parser.get_observers((5, 5))

# Remove observers
parser.remove_observer((5, 5), entity_id=1)
parser.remove_entity_from_all(entity_id=1)

# Clear observers
parser.clear_observers((5, 5))
```

**Visibility Types**:
- `VISIBLE`, `HIDDEN`, `FOG_OF_WAR`

**Visibility Flags**:
- `BLOCKING`, `TRANSPARENT`, `LIGHT_SOURCE`

---

### 8. Input System

**Purpose**: Handle user input and map to actions

**Files**:
- `engine/core/InputSystem/input.py`
- `engine/core/InputSystem/input_system.py`
- `engine/core/InputSystem/input_parser.py`

---

### 9. Grid System

**Purpose**: Manage tiles and grid-based maps

**Files**:
- `engine/core/TileAndGridSystems/tile.py`
- `engine/core/TileAndGridSystems/grid.py`
- `engine/core/TileAndGridSystems/grid_parser.py`

---

### 10. Scene System

**Purpose**: Manage scenes and scene switching

**Files**:
- `engine/core/SceneSystem/scene.py`
- `engine/core/SceneSystem/scene_system.py`
- `engine/core/SceneSystem/scene_parser.py`

---

## How to Implement a New System

Follow this pattern to add a new system:

### Step 1: Create Data Class (`new_feature.py`)

```python
from enum import Enum, IntFlag

class NewFeatureType(Enum):
    TYPE_A = 1
    TYPE_B = 2

class NewFeatureFlags(IntFlag):
    NONE = 0
    FLAG_A = 1
    FLAG_B = 2

class NewFeature:
    """Engine-level data for new feature."""
    
    def __init__(self, name: str, feature_type: NewFeatureType, flags: NewFeatureFlags = NewFeatureFlags.NONE):
        self.name = name
        self.type = feature_type
        self.flags = flags
    
    def to_dict(self):
        return {
            "name": self.name,
            "type": self.type.name,
            "flags": self.flags.value
        }
    
    @classmethod
    def from_dict(cls, data):
        feature_type = NewFeatureType[data["type"]]
        flags = NewFeatureFlags(data["flags"])
        return cls(data["name"], feature_type, flags)
    
    def __repr__(self):
        return f"<NewFeature {self.name}>"
```

### Step 2: Create System Class (`new_feature_system.py`)

```python
from typing import Callable, Dict
from .new_feature import NewFeature, NewFeatureType

class NewFeatureSystem:
    """Engine-level system for new feature."""
    
    def __init__(self):
        self.features: Dict[str, NewFeature] = {}
        
        # Define hooks
        self.on_feature_created: Callable[[NewFeature], None] = None
        self.on_feature_removed: Callable[[NewFeature], None] = None
    
    def add_feature(self, feature: NewFeature):
        if feature.name in self.features:
            raise ValueError(f"Feature '{feature.name}' already exists.")
        self.features[feature.name] = feature
        if self.on_feature_created:
            self.on_feature_created(feature)
    
    def get_feature(self, name: str) -> NewFeature:
        return self.features.get(name)
    
    def remove_feature(self, name: str):
        feature = self.features.pop(name, None)
        if feature and self.on_feature_removed:
            self.on_feature_removed(feature)
```

### Step 3: Create Parser Class (`new_feature_parser.py`)

```python
from typing import Callable
from .new_feature import NewFeature, NewFeatureType, NewFeatureFlags
from .new_feature_system import NewFeatureSystem

class NewFeatureParser:
    """Game-facing API for new feature."""
    
    def __init__(self):
        self.system = NewFeatureSystem()
    
    # Game-facing commands
    def create_feature(self, name: str, feature_type: NewFeatureType) -> NewFeature:
        feature = NewFeature(name, feature_type)
        self.system.add_feature(feature)
        return feature
    
    def get_feature(self, name: str) -> NewFeature:
        return self.system.get_feature(name)
    
    def remove_feature(self, name: str):
        self.system.remove_feature(name)
    
    # Hook registration
    def set_created_hook(self, hook: Callable[[NewFeature], None]):
        self.system.on_feature_created = hook
    
    def set_removed_hook(self, hook: Callable[[NewFeature], None]):
        self.system.on_feature_removed = hook
```

### Step 4: Create Tests (`test_new_feature.py`)

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../..'))

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.NewFeatureSystem.new_feature_parser import NewFeatureParser
from engine.core.NewFeatureSystem.new_feature import NewFeatureType

def test_new_feature_system():
    clock = EngineClock()
    clock.start()
    
    parser = NewFeatureParser()
    
    # Test 1: Create features
    print("Test 1: Create Features...")
    feature = parser.create_feature("Feature1", NewFeatureType.TYPE_A)
    assert feature is not None
    print("OKAY")
    
    # Test 2: Get features
    print("Test 2: Get Features...")
    retrieved = parser.get_feature("Feature1")
    assert retrieved.name == "Feature1"
    print("OKAY")
    
    # Test 3: Remove features
    print("Test 3: Remove Features...")
    parser.remove_feature("Feature1")
    assert parser.get_feature("Feature1") is None
    print("OKAY")
    
    clock.tick()
    print(f"All tests completed in {clock.get_elapsed():.6f} seconds.")

if __name__ == "__main__":
    test_new_feature_system()
```

## Integration Examples

### Example 1: Combat System

```python
from engine.core.EntitySystem.entity_parser import EntityParser
from engine.core.EventSystem.event_parser import EventParser
from engine.core.MessageLog.message_log_parser import MessageLogParser
from engine.core.EventSystem.event import EventType
from engine.core.MessageLog.message import MessageType

def setup_combat():
    entity_parser = EntityParser()
    event_parser = EventParser()
    message_parser = MessageLogParser()
    
    # Hook entity damage to event system
    def on_entity_damaged(entity):
        event_parser.emit(
            f"{entity.name}_damaged",
            EventType.ENTITY_DAMAGED,
            data={"entity": entity.name, "hp": entity.hp}
        )
        message_parser.log_game_event(f"{entity.name} took damage! HP: {entity.hp}")
    
    entity_parser.set_updated_hook(on_entity_damaged)
    
    # Subscribe to damage events
    def handle_damage(event):
        print(f"Damage event: {event.data}")
    
    event_parser.subscribe(EventType.ENTITY_DAMAGED, handle_damage)
    
    return entity_parser, event_parser, message_parser
```

### Example 2: Game Loop with Turn System

```python
from engine.core.TurnSystem.turn_parser import TurnParser
from engine.core.ActionCommandSystem.action_parser import ActionParser
from engine.core.ActionCommandSystem.action import ActionType

def game_loop(turn_parser, action_parser):
    while True:
        # Start turn
        turn = turn_parser.next_turn()
        if not turn:
            break  # No more entities
        
        entity_id = turn_parser.current_entity()
        
        # Execute actions for this entity
        while turn_parser.spend_ap(1):
            if action_parser.has_actions_for_entity(entity_id):
                action = action_parser.execute_next_action(entity_id)
                process_action(action)
            else:
                break
        
        # End turn
        turn_parser.end_turn()

def process_action(action):
    print(f"Processing: {action}")
```

## Best Practices

1. **Always use Parser classes in game code** - Never directly instantiate System or Data classes in game logic
2. **Register hooks early** - Set up all hooks before starting your game
3. **Keep systems independent** - Don't import from other systems; use events instead
4. **Use serialization** - Call to_dict/from_dict for save/load functionality
5. **Check return values** - Methods like spend_ap or get_entity can return None/False
6. **Use flags wisely** - Flags combine with bitwise operations for flexible state

## Running Tests

```bash
cd /home/soleo/Desktop/Wizardry
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_entity.py
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_event.py
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_message_log.py
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_visibility.py
```

## Project Structure

```
Wizardry/
├── engine/
│   └── core/
│       ├── ActionCommandSystem/
│       ├── ClockSystem/
│       ├── DirectionMovementSystem/
│       ├── EntitySystem/
│       ├── EventSystem/
│       ├── InputSystem/
│       ├── MapTransitionSystem/
│       ├── MessageLog/
│       ├── SceneSystem/
│       ├── SerializationSystems/
│       ├── StateSystem/
│       ├── TileAndGridSystems/
│       ├── TurnSystem/
│       └── VisibilitySystem/
├── Test_game/
│   └── tests/
│       ├── test_entity.py
│       ├── test_event.py
│       ├── test_message_log.py
│       ├── test_visibility.py
│       └── ...
└── README.md
```

## License

This engine is part of the Wizardry project.
>>>>>>> 47cc368 (Initial commit: Complete Wizardry Engine with all systems and comprehensive README)
