#!/usr/bin/env python3

from argparse import ArgumentParser
import json
import sys
from docker_manager.docker_config import DockerConfig
from docker_manager.docker_container_manager import DockerContainerManager
from docker_manager.docker_dependency_checker import DockerDependencyChecker
from docker_manager.docker_image_builder import DockerImageBuilder
from test_docker_manager.test_runner import TestRunner


class BuilderArgumentParser:
    def __init__(self):
        _description = 'Docker Management Script'
        self.parser = ArgumentParser(description=_description)
        self._setup_arguments()

    def _setup_arguments(self):
        self.parser.add_argument('-c', '--config', help='Path to the configuration file')
        self.parser.add_argument('-v', '--verbose', action='store_true', help='Enable output')
        self.parser.add_argument('-l', '--logging', action='store_true', help='Enable logging')
        self.parser.add_argument('-b', '--build-image', nargs='?', const='Dockerfile',
                                 help='Build Docker image, optionally specify a Dockerfile path')
        self.parser.add_argument('-cc', '--create-container', action='store_true', help='Create Docker container')
        self.parser.add_argument('-t', '--run-tests', action='store_true', help='Run unit tests')

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
                # Make sure 'required_config_files' is in the JSON
                req_files = 'required_config_files'
                if req_files not in config_json:
                    config_json[req_files] = []
                # Append 'build_image' to 'required_config_files' if it's not already in the list
                if args.build_image not in config_json[req_files]:
                    config_json[req_files].append(args.build_image)

            return config_json
        except Exception as e:
            raise ValueError(f'Error reading config file: {e}')


def build_image(docker_config):
    image_builder = DockerImageBuilder(docker_config)
    return image_builder.build_image()


def create_container(image_name_tag, docker_config):
    container_manager = DockerContainerManager(docker_config)
    container_manager.create_container(image_name_tag)


def run_tests():
    test_suite = TestRunner()
    test_suite.run()


def execute_main_logic(args, config_json):
    # init the module
    docker_config = DockerConfig(config_dict=config_json)
    dependency_checker = DockerDependencyChecker(docker_config)
    dependency_checker.prepare_environment()

    image_name_tag = None
    if args.build_image or args.create_container:
        image_name_tag = build_image(docker_config)
    if args.create_container:
        create_container(image_name_tag, docker_config)


def main():
    args = parse_arguments()
    EX_OK = 0
    EX_FAIL = 1

    # Check if --config is provided when --run-tests is not flagged
    if not args.run_tests and not args.config:
        print('Error: --config is required if not running tests')
        sys.exit(EX_FAIL)

    try:
        if args.run_tests:
            run_tests()
        else:
            config_json = load_configuration_file(args)
            execute_main_logic(args, config_json)

    except Exception as e:
        print(f'Error during Docker operations: {e}')
        sys.exit(EX_FAIL)

    print('Docker build and create script completed')
    sys.exit(EX_OK)


if __name__ == '__main__':
    main()
