"""
Drawing System - Engine layer for processing draw commands

Manages draw command registration, lifecycle, and hook system.
Completely independent from backend (Pygame, Headless, etc).
"""

from typing import Dict, List, Callable, Optional, Any
from .drawing import DrawCommand, RectCommand, CircleCommand, LineCommand, PolygonCommand


class DrawingSystem:
    """
    Manages all drawing commands for rendering.
    
    Communication is hook-based - backends register themselves
    to receive draw commands without direct coupling.
    """
    
    def __init__(self):
        """Initialize the drawing system."""
        self.commands: Dict[str, DrawCommand] = {}
        self.command_list: List[DrawCommand] = []
        
        # Hooks for backends to register
        self.on_draw_hooks: List[Callable] = []
        self.on_command_added: List[Callable] = []
        self.on_command_removed: List[Callable] = []
    
    def register_draw_hook(self, hook: Callable):
        """Register a backend to receive draw commands."""
        if hook not in self.on_draw_hooks:
            self.on_draw_hooks.append(hook)
    
    def unregister_draw_hook(self, hook: Callable):
        """Unregister a backend."""
        if hook in self.on_draw_hooks:
            self.on_draw_hooks.remove(hook)
    
    def register_add_hook(self, hook: Callable):
        """Register hook for when commands are added."""
        if hook not in self.on_command_added:
            self.on_command_added.append(hook)
    
    def register_remove_hook(self, hook: Callable):
        """Register hook for when commands are removed."""
        if hook not in self.on_command_removed:
            self.on_command_removed.append(hook)
    
    def add_command(self, command: DrawCommand) -> str:
        """Add a draw command."""
        if command.name in self.commands:
            raise ValueError(f"Draw command '{command.name}' already exists")
        
        self.commands[command.name] = command
        self.command_list.append(command)
        
        # Trigger hooks
        for hook in self.on_command_added:
            hook(command)
        
        return command.name
    
    def remove_command(self, name: str) -> Optional[DrawCommand]:
        """Remove a draw command."""
        if name not in self.commands:
            return None
        
        command = self.commands.pop(name)
        self.command_list.remove(command)
        
        # Trigger hooks
        for hook in self.on_command_removed:
            hook(command)
        
        return command
    
    def get_command(self, name: str) -> Optional[DrawCommand]:
        """Get a draw command by name."""
        return self.commands.get(name)
    
    def update_command(self, name: str, **kwargs) -> bool:
        """Update command properties."""
        if name not in self.commands:
            return False
        
        command = self.commands[name]
        for key, value in kwargs.items():
            if hasattr(command, key):
                setattr(command, key, value)
        
        return True
    
    def draw(self):
        """Process all draw commands through hooks."""
        # Sort by layer for correct rendering order
        sorted_commands = sorted(
            self.command_list,
            key=lambda cmd: cmd.layer.value
        )
        
        # Send to all registered backends
        for hook in self.on_draw_hooks:
            hook(sorted_commands)
    
    def clear_all(self):
        """Clear all draw commands."""
        self.commands.clear()
        self.command_list.clear()
    
    def get_all_commands(self) -> List[DrawCommand]:
        """Get all draw commands."""
        return list(self.command_list)
    
    def get_commands_by_layer(self, layer) -> List[DrawCommand]:
        """Get commands for a specific layer."""
        return [cmd for cmd in self.command_list if cmd.layer == layer]
    
    def to_dict(self) -> dict:
        """Serialize drawing system state."""
        return {
            'commands': {
                name: {
                    'type': cmd.command_type,
                    'data': cmd.__dict__
                }
                for name, cmd in self.commands.items()
            }
        }
