from docker_manager.docker_utility import DockerUtility
from docker.errors import BuildError, APIError
import docker


class DockerImageBuilder:
    def __init__(self, config):
        self.config = config
        self.client = docker.from_env()

    def list_images(self):
        """List Docker images."""
        try:
            return self.client.images.list()
        except docker.errors.APIError as e:
            return None

    def build_image(self):
        """Build a Docker image using configuration settings."""
        try:
            image_name = self.config.get_config_value('image_name')
            tag_format = self.config.get_config_value('tag_format')
            # Assuming create_tag is a method that creates a tag based on the given format
            image_tag = DockerUtility.create_tag(tag_format)
            dockerfile = self.config.get_config_value('dockerfile')
            image_path = '.'  # Assuming the context is the current directory

            # Build the docker image
            image, build_logs = self.client.images.build(path=image_path, dockerfile=dockerfile,
                                                         tag=f"{image_name}:{image_tag}")
            return f"{image_name}:{image_tag}"
        except BuildError as e:
            return None
        except APIError as e:
            return None
