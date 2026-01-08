import sys
import os

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from engine.core.ClockSystem.engineclock import EngineClock
from engine.core.SceneSystem.scene_parser import SceneParser
from engine.core.SceneSystem.scene import SceneType, SceneFlags
from engine.core.StateSystem.state_parser import StateParser
from engine.core.StateSystem.state import StateType, StateFlags


def test_scene_with_state_hooks():
    clock = EngineClock()
    clock.start()

    # -----------------------------
    # Initialize Parsers
    # -----------------------------
    scene_parser = SceneParser()
    state_parser = StateParser()

    # -----------------------------
    # State Hooks for logging
    # -----------------------------
    state_parser.set_created_hook(lambda s: print(f"[State Created] {s}"))
    state_parser.set_changed_hook(lambda s: print(f"[State Changed] {s}"))
    state_parser.set_removed_hook(lambda s: print(f"[State Removed] {s}"))

    # -----------------------------
    # Scene Hooks to handle states
    # -----------------------------
    def on_scene_changed(scene):
        """
        When a scene becomes active, create a state for it if it doesn't exist.
        Pause any previous state if needed.
        """
        # Map scene names to desired state types
        scene_state_map = {
            "OverworldScene": StateType.GAMEPLAY,
            "BattleScene": StateType.BATTLE,
            "MenuScene": StateType.MENU,
        }

        state_name = f"{scene.name}_State"
        state_type = scene_state_map.get(scene.name, StateType.GAMEPLAY)

        existing_state = state_parser.get_state(state_name)
        if not existing_state:
            # Create state for this scene
            state_parser.create_state(state_name, state_type)
        # Pause previous state if exists
        current_state = state_parser.get_current_state()
        if current_state and current_state.name != state_name:
            current_state.deactivate()
        # Activate the new state
        state_parser.set_current_state(state_name)

    scene_parser.set_created_hook(lambda s: print(f"[Scene Created] {s}"))
    scene_parser.set_changed_hook(on_scene_changed)
    scene_parser.set_removed_hook(lambda s: print(f"[Scene Removed] {s}"))

    # -----------------------------
    # Create Scenes
    # -----------------------------
    overworld_scene = scene_parser.create_scene(
        "OverworldScene", SceneType.OVERWORLD, SceneFlags.VISIBLE, nodes=["PlayerNode", "EnemyNode", "ChestNode"]
    )
    battle_scene = scene_parser.create_scene(
        "BattleScene", SceneType.BATTLE, SceneFlags.VISIBLE, nodes=["PlayerNode", "EnemyNode", "AttackButton"]
    )
    menu_scene = scene_parser.create_scene(
        "MenuScene", SceneType.MENU, SceneFlags.VISIBLE, nodes=["StartButton", "ExitButton", "InventoryButton"]
    )

    print("OKAY: Scenes Created")

    # -----------------------------
    # Switch Scenes
    # -----------------------------
    print("\n-- Switching to Overworld Scene --")
    scene_parser.set_current_scene("OverworldScene")
    current_state = state_parser.get_current_state()
    assert current_state.name == "OverworldScene_State"
    assert current_state.is_active()
    print("OKAY: Overworld Scene + State Active")

    print("\n-- Switching to Battle Scene --")
    scene_parser.set_current_scene("BattleScene")
    current_state = state_parser.get_current_state()
    assert current_state.name == "BattleScene_State"
    assert current_state.is_active()
    print("OKAY: Battle Scene + State Active")

    # Ensure previous state is paused
    overworld_state = state_parser.get_state("OverworldScene_State")
    assert not overworld_state.is_active()
    print("OKAY: Previous Overworld State Paused")

    print("\n-- Switching to Menu Scene --")
    scene_parser.set_current_scene("MenuScene")
    current_state = state_parser.get_current_state()
    assert current_state.name == "MenuScene_State"
    assert current_state.is_active()
    print("OKAY: Menu Scene + State Active")

    # -----------------------------
    # Timing Report
    # -----------------------------
    clock.tick()
    print(f"\nAll scene-with-states tests completed in {clock.get_elapsed():.6f} seconds.")
    print(f"Average FPS: {clock.get_fps():.2f}")


if __name__ == "__main__":
    test_scene_with_state_hooks()
