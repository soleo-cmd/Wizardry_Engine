# engine/core/DirectionMovementSystem/movement_system.py

from .direction import Direction

class DirectionMovementSystem:
    def __init__(self, grid):
        self.grid = grid

    # -------------------
    # Core helpers
    # -------------------
    def _can_move_direction(self, entity, direction: Direction) -> bool:
        x, y = entity.position
        nx, ny = x + direction.dx, y + direction.dy

        if not self.grid.in_bounds(nx, ny):
            return False

        tile = self.grid.get_tile(nx, ny)
        return tile.is_walkable()

    def _move_direction(self, entity, direction: Direction) -> bool:
        if not entity.is_movable():
            return False

        if not self._can_move_direction(entity, direction):
            return False

        x, y = entity.position
        entity.position = (x + direction.dx, y + direction.dy)
        return True

    # -------------------
    # Relative movement
    # -------------------
    def move_forward(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if not facing:
            return False
        return self._move_direction(entity, facing)

    def move_backward(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if not facing:
            return False
        return self._move_direction(entity, facing.opposite())

    def strafe_left(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if not facing:
            return False
        return self._move_direction(entity, facing.turn_left())

    def strafe_right(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if not facing:
            return False
        return self._move_direction(entity, facing.turn_right())

    # -------------------
    # Rotation
    # -------------------
    def turn_left(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if facing:
            entity.data['facing'] = facing.turn_left()
            if hasattr(entity, 'facing'):
                entity.facing = entity.data['facing']
        return True

    def turn_right(self, entity):
        facing = entity.data.get('facing', entity.facing if hasattr(entity, 'facing') else None)
        if facing:
            entity.data['facing'] = facing.turn_right()
            if hasattr(entity, 'facing'):
                entity.facing = entity.data['facing']
        return True

