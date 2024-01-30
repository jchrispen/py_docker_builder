#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import sys
from enum import Enum
from docker_manager.docker_config import DockerConfig
from docker_manager.docker_container_manager import DockerContainerManager
from docker_manager.docker_dependency_checker import DockerDependencyChecker
from docker_manager.docker_image_builder import DockerImageBuilder
from test_docker_manager.test_runner import TestRunner


# Usage:
# ExitCodes.SUCCESS.value, ExitCodes.FAIL.value
class ExitCodes(Enum):
    SUCCESS = 0
    FAIL = 1
    # You can add more specific error codes if needed


class BuilderArgumentParser:
    def __init__(self):
        _description = "Docker Management Script"
        self.parser = ArgumentParser(description=_description)
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument("-c", "--config", help="Path to the configuration file")
        self.parser.add_argument("-v", "--verbose", action='store_true', help="Enable output")
        self.parser.add_argument("-l", "--logging", action='store_true', help="Enable logging")
        self.parser.add_argument("--build-image", nargs='?', const='Dockerfile',
                                 help="Build Docker image, optionally specify a Dockerfile path")
        self.parser.add_argument("--create-container", action='store_true', help="Create Docker container")
        self.parser.add_argument('--run-tests', action='store_true', help='Run unit tests')

    def parse_args(self):
        # Parse and return the arguments
        return self.parser.parse_args()


def parse_arguments():
    parser = BuilderArgumentParser()
    return parser.parse_args()


def load_configuration_file(args):
    if args.config:
        try:
            with open(args.config, 'r') as config_file:
                config_json = json.load(config_file)
            config_json['verbose'] = args.verbose
            config_json['logging'] = args.logging
            if args.build_image and isinstance(args.build_image, str):
                config_json['dockerfile'] = args.build_image
            return config_json
        except Exception as e:
            print(f"Error reading config file: {e}")
            sys.exit(ExitCodes.FAIL.value)


def execute_main_logic(args, config_json):
    try:
        if not args.run_tests:
            # init the module
            docker_config = DockerConfig(config_dict=config_json)
            dependency_checker = DockerDependencyChecker(docker_config)
            dependency_checker.prepare_environment()

            image_name_tag = None
            if args.build_image or args.create_container:
                image_builder = DockerImageBuilder(docker_config)
                image_name_tag = image_builder.build_image()

                if image_name_tag is not None:
                    print("Docker image built successfully.")

            if args.create_container:
                if image_name_tag is not None:
                    container_manager = DockerContainerManager(docker_config)
                    container_manager.create_container(image_name_tag)
                    print("Docker container created successfully.")
                else:
                    print("Error: Docker image needs to be built before creating a container.")
                    sys.exit(ExitCodes.FAIL.value)

        if args.run_tests:
            test_suite = TestRunner()
            test_suite.run()

    except Exception as e:
        print(f"Error during Docker operations: {e}")
        sys.exit(ExitCodes.FAIL.value)


def main():
    args = parse_arguments()

    # Check if --config is provided when --run-tests is not flagged
    if not args.run_tests and not args.config:
        print("Error: --config is required if not running tests")
        sys.exit(ExitCodes.FAIL.value)

    config_json = load_configuration_file(args)
    execute_main_logic(args, config_json)

    print("Docker build and create script completed successfully.")
    sys.exit(ExitCodes.SUCCESS.value)


if __name__ == '__main__':
    main()
