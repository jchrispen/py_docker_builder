#!/usr/bin/env python3

import unittest
# Import your test classes
from test_docker_manager.test_docker_config import TestDockerConfig
from test_docker_manager.test_docker_container_manager import TestDockerContainerManager
from test_docker_manager.test_docker_dependency_checker import TestDockerDependencyChecker
from test_docker_manager.test_docker_image_builder import TestDockerImageBuilder
from test_docker_manager.test_docker_service_manager import TestDockerServiceManager
from test_docker_manager.test_docker_utility import TestDockerUtility


class TestRunner:
    def __init__(self):
        self.suite = unittest.TestSuite()
        self.add_tests()

    def add_tests(self):
        self.suite.addTest(unittest.makeSuite(TestDockerConfig))
        self.suite.addTest(unittest.makeSuite(TestDockerContainerManager))
        self.suite.addTest(unittest.makeSuite(TestDockerDependencyChecker))
        self.suite.addTest(unittest.makeSuite(TestDockerImageBuilder))
        self.suite.addTest(unittest.makeSuite(TestDockerServiceManager))
        self.suite.addTest(unittest.makeSuite(TestDockerUtility))

    def run(self):
        runner = unittest.TextTestRunner()
        runner.run(self.suite)


if __name__ == '__main__':
    test_suite = DockerTestSuite()
    test_suite.run()
