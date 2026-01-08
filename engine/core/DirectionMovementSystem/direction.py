# engine/core/DirectionMovementSystem/direction.py
from enum import Enum

class Direction(Enum):
    NORTH = (0, -1)
    EAST  = (1, 0)
    SOUTH = (0, 1)
    WEST  = (-1, 0)

    @property
    def dx(self):
        return self.value[0]

    @property
    def dy(self):
        return self.value[1]

    def turn_left(self):
        order = [Direction.NORTH, Direction.WEST, Direction.SOUTH, Direction.EAST]
        return order[(order.index(self) + 1) % 4]

    def turn_right(self):
        order = [Direction.NORTH, Direction.EAST, Direction.SOUTH, Direction.WEST]
        return order[(order.index(self) + 1) % 4]

    def opposite(self):
        return self.turn_left().turn_left()
