#!/usr/bin/env python3

import argparse
from datetime import datetime
import json
import os
import shutil
import subprocess

class DockerConfig:
    def __init__(self, config_path):
        self.config = self.load_config(config_path)

    def load_config(self, config_path):
        """Loads configuration from a JSON file."""
        with open(config_path, 'r') as config_file:
            return json.load(config_file)

    def get_config_value(self, key):
        """Gets a specific configuration value."""
        return self.config.get(key, None)  # Returns None if key is not found

class DockerManager:
    def __init__(self, config):
        self.config = config

    def _check_dependencies(self):
        """Internal method to check for required dependencies."""
        dependencies = self.config.get_config_value('dependencies')
        missing_dependencies = []
        for dep in dependencies:
            if not shutil.which(dep):  # Using shutil.which to check for command availability
                missing_dependencies.append(dep)

        if missing_dependencies:
            raise Exception(f"Missing dependencies: {', '.join(missing_dependencies)}")
        else:
            print("All dependencies are satisfied.")

    def _check_required_files(self):
        """Internal method to check for required files."""
        required_files = self.config.get_config_value('required_files')
        missing_dependencies = []
        for file in required_files:
            if not os.path.isfile(file):  # Using shutil.which to check for command availability
                missing_dependencies.append(dep)

        if missing_dependencies:
            raise Exception(f"Missing required files: {', '.join(missing_dependencies)}")
        else:
            print("All required files are satisfied.")

    def _is_docker_running(self):
        """Internal method to check if the Docker service running."""
        process = subprocess.Popen(['service', 'docker', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate()
        return 'is running' in stdout or 'active (running)' in stdout

    def _start_docker(self):
        """Internal method to start the Docker service."""
        print("Docker is not running, attempting to start Docker...")
        result = subprocess.run(['sudo', 'service', 'docker', 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to start Docker. Error: {result.stderr}")

    def prepare_environment(self):
        """Public method that gets the env ready."""
        try:
            self._check_dependencies()
            self._check_required_files()
            if not self._is_docker_running():
                self._start_docker()
            else:
                print("Docker is already running.")
            # Additional setup or checks can go here
        except Exception as e:
            print(e)
            exit(1)

    def _run_command_with_output(self, command, error_message, check=True, log_file=None):
        """A specific wrapper to ensure output streaming."""
        self._run_command(command, error_message, check=check, stream_output=True, log_file=log_file)

    def _run_command(self, command, error_message, check=True, stream_output=False, log_file=None):
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if log_file:
            with open(log_file, 'w') as file:
                for output_line in process.stdout:
                    line = output_line.decode() if isinstance(output_line, bytes) else output_line
                    print(line.strip())
                    file.write(line)
        else:
            for output_line in process.stdout:
                line = output_line.decode() if isinstance(output_line, bytes) else output_line
                print(line.strip())

        exit_code = process.wait()
        if exit_code != 0 and check:
            raise Exception(f"Error: {error_message}")

    def list_containers(self):
        """list docker containers"""
        command = "docker ps -a"
        error_msg = "Failed to list Docker containers."
        self._run_command_with_output(command, error_msg)

    def list_images(self):
        """list docker images"""
        command = "docker images"
        error_msg = "Failed to list Docker images."
        self._run_command_with_output(command, error_msg)

    def _create_tag(self):
        format = self.config.get_config_value('tag_format')
        git_hash_cmd = "git rev-parse --short HEAD"
        # set timestamp for this build
        timestamp = datetime.now().strftime(format)
        # get the hash of this branch
        git_commit_hash = subprocess.getoutput(git_hash_cmd)
        if git_commit_hash:
            tag = f"{timestamp}-{git_commit_hash}"
        else:
            tag = f"{timestamp}"
        return tag

    def build_image(self):
        """Build a Docker image using configuration settings."""
        # Assume this method might need dependencies checked first
        self.prepare_environment()

        # set up variables
        log_file_path = self.config.get_config_value('log_file_path')
        image_name = self.config.get_config_value('image_name')
        image_tag = self._create_tag()
        image_name_tag = f"{image_name}:{image_tag}"
        docker_build_command = f"docker buildx build -t {image_name_tag} ."
        error_msg = "Docker build failed."

        # do work
        print(f"Building Docker image with tag: {image_name_tag}, logging to: {log_file_path}")
        # build the docker image
        self._run_command_with_output(docker_build_command, error_msg, log_file=log_file_path)
        return image_name_tag

    def create_container(self, image_name_tag):
        """Create a Docker container using supplied image name and configuration settings."""
        # Assume this method might need dependencies checked first
        self.prepare_environment()

        # set up variables
        if ':' in image_name_tag:
            name, tag = image_name_tag.split(':')
        else:
            name = image_name_tag
            tag = 'latest'  # Default tag if not specified

        log_file_path = self.config.get_config_value('log_file_path')
        container_name = self.config.get_config_value('container_name')
        container_name_tag = f"{container_name}-{tag}"
        docker_create_command = f"docker create -it --name {container_name_tag} {image_name_tag}"
        error_msg = "Failed to create Docker container."

        # do work
        print(f"Creating Docker container with tag: {container_name_tag}, logging to: {log_file_path}")
        # create the docker container
        self._run_command_with_output(docker_create_command, error_msg, log_file=log_file_path)


def main():
    parser = argparse.ArgumentParser(description="Docker Management Script")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file")

    args = parser.parse_args()
    config_path = args.config

    # Load the configuration
    docker_config = DockerConfig(config_path)
    # Initialize DockerManager with the loaded configuration
    docker_manager = DockerManager(docker_config)
    # build the docker image
    image_name_tag = docker_manager.build_image()
    # create the docker container
    docker_manager.create_container(image_name_tag)

    # 5x5
    print("Docker build completed successfully.")

if __name__ == '__main__':
    main()
