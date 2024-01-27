import json


class DockerConfig:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        """Loads configuration from a JSON file."""
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def get_config_value(self, key):
        """Gets a specific configuration value."""
        return self.config.get(key, None)  # Returns None if key is not found
