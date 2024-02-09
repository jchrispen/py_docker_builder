#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from docker.models.containers import Container
import sys
import os
import logging

from docker_manager.docker_logging import DockerLogging

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_container_manager import DockerContainerManager


class TestDockerContainerManager(unittest.TestCase):

    def setUp(self):
        self.mock_config = MagicMock()
        self.test_config = {
            'container_name': 'test_container',
            'tag_format': 'latest',
            'dockerfile': 'Dockerfile.test',
            'config_files_dir': 'config_files',
            'logging_enabled': False,
            'verbose': True,
            'log_file': 'test_log.txt',
            'log_level': logging.DEBUG,
            'initializer': __class__.__name__
        }

        # Define the mock function within setUp
        def mock_get_custom_config_value(key, use_default=False):
            return self.test_config.get(key)

        def mock_add_custom_config_value(key, value):
            self.test_config[key] = value

        # Apply the mock function(s) as a side effect(s)
        self.mock_config.get_custom_config_value.side_effect = mock_get_custom_config_value
        self.mock_config.add_custom_value.side_effect = mock_add_custom_config_value

        # Ensure `.config` returns a serializable object
        self.mock_config.config = self.test_config

        self.logger = DockerLogging(self.mock_config)
        self.docker_container_manager = DockerContainerManager(self.mock_config)

    @patch('docker.DockerClient.containers')
    def test_list_containers_success(self, mock_containers):
        self.logger.log(f'TEST: {self.test_list_containers_success.__name__}')

        # Test successful listing of Docker containers
        mock_containers.list.return_value = [MagicMock(spec=Container)]
        containers = self.docker_container_manager.list_containers()
        self.assertTrue(len(containers) > 0)
        mock_containers.list.assert_called_with(all=True)

    @patch('docker.DockerClient.containers')
    def test_create_container_success(self, mock_containers):
        self.logger.log(f'TEST: {self.test_create_container_success.__name__}')

        # Test successful creation of a Docker container
        mock_containers.create.return_value = MagicMock(spec=Container)

        container = self.docker_container_manager.create_container('image_name:tag')

        self.assertIsInstance(container, Container)
        mock_containers.create.assert_called_with('image_name:tag', name='test_container-tag', detach=True, tty=True)

    # Additional tests can be added for failure scenarios and edge cases


if __name__ == '__main__':
    unittest.main()
