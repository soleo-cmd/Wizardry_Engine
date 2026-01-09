class DirectionMovementParser:
    def __init__(self, system):
        self.system = system

    def forward(self, entity):
        return self.system.move_forward(entity)
    def backward(self, entity):
        return self.system.move_backward(entity)

    def left(self, entity):
        return self.system.strafe_left(entity)

    def right(self, entity):
        return self.system.strafe_right(entity)

    def turn_left(self, entity):
        return self.system.turn_left(entity)

    def turn_right(self, entity):
        return self.system.turn_right(entity)
