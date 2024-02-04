from docker_manager.docker_utility import DockerUtility
from docker.errors import BuildError, APIError
from docker_manager.docker_logging import DockerLogging
import logging
import docker
import os


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
            config_files_dir = self.config.get_custom_config_value('config_files_dir', use_default=True)
            image_build_path = os.path.join(os.getcwd(), config_files_dir)
            # Configure variables used in the Dockerfile
            ubuntu_buildargs = {
                'base_image': 'ubuntu',
                'base_version': '20.04'
            }

            # Validate image name and tag
            if not image_name or '/' in image_name or not image_tag:
                raise ValueError("Invalid image name or tag format.")

            image_name_tag = f"{image_name}:{image_tag}"
            self.logging.log(f"Building image with name:tag {image_name_tag}")

            '''
            def build(self, path=None, tag=None, quiet=False, fileobj=None,
                      nocache=False, rm=False, timeout=None,
                      custom_context=False, encoding=None, pull=False,
                      forcerm=False, dockerfile=None, container_limits=None,
                      decode=False, buildargs=None, gzip=False, shmsize=None,
                      labels=None, cache_from=None, target=None, network_mode=None,
                      squash=None, extra_hosts=None, platform=None, isolation=None,
                      use_config_proxy=True):
            '''
            # Build the docker image
            client = docker.from_env()
            image, build_logs, *rest = client.images.build(path=image_build_path,
                                                           dockerfile=dockerfile,
                                                           tag=image_name_tag,
                                                           buildargs=ubuntu_buildargs,
                                                           squash=False)

            # display and or log the build logs
            for line in build_logs:
                self.logging.log(line)

            self.logging.log(f"Successfully built {image_name_tag}")
            return image_name_tag
        except BuildError as e:
            self.logging.log(f'Build Error: {e}', level=logging.ERROR)
            return None
        except APIError as e:
            self.logging.log(f'API Error: {e}', level=logging.ERROR)
            return None
        except TypeError as e:
            self.logging.log(f'Type Error: {e}', level=logging.ERROR)
            return None
        except ValueError as e:
            self.logging.log(f'Value Error: {e}', level=logging.ERROR)
            return None
