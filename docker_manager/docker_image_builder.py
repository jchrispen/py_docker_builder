from docker_manager.docker_utility import DockerUtility


class DockerImageBuilder:
    def __init__(self, config):
        self.config = config

    def list_images(self):
        """list docker images"""
        command = "docker images"
        error_msg = "Failed to list Docker images."
        DockerUtility.run_command_with_output(command, error_msg)

    def build_image(self):
        """Build a Docker image using configuration settings."""
        # set up variables
        log_file_path = self.config.get_config_value('log_file_path')
        image_name = self.config.get_config_value('image_name')
        format = self.config.get_config_value('tag_format')
        image_tag = DockerUtility.create_tag(format)
        image_name_tag = f"{image_name}:{image_tag}"
        docker_build_command = f"docker buildx build -t {image_name_tag} ."
        error_msg = "Docker build failed."

        # do work
        print(f"Building Docker image with tag: {image_name_tag}, logging to: {log_file_path}")
        # build the docker image
        DockerUtility.run_command_with_output(docker_build_command, error_msg, log_file=log_file_path)
        return image_name_tag
