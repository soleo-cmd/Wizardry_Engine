# Test_game/tests/test_input.py
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from engine.core.InputSystem.input_parser import InputParser
from engine.core.InputSystem.input import Key
import Test_game.input_context as input_context

def test_input_system():
    parser = InputParser()
    parser.bind_engine_hooks()

    # Setup contexts
    input_context.setup_menu_input(parser)
    input_context.setup_overworld_input(parser)

    # -----------------------------
    # Test Menu Context
    # -----------------------------
    parser.set_context("menu")
    print("\n-- Testing Menu Input --")
    parser.system.press_key(Key.UP)
    parser.system.press_key(Key.DOWN)
    parser.system.press_key(Key.ENTER)
    parser.system.update()  # Update prev states for next frame

    # Test just_pressed / just_released / held
    print("Key UP just pressed:", parser.system.just_pressed(Key.UP))
    parser.system.release_key(Key.UP)
    print("Key UP just released:", parser.system.just_released(Key.UP))
    print("Key DOWN held:", parser.system.held(Key.DOWN))

    # -----------------------------
    # Test Overworld Context
    # -----------------------------
    parser.set_context("overworld")
    print("\n-- Testing Overworld Input --")
    parser.system.press_key(Key.UP)
    parser.system.press_key(Key.DOWN)
    parser.system.press_key(Key.LEFT)
    parser.system.press_key(Key.RIGHT)
    parser.system.press_key(Key.SPACE)
    parser.system.update()

if __name__ == "__main__":
    test_input_system()
