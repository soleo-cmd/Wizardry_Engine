# engine/core/SerializationSystems/serialization_parser.py
from .serialization_system import SerializationSystem

class SerializationParser:
    """
    Game-facing API to handle saving and loading.
    """
    def __init__(self):
        self.system = SerializationSystem()

    # -----------------------------
    # Save / Load File
    # -----------------------------
    def save(self, filename: str, obj):
        self.system.save_to_file(filename, obj)

    def load(self, filename: str, cls=None):
        return self.system.load_from_file(filename, cls)

    # -----------------------------
    # Save / Load Memory (optional)
    # -----------------------------
    def save_memory(self, key: str, obj):
        self.system.save_to_memory(key, obj)

    def load_memory(self, key: str, cls=None):
        return self.system.load_from_memory(key, cls)
