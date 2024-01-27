import os
import shutil
from docker_service_manager import DockerServiceManager


class DockerDependencyChecker:

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
        missing_files = []
        for file in required_files:
            if not os.path.isfile(file):  # Using shutil.which to check for command availability
                missing_files.append(dep)

        if missing_files:
            raise Exception(f"Missing required files: {', '.join(missing_files)}")
        else:
            print("All required files are satisfied.")

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
