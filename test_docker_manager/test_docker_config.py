#!/usr/bin/env python3

import unittest
import json
import sys
import os

from docker_manager.docker_logging import DockerLogging

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_config import DockerConfig


class TestDockerConfig(unittest.TestCase):

    def setUp(self):
        # Setup a mock configuration file
        self.mock_config_path = 'mock_config.json'
        self.mock_config = {
            "custom_fields": {
                "os_dependencies": ["docker", "service", "date", "git"],
                "config_files_dir": "config_files",
                "image_name": "arbitrage-bot",
                "container_name": "bot",
                "initializer": __class__.__name__,
                "verbose": True,
                "logging": False
            },
            "default_fields": {
                "verbose": {
                    "field_name": "verbose",
                    "default_value": False,
                    "required": False
                },
                "log_file": {
                    "field_name": "logging",
                    "default_value": "docker_manager.log",
                    "required": False
                }
            }
        }

        with open(self.mock_config_path, 'w') as mock_config_file:
            json.dump(self.mock_config, mock_config_file)

        self.docker_config = DockerConfig(config_dict=self.mock_config)
        self.logger = DockerLogging(self.docker_config)

    def tearDown(self):
        # Clean up the mock configuration file
        os.remove(self.mock_config_path)

    def ppass(self, message=None):
        self.logger.log(message)
        self.logger.log('PASS')

    def test_instantiation_methods(self):
        self.logger.log(f'TEST: {self.test_instantiation_methods.__name__}')

        # Instantiate with file path
        config_from_file = DockerConfig(self.mock_config_path)
        self.assertEqual(config_from_file.config, self.mock_config)
        self.ppass('instantiate with file path')

        # Instantiate with dictionary
        config_from_dict = DockerConfig(config_dict=self.mock_config)
        self.assertEqual(config_from_dict.config, self.mock_config)
        self.ppass('instantiate with dictionary')

        # Instantiate with JSON string
        config_from_json = DockerConfig(config_json=json.dumps(self.mock_config))
        self.assertEqual(config_from_json.config, self.mock_config)
        self.ppass('instantiate with JSON string')

    def test_load_config_success(self):
        self.logger.log(f'TEST: {self.test_load_config_success.__name__}')

        # Test successful loading of configuration
        docker_config = DockerConfig(self.mock_config_path)
        # Check if the top-level keys are correct
        self.assertSetEqual(set(docker_config.config.keys()), set(self.mock_config.keys()))
        self.ppass('load configuration top-level keys are correct')

        # Check if the nested structures are loaded correctly
        for key in self.mock_config:
            self.assertEqual(docker_config.config[key], self.mock_config[key])
        self.ppass('load configuration nested keys are correct')

    def test_load_config_failure(self):
        self.logger.log(f'TEST: {self.test_load_config_failure.__name__}')

        # Test failure to load configuration from a non-existent file
        with self.assertRaises(ValueError) as context:
            DockerConfig('non_existent_config.json')
        self.ppass('load config from non-existent file')

        # Update the error message check if the message has changed
        expected_error = "One of config_path, config_json, or config_dict must be provided"
        expected_alt_error = "Error loading configuration from file:"
        # Check if either of the expected messages is in the exception
        error_message = str(context.exception)
        self.assertTrue(expected_error in error_message or expected_alt_error in error_message)
        self.ppass('expected error messages')

    def test_get_default_config_value(self):
        self.logger.log(f'TEST: {self.test_get_default_config_value.__name__}')

        docker_config = DockerConfig(self.mock_config_path)

        # Assuming 'verbose' has a default value of False in default_fields
        verbose_value = docker_config.get_default_config_value('verbose')
        self.assertEqual(verbose_value, False)
        self.ppass('verbose false by default')

        # For a key that doesn't exist, you might return None or a specific default
        non_existent_value = docker_config.get_default_config_value('non_existent_key')
        self.assertIsNone(non_existent_value)
        self.ppass('Return None for non-existent key')

    def test_get_default_config_name(self):
        self.logger.log(f'TEST: {self.test_get_default_config_name.__name__}')

        docker_config = DockerConfig(self.mock_config_path)

        test_value = docker_config.get_default_config_name('log_file')
        self.assertEqual(test_value, 'logging')
        self.ppass('get default config item name')

        # For a key that doesn't exist, you might return None or a specific default
        non_existent_value = docker_config.get_default_config_name('non_existent_key')
        self.assertIsNone(non_existent_value)
        self.ppass('get default config item value')

    def test_get_custom_config_value(self):
        self.logger.log(f'TEST: {self.test_get_custom_config_value.__name__}')

        docker_config = DockerConfig(config_dict=self.mock_config)

        # Test retrieving an existing custom value
        self.assertEqual(docker_config.get_custom_config_value('config_files_dir'), 'config_files')
        self.ppass('get custom value')

        # Test retrieving a non-existing custom value
        self.assertIsNone(docker_config.get_custom_config_value('log_file'))
        self.ppass('get non-existent value')

        # Test retrieving a non-existing custom value with use_default=True
        self.assertEqual(docker_config.get_custom_config_value('log_file', use_default=True), 'docker_manager.log')
        self.ppass('get default value when no custom value exists')

        # Test retrieving a non-existent custom value with use_default=True
        self.assertIsNone(docker_config.get_custom_config_value('non_existent_key', use_default=True))
        self.ppass('return None when no custom or default value exists')

    def test_add_config_value(self):
        self.logger.log(f'TEST: {self.test_add_config_value.__name__}')

        docker_config = DockerConfig(self.mock_config_path)

        # Set a new value
        docker_config.add_custom_value('verbose', True)
        self.assertTrue(docker_config.get_custom_config_value('verbose'))
        self.ppass('add custom value')

        # Set a value in nested configuration
        docker_config.add_custom_value('container_name', 'new_bot')
        self.assertEqual(docker_config.get_custom_config_value('container_name'), 'new_bot')
        self.ppass('add nested value')

    def test_add_different_custom_values(self):
        self.logger.log(f'TEST: {self.test_add_different_custom_values.__name__}')

        docker_config = DockerConfig(config_dict=self.mock_config)

        # Add string value
        docker_config.add_custom_value('new_string_key', 'string_value')
        self.assertEqual(docker_config.get_custom_config_value('new_string_key'), 'string_value')
        self.ppass('add custom string value')

        # Add boolean value
        docker_config.add_custom_value('new_bool_key', True)
        self.assertTrue(docker_config.get_custom_config_value('new_bool_key'))
        self.ppass('add custom boolean value')

        # Add list value
        docker_config.add_custom_value('new_list_key', ['item1', 'item2'])
        self.assertEqual(docker_config.get_custom_config_value('new_list_key'), ['item1', 'item2'])
        self.ppass('add custom [list] item')


if __name__ == '__main__':
    unittest.main()
