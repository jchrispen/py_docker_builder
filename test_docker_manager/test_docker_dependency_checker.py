#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
sys.path.append(os.path.abspath('../'))
from docker_manager.docker_dependency_checker import DockerDependencyChecker


class TestDockerDependencyChecker(unittest.TestCase):

    def setUp(self):
        # Example JSON string for configuration
        json_config = '''
        {
            "os_dependencies": ["docker", "git"],
            "required_config_files": ["/path/to/required_file1", "/path/to/required_file2"]
        }
        '''
        # Parse JSON string to dictionary
        self.mock_config = json.loads(json_config)

        # Set up MagicMock to return values from the dictionary
        mock_config = MagicMock()
        mock_config.get_config_value.side_effect = lambda key: self.mock_config.get(key)

        # Create an instance of DockerDependencyChecker with the mocked config
        self.dependency_checker = DockerDependencyChecker(mock_config)

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
