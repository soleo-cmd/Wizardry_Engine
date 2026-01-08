# engine/core/StateSystems/scene_parser.py
from typing import Callable
from .scene import Scene, SceneType, SceneFlags
from .scene_system import SceneSystem

class SceneParser:
    """
    Game-facing API for scene management.
    Similar to Godot's scene tree.
    """
    def __init__(self):
        self.system = SceneSystem()

    # -----------------------------
    # Scene Commands
    # -----------------------------
    def create_scene(self, name: str, scene_type: SceneType, flags: SceneFlags = SceneFlags(0), nodes: list = None) -> Scene:
        scene = Scene(name, scene_type, flags, nodes)
        self.system.add_scene(scene)
        return scene

    def get_scene(self, name: str) -> Scene:
        return self.system.get_scene(name)

    def remove_scene(self, name: str):
        self.system.remove_scene(name)

    def set_current_scene(self, name: str):
        self.system.set_current_scene(name)

    def get_current_scene(self) -> Scene | None:
        return self.system.current_scene

    # -----------------------------
    # Hooks
    # -----------------------------
    def set_created_hook(self, hook: Callable[[Scene], None]):
        self.system.on_scene_created = hook

    def set_changed_hook(self, hook: Callable[[Scene], None]):
        self.system.on_scene_changed = hook

    def set_removed_hook(self, hook: Callable[[Scene], None]):
        self.system.on_scene_removed = hook
