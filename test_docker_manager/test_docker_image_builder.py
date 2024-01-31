import unittest
from unittest.mock import Mock, patch
from docker.errors import BuildError
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_image_builder import DockerImageBuilder
from docker_manager.docker_utility import DockerUtility


class TestDockerImageBuilder(unittest.TestCase):

    def setUp(self):
        self.mock_config = Mock()
        self.builder = DockerImageBuilder(self.mock_config)

    @patch('docker.models.images.ImageCollection.list')
    def test_list_images(self, mock_list):
        # Setup mock response
        mock_list.return_value = [Mock(tags=['image1:latest']), Mock(tags=['image2:v1'])]

        # Execute the method
        self.builder.list_images()

        # Check if the docker list method was called
        mock_list.assert_called_once()

    @patch('docker.models.images.ImageCollection.build')
    @patch('docker_manager.docker_utility.DockerUtility.create_tag')  # Replace 'your_module' with the actual module name
    def test_build_image_success(self, mock_create_tag, mock_build):
        # Setup mocks
        self.mock_config.get_config_value.side_effect = lambda key: \
            {'image_name': 'test_image', 'tag_format': 'latest', 'dockerfile': 'Dockerfile'}[key]
        mock_create_tag.return_value = 'v1'
        mock_build.return_value = (Mock(), ['Building...'])

        # Execute the method
        image_tag = self.builder.build_image()

        # Asserts
        self.assertEqual(image_tag, 'test_image:v1')
        mock_build.assert_called_once_with(path='.', dockerfile='Dockerfile', tag='test_image:v1')

    @patch('docker.models.images.ImageCollection.build')
    @patch('docker_manager.docker_utility.DockerUtility.create_tag')  # Replace 'your_module' with the actual module name
    def test_build_image_fail(self, mock_create_tag, mock_build):
        # Setup mocks
        self.mock_config.get_config_value.side_effect = lambda key: \
            {'image_name': 'test_image', 'tag_format': 'latest', 'dockerfile': 'Dockerfile'}[key]
        mock_create_tag.return_value = 'v1'
        mock_build.side_effect = BuildError(reason="Build failed", build_log="Error log")

        # Execute the method and assert exception
        self.assertIsNone(self.builder.build_image())


if __name__ == '__main__':
    unittest.main()
