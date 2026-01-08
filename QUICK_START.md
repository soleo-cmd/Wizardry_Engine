# Quick Start Guide

## For Game Developers Using the Engine

### Installation

```bash
cd /path/to/your/game
# Add the Wizardry engine to your project path
export PYTHONPATH=$PYTHONPATH:/home/soleo/Desktop/Wizardry
```

### Basic Game Loop Example

```python
import sys
sys.path.insert(0, '/home/soleo/Desktop/Wizardry')

from engine.core.EntitySystem.entity_parser import EntityParser
from engine.core.EventSystem.event_parser import EventParser
from engine.core.MessageLog.message_log_parser import MessageLogParser
from engine.core.TurnSystem.turn_parser import TurnParser
from engine.core.ActionCommandSystem.action_parser import ActionParser
from engine.core.ActionCommandSystem.action import ActionType

from engine.core.EntitySystem.entity import EntityType, EntityFlags
from engine.core.EventSystem.event import EventType
from engine.core.MessageLog.message import MessageType

# Initialize systems
entities = EntityParser()
events = EventParser()
messages = MessageLogParser()
turns = TurnParser()
actions = ActionParser()

# Set up hooks to connect systems
def on_entity_spawned(entity):
    events.emit(f"spawn_{entity.name}", EventType.ENTITY_SPAWNED, 
                data={"entity": entity.name})

def on_event_spawned(event):
    messages.log_game_event(f"{event.data['entity']} has entered!")

entities.set_created_hook(on_entity_spawned)
events.subscribe(EventType.ENTITY_SPAWNED, on_event_spawned)

# Create game world
messages.log_info("=== Game Started ===")

player = entities.spawn_entity("Hero", EntityType.PLAYER, 
                               EntityFlags.ALIVE | EntityFlags.MOVABLE, hp=100)
enemy = entities.spawn_entity("Goblin", EntityType.ENEMY,
                              EntityFlags.ALIVE | EntityFlags.MOVABLE, hp=30)

# Register for turn system
turns.register_entity(player.name, action_points=5)
turns.register_entity(enemy.name, action_points=3)

# Simple combat loop
print("\nStarting combat...\n")
for round_num in range(2):
    # Player turn
    turn = turns.next_turn()
    entity_name = turn.entity_id
    
    print(f">>> {entity_name}'s turn")
    
    # Simulate player action
    if entity_name == player.name:
        actions.create_action(player.name, ActionType.ATTACK, target=enemy.name)
    
    # Execute actions
    while turns.spend_ap(1):
        if actions.has_actions_for_entity(entity_name):
            action = actions.execute_next_action(entity_name)
            if action:
                print(f"  - {entity_name} uses {action.type.name}")
                
                if action.type == ActionType.ATTACK:
                    entities.damage_entity(action.target, 15)
                    print(f"  - {action.target} takes 15 damage!")
        else:
            break
    
    turns.end_turn()

# Display results
print(f"\n{player.name}: {player.hp} HP")
print(f"{enemy.name}: {enemy.hp} HP")

# Show message log
print("\n=== Message Log ===")
for msg in messages.get_recent_messages(limit=10):
    print(f"  {msg.type.name}: {msg.text}")
```

### Running Tests

```bash
cd /home/soleo/Desktop/Wizardry
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_event.py
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_message_log.py
PYTHONPATH=/home/soleo/Desktop/Wizardry python Test_game/tests/test_visibility.py
```

### Common Patterns

#### Pattern 1: React to Events

```python
events = EventParser()

def handle_player_damaged(event):
    print(f"Alert: {event.data['entity']} took damage!")

events.subscribe(EventType.ENTITY_DAMAGED, handle_player_damaged)
events.emit("player_hit", EventType.ENTITY_DAMAGED, 
            data={"entity": "Hero", "amount": 25})
```

#### Pattern 2: Log Game Events

```python
messages = MessageLogParser()

messages.log_info("Game initialized")
messages.log_warning("Low mana!")
messages.log_game_event("Boss defeated!", MessageFlags.IMPORTANT)

# Query logs later
recent = messages.get_recent_messages(5)
for msg in recent:
    print(f"{msg.type.name}: {msg.text}")
```

#### Pattern 3: Fog of War

```python
visibility = VisibilityParser(grid_width=100, grid_height=100)

# Create game world
for x in range(100):
    for y in range(100):
        visibility.create_tile((x, y), VisibilityType.HIDDEN)

# Player can see tiles around them
player_x, player_y = 50, 50
vision_range = 5

for x in range(player_x - vision_range, player_x + vision_range):
    for y in range(player_y - vision_range, player_y + vision_range):
        if 0 <= x < 100 and 0 <= y < 100:
            visibility.set_tile_visibility((x, y), VisibilityType.VISIBLE)
            visibility.add_observer((x, y), entity_id=1)  # player ID

# Check what player can see
visible = visibility.get_visible_tiles(entity_id=1)
print(f"Player can see {len(visible)} tiles")
```

## Documentation

- **README.md** - Complete API reference
- **GITHUB_SETUP.md** - How to push to GitHub
- **DELIVERY_SUMMARY.md** - Project overview

## Need Help?

1. Check README.md for detailed API docs
2. Look at test files for usage examples
3. Run tests to verify installation
4. Review code examples in Quick Start Guide

## Next Steps

1. Copy this engine to your project
2. Implement your game logic using the parsers
3. Add custom events and hooks as needed
4. Extend with new systems following the pattern
5. Share your game!

---

**Happy game development! 🎮**
