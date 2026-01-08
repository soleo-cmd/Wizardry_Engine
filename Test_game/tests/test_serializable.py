# Test_game/tests/test_serializable.py
class Player:
    def __init__(self, name, hp):
        self.name = name
        self.hp = hp

    def to_dict(self):
        return {"name": self.name, "hp": self.hp}

    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["hp"])
