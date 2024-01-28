import json

class DockerConfig:

    def __init__(self, config_path=None, config_json=None):
        if config_path:
            self.config = self.load_config_from_file(config_path)
        elif config_json:
            self.config = json.loads(config_json)
        else:
            raise ValueError("Either config_path or config_json must be provided")

    def load_config_from_file(self, config_path):
        """Loads configuration from a JSON file."""
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def get_config_value(self, key):
        """Gets a specific configuration value."""
        return self.config.get(key, None)  # Returns None if key is not found
