#!/usr/bin/env python3

import unittest
from unittest.mock import patch, mock_open, MagicMock
from datetime import datetime
import sys
import os

sys.path.append(os.path.abspath('../'))
from docker_manager.docker_utility import DockerUtility


class TestDockerUtility(unittest.TestCase):

    def test_run_command_success(self):
        command = "exit 0"
        error_message = "Command failed"
        with patch('subprocess.Popen') as mock_popen:
            process_mock = MagicMock()
            process_mock.communicate.return_value = ("", "")  # Mock the output of communicate
            process_mock.returncode = 0  # Mock a successful return code
            mock_popen.return_value = process_mock

            DockerUtility.run_command(command, error_message)
            # Further assertions can be added here if necessary

    def test_run_command_failure(self):
        command = "exit 1"
        error_message = "Command failed"
        with patch('subprocess.Popen') as mock_popen:
            process_mock = MagicMock()
            process_mock.communicate.return_value = ("", "")  # Mock the output of communicate
            process_mock.returncode = 1  # Mock a non-zero return code
            mock_popen.return_value = process_mock

            with self.assertRaises(Exception) as context:
                DockerUtility.run_command(command, error_message)
            self.assertIn(error_message, str(context.exception))

    @patch('docker_manager.docker_utility.datetime')
    def test_create_tag(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 31, 0, 17, 0)
        date_format = "%Y%m%d%H%M%S"
        expected_git_commit_hash = "abc123"
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.communicate.return_value = (expected_git_commit_hash, '')
            expected_timestamp = mock_datetime.now().strftime(date_format)
            tag = DockerUtility.create_tag(date_format)
            expected_tag = f"{expected_timestamp}-{expected_git_commit_hash}"
            self.assertEqual(tag, expected_tag)

    @patch('docker_manager.docker_utility.datetime')
    def test_create_tag_no_git_hash(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2024, 1, 31, 0, 17, 0)
        date_format = "%Y%m%d%H%M%S"
        expected_git_commit_hash = ""
        with patch('subprocess.Popen') as mock_popen:
            mock_popen.return_value.communicate.return_value = (expected_git_commit_hash, '')
            expected_timestamp = mock_datetime.now().strftime(date_format)
            tag = DockerUtility.create_tag(date_format)
            expected_tag = f"{expected_timestamp}"
            self.assertEqual(tag, expected_tag)


if __name__ == '__main__':
    unittest.main()
