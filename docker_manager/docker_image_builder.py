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
        """Build a Docker image using configuration settings and stream logs to console."""
        try:
            image_name = self.config.get_custom_config_value('image_name', use_default=True)
            tag_format = self.config.get_custom_config_value('tag_format', use_default=True)
            image_tag = DockerUtility.create_tag(tag_format)
            dockerfile = self.config.get_custom_config_value('dockerfile', use_default=True)
            image_build_path = os.getcwd()
            ubuntu_buildargs = self.config.get_custom_config_value('buildargs', use_default=True)

            if not image_name or '/' in image_name or not image_tag:
                raise ValueError("Invalid image name or tag format.")

            image_name_tag = f"{image_name}:{image_tag}"
            self.logging.log(f"Building image with name:tag {image_name_tag}")
            self.logging.log(f"Building image with Dockerfile: {dockerfile}")

            client = docker.from_env()
            # Note: No 'decode' attribute is manually accessed here.
            # The 'decode=True' argument ensures the build logs are automatically decoded.
            _, build_logs = client.images.build(path=image_build_path,
                                                tag=f"{image_name}:{image_tag}",
                                                dockerfile=dockerfile,
                                                rm=True,
                                                buildargs=ubuntu_buildargs)

            # Process and print build logs in real-time
            for log_entry in build_logs:  # Iterate through the generator of log entries
                if 'stream' in log_entry:
                    log_line = log_entry['stream'].strip()
                    self.logging.log(log_line)
                elif 'error' in log_entry:  # Handling potential error messages in the logs
                    error_message = log_entry['error'].strip()
                    self.logging.log(error_message, level=logging.ERROR)
                    break  # Exit loop on error to stop processing further logs

            # Prune dangling images
            pruned = client.images.prune(filters={'dangling': True})
            # Output the amount of reclaimed space
            self.logging.log(f"Reclaimed space: {pruned['SpaceReclaimed']} bytes")

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
