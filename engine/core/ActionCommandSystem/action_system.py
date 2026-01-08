from collections import deque
from .action import Action

class ActionSystem:
    """
    Engine-level action queue.
    """

    def __init__(self):
        self.queue = deque()

    def add_action(self, action: Action):
        self.queue.append(action)

    def get_next_action_for_entity(self, entity_id: int):
        for action in self.queue:
            if action.entity_id == entity_id:
                self.queue.remove(action)  # remove first match
                return action
        return None

    def has_action_for_entity(self, entity_id: int):
        return any(a.entity_id == entity_id for a in self.queue)
