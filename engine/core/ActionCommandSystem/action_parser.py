from .action import Action, ActionType
from .action_system import ActionSystem

class ActionParser:
    """
    Game-facing API for ActionSystem.
    """
    def __init__(self):
        self.system = ActionSystem()
        self.on_execute_action = None  # Hook: function(action)

    def create_action(self, entity_id: int, action_type: ActionType, target=None):
        action = Action(entity_id, action_type, target=target)
        self.system.add_action(action)

    def execute_next_action(self, entity_id: int = None):
        """
        Executes the next action in the queue.
        If entity_id is provided, executes the next action for that entity only.
        Calls hook if set.
        """
        if entity_id is not None:
            action = self.system.get_next_action_for_entity(entity_id)
        else:
            if not self.system.queue:
                return None
            action = self.system.queue.popleft()

        if action and self.on_execute_action:
            self.on_execute_action(action)
        return action

    def has_actions_for_entity(self, entity_id: int):
        """
        Check if there are actions queued for a specific entity.
        """
        return self.system.has_action_for_entity(entity_id)
