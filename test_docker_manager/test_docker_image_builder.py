#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os
sys.path.append(os.path.abspath('../'))
from docker_manager.docker_image_builder import DockerImageBuilder
from docker_manager.docker_utility import DockerUtility


class TestDockerImageBuilder(unittest.TestCase):

    def setUp(self):
        # Example JSON string for configuration
        json_config = '''
        {
            "log_file_path": "test.log",
            "image_name": "test_image",
            "tag_format": "%Y%m%d-%H%M%S"
        }
        '''
        # Parse JSON string to dictionary
        self.mock_config = json.loads(json_config)

        # Set up MagicMock to return values from the dictionary
        mock_config = MagicMock()
        mock_config.get_config_value.side_effect = lambda key: self.mock_config.get(key)

        # Create an instance of DockerDependencyChecker with the mocked config
        self.image_builder = DockerImageBuilder(mock_config)


    @patch('docker_manager.docker_utility.DockerUtility.run_command_with_output')
    def test_list_images_success(self, mock_run_command):
        # Test successful listing of Docker images
        mock_run_command.return_value = None  # Simulate successful command execution
        self.image_builder.list_images()
        mock_run_command.assert_called_with("docker images", "Failed to list Docker images.")

    @patch('docker_manager.docker_utility.DockerUtility.run_command_with_output')
    @patch('docker_manager.docker_utility.DockerUtility.create_tag')
    def test_build_image_success(self, mock_create_tag, mock_run_command):
        # Test successful building of a Docker image
        mock_create_tag.return_value = 'latest'  # Simulate tag creation
        mock_run_command.return_value = None  # Simulate successful command execution
        log_file_path = self.mock_config.get("log_file_path")
        self.image_builder.build_image()
        expected_command = "docker buildx build -t test_image:latest ."
        mock_run_command.assert_called_with(expected_command, "Docker build failed.", log_file_path)

    # Additional tests can be added for failure scenarios

if __name__ == '__main__':
    unittest.main()
