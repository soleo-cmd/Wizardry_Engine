from typing import Callable, List, Tuple
from .visibility import Visibility, VisibilityType, VisibilityFlags
from .visibility_system import VisibilitySystem

class VisibilityParser:
    """
    Game-facing API for VisibilitySystem.
    Completely independent - game code manages visibility and line-of-sight.
    """
    def __init__(self, grid_width: int = 100, grid_height: int = 100):
        self.system = VisibilitySystem(grid_width, grid_height)

    # -------------------
    # Visibility Commands
    # -------------------
    def create_tile(self, position: tuple, visibility_type: VisibilityType, flags: VisibilityFlags = VisibilityFlags.NONE) -> Visibility:
        """
        Create a visibility entry at a tile position.
        """
        return self.system.create_visibility(position, visibility_type, flags)

    def get_tile(self, position: tuple) -> Visibility:
        """
        Get the visibility data for a tile.
        """
        return self.system.get_visibility(position)

    def set_tile_visibility(self, position: tuple, visibility_type: VisibilityType):
        """
        Change the visibility state of a tile.
        """
        self.system.set_visibility_type(position, visibility_type)

    # -------------------
    # Observer Management
    # -------------------
    def add_observer(self, position: tuple, entity_id: int):
        """
        Add an entity as an observer of a position.
        """
        self.system.add_observer(position, entity_id)

    def remove_observer(self, position: tuple, entity_id: int):
        """
        Remove an entity as observer from a position.
        """
        self.system.remove_observer(position, entity_id)

    def remove_entity_from_all(self, entity_id: int):
        """
        Remove an entity as observer from all positions.
        """
        self.system.remove_entity_from_all_positions(entity_id)

    # -------------------
    # Visibility Queries
    # -------------------
    def can_see(self, position: tuple, entity_id: int) -> bool:
        """
        Check if an entity can see a position.
        """
        return self.system.is_visible_to(position, entity_id)

    def get_visible_tiles(self, entity_id: int) -> List[Tuple]:
        """
        Get all tiles visible to an entity.
        """
        return self.system.get_visible_positions_for_entity(entity_id)

    def get_observers(self, position: tuple) -> set:
        """
        Get all entities observing a position.
        """
        return self.system.get_observers_at(position)

    def clear_observers(self, position: tuple):
        """
        Clear all observers from a position.
        """
        self.system.clear_observers_at(position)

    # -------------------
    # Hooks
    # -------------------
    def set_visibility_changed_hook(self, hook: Callable[[Visibility], None]):
        """
        Hook called when visibility at a position changes.
        """
        self.system.on_visibility_changed = hook

    def set_observer_added_hook(self, hook: Callable[[Tuple, int], None]):
        """
        Hook called when an observer is added to a position.
        """
        self.system.on_observer_added = hook

    def set_observer_removed_hook(self, hook: Callable[[Tuple, int], None]):
        """
        Hook called when an observer is removed from a position.
        """
        self.system.on_observer_removed = hook
