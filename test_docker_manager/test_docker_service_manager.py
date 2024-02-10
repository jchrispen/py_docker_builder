#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from docker.errors import APIError
import sys
import os

sys.path.append(os.path.abspath('../'))
from test_docker_manager.base_test import BaseTest
from docker_manager.docker_service_manager import DockerServiceManager


class TestDockerServiceManager(BaseTest):

    def setUp(self, **kwargs):
        super().setUp(initializer=self._get_current_class_name())  # ensure proper initialization

    @patch('docker.DockerClient.ping')
    @patch('docker.from_env')
    def test_is_docker_running_true(self, mock_from_env, mock_ping):
        # Test detection of Docker running
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_ping.return_value = None  # ping succeeds without raising an exception

        self.assertTrue(DockerServiceManager.is_docker_running())
        self._ppass(message='ping succeeds',
                    test_name=self._get_current_function_name())

    @patch('docker.from_env')
    def test_is_docker_running_false(self, mock_from_env):
        # Create a mock Docker client
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        # Set the ping method to raise an APIError
        mock_client.ping.side_effect = APIError("Docker daemon not running")

        self.assertFalse(DockerServiceManager.is_docker_running())
        self._ppass(message='ping fails',
                    test_name=self._get_current_function_name())

    @patch('subprocess.run')
    def test_start_docker_success(self, mock_run):
        # Test successful start of Docker service
        mock_run.return_value = MagicMock(returncode=0)
        self.assertTrue(DockerServiceManager.start_docker())
        self._ppass(message='service starts',
                    test_name=self._get_current_function_name())

    @patch('subprocess.run')
    def test_start_docker_failure(self, mock_run):
        # Test failure in starting Docker service
        mock_run.return_value = MagicMock(returncode=1, stderr='Error')
        self.assertFalse(DockerServiceManager.start_docker())
        self._ppass(message='fails to start',
                    test_name=self._get_current_function_name())


if __name__ == '__main__':
    unittest.main()
