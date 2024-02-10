#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from docker.models.containers import Container
import sys
import os

sys.path.append(os.path.abspath('../'))
from test_docker_manager.base_test import BaseTest
from docker_manager.docker_container_manager import DockerContainerManager


class TestDockerContainerManager(BaseTest):

    def setUp(self, **kwargs):
        super().setUp(initializer=self._get_current_class_name())  # ensure proper initialization
        # add custom values specific to these tests
        self.docker_config.add_custom_value('container_name', 'test_container')
        self.docker_config.add_custom_value('tag_format', 'latest')
        self.docker_config.add_custom_value('dockerfile', 'Dockerfile.test')
        self.docker_config.add_custom_value('config_files_dir', 'config_files')
        # initialize the container manager
        self.docker_container_manager = DockerContainerManager(self.docker_config)

    @patch('docker.DockerClient.containers')
    def test_list_containers_success(self, mock_containers):
        # Test successful listing of Docker containers
        mock_containers.list.return_value = [MagicMock(spec=Container)]
        containers = self.docker_container_manager.list_containers()
        self.assertTrue(len(containers) > 0)
        self._ppass('list returns values')
        mock_containers.list.assert_called_with(all=True)
        self._ppass(message='properly called with arguments',
                    test_name=self._get_current_function_name())

    @patch('docker.DockerClient.containers')
    def test_create_container_success(self, mock_containers):
        # Test successful creation of a Docker container
        mock_containers.create.return_value = MagicMock(spec=Container)

        container = self.docker_container_manager.create_container('image_name:tag')

        self.assertIsInstance(container, Container)
        self._ppass(message='returns container object',
                    test_name=self._get_current_function_name())
        mock_containers.create.assert_called_with('image_name:tag', name='test_container-tag', detach=True, tty=True)
        self._ppass(message='properly called with arguments')

    # Additional tests can be added for failure scenarios and edge cases


if __name__ == '__main__':
    unittest.main()
