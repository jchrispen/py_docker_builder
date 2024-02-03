import logging

from docker_manager.docker_utility import DockerUtility
from docker.errors import BuildError, APIError
from docker_manager.docker_logging import DockerLogging
import docker


class DockerImageBuilder:
    def __init__(self, docker_config):
        self.config = docker_config
        # let the logger know it's us
        self.config.add_custom_value('initializer', __class__.__name__)
        self.logging = DockerLogging(docker_config)

    def list_images(self):
        """List Docker images."""
        try:
            client = docker.from_env()
            image_list = client.images.list()
            for item in image_list:
                self.logging.log(f'Docker image: {item}')
            return image_list
        except APIError as e:
            return None

    def build_image(self):
        """Build a Docker image using configuration settings."""
        try:
            image_name = self.config.get_custom_config_value('image_name', use_default=True)
            tag_format = self.config.get_custom_config_value('tag_format', use_default=True)
            # Assuming create_tag is a method that creates a tag based on the given format
            image_tag = DockerUtility.create_tag(tag_format)
            dockerfile = self.config.get_custom_config_value('dockerfile', use_default=True)
            image_path = '.'  # Assuming the context is the current directory
            image_name_tag = f"{image_name}:{image_tag}"

            # Build the docker image
            client = docker.from_env()
            image, build_logs, *rest = client.images.build(path=image_path, dockerfile=dockerfile, tag=image_name_tag)

            # display and or log the build logs
            for line in build_logs:
                self.logging.log(f'Docker image: {line}')

            self.logging.log(f'image:tag: {image_name_tag}')
            return image_name_tag
        except BuildError as e:
            self.logging.log(f'Build Error: {e}', level=logging.ERROR)
            return None
        except APIError as e:
            self.logging.log(f'API Error: {e}', level=logging.ERROR)
            return None
