# Test_game/tests/test_entity.py

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.EntitySystem.entity_parser import EntityParser
from engine.core.EntitySystem.entity import EntityType, EntityFlags

def test_entity_system():
    clock = EngineClock()
    clock.start()

    parser = EntityParser()

    # -----------------------------
    # Hooks for debugging
    # -----------------------------
    parser.set_created_hook(lambda e: print(f"Created {e}"))
    parser.set_updated_hook(lambda e: print(f"Updated {e}"))
    parser.set_removed_hook(lambda e: print(f"Removed {e}"))

    # -----------------------------
    # Test 1: Spawn Entities
    # -----------------------------
    print("Test 1: Spawn Entities...")
    player = parser.spawn_entity("Hero", EntityType.PLAYER, EntityFlags.ALIVE | EntityFlags.MOVABLE, 100)
    enemy = parser.spawn_entity("Goblin1", EntityType.ENEMY, EntityFlags.ALIVE | EntityFlags.MOVABLE, 50)
    print("OKAY")

    # -----------------------------
    # Test 2: Move Entities
    # -----------------------------
    print("Test 2: Move Entities...")
    parser.move_entity("Hero", 1, 2)
    parser.move_entity("Goblin1", 3, 4)
    print("OKAY")

    # -----------------------------
    # Test 3: Damage Entities
    # -----------------------------
    print("Test 3: Damage Entities...")
    parser.damage_entity("Goblin1", 20)
    assert parser.get_entity("Goblin1").hp == 30
    parser.damage_entity("Hero", 50)
    assert parser.get_entity("Hero").hp == 50
    print("OKAY")

    # -----------------------------
    # Test 4: Heal Entities
    # -----------------------------
    print("Test 4: Heal Entities...")
    parser.heal_entity("Goblin1", 10)
    parser.heal_entity("Hero", 20)
    assert parser.get_entity("Goblin1").hp == 40
    assert parser.get_entity("Hero").hp == 70
    print("OKAY")

    # -----------------------------
    # Test 5: Remove Entity
    # -----------------------------
    print("Test 5: Remove Entity...")
    parser.remove_entity("Goblin1")
    assert parser.get_entity("Goblin1") is None
    print("OKAY")

    # -----------------------------
    # Report Timing
    # -----------------------------
    clock.tick()
    print(f"All entity tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_entity_system()
