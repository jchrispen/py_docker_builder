#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from docker.models.containers import Container
from docker.errors import DockerException
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_container_manager import DockerContainerManager


class TestDockerContainerManager(unittest.TestCase):

    def setUp(self):
        # Mock configuration for DockerContainerManager
        mock_config = MagicMock()
        mock_config.get_config_value.side_effect = lambda key: {'log_file_path': 'test.log',
                                                                'container_name': 'test_container'}.get(key)
        self.docker_container_manager = DockerContainerManager(mock_config)

    @patch('docker.DockerClient.containers')
    def test_list_containers_success(self, mock_containers):
        # Test successful listing of Docker containers
        mock_containers.list.return_value = [MagicMock(spec=Container)]
        containers = self.docker_container_manager.list_containers()
        self.assertTrue(len(containers) > 0)
        mock_containers.list.assert_called_with(all=True)

    @patch('docker.DockerClient.containers')
    def test_create_container_success(self, mock_containers):
        # Test successful creation of a Docker container
        mock_containers.create.return_value = MagicMock(spec=Container)
        container = self.docker_container_manager.create_container('image_name:tag')
        self.assertIsInstance(container, Container)
        mock_containers.create.assert_called_with('image_name:tag', name='test_container-tag', detach=True, tty=True)

    # Additional tests can be added for failure scenarios and edge cases


if __name__ == '__main__':
    unittest.main()
