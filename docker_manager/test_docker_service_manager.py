import unittest
from unittest.mock import patch, MagicMock
from docker_service_manager import DockerServiceManager

class TestDockerServiceManager(unittest.TestCase):

    @patch('subprocess.Popen')
    def test_is_docker_running_true(self, mock_popen):
        # Test detection of Docker running
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('docker is running', ''), 'returncode': 0}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

        self.assertTrue(DockerServiceManager.is_docker_running())

    @patch('subprocess.Popen')
    def test_is_docker_running_false(self, mock_popen):
        # Test detection of Docker not running
        process_mock = MagicMock()
        attrs = {'communicate.return_value': ('docker is not running', ''), 'returncode': 1}
        process_mock.configure_mock(**attrs)
        mock_popen.return_value = process_mock

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
        with self.assertRaises(Exception) as context:
            DockerServiceManager.start_docker()
        self.assertIn("Failed to start Docker", str(context.exception))

if __name__ == '__main__':
    unittest.main()
