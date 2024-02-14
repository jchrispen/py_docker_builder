#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import sys
import os

sys.path.append(os.path.abspath('../'))
from test_docker_manager.base_test import BaseTest
from docker_manager.docker_dependency_checker import DockerDependencyChecker


class TestDockerDependencyChecker(BaseTest):

    def setUp(self, **kwargs):
        super().setUp(initializer=self._get_current_class_name())  # ensure proper initialization
        # add custom values specific to these tests
        self.docker_config.add_custom_value("os_dependencies", ["docker", "service", "date", "git"])
        self.docker_config.add_custom_value("config_files_dir", "config_files")
        self.docker_config.add_custom_value("required_config_files", [])
        self.docker_config.add_custom_value("dockerfile", "Dockerfile")
        # Create an instance of DockerDependencyChecker with the mocked config
        self.dependency_checker = DockerDependencyChecker(self.docker_config)

    @patch('shutil.which')
    def test_check_dependencies_all_present(self, mock_which):
        # Test all dependencies are present
        mock_which.side_effect = lambda x: '/usr/bin/' + x  # Simulate all dependencies are found
        self.dependency_checker._check_dependencies()  # This should not raise an exception
        self._ppass(message='does not raise error for dependencies',
                    test_name=self._get_function_name())

    @patch('shutil.which')
    def test_check_dependencies_missing(self, mock_which):
        # Test handling missing dependencies
        mock_which.return_value = None  # Simulate missing dependencies
        with self.assertRaises(Exception) as context:
            self.dependency_checker._check_dependencies()
            self.assertIn("Missing dependencies", str(context.exception))
        self._ppass(message='properly raises error for missing dependencies',
                    test_name=self._get_function_name())

    @patch('os.path.isfile')
    def test_check_required_files_all_present(self, mock_isfile):
        # Test all required files are present
        mock_isfile.return_value = True  # Simulate all files exist
        self.dependency_checker._check_required_files()  # This should not raise an exception
        self._ppass(message='does not raise error',
                    test_name=self._get_function_name())

    @patch('os.path.isfile')
    def test_check_required_files_missing(self, mock_isfile):
        # Test handling missing required files
        mock_isfile.return_value = False  # Simulate missing files
        with self.assertRaises(Exception) as context:
            self.dependency_checker._check_required_files()
            self.assertIn("Missing required files", str(context.exception))
        self._ppass(message='properly raises error',
                    test_name=self._get_function_name())


if __name__ == '__main__':
    unittest.main()
