import subprocess


class DockerServiceManager:
    def __init__(self, config):
        self.config = config

    def is_docker_running(self):
        """Internal method to check if the Docker service running."""
        process = subprocess.Popen(['service', 'docker', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, _ = process.communicate()
        return 'is running' in stdout or 'active (running)' in stdout

    def start_docker(self):
        """Internal method to start the Docker service."""
        print("Docker is not running, attempting to start Docker...")
        result = subprocess.run(['sudo', 'service', 'docker', 'start'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if result.returncode != 0:
            raise Exception(f"Failed to start Docker. Error: {result.stderr}")
