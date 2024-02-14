import unittest
from unittest.mock import MagicMock, Mock, patch
from docker.errors import BuildError, APIError
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_image_builder import DockerImageBuilder
from test_docker_manager.base_test import BaseTest


class TestDockerImageBuilder(BaseTest):

    def setUp(self, **kwargs):
        super().setUp(initializer=self._get_current_class_name())  # ensure proper initialization
        # add custom values specific to these tests
        self.docker_config.add_custom_value('image_name', 'test_image')
        self.docker_config.add_custom_value('tag_format', 'latest')
        self.docker_config.add_custom_value('dockerfile', 'Dockerfile.test')
        self.docker_config.add_custom_value('config_files_dir', 'config_files')
        # initializing DockerImageBuilder
        self.builder = DockerImageBuilder(self.docker_config)

    @patch('docker.models.images.ImageCollection.list')
    def test_list_images(self, mock_list):
        # Setup mock response
        mock_list.return_value = [Mock(tags=['image1:latest']), Mock(tags=['image2:v1'])]

        # Execute the method
        self.builder.list_images()

        # Check if the docker list method was called
        mock_list.assert_called_once()
        self._ppass(message='method called',
                    test_name=self._get_function_name())

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_success")
    @patch('docker_manager.docker_image_builder.docker.from_env')
    def test_build_image_success(self, mock_docker_from_env, mock_create_tag):
        # Create a mock for the Docker client and its chain of method calls
        mock_client = MagicMock()
        mock_docker_from_env.return_value = mock_client
        mock_client.images.build.return_value = ("mock_image_id", ["mock_output_log"])

        # Define the expected result
        expected_image_name_tag = 'test_image:test_success'

        # Call the method
        result = self.builder.build_image()

        # Assert the expected result
        self.assertEqual(result, expected_image_name_tag)
        self._ppass(message='returns expected image:tag',
                    test_name=self._get_function_name())

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_build_error")
    @patch('docker_manager.docker_image_builder.docker')
    def test_build_image_build_error(self, mock_docker, mock_create_tag):
        # Simulate a BuildError
        mock_docker.from_env().images.build.side_effect = BuildError(reason="build failed", build_log=[])

        # Call the method and assert None is returned
        self.assertIsNone(self.builder.build_image())
        self._ppass(message='returns None on build error',
                    test_name=self._get_function_name())

    @patch('docker_manager.docker_image_builder.DockerUtility.create_tag', return_value="test_api_error")
    @patch('docker_manager.docker_image_builder.docker')
    def test_build_image_api_error(self, mock_docker, mock_create_tag):
        # Simulate an APIError
        mock_docker.from_env().images.build.side_effect = APIError("api error")

        # Call the method and assert None is returned
        self.assertIsNone(self.builder.build_image())
        self._ppass(message='returns None on api error',
                    test_name=self._get_function_name())


if __name__ == '__main__':
    unittest.main()
