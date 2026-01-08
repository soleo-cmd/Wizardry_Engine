from typing import Callable, Dict, List, Tuple
from .visibility import Visibility, VisibilityType, VisibilityFlags

class VisibilitySystem:
    """
    Engine-level visibility management system.
    Completely independent - manages visibility for tiles/entities.
    Uses a grid-based approach for line-of-sight calculations.
    """
    def __init__(self, grid_width: int = 100, grid_height: int = 100):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.visibility_map: Dict[Tuple[int, int], Visibility] = {}
        
        # Hooks
        self.on_visibility_changed: Callable[[Visibility], None] = None
        self.on_observer_added: Callable[[Tuple[int, int], int], None] = None
        self.on_observer_removed: Callable[[Tuple[int, int], int], None] = None

    def create_visibility(self, position: tuple, visibility_type: VisibilityType, flags: VisibilityFlags = VisibilityFlags.NONE) -> Visibility:
        """
        Create a visibility entry at a position.
        """
        if position in self.visibility_map:
            raise ValueError(f"Visibility already exists at {position}")
        
        visibility = Visibility(position, visibility_type, flags)
        self.visibility_map[position] = visibility
        if self.on_visibility_changed:
            self.on_visibility_changed(visibility)
        return visibility

    def get_visibility(self, position: tuple) -> Visibility:
        """
        Get visibility at a position.
        """
        return self.visibility_map.get(position)

    def set_visibility_type(self, position: tuple, visibility_type: VisibilityType):
        """
        Change the visibility type at a position.
        """
        visibility = self.get_visibility(position)
        if visibility:
            visibility.type = visibility_type
            if self.on_visibility_changed:
                self.on_visibility_changed(visibility)

    def add_observer(self, position: tuple, entity_id: int):
        """
        Add an observer (entity) that can see this position.
        """
        visibility = self.get_visibility(position)
        if visibility:
            visibility.add_observer(entity_id)
            if self.on_observer_added:
                self.on_observer_added(position, entity_id)

    def remove_observer(self, position: tuple, entity_id: int):
        """
        Remove an observer from this position.
        """
        visibility = self.get_visibility(position)
        if visibility:
            visibility.remove_observer(entity_id)
            if self.on_observer_removed:
                self.on_observer_removed(position, entity_id)

    def is_visible_to(self, position: tuple, entity_id: int) -> bool:
        """
        Check if a position is visible to a specific entity.
        """
        visibility = self.get_visibility(position)
        return visibility is not None and entity_id in visibility.observed_by if visibility else False

    def get_visible_positions_for_entity(self, entity_id: int) -> List[Tuple]:
        """
        Get all positions visible to an entity.
        """
        return [pos for pos, vis in self.visibility_map.items() if entity_id in vis.observed_by]

    def get_observers_at(self, position: tuple) -> set:
        """
        Get all entities observing a position.
        """
        visibility = self.get_visibility(position)
        return visibility.observed_by if visibility else set()

    def clear_observers_at(self, position: tuple):
        """
        Clear all observers from a position.
        """
        visibility = self.get_visibility(position)
        if visibility:
            visibility.observed_by.clear()

    def remove_entity_from_all_positions(self, entity_id: int):
        """
        Remove an entity as observer from all positions.
        """
        for position, visibility in self.visibility_map.items():
            if entity_id in visibility.observed_by:
                visibility.remove_observer(entity_id)
