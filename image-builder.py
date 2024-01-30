#!/usr/bin/env python3

from argparse import ArgumentParser
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
            config = DockerConfig(args.config)

            # setup default field names
            # note, these fields can be None
            verbose = config.get_default_config_name('verbose')
            logging_enabled = config.get_default_config_name('logging_enabled')
            log_file = config.get_default_config_name('log_file')
            log_level = config.get_default_config_name('log_level')
            dockerfile = config.get_default_config_name('dockerfile')
            required_config_files = config.get_default_config_name('required_config_files')

            config.add_custom_value(verbose, args.verbose)
            config.add_custom_value(logging_enabled, args.logging)

            if args.logging:
                if isinstance(args.logging, str):
                    config.add_custom_value(log_file, args.logging)

            if args.build_image and isinstance(args.build_image, str):
                config.add_custom_value(dockerfile, args.build_image)
                # Append 'build_image' to 'required_config_files'
                config.add_custom_value(required_config_files, [args.build_image])

            return config
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


def execute_main_logic(args, docker_config):
    # init the module
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
            docker_config = load_configuration_file(args)
            execute_main_logic(args, docker_config)

    except Exception as e:
        print(f'Error during Docker operations: {e}')
        sys.exit(EX_FAIL)

    sys.exit(EX_OK)


if __name__ == '__main__':
    main()
