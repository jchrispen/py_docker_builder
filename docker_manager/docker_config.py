import json
from typing import Any, Optional, Union

class DockerConfig:
    def __init__(self, config_path: Optional[str] = None, config_json: Optional[str] = None, config_dict: Optional[dict] = None):
        if config_dict:
            self.config = config_dict
        elif config_path:
            self.config = self.load_config_from_file(config_path)
        elif config_json:
            self.config = json.loads(config_json)
        else:
            raise ValueError("One of config_path, config_json, or config_dict must be provided")

    def load_config_from_file(self, config_path: str) -> dict:
        """Loads configuration from a JSON file."""
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading configuration from file: {e}")

    def get_config_value(self, key: str, default: Optional[Any] = None) -> Any:
        """Gets a specific configuration value."""
        return self.config.get(key, default)
