#!/usr/bin/env python3

import argparse
from docker_manager.docker_config import DockerConfig
from docker_manager.docker_container_manager import DockerContainerManager
from docker_manager.docker_dependency_checker import DockerDependencyChecker
from docker_manager.docker_image_builder import DockerImageBuilder
from docker_manager.docker_service_manager import DockerServiceManager


def main():
    parser = argparse.ArgumentParser(description="Docker Management Script")
    parser.add_argument("-c", "--config", required=True, help="Path to the configuration file")

    args = parser.parse_args()
    config_path = args.config

    # Initialize the new classes
    docker_config = DockerConfig(config_path)
    dependency_checker = DockerDependencyChecker(docker_config)
    service_manager = DockerServiceManager(docker_config)
    image_builder = DockerImageBuilder(docker_config)
    container_manager = DockerContainerManager(docker_config)

    # Get ready to work
    dependency_checker.prepare_environment()
    if not service_manager.is_docker_running():
        service_manager.start_docker()

    # do work
    image_name_tag = image_builder.build_image()
    container_manager.create_container(image_name_tag)

    # 5x5
    print("Docker build completed successfully.")

if __name__ == '__main__':
    main()
