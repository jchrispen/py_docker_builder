import json
from typing import Any, Optional, Union


class DockerConfig:
    def __init__(self, config_path: Optional[str] = None, config_json: Optional[str] = None,
                 config_dict: Optional[dict] = None):
        if config_dict:
            self.config = config_dict
        elif config_path:
            self.config = self.load_config_from_file(config_path)
        elif config_json:
            self.config = json.loads(config_json)
        else:
            raise ValueError("One of config_path, config_json, or config_dict must be provided")

    @staticmethod
    def load_config_from_file(config_path: str) -> dict:
        """Loads configuration from a JSON file."""
        try:
            with open(config_path, 'r') as config_file:
                return json.load(config_file)
        except (IOError, json.JSONDecodeError) as e:
            raise ValueError(f"Error loading configuration from file: {e}")

    def get_default_config_value(self, key: str) -> Any:
        """Gets a specific default configuration item value."""
        return self.config.get('default_fields', {}).get(key, {}).get('default_value')

    def get_default_config_name(self, key: str) -> Any:
        """Gets a specific default configuration item name."""
        return self.config.get('default_fields', {}).get(key, {}).get('field_name')

    def get_custom_config_value(self, key: str, use_default: bool = False) -> Any:
        """Gets a specific custom configuration item value."""
        value = self.config.get('custom_fields', {}).get(key, {}).get('default_value')
        if use_default and value is None:
            value = self.get_default_config_value(key)
        return value

    def get_custom_config_name(self, key: str, use_default: bool = False) -> Any:
        """Gets a specific custom configuration item name."""
        value = self.config.get('custom_fields', {}).get(key, {}).get('field_name')
        if use_default and value is None:
            value = self.get_default_config_name(key)
        return value

    def add_custom_value(self, key: str, value: Union[str, list]) -> None:
        """Adds a custom value to the configuration. Handles both single and multiple values."""
        custom_fields = 'custom_fields'
        if custom_fields not in self.config:
            self.config[custom_fields] = {}

        if isinstance(value, list):
            # Check if the key exists and its value is a list
            if key in self.config[custom_fields] and isinstance(self.config[custom_fields][key], list):
                # Append to the existing list if value is not already in the list
                if value not in self.config[custom_fields][key]:
                    self.config[custom_fields][key].append(value)
            else:
                # Set the value for the key (as a list if it's not already a list)
                self.config[custom_fields][key] = value
        else: # it's a str
            # Set the value for the key
            self.config[custom_fields][key] = value
