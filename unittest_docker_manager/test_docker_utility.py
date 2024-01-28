#!/usr/bin/env python3

import unittest
from unittest.mock import patch, mock_open
from datetime import datetime
import subprocess
import sys
import os
sys.path.append(os.path.abspath('../'))
from docker_manager.docker_utility import DockerUtility


class TestDockerUtility(unittest.TestCase):

    def test_run_command_success(self):
        command = "echo 'Hello, World!'"
        error_message = "Command failed"
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.stdout = iter(["Hello, World!\n"])
            mock_popen.return_value.wait.return_value = 0
            DockerUtility.run_command(command, error_message)
            mock_popen.assert_called_with(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    def test_run_command_failure(self):
        command = "exit 1"
        error_message = "Command failed"
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.wait.return_value = 1
            with self.assertRaises(Exception) as context:
                DockerUtility.run_command(command, error_message)
            self.assertIn(error_message, str(context.exception))

    def test_run_command_with_log_file(self):
        command = "echo 'Hello, World!'"
        error_message = "Command failed"
        log_file_path = "/path/to/logfile.log"
        with patch('subprocess.Popen') as mock_popen, patch("builtins.open", mock_open()) as mock_file:
            mock_popen.return_value.stdout = iter(["Hello, World!\n"])
            mock_popen.return_value.wait.return_value = 0
            DockerUtility.run_command(command, error_message, log_file_path=log_file_path)
            mock_file.assert_called_with(log_file_path, 'w')

    def test_create_tag(self):
        date_format = "%Y%m%d%H%M%S"
        git_hash_cmd = "git rev-parse --short HEAD"
        expected_timestamp = datetime.now().strftime(date_format)
        expected_git_commit_hash = "abc123"
        with patch('subprocess.getoutput', return_value=expected_git_commit_hash):
            tag = DockerUtility.create_tag(date_format)
            self.assertEqual(tag, f"{expected_timestamp}-{expected_git_commit_hash}")

    def test_create_tag_no_git_hash(self):
        date_format = "%Y%m%d%H%M%S"
        expected_timestamp = datetime.now().strftime(date_format)
        with patch('subprocess.getoutput', return_value=""):
            tag = DockerUtility.create_tag(date_format)
            self.assertEqual(tag, expected_timestamp)

if __name__ == '__main__':
    unittest.main()
