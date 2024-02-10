import unittest
import logging
import inspect

from docker_manager.docker_config import DockerConfig
from docker_manager.docker_logging import DockerLogging


class BaseTest(unittest.TestCase):
    def setUp(self, initializer=None):
        super().setUp()  # ensure proper initialization
        #
        config_dict = \
            {
                "custom_fields": {
                    'logging_enabled': False,
                    'verbose': True,
                    'log_file': 'test_log.txt',
                    'log_level': logging.DEBUG,
                    'initializer': initializer
                },
                "default_fields": {
                    "logging_enabled": {
                        "field_name": "logging_enabled",
                        "default_value": False,
                        "required": True
                    }
                }
            }
        self.docker_config = DockerConfig(config_dict=config_dict)
        self.logger = DockerLogging(self.docker_config)

    def tearDown(self):
        super().tearDown()  # ensure proper clean up

    def _ppass(self, message=None, test_name=None):
        if test_name is not None:
            self.logger.log(f'TEST {test_name}')
        if message is not None:
            self.logger.log(message)
        self.logger.log('PASS')

    def _get_current_function_name(self) -> str:
        """Returns the name of the current function."""
        # f_back goes one step back in the stack to the caller of this method
        # f_code contains code object information about the frame
        # co_name gives the name of the code object, which in this case is the caller's name
        return inspect.currentframe().f_back.f_code.co_name

    def _get_caller_function_name(self) -> str:
        """Returns the name of the caller function."""
        # f_back goes one step back in the stack to the caller of this method
        # f_back goes one step back in the stack to the caller of previous method
        # f_code contains code object information about the frame
        # co_name gives the name of the code object, which in this case is the caller's name
        return inspect.currentframe().f_back.f_back.f_code.co_name

    @classmethod
    def _get_current_class_name(cls):
        """Returns the name of the current class."""
        return cls.__name__
