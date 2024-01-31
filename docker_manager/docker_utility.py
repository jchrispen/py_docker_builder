from datetime import datetime
import subprocess


class DockerUtility:

    @staticmethod
    def run_command_with_output(command, error_message, log_file_path=None):
        """Run a command and stream its output."""
        DockerUtility.run_command(command=command, error_message=error_message, check=True, stream_output=True, log_file_path=log_file_path)

    @staticmethod
    def run_command(command, error_message, check=True, stream_output=False, log_file_path=None):
        """Run a command and handle its output."""
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = process.communicate()

        if log_file_path is not None:
            with open(log_file_path, 'w') as file:
                file.write(stdout)
                if stderr:
                    file.write(stderr)

        if stream_output:
            print(stdout.strip())

        if process.returncode != 0 and check:
            raise Exception(f"Error: {error_message}\n{stderr}")

    @staticmethod
    def create_tag(date_format):
        """Create a tag using the current date and git commit hash."""
        git_hash_cmd = ["git", "rev-parse", "--short", "HEAD"]
        timestamp = datetime.now().strftime(date_format)
        process = subprocess.Popen(git_hash_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        git_commit_hash, _ = process.communicate()

        if git_commit_hash:
            return f"{timestamp}-{git_commit_hash.strip()}"
        else:
            return timestamp
