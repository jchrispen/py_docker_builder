import logging
import os
import sys


class DockerLogging:
    """Handles logging to file and or stdout"""
    def __init__(self, docker_config):
        self.config = docker_config
        self.log_file_path = self.config.get_custom_config_value('log_file', use_default=True)
        self.log_level = self.config.get_custom_config_value('log_level', use_default=True)
        self.log_enabled = self.config.get_custom_config_value('logging_enabled', use_default=True)
        self.verbose_enabled = self.config.get_custom_config_value('verbose', use_default=True)
        self.initializer = self.config.get_custom_config_value('initializer', use_default=True)
        self.logger = None
        self.setup_logging()
        # let logging begin
        if self.initializer.startswith('TestDocker'):
                self.log('')
        self.log(f'DockerLogging initialized by {self.initializer}')

    def setup_logging(self):
        if not self.log_enabled:
            return

        if os.path.dirname(self.log_file_path) != '':
            if not os.path.exists(os.path.dirname(self.log_file_path)):
                os.makedirs(os.path.dirname(self.log_file_path))
        logging.basicConfig(filename=self.log_file_path, level=self.log_level,
                            format='%(asctime)s %(levelname)s:%(message)s')
        self.logger = logging.getLogger(__name__)

    def print_message(self, message, level):
        if not self.verbose_enabled:
            return

        # Define a mapping of logging levels to corresponding print actions
        action = {
            logging.DEBUG: lambda msg: print(msg),
            logging.INFO: lambda msg: print(msg),
            logging.WARNING: lambda msg: print(msg),
            logging.ERROR: lambda msg: print(msg, file=sys.stderr)
        }.get(level, lambda msg: print(msg, file=sys.stderr))  # Default action

        # Execute the corresponding action
        action(message)

    def log_message(self, message, level):
        if not self.log_enabled:
            return

        # Define a mapping of logging levels to corresponding log actions
        action = {
            logging.DEBUG: lambda msg: self.logger.debug(msg),
            logging.WARNING: lambda msg: self.logger.warning(msg),
            logging.ERROR: lambda msg: self.logger.error(msg, file=sys.stderr)
        }.get(level, lambda msg: self.logger.info(msg))  # Default action

        # Execute the corresponding action
        action(message)

    def log(self, message, level=logging.INFO):
        self.print_message(message, level)
        self.log_message(message, level)
