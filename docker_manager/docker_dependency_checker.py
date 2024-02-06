import os
import shutil
from docker_manager.docker_service_manager import DockerServiceManager

from docker_manager.docker_logging import DockerLogging


class DockerDependencyChecker:

    def __init__(self, config):
        self.config = config
        self.os_dependencies = config.get_default_config_name('os_dependencies')
        self.config_files_dir = config.get_default_config_name('config_files_dir')
        self.required_config_files = config.get_default_config_name('required_config_files')
        # let the logger know it's us
        self.config.add_custom_value('initializer', __class__.__name__)
        self.logging = DockerLogging(config)

    def _check_dependencies(self):
        """Internal method to check for required dependencies."""
        dependencies = self.config.get_custom_config_value(self.os_dependencies, use_default=True)

        # No os_dependencies, no check needed
        if dependencies is None or len(dependencies) == 0:
            return

        missing_dependencies = []
        for dep in dependencies:
            if not shutil.which(dep):  # Using shutil.which to check for command availability
                missing_dependencies.append(dep)

        if missing_dependencies:
            raise Exception(f"Missing dependencies: {', '.join(missing_dependencies)}")

    def _check_required_files(self):
        """Internal method to check for required files."""
        config_dir = self.config.get_custom_config_value(self.config_files_dir, use_default=True)
        required_files = self.config.get_custom_config_value(self.required_config_files, use_default=True)

        # No required_files, no check needed
        if required_files is None or len(required_files) == 0:
            return

        missing_files = []

        for file in required_files:
            # Check if the file already starts with config_dir and adjust accordingly
            if config_dir is None or file.startswith(config_dir):
                req_file = file
            else:
                req_file = os.path.join(config_dir, file)

            if not os.path.isfile(req_file):
                missing_files.append(file)

        if missing_files:
            raise FileNotFoundError(f"Missing required files: {', '.join(missing_files)}")

    def prepare_environment(self):
        """Public method that gets the env ready."""
        try:
            self._check_dependencies()
            self._check_required_files()
            # ensure the docker service is up and running
            if not DockerServiceManager.is_docker_running():
                DockerServiceManager.start_docker()
            # Additional setup or checks can go here
        except Exception as e:
            print(e)
            exit(1)
