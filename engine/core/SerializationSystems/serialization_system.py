# engine/core/SerializationSystems/serialization_system.py
import json
from typing import Any, Dict

class SerializationSystem:
    """
    Engine-level serialization system.
    Can save/load data in JSON format. 
    Game objects should implement to_dict() / from_dict() for custom data.
    """
    def __init__(self):
        self.storage: Dict[str, Any] = {}  # optional in-memory storage

    # -----------------------------
    # Save / Load JSON to disk
    # -----------------------------
    def save_to_file(self, filename: str, obj: Any):
        """
        Save object to a JSON file. Object must be serializable.
        """
        try:
            if hasattr(obj, "to_dict"):
                data = obj.to_dict()
            else:
                data = obj  # assume obj is JSON-serializable
            with open(filename, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"[Serialization Error] Could not save {filename}: {e}")

    def load_from_file(self, filename: str, cls=None):
        """
        Load JSON from file. If cls is provided, calls cls.from_dict(data)
        """
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            if cls and hasattr(cls, "from_dict"):
                return cls.from_dict(data)
            return data
        except Exception as e:
            print(f"[Serialization Error] Could not load {filename}: {e}")
            return None

    # -----------------------------
    # In-Memory Storage (optional)
    # -----------------------------
    def save_to_memory(self, key: str, obj: Any):
        if hasattr(obj, "to_dict"):
            self.storage[key] = obj.to_dict()
        else:
            self.storage[key] = obj

    def load_from_memory(self, key: str, cls=None):
        data = self.storage.get(key)
        if cls and hasattr(cls, "from_dict"):
            return cls.from_dict(data)
        return data
