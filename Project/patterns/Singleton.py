import json
from pathlib import Path
from threading import Lock
from typing import Any, Dict, Optional

class Config:
    """
    Singleton configuration loader.
    Loads settings once from config.json and shares them across the system.
    """

    _instance = None
    _lock = Lock()

    def __new__(cls, path: Optional[str] = None):
        """
        Enforces Singleton behavior — only one instance will ever be created.
        """
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance

    def __init__(self, path: Optional[str] = None):
        if self._initialized:
            return  # Prevent reinitialization

        base_dir = Path(__file__).resolve().parent.parent  # points to: Robert/
        self._path = base_dir / "data" / "config.json"
        self._data: Dict[str, Any] = {}
        self._load()
        self._initialized = True

    def _load(self) -> None:
        if not self._path.exists():
            raise FileNotFoundError(f"Config file not found: {self._path}")

        with self._path.open("r", encoding="utf-8") as f:
            self._data = json.load(f)

    # Public API
    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def require(self, key: str) -> Any:
        if key not in self._data:
            raise KeyError(f"Missing required config key: {key}")
        return self._data[key]

    def reload(self) -> None:
        """Reloads the configuration file in place (same singleton instance)."""
        self._load()

    def to_dict(self) -> Dict[str, Any]:
        return dict(self._data)
