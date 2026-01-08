
from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.StateSystem.state_parser import StateParser
from engine.core.StateSystem.state import StateType, StateFlags

def test_state_system():
    clock = EngineClock()
    clock.start()

    parser = StateParser()

    # -----------------------------
    # Hooks for debugging
    # -----------------------------
    parser.set_created_hook(lambda s: print(f"Created {s}"))
    parser.set_changed_hook(lambda s: print(f"Changed to {s}"))
    parser.set_removed_hook(lambda s: print(f"Removed {s}"))

    # -----------------------------
    # Test 1: Create States
    # -----------------------------
    print("Test 1: Create States...")
    parser.create_state("MainMenu", StateType.MENU, StateFlags.VISIBLE | StateFlags.BLOCKS_INPUT)
    parser.create_state("Gameplay", StateType.GAMEPLAY, StateFlags.VISIBLE)
    parser.create_state("Pause", StateType.PAUSE, StateFlags.BLOCKS_INPUT)
    print("OKAY")

    # -----------------------------
    # Test 2: Switch States
    # -----------------------------
    print("Test 2: Switch States...")
    parser.set_current_state("MainMenu")
    assert parser.get_current_state().name == "MainMenu"
    parser.set_current_state("Gameplay")
    assert parser.get_current_state().name == "Gameplay"
    parser.set_current_state("Pause")
    assert parser.get_current_state().name == "Pause"
    print("OKAY")

    # -----------------------------
    # Test 3: Remove State
    # -----------------------------
    print("Test 3: Remove State...")
    parser.remove_state("MainMenu")
    parser.remove_state("Gameplay")
    assert parser.get_state("MainMenu") is None
    assert parser.get_state("Gameplay") is None
    print("OKAY")

    # -----------------------------
    # Timing Report
    # -----------------------------
    clock.tick()
    print(f"All state tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")

if __name__ == "__main__":
    test_state_system()
