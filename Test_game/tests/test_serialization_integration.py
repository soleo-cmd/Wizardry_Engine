# Test_game/tests/test_serialization_integration.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from engine.core.SerializationSystems.serialization_parser import SerializationParser
from engine.core.TileAndGridSystems.grid import Grid
from engine.core.EntitySystem.entity import Entity, EntityFlags, EntityType
from engine.core.StateSystem.state import State, StateType, StateFlags
from engine.core.SceneSystem.scene import Scene, SceneType, SceneFlags

def test_game_serialization():
    parser = SerializationParser()

    # Create example objects
    grid = Grid(3, 3, None)
    player = Entity("Hero", EntityType.PLAYER, EntityFlags.ALIVE | EntityFlags.MOVABLE, 100, (2,3))
    state = State("Gameplay", StateType.GAMEPLAY, StateFlags.BLOCKS_INPUT)
    scene = Scene("Overworld", SceneType.OVERWORLD, SceneFlags.PAUSES_STATE)

    # Save everything to memory
    parser.save_memory("grid", grid)
    parser.save_memory("player", player)
    parser.save_memory("state", state)
    parser.save_memory("scene", scene)

    # Load from memory
    loaded_grid = parser.load_memory("grid", Grid)
    loaded_player = parser.load_memory("player", Entity)
    loaded_state = parser.load_memory("state", State)
    loaded_scene = parser.load_memory("scene", Scene)

    # Verify
    print("Grid size:", loaded_grid.width, "x", loaded_grid.height)
    print("Player:", loaded_player.name, loaded_player.hp)
    print("State:", loaded_state.name, loadeoleo@IcecreamMachine:~/Desktop/Wizardry$ python3 -m Test_game.tests.test_serialization_integration
Traceback (most recent call last):
  File "<frozen runpy>", line 198, in _run_module_as_main
  File "<frozen runpy>", line 88, in _run_code
  File "/home/soleo/Desktop/Wizardry/Test_game/tests/test_serialization_integration.py", line 39, in <module>
    test_game_serialization()
  File "/home/soleo/Desktop/Wizardry/Test_game/tests/test_serialization_integration.py", line 24, in test_game_serialization
    parser.save_memory("scene", scene)
  File "/home/soleo/Desktop/Wizardry/engine/core/SerializationSystems/serialization_parser.py", line 24, in save_memory
    self.system.save_to_memory(key, obj)
  File "/home/soleo/Desktop/Wizardry/engine/core/SerializationSystems/serialization_system.py", line 50, in save_to_memory
    self.storage[key] = obj.to_dict()
                        ^^^^^^^^^^^^^
  File "/home/soleo/Desktop/Wizardry/engine/core/SceneSystem/scene.py", line 31, in to_dict
    "type": self.type.name,     # Enum -> string
            ^^^^^^^^^^^^^^
AttributeError: 'int' object has no attribute 'name'
d_state.type, loaded_state.flags)
    print("Scene:", loaded_scene.name)

if __name__ == "__main__":
    test_game_serialization()
