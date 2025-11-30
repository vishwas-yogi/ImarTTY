import os
import pytest
import yaml
from utils.config import ConfigManager

@pytest.fixture
def config_file(tmp_path):
    path = tmp_path / "test_config.yaml"
    data = {"theme": "dark", "custom_key": "value"}
    with open(path, "w") as f:
        yaml.dump(data, f)
    return str(path)

def test_load_defaults():
    # Test with non-existent file
    manager = ConfigManager("non_existent.yaml")
    assert manager.get("theme") == "default"
    assert manager.get("ai_provider") == "gemini"

def test_load_file(config_file):
    manager = ConfigManager(config_file)
    assert manager.get("theme") == "dark"
    assert manager.get("custom_key") == "value"
    # Should still have defaults for missing keys
    assert manager.get("ai_provider") == "gemini"

def test_set_and_save(tmp_path):
    path = tmp_path / "save_config.yaml"
    manager = ConfigManager(str(path))
    
    manager.set("new_key", 123)
    assert manager.get("new_key") == 123
    
    # Reload to verify persistence
    manager2 = ConfigManager(str(path))
    assert manager2.get("new_key") == 123
