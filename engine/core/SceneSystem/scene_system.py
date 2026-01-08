# engine/core/SceneSystem/scene_system.py
from typing import Callable, Dict
from .scene import Scene, SceneType, SceneFlags

class SceneSystem:
    """
    Engine-level scene system.
    Fully independent of states.
    """
    def __init__(self):
        self.scenes: Dict[str, Scene] = {}
        self.current_scene: Scene | None = None

        # Hooks
        self.on_scene_created: Callable[[Scene], None] = None
        self.on_scene_changed: Callable[[Scene], None] = None
        self.on_scene_removed: Callable[[Scene], None] = None

    # -----------------------------
    # Scene Management
    # -----------------------------
    def add_scene(self, scene: Scene):
        if scene.name in self.scenes:
            raise ValueError(f"Scene '{scene.name}' already exists.")
        self.scenes[scene.name] = scene
        if self.on_scene_created:
            self.on_scene_created(scene)

    def get_scene(self, name: str) -> Scene:
        return self.scenes.get(name)

    def remove_scene(self, name: str):
        scene = self.scenes.pop(name, None)
        if scene and self.on_scene_removed:
            self.on_scene_removed(scene)
        if self.current_scene == scene:
            self.current_scene = None

    # -----------------------------
    # Scene Switching
    # -----------------------------
    def set_current_scene(self, name: str):
        scene = self.get_scene(name)
        if not scene:
            raise ValueError(f"Scene '{name}' does not exist.")
        if self.current_scene:
            self.current_scene.deactivate()
        scene.activate()
        self.current_scene = scene
        if self.on_scene_changed:
            self.on_scene_changed(scene)
