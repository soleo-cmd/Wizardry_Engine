from collections import deque
from .turn import Turn

class TurnSystem:
    """
    Engine-level turn manager.
    """

    def __init__(self):
        self.turn_queue = deque()
        self.current_turn: Turn | None = None

        # -----------------------------
        # Hooks (engine-level integration)
        # -----------------------------
        self.on_turn_started = None       # Callable[[Turn], None]
        self.on_turn_ended = None         # Callable[[Turn], None]
        self.on_action_spent = None       # Callable[[Turn, int], None]

    def to_dict(self):
        return {"turn_queue": [t.to_dict() for t in self.turn_queue]}

    @classmethod 
    def from_dict(cls, data):
        system = cls()
        system.turn_queue = deque(Turn.from_dict(t) for t in data["turn_queue"])
        return system

    # -----------------------------
    # Turn Management
    # -----------------------------
    def add_entity(self, entity_id: int, action_points: int = 1):
        self.turn_queue.append(Turn(entity_id, action_points))

    def remove_entity(self, entity_id: int):
        self.turn_queue = deque(
            t for t in self.turn_queue if t.entity_id != entity_id
        )
        if self.current_turn and self.current_turn.entity_id == entity_id:
            self.current_turn = None

    # -----------------------------
    # Turn Flow
    # -----------------------------
    def start_next_turn(self) -> Turn | None:
        if not self.turn_queue:
            self.current_turn = None
            return None

        if self.current_turn:
            self.end_turn()

        self.current_turn = self.turn_queue.popleft()
        self.current_turn.active = True
        self.turn_queue.append(self.current_turn)

        if self.on_turn_started:
            self.on_turn_started(self.current_turn)

        return self.current_turn

    def end_turn(self):
        if self.current_turn:
            self.current_turn.active = False
            if self.on_turn_ended:
                self.on_turn_ended(self.current_turn)
            self.current_turn = None

    # -----------------------------
    # Action Points
    # -----------------------------
    def consume_action_point(self, amount: int = 1) -> bool:
        if not self.current_turn:
            return False

        if self.current_turn.action_points < amount:
            return False

        self.current_turn.action_points -= amount

        if self.on_action_spent:
            self.on_action_spent(self.current_turn, amount)

        return True

    # -----------------------------
    # Queries
    # -----------------------------
    def get_current_entity(self) -> int | None:
        return self.current_turn.entity_id if self.current_turn else None

    def has_active_turn(self) -> bool:
        return self.current_turn is not None
