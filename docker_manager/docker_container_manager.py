from docker.models.containers import Container
from docker.errors import DockerException
import docker

from docker_manager.docker_logging import DockerLogging


class DockerContainerManager:
    def __init__(self, config):
        self.client = docker.from_env()
        self.config = config
        self.default_tag = 'latest'
        self.container_name = config.get_custom_config_value('container_name', use_default=True)
        # let the logger know it's us
        self.config.add_custom_value('initializer', __class__.__name__)
        self.logger = DockerLogging(config)

    def list_containers(self) -> [Container]:
        """List Docker containers."""
        try:
            return self.client.containers.list(all=True)
        except DockerException as e:
            print(f"Failed to list Docker containers: {e}")
            return []

    def create_container(self, image_name_tag: str) -> Container:
        """Create a Docker container using the supplied image name and configuration settings."""
        # set up variables
        if ':' in image_name_tag:
            name, tag = image_name_tag.split(':')
        else:
            name = image_name_tag
            tag = self.default_tag  # Default tag if not specified

        # container_name = self.config.get_custom_config_value(self.container_name, use_default=True)
        container_name_tag = f"{self.container_name}-{tag}"

        self.logger.log(f"{container_name_tag}")

        try:
            return self.client.containers.create(image_name_tag, name=container_name_tag, detach=True, tty=True)
        except DockerException as e:
            self.logger.log(f"Failed to create Docker container: {e}")
            return None
