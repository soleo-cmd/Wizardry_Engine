# Test_game/tests/test_serialization.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from engine.core.SerializationSystems.serialization_parser import SerializationParser
from Test_game.tests.test_serializable import Player

def test_serialization():
    parser = SerializationParser()

    player = Player("Hero", 100)

    # Save to file
    parser.save("player.json", player)
    # Load from file
    loaded_player = parser.load("player.json", Player)
    print(f"Loaded Player: {loaded_player.name}, HP: {loaded_player.hp}")

    # Save to memory
    parser.save_memory("player1", player)

    # Load from memory
    mem_player = parser.load_memory("player1", Player)
    print(f"Memory Player: {mem_player.name}, HP: {mem_player.hp}")

if __name__ == "__main__":
    test_serialization()
