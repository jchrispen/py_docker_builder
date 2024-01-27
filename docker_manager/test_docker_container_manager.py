import unittest
from unittest.mock import patch
from docker_container_manager import DockerContainerManager

class TestDockerContainerManager(unittest.TestCase):

    def setUp(self):
        # Mock configuration for DockerContainerManager
        self.mock_config = {'log_file_path': '/path/to/log', 'container_name': 'test_container'}
        self.docker_container_manager = DockerContainerManager(self.mock_config)

    @patch('docker_manager.docker_utility.DockerUtility.run_command_with_output')
    def test_list_containers_success(self, mock_run_command):
        # Test successful listing of Docker containers
        mock_run_command.return_value = None  # Simulate successful command execution
        self.docker_container_manager.list_containers()
        mock_run_command.assert_called_with("docker ps -a", "Failed to list Docker containers.")

    @patch('docker_manager.docker_utility.DockerUtility.run_command_with_output')
    def test_create_container_success(self, mock_run_command):
        # Test successful creation of a Docker container
        mock_run_command.return_value = None  # Simulate successful command execution
        self.docker_container_manager.create_container('image_name:tag')
        expected_command = "docker create -it --name test_container-tag image_name:tag"
        mock_run_command.assert_called_with(expected_command, "Failed to create Docker container.")

    # Additional tests can be added for failure scenarios and edge cases

if __name__ == '__main__':
    unittest.main()
