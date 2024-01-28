#!/usr/bin/env python3

import unittest
from unittest.mock import patch
import sys
import os
sys.path.append(os.path.abspath('../'))
from docker_manager.docker_image_builder import DockerImageBuilder


class TestDockerImageBuilder(unittest.TestCase):

    def setUp(self):
        # Mock configuration
        self.mock_config = {
            'log_file_path': '/path/to/log',
            'image_name': 'test_image',
            'tag_format': 'latest'
        }
        self.image_builder = DockerImageBuilder(self.mock_config)

    @patch('docker_utility.DockerUtility.run_command_with_output')
    def test_list_images_success(self, mock_run_command):
        # Test successful listing of Docker images
        mock_run_command.return_value = None  # Simulate successful command execution
        self.image_builder.list_images()
        mock_run_command.assert_called_with("docker images", "Failed to list Docker images.")

    @patch('docker_utility.DockerUtility.run_command_with_output')
    @patch('docker_utility.DockerUtility.create_tag')
    def test_build_image_success(self, mock_create_tag, mock_run_command):
        # Test successful building of a Docker image
        mock_create_tag.return_value = 'latest'  # Simulate tag creation
        mock_run_command.return_value = None  # Simulate successful command execution
        self.image_builder.build_image()
        expected_command = "docker buildx build -t test_image:latest ."
        mock_run_command.assert_called_with(expected_command, "Docker build failed.")

    # Additional tests can be added for failure scenarios

if __name__ == '__main__':
    unittest.main()
