from datetime import datetime
import subprocess


class DockerUtility:

    @staticmethod
    def run_command_with_output(command, error_message, log_file_path=None):
        """A specific wrapper to ensure output streaming."""
        DockerUtility.run_command(command=command, error_message=error_message, check=True, stream_output=True, log_file_path=log_file_path)

    @staticmethod
    def run_command(command, error_message, check=True, stream_output=False, log_file_path=None):
        process = subprocess.Popen(command, shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        if log_file_path:
            with open(log_file_path, 'w') as file:
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

    @staticmethod
    def create_tag(date_format):
        git_hash_cmd = "git rev-parse --short HEAD"
        # set timestamp for this build
        timestamp = datetime.now().strftime(date_format)
        # get the hash of this branch
        git_commit_hash = subprocess.getoutput(git_hash_cmd)
        if git_commit_hash:
            tag = f"{timestamp}-{git_commit_hash}"
        else:
            tag = f"{timestamp}"
        return tag
