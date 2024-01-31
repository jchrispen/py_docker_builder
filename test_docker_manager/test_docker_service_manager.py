#!/usr/bin/env python3

import unittest
from unittest.mock import patch, MagicMock
from docker.errors import APIError
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_service_manager import DockerServiceManager


class TestDockerServiceManager(unittest.TestCase):

    @patch('docker.DockerClient.ping')
    @patch('docker.from_env')
    def test_is_docker_running_true(self, mock_from_env, mock_ping):
        # Test detection of Docker running
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client
        mock_ping.return_value = None  # ping succeeds without raising an exception

        self.assertTrue(DockerServiceManager.is_docker_running())

    @patch('docker.from_env')
    def test_is_docker_running_false(self, mock_from_env):
        # Create a mock Docker client
        mock_client = MagicMock()
        mock_from_env.return_value = mock_client

        # Set the ping method to raise an APIError
        mock_client.ping.side_effect = APIError("Docker daemon not running")

        self.assertFalse(DockerServiceManager.is_docker_running())

    @patch('subprocess.run')
    def test_start_docker_success(self, mock_run):
        # Test successful start of Docker service
        mock_run.return_value = MagicMock(returncode=0)
        DockerServiceManager.start_docker()  # Should not raise an exception

    @patch('subprocess.run')
    def test_start_docker_failure(self, mock_run):
        # Test failure in starting Docker service
        mock_run.return_value = MagicMock(returncode=1, stderr='Error')
        self.assertFalse(DockerServiceManager.start_docker())



if __name__ == '__main__':
    unittest.main()
