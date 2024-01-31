#!/usr/bin/env python3

import unittest
# Import your test classes
from test_docker_manager.test_docker_config import TestDockerConfig
from test_docker_manager.test_docker_container_manager import TestDockerContainerManager
from test_docker_manager.test_docker_dependency_checker import TestDockerDependencyChecker
from test_docker_manager.test_docker_image_builder import TestDockerImageBuilder
from test_docker_manager.test_docker_service_manager import TestDockerServiceManager
from test_docker_manager.test_docker_utility import TestDockerUtility


class DockerTestSuite:
    def __init__(self):
        self.loader = unittest.TestLoader()
        self.suite = unittest.TestSuite()
        self.add_tests()

    def add_tests(self):
        self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerConfig))
        self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerContainerManager))
        self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerDependencyChecker))
        self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerImageBuilder))
        # self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerServiceManager))
        # self.suite.addTests(self.loader.loadTestsFromTestCase(TestDockerUtility))

    def run(self):
        runner = unittest.TextTestRunner()
        runner.run(self.suite)


if __name__ == '__main__':
    test_suite = DockerTestSuite()
    test_suite.run()
