class Turn:
    """
    Engine-level turn data.
    Represents a single actor's turn.
    """

    def __init__(self, entity_id: int, action_points: int = 1):
        self.entity_id = entity_id
        self.action_points = action_points
        self.active = False

    def to_dict(self):
        return {
            "entity_id": self.entity_id,
            "action_points": self.action_points
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["entity_id"],
            data["action_points"]
        )

    def reset(self, points: int = 1):
        self.action_points = points
        self.active = False

    def __repr__(self):
        return f"<Turn Entity={self.entity_id} AP={self.action_points} Active={self.active}>"
