import unittest
from unittest.mock import patch, MagicMock
from docker_utility import DockerUtility

class TestDockerUtility(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_run_command_success(self, mock_popen):
        # Test successful execution of a command
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('output', ''), 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        DockerUtility.run_command("echo 'Hello'", "Command failed")
        # Assertions can be added to check the handling of command output

    @patch('subprocess.Popen')
    def test_run_command_failure(self, mock_popen):
        # Test handling of command failure
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('', 'error'), 'returncode': 1}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        with self.assertRaises(Exception) as context:
            DockerUtility.run_command("false", "Command failed")
        self.assertIn("Command failed", str(context.exception))

    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    @patch('subprocess.Popen')
    def test_run_command_with_output_to_file(self, mock_popen, mock_open):
        # Test logging command output to a file
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('output', ''), 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        DockerUtility.run_command_with_output("echo 'Hello'", "Command failed", log_file='log.txt')
        mock_open.assert_called_with('log.txt', 'w')

        # Additional assertions can be added to check file writing behavior

if __name__ == '__main__':
    unittest.main()
