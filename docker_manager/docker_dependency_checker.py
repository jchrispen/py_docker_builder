import os
import shutil
from docker_manager.docker_service_manager import DockerServiceManager


class DockerDependencyChecker:

    def __init__(self, config):
        self.config = config
        self.os_dependencies = 'os_dependencies'
        self.config_files_dir = 'config_files_dir'
        self.required_config_files = 'required_config_files'

    def _check_dependencies(self):
        """Internal method to check for required dependencies."""
        dependencies = self.config.get_config_value(self.os_dependencies)
        missing_dependencies = []
        for dep in dependencies:
            if not shutil.which(dep):  # Using shutil.which to check for command availability
                missing_dependencies.append(dep)

        if missing_dependencies:
            raise Exception(f"Missing dependencies: {', '.join(missing_dependencies)}")

    def _check_required_files(self):
        """Internal method to check for required files."""
        config_dir = self.config.get_config_value(self.config_files_dir)
        required_files = self.config.get_config_value(self.required_config_files)
        missing_files = []
        for file in required_files:
            if not os.path.isfile(f"{config_dir}/{file}"):  # Using shutil.which to check for command availability
                missing_files.append(file)

        if missing_files:
            raise Exception(f"Missing required files: {', '.join(missing_files)}")

    def prepare_environment(self):
        """Public method that gets the env ready."""
        try:
            self._check_dependencies()
            self._check_required_files()
            if not DockerServiceManager.is_docker_running():
                DockerServiceManager.start_docker()
            # Additional setup or checks can go here
        except Exception as e:
            print(e)
            exit(1)
