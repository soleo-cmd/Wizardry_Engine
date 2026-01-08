# engine/core/EntitySystem/entity_parser.py
from typing import Callable
from .entity import Entity, EntityType, EntityFlags
from .entity_system import EntitySystem

class EntityParser:
    """
    Game-facing API for entity management.
    Works like GridParser for tiles.
    """
    def __init__(self):
        self.system = EntitySystem()

    # -------------------
    # Entity Commands
    # -------------------
    def spawn_entity(self, name: str, entity_type: EntityType, flags: EntityFlags = EntityFlags(0), hp: int = 100):
        entity = Entity(name, entity_type, flags, hp)
        self.system.add_entity(entity)
        return entity

    def get_entity(self, name: str):
        return self.system.get_entity(name)

    def remove_entity(self, name: str):
        self.system.remove_entity(name)

    def move_entity(self, name: str, x: int, y: int):
        self.system.move_entity(name, x, y)

    def damage_entity(self, name: str, amount: int):
        self.system.damage_entity(name, amount)

    def heal_entity(self, name: str, amount: int):
        self.system.heal_entity(name, amount)

    # -------------------
    # Hooks for game/renderers
    # -------------------
    def set_created_hook(self, hook: Callable[[Entity], None]):
        self.system.on_entity_created = hook

    def set_updated_hook(self, hook: Callable[[Entity], None]):
        self.system.on_entity_updated = hook

    def set_removed_hook(self, hook: Callable[[Entity], None]):
        self.system.on_entity_removed = hook
