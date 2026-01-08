class DirectionMovementParser:
    def __init__(self, system):
        self.system = system

    def forward(self, entity, facing):
        return self.system.move_forward(entity, facing)

    def left(self, entity, facing):
        return self.system.strafe_left(entity, facing)

    def right(self, entity, facing):
        return self.system.strafe_right(entity, facing)

    def turn_left(self, facing):
        return self.system.turn_left(facing)

    def turn_right(self, facing):
        return self.system.turn_right(facing)
