import unittest
import json
import os
from docker_config import DockerConfig

class TestDockerConfig(unittest.TestCase):

    def setUp(self):
        # Setup a mock configuration file
        self.mock_config_path = 'mock_config.json'
        self.mock_config = {'key1': 'value1', 'key2': 'value2'}
        with open(self.mock_config_path, 'w') as mock_config_file:
            json.dump(self.mock_config, mock_config_file)

    def tearDown(self):
        # Clean up the mock configuration file
        os.remove(self.mock_config_path)

    def test_load_config_success(self):
        # Test successful loading of configuration
        docker_config = DockerConfig(self.mock_config_path)
        self.assertEqual(docker_config.config, self.mock_config)

    def test_load_config_failure(self):
        # Test failure to load configuration from a non-existent file
        with self.assertRaises(FileNotFoundError):
            DockerConfig('non_existent_config.json')

    def test_get_config_value_existing_key(self):
        # Test retrieving an existing configuration value
        docker_config = DockerConfig(self.mock_config_path)
        self.assertEqual(docker_config.get_config_value('key1'), 'value1')

    def test_get_config_value_non_existent_key(self):
        # Test retrieving a non-existent configuration key
        docker_config = DockerConfig(self.mock_config_path)
        self.assertIsNone(docker_config.get_config_value('non_existent_key'))

if __name__ == '__main__':
    unittest.main()
