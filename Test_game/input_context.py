# Test_game/input_context.py
from engine.core.InputSystem.input import Key

def setup_menu_input(parser):
    parser.add_context_action("menu", Key.UP, lambda: print("Menu UP pressed"))
    parser.add_context_action("menu", Key.DOWN, lambda: print("Menu DOWN pressed"))
    parser.add_context_action("menu", Key.ENTER, lambda: print("Menu ENTER pressed"))

def setup_overworld_input(parser):
    parser.add_context_action("overworld", Key.UP, lambda: print("Move Player Up"))
    parser.add_context_action("overworld", Key.DOWN, lambda: print("Move Player Down"))
    parser.add_context_action("overworld", Key.LEFT, lambda: print("Move Player Left"))
    parser.add_context_action("overworld", Key.RIGHT, lambda: print("Move Player Right"))
    parser.add_context_action("overworld", Key.SPACE, lambda: print("Interact"))
