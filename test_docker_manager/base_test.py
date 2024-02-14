import unittest
import logging
import sys
from enum import IntEnum

from docker_manager.docker_config import DockerConfig
from docker_manager.docker_logging import DockerLogging


class BaseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()  # ensure proper initialization
        # function name enum
        cls.current = 0
        cls.parent = 1
        cls.grand_parent = 2
        cls.great_grand_parent = 3
        # end enum

    def setUp(self, initializer=None):
        super().setUp()  # ensure proper initialization
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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()  # ensure proper clean up

    def tearDown(self):
        super().tearDown()  # ensure proper clean up

    def _ppass(self, message=None, test_name=None):
        if test_name is not None:
            self.logger.log(f'TEST {test_name}')
        if message is not None:
            self.logger.log(message)
        self.logger.log('PASS')

    def _get_function_name(self, generation: int = 0) -> str:
        return sys._getframe(generation + 1).f_code.co_name

    @classmethod
    def _get_current_class_name(cls):
        """Returns the name of the current class."""
        return cls.__name__
