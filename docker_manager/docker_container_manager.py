from docker_manager.docker_utility import DockerUtility


class DockerContainerManager:

    def __init__(self, config):
        self.config = config
        self.default_tag = 'latest'
        self.log_file_name = 'log_file_path'
        self.container_name = 'container_name'

    def list_containers(self):
        """list docker containers"""
        command = "docker ps -a"
        error_msg = "Failed to list Docker containers."
        DockerUtility.run_command_with_output(command, error_msg)

    def create_container(self, image_name_tag):
        """Create a Docker container using supplied image name and configuration settings."""
        # set up variables
        if ':' in image_name_tag:
            name, tag = image_name_tag.split(':')
        else:
            name = image_name_tag
            tag = self.default_tag  # Default tag if not specified

        log_file_path = self.config.get_config_value(self.log_file_name)
        container_name = self.config.get_config_value(self.container_name)
        container_name_tag = f"{container_name}-{tag}"
        docker_create_command = f"docker create -it --name {container_name_tag} {image_name_tag}"
        error_msg = "Failed to create Docker container."

        # create the docker container
        DockerUtility.run_command_with_output(docker_create_command, error_msg, log_file_path)
