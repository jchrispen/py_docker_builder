import unittest
from unittest.mock import MagicMock, Mock, patch
from docker.errors import BuildError, APIError
import sys
import os
import logging

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_image_builder import DockerImageBuilder
from docker_manager.docker_utility import DockerUtility


class TestDockerImageBuilder(unittest.TestCase):

    def setUp(self):
        self.mock_config = MagicMock()
        self.test_config = {
            'image_name': 'test_image',
            'tag_format': 'latest',
            'dockerfile': 'Dockerfile',
            'logging_enabled': False,
            'verbose': False,
            'log_file': 'test_log.txt',
            'log_level': logging.DEBUG
        }

        # Define the mock function within setUp
        def mock_get_custom_config_value(key, use_default=False):
            return self.test_config.get(key)

        # Apply the mock function as a side effect
        self.mock_config.get_custom_config_value.side_effect = mock_get_custom_config_value

        # Ensure `.config` returns a serializable object
        self.mock_config.config = self.test_config

        # Now, this mock behavior will be used for initializing DockerImageBuilder
        self.builder = DockerImageBuilder(self.mock_config)

    @patch('docker.models.images.ImageCollection.list')
    def test_list_images(self, mock_list):
        # Setup mock response
        mock_list.return_value = [Mock(tags=['image1:latest']), Mock(tags=['image2:v1'])]

        # Execute the method
        self.builder.list_images()

        # Check if the docker list method was called
        mock_list.assert_called_once()

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_success")
    @patch('docker_manager.docker_image_builder.docker.from_env')
    def test_build_image_success(self, mock_docker_from_env, mock_create_tag):
        # Create a mock for the Docker client and its chain of method calls
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.images.build.return_value = ("mock_image_id", "mock_output_log")

        # Define the expected result
        expected_image_name_tag = 'test_image:test_success'

        # Call the method
        result = self.builder.build_image()

        # Assert the expected result
        self.assertEqual(result, expected_image_name_tag)

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_build_error")
    @patch('docker_manager.docker_image_builder.docker')
    def test_build_image_build_error(self, mock_docker, mock_create_tag):
        # Simulate a BuildError
        mock_docker.from_env().images.build.side_effect = BuildError(reason="build failed", build_log=[])

        # Call the method and assert None is returned
        self.assertIsNone(self.builder.build_image())

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_api_error")
    @patch('docker_manager.docker_image_builder.docker')
    def test_build_image_api_error(self, mock_docker, mock_create_tag):
        # Simulate an APIError
        mock_docker.from_env().images.build.side_effect = APIError("api error")

        # Call the method and assert None is returned
        self.assertIsNone(self.builder.build_image())


if __name__ == '__main__':
    unittest.main()
