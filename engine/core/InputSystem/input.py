# engine/core/InputSystem/input_enum.py
from enum import Enum, auto

class Key(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    ENTER = auto()
    ESCAPE = auto()
    SPACE = auto()
    PAUSE = auto()
    # Movement/interaction keys (semantic names for game binding)
    TURN_LEFT = auto()   # typically 'A'
    TURN_RIGHT = auto()  # typically 'D'
    STRAFE_LEFT = auto() # typically 'Q'
    STRAFE_RIGHT = auto()# typically 'E'
    # Add more keys as needed
