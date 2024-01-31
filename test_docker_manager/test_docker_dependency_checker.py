#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_dependency_checker import DockerDependencyChecker
from docker_manager.docker_config import DockerConfig


class TestDockerDependencyChecker(unittest.TestCase):

    def setUp(self):
        # Test 'valid' JSON string for configuration
        json_config = '''
            {
                "custom_fields": {
                    "os_dependencies": ["docker", "service", "date", "git"],
                    "config_files_dir": "config_files"
                },
                "default_fields": {
                    "logging_enabled": {
                        "field_name": "logging_enabled",
                        "default_value": false,
                        "required": true
                    },
                    "required_config_files": {
                        "field_name": "required_config_files",
                        "default_value": [],
                        "required": false
                    },
                    "dockerfile": {
                        "field_name": "dockerfile",
                        "default_value": "Dockerfile",
                        "required": true
                    }
                }
            }
        '''

        # Create an instance of DockerConfig to use with DockerDependencyChecker
        docker_config = DockerConfig(config_json=json_config)
        # Create an instance of DockerDependencyChecker with the mocked config
        self.dependency_checker = DockerDependencyChecker(docker_config)

    @patch('shutil.which')
    def test_check_dependencies_all_present(self, mock_which):
        # Test all dependencies are present
        mock_which.side_effect = lambda x: '/usr/bin/' + x  # Simulate all dependencies are found
        self.dependency_checker._check_dependencies()  # This should not raise an exception

    @patch('shutil.which')
    def test_check_dependencies_missing(self, mock_which):
        # Test handling missing dependencies
        mock_which.return_value = None  # Simulate missing dependencies
        with self.assertRaises(Exception) as context:
            self.dependency_checker._check_dependencies()
            self.assertIn("Missing dependencies", str(context.exception))

    @patch('os.path.isfile')
    def test_check_required_files_all_present(self, mock_isfile):
        # Test all required files are present
        mock_isfile.return_value = True  # Simulate all files exist
        self.dependency_checker._check_required_files()  # This should not raise an exception

    @patch('os.path.isfile')
    def test_check_required_files_missing(self, mock_isfile):
        # Test handling missing required files
        mock_isfile.return_value = False  # Simulate missing files
        with self.assertRaises(Exception) as context:
            self.dependency_checker._check_required_files()
            self.assertIn("Missing required files", str(context.exception))


if __name__ == '__main__':
    unittest.main()
