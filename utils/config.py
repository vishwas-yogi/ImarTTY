import os
import yaml
from typing import Any, Dict

DEFAULT_CONFIG = {
    "theme": "default",
    "ai_provider": "gemini",
    "history_file": os.path.expanduser("~/.imartty_history.db"),
    "auto_scroll": True
}

class ConfigManager:
    def __init__(self, config_path: str = "config.yaml"):
        self.config_path = config_path
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """Load config from file or return defaults."""
        if not os.path.exists(self.config_path):
            return DEFAULT_CONFIG.copy()
        
        try:
            with open(self.config_path, 'r') as f:
                user_config = yaml.safe_load(f) or {}
                # Merge with defaults
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except Exception as e:
            print(f"Error loading config: {e}")
            return DEFAULT_CONFIG.copy()

    def get(self, key: str, default: Any = None) -> Any:
        """Get a config value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any):
        """Set a config value and save."""
        self.config[key] = value
        self._save_config()

    def _save_config(self):
        """Save current config to file."""
        try:
            with open(self.config_path, 'w') as f:
                yaml.dump(self.config, f)
        except Exception as e:
            print(f"Error saving config: {e}")
