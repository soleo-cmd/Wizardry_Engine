# engine/core/EntitySystem/entity_system.py
from typing import Callable, Dict
from .entity import Entity

class EntitySystem:
    """
    Manages all entities.
    """
    def __init__(self):
        self.entities: Dict[str, Entity] = {}  # store entities by unique name

        # Hooks
        self.on_entity_created: Callable[[Entity], None] = None
        self.on_entity_updated: Callable[[Entity], None] = None
        self.on_entity_removed: Callable[[Entity], None] = None

    # -------------------
    # Entity Management
    # -------------------
    def add_entity(self, entity: Entity):
        if entity.name in self.entities:
            raise ValueError(f"Entity '{entity.name}' already exists.")
        self.entities[entity.name] = entity
        if self.on_entity_created:
            self.on_entity_created(entity)

    def get_entity(self, name: str) -> Entity:
        return self.entities.get(name)

    def remove_entity(self, name: str):
        entity = self.entities.pop(name, None)
        if entity and self.on_entity_removed:
            self.on_entity_removed(entity)

    # -------------------
    # Update / Tick
    # -------------------
    def move_entity(self, name: str, x: int, y: int):
        entity = self.get_entity(name)
        if entity:
            entity.move(x, y)
            if self.on_entity_updated:
                self.on_entity_updated(entity)

    def damage_entity(self, name: str, amount: int):
        entity = self.get_entity(name)
        if entity:
            entity.take_damage(amount)
            if self.on_entity_updated:
                self.on_entity_updated(entity)

    def heal_entity(self, name: str, amount: int):
        entity = self.get_entity(name)
        if entity:
            entity.heal(amount)
            if self.on_entity_updated:
                self.on_entity_updated(entity)
